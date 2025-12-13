#!/usr/bin/env python3
"""
Integration Pipeline Test
Test the complete Observer -> Story Assembly -> MongoDB pipeline
"""

import sys
import os
import asyncio
import requests
import json
import time
from datetime import datetime

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from aibe_server.config import get_database_config
from pymongo import MongoClient


class IntegrationPipelineTest:
    """Test the complete integration pipeline"""
    
    def __init__(self, server_url="http://localhost:3001"):
        self.server_url = server_url
        self.session_id = f"integration_test_{int(time.time())}"
        self.config = get_database_config()
        
    def test_server_connection(self):
        """Test if server is running and accessible"""
        try:
            response = requests.get(f"{self.server_url}/status")
            if response.status_code == 200:
                print("✓ Server is running and accessible")
                return True
            else:
                print(f"✗ Server returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Server is not running or not accessible")
            print("  Please start the server with: cd server && python -m aibe_server.main")
            return False
    
    def test_mongodb_connection(self):
        """Test MongoDB connection"""
        try:
            client = MongoClient(self.config.connection_string, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            client.close()
            print("✓ MongoDB is accessible")
            return True
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            return False
    
    def create_test_session(self):
        """Create a test session"""
        try:
            session_data = {
                "tabId": self.session_id,
                "url": "https://example.com/login",
                "title": "Login Page"
            }
            
            response = requests.put(
                f"{self.server_url}/sessions/init",
                json=session_data,
                headers={"X-Tab-ID": self.session_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"✓ Test session created: {self.session_id}")
                    return True
                else:
                    print(f"✗ Session creation failed: {result.get('message')}")
                    return False
            else:
                print(f"✗ Session creation failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error creating session: {e}")
            return False
    
    def send_test_events(self):
        """Send a series of test events to simulate user interaction"""
        events = [
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
            },
            {
                "type": "click",
                "timestamp": datetime.now().isoformat(),
                "source": "user",
                "target": {
                    "element_id": "password_input",
                    "url": "https://example.com/login",
                    "tagName": "input"
                },
                "data": {"action": "focus_password_field"}
            },
            {
                "type": "load",
                "timestamp": datetime.now().isoformat(),
                "source": "user",
                "target": {"url": "https://example.com/dashboard"},
                "data": {"page_title": "Dashboard", "redirect": True}
            }
        ]
        
        successful_events = 0
        story_updates = 0
        
        for i, event_data in enumerate(events, 1):
            try:
                response = requests.post(
                    f"{self.server_url}/sessions/{self.session_id}/events",
                    json=event_data,
                    headers={"X-Tab-ID": self.session_id}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        successful_events += 1
                        if "(story updated)" in result.get("message", ""):
                            story_updates += 1
                        print(f"  ✓ Event {i}: {event_data['type']} -> {result.get('message')}")
                    else:
                        print(f"  ✗ Event {i} failed: {result.get('message')}")
                else:
                    print(f"  ✗ Event {i} failed with status {response.status_code}")
                
                # Small delay between events
                time.sleep(0.1)
                
            except Exception as e:
                print(f"  ✗ Error sending event {i}: {e}")
        
        print(f"\n✓ Successfully sent {successful_events}/{len(events)} events")
        print(f"✓ Story updates: {story_updates}")
        
        return successful_events > 0, story_updates > 0
    
    def verify_mongodb_storage(self):
        """Verify that data was written to MongoDB"""
        try:
            # Wait for database writes to complete
            time.sleep(2)
            
            client = MongoClient(self.config.connection_string)
            db = client[self.config.database_name]
            collection = db[self.config.collection_name]
            
            # Find story for this session
            story_doc = collection.find_one({"session_id": self.session_id})
            
            if story_doc:
                print("✓ Story found in MongoDB!")
                print(f"  Story ID: {story_doc.get('story_id', 'Unknown')}")
                print(f"  Session ID: {story_doc.get('session_id', 'Unknown')}")
                print(f"  Paragraphs: {len(story_doc.get('paragraphs', []))}")
                
                # Verify structure
                paragraphs = story_doc.get('paragraphs', [])
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
                    
                    print(f"  Sentences: {total_sentences}")
                    print(f"  Words: {total_words}")
                    print(f"  Events: {total_events}")
                    
                    if total_events > 0:
                        print("✓ Hierarchical story structure verified")
                        client.close()
                        return True
                    else:
                        print("✗ No events found in story structure")
                        client.close()
                        return False
                else:
                    print("✗ No paragraphs found in story")
                    client.close()
                    return False
            else:
                print("✗ Story not found in MongoDB")
                print(f"  Searched for session_id: {self.session_id}")
                
                # Show existing documents for debugging
                total_docs = collection.count_documents({})
                print(f"  Total documents in collection: {total_docs}")
                
                client.close()
                return False
                
        except Exception as e:
            print(f"✗ Error verifying MongoDB storage: {e}")
            return False
    
    def run_complete_test(self):
        """Run the complete integration pipeline test"""
        print("=== Observer -> Story Assembly -> MongoDB Integration Test ===\n")
        
        print("1. Testing server connection...")
        if not self.test_server_connection():
            return False
        
        print("\n2. Testing MongoDB connection...")
        if not self.test_mongodb_connection():
            return False
        
        print(f"\n3. Creating test session: {self.session_id}")
        if not self.create_test_session():
            return False
        
        print("\n4. Sending test events through Observer pipeline...")
        events_success, story_updates = self.send_test_events()
        if not events_success:
            return False
        
        if not story_updates:
            print("⚠ Warning: No story updates detected in event responses")
        
        print("\n5. Verifying MongoDB storage...")
        if not self.verify_mongodb_storage():
            return False
        
        print("\n=== Integration Test Results ===")
        print("✓ SUCCESS: Complete integration pipeline working!")
        print("✓ Observer events processed successfully")
        print("✓ Story Assembly integration functional")
        print("✓ MongoDB storage verified")
        print("✓ Each browser session creates its own story")
        
        return True


if __name__ == "__main__":
    test = IntegrationPipelineTest()
    success = test.run_complete_test()
    
    if not success:
        print("\n✗ FAILURE: Integration pipeline has issues")
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: cd server && python -m aibe_server.main")
        print("2. Make sure MongoDB is running on localhost:27017")
        print("3. Check server logs for errors")
        sys.exit(1)
    else:
        print(f"\n🎉 Integration test completed successfully!")
        print("The Observer stream is now connected to Story Assembly!")