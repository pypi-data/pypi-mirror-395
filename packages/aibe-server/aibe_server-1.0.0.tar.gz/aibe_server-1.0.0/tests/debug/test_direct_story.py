#!/usr/bin/env python3
"""
Direct test of story integration service
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the server directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_direct_story_integration():
    """Test story integration service directly"""
    print("=== Direct Story Integration Test ===\n")
    
    try:
        from aibe_server.services.story_integration import get_observer_story_bridge
        print("✓ Successfully imported get_observer_story_bridge")
        
        bridge = get_observer_story_bridge()
        print("✓ Successfully created story bridge")
        
        session_id = "direct_test_session"
        
        # Test event
        test_event = {
            "type": "load",
            "timestamp": datetime.now().isoformat(),
            "source": "user",
            "target": {"url": "https://example.com/test"},
            "data": {"page_title": "Test Page"}
        }
        
        print(f"Testing with session: {session_id}")
        print(f"Event type: {test_event['type']}")
        
        # Process event
        result = asyncio.run(bridge.process_observer_event(session_id, test_event))
        print(f"Result: {result}")
        
        if result.get('success'):
            print("✓ Story processing successful")
            if result.get('story_updated'):
                print("✓ Story was updated")
            else:
                print("⚠ Story processing succeeded but no update")
        else:
            print(f"✗ Story processing failed: {result.get('error')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_story_integration()