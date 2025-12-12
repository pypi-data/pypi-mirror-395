"""API client for Meld backend."""

from typing import Any

import httpx

from .config import get_access_token, get_api_url


class MeldAPIClient:
    """Async client for Meld API."""

    def __init__(self):
        self.base_url = get_api_url()
        self._token = None

    @property
    def token(self) -> str | None:
        """Get the access token (cached)."""
        if self._token is None:
            self._token = get_access_token()
        return self._token

    def _headers(self) -> dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        json_data: dict | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """Make an API request."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.base_url}{path}",
                json=json_data,
                params=params,
                headers=self._headers(),
                timeout=30.0,
            )

            if response.status_code >= 400:
                return {"error": response.text, "status_code": response.status_code}

            return response.json()

    # Session endpoints

    async def hello(self) -> dict[str, Any]:
        """Call meld_hello - get user state and recommended action."""
        return await self._request("GET", "/session/hello")

    async def start_checkin(self) -> dict[str, Any]:
        """Start a check-in session."""
        return await self._request("POST", "/session/checkin/start", json_data={})

    async def checkin_respond(
        self, session_id: str, question_id: str, response: str
    ) -> dict[str, Any]:
        """Respond to a check-in question."""
        return await self._request(
            "POST",
            "/session/checkin/respond",
            json_data={
                "session_id": session_id,
                "question_id": question_id,
                "response": response,
            },
        )

    # Profile endpoints

    async def get_profile(self) -> dict[str, Any]:
        """Get user profile."""
        return await self._request("GET", "/profile")

    async def set_slot(
        self, key: str, value: str, confidence: float = 0.9
    ) -> dict[str, Any]:
        """Set a profile slot."""
        return await self._request(
            "POST",
            "/profile/slots",
            json_data={"key": key, "value": value, "confidence": confidence},
        )

    async def update_preference(self, preference: str, value: str) -> dict[str, Any]:
        """Update a profile preference."""
        return await self._request(
            "PUT",
            "/profile/preferences",
            json_data={"preference": preference, "value": value},
        )

    # Memory endpoints

    async def store_memory(
        self,
        content: str,
        kind: str = "explicit",
        title: str | None = None,
        metadata: dict | None = None,
    ) -> dict[str, Any]:
        """Store a memory."""
        return await self._request(
            "POST",
            "/memories",
            json_data={
                "content": content,
                "kind": kind,
                "title": title,
                "metadata": metadata or {},
            },
        )

    async def recall(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Recall memories using semantic search."""
        result = await self._request(
            "POST",
            "/memories/recall",
            json_data={"query": query, "limit": limit},
        )
        # API returns list, but _request wraps errors in dict
        if isinstance(result, dict) and "error" in result:
            return []
        return result if isinstance(result, list) else []

    async def check_duplicate(
        self, content: str, kind: str = "explicit"
    ) -> dict[str, Any]:
        """Check if a similar memory exists."""
        return await self._request(
            "POST",
            "/memories/check-duplicate",
            json_data={"content": content, "kind": kind},
        )

    # Project endpoints

    async def list_projects(self, status: str | None = None) -> list[dict[str, Any]]:
        """List user projects."""
        params = {"status_filter": status} if status else None
        result = await self._request("GET", "/projects", params=params)
        # API returns list, but _request wraps errors in dict
        if isinstance(result, dict) and "error" in result:
            return []
        return result if isinstance(result, list) else []

    async def create_project(
        self,
        name: str,
        description: str | None = None,
        domains: list[str] | None = None,
        goals: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new project."""
        return await self._request(
            "POST",
            "/projects",
            json_data={
                "name": name,
                "description": description,
                "domains": domains or [],
                "goals": goals or [],
            },
        )

    async def update_project(
        self, project_id: str, **updates
    ) -> dict[str, Any]:
        """Update a project."""
        return await self._request(
            "PATCH",
            f"/projects/{project_id}",
            json_data=updates,
        )

    async def add_interest(
        self,
        domain: str,
        specifics: list[str] | None = None,
        priority: str = "medium",
    ) -> dict[str, Any]:
        """Add a user interest."""
        return await self._request(
            "POST",
            "/profile/interests",
            json_data={
                "domain": domain,
                "specifics": specifics or [],
                "priority": priority,
            },
        )

    # Session history endpoints

    async def search_sessions(
        self,
        query: str,
        limit: int = 10,
        project_filter: str | None = None,
        source_filter: str = "all",
    ) -> dict[str, Any]:
        """Search session history using semantic search."""
        payload = {"query": query, "limit": limit}
        if project_filter:
            payload["project_filter"] = project_filter
        if source_filter and source_filter != "all":
            payload["source_filter"] = source_filter
        return await self._request("POST", "/sessions/search", json_data=payload)

    async def get_session_stats(self) -> dict[str, Any]:
        """Get session indexing statistics."""
        return await self._request("GET", "/sessions/stats")

