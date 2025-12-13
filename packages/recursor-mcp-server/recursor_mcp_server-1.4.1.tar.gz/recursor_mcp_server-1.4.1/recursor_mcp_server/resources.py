from .server import mcp, get_client

@mcp.resource("recursor://recent_activity")
async def get_recent_activity() -> str:
    """
    Get a log of the most recent corrections and learnings.
    """
    client = get_client()
    # We can reuse search with empty query or add a list endpoint to client
    # For now, let's use search with a wildcard if supported, or just list
    # The client doesn't have a list method yet, let's add it or use search
    corrections = await client.search_corrections("", limit=10)
    
    if not corrections:
        return "No recent activity recorded."
        
    activity_log = "\n".join([f"- [{c.get('created_at')}] {c.get('correction_type')}: {c.get('context', {}).get('explanation', 'No details')}" for c in corrections])
    return f"Recent Recursor Activity:\n{activity_log}"

@mcp.resource("recursor://system_prompt")
async def get_optimized_system_prompt() -> str:
    """
    Get the current optimized system prompt based on accumulated learnings.
    """
    # For now, return a static prompt as the API doesn't expose system prompt yet
    return (
        "You are an AI assistant enhanced by Recursor. "
        "You have access to a database of past corrections and coding patterns. "
        "Always check 'search_memory' before writing code for complex tasks. "
        "Prioritize functional safety and clean architecture."
    )

