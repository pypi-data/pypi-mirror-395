#!/usr/bin/env python3
"""
MongoDB Connection Test
Check if MongoDB is running and accessible
"""

import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from aibe_server.config import get_database_config


def test_mongodb_connection():
    """Test MongoDB connection and accessibility"""
    print("Testing MongoDB Connection...")
    
    # Get configuration
    config = get_database_config()
    print(f"Connection String: {config.connection_string}")
    print(f"Database: {config.database_name}")
    print(f"Collection: {config.collection_name}")
    
    try:
        # Create MongoDB client with short timeout for quick test
        client = MongoClient(config.connection_string, serverSelectionTimeoutMS=3000)
        
        # Test connection by pinging the server
        client.admin.command('ping')
        print("✓ MongoDB connection successful")
        
        # Test database access
        db = client[config.database_name]
        collection = db[config.collection_name]
        
        # Check if collection exists and has any documents
        doc_count = collection.count_documents({})
        print(f"✓ Collection '{config.collection_name}' found with {doc_count} documents")
        
        # List a few recent documents if any exist
        if doc_count > 0:
            print("\nRecent documents:")
            for doc in collection.find().sort("_id", -1).limit(3):
                doc_id = doc.get("_id", "Unknown")
                session_id = doc.get("session_id", "Unknown")
                story_id = doc.get("story_id", "Unknown")
                created_at = doc.get("created_at", "Unknown")
                print(f"  - Story ID: {story_id}, Session: {session_id}, Created: {created_at}")
        else:
            print("No documents found in the collection")
        
        client.close()
        return True
        
    except ConnectionFailure as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False
    except ServerSelectionTimeoutError as e:
        print(f"✗ MongoDB server not accessible: {e}")
        print("Make sure MongoDB service is running on localhost:27017")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_mongodb_connection()
    if not success:
        print("\nTroubleshooting:")
        print("1. Make sure MongoDB is installed and running")
        print("2. Check if MongoDB service is running on port 27017")
        print("3. Verify MongoDB is accessible at localhost:27017")
        sys.exit(1)