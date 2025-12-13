/**
 * MongoDB Node.js Driver Examples for AIBE Stories
 * 
 * Programmatic access examples for AI systems and applications.
 * 
 * Prerequisites:
 *   npm install mongodb
 * 
 * Run:
 *   node nodejs-driver.js
 */

const { MongoClient } = require('mongodb');

// ============================================================================
// Example 1: Basic Queries with Projections
// ============================================================================

async function queryStories() {
    const client = new MongoClient('mongodb://localhost:27017');

    try {
        await client.connect();
        const db = client.db('AIBE');
        const stories = db.collection('Stories');

        // Find stories with projection (exclude heavy fields)
        const lightweightStories = await stories.find(
            {},
            {
                projection: {
                    'paragraphs.sentences.words.screen_status': 0,  // Exclude
                    'paragraphs.sentences.words.events.target': 0
                }
            }
        ).toArray();

        console.log(`Found ${lightweightStories.length} stories (lightweight)`);

        // Aggregation pipeline (select specific fields)
        const sessionSummaries = await stories.aggregate([
            {
                $project: {
                    session_id: 1,
                    domains: '$paragraphs.domain',
                    total_paragraphs: { $size: '$paragraphs' },
                    _id: 0
                }
            }
        ]).toArray();

        console.log(`Session summaries: ${sessionSummaries.length}`);

        // Filter and project in one query
        const todayStories = await stories.find(
            {
                'paragraphs.sentences.words.events.timestamp': {
                    $gte: new Date().toISOString()
                }
            },
            {
                projection: {
                    session_id: 1,
                    'paragraphs.domain': 1,
                    _id: 0
                }
            }
        ).toArray();

        console.log(`Stories from today: ${todayStories.length}`);

        return { lightweightStories, sessionSummaries, todayStories };

    } finally {
        await client.close();
    }
}

// ============================================================================
// Example 2: Extract Element Interactions
// ============================================================================

async function extractInteractions() {
    const client = new MongoClient('mongodb://localhost:27017');

    try {
        await client.connect();
        const db = client.db('AIBE');
        const stories = db.collection('Stories');

        const interactions = await stories.aggregate([
            { $unwind: '$paragraphs' },
            { $unwind: '$paragraphs.sentences' },
            { $unwind: '$paragraphs.sentences.words' },
            { $unwind: '$paragraphs.sentences.words.events' },
            {
                $match: {
                    'paragraphs.sentences.words.events.type': 'keyboard'
                }
            },
            {
                $project: {
                    session_id: 1,
                    domain: '$paragraphs.domain',
                    url: '$paragraphs.sentences.url',
                    element_label: '$paragraphs.sentences.words.events.target.label',
                    timestamp: '$paragraphs.sentences.words.events.timestamp',
                    _id: 0
                }
            },
            { $limit: 100 }
        ]).toArray();

        console.log(`Found ${interactions.length} keyboard interactions`);
        return interactions;

    } finally {
        await client.close();
    }
}

// ============================================================================
// Example 3: Streaming Large Result Sets (Memory Efficient)
// ============================================================================

async function streamStories() {
    const client = new MongoClient('mongodb://localhost:27017');

    try {
        await client.connect();
        const db = client.db('AIBE');
        const stories = db.collection('Stories');

        // Use cursor for large datasets instead of toArray()
        const cursor = stories.find(
            {},
            {
                projection: {
                    session_id: 1,
                    'paragraphs.domain': 1,
                    _id: 0
                }
            }
        );

        let count = 0;
        // Process one document at a time
        for await (const story of cursor) {
            // Process each story without loading all into memory
            console.log(`Session: ${story.session_id}, Domains: ${story.paragraphs?.map(p => p.domain)}`);
            count++;
        }

        console.log(`Streamed ${count} stories`);

    } finally {
        await client.close();
    }
}

// ============================================================================
// Example 4: Conditional Field Handling (Handle Missing Fields)
// ============================================================================

async function safeFieldAccess() {
    const client = new MongoClient('mongodb://localhost:27017');

    try {
        await client.connect();
        const db = client.db('AIBE');
        const stories = db.collection('Stories');

        const results = await stories.aggregate([
            { $unwind: '$paragraphs' },
            { $unwind: '$paragraphs.sentences' },
            { $unwind: '$paragraphs.sentences.words' },
            {
                $project: {
                    session_id: 1,
                    domain: '$paragraphs.domain',
                    // Safely access potentially missing fields
                    has_events: {
                        $cond: {
                            if: { $gt: [{ $size: { $ifNull: ['$paragraphs.sentences.words.events', []] } }, 0] },
                            then: true,
                            else: false
                        }
                    },
                    event_count: { $size: { $ifNull: ['$paragraphs.sentences.words.events', []] } },
                    _id: 0
                }
            }
        ]).toArray();

        console.log(`Analyzed ${results.length} words for field presence`);
        return results;

    } finally {
        await client.close();
    }
}

// ============================================================================
// Run Examples
// ============================================================================

async function main() {
    console.log('=== MongoDB Node.js Driver Examples ===\n');

    try {
        console.log('--- Example 1: Basic Queries ---');
        await queryStories();

        console.log('\n--- Example 2: Extract Interactions ---');
        await extractInteractions();

        console.log('\n--- Example 3: Stream Stories ---');
        await streamStories();

        console.log('\n--- Example 4: Safe Field Access ---');
        await safeFieldAccess();

        console.log('\n=== All examples completed ===');

    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

main();
