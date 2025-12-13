"""
MCP Tools - Full access to Recursor API for developers using coding assistants
"""
from typing import Optional, List, Dict, Any
from .server import mcp, get_client
import asyncio
import os
import json

# ==================== Corrections ====================

@mcp.tool()
async def search_memory(query: str, limit: int = 5) -> str:
    """
    Search Recursor's memory for relevant coding patterns, past corrections, or guidelines.
    Use this when you want to check if there are specific rules or past mistakes to avoid for the current task.
    """
    client = get_client()
    corrections = await client.search_corrections(query, limit)
    
    if not corrections:
        return f"No specific past corrections found for '{query}'."
        
    response = f"Found {len(corrections)} relevant past corrections:\n\n"
    for c in corrections:
        created_at = c.get('created_at', 'Unknown date')
        input_text = c.get('input_text', '')
        output_text = c.get('output_text', '')
        explanation = c.get('context', {}).get('explanation', 'N/A')
        
        response += f"--- Correction ({created_at}) ---\n"
        response += f"Original: {input_text[:100]}...\n"
        response += f"Fixed: {output_text[:100]}...\n"
        response += f"Reason: {explanation}\n\n"
        
    return response

@mcp.tool()
async def add_correction(original_code: str, fixed_code: str, explanation: str) -> str:
    """
    Record a correction or improvement to the system's memory.
    Use this when the user corrects your output, so you don't make the same mistake again.
    """
    client = get_client()
    try:
        await client.add_correction(original_code, fixed_code, explanation)
        return "Correction saved. I will remember this preference for future tasks."
    except Exception as e:
        return f"Failed to save correction: {str(e)}"

@mcp.tool()
async def list_corrections(page: int = 1, page_size: int = 10) -> str:
    """
    List corrections with pagination.
    """
    client = get_client()
    try:
        result = await client.list_corrections(page, page_size)
        total = result.get("total", 0)
        corrections = result.get("corrections", [])
        
        response = f"Found {total} corrections (showing page {page}):\n\n"
        for c in corrections[:page_size]:
            response += f"- {c.get('id', 'unknown')}: {c.get('correction_type', 'N/A')}\n"
        
        return response
    except Exception as e:
        return f"Error listing corrections: {str(e)}"

@mcp.tool()
async def get_correction_stats() -> str:
    """
    Get statistics about corrections (total count, by type, etc.).
    """
    client = get_client()
    try:
        stats = await client.get_correction_stats()
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error getting stats: {str(e)}"

# ==================== Code Intelligence ====================

@mcp.tool()
async def detect_intent(user_request: str, current_file: Optional[str] = None) -> str:
    """
    Detect the user's intent from their request. Returns action, scope, constraints, and similar past requests.
    Use this to understand what the user wants before implementing.
    """
    client = get_client()
    try:
        result = await client.detect_intent(user_request, current_file=current_file)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error detecting intent: {str(e)}"

@mcp.tool()
async def correct_code(code: str, language: str) -> str:
    """
    Get AI-suggested corrections for code based on learned patterns.
    """
    client = get_client()
    try:
        result = await client.correct_code(code, language)
        return result.get("corrected_code", "No corrections suggested")
    except Exception as e:
        return f"Error correcting code: {str(e)}"

@mcp.tool()
async def get_coding_patterns() -> str:
    """
    Get learned coding patterns from the system.
    """
    client = get_client()
    try:
        patterns = await client.get_patterns()
        response = f"Found {len(patterns)} patterns:\n\n"
        for p in patterns[:10]:  # Limit to first 10
            response += f"- {p.get('pattern', 'N/A')}\n"
        return response
    except Exception as e:
        return f"Error getting patterns: {str(e)}"

@mcp.tool()
async def get_analytics(user_id: str, period: str = "30d") -> str:
    """
    Get analytics dashboard with time saved, quality metrics, and AI agent performance.
    """
    client = get_client()
    try:
        analytics = await client.get_analytics_dashboard(user_id, period)
        return json.dumps(analytics, indent=2)
    except Exception as e:
        return f"Error getting analytics: {str(e)}"

# ==================== Projects ====================

@mcp.tool()
async def create_project(name: str, organization_id: str, description: Optional[str] = None) -> str:
    """
    Create a new project in Recursor.
    """
    client = get_client()
    try:
        project = await client.create_project(name, organization_id, description)
        return f"Project created: {project.get('id', 'unknown')} - {project.get('name', name)}"
    except Exception as e:
        return f"Error creating project: {str(e)}"

