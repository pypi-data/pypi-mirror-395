#!/usr/bin/env python3
"""
Complete Story Assembly Pipeline Test
Test the entire pipeline from event creation to MongoDB storage
"""

import sys
import os
import asyncio
from datetime import datetime
import time

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from aibe_server.story_assembler import create_mongodb_story_assembler
from aibe_server.models.events import BrowserEvent
from aibe_server.config import get_database_config
from pymongo import MongoClient


def create_test_events():
    """Create a series of test events to simulate real user interaction"""
    events = [
        BrowserEvent(
            type="load",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={"url": "https://example.com/login"},
            data={"page_title": "Login Page"}
        ),
        BrowserEvent(
            type="click",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "email_input",
                "url": "https://example.com/login",
                "tagName": "input",
                "type": "email"
            },
            data={"action": "focus_email_field"}
        ),
        BrowserEvent(
            type="keyboard",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "email_input",
                "url": "https://example.com/login"
            },
            data={"key": "test@example.com", "action": "type_email"}
        ),
        BrowserEvent(
            type="click",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "password_input",
                "url": "https://example.com/login",
                "tagName": "input",
                "type": "password"
            },
            data={"action": "focus_password_field"}
        ),
        BrowserEvent(
            type="keyboard",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "password_input",
                "url": "https://example.com/login"
            },
            data={"action": "type_password"}
        ),
        BrowserEvent(
            type="click",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "login_button",
                "url": "https://example.com/login",
                "tagName": "button"
            },
            data={"action": "submit_login"}
        ),
        BrowserEvent(
            type="load",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={"url": "https://example.com/dashboard"},
            data={"page_title": "Dashboard", "redirect": True}
        ),
        BrowserEvent(
            type="click",
            timestamp=datetime.now().isoformat(),
            source="user",
            target={
                "element_id": "menu_profile",
                "url": "https://example.com/dashboard",
                "tagName": "a"
            },
            data={"action": "navigate_to_profile"}
        )
    ]
    return events


async def test_complete_pipeline():
    """Test the complete story assembly pipeline"""
    print("=== Complete Story Assembly Pipeline Test ===\n")
    
    # Show configuration
    config = get_database_config()
    print(f"MongoDB Configuration:")
    print(f"  Connection: {config.connection_string}")
    print(f"  Database: {config.database_name}")
    print(f"  Collection: {config.collection_name}\n")
    
    # Create story assembler
    print("1. Creating Story Assembler...")
    assembler = create_mongodb_story_assembler()
    print("   ✓ Story Assembler created\n")
    
    # Create test session
    session_id = f"pipeline_test_{int(time.time())}"
    print(f"2. Starting test session: {session_id}")
    
    # Create and process test events
    events = create_test_events()
    print(f"3. Processing {len(events)} test events...")
    
    story = None
    for i, event in enumerate(events, 1):
        print(f"   Processing event {i}: {event.type} -> {event.target.get('element_id', event.target.get('url', 'unknown'))}")
        story = assembler.process_event(session_id, event)
        
        if story:
            print(f"     Story updated: {len(story.paragraphs)} paragraphs")
        else:
            print(f"     ✗ Failed to process event {i}")
            break
        
        # Small delay to simulate real user interaction timing
        time.sleep(0.1)
    
    if story:
        print(f"\n4. Final Story Structure:")
        print(f"   Story ID: {story.id}")
        print(f"   Session ID: {story.session_id}")
        print(f"   Paragraphs: {len(story.paragraphs)}")
        
        for p_idx, paragraph in enumerate(story.paragraphs):
            print(f"     Paragraph {p_idx + 1} (domain: {paragraph.domain}):")
            print(f"       Sentences: {len(paragraph.sentences)}")
            
            for s_idx, sentence in enumerate(paragraph.sentences):
                print(f"         Sentence {s_idx + 1} (URL: {sentence.url}):")
                print(f"           Words: {len(sentence.words)}")
                
                for w_idx, word in enumerate(sentence.words):
                    print(f"             Word {w_idx + 1}: {len(word.events)} events")
    
    # Wait for database writes to complete
    print(f"\n5. Waiting for database writes to complete...")
    await asyncio.sleep(3)
    
    # Check database directly
    print(f"6. Verifying data in MongoDB...")
    try:
        client = MongoClient(config.connection_string)
        db = client[config.database_name]
        collection = db[config.collection_name]
        
        # Find our story in the database
        db_story = collection.find_one({"session_id": session_id})
        
        if db_story:
            print(f"   ✓ Story found in database!")
            print(f"   Story ID: {db_story.get('story_id', 'Unknown')}")
            print(f"   Created: {db_story.get('created_at', 'Unknown')}")
            print(f"   Updated: {db_story.get('updated_at', 'Unknown')}")
            print(f"   Paragraphs in DB: {len(db_story.get('paragraphs', []))}")
            
            # Verify structure matches
            if len(db_story.get('paragraphs', [])) == len(story.paragraphs):
                print(f"   ✓ Database structure matches in-memory structure")
            else:
                print(f"   ⚠ Database structure differs from in-memory structure")
        else:
            print(f"   ✗ Story NOT found in database!")
            print(f"   This indicates a problem with database writes")
        
        client.close()
        
    except Exception as e:
        print(f"   ✗ Error checking database: {e}")
    
    # Close session
    print(f"\n7. Closing session...")
    assembler.close_session(session_id)
    print(f"   ✓ Session closed")
    
    # Final database check
    print(f"\n8. Final database verification...")
    try:
        client = MongoClient(config.connection_string)
        db = client[config.database_name]
        collection = db[config.collection_name]
        
        # Check if session close was recorded
        db_story = collection.find_one({"session_id": session_id})
        if db_story and db_story.get('end_time'):
            print(f"   ✓ Session closure recorded in database")
        else:
            print(f"   ⚠ Session closure may not be recorded yet")
        
        # Count total documents
        total_docs = collection.count_documents({})
        print(f"   Total documents in collection: {total_docs}")
        
        client.close()
        
    except Exception as e:
        print(f"   ✗ Error in final check: {e}")
    
    print(f"\n=== Pipeline Test Complete ===")
    
    if story and db_story:
        print("✓ SUCCESS: Complete pipeline working correctly!")
        print("✓ Events processed into hierarchical structure")
        print("✓ Data written to MongoDB successfully")
        return True
    else:
        print("✗ FAILURE: Pipeline has issues")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(test_complete_pipeline())
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)