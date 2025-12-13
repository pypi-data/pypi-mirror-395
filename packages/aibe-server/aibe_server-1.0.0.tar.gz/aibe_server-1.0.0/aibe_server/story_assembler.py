"""
Story Assembly Implementation - Phase 2

This module implements the StoryAssembler class that processes browser events
into a hierarchical Word-Sentence-Paragraph-Story structure as specified in
the design requirements.

Key Features:
- Event processing into hierarchical structure
- Word boundary detection based on element targeting
- Sentence boundary detection based on URL changes and page loads
- Paragraph boundary detection based on domain changes
- Real-time database persistence integration
- Session lifecycle management
- Edge case handling for malformed events
"""

import asyncio
from datetime import datetime
from typing import Dict, Optional, Any, List
from urllib.parse import urlparse
import logging
from concurrent.futures import ThreadPoolExecutor

from .models.screen import Word, Sentence, Paragraph, Story, Control
from .persistence.base import StoryPersistence
from .config_manager import get_database_config

# Set up logging
logger = logging.getLogger(__name__)

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=4)




class StoryAssembler:
    """
    Processes browser events into hierarchical Story structure.
    
    Handles event-by-event processing with real-time database updates
    following the Word-Sentence-Paragraph-Story hierarchy as specified
    in the design requirements.
    """
    
    def __init__(self, persistence: StoryPersistence):
        """
        Initialize StoryAssembler with persistence interface.
        
        Args:
            persistence: Database-agnostic persistence implementation
        """
        self.persistence = persistence
        self._stories: Dict[str, Story] = {}
        self._current_words: Dict[str, Optional[Word]] = {}
        self._current_sentences: Dict[str, Optional[Sentence]] = {}
        self._current_paragraphs: Dict[str, Optional[Paragraph]] = {}
        
    async def process_event(self, session_id: str, event_data: Dict[str, Any]) -> Optional[Story]:
        """
        Process a single browser event into the story structure.
        
        Args:
            session_id: Unique session identifier
            event_data: Browser event data as dict
            
        Returns:
            Updated Story object or None if processing fails
        """
        try:
            # Filter out log, debug, heartbeat and other non-user events
            if self._should_filter_event(event_data):
                logger.debug(f"Filtering out event type: {event_data.get('type')}")
                return self._stories.get(session_id)
            
            # Get or create story for this session
            is_new_story = session_id not in self._stories
            story = self._get_or_create_story(session_id)
            
            # Extract event metadata
            event_url = self._extract_url(event_data)
            event_target = self._extract_target_element(event_data)
            
            # Handle malformed events gracefully
            if not event_url:
                # Create a default URL if missing
                event_url = "about:blank"
            
            # Check if we need a new paragraph (domain change)
            current_domain = urlparse(event_url).netloc or "localhost"
            if self._should_create_new_paragraph(session_id, current_domain):
                self._create_new_paragraph(session_id, story, current_domain)
            
            # Check if we need a new sentence (URL change or page load)
            if self._should_create_new_sentence(session_id, event_data, event_url):
                self._create_new_sentence(session_id, event_url)
            
            # Check if we need a new word (element change or after screen_status)
            if self._should_create_new_word(session_id, event_data, event_target):
                self._create_new_word(session_id, event_data, event_url)
            
            # Add event to current word using the proper addEvent method
            current_word = self._current_words.get(session_id)
            if current_word:
                word_ended = current_word.addEvent(event_data)
                # If this was a screen_status, next event will start new word
                # (handled by _should_create_new_word checking screen_status field)
                
            # Update story timestamp
            # fixme story.timestamp = datetime.now()
            
            # Write to database immediately - events are queued so we won't lose data
            try:
                if is_new_story:
                    success = await self.persistence.store_story(story)
                    logger.info(f"STORED NEW story to MongoDB: {session_id}, success: {success}")
                else:
                    success = await self.persistence.update_story(session_id, story)
                    logger.info(f"UPDATED story in MongoDB: {story.session_id}, success: {success}")
            except Exception as e:
                logger.error(f"Database write FAILED for story {story.session_id}: {e}")
            
            return story
            
        except Exception as e:
            logger.error(f"Error processing event for session {session_id}: {e}")
            return self._stories.get(session_id)
    
    def _schedule_database_update(self, story: Story, is_new_story: bool) -> None:
        """
        Schedule real-time database update for the story
        
        Args:
            story: Story object to persist
            is_new_story: True if this is a new story creation
        """
        try:
            # Real-time database update using asyncio
            loop = asyncio.get_event_loop()
            if is_new_story:
                loop.create_task(self.persistence.store_story(story))
                logger.debug(f"Scheduled new story creation for session {story.session_id}")
            else:
                loop.create_task(self.persistence.update_story(story.session_id, story))
                logger.debug(f"Scheduled story update for session {story.session_id}")
        except Exception as e:
            logger.error(f"Failed to schedule database update for story {story.session_id}: {e}")
    
    def get_story(self, session_id: str) -> Optional[Story]:
        """
        Get the current story for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Story object or None if session doesn't exist
        """
        return self._stories.get(session_id)
    
    async def close_session(self, session_id: str) -> None:
        """
        Close a session and mark the story as complete.
        
        Args:
            session_id: Session identifier to close
        """
        story = self._stories.get(session_id)
        if story:
            # Clean up session tracking
            self._current_words.pop(session_id, None)
            self._current_sentences.pop(session_id, None)
            self._current_paragraphs.pop(session_id, None)
            
            # Final database update
            self._schedule_database_update(story, is_new=False)
    
    def _get_or_create_story(self, session_id: str) -> Story:
        """Get existing story or create new one for session"""
        if session_id not in self._stories:
            story = Story(
                session_id=session_id,
                start_time=datetime.now()
            )
            self._stories[session_id] = story
            
        return self._stories[session_id]
    
    def _extract_url(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Extract URL from event data (screen_status and load events)"""
        # Priority order: direct url field, then target.url, then data.url
        url = event_data.get('url')
        if url:
            return url
        
        target = event_data.get('target')
        if target and isinstance(target, dict):
            url = target.get('url')
            if url:
                return url
        
        data = event_data.get('data')
        if data and isinstance(data, dict):
            return data.get('url')
        
        return None
    
    def _extract_target_element(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Extract target element identifier from event.

        Preference order:
        1. target.label (human-visible label used as element identity within a URL)
        2. Legacy identifier fields (element_id / id / selector / tagName) for backward compatibility.
        """
        target = event_data.get('target')

        # If target is a simple string, treat it as a label directly
        if isinstance(target, str):
            return target

        if target and isinstance(target, dict):
            # Prefer human-visible label for identity within a Sentence/URL
            label = target.get('label')
            if label:
                return label

            # Fallback: legacy identifier fields (for older event schemas)
            return (
                target.get('element_id')
                or target.get('id')
                or target.get('selector')
                or target.get('tagName')
            )
        return None
    
    def _should_create_new_paragraph(self, session_id: str, domain: str) -> bool:
        """Check if domain change requires new paragraph"""
        current_paragraph = self._current_paragraphs.get(session_id)
        if not current_paragraph:
            return True
        return current_paragraph.domain != domain
    
    def _should_create_new_sentence(self, session_id: str, event_data: Dict[str, Any], url: str) -> bool:
        """Check if URL change or page load requires new sentence"""
        current_sentence = self._current_sentences.get(session_id)
        
        # Always create new sentence for load events
        if event_data.get('type') == "load":
            return True
            
        # Create new sentence if URL changed
        if not current_sentence:
            return True
        return current_sentence.url != url
    
    def _should_create_new_word(self, session_id: str, event_data: Dict[str, Any], target_element: Optional[str]) -> bool:
        """Check if a new Word is needed based on target element.

        A Word groups all consecutive events directed at the same logical element
        (identified by label) on a given URL. `screen_status` events belong to the
        current Word but do not, by themselves, terminate it.
        """
        current_word = self._current_words.get(session_id)

        event_type = event_data.get('type')
        # screen_status events attach to the current word when present, or create
        # a new word only if no word exists yet.
        if event_type == 'screen_status':
            return current_word is None
        
        if not current_word:
            return True
        
        # Compare with last non-screen_status event's target element
        if not current_word.events:
            return True
        
        last_event_data = current_word.events[-1]
        last_target = self._extract_target_element(last_event_data)
        
        return last_target != target_element
    
    def _create_new_paragraph(self, session_id: str, story: Story, domain: str) -> None:
        """Create new paragraph for domain change"""
        paragraph = Paragraph(
            domain=domain
        )
        
        story.add_paragraph(paragraph)
        self._current_paragraphs[session_id] = paragraph
        
        # Reset sentence and word tracking for new paragraph
        self._current_sentences[session_id] = None
        self._current_words[session_id] = None
    
    def _create_new_sentence(self, session_id: str, url: str) -> None:
        """Create new sentence for URL change or page load"""
        sentence = Sentence(
            url=url
        )
        
        current_paragraph = self._current_paragraphs.get(session_id)
        if current_paragraph:
            current_paragraph.sentences.append(sentence)
        
        self._current_sentences[session_id] = sentence
        
        # Reset word tracking for new sentence
        self._current_words[session_id] = None
    
    def _create_new_word(self, session_id: str, event_data: Dict[str, Any], url: str) -> None:
        """Create new word for element change"""        
        word = Word()
        
        current_sentence = self._current_sentences.get(session_id)
        if current_sentence:
            current_sentence.words.append(word)
        
        self._current_words[session_id] = word
    
    def _should_filter_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Filter out non-user events that shouldn't contribute to Story structure
        
        Args:
            event_data: Browser event data to evaluate
            
        Returns:
            True if event should be filtered out, False if it should be processed
        """
        # Filter only log events - these are debug messages, not user interactions
        if event_data.get('type') == 'log':
            return True
            
        return False
    
    def _schedule_database_update(self, story: Story, is_new: bool) -> None:
        """Schedule database update without blocking"""
        try:
            loop = asyncio.get_event_loop()
            
            async def do_database_update():
                try:
                    if is_new:
                        success = await self.persistence.store_story(story)
                        logger.info(f"Database STORE result for story {story.session_id}: {success}")
                    else:
                        success = await self.persistence.update_story(story.session_id, story)
                        logger.info(f"Database UPDATE result for story {story.session_id}: {success}")
                except Exception as e:
                    logger.error(f"Database operation error for story {story.session_id}: {e}")
                    import traceback
                    logger.error(f"Database error traceback: {traceback.format_exc()}")
            
            # Schedule as background task
            task = loop.create_task(do_database_update())
            logger.info(f"Scheduled database {'STORE' if is_new else 'UPDATE'} for story: {story.session_id}")
            
        except Exception as e:
            logger.error(f"Failed to schedule database update for story {story.session_id}: {e}")
    
    async def _store_new_story(self, story: Story) -> None:
        """Store new story in database"""
        try:
            success = await self.persistence.store_story(story)
            if not success:
                logger.error(f"Failed to store new story: {story.session_id}")
        except Exception as e:
            logger.error(f"Error storing story {story.session_id}: {e}")
    
    async def _update_database(self, story: Story) -> None:
        """Update existing story in database"""
        try:
            # Check if story exists, otherwise store it
            if await self.persistence.story_exists(story.session_id):
                success = await self.persistence.update_story(story.session_id, story)
                if not success:
                    logger.error(f"Failed to update story: {story.session_id}")
            else:
                success = await self.persistence.store_story(story)
                if not success:
                    logger.error(f"Failed to store story: {story.session_id}")
        except Exception as e:
            logger.error(f"Error updating story {story.session_id}: {e}")


def create_mongodb_story_assembler(connection_string: str = None) -> StoryAssembler:
    """
    Factory function to create StoryAssembler with MongoDB persistence
    
    Args:
        connection_string: MongoDB connection string. If None, uses config default.
        
    Returns:
        StoryAssembler instance configured with MongoDB persistence
    """
    from .persistence.mongodb_persistence import MongoStoryPersistence
    
    if connection_string is None:
        db_config = get_database_config()
        connection_string = db_config.connection_string
        database_name = db_config.database_name
        collection_name = db_config.collection_name
    else:
        # Extract database name from connection string or use default
        database_name = "AIBE"
        collection_name = "Stories"
    
    persistence = MongoStoryPersistence(
        connection_string=connection_string,
        database_name=database_name,
        collection_name=collection_name
    )
    
    return StoryAssembler(persistence=persistence)