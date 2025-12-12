"""
Vettly Python SDK - Content moderation made simple.

Usage:
    from vettly import ModerationClient

    client = ModerationClient(api_key="your-api-key")
    result = client.check(content="Hello world", policy_id="moderate")

    if result.action == "block":
        print("Content blocked!")
"""

from vettly.client import ModerationClient, AsyncModerationClient
from vettly.models import (
    CheckRequest,
    CheckResponse,
    CategoryResult,
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
    VettlyValidationError,
)

__version__ = "0.1.1"
__all__ = [
    # Clients
    "ModerationClient",
    "AsyncModerationClient",
    # Models
    "CheckRequest",
    "CheckResponse",
    "CategoryResult",
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
    "VettlyValidationError",
]
