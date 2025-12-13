#!/usr/bin/env mongosh
/**
 * Element Interaction Queries for AIBE Stories
 * 
 * This file is intended for mongosh (MongoDB Shell), not Node.js.
 * 
 * Extract user interactions with specific form fields, buttons, and controls.
 * 
 * Run interactively:
 *   mongosh
 *   load("element-interactions.js")
 */

use AIBE

// ============================================================================
// Find Words Targeting Specific Controls
// ============================================================================

// Find all Words where user interacted with login/username fields
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    {
        $match: {
            $or: [
                { "paragraphs.sentences.words.events.target.label": /username/i },
                { "paragraphs.sentences.words.events.target.label": /email/i },
                { "paragraphs.sentences.words.events.target.label": /login/i }
            ]
        }
    },
    {
        $project: {
            session_id: 1,
            domain: "$paragraphs.domain",
            url: "$paragraphs.sentences.url",
            word: "$paragraphs.sentences.words"
        }
    }
])

// Find all password field interactions with final values
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    {
        $match: {
            "paragraphs.sentences.words.events.target.control_type": "INPUT_TEXT",
            "paragraphs.sentences.words.events.target.label": /password/i
        }
    },
    {
        $project: {
            session_id: 1,
            url: "$paragraphs.sentences.url",
            target_label: "$paragraphs.sentences.words.events.target.label",
            timestamp: "$paragraphs.sentences.words.events.timestamp"
        }
    }
])

// Extract all button clicks across all stories
db.Stories.aggregate([
    { $unwind: "$paragraphs" },
    { $unwind: "$paragraphs.sentences" },
    { $unwind: "$paragraphs.sentences.words" },
    { $unwind: "$paragraphs.sentences.words.events" },
    {
        $match: {
            "paragraphs.sentences.words.events.type": "mouse",
            "paragraphs.sentences.words.events.target.control_type": "BUTTON"
        }
    },
    {
        $project: {
            session_id: 1,
            domain: "$paragraphs.domain",
            button_label: "$paragraphs.sentences.words.events.target.label",
            timestamp: "$paragraphs.sentences.words.events.timestamp"
        }
    },
    { $sort: { timestamp: -1 } }
])
