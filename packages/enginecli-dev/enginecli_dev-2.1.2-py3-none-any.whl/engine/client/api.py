"""
Engine API Client - communicates with the Engine API server.
All LLM calls go through the server, keeping prompts hidden.
"""
import httpx
from typing import Optional
from dataclasses import dataclass

from engine.client.auth import get_license_key
from engine.config import get_config


# Default API URL (can be overridden in config)
DEFAULT_API_URL = "https://api.engine.dev"


class APIError(Exception):
    """Base API error."""
    pass


class AuthenticationError(APIError):
    """Invalid or missing license key."""
    pass


class UsageLimitError(APIError):
    """Usage limit exceeded."""
    def __init__(self, message: str, limit_name: str, current: int, limit: int, upgrade_url: str):
        super().__init__(message)
        self.limit_name = limit_name
        self.current = current
        self.limit = limit
        self.upgrade_url = upgrade_url


class FeatureNotAvailableError(APIError):
    """Feature not available on current tier."""
    def __init__(self, message: str, upgrade_url: str):
        super().__init__(message)
        self.upgrade_url = upgrade_url


class ServerError(APIError):
    """Server-side error."""
    pass


@dataclass
class GenerateResponse:
    """Response from generate endpoint."""
    content: str
    input_tokens: int
    output_tokens: int
    model: str
    files_generated: list[str]


@dataclass
class PlanTask:
    """A task in a plan."""
    id: int
    title: str
    description: str
    files: list[str]
    dependencies: list[int]


@dataclass
class PlanResponse:
    """Response from plan endpoint."""
    tasks: list[PlanTask]
    input_tokens: int
    output_tokens: int


@dataclass
class ChatResponse:
    """Response from chat endpoint."""
    content: str
    input_tokens: int
    output_tokens: int


@dataclass
class UsageInfo:
    """Usage information."""
    tier: str
    daily_used: int
    daily_limit: int
    daily_remaining: int
    monthly_used: int
    monthly_limit: int
    monthly_remaining: int


@dataclass
class LicenseInfo:
    """License information."""
    license_key: str
    tier: str
    status: str
    is_active: bool
    limits: dict


