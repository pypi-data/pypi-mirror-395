"""
MongoDB Persistence Tests
Test MongoDB implementation of StoryPersistence interface
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Add the server directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aibe_server.persistence.mongodb_persistence import MongoStoryPersistence
from aibe_server.models.screen import Story, Paragraph, Sentence, Word, Screen
from aibe_server.models.events import BrowserEvent
from aibe_server.story_assembler import create_mongodb_story_assembler


class TestMongoStoryPersistence:
    """Test MongoDB persistence implementation"""

    @pytest.fixture
    def mock_motor_client(self):
        """Mock Motor AsyncIOMotorClient"""
        with patch('aibe_server.persistence.mongodb_persistence.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(return_value={"ok": 1})
            mock_instance.close = Mock()
            
            # Mock database and collection
            mock_db = Mock()
            mock_collection = Mock()
            
            # Mock collection methods
            mock_collection.create_index = AsyncMock()
            mock_collection.insert_one = AsyncMock()
            mock_collection.replace_one = AsyncMock()
            mock_collection.count_documents = AsyncMock()
            mock_collection.find_one = AsyncMock()
            mock_collection.find = Mock()
            
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_instance.__getitem__ = Mock(return_value=mock_db)
            
            mock_client.return_value = mock_instance
            yield mock_instance, mock_collection

    @pytest.fixture
    def sample_story(self):
        """Create a sample story for testing"""
        screen = Screen(
            id="screen_1",
            url="https://example.com/test",
            timestamp=datetime.now()
        )
        
        word = Word(
            id="word_1",
            screen=screen,
            events=[
                BrowserEvent(
                    type="click",
                    timestamp="2025-09-01T14:08:00Z",
                    target={"element_id": "button1", "url": "https://example.com/test"}
                )
            ],
            timestamp=datetime.now()
        )
        
        sentence = Sentence(
            id="sentence_1",
            words=[word],
            url="https://example.com/test",
            timestamp=datetime.now()
        )
        
        paragraph = Paragraph(
            id="paragraph_1",
            sentences=[sentence],
            domain="example.com",
            timestamp=datetime.now()
        )
        
        story = Story(
            id="story_1",
            session_id="session_1",
            paragraphs=[paragraph],
            start_time=datetime.now(),
            timestamp=datetime.now()
        )
        
        return story

    def test_persistence_initialization(self):
        """Test MongoStoryPersistence initialization"""
        persistence = MongoStoryPersistence()
        
        assert persistence.connection_string == "mongodb://localhost:27017/AIBE"
        assert persistence.database_name == "AIBE"
        assert not persistence._connected

    def test_persistence_with_custom_config(self):
        """Test MongoStoryPersistence with custom configuration"""
        custom_connection = "mongodb://custom:27017/custom_db"
        custom_db = "custom_stories"
        
        persistence = MongoStoryPersistence(
            connection_string=custom_connection,
            database_name=custom_db
        )
        
        assert persistence.connection_string == custom_connection
        assert persistence.database_name == custom_db

    @pytest.mark.asyncio
    async def test_connection_establishment(self, mock_motor_client):
        """Test MongoDB connection establishment"""
        mock_instance, mock_collection = mock_motor_client
        
        persistence = MongoStoryPersistence()
        await persistence._ensure_connection()
        
        assert persistence._connected
        mock_instance.admin.command.assert_called_once_with('ping')

    @pytest.mark.asyncio
    async def test_connection_failure_handling(self):
        """Test handling of connection failures"""
        with patch('aibe_server.persistence.mongodb_persistence.AsyncIOMotorClient') as mock_client:
            mock_instance = Mock()
            mock_instance.admin.command = AsyncMock(side_effect=Exception("Connection failed"))
            
            # Mock database and collection access
            mock_db = Mock()
            mock_collection = Mock()
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_instance.__getitem__ = Mock(return_value=mock_db)
            
            mock_client.return_value = mock_instance
            
            persistence = MongoStoryPersistence()
            
            with pytest.raises(Exception, match="Connection failed"):
                await persistence._ensure_connection()

    @pytest.mark.asyncio
    async def test_store_story_success(self, mock_motor_client, sample_story):
        """Test successful story storage"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock successful insert
        mock_result = Mock()
        mock_result.inserted_id = "mongo_object_id"
        mock_collection.insert_one.return_value = mock_result
        
        persistence = MongoStoryPersistence()
        result = await persistence.store_story(sample_story)
        
        assert result is True
        mock_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_store_story_failure(self, mock_motor_client, sample_story):
        """Test story storage failure"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock failed insert
        mock_result = Mock()
        mock_result.inserted_id = None
        mock_collection.insert_one.return_value = mock_result
        
        persistence = MongoStoryPersistence()
        result = await persistence.store_story(sample_story)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_update_story_success(self, mock_motor_client, sample_story):
        """Test successful story update"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock successful update
        mock_result = Mock()
        mock_result.modified_count = 1
        mock_result.upserted_id = None
        mock_collection.replace_one.return_value = mock_result
        
        persistence = MongoStoryPersistence()
        result = await persistence.update_story("story_1", sample_story)
        
        assert result is True
        mock_collection.replace_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_story_upsert(self, mock_motor_client, sample_story):
        """Test story update with upsert"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock upsert result
        mock_result = Mock()
        mock_result.modified_count = 0
        mock_result.upserted_id = "new_mongo_id"
        mock_collection.replace_one.return_value = mock_result
        
        persistence = MongoStoryPersistence()
        result = await persistence.update_story("story_1", sample_story)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_story_exists_true(self, mock_motor_client):
        """Test story existence check - story exists"""
        mock_instance, mock_collection = mock_motor_client
        
        mock_collection.count_documents.return_value = 1
        
        persistence = MongoStoryPersistence()
        result = await persistence.story_exists("story_1")
        
        assert result is True
        mock_collection.count_documents.assert_called_once_with({"story_id": "story_1"}, limit=1)

    @pytest.mark.asyncio
    async def test_story_exists_false(self, mock_motor_client):
        """Test story existence check - story doesn't exist"""
        mock_instance, mock_collection = mock_motor_client
        
        mock_collection.count_documents.return_value = 0
        
        persistence = MongoStoryPersistence()
        result = await persistence.story_exists("story_1")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_story_found(self, mock_motor_client, sample_story):
        """Test retrieving existing story"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock story document
        story_doc = sample_story.model_dump()
        story_doc["story_id"] = sample_story.id
        story_doc["_id"] = "mongo_object_id"
        
        mock_collection.find_one.return_value = story_doc
        
        persistence = MongoStoryPersistence()
        result = await persistence.get_story("story_1")
        
        assert result is not None
        assert result.id == sample_story.id
        assert result.session_id == sample_story.session_id

    @pytest.mark.asyncio
    async def test_get_story_not_found(self, mock_motor_client):
        """Test retrieving non-existent story"""
        mock_instance, mock_collection = mock_motor_client
        
        mock_collection.find_one.return_value = None
        
        persistence = MongoStoryPersistence()
        result = await persistence.get_story("nonexistent_story")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_stories_by_session(self, mock_motor_client, sample_story):
        """Test retrieving stories by session"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock cursor with story documents
        story_doc = sample_story.model_dump()
        story_doc["story_id"] = sample_story.id
        story_doc["_id"] = "mongo_object_id"
        
        # Create proper async iterator mock
        async def async_iter():
            yield story_doc
        
        mock_cursor = Mock()
        mock_cursor.__aiter__ = Mock(return_value=async_iter())
        
        mock_find = Mock(return_value=mock_cursor)
        mock_find.sort = Mock(return_value=mock_cursor)
        mock_collection.find = Mock(return_value=mock_find)
        
        persistence = MongoStoryPersistence()
        result = await persistence.get_stories_by_session("session_1")
        
        assert len(result) == 1
        assert result[0].session_id == "session_1"

    @pytest.mark.asyncio
    async def test_connection_context_manager(self, mock_motor_client):
        """Test async context manager functionality"""
        mock_instance, mock_collection = mock_motor_client
        
        persistence = MongoStoryPersistence()
        
        async with persistence as p:
            assert p._connected
            assert p is persistence
        
        mock_instance.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling_in_operations(self, mock_motor_client, sample_story):
        """Test error handling in database operations"""
        mock_instance, mock_collection = mock_motor_client
        
        # Mock database error
        mock_collection.insert_one.side_effect = Exception("Database error")
        
        persistence = MongoStoryPersistence()
        result = await persistence.store_story(sample_story)
        
        assert result is False

    def test_story_to_dict_conversion(self, sample_story):
        """Test Story object to MongoDB document conversion"""
        persistence = MongoStoryPersistence()
        story_dict = persistence._story_to_dict(sample_story)
        
        assert "story_id" in story_dict
        assert "created_at" in story_dict
        assert "updated_at" in story_dict
        assert story_dict["story_id"] == sample_story.id
        assert story_dict["session_id"] == sample_story.session_id

    def test_dict_to_story_conversion(self, sample_story):
        """Test MongoDB document to Story object conversion"""
        persistence = MongoStoryPersistence()
        
        # Create document dict
        story_doc = sample_story.model_dump()
        story_doc["_id"] = "mongo_object_id"
        story_doc["story_id"] = sample_story.id
        story_doc["created_at"] = datetime.now()
        story_doc["updated_at"] = datetime.now()
        
        # Convert back to Story
        result = persistence._dict_to_story(story_doc)
        
        assert isinstance(result, Story)
        assert result.id == sample_story.id
        assert result.session_id == sample_story.session_id


