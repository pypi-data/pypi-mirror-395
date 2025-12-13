#!/usr/bin/env mongosh
/**
 * Pattern Analysis Queries for AIBE Stories
 * 
 * This file is intended for mongosh (MongoDB Shell), not Node.js.
 * 
 * Analyze navigation patterns, form completion, and session flows.
 * 
 * Run interactively:
 *   mongosh
 *   load("pattern-analysis.js")
 */

use AIBE

// ============================================================================
// Analyze Patterns Across Sessions
// ============================================================================

// Find common URL navigation patterns
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    {
        $group: {
            _id: {
                domain: "$paragraphs.domain",
                url: "$paragraphs.sentences.url"
            },
            visit_count: { $sum: 1 },
            sessions: { $addToSet: "$session_id" }
        }
    },
    {
        $project: {
            domain: "$_id.domain",
            url: "$_id.url",
            visit_count: 1,
            unique_sessions: { $size: "$sessions" }
        }
    },
    { $sort: { visit_count: -1 } },
    { $limit: 20 }
])

// Analyze form completion patterns - find which fields users fill most often
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    { $unwind: "$paragraphs.sentences.words.events" },
    {
        $match: {
            "paragraphs.sentences.words.events.type": "keyboard"
        }
    },
    {
        $group: {
            _id: {
                domain: "$paragraphs.domain",
                field_label: "$paragraphs.sentences.words.events.target.label"
            },
            interaction_count: { $sum: 1 }
        }
    },
    { $sort: { interaction_count: -1 } },
    { $limit: 20 }
])

// Find navigation flow patterns (domain sequences)
db.Stories.aggregate([
    {
        $project: {
            session_id: 1,
            domain_sequence: "$paragraphs.domain"
        }
    },
    {
        $group: {
            _id: "$domain_sequence",
            count: { $sum: 1 },
            example_session: { $first: "$session_id" }
        }
    },
    { $sort: { count: -1 } },
    { $limit: 10 }
])

// Calculate average session length (number of paragraphs/domains visited)
db.Stories.aggregate([
    {
        $project: {
            session_id: 1,
            paragraph_count: { $size: "$paragraphs" }
        }
    },
    {
        $group: {
            _id: null,
            avg_domains_per_session: { $avg: "$paragraph_count" },
            min_domains: { $min: "$paragraph_count" },
            max_domains: { $max: "$paragraph_count" }
        }
    }
])
