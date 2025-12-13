"""
Event models for the Browser-AI Interface Server
Pydantic models for request/response validation
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class BrowserEvent(BaseModel):
    """Browser event data structure"""
    type: str = Field(..., description="Event type (e.g., 'click', 'keyboard', 'screen_status')")
    timestamp: Optional[str] = Field(None, description="ISO timestamp")
    source: str = Field(default="user", description="Event source: 'user' or 'ai'")
    target: Optional[Union[Dict[str, Any], str, int, float, list]] = Field(None, description="Event target information")
    data: Optional[Union[Dict[str, Any], str, int, float, list]] = Field(None, description="Additional event data")
    
    model_config = ConfigDict(extra="allow")  # Allow additional fields for flexibility

    def is_screenStatus(self) -> bool:
        return self.type == "screen_status"

    def is_load(self):
        return self.type == "load"


class EventResponse(BaseModel):
    """Response for event operations"""
    success: bool
    sessionId: Optional[str] = None
    message: Optional[str] = None


class EventsListResponse(BaseModel):
    """Response containing list of events"""
    events: List[BrowserEvent]
    total: int
    sessionId: str