class EngineAPIClient:
    """Client for Engine API server."""
    
    def __init__(self, api_url: Optional[str] = None, license_key: Optional[str] = None):
        config = get_config()
        self.api_url = api_url or config.get("api_url", DEFAULT_API_URL)
        self.license_key = license_key or get_license_key()
        self.timeout = 120.0  # 2 minutes for generation
    
    def _get_headers(self) -> dict:
        """Get headers with license key."""
        if not self.license_key:
            raise AuthenticationError("No license key found. Run 'engine license activate <key>' first.")
        return {
            "X-License-Key": self.license_key,
            "Content-Type": "application/json",
        }
    
    def _handle_error(self, response: httpx.Response):
        """Handle error responses from API."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid license key. Run 'engine license activate <key>' to fix.")
        
        if response.status_code == 403:
            try:
                data = response.json()
                if data.get("error") == "feature_not_available":
                    raise FeatureNotAvailableError(
                        data.get("message", "Feature not available"),
                        data.get("upgrade_url", "https://engine.dev/pricing"),
                    )
            except ValueError:
                pass
            raise AuthenticationError(f"Access denied: {response.text}")
        
        if response.status_code == 429:
            try:
                data = response.json()
                detail = data.get("detail", {})
                raise UsageLimitError(
                    detail.get("message", "Usage limit exceeded"),
                    detail.get("limit_name", "unknown"),
                    detail.get("current", 0),
                    detail.get("limit", 0),
                    detail.get("upgrade_url", "https://engine.dev/pricing"),
                )
            except ValueError:
                raise UsageLimitError("Usage limit exceeded", "unknown", 0, 0, "https://engine.dev/pricing")
        
        if response.status_code >= 500:
            raise ServerError(f"Server error: {response.text}")
        
        if response.status_code >= 400:
            raise APIError(f"API error ({response.status_code}): {response.text}")
    
    def generate(
        self,
        task: str,
        context: str,
        file_paths: list[str] = None,
        language: str = "python",
    ) -> GenerateResponse:
        """
        Generate code for a task.
        
        Args:
            task: What to generate
            context: Assembled context from indexer
            file_paths: Files that might be affected
            language: Primary language
        
        Returns:
            GenerateResponse with generated code
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.api_url}/v1/generate",
                headers=self._get_headers(),
                json={
                    "task": task,
                    "context": context,
                    "file_paths": file_paths or [],
                    "language": language,
                },
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return GenerateResponse(
            content=data["content"],
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
            model=data["model"],
            files_generated=data["files_generated"],
        )
    
    def generate_stream(
        self,
        task: str,
        context: str,
        file_paths: list[str] = None,
        language: str = "python",
    ):
        """
        Stream code generation.
        
        Args:
            task: What to generate
            context: Assembled context from indexer
            file_paths: Files that might be affected
            language: Primary language
        
        Yields:
            dict: Event dictionaries
            - {"type": "token", "content": "..."}
            - {"type": "done", "content": "full", "input_tokens": N, "output_tokens": M}
            - {"type": "error", "message": "..."}
        """
        import json
        
        with httpx.Client(timeout=httpx.Timeout(300.0, connect=10.0)) as client:
            with client.stream(
                "POST",
                f"{self.api_url}/v1/generate/stream",
                headers=self._get_headers(),
                json={
                    "task": task,
                    "context": context,
                    "file_paths": file_paths or [],
                    "language": language,
                },
            ) as response:
                # Check for errors first
                if response.status_code == 401:
                    raise AuthenticationError("Invalid or missing license key")
                if response.status_code == 429:
                    raise UsageLimitError("Usage limit exceeded", "unknown", 0, 0, "https://engine.dev/pricing")
                if response.status_code >= 400:
                    raise APIError(f"API error ({response.status_code})")
                
                # Parse SSE events
                buffer = ""
                for chunk in response.iter_text():
                    buffer += chunk
                    
                    # Process complete events
                    while "\n\n" in buffer:
                        event_str, buffer = buffer.split("\n\n", 1)
                        
                        # Parse data: prefix
                        for line in event_str.split("\n"):
                            if line.startswith("data: "):
                                try:
                                    event = json.loads(line[6:])
                                    yield event
                                except json.JSONDecodeError:
                                    continue
    
    def plan(
        self,
        feature: str,
        context: str,
        max_tasks: int = 20,
    ) -> PlanResponse:
        """
        Create a multi-task plan for a feature.
        
        Args:
            feature: Feature to implement
            context: Assembled context from indexer
            max_tasks: Maximum number of tasks
        
        Returns:
            PlanResponse with list of tasks
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.api_url}/v1/plan",
                headers=self._get_headers(),
                json={
                    "feature": feature,
                    "context": context,
                    "max_tasks": max_tasks,
                },
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        tasks = [
            PlanTask(
                id=t["id"],
                title=t["title"],
                description=t["description"],
                files=t["files"],
                dependencies=t["dependencies"],
            )
            for t in data["tasks"]
        ]
        
        return PlanResponse(
            tasks=tasks,
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
        )
    
    def chat(
        self,
        message: str,
        context: str,
        history: list[dict] = None,
    ) -> ChatResponse:
        """
        Chat about the codebase.
        
        Args:
            message: User message
            context: Assembled context
            history: Chat history
        
        Returns:
            ChatResponse with assistant reply
        """
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.api_url}/v1/chat",
                headers=self._get_headers(),
                json={
                    "message": message,
                    "context": context,
                    "history": history or [],
                },
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return ChatResponse(
            content=data["content"],
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
        )
    
    def get_usage(self) -> UsageInfo:
        """Get current usage statistics."""
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/usage/remaining",
                headers=self._get_headers(),
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return UsageInfo(
            tier=data["tier"],
            daily_used=data["daily"]["used"],
            daily_limit=data["daily"]["limit"],
            daily_remaining=data["daily"]["remaining"],
            monthly_used=data["monthly"]["used"],
            monthly_limit=data["monthly"]["limit"],
            monthly_remaining=data["monthly"]["remaining"],
        )
    
    def activate_license(self, license_key: str, machine_id: Optional[str] = None) -> LicenseInfo:
        """Activate a license key."""
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.api_url}/v1/license/activate",
                json={
                    "license_key": license_key,
                    "machine_id": machine_id,
                },
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return LicenseInfo(
            license_key=data["license_key"],
            tier=data["tier"],
            status=data["status"],
            is_active=data["is_active"],
            limits=data["limits"],
        )
    
    def get_license_status(self) -> LicenseInfo:
        """Get current license status."""
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/license/status",
                headers=self._get_headers(),
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return LicenseInfo(
            license_key=data["license_key"],
            tier=data["tier"],
            status=data["status"],
            is_active=data["is_active"],
            limits=data["limits"],
        )
    
    def request_trial(self, email: str) -> dict:
        """Request a verification code for trial signup."""
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.api_url}/v1/license/trial/request",
                json={"email": email},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()
    
    def verify_trial(self, email: str, code: str) -> LicenseInfo:
        """Verify code and create trial license."""
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.api_url}/v1/license/trial/verify",
                json={"email": email, "code": code},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return LicenseInfo(
            license_key=data["license_key"],
            tier=data["tier"],
            status=data["status"],
            is_active=data["is_active"],
            limits=data["limits"],
        )
    
    def create_trial(self, email: str) -> LicenseInfo:
        """Legacy method - now requires email verification."""
        # This method is kept for backward compatibility
        # But will fail because verification is now required
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.api_url}/v1/license/trial",
                json={"email": email},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        data = response.json()
        return LicenseInfo(
            license_key=data["license_key"],
            tier=data["tier"],
            status=data["status"],
            is_active=data["is_active"],
            limits=data["limits"],
        )
    
    def deactivate_license(self) -> bool:
        """Deactivate current license (for machine swap)."""
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.api_url}/v1/license/deactivate",
                json={"license_key": self.license_key},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return True
    
    # ============================================================
    # Analytics Methods
    # ============================================================
    
    def get_analytics_stats(self, period: str = "month") -> dict:
        """
        Get usage statistics for a period.
        
        Args:
            period: One of: today, yesterday, week, month, quarter, year, all
        
        Returns:
            Dictionary with usage stats, cost, and ROI
        """
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/analytics/stats",
                headers=self._get_headers(),
                params={"period": period},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()
    
    def get_analytics_daily(self, days: int = 30) -> dict:
        """Get daily usage breakdown."""
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/analytics/daily",
                headers=self._get_headers(),
                params={"days": days},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()
    
    def get_analytics_activity(self, limit: int = 50) -> dict:
        """Get recent generation activity."""
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/analytics/activity",
                headers=self._get_headers(),
                params={"limit": limit},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()
    
    def get_analytics_roi(
        self, 
        period: str = "month", 
        hourly_rate: float = 75.0
    ) -> dict:
        """
        Get ROI report for executive dashboard.
        
        Args:
            period: Time period
            hourly_rate: Developer hourly rate for value calculation
        
        Returns:
            Dictionary with ROI calculations
        """
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/analytics/roi",
                headers=self._get_headers(),
                params={"period": period, "hourly_rate": hourly_rate},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()
    
    def get_analytics_team(self, domain: str, period: str = "month") -> dict:
        """
        Get team usage statistics (Team/Enterprise only).
        
        Args:
            domain: Email domain (e.g., "acme.com")
            period: Time period
        
        Returns:
            Dictionary with team statistics
        """
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{self.api_url}/v1/analytics/team",
                headers=self._get_headers(),
                params={"domain": domain, "period": period},
            )
        
        if not response.is_success:
            self._handle_error(response)
        
        return response.json()


# Singleton instance
_client: Optional[EngineAPIClient] = None


def get_api_client() -> EngineAPIClient:
    """Get or create API client instance."""
    global _client
    if _client is None:
        _client = EngineAPIClient()
    return _client
