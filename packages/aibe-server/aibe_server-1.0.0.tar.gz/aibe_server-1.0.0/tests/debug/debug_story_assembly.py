#!/usr/bin/env python3
"""
Debug script to test story assembly pipeline
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the server directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from aibe_server.services.story_integration import get_story_integration_service
from aibe_server.models.events import BrowserEvent

def test_story_assembly():
    """Test the story assembly pipeline with sample events"""
    print("=== Story Assembly Debug Test ===\n")
    
    # Create story integration service
    story_service = get_story_integration_service()
    session_id = "debug_test_session"
    
    # Create test events similar to integration test
    test_events = [
        {
            "type": "load",
            "timestamp": datetime.now().isoformat(),
            "source": "user",
            "target": {"url": "https://example.com/login"},
            "data": {"page_title": "Login Page"}
        },
        {
            "type": "click",
            "timestamp": datetime.now().isoformat(),
            "source": "user",
            "target": {
                "element_id": "email_input",
                "url": "https://example.com/login",
                "tagName": "input"
            },
            "data": {"action": "focus_email_field"}
        },
        {
            "type": "keyboard",
            "timestamp": datetime.now().isoformat(),
            "source": "user",
            "target": {
                "element_id": "email_input",
                "url": "https://example.com/login"
            },
            "data": {"key": "test@example.com", "action": "type_email"}
        }
    ]
    
    print(f"Testing with session ID: {session_id}")
    print(f"Number of test events: {len(test_events)}\n")
    
    # Process each event
    for i, event_data in enumerate(test_events, 1):
        print(f"Processing event {i}: {event_data['type']}")
        
        try:
            # Process event synchronously (not async)
            result = asyncio.run(story_service.process_event(session_id, event_data))
            
            if result:
                print(f"  ✓ Story returned: ID={result.id}")
                print(f"  ✓ Paragraphs: {len(result.paragraphs)}")
                
                total_sentences = sum(len(p.sentences) for p in result.paragraphs)
                total_words = sum(len(s.words) for p in result.paragraphs for s in p.sentences)
                total_events = sum(len(w.events) for p in result.paragraphs for s in p.sentences for w in s.words)
                
                print(f"  ✓ Sentences: {total_sentences}")
                print(f"  ✓ Words: {total_words}")
                print(f"  ✓ Events: {total_events}")
            else:
                print(f"  ✗ Story returned None")
                
        except Exception as e:
            print(f"  ✗ Exception: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    # Check final story
    final_story = story_service.get_story(session_id)
    if final_story:
        print(f"Final story: {final_story.id}")
        print(f"Total paragraphs: {len(final_story.paragraphs)}")
    else:
        print("No final story found")
    
    # Get session stats
    stats = story_service.get_session_stats(session_id)
    print(f"Session stats: {stats}")

if __name__ == "__main__":
    test_story_assembly()