"""
Services package for the Browser-AI Interface Server
Contains business logic services that integrate different system components
"""

from .story_integration import (
    StoryIntegrationService, 
    ObserverStoryBridge,
    get_story_integration_service,
    get_observer_story_bridge
)

__all__ = [
    'StoryIntegrationService', 
    'ObserverStoryBridge',
    'get_story_integration_service',
    'get_observer_story_bridge'
]