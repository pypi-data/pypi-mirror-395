"""
Screen models for the Browser-AI Interface Server
Pydantic models for screen composition with controls and timestamps
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class Control(BaseModel):
    """Base control model for screen elements"""
    id: str = Field(..., description="Unique control identifier")
    type: str = Field(..., description="Control type (e.g., button, input, text)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Control properties")
    position: Optional[int] = Field(None, description="Position in the control list")
    
    model_config = ConfigDict(extra="allow")  # Allow additional fields for flexibility


class Screen(BaseModel):
    """Screen model composed of an ordered list of controls and a datetime timestamp"""
    id: str = Field(..., description="Unique screen identifier")
    url: str = Field(..., description="Screen URL")
    controls: List[Control] = Field(default_factory=list, description="Ordered list of controls")
    timestamp: datetime = Field(default_factory=datetime.now, description="Screen creation/update timestamp")
    title: Optional[str] = Field(None, description="Screen title")
    description: Optional[str] = Field(None, description="Screen description")
    
    def add_control(self, control: Control) -> None:
        """Add a control to the screen at the end of the list"""
        control.position = len(self.controls)
        self.controls.append(control)
        self.timestamp = datetime.now()
    
    def insert_control(self, index: int, control: Control) -> None:
        """Insert a control at a specific position in the list"""
        if index < 0 or index > len(self.controls):
            raise ValueError(f"Index {index} out of range for controls list")
        
        control.position = index
        self.controls.insert(index, control)
        
        # Update positions for controls after the inserted one
        for i in range(index + 1, len(self.controls)):
            self.controls[i].position = i
        
        self.timestamp = datetime.now()
    
    def remove_control(self, control_id: str) -> bool:
        """Remove a control by its ID. Returns True if control was found and removed."""
        for i, control in enumerate(self.controls):
            if control.id == control_id:
                self.controls.pop(i)
                # Update positions for remaining controls
                for j in range(i, len(self.controls)):
                    self.controls[j].position = j
                self.timestamp = datetime.now()
                return True
        return False
    
    def get_control_by_id(self, control_id: str) -> Optional[Control]:
        """Get a control by its ID"""
        for control in self.controls:
            if control.id == control_id:
                return control
        return None
    
    model_config = ConfigDict(extra="allow")  # Allow additional fields for flexibility

    @field_serializer('timestamp')
    def serialize_timestamp(self, timestamp: datetime) -> str:
        return timestamp.isoformat()


class Word(BaseModel):
    """Word model composed of a list of event data dicts and an optional screen_status.

    A Word groups all events directed at a single logical element on a page.
    `screen_status` events are associated with the Word as the resulting screen
    snapshot, but they do not, by themselves, terminate the Word.
    """
    events: List[Dict[str, Any]] = Field(default_factory=list, description="List of browser event data")
    screen_status: Optional[Dict[str, Any]] = Field(None, description="Associated screen_status event data")
    
    model_config = ConfigDict(extra="allow")
    
    def addEvent(self, event_data: Dict[str, Any]) -> bool:
        """Add event to word.

        - `screen_status` events are stored in `screen_status` (not in `events`).
        - Other events are appended to `events`.
        - The return value is retained for backward compatibility but is not
          used to signal end-of-word.
        """
        
        # Check if this is a screen_status event
        if event_data.get('type') == 'screen_status':
            # Store the entire screen_status event data (not in events list)
            self.screen_status = event_data
            # Do not treat screen_status as a word terminator; subsequent events
            # for the same element remain in this Word.
            return False
        
        # Add regular events to the events list
        self.events.append(event_data)
        return False

    def lastEvent(self) -> Optional[Dict[str, Any]]:
        if len(self.events) == 0:
            return None
        return self.events[-1]

class Sentence(BaseModel):
    """Sentence model composed of a list of Words, all related to the same Screen.URL"""
    words: List[Word] = Field(default_factory=list, description="List of words")
    url: Optional[str] = Field(None, description="Common URL for all words in the sentence")

    def addWord(self, word: Word) -> bool:
        """Add a word to the sentence, ensuring all words share the same URL"""
        # For now, just add words to sentence - URL logic handled in story_assembler
        self.words.append(word)
        return False

    model_config = ConfigDict(extra="allow")


class Paragraph(BaseModel):
    """Paragraph model composed of a list of Sentences, all related to the same Screen.URL.Domain"""
    sentences: List[Sentence] = Field(default_factory=list, description="List of sentences")
    domain: Optional[str] = Field(None, description="Common domain for all sentences in the paragraph")
    
    def add_sentence(self, sentence: Sentence) -> None:
        """Add a sentence to the paragraph, ensuring all sentences share the same domain"""
        if sentence.url:
            sentence_domain = urlparse(sentence.url).netloc
            
            if self.sentences and self.domain:
                if sentence_domain != self.domain:
                    raise ValueError(f"Sentence domain {sentence_domain} does not match paragraph domain {self.domain}")
            
            if not self.sentences:
                self.domain = sentence_domain
        
        self.sentences.append(sentence)
    
    model_config = ConfigDict(extra="allow")


class Story(BaseModel):
    """Story model composed of a list of Paragraphs, from session start to close"""
    session_id: str = Field(..., description="Session identifier")
    paragraphs: List[Paragraph] = Field(default_factory=list, description="List of paragraphs")
    
    def add_paragraph(self, paragraph: Paragraph) -> None:
        """Add a paragraph to the story"""
        self.paragraphs.append(paragraph)
    
    model_config = ConfigDict(extra="allow")