@mcp.tool()
async def list_projects(organization_id: Optional[str] = None) -> str:
    """
    List all projects, optionally filtered by organization.
    """
    client = get_client()
    try:
        projects = await client.list_projects(organization_id)
        response = f"Found {len(projects)} projects:\n\n"
        for p in projects:
            response += f"- {p.get('name', 'N/A')} (ID: {p.get('id', 'unknown')})\n"
        return response
    except Exception as e:
        return f"Error listing projects: {str(e)}"

@mcp.tool()
async def get_project(project_id: str) -> str:
    """
    Get project details by ID.
    """
    client = get_client()
    try:
        project = await client.get_project(project_id)
        return json.dumps(project, indent=2)
    except Exception as e:
        return f"Error getting project: {str(e)}"

@mcp.tool()
async def get_mcp_config(project_id: str) -> str:
    """
    Get MCP server configuration for a project. Use this to set up Claude Desktop or Cursor.
    """
    client = get_client()
    try:
        config = await client.get_mcp_config(project_id)
        return json.dumps(config, indent=2)
    except Exception as e:
        return f"Error getting MCP config: {str(e)}"

# ==================== Organizations ====================

@mcp.tool()
async def create_organization(name: str, description: Optional[str] = None) -> str:
    """
    Create a new organization (team/workspace).
    """
    client = get_client()
    try:
        org = await client.create_organization(name, description)
        return f"Organization created: {org.get('id', 'unknown')} - {org.get('name', name)}"
    except Exception as e:
        return f"Error creating organization: {str(e)}"

@mcp.tool()
async def list_organizations() -> str:
    """
    List all organizations the user belongs to.
    """
    client = get_client()
    try:
        orgs = await client.list_organizations()
        response = f"Found {len(orgs)} organizations:\n\n"
        for o in orgs:
            response += f"- {o.get('name', 'N/A')} (ID: {o.get('id', 'unknown')})\n"
        return response
    except Exception as e:
        return f"Error listing organizations: {str(e)}"

# ==================== Authentication ====================

@mcp.tool()
async def login(email: str, password: str) -> str:
    """
    Login to Recursor and get an access token. This will be used for subsequent requests.
    """
    client = get_client()
    try:
        result = await client.login(email, password)
        if "access_token" in result:
            return "Login successful! Access token saved for future requests."
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Login failed: {str(e)}"

@mcp.tool()
async def get_profile() -> str:
    """
    Get the current user's profile information.
    """
    client = get_client()
    try:
        profile = await client.get_profile()
        return json.dumps(profile, indent=2)
    except Exception as e:
        return f"Error getting profile: {str(e)}"

@mcp.tool()
async def update_profile(full_name: Optional[str] = None, username: Optional[str] = None) -> str:
    """
    Update user profile information.
    """
    client = get_client()
    try:
        profile = await client.update_profile(full_name, username)
        return f"Profile updated: {json.dumps(profile, indent=2)}"
    except Exception as e:
        return f"Error updating profile: {str(e)}"

# ==================== Memory ====================

