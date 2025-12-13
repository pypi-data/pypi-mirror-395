# Memory Hub Best Practices
**ticket_id:** memory-hub-usage  
**app_id:** global  
**project_id:** workflow

## A. Content Detail Preservation & Formatting for Storage

When storing information in the Memory Hub, preserve maximum detail from source material. The semantic chunking system handles large context windows, so prioritize completeness over brevity:

- **Reorganize for clarity** - restructure information logically but maintain all content
- **Preserve technical specifics** - exact names, processes, relationships, constraints
- **Maintain structural elements** - keep bullet points, sequences, distinctions between current/future states
- **Standardize terminology** - ensure consistent naming while preserving all original concepts
- **DO NOT summarize or condense** - avoid converting detailed information into flowing prose that loses specificity
- **Your role is reorganization, not summarization**
- **Enhance with markdown structure** - if source content lacks markdown formatting, add appropriate headers (##, ###), bullet points, numbered lists, and emphasis to improve semantic chunking and retrieval. Convert plain text sections into structured markdown while preserving all original information.

## B. Document Chunking Strategy (Agent Awareness)

The Memory Hub uses semantic chunking (semchunk) for optimal content division:

- **Preserve markdown structure** - maintain headers (##, ###), bullet points, numbered lists, and document hierarchy
- **Single document ingestion** - do NOT pre-chunk documents unless they exceed 12,000 tokens
- **Let semchunk decide** - semantic chunking finds natural break points better than manual division
- **Structure is semantic** - markdown hierarchy provides valuable context for AI understanding and retrieval
- **Cross-section synthesis** - connected content enables our strongest feature (outstanding cross-section information synthesis)

## C. Metadata for Stored Memories

**Crucial Metadata (`metadata`):** ALWAYS include:

- `app_id`: (Required).
- `project_id`: (Optional, provide if context is project-specific or more granular).
- `ticket_id`: (Optional, provide if context is ticket-specific).
- `type`: (Choose from the PREDEFINED LIST below. If you believe a new `type` is genuinely needed for a novel kind of information, please propose it to the User for approval before using it. Your goal is to categorize information consistently.)
- `version`: Integer. Start at 1. If updating an existing specific item at its correct hierarchy level, find its latest version and store new as `version + 1`.
- `timestamp_iso`: Current ISO 8601 timestamp.
- `keywords`: A list of 3-5 relevant keywords. 