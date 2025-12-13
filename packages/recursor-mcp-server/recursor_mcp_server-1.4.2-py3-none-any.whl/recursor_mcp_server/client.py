"""
HTTP Client for Recursor MCP Server.
Full-featured client matching SDK capabilities for developers using coding assistants.
"""

import os
import aiohttp
import json
from typing import Dict, Any, List, Optional

class RecursorClient:
    def __init__(self):
        self.api_url = os.getenv("RECURSOR_API_URL", "https://recursor.dev/v1")
        self.api_key = os.getenv("RECURSOR_API_KEY")
        self.access_token = os.getenv("RECURSOR_ACCESS_TOKEN")
        self._ws_client: Optional[Any] = None
        
        if not self.api_key and not self.access_token:
            raise ValueError("Either RECURSOR_API_KEY or RECURSOR_ACCESS_TOKEN environment variable is required")
            
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.access_token:
            self.headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.api_key:
            self.headers["X-API-Key"] = self.api_key
    
    def set_access_token(self, token: str) -> None:
        """Set access token for authenticated requests"""
        self.access_token = token
        self.headers["Authorization"] = f"Bearer {token}"
        if "X-API-Key" in self.headers:
            del self.headers["X-API-Key"]
    
    def set_api_key(self, key: str) -> None:
        """Set API key for authenticated requests"""
        self.api_key = key
        self.headers["X-API-Key"] = key
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
    
    async def close(self) -> None:
        """Close client and cleanup resources"""
        if self._ws_client:
            try:
                await self.disconnect_websocket()
            except Exception:
                pass
    
    def _get_full_url(self, path: str) -> str:
        """Build full URL with proper prefix"""
        if path.startswith("/"):
            return f"{self.api_url}{path}"
        return f"{self.api_url}/{path}"
    
    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make HTTP request"""
        url = self._get_full_url(path)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.headers, **kwargs) as resp:
                if resp.status >= 400:
                    error_text = await resp.text()
                    raise Exception(f"API error {resp.status}: {error_text}")
                
                if resp.status == 204:  # No Content
                    return {}
                
                try:
                    return await resp.json()
                except:
                    return {}
    
    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("GET", path, params=params)
    
    async def _post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("POST", path, json=data)
    
    async def _put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("PUT", path, json=data)
    
    async def _patch(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return await self._request("PATCH", path, json=data)
    
    async def _delete(self, path: str) -> Any:
        return await self._request("DELETE", path)
    
    # ==================== Health & Status ====================
    
    async def check_health(self) -> bool:
        """Check if API is reachable"""
        try:
            result = await self._get("/status/health")
            return True
        except Exception:
            return False
    
    # ==================== Corrections ====================
    
    async def search_corrections(self, query: str, limit: int = 5, organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search corrections via API"""
        params = {"query": query, "limit": limit}
        if organization_id:
            params["organization_id"] = organization_id
        data = await self._get("/client/corrections/search", params)
        return data.get("corrections", []) if isinstance(data, dict) else data if isinstance(data, list) else []

    async def add_correction(
        self, 
        input_text: str, 
        output_text: str, 
        explanation: str,
        expected_output: Optional[str] = None,
        correction_type: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a correction via API"""
        payload = {
            "input_text": input_text,
            "output_text": output_text,
            "expected_output": expected_output or output_text,
            "correction_type": correction_type or "mcp_learned",
            "context": {"explanation": explanation, "source": "mcp"}
        }
        path = "/client/corrections/"
        if organization_id:
            path = f"/client/corrections/?organization_id={organization_id}"
        return await self._post(path, payload)
    
    async def list_corrections(
        self,
        page: int = 1,
        page_size: int = 50,
        include_inactive: bool = False,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """List corrections"""
        params = {"page": page, "page_size": page_size, "include_inactive": include_inactive}
        if organization_id:
            params["organization_id"] = organization_id
        return await self._get("/client/corrections/", params)
    
    async def get_correction(self, correction_id: str) -> Dict[str, Any]:
        """Get correction by ID"""
        return await self._get(f"/client/corrections/{correction_id}")
    
    async def update_correction(self, correction_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update correction"""
        return await self._put(f"/client/corrections/{correction_id}", updates)
    
    async def get_correction_stats(self) -> Dict[str, Any]:
        """Get correction statistics"""
        return await self._get("/client/corrections/stats")
    
    # ==================== Code Intelligence ====================
    
    async def detect_intent(
        self,
        user_request: str,
        current_file: Optional[str] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        similar_limit: int = 5,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Detect user intent"""
        payload = {
            "user_request": user_request[:4000],
            "current_file": current_file,
            "user_id": user_id,
            "project_id": project_id,
            "tags": tags or [],
            "similar_limit": similar_limit,
            "organization_id": organization_id
        }
        return await self._post("/client/code_intelligence/detect-intent", payload)
    
    async def get_intent_history(self, limit: int = 50, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get intent history"""
        params = {"limit": limit}
        if project_id:
            params["project_id"] = project_id
        data = await self._get("/client/code_intelligence/intent-history", params)
        return data if isinstance(data, list) else []
    
    async def correct_code(
        self,
        code: str,
        language: str,
        project_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Correct code"""
        payload = {
            "code": code,
            "language": language,
            "project_profile": project_profile or {}
        }
        return await self._post("/client/code_intelligence/correct/code", payload)
    
    async def correct_config(self, config: str, config_type: str) -> Dict[str, Any]:
        """Correct config"""
        payload = {"config": config, "config_type": config_type}
        return await self._post("/client/code_intelligence/correct/config", payload)
    
    async def correct_documentation(self, markdown: str, doc_type: str = "README") -> Dict[str, Any]:
        """Correct documentation"""
        payload = {"markdown": markdown, "doc_type": doc_type}
        return await self._post("/client/code_intelligence/correct/documentation", payload)
    
    async def get_patterns(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get patterns"""
        params = {"user_id": user_id} if user_id else None
        data = await self._get("/client/code_intelligence/patterns", params)
        return data if isinstance(data, list) else []
    
    async def get_analytics_dashboard(
        self,
        user_id: str,
        period: str = "30d",
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get analytics dashboard"""
        params = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return await self._get("/client/code_intelligence/analytics/dashboard", params)
    
    # ==================== Authentication ====================
    
    async def register(
        self,
        email: str,
        password: str,
        username: str,
        full_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register a new user"""
        payload = {
            "email": email,
            "password": password,
            "username": username,
            "full_name": full_name
        }
        return await self._post("/client/auth/register", payload)
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and get access token"""
        payload = {"email": email, "password": password}
        response = await self._post("/client/auth/login", payload)
        if "access_token" in response:
            self.access_token = response["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            if "X-API-Key" in self.headers:
                del self.headers["X-API-Key"]
        return response
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return await self._get("/client/auth/me")
    
    async def update_profile(self, full_name: Optional[str] = None, username: Optional[str] = None) -> Dict[str, Any]:
        """Update user profile"""
        payload = {}
        if full_name is not None:
            payload["full_name"] = full_name
        if username is not None:
            payload["username"] = username
        return await self._put("/client/auth/me", payload)
    
    # ==================== Projects ====================
    
    async def create_project(
        self,
        name: str,
        organization_id: str,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new project"""
        payload = {
            "name": name,
            "organization_id": organization_id,
            "description": description,
            "settings": settings or {}
        }
        return await self._post("/client/projects/", payload)
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID"""
        return await self._get(f"/client/projects/{project_id}")
    
    async def list_projects(self, organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List projects"""
        if organization_id:
            data = await self._get(f"/client/projects/org/{organization_id}")
        else:
            data = await self._get("/client/projects/")
        return data if isinstance(data, list) else []
    
    async def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update project"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if settings is not None:
            payload["settings"] = settings
        if is_active is not None:
            payload["is_active"] = is_active
        return await self._patch(f"/client/projects/{project_id}", payload)
    
    async def get_mcp_config(self, project_id: str) -> Dict[str, Any]:
        """Get MCP configuration for project"""
        return await self._get(f"/client/projects/{project_id}/mcp-config")
    
    # ==================== Organizations ====================
    
    async def create_organization(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new organization"""
        payload = {"name": name, "description": description}
        return await self._post("/client/organizations/", payload)
    
    async def list_organizations(self) -> List[Dict[str, Any]]:
        """List user's organizations"""
        data = await self._get("/client/organizations/")
        return data.get("organizations", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
    
    async def get_organization(self, org_id: str) -> Dict[str, Any]:
        """Get organization by ID"""
        return await self._get(f"/client/organizations/{org_id}")
    
    async def update_organization(self, org_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update organization"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        return await self._put(f"/client/organizations/{org_id}", payload)
    
    async def add_member_to_organization(self, org_id: str, user_id: str) -> None:
        """Add member to organization"""
        await self._post(f"/client/organizations/{org_id}/members", {"user_id": user_id})
    
    async def remove_member_from_organization(self, org_id: str, user_id: str) -> None:
        """Remove member from organization"""
        await self._delete(f"/client/organizations/{org_id}/members/{user_id}")
    
    # ==================== Billing ====================
    
    async def get_usage(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return await self._get("/client/billing/usage")
    
    async def get_usage_history(self, days: int = 30, resource_type: Optional[str] = None) -> Dict[str, Any]:
        """Get usage history"""
        params = {"days": days}
        if resource_type:
            params["resource_type"] = resource_type
        return await self._get("/client/billing/usage/history", params)
    
    async def list_billing_plans(self) -> List[Dict[str, Any]]:
        """List available billing plans"""
        data = await self._get("/client/billing/plans")
        return data.get("plans", []) if isinstance(data, dict) else []
    
    async def get_subscription(self) -> Dict[str, Any]:
        """Get current subscription"""
        return await self._get("/client/billing/subscription")
    
    # ==================== Notifications ====================
    
    async def list_notifications(self) -> List[Dict[str, Any]]:
        """List notifications"""
        data = await self._get("/client/notifications")
        return data.get("notifications", []) if isinstance(data, dict) else []
    
    async def mark_notification_as_read(self, notification_id: str) -> Dict[str, Any]:
        """Mark notification as read"""
        return await self._post(f"/client/notifications/{notification_id}/read", {})
    
    async def mark_all_notifications_as_read(self) -> None:
        """Mark all notifications as read"""
        await self._post("/client/notifications/read-all", {})
    
    async def delete_notification(self, notification_id: str) -> None:
        """Delete notification"""
        await self._delete(f"/client/notifications/{notification_id}")
    
    # ==================== Settings ====================
    
    async def get_settings(self) -> Dict[str, Any]:
        """Get user settings"""
        return await self._get("/client/settings")
    
    async def update_account(self, full_name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """Update account information"""
        payload = {}
        if full_name is not None:
            payload["full_name"] = full_name
        if email is not None:
            payload["email"] = email
        return await self._put("/client/settings/account", payload)
    
    async def update_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user preferences"""
        return await self._put("/client/settings/preferences", preferences)
    
    async def get_guidelines(self) -> Dict[str, Any]:
        """Get coding guidelines"""
        return await self._get("/client/settings/guidelines")
    
    async def change_password_via_settings(self, current_password: str, new_password: str) -> None:
        """Change password via settings"""
        await self._put("/client/settings/password", {
            "current_password": current_password,
            "new_password": new_password
        })
    
    async def delete_account(self) -> None:
        """Delete user account"""
        await self._delete("/client/settings/account")
    
    # ==================== Activity Logs ====================
    
    async def list_activity_logs(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """List activity logs"""
        params = {"page": page, "page_size": page_size}
        return await self._get("/client/activity", params)
    
    async def export_activity_logs(self) -> bytes:
        """Export activity logs as CSV"""
        url = self._get_full_url("/client/activity/export")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status >= 400:
                    raise Exception(f"API error {resp.status}: {await resp.text()}")
                return await resp.read()
    
    # ==================== Additional Corrections ====================
    
    async def get_correction(self, correction_id: str) -> Dict[str, Any]:
        """Get correction by ID"""
        return await self._get(f"/client/corrections/{correction_id}")
    
    # ==================== Additional Code Intelligence ====================
    
    async def get_time_saved(self, user_id: str, period: str = "30d", project_id: Optional[str] = None) -> Dict[str, Any]:
        """Get time saved metrics"""
        params = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return await self._get("/client/code_intelligence/analytics/time-saved", params)
    
    async def get_quality_metrics(self, user_id: str, period: str = "30d", project_id: Optional[str] = None) -> Dict[str, Any]:
        """Get quality metrics"""
        params = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return await self._get("/client/code_intelligence/analytics/quality", params)
    
    async def get_ai_agent_metrics(self, user_id: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """Get AI agent metrics"""
        params = {"user_id": user_id}
        if project_id:
            params["project_id"] = project_id
        return await self._get("/client/code_intelligence/analytics/ai-agent", params)
    
    async def apply_auto_corrections(self, user_id: str, model_name: str, corrections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply auto corrections"""
        payload = {
            "user_id": user_id,
            "model_name": model_name,
            "corrections": corrections
        }
        return await self._post("/client/code_intelligence/auto-correct", payload)
    
    async def get_trust_score(self, user_id: str, model_name: str) -> float:
        """Get trust score"""
        params = {"user_id": user_id, "model_name": model_name}
        data = await self._get("/client/code_intelligence/trust-score", params)
        try:
            return float(data.get("trust_score", 0))
        except Exception:
            return 0.0
    
    async def submit_feedback(self, prediction_id: str, accepted: bool) -> Dict[str, Any]:
        """Submit feedback"""
        payload = {"prediction_id": prediction_id, "accepted": bool(accepted)}
        return await self._post("/client/code_intelligence/feedback", payload)
    
    async def get_auto_correct_stats(self, user_id: str) -> Dict[str, Any]:
        """Get auto correction stats"""
        params = {"user_id": user_id}
        return await self._get("/client/code_intelligence/stats", params)
    
    # ==================== Additional Projects ====================
    
    async def delete_project(self, project_id: str) -> None:
        """Delete project"""
        await self._delete(f"/client/projects/{project_id}")
    
    async def regenerate_project_api_key(self, project_id: str) -> Dict[str, Any]:
        """Regenerate project API key"""
        return await self._post(f"/client/projects/{project_id}/api-key", {})
    
    async def get_mcp_stats(self, project_id: str) -> Dict[str, Any]:
        """Get MCP usage statistics for project"""
        return await self._get(f"/client/projects/{project_id}/mcp-stats")
    
    # ==================== Additional Authentication ====================
    
    async def logout(self) -> None:
        """Logout current user"""
        await self._post("/client/auth/logout", {})
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        response = await self._post("/client/auth/refresh", {"refresh_token": refresh_token})
        if "access_token" in response:
            self.access_token = response["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            if "X-API-Key" in self.headers:
                del self.headers["X-API-Key"]
        return response
    
    async def change_password(self, current_password: str, new_password: str) -> None:
        """Change user password"""
        await self._post("/client/auth/change-password", {
            "current_password": current_password,
            "new_password": new_password
        })
    
    async def generate_api_key(self) -> Dict[str, Any]:
        """Generate API key for current user"""
        return await self._post("/client/auth/api-key", {})
    
    async def revoke_api_key(self) -> None:
        """Revoke current user's API key"""
        await self._delete("/client/auth/api-key")
    
    async def get_password_requirements(self) -> Dict[str, Any]:
        """Get password requirements"""
        return await self._get("/client/auth/password-requirements")
    
    # ==================== Gateway Policies ====================
    
    async def get_llm_gateway_policy(self) -> Dict[str, Any]:
        """Get LLM gateway policy"""
        return await self._get("/recursor/llm/gateway/policy")
    
    async def get_robotics_gateway_policy(self) -> Dict[str, Any]:
        """Get robotics gateway policy"""
        return await self._get("/recursor/robotics/gateway/policy")
    
    async def robotics_gateway_observe(
        self,
        state: Dict[str, Any],
        command: Optional[Dict[str, Any]] = None,
        environment: Optional[List[Dict[str, Any]]] = None,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Robotics gateway observe"""
        payload = {
            "state": state,
            "command": command,
            "environment": environment or [],
            "user_id": user_id,
            "organization_id": organization_id
        }
        return await self._post("/recursor/robotics/gateway/observe", payload)
    
    async def get_av_gateway_policy(self) -> Dict[str, Any]:
        """Get AV gateway policy"""
        return await self._get("/recursor/av/gateway/policy")
    
    async def av_gateway_observe(
        self,
        sensors: Dict[str, Any],
        state: Dict[str, Any],
        action: Dict[str, Any],
        timestamp: int,
        vehicle_id: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """AV gateway observe"""
        payload = {
            "sensors": sensors,
            "state": state,
            "action": action,
            "timestamp": timestamp,
            "vehicle_id": vehicle_id,
            "user_id": user_id,
            "organization_id": organization_id
        }
        return await self._post("/recursor/av/gateway/observe", payload)
    
    # ==================== Additional Memory Operations ====================
    
    async def create_conversation_summary(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        summary_text: str,
        key_points: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a conversation summary"""
        payload = {
            "conversation_id": conversation_id,
            "messages": messages,
            "summary_text": summary_text,
            "key_points": key_points or [],
            "topics": topics or [],
            "metadata": metadata or {}
        }
        return await self._post("/client/memory/conversations/summaries", payload)
    
    async def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get a conversation summary by ID"""
        return await self._get(f"/client/memory/conversations/summaries/{conversation_id}")
    
    async def record_architectural_change(
        self,
        change_type: str,
        component: str,
        description: str,
        before: Optional[Dict[str, Any]] = None,
        after: Optional[Dict[str, Any]] = None,
        impact: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Record an architectural change"""
        payload = {
            "change_type": change_type,
            "component": component,
            "description": description,
            "before": before,
            "after": after,
            "impact": impact or [],
            "metadata": metadata or {}
        }
        return await self._post("/client/memory/architectural/changes", payload)
    
    async def record_pattern_usage(self, pattern_id: str, successful: bool) -> Dict[str, Any]:
        """Record pattern usage and update effectiveness"""
        payload = {
            "pattern_id": pattern_id,
            "successful": successful
        }
        return await self._post("/client/memory/rotatable/usage", payload)
    
    # ==================== Memory Operations ====================
    
    async def query_rotatable_memory(
        self,
        domain: Optional[str] = None,
        pattern_type: Optional[str] = None,
        min_effectiveness: Optional[float] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Query rotatable memory patterns"""
        payload = {
            "domain": domain,
            "pattern_type": pattern_type,
            "min_effectiveness": min_effectiveness,
            "limit": limit
        }
        return await self._post("/client/memory/rotatable/query", payload)
    
    async def get_rotatable_memory_stats(self) -> Dict[str, Any]:
        """Get rotatable memory statistics"""
        return await self._get("/client/memory/rotatable/stats")
    
    async def list_conversation_summaries(self, limit: int = 10, days: int = 7) -> Dict[str, Any]:
        """List recent conversation summaries"""
        params = {"limit": limit, "days": days}
        return await self._get("/client/memory/conversations/summaries", params)
    
    async def list_architectural_changes(
        self,
        limit: int = 20,
        days: int = 30,
        change_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """List recent architectural changes"""
        params = {"limit": limit, "days": days}
        if change_type:
            params["change_type"] = change_type
        return await self._get("/client/memory/architectural/changes", params)
    
    # ==================== Gateway ====================
    
    async def gateway_chat(
        self,
        messages: List[Dict[str, str]],
        provider: str = "openai",
        model: Optional[str] = None,
        call_provider: bool = False,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """LLM gateway chat"""
        payload = {
            "provider": provider,
            "model": model,
            "messages": messages,
            "call_provider": call_provider,
            "user_id": user_id,
            "organization_id": organization_id
        }
        return await self._post("/recursor/llm/gateway/chat", payload)
    
    # ==================== WebSocket Support ====================
    
    def create_websocket(self):
        """Create WebSocket connection for real-time updates"""
        if not self.access_token:
            raise ValueError(
                "Access token required for WebSocket connection. Use login() first or set_access_token()"
            )
        
        try:
            from websockets.client import connect as ws_connect
        except ImportError:
            raise ImportError("websockets package is required. Install with: pip install websockets")
        
        # Convert http/https to ws/wss
        ws_url = self.api_url.replace("http://", "ws://").replace("https://", "wss://")
        ws_url = f"{ws_url}/client/ws?token={self.access_token}"
        
        return ws_url  # Return URL for connection
    
    async def connect_websocket(self):
        """Connect WebSocket and return client (stores internally)"""
        if not self.access_token:
            raise ValueError("Access token required for WebSocket connection. Use login() first or set_access_token()")
        
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets package is required. Install with: pip install websockets")
        
        ws_url = self.create_websocket()
        self._ws_client = await websockets.connect(ws_url)
        return self._ws_client
    
    async def disconnect_websocket(self) -> None:
        """Disconnect WebSocket if connected"""
        if self._ws_client:
            try:
                await self._ws_client.close()
            except Exception:
                pass
            self._ws_client = None