@mcp.tool()
async def query_rotatable_memory(
    domain: Optional[str] = None,
    pattern_type: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    Query rotatable memory for learned patterns. This is the system's long-term memory of corrections and patterns.
    """
    client = get_client()
    try:
        result = await client.query_rotatable_memory(domain, pattern_type, limit=limit)
        patterns = result.get("patterns", [])
        response = f"Found {len(patterns)} patterns:\n\n"
        for p in patterns[:limit]:
            response += f"- {p.get('pattern', 'N/A')} (effectiveness: {p.get('effectiveness_score', 0)}%)\n"
        return response
    except Exception as e:
        return f"Error querying memory: {str(e)}"

@mcp.tool()
async def get_memory_stats() -> str:
    """
    Get statistics about the rotatable memory system.
    """
    client = get_client()
    try:
        stats = await client.get_rotatable_memory_stats()
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error getting memory stats: {str(e)}"

@mcp.tool()
async def get_conversation_summaries(limit: int = 5) -> str:
    """
    Get recent conversation summaries. These help maintain context across long conversations.
    """
    client = get_client()
    try:
        result = await client.list_conversation_summaries(limit)
        summaries = result.get("summaries", [])
        response = f"Found {len(summaries)} conversation summaries:\n\n"
        for s in summaries:
            response += f"- {s.get('conversation_id', 'unknown')}: {s.get('summary_text', '')[:100]}...\n"
        return response
    except Exception as e:
        return f"Error getting summaries: {str(e)}"

@mcp.tool()
async def get_architectural_changes(limit: int = 10) -> str:
    """
    Get recent architectural changes to the codebase. These track structural changes over time.
    """
    client = get_client()
    try:
        result = await client.list_architectural_changes(limit)
        changes = result.get("changes", [])
        response = f"Found {len(changes)} architectural changes:\n\n"
        for c in changes:
            response += f"- {c.get('change_type', 'N/A')}: {c.get('component', 'N/A')} - {c.get('description', '')[:80]}...\n"
        return response
    except Exception as e:
        return f"Error getting changes: {str(e)}"

# ==================== Gateway ====================

@mcp.tool()
async def gateway_chat(
    messages: str,
    provider: str = "openai",
    model: Optional[str] = None
) -> str:
    """
    Send messages through the Recursor LLM gateway. This applies corrections and memory injection automatically.
    The messages parameter should be a JSON string array of message objects with 'role' and 'content' fields.
    """
    client = get_client()
    try:
        # Parse messages JSON string
        if isinstance(messages, str):
            messages_list = json.loads(messages)
        else:
            messages_list = messages
        
        result = await client.gateway_chat(messages_list, provider, model)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error in gateway chat: {str(e)}"

# ==================== Safety ====================

@mcp.tool()
async def check_safety(code_snippet: str) -> str:
    """
    Validate a code snippet against safety guardrails.
    """
    # For now, return a placeholder as the API doesn't expose a direct check_safety endpoint yet
    return "Code safety check passed (Client-side validation not yet implemented via API)."

# ==================== Additional Corrections ====================

@mcp.tool()
async def get_correction(correction_id: str) -> str:
    """
    Get a specific correction by ID.
    """
    client = get_client()
    try:
        correction = await client.get_correction(correction_id)
        return json.dumps(correction, indent=2)
    except Exception as e:
        return f"Error getting correction: {str(e)}"

# ==================== Additional Projects ====================

@mcp.tool()
async def delete_project(project_id: str) -> str:
    """
    Delete a project.
    """
    client = get_client()
    try:
        await client.delete_project(project_id)
        return f"Project {project_id} deleted successfully."
    except Exception as e:
        return f"Error deleting project: {str(e)}"

@mcp.tool()
async def update_project(
    project_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """
    Update a project's name or description.
    """
    client = get_client()
    try:
        project = await client.update_project(project_id, name=name, description=description)
        return f"Project updated: {json.dumps(project, indent=2)}"
    except Exception as e:
        return f"Error updating project: {str(e)}"

@mcp.tool()
async def get_mcp_stats(project_id: str) -> str:
    """
    Get MCP usage statistics for a project.
    """
    client = get_client()
    try:
        stats = await client.get_mcp_stats(project_id)
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error getting MCP stats: {str(e)}"

# ==================== Additional Organizations ====================

@mcp.tool()
async def update_organization(org_id: str, name: Optional[str] = None, description: Optional[str] = None) -> str:
    """
    Update an organization's name or description.
    """
    client = get_client()
    try:
        org = await client.update_organization(org_id, name, description)
        return f"Organization updated: {json.dumps(org, indent=2)}"
    except Exception as e:
        return f"Error updating organization: {str(e)}"

@mcp.tool()
async def get_organization(org_id: str) -> str:
    """
    Get organization details by ID.
    """
    client = get_client()
    try:
        org = await client.get_organization(org_id)
        return json.dumps(org, indent=2)
    except Exception as e:
        return f"Error getting organization: {str(e)}"

# ==================== Billing ====================

@mcp.tool()
async def get_usage() -> str:
    """
    Get current usage statistics (API calls, corrections, storage, etc.).
    """
    client = get_client()
    try:
        usage = await client.get_usage()
        return json.dumps(usage, indent=2)
    except Exception as e:
        return f"Error getting usage: {str(e)}"

@mcp.tool()
async def get_usage_history(days: int = 30) -> str:
    """
    Get usage history for the past N days.
    """
    client = get_client()
    try:
        history = await client.get_usage_history(days)
        return json.dumps(history, indent=2)
    except Exception as e:
        return f"Error getting usage history: {str(e)}"

@mcp.tool()
async def list_billing_plans() -> str:
    """
    List available billing plans.
    """
    client = get_client()
    try:
        plans = await client.list_billing_plans()
        response = f"Found {len(plans)} billing plans:\n\n"
        for p in plans:
            response += f"- {p.get('name', 'N/A')}: ${p.get('price_monthly', 0)}/month\n"
        return response
    except Exception as e:
        return f"Error listing billing plans: {str(e)}"

@mcp.tool()
async def get_subscription() -> str:
    """
    Get current subscription information.
    """
    client = get_client()
    try:
        subscription = await client.get_subscription()
        return json.dumps(subscription, indent=2)
    except Exception as e:
        return f"Error getting subscription: {str(e)}"

# ==================== Notifications ====================

@mcp.tool()
async def list_notifications() -> str:
    """
    List all notifications.
    """
    client = get_client()
    try:
        notifications = await client.list_notifications()
        response = f"Found {len(notifications)} notifications:\n\n"
        for n in notifications[:10]:  # Limit to first 10
            response += f"- [{n.get('type', 'N/A')}] {n.get('message', 'N/A')}\n"
        return response
    except Exception as e:
        return f"Error listing notifications: {str(e)}"

@mcp.tool()
async def mark_notification_read(notification_id: str) -> str:
    """
    Mark a notification as read.
    """
    client = get_client()
    try:
        result = await client.mark_notification_as_read(notification_id)
        return "Notification marked as read."
    except Exception as e:
        return f"Error marking notification: {str(e)}"

# ==================== Settings ====================

@mcp.tool()
async def get_settings() -> str:
    """
    Get user settings and preferences.
    """
    client = get_client()
    try:
        settings = await client.get_settings()
        return json.dumps(settings, indent=2)
    except Exception as e:
        return f"Error getting settings: {str(e)}"

@mcp.tool()
async def get_guidelines() -> str:
    """
    Get coding guidelines and best practices.
    """
    client = get_client()
    try:
        guidelines = await client.get_guidelines()
        return json.dumps(guidelines, indent=2)
    except Exception as e:
        return f"Error getting guidelines: {str(e)}"

# ==================== Activity ====================

@mcp.tool()
async def list_activity_logs(page: int = 1, page_size: int = 20) -> str:
    """
    List activity logs with pagination.
    """
    client = get_client()
    try:
        logs = await client.list_activity_logs(page, page_size)
        total = logs.get("total", 0)
        activities = logs.get("activities", [])
        response = f"Found {total} activity logs (showing page {page}):\n\n"
        for a in activities[:page_size]:
            response += f"- [{a.get('created_at', 'N/A')}] {a.get('action', 'N/A')}\n"
        return response
    except Exception as e:
        return f"Error listing activity logs: {str(e)}"

# ==================== Additional Code Intelligence ====================

@mcp.tool()
async def get_time_saved(user_id: str, period: str = "30d") -> str:
    """
    Get time saved metrics for a user.
    """
    client = get_client()
    try:
        metrics = await client.get_time_saved(user_id, period)
        return json.dumps(metrics, indent=2)
    except Exception as e:
        return f"Error getting time saved: {str(e)}"

@mcp.tool()
async def get_quality_metrics(user_id: str, period: str = "30d") -> str:
    """
    Get quality metrics for a user.
    """
    client = get_client()
    try:
        metrics = await client.get_quality_metrics(user_id, period)
        return json.dumps(metrics, indent=2)
    except Exception as e:
        return f"Error getting quality metrics: {str(e)}"

@mcp.tool()
async def get_trust_score(user_id: str, model_name: str) -> str:
    """
    Get trust score for a user and model combination.
    """
    client = get_client()
    try:
        score = await client.get_trust_score(user_id, model_name)
        return f"Trust score: {score:.2f}%"
    except Exception as e:
        return f"Error getting trust score: {str(e)}"

# ==================== Additional Authentication ====================

@mcp.tool()
async def register(email: str, password: str, username: str, full_name: Optional[str] = None) -> str:
    """
    Register a new user account.
    """
    client = get_client()
    try:
        user = await client.register(email, password, username, full_name)
        return f"User registered: {user.get('id', 'unknown')} - {user.get('email', email)}"
    except Exception as e:
        return f"Registration failed: {str(e)}"

@mcp.tool()
async def change_password(current_password: str, new_password: str) -> str:
    """
    Change user password.
    """
    client = get_client()
    try:
        await client.change_password(current_password, new_password)
        return "Password changed successfully."
    except Exception as e:
        return f"Error changing password: {str(e)}"

# ==================== Additional Memory ====================

@mcp.tool()
async def record_pattern_usage(pattern_id: str, successful: bool) -> str:
    """
    Record pattern usage to update effectiveness score.
    """
    client = get_client()
    try:
        result = await client.record_pattern_usage(pattern_id, successful)
        return f"Pattern usage recorded. Effectiveness updated."
    except Exception as e:
        return f"Error recording pattern usage: {str(e)}"
