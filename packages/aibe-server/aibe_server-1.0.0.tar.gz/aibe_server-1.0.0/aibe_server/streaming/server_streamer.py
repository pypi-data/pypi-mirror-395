"""
ServerStreamer - MongoDB streaming for live AIBE server debugging

Captures Actor, Observer, Story, and Log events during live server operation
to enable debugging of story assembly and event processing.
"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from ..config_manager import get_server_streaming_config, get_database_config


class ServerStreamer:
    """MongoDB streaming for server debugging events"""
    
    def __init__(self, stream_prefix: str = "production"):
        """Initialize ServerStreamer with configuration from ~/.AIBE/config.json"""
        self.stream_prefix = stream_prefix
        self.read_config()  # Set initial config state
        
        # MongoDB connection
        self.mongo_client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None
        self.collection_name: Optional[str] = None
        
        # Event buffering
        self.event_buffer: List[Dict[str, Any]] = []
        self.sequence_counter = 0
        self.is_flushing_buffer = False
        self.buffer_flush_task: Optional[asyncio.Task] = None
        
        # Buffer configuration
        self.max_buffer_size = 50
        self.flush_interval_seconds = 2.0
    
    def read_config(self) -> None:
        """Read current configuration from file and update instance state"""
        self.config = get_server_streaming_config()
        self.db_config = get_database_config()
        self.is_enabled = self.config.enabled
        
    async def connect(self) -> None:
        """Connect to MongoDB and initialize collection"""
        if not self.is_enabled:
            return
            
        try:
            # Connect to MongoDB
            self.mongo_client = AsyncIOMotorClient(self.db_config.connection_string)
            self.db = self.mongo_client[self.config.database]
            
            # Generate unique collection name with date and sequence
            date_stamp = datetime.now().strftime("%Y%m%d")
            counter = 1
            
            # Find next available sequence number for this date
            while True:
                candidate_name = f"{self.config.collection_prefix}{date_stamp}_{counter:03d}"
                existing_collections = await self.db.list_collection_names()
                if candidate_name not in existing_collections:
                    self.collection_name = candidate_name
                    break
                counter += 1
            self.collection = self.db[self.collection_name]
            
            # Create index for efficient timestamp queries
            await self.collection.create_index("timestamp")
            
            # Connected to MongoDB (silent operation)
            
            # Start periodic buffer flush task
            self.buffer_flush_task = asyncio.create_task(self._periodic_flush())
            
        except Exception as error:
            # Connection failed (silent operation)
            self.is_enabled = False
            
    async def disconnect(self) -> None:
        """Disconnect from MongoDB and flush remaining events"""
        if not self.is_enabled:
            return
            
        try:
            # Cancel periodic flush task
            if self.buffer_flush_task:
                self.buffer_flush_task.cancel()
                try:
                    await self.buffer_flush_task
                except asyncio.CancelledError:
                    pass
            
            # Flush remaining events
            await self._flush_buffer()
            
            # Close MongoDB connection
            if self.mongo_client:
                self.mongo_client.close()
                
            # Disconnected from MongoDB (silent operation)
            
        except Exception as error:
            # Disconnect error (silent operation)
            pass
    
    async def stream_event(self, event_data: Dict[str, Any]) -> None:
        """Add event to buffer for streaming to MongoDB"""
        if not self.is_enabled or self.collection is None:
            return
            
        try:
            # Enrich event with sequence and timestamp (ISO format)
            enriched_event = {
                **event_data,
                "sequence": self.sequence_counter,
                "timestamp": datetime.now().isoformat()
            }
            
            self.sequence_counter += 1
            self.event_buffer.append(enriched_event)
            
            # Flush buffer if it's getting full
            if len(self.event_buffer) >= self.max_buffer_size:
                await self._flush_buffer()
                
        except Exception as error:
            # Streaming error (silent operation)
            pass
    
    async def stream_observer_event(self, session_id: str, event_data: Dict[str, Any]) -> None:
        """Stream an Observer event (incoming browser event)"""
        if not self.config.stream_observer:
            return
        await self.stream_event({
            "stream": "Observer",
            "session_id": session_id,
            **event_data
        })
    
    async def stream_actor_event(self, session_id: str, command_data: Dict[str, Any]) -> None:
        """Stream an Actor event (outgoing command to browser)"""
        if not self.config.stream_actor:
            return
        await self.stream_event({
            "stream": "Actor", 
            "session_id": session_id,
            **command_data
        })
    
    async def stream_story_event(self, session_id: str, story_data: Dict[str, Any]) -> None:
        """Stream a Story event (story assembly state)"""
        if not self.config.stream_story:
            return
        await self.stream_event({
            "stream": "Story",
            "session_id": session_id,
            **story_data
        })
    
    async def stream_log_event(self, level: str, message: str, session_id: Optional[str] = None) -> None:
        """Stream a Log event (server logging)"""
        if not self.config.stream_log:
            return
        await self.stream_event({
            "stream": "Log",
            "level": level,
            "message": message,
            "session_id": session_id
        })
    
    async def _flush_buffer(self) -> None:
        """Flush buffered events to MongoDB"""
        if not self.is_enabled or self.collection is None or self.is_flushing_buffer or not self.event_buffer:
            return
            
        self.is_flushing_buffer = True
        
        try:
            # Get current buffer and clear it
            events_to_write = self.event_buffer.copy()
            self.event_buffer.clear()
            
            # Write to MongoDB
            if events_to_write:
                await self.collection.insert_many(events_to_write)
                
        except Exception as error:
            # Buffer flush error (silent operation)
            # Put events back in buffer if write failed
            self.event_buffer.extend(events_to_write)
            
        finally:
            self.is_flushing_buffer = False
    
    async def _periodic_flush(self) -> None:
        """Periodic task to flush buffer every few seconds"""
        try:
            while True:
                await asyncio.sleep(self.flush_interval_seconds)
                await self._flush_buffer()
        except asyncio.CancelledError:
            # Task was cancelled during shutdown
            pass
        except Exception as error:
            # Periodic flush error (silent operation)
            pass
    
    def get_collection_name(self) -> Optional[str]:
        """Get the current collection name for monitoring"""
        return self.collection_name
    
    def get_buffer_size(self) -> int:
        """Get current buffer size for monitoring"""
        return len(self.event_buffer)
    
    def is_connected(self) -> bool:
        """Check if ServerStreamer is connected and ready"""
        return self.is_enabled and self.collection is not None
    
    async def reload_config(self) -> None:
        """Reload configuration from file and reconnect if needed"""
        # Store old enabled state
        old_enabled = self.is_enabled
        
        # Read current config from file
        self.read_config()
        
        # If streaming was disabled, disconnect
        if old_enabled and not self.is_enabled:
            await self.disconnect()
        
        # If streaming was enabled or settings changed, reconnect
        elif self.is_enabled:
            await self.disconnect()  # Disconnect first to ensure clean state
            await self.connect()     # Reconnect with new settings


# Global ServerStreamer instance
_server_streamer: Optional[ServerStreamer] = None


async def get_server_streamer() -> Optional[ServerStreamer]:
    """Get the global ServerStreamer instance, creating it if needed"""
    global _server_streamer
    
    if _server_streamer is None:
        _server_streamer = ServerStreamer()
        if _server_streamer.is_enabled:
            await _server_streamer.connect()
    
    return _server_streamer


async def shutdown_server_streamer() -> None:
    """Shutdown the global ServerStreamer instance"""
    global _server_streamer
    
    if _server_streamer:
        await _server_streamer.disconnect()
        _server_streamer = None


async def reload_server_streamer() -> Optional[ServerStreamer]:
    """Reload the global ServerStreamer configuration from file"""
    global _server_streamer
    
    if _server_streamer:
        await _server_streamer.reload_config()
    else:
        # Create new instance if one doesn't exist
        _server_streamer = ServerStreamer()
        if _server_streamer.is_enabled:
            await _server_streamer.connect()
    
    # Return the instance if enabled and connected (has collection_name)
    if _server_streamer and _server_streamer.is_enabled and hasattr(_server_streamer, 'collection_name') and _server_streamer.collection_name:
        return _server_streamer
    elif _server_streamer and _server_streamer.is_enabled:
        # Enabled but not connected - this shouldn't happen but let's be defensive
        await _server_streamer.connect()
        return _server_streamer if hasattr(_server_streamer, 'collection_name') and _server_streamer.collection_name else None
    else:
        return None