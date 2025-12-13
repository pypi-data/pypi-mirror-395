#!/usr/bin/env mongosh
/**
 * Projection Queries for AIBE Stories
 * 
 * This file is intended for mongosh (MongoDB Shell), not Node.js.
 * 
 * Efficient queries using projections to reduce data size.
 * Story documents can be very large; projections help manage this.
 * 
 * Run interactively:
 *   mongosh
 *   load("projections.js")
 */

use AIBE

// ============================================================================
// Exclude Heavy Fields (Suppressing Data)
// ============================================================================

// Exclude screen_status from all Words (can be very large with full DOM snapshots)
db.Stories.find(
    {},
    {
        "paragraphs.sentences.words.screen_status": 0  // 0 = exclude this field
    }
)

// Exclude multiple heavy fields
db.Stories.find(
    {},
    {
        "paragraphs.sentences.words.screen_status": 0,
        "paragraphs.sentences.words.events.target": 0,  // Exclude detailed target info
        "_id": 0  // Exclude MongoDB's internal ID
    }
)

// Exclude all event data, keep only Word structure
db.Stories.aggregate([
    {
        $project: {
            session_id: 1,
            "paragraphs.domain": 1,
            "paragraphs.sentences.url": 1,
            "paragraphs.sentences.words.screen_status": 0,
            "paragraphs.sentences.words.events": 0
        }
    }
])

// ============================================================================
// Select Specific Fields (Including Only What You Need)
// ============================================================================

// Get only session IDs and domains visited
db.Stories.find(
    {},
    {
        session_id: 1,  // 1 = include this field
        "paragraphs.domain": 1,
        _id: 0  // Exclude MongoDB ID
    }
)

// Get only URLs visited and timestamps (no event details)
db.Stories.aggregate([
    {
        $project: {
            session_id: 1,
            urls: "$paragraphs.sentences.url",
            timestamps: "$paragraphs.sentences.words.events.timestamp"
        }
    }
])

// Extract only element labels that users interacted with
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    { $unwind: "$paragraphs.sentences.words.events" },
    {
        $project: {
            session_id: 1,
            domain: "$paragraphs.domain",
            url: "$paragraphs.sentences.url",
            element_label: "$paragraphs.sentences.words.events.target.label",
            event_type: "$paragraphs.sentences.words.events.type",
            timestamp: "$paragraphs.sentences.words.events.timestamp",
            _id: 0
        }
    },
    { $limit: 100 }
])

// ============================================================================
// Handle Varying Field Paths
// ============================================================================

// Use aggregation with $ifNull to handle missing fields
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    {
        $project: {
            session_id: 1,
            domain: "$paragraphs.domain",
            url: "$paragraphs.sentences.url",
            // Safely access potentially missing fields
            has_events: {
                $cond: {
                    if: { $gt: [{ $size: { $ifNull: ["$paragraphs.sentences.words.events", []] } }, 0] },
                    then: true,
                    else: false
                }
            },
            has_screen_status: {
                $cond: {
                    if: { $ifNull: ["$paragraphs.sentences.words.screen_status", false] },
                    then: true,
                    else: false
                }
            },
            event_count: { $size: { $ifNull: ["$paragraphs.sentences.words.events", []] } }
        }
    }
])

// Filter to only Words that have events
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    {
        $match: {
            "paragraphs.sentences.words.events": { $exists: true, $ne: [] }
        }
    },
    {
        $project: {
            session_id: 1,
            domain: "$paragraphs.domain",
            events: "$paragraphs.sentences.words.events"
        }
    }
])

// ============================================================================
// Practical Example: Lightweight Session Summary
// ============================================================================

// Compact session summary (domains, URLs, element counts - no event details)
// Result is ~100x smaller than full document with all events and screen_status
db.Stories.aggregate([
    {
        $project: {
            session_id: 1,
            total_paragraphs: { $size: "$paragraphs" },
            domains: "$paragraphs.domain",
            sentences_per_paragraph: {
                $map: {
                    input: "$paragraphs",
                    as: "para",
                    in: { $size: "$$para.sentences" }
                }
            },
            urls_visited: {
                $reduce: {
                    input: "$paragraphs.sentences.url",
                    initialValue: [],
                    in: { $concatArrays: ["$$value", ["$$this"]] }
                }
            },
            _id: 0
        }
    }
])

// ============================================================================
// Key Principles
// ============================================================================
//
// - Exclude first if you know most fields aren't needed: { field: 0 }
// - Include specific if you need only a few fields: { field: 1 }
// - Can't mix include (1) and exclude (0) except for _id
// - Use aggregation pipelines for complex field selection with transformations
// - Always use projections when working with production data to reduce network/memory overhead
