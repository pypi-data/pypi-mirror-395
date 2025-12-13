"""
MongoDB persistence implementation for Story Assembly
Concrete implementation of the StoryPersistence interface using MongoDB
"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
import json

from .base import StoryPersistence
from ..models.screen import Story, Paragraph, Sentence, Word
from ..utils.logging import log_info, log_warn, log_error, log_debug


class MongoStoryPersistence(StoryPersistence):
    """
    MongoDB implementation of StoryPersistence interface
    
    Provides async MongoDB operations for storing and retrieving Story objects
    with configurable connection string and database settings.
    """
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/AIBE", database_name: str = "AIBE", collection_name: str = "Stories"):
        """
        Initialize MongoDB persistence layer
        
        Args:
            connection_string: MongoDB connection string (default: "mongodb://localhost:27017/AIBE")
            database_name: Database name for storing stories (default: "AIBE")
            collection_name: Collection name for storing stories (default: "Stories")
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None
        self._collection: Optional[AsyncIOMotorCollection] = None
        self._connected = False
        
    async def _ensure_connection(self) -> None:
        """Ensure MongoDB connection is established"""
        if not self._connected:
            try:
                self._client = AsyncIOMotorClient(self.connection_string)
                self._db = self._client[self.database_name]
                self._collection = self._db[self.collection_name]
                
                # Test connection
                await self._client.admin.command('ping')
                self._connected = True
                log_info(f"[MongoDB] Connected to MongoDB at {self.connection_string}")
                
                # Create indexes for better performance
                await self._create_indexes()
                
            except ConnectionFailure as e:
                log_error(f"[MongoDB] Failed to connect to MongoDB: {e}")
                raise
            except Exception as e:
                log_error(f"[MongoDB] Unexpected error connecting to MongoDB: {e}")
                raise
    
    async def _create_indexes(self) -> None:
        """Create necessary indexes for optimal query performance"""
        try:
            # Create unique index on session_id with a specific name to avoid conflicts
            await self._collection.create_index(
                "session_id", 
                unique=True, 
                name="session_id_unique"
            )
            # Compound index on session_id and timestamp for ordered retrieval
            await self._collection.create_index(
                [("session_id", 1), ("timestamp", -1)],
                name="session_timestamp_compound"
            )
            
        except Exception as e:
            log_warn(f"[MongoDB] Failed to create indexes: {e}")
    
    def _story_to_dict(self, story: Story) -> Dict[str, Any]:
        """Convert Story object to MongoDB document"""
        try:
            # Use Pydantic's model_dump with mode='json' to use field_serializers
            story_dict = story.model_dump(mode='json')
            
            # Note: created_at and updated_at are added by store_story/update_story
            
            return story_dict
            
        except Exception as e:
            log_error(f"[MongoDB] Error converting story to dict: {e}")
            raise
    
    def _dict_to_story(self, doc: Dict[str, Any]) -> Story:
        """Convert MongoDB document back to Story object"""
        try:
            # Remove MongoDB-specific fields
            doc.pop("_id", None)
            doc.pop("created_at", None)
            doc.pop("updated_at", None)
            
            # Create Story object from dict
            return Story(**doc)
            
        except Exception as e:
            log_error(f"[MongoDB] Error converting dict to story: {e}")
            raise
    
    async def store_story(self, story: Story) -> bool:
        """
        Store a new story in MongoDB
        
        Args:
            story: Story object to store
            
        Returns:
            bool: True if stored successfully, False otherwise
        """
        try:
            await self._ensure_connection()
            
            story_doc = self._story_to_dict(story)
            # Set created_at on new story (ISO format)
            now = datetime.now().isoformat()
            story_doc["created_at"] = now
            story_doc["updated_at"] = now
            
            # Insert the story document
            result = await self._collection.insert_one(story_doc)
            
            if result.inserted_id:
                log_debug(f"[MongoDB] Successfully stored NEW story: {story.session_id} for session: {story.session_id}")
                return True
            else:
                log_error(f"[MongoDB] Failed to store story: {story.session_id}")
                return False
                
        except DuplicateKeyError:
            log_warn(f"[MongoDB] Story {story.session_id} already exists, use update_story instead")
            return False
        except Exception as e:
            log_error(f"[MongoDB] Error storing story {story.session_id}: {e}")
            return False
    
    async def update_story(self, session_id: str, story: Story) -> bool:
        """
        Update an existing story in MongoDB
        
        Args:
            session_id: Unique session identifier
            story: Updated Story object
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            await self._ensure_connection()
            
            story_doc = self._story_to_dict(story)
            # Preserve created_at, only update updated_at (ISO format)
            existing = await self._collection.find_one({"session_id": session_id})
            now = datetime.now().isoformat()
            
            if existing and "created_at" in existing:
                # Updating existing story - preserve original created_at
                story_doc["created_at"] = existing["created_at"]
                story_doc["updated_at"] = now
            else:
                # New story (shouldn't happen in update_story, but be defensive)
                story_doc["created_at"] = now
                story_doc["updated_at"] = now
            
            # Update the story document
            result = await self._collection.replace_one(
                {"session_id": session_id},
                story_doc,
                upsert=True  # Create if doesn't exist
            )
            
            if result.modified_count > 0 or result.upserted_id:
                log_debug(f"[MongoDB] Successfully updated story: {session_id} for session: {story.session_id}")
                return True
            else:
                log_warn(f"[MongoDB] No story found to update: {session_id}")
                return False
                
        except Exception as e:
            log_error(f"[MongoDB] Error updating story {session_id}: {e}")
            return False
    
    async def story_exists(self, session_id: str) -> bool:
        """
        Check if a story exists in MongoDB
        
        Args:
            session_id: Unique story identifier
            
        Returns:
            bool: True if story exists, False otherwise
        """
        try:
            await self._ensure_connection()
            
            count = await self._collection.count_documents({"session_id": session_id}, limit=1)
            return count > 0
            
        except Exception as e:
            log_error(f"[MongoDB] Error checking story existence {session_id}: {e}")
            return False
    
    async def get_story(self, session_id: str) -> Optional[Story]:
        """
        Retrieve a story from MongoDB
        
        Args:
            session_id: Unique story identifier
            
        Returns:
            Story object if found, None otherwise
        """
        try:
            await self._ensure_connection()
            
            doc = await self._collection.find_one({"session_id": session_id})
            
            if doc:
                return self._dict_to_story(doc)
            else:
                return None
                
        except Exception as e:
            log_error(f"[MongoDB] Error retrieving story {session_id}: {e}")
            return None
    
    async def get_stories_by_session(self, session_id: str) -> list[Story]:
        """
        Retrieve all stories for a session from MongoDB
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of Story objects for the session
        """
        try:
            await self._ensure_connection()
            
            cursor = self._collection.find({"session_id": session_id}).sort("timestamp", 1)
            stories = []
            
            async for doc in cursor:
                try:
                    story = self._dict_to_story(doc)
                    stories.append(story)
                except Exception as e:
                    log_warn(f"[MongoDB] Failed to parse story document: {e}")
                    continue
            
            return stories
            
        except Exception as e:
            log_error(f"[MongoDB] Error retrieving stories for session {session_id}: {e}")
            return []
    
    async def close_connection(self) -> None:
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._connected = False
            log_info("[MongoDB] MongoDB connection closed")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_connection()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_connection()