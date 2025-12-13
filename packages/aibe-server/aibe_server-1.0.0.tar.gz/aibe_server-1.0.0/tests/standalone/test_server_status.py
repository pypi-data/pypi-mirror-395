#!/usr/bin/env python3
"""
Test server status and story assembly integration
"""

import requests
import json
from datetime import datetime
import time

def test_server_integration():
    print('Testing server connection...')
    try:
        response = requests.get('http://localhost:3001/health', timeout=5)
        print(f'✓ Server is running - Status: {response.status_code}')
    except Exception as e:
        print(f'✗ Server connection failed: {e}')
        return False

    print('\nTesting MongoDB connection...')
    try:
        from aibe_server.config import get_database_config
        from pymongo import MongoClient
        
        config = get_database_config()
        client = MongoClient(config.connection_string, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print('✓ MongoDB connection successful')
        
        # Check collection
        db = client[config.database_name]
        collection = db[config.collection_name]
        doc_count = collection.count_documents({})
        print(f'✓ Collection \'{config.collection_name}\' has {doc_count} documents')
        client.close()
    except Exception as e:
        print(f'✗ MongoDB connection failed: {e}')
        return False

    print('\nTesting story assembly integration...')
    session_id = f'test_session_{int(time.time())}'

    # Create session
    session_data = {
        'tabId': session_id,
        'url': 'https://example.com/test',
        'title': 'Test Page'
    }

    try:
        response = requests.post(
            'http://localhost:3001/sessions/init',
            json=session_data,
            headers={'X-Tab-ID': session_id},
            timeout=5
        )
        result = response.json()
        print(f'Session creation: {response.status_code} - {result.get("message", "")}')
    except Exception as e:
        print(f'✗ Session creation failed: {e}')

    # Send test event
    event_data = {
        'type': 'click',
        'timestamp': datetime.now().isoformat(),
        'source': 'user',
        'target': {
            'element_id': 'test_button',
            'url': 'https://example.com/test'
        },
        'data': {'action': 'test_click'}
    }

    try:
        response = requests.post(
            f'http://localhost:3001/sessions/{session_id}/events',
            json=event_data,
            headers={'X-Tab-ID': session_id},
            timeout=5
        )
        result = response.json()
        print(f'Event processing: {response.status_code} - {result.get("message", "")}')
        
        if '(story updated)' in result.get('message', ''):
            print('✓ Story assembly is working!')
            story_working = True
        else:
            print('⚠ Story assembly may not be processing events')
            story_working = False
            
    except Exception as e:
        print(f'✗ Event sending failed: {e}')
        story_working = False

    print('\nChecking database for new story...')
    time.sleep(2)  # Wait for database write

    try:
        from aibe_server.config import get_database_config
        from pymongo import MongoClient
        
        config = get_database_config()
        client = MongoClient(config.connection_string)
        db = client[config.database_name] 
        collection = db[config.collection_name]
        
        story = collection.find_one({'session_id': session_id})
        if story:
            print('✓ Story found in database!')
            print(f'  Story ID: {story.get("story_id", "Unknown")}')
            print(f'  Paragraphs: {len(story.get("paragraphs", []))}')
            
            # Show structure
            paragraphs = story.get('paragraphs', [])
            if paragraphs:
                total_sentences = sum(len(p.get('sentences', [])) for p in paragraphs)
                total_words = sum(
                    len(s.get('words', []))
                    for p in paragraphs
                    for s in p.get('sentences', [])
                )
                total_events = sum(
                    len(w.get('events', []))
                    for p in paragraphs
                    for s in p.get('sentences', [])
                    for w in s.get('words', [])
                )
                print(f'  Structure: {total_sentences} sentences, {total_words} words, {total_events} events')
            
            database_working = True
        else:
            print('✗ No story found in database')
            database_working = False
            
        client.close()
    except Exception as e:
        print(f'✗ Database check failed: {e}')
        database_working = False
    
    print('\n=== Integration Status ===')
    print(f'Server: ✓ Running')
    print(f'MongoDB: ✓ Connected')
    print(f'Story Assembly: {"✓ Working" if story_working else "✗ Not Working"}')
    print(f'Database Storage: {"✓ Working" if database_working else "✗ Not Working"}')
    
    return story_working and database_working

if __name__ == "__main__":
    success = test_server_integration()
    if success:
        print('\n🎉 Story assembly integration is fully functional!')
    else:
        print('\n⚠ Some issues detected in story assembly integration')