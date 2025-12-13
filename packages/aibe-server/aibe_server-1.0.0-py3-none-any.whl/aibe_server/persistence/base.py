"""
Base persistence interface for Story Assembly
Abstract base class for database-agnostic storage
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..models.screen import Story


class StoryPersistence(ABC):
    """Abstract persistence interface for database-agnostic storage"""
    
    @abstractmethod
    async def store_story(self, story: Story) -> bool:
        """
        Store a new story in the database
        
        Args:
            story: Story object to store
            
        Returns:
            bool: True if stored successfully, False otherwise
        """
        raise NotImplementedError
    
    @abstractmethod
    async def update_story(self, story_id: str, story: Story) -> bool:
        """
        Update an existing story in the database
        
        Args:
            story_id: Unique story identifier
            story: Updated Story object
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        raise NotImplementedError
    
    @abstractmethod
    async def story_exists(self, story_id: str) -> bool:
        """
        Check if a story exists in the database
        
        Args:
            story_id: Unique story identifier
            
        Returns:
            bool: True if story exists, False otherwise
        """
        raise NotImplementedError