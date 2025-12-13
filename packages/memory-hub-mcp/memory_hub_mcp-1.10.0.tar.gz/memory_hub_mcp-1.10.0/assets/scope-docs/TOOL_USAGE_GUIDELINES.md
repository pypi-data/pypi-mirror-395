# Tool Usage Guidelines
**ticket_id:** tool-usage  
**app_id:** global  
**project_id:** workflow

## A. context7

Before implementing new code involving unfamiliar libraries/APIs, consider using `context7`. This tool provides both documentation and code examples for libraries, frameworks, and APIs you're not familiar with.

## B. perplexity-ask

`perplexity-ask` is a powerful problem-solving tool that can greatly increase your ability to resolve complex issues. Use this escalation strategy:

1. **After 3+ failed attempts** at a task without resolution, use `perplexity-ask`
2. **If still unable to complete** the task after using perplexity, stop and inform the User
3. **This prevents endless loops** while giving you access to broader knowledge when stuck

## C. Local Memory Hub (Primary Tool)

The **`local-memory-hub`** MCP is your primary, high-speed knowledge base. All Memory Hub interaction mechanics (context retrieval, storage workflows) are defined in your core prompt. 