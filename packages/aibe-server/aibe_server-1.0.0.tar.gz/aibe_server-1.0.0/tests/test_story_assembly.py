"""
Story Assembly Tests - Phase 1 (TDD Implementation)

These tests define the expected behavior of the StoryAssembler class
before implementation. All tests should initially FAIL as required by TDD methodology.

Test Coverage:
- Core StoryAssembler functionality
- Event processing into hierarchical Word-Sentence-Paragraph-Story structure
- Boundary detection rules (Word, Sentence, Paragraph)
- Edge cases: empty sessions, single events, rapid switching, URL changes
- Abstract persistence interface integration
- Real-time database updates
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from typing import List, Optional
import sys
import os

# Add the server directory to the path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from aibe_server.models.events import BrowserEvent
from aibe_server.models.screen import Word, Sentence, Paragraph, Story, Screen, Control


# Abstract Persistence Interface (as specified in design requirements)
class StoryPersistence:
    """Abstract persistence interface for database-agnostic storage"""
    async def store_story(self, story: Story) -> bool:
        raise NotImplementedError
    
    async def update_story(self, story_id: str, story: Story) -> bool:
        raise NotImplementedError
    
    async def story_exists(self, story_id: str) -> bool:
        raise NotImplementedError


class TestStoryAssemblerCore:
    """Test core StoryAssembler class functionality"""

    def test_story_assembler_instantiation(self):
        """StoryAssembler should instantiate with persistence interface"""
        mock_persistence = Mock(spec=StoryPersistence)
        
        # This will fail - StoryAssembler doesn't exist yet
        from aibe_server.story_assembler import StoryAssembler
        assembler = StoryAssembler(persistence=mock_persistence)
        assert assembler is not None
        assert assembler.persistence == mock_persistence

    def test_story_assembler_has_required_methods(self):
        """StoryAssembler should have all required public methods"""
        mock_persistence = Mock(spec=StoryPersistence)
        from aibe_server.story_assembler import StoryAssembler
        
        assembler = StoryAssembler(persistence=mock_persistence)
        
        # Required methods per design requirements
        assert hasattr(assembler, 'process_event')
        assert hasattr(assembler, 'get_story')
        assert hasattr(assembler, 'close_session')
        assert callable(assembler.process_event)
        assert callable(assembler.get_story)
        assert callable(assembler.close_session)


class TestEventProcessing:
    """Test event processing into hierarchical structure"""

    @pytest.fixture
    def mock_persistence(self):
        """Mock persistence layer for testing"""
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        """Story assembler instance for testing"""
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    def test_single_event_creates_word(self, assembler):
        """Single event should create a Word within a Sentence within a Paragraph within a Story"""
        session_id = "test_session_1"
        event = BrowserEvent(
            type="click",
            timestamp="2025-09-01T13:35:00Z",
            target={"element_id": "submit_button", "url": "https://example.com/form"}
        )

        story = assembler.process_event(session_id, event)
        
        assert story is not None
        assert story.session_id == session_id
        assert len(story.paragraphs) == 1
        assert len(story.paragraphs[0].sentences) == 1
        assert len(story.paragraphs[0].sentences[0].words) == 1
        assert len(story.paragraphs[0].sentences[0].words[0].events) == 1

    def test_same_element_events_create_single_word(self, assembler):
        """Multiple events targeting same element should create single Word"""
        session_id = "test_session_2"
        
        events = [
            BrowserEvent(type="focus", timestamp="2025-09-01T13:35:00Z", 
                        target={"element_id": "email_input", "url": "https://example.com/login"}),
            BrowserEvent(type="keyboard", timestamp="2025-09-01T13:35:01Z", 
                        target={"element_id": "email_input", "url": "https://example.com/login"}),
            BrowserEvent(type="keyboard", timestamp="2025-09-01T13:35:02Z", 
                        target={"element_id": "email_input", "url": "https://example.com/login"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        assert len(story.paragraphs[0].sentences[0].words) == 1
        assert len(story.paragraphs[0].sentences[0].words[0].events) == 3

    def test_different_elements_create_multiple_words(self, assembler):
        """Events targeting different elements should create separate Words"""
        session_id = "test_session_3"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "email_input", "url": "https://example.com/login"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:01Z",
                        target={"element_id": "password_input", "url": "https://example.com/login"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        assert len(story.paragraphs[0].sentences[0].words) == 2


class TestSentenceBoundaries:
    """Test Sentence boundary detection based on URL changes"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    def test_url_change_creates_new_sentence(self, assembler):
        """URL change should trigger new Sentence creation"""
        session_id = "test_session_4"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "link1", "url": "https://example.com/page1"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:01Z",
                        target={"url": "https://example.com/page2"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "button1", "url": "https://example.com/page2"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should have 2 sentences (URL changed from page1 to page2)
        assert len(story.paragraphs[0].sentences) == 2

    def test_page_load_creates_new_sentence(self, assembler):
        """Page load event should trigger new Sentence creation"""
        session_id = "test_session_5"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "submit", "url": "https://example.com/form"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:01Z",
                        target={"url": "https://example.com/form"}),  # Same URL but reload
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "button1", "url": "https://example.com/form"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should have 2 sentences (page reload triggered new sentence)
        assert len(story.paragraphs[0].sentences) == 2

    def test_form_submission_with_redirect_creates_new_sentence(self, assembler):
        """Form submission with redirect should create new Sentence"""
        session_id = "test_session_6"
        
        events = [
            BrowserEvent(type="submit", timestamp="2025-09-01T13:35:00Z",
                        target={"form_id": "login_form", "url": "https://example.com/login"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:01Z",
                        target={"url": "https://example.com/dashboard"}),  # Redirected
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "menu_item", "url": "https://example.com/dashboard"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should have 2 sentences (redirect after form submission)
        assert len(story.paragraphs[0].sentences) == 2


class TestParagraphBoundaries:
    """Test Paragraph boundary detection based on domain changes"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    def test_domain_change_creates_new_paragraph(self, assembler):
        """Domain change should trigger new Paragraph creation"""
        session_id = "test_session_7"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "link1", "url": "https://site1.com/page1"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:01Z",
                        target={"url": "https://site2.com/page1"}),  # Different domain
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "button1", "url": "https://site2.com/page1"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should have 2 paragraphs (domain changed from site1.com to site2.com)
        assert len(story.paragraphs) == 2

    def test_subdomain_change_creates_new_paragraph(self, assembler):
        """Subdomain change should trigger new Paragraph creation"""
        session_id = "test_session_8"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "link1", "url": "https://www.example.com/page1"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:01Z",
                        target={"url": "https://api.example.com/data"}),  # Different subdomain
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "button1", "url": "https://api.example.com/data"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should have 2 paragraphs (subdomain changed)
        assert len(story.paragraphs) == 2


class TestStorySessionManagement:
    """Test Story session lifecycle management"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    def test_get_story_returns_current_story(self, assembler):
        """get_story() should return current story for session"""
        session_id = "test_session_9"
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        assembler.process_event(session_id, event)
        story = assembler.get_story(session_id)
        
        assert story is not None
        assert story.session_id == session_id
        assert not story.is_closed

    def test_close_session_marks_story_closed(self, assembler):
        """close_session() should mark story as closed with end_time"""
        session_id = "test_session_10"
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        assembler.process_event(session_id, event)
        assembler.close_session(session_id)
        
        story = assembler.get_story(session_id)
        assert story.is_closed
        assert story.end_time is not None

    def test_multiple_sessions_isolated(self, assembler):
        """Multiple sessions should be isolated from each other"""
        session1 = "test_session_11"
        session2 = "test_session_12"
        
        event1 = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                            target={"element_id": "button1", "url": "https://example.com/page1"})
        event2 = BrowserEvent(type="click", timestamp="2025-09-01T13:35:01Z",
                            target={"element_id": "button2", "url": "https://different.com/page1"})
        
        assembler.process_event(session1, event1)
        assembler.process_event(session2, event2)
        
        story1 = assembler.get_story(session1)
        story2 = assembler.get_story(session2)
        
        assert story1.session_id == session1
        assert story2.session_id == session2
        assert story1.paragraphs[0].domain != story2.paragraphs[0].domain


class TestEdgeCases:
    """Test edge cases: empty sessions, single events, rapid switching, URL changes"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    def test_empty_session_returns_none(self, assembler):
        """get_story() for non-existent session should return None"""
        story = assembler.get_story("non_existent_session")
        assert story is None

    def test_single_event_creates_complete_hierarchy(self, assembler):
        """Single event should create complete Story->Paragraph->Sentence->Word hierarchy"""
        session_id = "test_session_13"
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        story = assembler.process_event(session_id, event)
        
        assert len(story.paragraphs) == 1
        assert len(story.paragraphs[0].sentences) == 1
        assert len(story.paragraphs[0].sentences[0].words) == 1
        assert len(story.paragraphs[0].sentences[0].words[0].events) == 1

    def test_rapid_element_switching(self, assembler):
        """Rapid switching between elements should create separate Words"""
        session_id = "test_session_14"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "button1", "url": "https://example.com/page1"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",  # Same timestamp
                        target={"element_id": "button2", "url": "https://example.com/page1"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",  # Same timestamp
                        target={"element_id": "button1", "url": "https://example.com/page1"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",  # Same timestamp
                        target={"element_id": "button2", "url": "https://example.com/page1"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should create 4 separate Words due to element switching
        assert len(story.paragraphs[0].sentences[0].words) == 4

    def test_rapid_url_changes(self, assembler):
        """Rapid URL changes should create separate Sentences"""
        session_id = "test_session_15"
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "link1", "url": "https://example.com/page1"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:00Z",
                        target={"url": "https://example.com/page2"}),
            BrowserEvent(type="load", timestamp="2025-09-01T13:35:00Z",
                        target={"url": "https://example.com/page3"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:01Z",
                        target={"element_id": "button1", "url": "https://example.com/page3"})
        ]

        story = None
        for event in events:
            story = assembler.process_event(session_id, event)

        # Should create 3 separate Sentences due to URL changes
        assert len(story.paragraphs[0].sentences) == 3

    def test_malformed_event_handling(self, assembler):
        """Malformed events should be handled gracefully"""
        session_id = "test_session_16"
        
        # Event with missing target information
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z")
        
        # Should not raise exception
        story = assembler.process_event(session_id, event)
        assert story is not None


class TestPersistenceIntegration:
    """Test integration with abstract persistence interface"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    @pytest.mark.asyncio
    async def test_first_event_calls_store_story(self, assembler, mock_persistence):
        """First event in session should call store_story()"""
        session_id = "test_session_17"
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        assembler.process_event(session_id, event)
        
        # Should call store_story for new session
        mock_persistence.store_story.assert_called_once()

    @pytest.mark.asyncio
    async def test_subsequent_events_call_update_story(self, assembler, mock_persistence):
        """Subsequent events should call update_story()"""
        session_id = "test_session_18"
        
        # Mock existing story
        mock_persistence.story_exists.return_value = True
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "button1", "url": "https://example.com/page1"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:01Z",
                        target={"element_id": "button2", "url": "https://example.com/page1"})
        ]

        for event in events:
            assembler.process_event(session_id, event)

        # Should call update_story for existing session
        assert mock_persistence.update_story.call_count >= 1

    @pytest.mark.asyncio
    async def test_persistence_failure_handling(self, assembler, mock_persistence):
        """Persistence failures should be handled gracefully"""
        session_id = "test_session_19"
        
        # Mock persistence failure
        mock_persistence.store_story.return_value = False
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        # Should not raise exception even if persistence fails
        story = assembler.process_event(session_id, event)
        assert story is not None

    def test_no_empty_structures_persisted(self, assembler, mock_persistence):
        """Empty structures should not be persisted per design requirements"""
        session_id = "test_session_20"
        
        # Just getting story without events should not trigger persistence
        story = assembler.get_story(session_id)
        
        # Should not call store_story for empty session
        mock_persistence.store_story.assert_not_called()
        mock_persistence.update_story.assert_not_called()


