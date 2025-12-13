"""
Persistence layer for the Browser-AI Interface Server
Database-agnostic persistence implementations
"""

from .base import StoryPersistence
from .mongodb_persistence import MongoStoryPersistence

__all__ = ['StoryPersistence', 'MongoStoryPersistence']