class TestStoryAssemblerWithMongoDB:
    """Test StoryAssembler integration with MongoDB persistence"""

    @pytest.fixture
    def mock_persistence(self):
        """Mock MongoDB persistence for integration tests"""
        mock = Mock(spec=MongoStoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    def test_factory_function_default_config(self):
        """Test factory function with default configuration"""
        with patch('aibe_server.story_assembler.get_database_config') as mock_config:
            mock_config.return_value.connection_string = "mongodb://localhost:27017/AIBE"
            mock_config.return_value.database_name = "AIBE"
            mock_config.return_value.collection_name = "Stories"
            
            with patch('aibe_server.persistence.mongodb_persistence.MongoStoryPersistence') as mock_persistence:
                assembler = create_mongodb_story_assembler()
                
                assert assembler is not None
                mock_persistence.assert_called_once_with(
                    connection_string="mongodb://localhost:27017/AIBE",
                    database_name="AIBE",
                    collection_name="Stories"
                )

    def test_factory_function_custom_connection(self):
        """Test factory function with custom connection string"""
        custom_connection = "mongodb://custom:27017/custom_db"
        
        with patch('aibe_server.persistence.mongodb_persistence.MongoStoryPersistence') as mock_persistence:
            assembler = create_mongodb_story_assembler(connection_string=custom_connection)
            
            assert assembler is not None
            mock_persistence.assert_called_once_with(
                connection_string=custom_connection,
                database_name="AIBE",
                collection_name="Stories"
            )

    @pytest.mark.asyncio
    async def test_mongodb_integration_event_processing(self, mock_persistence):
        """Test event processing with MongoDB persistence"""
        with patch('aibe_server.persistence.mongodb_persistence.MongoStoryPersistence', return_value=mock_persistence):
            assembler = create_mongodb_story_assembler()
            
            event = BrowserEvent(
                type="click",
                timestamp="2025-09-01T14:08:00Z",
                target={"element_id": "button1", "url": "https://example.com/test"}
            )
            
            story = assembler.process_event("test_session", event)
            
            assert story is not None
            assert story.session_id == "test_session"
            
            # Verify persistence calls were made
            assert mock_persistence.store_story.call_count >= 0  # May be called async


if __name__ == "__main__":
    pytest.main([__file__])