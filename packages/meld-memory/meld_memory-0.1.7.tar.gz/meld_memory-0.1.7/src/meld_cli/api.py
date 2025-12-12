"""API client for Meld backend."""

import httpx

from .config import get_access_token, get_api_url


class MeldAPIError(Exception):
    """API error with status code and message."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class MeldAPI:
    """Client for Meld API."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = base_url or get_api_url()
        self.token = token or get_access_token()

    def _headers(self) -> dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_user_info(self) -> dict:
        """Get current user info (verifies token is valid)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/auth/me",
                headers=self._headers(),
            )

            if response.status_code != 200:
                return {"error": response.text, "status_code": response.status_code}

            return response.json()

    async def exchange_token(self) -> dict:
        """Exchange short-lived Clerk token for long-lived Meld token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/auth/token/exchange",
                headers=self._headers(),
            )

            if response.status_code != 200:
                return {"error": response.text, "status_code": response.status_code}

            return response.json()

    async def get_user_state(self) -> dict:
        """Get current user state (meld_hello equivalent)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/session/hello",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def get_profile(self) -> dict:
        """Get user profile."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/profile",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def health_check(self) -> dict:
        """Check API health."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            return response.json()

    async def reset_user(self) -> dict:
        """Reset all user data (for testing)."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/profile/reset",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def ingest_sessions(self, chunks: list[dict]) -> dict:
        """Ingest session chunks to cloud storage."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/sessions/ingest",
                headers=self._headers(),
                json={"chunks": chunks},
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def search_sessions(
        self, query: str, limit: int = 10, project_filter: str | None = None
    ) -> dict:
        """Search session history."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"query": query, "limit": limit}
            if project_filter:
                payload["project_filter"] = project_filter

            response = await client.post(
                f"{self.base_url}/sessions/search",
                headers=self._headers(),
                json=payload,
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def get_session_stats(self) -> dict:
        """Get session indexing statistics."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/sessions/stats",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def list_projects(self, status_filter: str | None = None) -> list[dict]:
        """List user projects."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/projects"
            if status_filter:
                url += f"?status_filter={status_filter}"
            response = await client.get(url, headers=self._headers())

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def list_memories(self, limit: int = 20) -> list[dict]:
        """List user memories."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/memories?limit={limit}",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def delete_memory(self, memory_id: int) -> dict:
        """Delete a specific memory."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/memories/{memory_id}",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def delete_project(self, project_id: str) -> dict:
        """Delete a project."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/projects/{project_id}",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

    async def delete_all_sessions(self) -> dict:
        """Delete all indexed sessions."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.delete(
                f"{self.base_url}/sessions",
                headers=self._headers(),
            )

            if response.status_code != 200:
                raise MeldAPIError(response.status_code, response.text)

            return response.json()