class TestRealTimeUpdates:
    """Test real-time database update behavior"""

    @pytest.fixture
    def mock_persistence(self):
        mock = Mock(spec=StoryPersistence)
        mock.store_story = AsyncMock(return_value=True)
        mock.update_story = AsyncMock(return_value=True)
        mock.story_exists = AsyncMock(return_value=False)
        return mock

    @pytest.fixture
    def assembler(self, mock_persistence):
        from aibe_server.story_assembler import StoryAssembler
        return StoryAssembler(persistence=mock_persistence)

    @pytest.mark.asyncio
    async def test_each_event_triggers_database_update(self, assembler, mock_persistence):
        """Each event should trigger immediate database update per design requirements"""
        session_id = "test_session_21"
        
        # Mock existing story after first event
        mock_persistence.story_exists.side_effect = [False, True, True]
        
        events = [
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                        target={"element_id": "button1", "url": "https://example.com/page1"}),
            BrowserEvent(type="keyboard", timestamp="2025-09-01T13:35:01Z",
                        target={"element_id": "input1", "url": "https://example.com/page1"}),
            BrowserEvent(type="click", timestamp="2025-09-01T13:35:02Z",
                        target={"element_id": "button2", "url": "https://example.com/page1"})
        ]

        for event in events:
            assembler.process_event(session_id, event)

        # First event should call store_story, subsequent should call update_story
        mock_persistence.store_story.assert_called_once()
        assert mock_persistence.update_story.call_count >= 2

    @pytest.mark.asyncio 
    async def test_session_close_triggers_final_update(self, assembler, mock_persistence):
        """Closing session should trigger final database update"""
        session_id = "test_session_22"
        
        event = BrowserEvent(type="click", timestamp="2025-09-01T13:35:00Z",
                           target={"element_id": "button1", "url": "https://example.com/page1"})
        
        assembler.process_event(session_id, event)
        assembler.close_session(session_id)
        
        # Should have called update_story for session close
        assert mock_persistence.update_story.call_count >= 1


if __name__ == "__main__":
    pytest.main([__file__])
