# Design Requirements -- Story Assembly and Database Storage

## Overview

The goal of this document is to guide the coding of the StoryAssembler and eventual database artifact storage with a database-agnostic persistence layer. 

## Use TDD Method

Use the Test Driven Development method to write the implementation of these requirements. Development will be done in four phases:

1. **Phase 1:** Implement Story Assembly tests
   - Tests validate correct Story-Paragraph-Sentence-Word structure creation from Observer channel events
   - Include edge cases: empty sessions, single events, rapid element switching, URL changes
   - Verify all tests initially fail (TDD requirement)

2. **Phase 2:** Implement Story Assembly logic
   - Build StoryAssembler class that processes events into hierarchical structure
   - Handle event queuing and sequential processing per tab session
   - Ensure all Phase 1 tests pass

3. **Phase 3:** Implement database persistence tests
   - Tests validate Story creation and updates through abstract persistence interface
   - Include mock database implementations for testing
   - Test real-time update behavior and empty structure filtering
   - Verify all tests initially fail (TDD requirement)

4. **Phase 4:** Implement database persistence layer
   - Build abstract StoryPersistence interface
   - Create concrete implementation (initially for one database type)
   - Integrate with StoryAssembler for real-time updates
   - Ensure all Phase 3 tests pass

## Implementation

### Coding standards

The coding standard document for this project is PRD-Code_Style.md, in the root of the project. You must follow it, or else ask for and be granted an exception to its requirements.

Also refer to CLAUDE.md for project context and to  server/aibe_server/models/events.py for data structures.
### Data Models

The hierarchical structure requires clear data models for each level:

**Event:** Individual browser interaction (click, keypress, load, etc.)
**Word:** Collection of events targeting same element
**Sentence:** Collection of words within same page context (URL)  
**Paragraph:** Collection of sentences within same domain
**Story:** Complete collection of paragraphs for a tab session (open to close)

**Key Identifiers:**
- **Story ID:** Unique tab session identifier
- **Element Target:** For Word boundaries (CSS selector, element ID, or label)
- **URL:** For Sentence boundaries (full URL including hash/query)
- **Domain:** For Paragraph boundaries (hostname only)

### Story Assembly

Events from the Observer channel are assembled, event by event, into Words, then Sentences, Paragraphs, and finally into a complete Story. A Story captures whatever actually happens in a browser tab from open to close - this may be focused work, random browsing, tangents, or any combination. Stories record actual human web behavior without assuming intentionality or goal-oriented sequences. 

#### Word

A Word is defined as the complete sequence of events directed at a single page element. This approach ensures Words represent logical interaction units rather than timing-dependent fragments.

**Word Boundary Rules:**
- **New Word starts when:** Target element changes (different element receiving events)
- **Word ends when:** Next event targets a different element OR session ends
- **Status Updates:** Provide validation that screen state matches expected result of Word's events, protecting against missed AJAX changes that might affect other fields

**Example:** Typing "john@email.com" in an email field = 1 Word (all events target same email input element)

#### Sentence

A Sentence is the sequential list of Words directed at a single page context (URL + page state). 

**New Sentence Triggers:**
- **Page Load events** (navigation, refresh, back/forward)
- **URL changes** (including same URL reloads)
- **Form submissions with navigation** (GET forms, POST redirects)
- **AJAX navigation** that updates browser history/URL

**Ambiguity Note:** Form submission behavior varies - some POST forms redirect (new Sentence), others update in place (same Sentence). The system relies on observing actual URL/load events rather than predicting form behavior.

**Note:** AJAX submissions without navigation changes stay within the current Sentence.

When a new Sentence starts, it contains all subsequent Words until the next Sentence trigger occurs.

#### Paragraph

The sequence of all consecutive Sentences aimed at the same URL domain, is a Paragraph.

#### Story

The story is the sequential list of all paragraphs from the time a browser tab is opened (session begins) to the time it is closed.

#### Immediate Database Update

Each time the Story-Paragraph-Sentence-Word structure is updated by adding a new event, it's record in the database is to be updated, ensuring that up-to-date data is always available to database clients.

#### Events

Events are delivered by the Observer channel for processing, one at a time. The entire Story-Paragraph-Sentence-Word structure is updated with the addition of each new event, and then the database document for the Story needs also to be updated.

### Database Abstraction Layer

The implementation must use a database-agnostic persistence interface to avoid lock-in to specific database technologies.

**Abstract Persistence Interface:**
```python
class StoryPersistence:
    async def store_story(self, story: Story) -> bool
    async def update_story(self, story_id: str, story: Story) -> bool
    async def story_exists(self, story_id: str) -> bool
```

**Implementation Notes:**
- Concrete implementations (MongoDB, PostgreSQL, etc.) implement this interface
- Story assembly logic remains database-agnostic
- Configuration determines which persistence backend to use

### Event Processing Pipeline

**Event Flow:**
1. **Observer Channel** → Events arrive from browser extension
2. **Event Queue** → Buffer events for processing (handles DB performance variations) 
3. **Story Assembler** → Processes events sequentially, updates Story structure
4. **Persistence Layer** → Writes updated Story to database

**Threading Considerations:**
- Events processed sequentially per tab session (maintains Word/Sentence ordering)
- Database writes asynchronous to avoid blocking event processing
- Queue provides backpressure protection if database is slow

### Database Update Rules

- **No empty structures:** Stories, Paragraphs, Sentences, or Words are not written until they contain at least one event
- **Real-time updates:** As soon as a new event is added and the Story structure is updated, the database document must be updated
- **Incremental writes:** Only the changed Story is written (not all Stories for the session)
