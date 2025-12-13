#!/usr/bin/env python3
"""
Inspect and summarize AIBE MongoDB data sources for analysis.

This script connects to Mongo using the AIBE server's config and reports:
- Stories (AIBE.<collection>) structure stats: stories, paragraphs, sentences, words, events
- Server Streams (server_streams.server_YYYYMMDD_###) event stats by stream/type/session

Outputs a concise Markdown + JSON summary to stdout and optional files.

USAGE (run locally where Mongo is accessible):
  python server/tools/inspect_streams.py \
    --samples 3 \
    --write ./stream_summary.md ./stream_summary.json

Notes:
- Uses the AIBE config at ~/.AIBE/config.json if present.
- You can override Mongo with --mongo-uri if needed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Local imports: allow running from repo root
import sys
REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_DIR = REPO_ROOT / "server"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

try:
    from aibe_server.config_manager import get_config_manager
except Exception:
    get_config_manager = None

from pymongo import MongoClient


def load_config_overrides(args) -> Tuple[str, str, str, str]:
    """Resolve Mongo connection string and DB/collection names.

    Returns: (mongo_uri, stories_db, stories_collection, streams_db)
    """
    # Defaults consistent with codebase
    default_uri = "mongodb://localhost:27017/AIBE"
    stories_db = "AIBE"
    stories_collection = "Stories"
    streams_db = "server_streams"

    if get_config_manager is not None:
        try:
            cfg = get_config_manager().get_config()
            default_uri = cfg.database.connection_string or default_uri
            stories_db = cfg.database.database_name or stories_db
            stories_collection = cfg.database.collection_name or stories_collection
            # server_streaming is for live streams; we use its database field name
            streams_db = getattr(cfg.server_streaming, "database", streams_db) or streams_db
        except Exception:
            pass

    # Allow CLI override
    mongo_uri = args.mongo_uri or os.getenv("AIBE_MONGO_URI") or default_uri
    if args.stories_db:
        stories_db = args.stories_db
    if args.stories_collection:
        stories_collection = args.stories_collection
    if args.streams_db:
        streams_db = args.streams_db

    return mongo_uri, stories_db, stories_collection, streams_db


def redact_value(value: Any) -> Any:
    """Redact potentially sensitive values conservatively."""
    if isinstance(value, str):
        # Mask emails and long alphanumerics
        if re.search(r"[\w.\-+]+@[\w\-]+\.[\w\-.]+", value):
            return "[redacted-email]"
        if len(value) > 40:
            return value[:20] + "…[redacted]…" + value[-5:]
    return value


def sanitize_event(doc: Dict[str, Any]) -> Dict[str, Any]:
    doc = dict(doc)
    doc.pop("_id", None)
    # Common fields
    if "data" in doc and isinstance(doc["data"], dict):
        d = dict(doc["data"])
        for k in list(d.keys()):
            if k.lower() in {"value", "password", "token", "authorization"}:
                d[k] = "[redacted]"
            else:
                d[k] = redact_value(d[k])
        doc["data"] = d
    if "target" in doc and isinstance(doc["target"], dict):
        t = dict(doc["target"])
        for k in list(t.keys()):
            if k.lower() in {"value", "password"}:
                t[k] = "[redacted]"
            else:
                t[k] = redact_value(t[k])
        doc["target"] = t
    return doc


def summarize_stories(client: MongoClient, stories_db: str, stories_coll: str, sample_n: int) -> Dict[str, Any]:
    db = client[stories_db]
    col = db[stories_coll]
    count = col.estimated_document_count()

    metrics = {
        "stories_total": count,
        "paragraphs_per_story": [],
        "sentences_per_paragraph": [],
        "words_per_sentence": [],
        "events_per_word": [],
        "samples": [],
    }

    cursor = col.find({}).sort("updated_at", -1) if count else []
    for idx, doc in enumerate(cursor):
        if idx >= max(sample_n, 10):
            break
        story = dict(doc)
        story.pop("_id", None)

        # Traverse structure
        paragraphs = story.get("paragraphs", []) or []
        metrics["paragraphs_per_story"].append(len(paragraphs))
        if idx < sample_n:
            # Take a small slice of structure for sampling
            sample = {
                "session_id": story.get("session_id"),
                "paragraphs": [],
                "created": story.get("created_at"),
                "updated": story.get("updated_at"),
            }
        for p in paragraphs[:2]:
            sentences = p.get("sentences", []) or []
            metrics["sentences_per_paragraph"].append(len(sentences))
            if idx < sample_n:
                s_sample = {"domain": p.get("domain"), "sentences": []}
            for s in sentences[:2]:
                words = s.get("words", []) or []
                metrics["words_per_sentence"].append(len(words))
                if idx < sample_n:
                    w_sample = []
                for w in words[:2]:
                    events = w.get("events", []) or []
                    metrics["events_per_word"].append(len(events))
                    if idx < sample_n:
                        w_sample.append({
                            "events": [sanitize_event(e) for e in events[:2]],
                            "screen_status": sanitize_event(w.get("screen_status", {})) if w.get("screen_status") else None,
                        })
                if idx < sample_n:
                    s_sample["sentences"].append({
                        "url": s.get("url"),
                        "words": w_sample,
                    })
            if idx < sample_n:
                sample["paragraphs"].append(s_sample)
        if idx < sample_n:
            metrics["samples"].append(sample)

    def avg(lst: List[int]) -> float:
        return round(sum(lst) / len(lst), 2) if lst else 0.0

    summary = {
        "stories_total": metrics["stories_total"],
        "avg_paragraphs_per_story": avg(metrics["paragraphs_per_story"]),
        "avg_sentences_per_paragraph": avg(metrics["sentences_per_paragraph"]),
        "avg_words_per_sentence": avg(metrics["words_per_sentence"]),
        "avg_events_per_word": avg(metrics["events_per_word"]),
        "samples": metrics["samples"],
    }
    return summary


def latest_streams_collection(client: MongoClient, streams_db: str) -> str | None:
    db = client[streams_db]
    names = db.list_collection_names()
    # Pick collections like server_YYYYMMDD_### and choose max by lexicographic order
    candidates = [n for n in names if re.match(r"^server_\d{8}_\d{3}$", n)]
    return sorted(candidates)[-1] if candidates else (names[-1] if names else None)


def summarize_streams(client: MongoClient, streams_db: str, collection: str | None, sample_n: int) -> Dict[str, Any]:
    db = client[streams_db]
    coll_name = collection or latest_streams_collection(client, streams_db)
    if not coll_name:
        return {"collections": [], "note": "No stream collections found"}

    col = db[coll_name]
    total = col.estimated_document_count()

    by_stream = Counter()
    by_type = Counter()
    by_session = Counter()
    samples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    # Sample most recent N docs
    cursor = col.find({}).sort("timestamp", -1).limit(max(sample_n * 20, 200)) if total else []
    for doc in cursor:
        stream = doc.get("stream", "Unknown")
        evt_type = doc.get("type") or doc.get("data", {}).get("type") or "Unknown"
        session_id = doc.get("session_id", "Unknown")
        by_stream[stream] += 1
        by_type[evt_type] += 1
        by_session[session_id] += 1
        if len(samples[stream]) < sample_n:
            samples[stream].append(sanitize_event(doc))

    return {
        "collection": coll_name,
        "total": total,
        "by_stream": by_stream.most_common(),
        "by_type": by_type.most_common(20),
        "top_sessions": by_session.most_common(10),
        "samples": samples,
    }


def to_markdown(stories: Dict[str, Any], streams: Dict[str, Any]) -> str:
    lines = []
    lines.append("# AIBE Data Sources Summary\n")

    # Stories
    lines.append("## Stories (AIBE)\n")
    lines.append(f"- Total stories: {stories.get('stories_total', 0)}")
    lines.append(f"- Avg paragraphs/story: {stories.get('avg_paragraphs_per_story', 0)}")
    lines.append(f"- Avg sentences/paragraph: {stories.get('avg_sentences_per_paragraph', 0)}")
    lines.append(f"- Avg words/sentence: {stories.get('avg_words_per_sentence', 0)}")
    lines.append(f"- Avg events/word: {stories.get('avg_events_per_word', 0)}\n")

    if stories.get("samples"):
        lines.append("### Story Samples (redacted)\n")
        for i, s in enumerate(stories["samples"], 1):
            sid = s.get("session_id")
            lines.append(f"- Sample {i} — session: `{sid}`")
    lines.append("")

    # Streams
    lines.append("## Server Streams\n")
    lines.append(f"- Collection: {streams.get('collection', '-')}")
    lines.append(f"- Total events: {streams.get('total', 0)}")
    lines.append("- By stream: " + ", ".join([f"{k}={v}" for k, v in streams.get("by_stream", [])]))
    by_type = streams.get("by_type", [])
    if by_type:
        lines.append("- Top event types: " + ", ".join([f"{k}={v}" for k, v in by_type[:10]]))
    lines.append("")
    return "\n".join(lines)


def _normalize_target(e: Dict[str, Any]) -> str:
    """Best-effort target identity string for grouping."""
    t = e.get("target") or {}
    if isinstance(t, dict):
        label = t.get("label") or t.get("ariaLabel") or t.get("label_text") or t.get("text")
        cid = t.get("id") or t.get("element_id") or t.get("selector") or t.get("name")
        typ = t.get("type") or t.get("tagName")
        parts = [p for p in [label, cid, typ] if p]
        return "|".join(map(str, parts)) if parts else "unknown"
    return str(t)


def build_context_packet(
    client: MongoClient,
    session_id: str,
    streams_db: str,
    collection: str | None,
    max_words: int = 8,
    include_actor: bool = False,
) -> Dict[str, Any]:
    """
    Construct a compact, LLM-friendly context packet from server_streams.

    Rules:
    - Use only this session's events from the latest streams collection.
    - Group Observer events into words, ending on screen_status.
    - Deduplicate Story snapshots; keep only the most recent one.
    - Drop Actor by default; optionally include last 2 commands (type/target only).
    """
    db = client[streams_db]
    coll_name = collection or latest_streams_collection(client, streams_db)
    if not coll_name:
        return {"error": "No streams collection found"}

    col = db[coll_name]

    # Get last N events for this session, then process forward
    raw = list(col.find({"session_id": session_id}).sort("timestamp", -1).limit(800))
    events = list(reversed(raw))

    words = []
    current_events: List[Dict[str, Any]] = []
    last_story: Dict[str, Any] | None = None
    recent_actor: List[Dict[str, Any]] = []

    for doc in events:
        stream = doc.get("stream")
        if stream == "Story":
            last_story = sanitize_event(doc)
            continue
        if stream == "Actor":
            if include_actor and len(recent_actor) < 2:
                recent_actor.append({
                    "type": doc.get("type") or doc.get("data", {}).get("type"),
                    "target": _normalize_target(doc.get("target", {})),
                    "timestamp": doc.get("timestamp"),
                })
            continue
        if stream != "Observer":
            continue

        e = sanitize_event(doc)
        etype = e.get("type") or e.get("data", {}).get("type")
        if not etype or etype == "log":
            continue

        # Collect events until screen_status, then finalize a word
        if etype == "screen_status":
            # finalize word if we have user events
            if current_events:
                # summarize events
                target = _normalize_target(current_events[-1]) if current_events else "unknown"
                type_counts = Counter([ce.get("type") or ce.get("data", {}).get("type") for ce in current_events])
                words.append({
                    "target": target,
                    "event_types": dict(type_counts),
                    "events": current_events[-3:],  # last few raw events (redacted)
                    "result_screen": {
                        "url": e.get("data", {}).get("url") or e.get("url"),
                        "title": e.get("data", {}).get("title") or e.get("title"),
                    },
                })
                current_events = []
                # keep only last max_words
                if len(words) > max_words:
                    words = words[-max_words:]
            else:
                # screen_status without user events — ignore as standalone
                pass
        else:
            current_events.append(e)

    # Build packet
    packet: Dict[str, Any] = {
        "session_id": session_id,
        "source_collection": coll_name,
        "words": words[-max_words:],
    }

    if last_story:
        # Compact story snapshot
        story_data = dict(last_story)
        story_data.pop("_id", None)
        story_data.pop("timestamp", None)
        packet["story_snapshot"] = {
            "type": story_data.get("type"),
            "summary": {
                "paragraphs": len(story_data.get("paragraphs", [])) if isinstance(story_data.get("paragraphs"), list) else None,
            }
        }

    if include_actor and recent_actor:
        packet["recent_actor"] = recent_actor

    # Basic header: try to pull URL/title from last word's result_screen
    if packet["words"]:
        last_result = packet["words"][-1].get("result_screen", {})
        packet["url"] = last_result.get("url")
        packet["title"] = last_result.get("title")

    return packet


def main():
    parser = argparse.ArgumentParser(description="Summarize AIBE Stories and Server Streams from MongoDB")
    parser.add_argument("--mongo-uri", help="MongoDB connection string override")
    parser.add_argument("--stories-db", help="Stories database name override")
    parser.add_argument("--stories-collection", help="Stories collection name override")
    parser.add_argument("--streams-db", help="Server streams database name override")
    parser.add_argument("--streams-collection", help="Specific streams collection to inspect")
    parser.add_argument("--samples", type=int, default=3, help="Number of samples to include per section")
    parser.add_argument("--write", nargs="*", help="Optional output file(s): .md and/or .json")
    parser.add_argument("--context", help="Build a compact context packet for this sessionId from streams")
    parser.add_argument("--max-words", type=int, default=8, help="Max words to include in context packet")
    parser.add_argument("--include-actor", action="store_true", help="Include last Actor commands in context packet")
    args = parser.parse_args()

    mongo_uri, stories_db, stories_collection, streams_db = load_config_overrides(args)

    client = MongoClient(mongo_uri)

    stories_summary = summarize_stories(client, stories_db, stories_collection, args.samples)
    streams_summary = summarize_streams(client, streams_db, args.streams_collection, args.samples)

    md = to_markdown(stories_summary, streams_summary)
    print(md)

    out = {"stories": stories_summary, "streams": streams_summary, "generated_at": datetime.now(timezone.utc).isoformat()}

    # Optional context packet
    if args.context:
        context = build_context_packet(client, args.context, streams_db, args.streams_collection, args.max_words, args.include_actor)
        out["context"] = context
        print("\n## Context Packet\n")
        print(json.dumps(context, indent=2, default=_json_default))
    if args.write:
        for path in args.write:
            p = Path(path)
            try:
                if p.suffix.lower() == ".md":
                    p.write_text(md, encoding="utf-8")
                elif p.suffix.lower() == ".json":
                    p.write_text(json.dumps(out, indent=2, default=_json_default), encoding="utf-8")
            except Exception as e:
                print(f"[warn] failed to write {p}: {e}")


def _json_default(o: Any):
    if isinstance(o, datetime):
        # Ensure timezone-aware ISO
        if o.tzinfo is None:
            o = o.replace(tzinfo=timezone.utc)
        return o.astimezone(timezone.utc).isoformat()
    return str(o)


if __name__ == "__main__":
    main()
