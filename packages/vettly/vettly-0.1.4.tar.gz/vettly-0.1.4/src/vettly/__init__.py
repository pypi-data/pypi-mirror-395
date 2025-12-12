"""
Vettly Python SDK - Content moderation made simple.

Usage:
    from vettly import ModerationClient

    client = ModerationClient(api_key="your-api-key")
    result = client.check(content="Hello world", policy_id="moderate")

    if result.action == "block":
        print("Content blocked!")
"""

from vettly.client import (
    ModerationClient,
    AsyncModerationClient,
    verify_webhook_signature,
    construct_webhook_event,
)
from vettly.models import (
    CheckRequest,
    CheckResponse,
    CategoryResult,
    ContentType,
    Action,
    Decision,
    Policy,
    Webhook,
    WebhookDelivery,
    BatchCheckRequest,
    BatchCheckResponse,
    BatchItem,
    BatchResult,
)
from vettly.exceptions import (
    VettlyError,
    VettlyAPIError,
    VettlyAuthError,
    VettlyRateLimitError,
    VettlyQuotaError,
    VettlyValidationError,
    VettlyServerError,
)

__version__ = "0.1.4"
__all__ = [
    # Clients
    "ModerationClient",
    "AsyncModerationClient",
    # Webhook utilities
    "verify_webhook_signature",
    "construct_webhook_event",
    # Models
    "CheckRequest",
    "CheckResponse",
    "CategoryResult",
    "ContentType",
    "Action",
    "Decision",
    "Policy",
    "Webhook",
    "WebhookDelivery",
    "BatchCheckRequest",
    "BatchCheckResponse",
    "BatchItem",
    "BatchResult",
    # Exceptions
    "VettlyError",
    "VettlyAPIError",
    "VettlyAuthError",
    "VettlyRateLimitError",
    "VettlyQuotaError",
    "VettlyValidationError",
    "VettlyServerError",
]
