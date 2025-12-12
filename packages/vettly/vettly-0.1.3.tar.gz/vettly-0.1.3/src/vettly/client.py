"""Vettly SDK client implementations."""

from typing import Any, Dict, List, Optional, Union

import httpx

from vettly.exceptions import (
    VettlyAPIError,
    VettlyAuthError,
    VettlyRateLimitError,
    VettlyValidationError,
)
from vettly.models import (
    Action,
    BatchCheckRequest,
    BatchCheckResponse,
    BatchItem,
    CheckResponse,
    ContentType,
    Decision,
    Policy,
    Webhook,
    WebhookDelivery,
)

DEFAULT_API_URL = "https://api.vettly.dev"
DEFAULT_TIMEOUT = 30.0


class ModerationClient:
    """
    Synchronous client for Vettly content moderation API.

    Usage:
        client = ModerationClient(api_key="your-api-key")
        result = client.check(content="Hello world", policy_id="moderate")

        if result.action == Action.BLOCK:
            print("Content blocked!")
    """

    def __init__(
        self,
        api_key: str,
        *,
        api_url: str = DEFAULT_API_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the Vettly client.

        Args:
            api_key: Your Vettly API key
            api_url: Base URL for the API (default: https://api.vettly.dev)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "vettly-python/0.1.0",
            },
            timeout=timeout,
        )

    def __enter__(self) -> "ModerationClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 401:
            raise VettlyAuthError(
                "Invalid API key",
                status_code=401,
                response_body=response.text,
            )
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise VettlyRateLimitError(
                "Rate limit exceeded",
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
            )
        if response.status_code == 422:
            raise VettlyValidationError(
                "Validation error",
                status_code=422,
                response_body=response.json(),
            )
        if not response.is_success:
            raise VettlyAPIError(
                f"API request failed: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        return response.json()

    # Content Moderation

    def check(
        self,
        content: str,
        policy_id: str,
        *,
        content_type: Union[ContentType, str] = ContentType.TEXT,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
    ) -> CheckResponse:
        """
        Check content for moderation.

        Args:
            content: The content to moderate
            policy_id: ID of the policy to apply
            content_type: Type of content (text, image, video)
            metadata: Optional metadata to attach
            user_id: Optional user ID for tracking

        Returns:
            CheckResponse with moderation results
        """
        payload = {
            "content": content,
            "policyId": policy_id,
            "contentType": content_type.value if isinstance(content_type, ContentType) else content_type,
        }
        if metadata:
            payload["metadata"] = metadata
        if user_id:
            payload["userId"] = user_id

        response = self._client.post("/v1/check", json=payload)
        data = self._handle_response(response)
        return CheckResponse.model_validate(data)

    def dry_run(
        self,
        policy_id: str,
        mock_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Dry-run a policy without making provider calls.

        Args:
            policy_id: ID of the policy to test
            mock_scores: Optional mock category scores

        Returns:
            Dict with dry-run results
        """
        payload = {
            "content": "dry-run",
            "policyId": policy_id,
        }
        if mock_scores:
            payload["mockScores"] = mock_scores

        response = self._client.post("/v1/check/dry-run", json=payload)
        return self._handle_response(response)

    # Batch Operations

    def batch_check(
        self,
        policy_id: str,
        items: List[BatchItem],
    ) -> BatchCheckResponse:
        """
        Check multiple items synchronously.

        Args:
            policy_id: ID of the policy to apply
            items: List of items to moderate

        Returns:
            BatchCheckResponse with results for all items
        """
        payload = {
            "policyId": policy_id,
            "items": [item.model_dump(by_alias=True) for item in items],
        }
        response = self._client.post("/v1/batch/check", json=payload)
        data = self._handle_response(response)
        return BatchCheckResponse.model_validate(data)

    def batch_check_async(
        self,
        policy_id: str,
        items: List[BatchItem],
        webhook_url: str,
    ) -> BatchCheckResponse:
        """
        Check multiple items asynchronously with webhook delivery.

        Args:
            policy_id: ID of the policy to apply
            items: List of items to moderate
            webhook_url: URL to receive results

        Returns:
            BatchCheckResponse with batch ID for tracking
        """
        payload = {
            "policyId": policy_id,
            "items": [item.model_dump(by_alias=True) for item in items],
            "webhookUrl": webhook_url,
        }
        response = self._client.post("/v1/batch/check/async", json=payload)
        data = self._handle_response(response)
        return BatchCheckResponse.model_validate(data)

    # Policies

    def create_policy(
        self,
        policy_id: str,
        yaml_content: str,
        user_id: Optional[str] = None,
    ) -> Policy:
        """
        Create or update a policy.

        Args:
            policy_id: Unique ID for the policy
            yaml_content: Policy configuration in YAML format
            user_id: Optional user ID for ownership

        Returns:
            Created Policy object
        """
        payload = {
            "policyId": policy_id,
            "yamlContent": yaml_content,
        }
        if user_id:
            payload["userId"] = user_id

        response = self._client.post("/v1/policies", json=payload)
        data = self._handle_response(response)
        return Policy.model_validate(data)

    def get_policy(self, policy_id: str) -> Policy:
        """Get a specific policy by ID."""
        response = self._client.get(f"/v1/policies/{policy_id}")
        data = self._handle_response(response)
        return Policy.model_validate(data)

    def list_policies(self) -> List[Policy]:
        """List all policies."""
        response = self._client.get("/v1/policies")
        data = self._handle_response(response)
        return [Policy.model_validate(p) for p in data.get("policies", [])]

    # Decisions

    def get_decision(self, decision_id: str) -> Decision:
        """Get a specific decision by ID."""
        response = self._client.get(f"/v1/decisions/{decision_id}")
        data = self._handle_response(response)
        return Decision.model_validate(data)

    def list_decisions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Decision]:
        """
        List recent decisions.

        Args:
            limit: Maximum number of decisions to return
            offset: Number of decisions to skip

        Returns:
            List of Decision objects
        """
        response = self._client.get(
            "/v1/decisions",
            params={"limit": limit, "offset": offset},
        )
        data = self._handle_response(response)
        return [Decision.model_validate(d) for d in data.get("decisions", [])]

    def replay_decision(self, decision_id: str, policy_id: str) -> CheckResponse:
        """
        Replay a decision with a different policy.

        Args:
            decision_id: ID of the original decision
            policy_id: ID of the policy to use for replay

        Returns:
            CheckResponse with new results
        """
        response = self._client.post(
            f"/v1/decisions/{decision_id}/replay",
            json={"policyId": policy_id},
        )
        data = self._handle_response(response)
        return CheckResponse.model_validate(data)

    def get_curl_command(self, decision_id: str) -> str:
        """Get cURL command to reproduce a decision."""
        response = self._client.get(f"/v1/decisions/{decision_id}/curl")
        data = self._handle_response(response)
        return data["curl"]

    # Webhooks

    def register_webhook(
        self,
        url: str,
        events: List[str],
        description: Optional[str] = None,
    ) -> Webhook:
        """
        Register a webhook endpoint.

        Args:
            url: Webhook URL
            events: List of event types to subscribe to
            description: Optional description

        Returns:
            Created Webhook object
        """
        payload = {"url": url, "events": events}
        if description:
            payload["description"] = description

        response = self._client.post("/v1/webhooks", json=payload)
        data = self._handle_response(response)
        return Webhook.model_validate(data)

    def list_webhooks(self) -> List[Webhook]:
        """List all webhook endpoints."""
        response = self._client.get("/v1/webhooks")
        data = self._handle_response(response)
        return [Webhook.model_validate(w) for w in data.get("webhooks", [])]

    def get_webhook(self, webhook_id: str) -> Webhook:
        """Get a specific webhook by ID."""
        response = self._client.get(f"/v1/webhooks/{webhook_id}")
        data = self._handle_response(response)
        return Webhook.model_validate(data)

    def update_webhook(
        self,
        webhook_id: str,
        *,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Webhook:
        """Update a webhook endpoint."""
        payload: Dict[str, Any] = {}
        if url is not None:
            payload["url"] = url
        if events is not None:
            payload["events"] = events
        if description is not None:
            payload["description"] = description
        if enabled is not None:
            payload["enabled"] = enabled

        response = self._client.patch(f"/v1/webhooks/{webhook_id}", json=payload)
        data = self._handle_response(response)
        return Webhook.model_validate(data)

    def delete_webhook(self, webhook_id: str) -> None:
        """Delete a webhook endpoint."""
        response = self._client.delete(f"/v1/webhooks/{webhook_id}")
        if not response.is_success:
            self._handle_response(response)

    def test_webhook(self, webhook_id: str, event_type: str) -> Dict[str, Any]:
        """Send a test event to a webhook."""
        response = self._client.post(
            f"/v1/webhooks/{webhook_id}/test",
            json={"eventType": event_type},
        )
        return self._handle_response(response)

    def get_webhook_deliveries(
        self,
        webhook_id: str,
        limit: int = 50,
    ) -> List[WebhookDelivery]:
        """Get delivery logs for a webhook."""
        response = self._client.get(
            f"/v1/webhooks/{webhook_id}/deliveries",
            params={"limit": limit},
        )
        data = self._handle_response(response)
        return [WebhookDelivery.model_validate(d) for d in data.get("deliveries", [])]


class AsyncModerationClient:
    """
    Async client for Vettly content moderation API.

    Usage:
        async with AsyncModerationClient(api_key="your-api-key") as client:
            result = await client.check(content="Hello world", policy_id="moderate")

            if result.action == Action.BLOCK:
                print("Content blocked!")
    """

    def __init__(
        self,
        api_key: str,
        *,
        api_url: str = DEFAULT_API_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the async Vettly client.

        Args:
            api_key: Your Vettly API key
            api_url: Base URL for the API (default: https://api.vettly.dev)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "vettly-python/0.1.0",
            },
            timeout=timeout,
        )

    async def __aenter__(self) -> "AsyncModerationClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 401:
            raise VettlyAuthError(
                "Invalid API key",
                status_code=401,
                response_body=response.text,
            )
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise VettlyRateLimitError(
                "Rate limit exceeded",
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
            )
        if response.status_code == 422:
            raise VettlyValidationError(
                "Validation error",
                status_code=422,
                response_body=response.json(),
            )
        if not response.is_success:
            raise VettlyAPIError(
                f"API request failed: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        return response.json()

    async def check(
        self,
        content: str,
        policy_id: str,
        *,
        content_type: Union[ContentType, str] = ContentType.TEXT,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
    ) -> CheckResponse:
        """Check content for moderation."""
        payload = {
            "content": content,
            "policyId": policy_id,
            "contentType": content_type.value if isinstance(content_type, ContentType) else content_type,
        }
        if metadata:
            payload["metadata"] = metadata
        if user_id:
            payload["userId"] = user_id

        response = await self._client.post("/v1/check", json=payload)
        data = self._handle_response(response)
        return CheckResponse.model_validate(data)

    async def batch_check(
        self,
        policy_id: str,
        items: List[BatchItem],
    ) -> BatchCheckResponse:
        """Check multiple items."""
        payload = {
            "policyId": policy_id,
            "items": [item.model_dump(by_alias=True) for item in items],
        }
        response = await self._client.post("/v1/batch/check", json=payload)
        data = self._handle_response(response)
        return BatchCheckResponse.model_validate(data)

    async def get_policy(self, policy_id: str) -> Policy:
        """Get a specific policy by ID."""
        response = await self._client.get(f"/v1/policies/{policy_id}")
        data = self._handle_response(response)
        return Policy.model_validate(data)

    async def list_policies(self) -> List[Policy]:
        """List all policies."""
        response = await self._client.get("/v1/policies")
        data = self._handle_response(response)
        return [Policy.model_validate(p) for p in data.get("policies", [])]

    async def get_decision(self, decision_id: str) -> Decision:
        """Get a specific decision by ID."""
        response = await self._client.get(f"/v1/decisions/{decision_id}")
        data = self._handle_response(response)
        return Decision.model_validate(data)

    async def list_decisions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Decision]:
        """List recent decisions."""
        response = await self._client.get(
            "/v1/decisions",
            params={"limit": limit, "offset": offset},
        )
        data = self._handle_response(response)
        return [Decision.model_validate(d) for d in data.get("decisions", [])]
