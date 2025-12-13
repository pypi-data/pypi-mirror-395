 Revised Proposal: dev-session Skill (Generic)

  Core Concept

  The skill works in any project by:
  1. Detecting current project from working directory or CLAUDE.md
  2. Using consistent Memory Hub structure across all projects
  3. Providing the same commands everywhere

  Memory Hub Structure (Per-Project)

  Every project using this pattern has:
  app_id: <detected from CLAUDE.md or folder name>
  project_id: <detected from CLAUDE.md or folder name>
  ticket_id: _session   ← Reserved system ticket

  The _session memory contains:
  active_ticket: <current working ticket>
  focus: <what we're actively working on>
  recent_decisions: [...]
  blocking: <any blockers>
  next_steps: [...]
  env_notes: <model configs, feature flags, etc>
  last_updated: <timestamp>

  Commands

  | Command         | Description                                                                      |
  |-----------------|----------------------------------------------------------------------------------|
  | resume          | Load _session index + last 3 memories from active ticket. Display current state. |
  | tickets         | List all tickets in current project with memory counts                           |
  | switch <ticket> | Change active ticket, update _session index                                      |
  | save [note]     | Update _session with current context, optionally add memory to active ticket     |
  | handoff         | End-of-session: comprehensive save + summary for next agent                      |
  | status          | Quick view of current state without full context load                            |

  Project Detection

  The skill would instruct me to:
  1. Check CLAUDE.md for Memory Hub Address section (we already have this for covenant)
  2. Fall back to folder name parsing if not found
  3. Prompt user to configure if neither works

  Example Flow

  Session Start:
  User: /dev-session resume

  Claude: Loading session context for covenant/portal...

  📍 Active Ticket: smart-actions-testing
  🎯 Focus: Testing email 04 with Haiku 4.5
  📝 Recent Decisions:
     - Switched to Haiku 4.5 model
     - Added code fence stripping
     - Fixed Execute Selected count
  ⏭️ Next Steps:
     - Decide on always-suggest-email-reply
     - Update CLAUDE.md

  Loading last 3 memories from smart-actions-testing...
  [memories displayed]

  Ready to continue.

  Mid-Session:
  User: /dev-session tickets

  Claude: Tickets in covenant/portal:
    → smart-actions-testing (active) - 3 memories
      triage-create-intake - 8 memories
      email-actions-system - 5 memories
      auth-flow - 5 memories
      ...

  Session End:
  User: /dev-session handoff

  Claude: Saving session state...

  Updated _session index:
  - active_ticket: smart-actions-testing
  - focus: Haiku 4.5 working, need draft_email_response decision
  - next_steps: [updated list]

  Created memory in smart-actions-testing:
  "Session 2025-12-05: Fixed code fence parsing, Execute Selected count bug..."

  Ready for next agent.

  What Memory Hub Needs

  For this to work cleanly, we need:
  1. _session as a reserved ticket_id - Or any convention like underscore prefix
  2. Single-memory update pattern - The _session ticket always has exactly 1 memory that gets updated (not appended)

  Skill Name Options

  | Name        | Notes                       |
  |-------------|-----------------------------|
  | dev-session | Clear, describes purpose    |
  | session     | Simpler, might conflict     |
  | context     | Generic, might be confusing |

  I'd go with dev-session - clear, unlikely to conflict, describes exactly what it does.