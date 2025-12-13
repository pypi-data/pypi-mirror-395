/**
 * Drop MongoDB databases specified in ~/.AIBE/config.json
 * Usage: node drop-databases.js
 */

const { MongoClient } = require('mongodb');
const fs = require('fs');
const path = require('path');
const os = require('os');

async function dropDatabases() {
    try {
        // Read config from ~/.AIBE/config.json
        const configPath = path.join(os.homedir(), '.AIBE', 'config.json');
        console.log(`Reading config from: ${configPath}`);
        
        const configData = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        
        // Extract database names from config
        const databases = [
            configData.database?.database_name,
            configData.test_streaming?.database,
            configData.server_streaming?.database
        ].filter(Boolean); // Remove undefined/null values
        
        // Get connection string
        const connectionString = configData.database?.connection_string || 'mongodb://localhost:27017';
        
        console.log(`\nConnection: ${connectionString}`);
        console.log(`Databases to drop: ${databases.join(', ')}\n`);
        
        // Connect to MongoDB
        const client = new MongoClient(connectionString);
        await client.connect();
        console.log('✓ Connected to MongoDB\n');
        
        // Drop each database
        for (const dbName of databases) {
            try {
                const db = client.db(dbName);
                await db.dropDatabase();
                console.log(`✓ Dropped database: ${dbName}`);
            } catch (error) {
                console.error(`✗ Error dropping ${dbName}:`, error.message);
            }
        }
        
        await client.close();
        console.log('\n✓ Done - all databases dropped');
        
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

// Run the script
dropDatabases();