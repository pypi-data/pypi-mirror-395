#!/usr/bin/env mongosh
/**
 * Basic MongoDB Queries for AIBE Stories
 * 
 * This file is intended for mongosh (MongoDB Shell), not Node.js.
 * 
 * Run interactively:
 *   mongosh
 *   load("basic-queries.js")
 * 
 * Or copy/paste individual queries into mongosh or MongoDB Compass.
 */

// Switch to AIBE database
use AIBE

// ============================================================================
// Query All Stories from Today
// ============================================================================

const today = new Date();
today.setHours(0, 0, 0, 0);

// Get all stories from today
db.Stories.find({
  "paragraphs.sentences.words.events.timestamp": {
    $gte: today.toISOString()
  }
})

// Count stories from today
db.Stories.countDocuments({
  "paragraphs.sentences.words.events.timestamp": {
    $gte: today.toISOString()
  }
})

// ============================================================================
// Find Stories by Domain
// ============================================================================

// Find all stories that visited github.com
db.Stories.find({
  "paragraphs.domain": "github.com"
})

// Find stories that visited multiple specific domains
db.Stories.find({
  "paragraphs.domain": {
    $in: ["github.com", "stackoverflow.com", "developer.mozilla.org"]
  }
})

// Get unique list of all domains visited across all stories
db.Stories.distinct("paragraphs.domain")

// Count how many stories visited each domain
db.Stories.aggregate([
  { $unwind: "$paragraphs" },
  {
    $group: {
      _id: "$paragraphs.domain",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
])
