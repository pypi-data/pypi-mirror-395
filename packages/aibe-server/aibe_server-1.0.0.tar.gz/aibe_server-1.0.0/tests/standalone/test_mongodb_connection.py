#!/usr/bin/env python3
"""
Test MongoDB Connection and Story Writing
Verify that the story assembler writes data to the correct MongoDB database and collection
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from aibe_server.story_assembler import create_mongodb_story_assembler
from aibe_server.models.events import BrowserEvent
from aibe_server.config import get_database_config


async def test_mongodb_writing():
    """Test that data is actually written to MongoDB"""
    print("Testing MongoDB Story Assembly...")
    
    # Show current configuration
    db_config = get_database_config()
    print(f"Connection String: {db_config.connection_string}")
    print(f"Database Name: {db_config.database_name}")
    print(f"Collection Name: {db_config.collection_name}")
    
    # Create story assembler with MongoDB persistence
    assembler = create_mongodb_story_assembler()
    
    # Create test event
    test_event = BrowserEvent(
        type="click",
        timestamp=datetime.now().isoformat(),
        source="test",
        target={
            "element_id": "test_button",
            "url": "https://example.com/test"
        },
        data={
            "test": True,
            "description": "Testing MongoDB connection"
        }
    )
    
    # Process event through story assembler
    print("\nProcessing test event...")
    session_id = "test_session_mongodb"
    story = assembler.process_event(session_id, test_event)
    
    if story:
        print(f"Story created successfully!")
        print(f"Story ID: {story.id}")
        print(f"Session ID: {story.session_id}")
        print(f"Paragraphs: {len(story.paragraphs)}")
        if story.paragraphs:
            print(f"Sentences: {len(story.paragraphs[0].sentences)}")
            if story.paragraphs[0].sentences:
                print(f"Words: {len(story.paragraphs[0].sentences[0].words)}")
                if story.paragraphs[0].sentences[0].words:
                    print(f"Events: {len(story.paragraphs[0].sentences[0].words[0].events)}")
        
        # Wait a moment for database write to complete
        print("\nWaiting for database write to complete...")
        await asyncio.sleep(2)
        
        # Try to retrieve the story to verify it was written
        retrieved_story = assembler.get_story(session_id)
        if retrieved_story:
            print("✓ Story retrieval successful - data is being written to MongoDB!")
        else:
            print("✗ Story retrieval failed")
            
        # Close the session
        assembler.close_session(session_id)
        print("✓ Session closed")
        
    else:
        print("✗ Failed to create story")
    
    print(f"\nData should be written to:")
    print(f"  Database: {db_config.database_name}")
    print(f"  Collection: {db_config.collection_name}")
    print(f"  Connection: {db_config.connection_string}")


if __name__ == "__main__":
    try:
        asyncio.run(test_mongodb_writing())
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()