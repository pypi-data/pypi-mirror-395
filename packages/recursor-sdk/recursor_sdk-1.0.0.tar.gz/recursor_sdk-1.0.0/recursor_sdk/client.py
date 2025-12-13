import os
from typing import Any, Dict, List, Optional

import httpx


class RecursorSDK:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        timeout: float = 10.0,
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = (base_url or os.getenv("RECURSOR_API_URL") or "http://localhost:8000/api/v1").rstrip("/")
        self.api_key = api_key or os.getenv("RECURSOR_API_KEY")
        self.access_token = access_token or os.getenv("RECURSOR_ACCESS_TOKEN")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        self._headers = headers

        self._client = httpx.Client(timeout=self.timeout, verify=self.verify_ssl)
        self._ws_client: Optional[Any] = None

    def set_access_token(self, token: str) -> None:
        """Set access token for authenticated requests"""
        self.access_token = token
        self._headers["Authorization"] = f"Bearer {token}"
        if "X-API-Key" in self._headers:
            del self._headers["X-API-Key"]

    def set_api_key(self, key: str) -> None:
        """Set API key for authenticated requests"""
        self.api_key = key
        self._headers["X-API-Key"] = key
        if "Authorization" in self._headers:
            del self._headers["Authorization"]

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = self._client.get(self._url(path), headers=self._headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = self._client.post(self._url(path), headers=self._headers, json=data)
        resp.raise_for_status()
        if resp.status_code == 204:  # No Content
            return {}
        return resp.json()

    def _put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = self._client.put(self._url(path), headers=self._headers, json=data)
        resp.raise_for_status()
        if resp.status_code == 204:
            return {}
        return resp.json()

    def _patch(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = self._client.patch(self._url(path), headers=self._headers, json=data)
        resp.raise_for_status()
        if resp.status_code == 204:
            return {}
        return resp.json()

    def _delete(self, path: str) -> Dict[str, Any]:
        resp = self._client.delete(self._url(path), headers=self._headers)
        resp.raise_for_status()
        if resp.status_code == 204:
            return {}
        return resp.json()

    def check_health(self) -> bool:
        try:
            # Health endpoint is at /v1/status/health, not /api/v1/status/health
            health_url = self.base_url.replace("/api/v1", "") + "/v1/status/health"
            resp = self._client.get(health_url)
            return resp.status_code == 200
        except Exception:
            return False

    def detect_intent(
        self,
        user_request: str,
        current_file: Optional[str] = None,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        similar_limit: Optional[int] = 5,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "user_request": (user_request or "").strip()[:4000],
            "current_file": current_file,
            "user_id": user_id,
            "project_id": project_id,
            "tags": tags or [],
            "similar_limit": similar_limit,
            "organization_id": organization_id,
        }
        return self._post("/client/code_intelligence/detect-intent", payload)

    def get_intent_history(
        self,
        limit: int = 50,
        project_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"limit": max(1, min(limit, 200))}
        if project_id:
            params["project_id"] = project_id
        data = self._get("/client/code_intelligence/intent-history", params)
        return data if isinstance(data, list) else []

    def create_correction(
        self,
        input_text: str,
        output_text: str,
        expected_output: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        correction_type: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "input_text": (input_text or "")[:4000],
            "output_text": (output_text or "")[:4000],
            "expected_output": (expected_output or output_text or "")[:4000],
            "context": context or {},
            "correction_type": correction_type,
        }
        path = "/client/corrections/"
        if organization_id:
            path = f"/client/corrections/?organization_id={organization_id}"
        return self._post(path, payload)

    def list_corrections(
        self,
        page: int = 1,
        page_size: int = 50,
        include_inactive: bool = False,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "page": max(1, page),
            "page_size": max(1, min(page_size, 100)),
            "include_inactive": bool(include_inactive),
        }
        if organization_id:
            params["organization_id"] = organization_id
        return self._get("/client/corrections/", params)

    def search_corrections(
        self,
        query: str,
        limit: int = 10,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "query": (query or "").strip()[:4000],
            "limit": max(1, min(limit, 50)),
        }
        if organization_id:
            params["organization_id"] = organization_id
        return self._get("/client/corrections/search", params)

    def close(self) -> None:
        try:
            self._client.close()
        except Exception:
            pass

    def get_analytics_dashboard(
        self,
        user_id: str,
        period: str = "30d",
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return self._get("/client/code_intelligence/analytics/dashboard", params)

    def get_time_saved(
        self,
        user_id: str,
        period: str = "30d",
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return self._get("/client/code_intelligence/analytics/time-saved", params)

    def get_quality_metrics(
        self,
        user_id: str,
        period: str = "30d",
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"user_id": user_id, "period": period}
        if project_id:
            params["project_id"] = project_id
        return self._get("/client/code_intelligence/analytics/quality", params)

    def get_ai_agent_metrics(
        self,
        user_id: str,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"user_id": user_id}
        if project_id:
            params["project_id"] = project_id
        return self._get("/client/code_intelligence/analytics/ai-agent", params)

    def correct_code(
        self,
        code: str,
        language: str,
        project_profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "code": code,
            "language": language,
            "project_profile": project_profile or {},
        }
        return self._post("/client/code_intelligence/correct/code", payload)

    def correct_config(self, config: str, config_type: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"config": config, "config_type": config_type}
        return self._post("/client/code_intelligence/correct/config", payload)

    def correct_documentation(self, markdown: str, doc_type: str = "README") -> Dict[str, Any]:
        payload: Dict[str, Any] = {"markdown": markdown, "doc_type": doc_type}
        return self._post("/client/code_intelligence/correct/documentation", payload)

    def apply_auto_corrections(
        self,
        user_id: str,
        model_name: str,
        corrections: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "user_id": user_id,
            "model_name": model_name,
            "corrections": corrections,
        }
        return self._post("/client/code_intelligence/auto-correct", payload)

    def get_trust_score(self, user_id: str, model_name: str) -> float:
        params: Dict[str, Any] = {"user_id": user_id, "model_name": model_name}
        data = self._get("/client/code_intelligence/trust-score", params)
        try:
            return float(data.get("trust_score", 0))
        except Exception:
            return 0.0

    def submit_feedback(self, prediction_id: str, accepted: bool) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"prediction_id": prediction_id, "accepted": bool(accepted)}
        return self._post("/client/code_intelligence/feedback", payload)

    def get_auto_correct_stats(self, user_id: str) -> Dict[str, Any]:
        params: Dict[str, Any] = {"user_id": user_id}
        return self._get("/client/code_intelligence/stats", params)

    def get_patterns(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Optional[Dict[str, Any]] = {"user_id": user_id} if user_id else None
        data = self._get("/client/code_intelligence/patterns", params)
        if isinstance(data, list):
            return data
        return []

    # ==================== Authentication & User Management ====================

    def register(
        self,
        email: str,
        password: str,
        username: str,
        full_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a new user"""
        payload = {
            "email": email,
            "password": password,
            "username": username,
            "full_name": full_name,
        }
        return self._post("/client/auth/register", payload)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and get access token"""
        payload = {"email": email, "password": password}
        response = self._post("/client/auth/login", payload)
        # Automatically set access token
        if "access_token" in response:
            self.set_access_token(response["access_token"])
            # Update WebSocket token if connected
            if self._ws_client:
                self._ws_client.update_token(response["access_token"])
        return response

    def logout(self) -> None:
        """Logout current user"""
        self._post("/client/auth/logout", {})

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        response = self._post("/client/auth/refresh", {"refresh_token": refresh_token})
        if "access_token" in response:
            self.set_access_token(response["access_token"])
        return response

    def get_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        return self._get("/client/auth/me")

    def update_profile(self, full_name: Optional[str] = None, username: Optional[str] = None) -> Dict[str, Any]:
        """Update user profile"""
        payload = {}
        if full_name is not None:
            payload["full_name"] = full_name
        if username is not None:
            payload["username"] = username
        return self._put("/client/auth/me", payload)

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change user password"""
        self._post("/client/auth/change-password", {
            "current_password": current_password,
            "new_password": new_password,
        })

    def generate_api_key(self) -> Dict[str, Any]:
        """Generate API key for current user"""
        return self._post("/client/auth/api-key", {})

    def revoke_api_key(self) -> None:
        """Revoke current user's API key"""
        self._delete("/client/auth/api-key")

    def get_password_requirements(self) -> Dict[str, Any]:
        """Get password requirements"""
        return self._get("/client/auth/password-requirements")

    # ==================== Project Management ====================

    def create_project(
        self,
        name: str,
        organization_id: str,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new project"""
        payload = {
            "name": name,
            "organization_id": organization_id,
            "description": description,
            "settings": settings or {},
        }
        return self._post("/client/projects/", payload)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID"""
        return self._get(f"/client/projects/{project_id}")

    def list_projects(self, organization_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List projects, optionally filtered by organization"""
        if organization_id:
            data = self._get(f"/client/projects/org/{organization_id}")
        else:
            data = self._get("/client/projects/")
        return data if isinstance(data, list) else []

    def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
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
        return self._patch(f"/client/projects/{project_id}", payload)

    def delete_project(self, project_id: str) -> None:
        """Delete project"""
        self._delete(f"/client/projects/{project_id}")

    def regenerate_project_api_key(self, project_id: str) -> Dict[str, Any]:
        """Regenerate project API key"""
        return self._post(f"/client/projects/{project_id}/api-key", {})

    def get_mcp_config(self, project_id: str) -> Dict[str, Any]:
        """Get MCP configuration for project"""
        return self._get(f"/client/projects/{project_id}/mcp-config")

    def get_mcp_stats(self, project_id: str) -> Dict[str, Any]:
        """Get MCP usage statistics for project"""
        return self._get(f"/client/projects/{project_id}/mcp-stats")

    # ==================== Organizations & Teams ====================

    def create_organization(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new organization"""
        payload = {"name": name, "description": description}
        return self._post("/client/organizations/", payload)

    def list_organizations(self) -> List[Dict[str, Any]]:
        """List user's organizations"""
        data = self._get("/client/organizations/")
        return data if isinstance(data, list) else []

    def get_organization(self, org_id: str) -> Dict[str, Any]:
        """Get organization by ID"""
        return self._get(f"/client/organizations/{org_id}")

    def update_organization(self, org_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update organization"""
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        return self._put(f"/client/organizations/{org_id}", payload)

    def add_member_to_organization(self, org_id: str, user_id: str) -> None:
        """Add member to organization"""
        self._post(f"/client/organizations/{org_id}/members", {"user_id": user_id})

    def remove_member_from_organization(self, org_id: str, user_id: str) -> None:
        """Remove member from organization"""
        self._delete(f"/client/organizations/{org_id}/members/{user_id}")

    # ==================== Billing & Usage ====================

    def get_usage(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self._get("/client/billing/usage")

    def get_usage_history(self, days: int = 30, resource_type: Optional[str] = None) -> Dict[str, Any]:
        """Get usage history"""
        params = {"days": days}
        if resource_type:
            params["resource_type"] = resource_type
        return self._get("/client/billing/usage/history", params)

    def list_billing_plans(self) -> List[Dict[str, Any]]:
        """List available billing plans"""
        data = self._get("/client/billing/plans")
        return data.get("plans", []) if isinstance(data, dict) else []

    def get_subscription(self) -> Dict[str, Any]:
        """Get current subscription"""
        return self._get("/client/billing/subscription")

    # ==================== Notifications ====================

    def list_notifications(self) -> List[Dict[str, Any]]:
        """List notifications"""
        data = self._get("/client/notifications")
        return data.get("notifications", []) if isinstance(data, dict) else []

    def mark_notification_as_read(self, notification_id: str) -> Dict[str, Any]:
        """Mark notification as read"""
        return self._post(f"/client/notifications/{notification_id}/read", {})

    def mark_all_notifications_as_read(self) -> None:
        """Mark all notifications as read"""
        self._post("/client/notifications/read-all", {})

    def delete_notification(self, notification_id: str) -> None:
        """Delete notification"""
        self._delete(f"/client/notifications/{notification_id}")

    # ==================== Settings ====================

    def get_settings(self) -> Dict[str, Any]:
        """Get user settings"""
        return self._get("/client/settings")

    def update_account(self, full_name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """Update account information"""
        payload = {}
        if full_name is not None:
            payload["full_name"] = full_name
        if email is not None:
            payload["email"] = email
        return self._put("/client/settings/account", payload)

    def update_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user preferences"""
        return self._put("/client/settings/preferences", preferences)

    def get_guidelines(self) -> Dict[str, Any]:
        """Get coding guidelines"""
        return self._get("/client/settings/guidelines")

    def change_password_via_settings(self, current_password: str, new_password: str) -> None:
        """Change password via settings"""
        self._put("/client/settings/password", {
            "current_password": current_password,
            "new_password": new_password,
        })

    def delete_account(self) -> None:
        """Delete user account"""
        self._delete("/client/settings/account")

    # ==================== Activity Logs ====================

    def list_activity_logs(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """List activity logs"""
        return self._get("/client/activity", {"page": page, "page_size": page_size})

    def export_activity_logs(self) -> bytes:
        """Export activity logs as CSV"""
        resp = self._client.get(self._url("/client/activity/export"), headers=self._headers)
        resp.raise_for_status()
        return resp.content

    # ==================== Corrections (Additional Methods) ====================

    def get_correction(self, correction_id: str) -> Dict[str, Any]:
        """Get correction by ID"""
        return self._get(f"/client/corrections/{correction_id}")

    def update_correction(self, correction_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update correction"""
        return self._put(f"/client/corrections/{correction_id}", updates)

    def get_correction_stats(self) -> Dict[str, Any]:
        """Get correction statistics"""
        return self._get("/client/corrections/stats")

    # ==================== Gateway Endpoints ====================

    def get_llm_gateway_policy(self) -> Dict[str, Any]:
        """Get LLM gateway policy"""
        return self._get("/recursor/llm/gateway/policy")

    def gateway_chat(
        self,
        messages: List[Dict[str, str]],
        provider: str = "openai",
        model: Optional[str] = None,
        call_provider: bool = False,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """LLM gateway chat"""
        payload = {
            "provider": provider,
            "model": model,
            "messages": messages,
            "call_provider": call_provider,
            "user_id": user_id,
            "organization_id": organization_id,
        }
        return self._post("/recursor/llm/gateway/chat", payload)

    def get_robotics_gateway_policy(self) -> Dict[str, Any]:
        """Get robotics gateway policy"""
        return self._get("/recursor/robotics/gateway/policy")

    def robotics_gateway_observe(
        self,
        state: Dict[str, Any],
        command: Optional[Dict[str, Any]] = None,
        environment: Optional[List[Dict[str, Any]]] = None,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Robotics gateway observe"""
        payload = {
            "state": state,
            "command": command,
            "environment": environment or [],
            "user_id": user_id,
            "organization_id": organization_id,
        }
        return self._post("/recursor/robotics/gateway/observe", payload)

    def get_av_gateway_policy(self) -> Dict[str, Any]:
        """Get AV gateway policy"""
        return self._get("/recursor/av/gateway/policy")

    def av_gateway_observe(
        self,
        sensors: Dict[str, Any],
        state: Dict[str, Any],
        action: Dict[str, Any],
        timestamp: int,
        vehicle_id: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """AV gateway observe"""
        payload = {
            "sensors": sensors,
            "state": state,
            "action": action,
            "timestamp": timestamp,
            "vehicle_id": vehicle_id,
            "user_id": user_id,
            "organization_id": organization_id,
        }
        return self._post("/recursor/av/gateway/observe", payload)

    # ==================== WebSocket Support ====================

    def create_websocket(self):
        """Create WebSocket connection for real-time updates"""
        if not self.access_token:
            raise ValueError(
                "Access token required for WebSocket connection. Use login() first or set_access_token()"
            )

        from .websocket import RecursorWebSocket
        return RecursorWebSocket(self.base_url, self.access_token)

    async def connect_websocket(self):
        """Connect WebSocket and return client (stores internally)"""
        if not self._ws_client:
            self._ws_client = self.create_websocket()
        await self._ws_client.connect()
        return self._ws_client

    async def disconnect_websocket(self) -> None:
        """Disconnect WebSocket if connected"""
        if self._ws_client:
            await self._ws_client.disconnect()
            self._ws_client = None

    # ==================== Memory Operations ====================

    def create_conversation_summary(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        summary_text: str,
        key_points: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a conversation summary"""
        payload = {
            "conversation_id": conversation_id,
            "messages": messages,
            "summary_text": summary_text,
            "key_points": key_points or [],
            "topics": topics or [],
            "metadata": metadata or {},
        }
        return self._post("/client/memory/conversations/summaries", payload)

    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get a conversation summary by ID"""
        return self._get(f"/client/memory/conversations/summaries/{conversation_id}")

    def list_conversation_summaries(
        self,
        limit: int = 10,
        days: int = 7,
    ) -> Dict[str, Any]:
        """List recent conversation summaries"""
        params = {"limit": limit, "days": days}
        return self._get("/client/memory/conversations/summaries", params)

    def record_architectural_change(
        self,
        change_type: str,
        component: str,
        description: str,
        before: Optional[Dict[str, Any]] = None,
        after: Optional[Dict[str, Any]] = None,
        impact: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record an architectural change"""
        payload = {
            "change_type": change_type,
            "component": component,
            "description": description,
            "before": before,
            "after": after,
            "impact": impact or [],
            "metadata": metadata or {},
        }
        return self._post("/client/memory/architectural/changes", payload)

    def list_architectural_changes(
        self,
        limit: int = 20,
        days: int = 30,
        change_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List recent architectural changes"""
        params = {"limit": limit, "days": days}
        if change_type:
            params["change_type"] = change_type
        return self._get("/client/memory/architectural/changes", params)

    # ==================== Rotatable Memory Operations ====================

    def query_rotatable_memory(
        self,
        domain: Optional[str] = None,
        pattern_type: Optional[str] = None,
        min_effectiveness: Optional[float] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """Query rotatable memory patterns"""
        payload = {}
        if domain:
            payload["domain"] = domain
        if pattern_type:
            payload["pattern_type"] = pattern_type
        if min_effectiveness is not None:
            payload["min_effectiveness"] = min_effectiveness
        payload["limit"] = limit
        return self._post("/client/memory/rotatable/query", payload)

    def record_pattern_usage(self, pattern_id: str, successful: bool) -> Dict[str, Any]:
        """Record pattern usage and update effectiveness"""
        payload = {
            "pattern_id": pattern_id,
            "successful": successful,
        }
        return self._post("/client/memory/rotatable/usage", payload)

    def get_rotatable_memory_stats(self) -> Dict[str, Any]:
        """Get rotatable memory statistics"""
        return self._get("/client/memory/rotatable/stats")
