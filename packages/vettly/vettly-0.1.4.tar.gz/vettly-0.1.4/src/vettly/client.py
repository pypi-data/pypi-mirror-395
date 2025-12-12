"""Vettly SDK client implementations."""

import asyncio
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional, Union

import httpx

from vettly.exceptions import (
    VettlyAPIError,
    VettlyAuthError,
    VettlyQuotaError,
    VettlyRateLimitError,
    VettlyServerError,
    VettlyValidationError,
)
from vettly.models import (
    Action,
    BatchCheckResponse,
    BatchItem,
    CheckResponse,
    ContentType,
    Decision,
    Policy,
    Webhook,
    WebhookDelivery,
)

__version__ = "0.1.4"

DEFAULT_API_URL = "https://api.vettly.dev"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0


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
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ) -> None:
        """
        Initialize the Vettly client.

        Args:
            api_key: Your Vettly API key
            api_url: Base URL for the API (default: https://api.vettly.dev)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for rate limits and server errors (default: 3)
            retry_delay: Base delay in seconds for exponential backoff (default: 1.0)
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._client = httpx.Client(
            base_url=self.api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"vettly-python/{__version__}",
                "X-Vettly-SDK-Version": __version__,
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
            try:
                body = response.json()
            except Exception:
                body = {"error": response.text}

            # Check if it's a quota error vs rate limit
            if body.get("code") == "QUOTA_EXCEEDED":
                raise VettlyQuotaError(
                    body.get("error", "Quota exceeded"),
                    status_code=429,
                    quota=body.get("quota"),
                    response_body=body,
                )

            retry_after = response.headers.get("Retry-After")
            raise VettlyRateLimitError(
                body.get("error", "Rate limit exceeded"),
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
                response_body=body,
            )
        if response.status_code == 422:
            try:
                body = response.json()
            except Exception:
                body = {"error": response.text}
            raise VettlyValidationError(
                body.get("error", "Validation error"),
                status_code=422,
                errors=body.get("errors"),
                response_body=body,
            )
        if response.status_code >= 500:
            raise VettlyServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        if not response.is_success:
            raise VettlyAPIError(
                f"API request failed: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        return response.json()

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make a request with automatic retry logic."""
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)

                # Check for retryable errors
                if response.status_code == 429:
                    try:
                        body = response.json()
                    except Exception:
                        body = {}

                    # Don't retry quota errors
                    if body.get("code") == "QUOTA_EXCEEDED":
                        return self._handle_response(response)

                    # Retry rate limits
                    if attempt < self.max_retries:
                        retry_after = response.headers.get("Retry-After")
                        delay = (
                            float(retry_after)
                            if retry_after
                            else self.retry_delay * (2 ** attempt)
                        )
                        time.sleep(delay)
                        continue

                if response.status_code >= 500 and attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue

                return self._handle_response(response)

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise VettlyAPIError(
                    f"Request failed after {self.max_retries} retries: {e}",
                    code="NETWORK_ERROR",
                )

        if last_error:
            raise VettlyAPIError(
                f"Request failed: {last_error}",
                code="RETRY_EXHAUSTED",
            )
        raise VettlyAPIError("Request failed", code="UNKNOWN_ERROR")

    # Content Moderation

    def check(
        self,
        content: str,
        policy_id: str,
        *,
        content_type: Union[ContentType, str] = ContentType.TEXT,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> CheckResponse:
        """
        Check content for moderation.

        Args:
            content: The content to moderate
            policy_id: ID of the policy to apply
            content_type: Type of content (text, image, video)
            metadata: Optional metadata to attach
            user_id: Optional user ID for tracking
            request_id: Optional idempotency key to prevent duplicate processing

        Returns:
            CheckResponse with moderation results
        """
        payload: Dict[str, Any] = {
            "content": content,
            "policyId": policy_id,
            "contentType": content_type.value if isinstance(content_type, ContentType) else content_type,
        }
        if metadata:
            payload["metadata"] = metadata
        if user_id:
            payload["userId"] = user_id
        if request_id:
            payload["requestId"] = request_id

        data = self._request("POST", "/v1/check", json=payload)
        return CheckResponse.model_validate(data)

    def check_image(
        self,
        image_url: str,
        policy_id: str,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> CheckResponse:
        """
        Check an image for moderation.

        Args:
            image_url: URL or base64 data URI of the image
            policy_id: ID of the policy to apply
            metadata: Optional metadata to attach
            user_id: Optional user ID for tracking
            request_id: Optional idempotency key to prevent duplicate processing

        Returns:
            CheckResponse with moderation results
        """
        return self.check(
            content=image_url,
            policy_id=policy_id,
            content_type=ContentType.IMAGE,
            metadata=metadata,
            user_id=user_id,
            request_id=request_id,
        )

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
        payload: Dict[str, Any] = {
            "content": "dry-run",
            "policyId": policy_id,
        }
        if mock_scores:
            payload["mockScores"] = mock_scores

        return self._request("POST", "/v1/check/dry-run", json=payload)

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
        data = self._request("POST", "/v1/batch/check", json=payload)
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
        data = self._request("POST", "/v1/batch/check/async", json=payload)
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
        payload: Dict[str, Any] = {
            "policyId": policy_id,
            "yamlContent": yaml_content,
        }
        if user_id:
            payload["userId"] = user_id

        data = self._request("POST", "/v1/policies", json=payload)
        return Policy.model_validate(data)

    def get_policy(self, policy_id: str) -> Policy:
        """Get a specific policy by ID."""
        data = self._request("GET", f"/v1/policies/{policy_id}")
        return Policy.model_validate(data)

    def list_policies(self) -> List[Policy]:
        """List all policies."""
        data = self._request("GET", "/v1/policies")
        return [Policy.model_validate(p) for p in data.get("policies", [])]

    # Decisions

    def get_decision(self, decision_id: str) -> Decision:
        """Get a specific decision by ID."""
        data = self._request("GET", f"/v1/decisions/{decision_id}")
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
        data = self._request(
            "GET",
            "/v1/decisions",
            params={"limit": limit, "offset": offset},
        )
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
        data = self._request(
            "POST",
            f"/v1/decisions/{decision_id}/replay",
            json={"policyId": policy_id},
        )
        return CheckResponse.model_validate(data)

    def get_curl_command(self, decision_id: str) -> str:
        """Get cURL command to reproduce a decision."""
        data = self._request("GET", f"/v1/decisions/{decision_id}/curl")
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
        payload: Dict[str, Any] = {"url": url, "events": events}
        if description:
            payload["description"] = description

        data = self._request("POST", "/v1/webhooks", json=payload)
        return Webhook.model_validate(data)

    def list_webhooks(self) -> List[Webhook]:
        """List all webhook endpoints."""
        data = self._request("GET", "/v1/webhooks")
        return [Webhook.model_validate(w) for w in data.get("webhooks", [])]

    def get_webhook(self, webhook_id: str) -> Webhook:
        """Get a specific webhook by ID."""
        data = self._request("GET", f"/v1/webhooks/{webhook_id}")
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

        data = self._request("PATCH", f"/v1/webhooks/{webhook_id}", json=payload)
        return Webhook.model_validate(data)

    def delete_webhook(self, webhook_id: str) -> None:
        """Delete a webhook endpoint."""
        self._request("DELETE", f"/v1/webhooks/{webhook_id}")

    def test_webhook(self, webhook_id: str, event_type: str) -> Dict[str, Any]:
        """Send a test event to a webhook."""
        return self._request(
            "POST",
            f"/v1/webhooks/{webhook_id}/test",
            json={"eventType": event_type},
        )

    def get_webhook_deliveries(
        self,
        webhook_id: str,
        limit: int = 50,
    ) -> List[WebhookDelivery]:
        """Get delivery logs for a webhook."""
        data = self._request(
            "GET",
            f"/v1/webhooks/{webhook_id}/deliveries",
            params={"limit": limit},
        )
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
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ) -> None:
        """
        Initialize the async Vettly client.

        Args:
            api_key: Your Vettly API key
            api_url: Base URL for the API (default: https://api.vettly.dev)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for rate limits and server errors (default: 3)
            retry_delay: Base delay in seconds for exponential backoff (default: 1.0)
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"vettly-python/{__version__}",
                "X-Vettly-SDK-Version": __version__,
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
            try:
                body = response.json()
            except Exception:
                body = {"error": response.text}

            if body.get("code") == "QUOTA_EXCEEDED":
                raise VettlyQuotaError(
                    body.get("error", "Quota exceeded"),
                    status_code=429,
                    quota=body.get("quota"),
                    response_body=body,
                )

            retry_after = response.headers.get("Retry-After")
            raise VettlyRateLimitError(
                body.get("error", "Rate limit exceeded"),
                status_code=429,
                retry_after=int(retry_after) if retry_after else None,
                response_body=body,
            )
        if response.status_code == 422:
            try:
                body = response.json()
            except Exception:
                body = {"error": response.text}
            raise VettlyValidationError(
                body.get("error", "Validation error"),
                status_code=422,
                errors=body.get("errors"),
                response_body=body,
            )
        if response.status_code >= 500:
            raise VettlyServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        if not response.is_success:
            raise VettlyAPIError(
                f"API request failed: {response.text}",
                status_code=response.status_code,
                response_body=response.text,
            )
        return response.json()

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make a request with automatic retry logic."""
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)

                if response.status_code == 429:
                    try:
                        body = response.json()
                    except Exception:
                        body = {}

                    if body.get("code") == "QUOTA_EXCEEDED":
                        return self._handle_response(response)

                    if attempt < self.max_retries:
                        retry_after = response.headers.get("Retry-After")
                        delay = (
                            float(retry_after)
                            if retry_after
                            else self.retry_delay * (2 ** attempt)
                        )
                        await asyncio.sleep(delay)
                        continue

                if response.status_code >= 500 and attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue

                return self._handle_response(response)

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                last_error = e
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise VettlyAPIError(
                    f"Request failed after {self.max_retries} retries: {e}",
                    code="NETWORK_ERROR",
                )

        if last_error:
            raise VettlyAPIError(
                f"Request failed: {last_error}",
                code="RETRY_EXHAUSTED",
            )
        raise VettlyAPIError("Request failed", code="UNKNOWN_ERROR")

    async def check(
        self,
        content: str,
        policy_id: str,
        *,
        content_type: Union[ContentType, str] = ContentType.TEXT,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> CheckResponse:
        """Check content for moderation."""
        payload: Dict[str, Any] = {
            "content": content,
            "policyId": policy_id,
            "contentType": content_type.value if isinstance(content_type, ContentType) else content_type,
        }
        if metadata:
            payload["metadata"] = metadata
        if user_id:
            payload["userId"] = user_id
        if request_id:
            payload["requestId"] = request_id

        data = await self._request("POST", "/v1/check", json=payload)
        return CheckResponse.model_validate(data)

    async def check_image(
        self,
        image_url: str,
        policy_id: str,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> CheckResponse:
        """Check an image for moderation."""
        return await self.check(
            content=image_url,
            policy_id=policy_id,
            content_type=ContentType.IMAGE,
            metadata=metadata,
            user_id=user_id,
            request_id=request_id,
        )

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
        data = await self._request("POST", "/v1/batch/check", json=payload)
        return BatchCheckResponse.model_validate(data)

    async def get_policy(self, policy_id: str) -> Policy:
        """Get a specific policy by ID."""
        data = await self._request("GET", f"/v1/policies/{policy_id}")
        return Policy.model_validate(data)

    async def list_policies(self) -> List[Policy]:
        """List all policies."""
        data = await self._request("GET", "/v1/policies")
        return [Policy.model_validate(p) for p in data.get("policies", [])]

    async def get_decision(self, decision_id: str) -> Decision:
        """Get a specific decision by ID."""
        data = await self._request("GET", f"/v1/decisions/{decision_id}")
        return Decision.model_validate(data)

    async def list_decisions(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Decision]:
        """List recent decisions."""
        data = await self._request(
            "GET",
            "/v1/decisions",
            params={"limit": limit, "offset": offset},
        )
        return [Decision.model_validate(d) for d in data.get("decisions", [])]


# ============================================================================
# Webhook Signature Verification
# ============================================================================


def verify_webhook_signature(
    payload: str,
    signature: str,
    secret: str,
    tolerance: int = 300,
) -> bool:
    """
    Verify a webhook signature.

    Args:
        payload: The raw request body as a string
        signature: The X-Vettly-Signature header value
        secret: Your webhook secret
        tolerance: Maximum age of the signature in seconds (default: 300)

    Returns:
        True if the signature is valid, False otherwise
    """
    # Parse signature header (format: t=timestamp,v1=signature)
    parts = signature.split(",")
    timestamp_part = next((p for p in parts if p.startswith("t=")), None)
    signature_part = next((p for p in parts if p.startswith("v1=")), None)

    if not timestamp_part or not signature_part:
        return False

    timestamp = timestamp_part[2:]
    expected_signature = signature_part[3:]

    # Check timestamp is within tolerance
    try:
        timestamp_int = int(timestamp)
    except ValueError:
        return False

    now = int(time.time())
    if abs(now - timestamp_int) > tolerance:
        return False

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload}"
    computed_signature = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison
    return hmac.compare_digest(computed_signature, expected_signature)


def construct_webhook_event(payload: str) -> Dict[str, Any]:
    """
    Construct a webhook event from a verified payload.

    Args:
        payload: The raw request body as a string

    Returns:
        Dict with type, data, and timestamp fields
    """
    parsed = json.loads(payload)
    return {
        "type": parsed["type"],
        "data": parsed["data"],
        "timestamp": parsed["timestamp"],
    }
