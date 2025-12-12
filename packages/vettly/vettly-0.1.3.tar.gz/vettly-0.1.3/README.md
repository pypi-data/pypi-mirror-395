# vettly

Content moderation that just works. One API for text, images, and video.

## Installation

```bash
pip install vettly
```

## Quick Start

```python
from vettly import Vettly

client = Vettly('sk_live_...')

result = client.check(
    content='User-generated text',
    policy='community-safe'
)

if result.action == 'block':
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
- **Deterministic** - Same input, same output, every time

## Response Format

```python
{
    "action": "block",
    "categories": {
        "hate": 0.91,
        "harassment": 0.08,
        "violence": 0.12
    },
    "flags": ["hate"],
    "latency_ms": 147
}
```

## Image Moderation

```python
result = client.check_image(
    url='https://example.com/image.jpg',
    policy='strict'
)
```

## Async Support

```python
from vettly import AsyncVettly

async with AsyncVettly('sk_live_...') as client:
    result = await client.check(
        content='User content',
        policy='community-safe'
    )
```

## FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from vettly import AsyncVettly

app = FastAPI()
client = AsyncVettly('sk_live_...')

@app.post("/comments")
async def create_comment(content: str):
    result = await client.check(content=content, policy='community-safe')

    if result.action == 'block':
        raise HTTPException(403, "Content blocked")

    return {"status": "ok"}
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
