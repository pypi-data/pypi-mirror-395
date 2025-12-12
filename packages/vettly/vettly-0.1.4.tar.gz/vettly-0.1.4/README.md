# vettly

Content moderation that just works. One API for text, images, and video.

## Installation

```bash
pip install vettly
```

## Quick Start

```python
from vettly import ModerationClient

client = ModerationClient("sk_live_...")

result = client.check(
    content="User-generated text",
    policy_id="community-safe"
)

if result.action == "block":
    # Content blocked
    pass
```

## Get Your API Key

1. Sign up at [vettly.dev](https://vettly.dev)
2. Go to Dashboard → API Keys
3. Create and copy your key

## Features

- **Text, images, video** - One unified API for all content types
- **Custom policies** - Define thresholds in YAML
- **Webhooks** - Get notified when content is flagged
- **Dashboard** - Monitor decisions and export logs
- **Automatic retries** - Exponential backoff for rate limits and server errors
- **Async support** - Full async/await support with `AsyncModerationClient`

## Text Moderation

```python
result = client.check(
    content="User-generated text",
    policy_id="community-safe"
)

print(result.action)      # 'allow' | 'flag' | 'block'
print(result.categories)  # List of CategoryResult
print(result.id)          # Decision ID for audit trail
```

## Image Moderation

```python
# From URL
result = client.check_image(
    image_url="https://example.com/image.jpg",
    policy_id="strict"
)

# From base64
result = client.check_image(
    image_url="data:image/jpeg;base64,/9j/4AAQ...",
    policy_id="strict"
)
```

## Idempotency

Prevent duplicate processing with request IDs:

```python
result = client.check(
    content="Hello",
    policy_id="default",
    request_id="unique-request-id-123"
)
```

## Error Handling

The SDK provides typed exceptions for better error handling:

```python
from vettly import (
    VettlyAuthError,
    VettlyRateLimitError,
    VettlyQuotaError,
    VettlyValidationError,
)

try:
    result = client.check(content="test", policy_id="default")
except VettlyAuthError:
    print("Invalid API key")
except VettlyRateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except VettlyQuotaError as e:
    print(f"Quota exceeded: {e.quota}")
```

## Webhook Signature Verification

Verify webhook signatures to ensure authenticity:

```python
from vettly import verify_webhook_signature, construct_webhook_event

@app.route("/webhooks/vettly", methods=["POST"])
def handle_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get("X-Vettly-Signature")

    if not verify_webhook_signature(payload, signature, webhook_secret):
        return "Invalid signature", 401

    event = construct_webhook_event(payload)

    if event["type"] == "decision.blocked":
        # Handle blocked content
        pass

    return "OK", 200
```

## Async Support

```python
from vettly import AsyncModerationClient

async with AsyncModerationClient("sk_live_...") as client:
    result = await client.check(
        content="User content",
        policy_id="community-safe"
    )
```

## Configuration

```python
from vettly import ModerationClient

client = ModerationClient(
    api_key="sk_live_...",
    api_url="https://api.vettly.dev",  # Optional: custom API URL
    timeout=30.0,                       # Optional: request timeout in seconds
    max_retries=3,                      # Optional: max retries for failures
    retry_delay=1.0,                    # Optional: base delay for backoff in seconds
)
```

## FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from vettly import AsyncModerationClient

app = FastAPI()
client = AsyncModerationClient("sk_live_...")

@app.post("/comments")
async def create_comment(content: str):
    result = await client.check(content=content, policy_id="community-safe")

    if result.action == "block":
        raise HTTPException(403, "Content blocked")

    return {"status": "ok"}
```

## Response Format

```python
CheckResponse(
    id="550e8400-e29b-41d4-a716-446655440000",
    safe=False,
    flagged=True,
    action=Action.BLOCK,
    categories=[
        CategoryResult(category="hate_speech", score=0.91, threshold=0.8, triggered=True),
        CategoryResult(category="harassment", score=0.08, threshold=0.8, triggered=False),
    ],
    latency_ms=147,
    policy_id="community-safe",
    provider="hive",
)
```

## Pricing

| Plan | Price | Text | Images | Videos |
|------|-------|------|--------|--------|
| Developer | Free | 10,000/mo | 250/mo | 100/mo |
| Starter | $29/mo | Unlimited | 5,000/mo | 2,000/mo |
| Pro | $79/mo | Unlimited | 20,000/mo | 10,000/mo |
| Enterprise | $499/mo | Unlimited | 200,000/mo | 100,000/mo |

## Links

- [vettly.dev](https://vettly.dev) - Sign up
- [docs.vettly.dev](https://docs.vettly.dev) - Documentation
