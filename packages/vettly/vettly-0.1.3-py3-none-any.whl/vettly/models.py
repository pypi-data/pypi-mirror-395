"""Vettly SDK data models."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ContentType(str, Enum):
    """Content types supported by Vettly."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class Action(str, Enum):
    """Moderation actions."""

    ALLOW = "allow"
    FLAG = "flag"
    BLOCK = "block"


class CategoryResult(BaseModel):
    """Result for a single moderation category."""

    category: str
    score: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    triggered: bool = False


class CheckRequest(BaseModel):
    """Request to check content for moderation."""

    content: str
    policy_id: str = Field(alias="policyId")
    content_type: ContentType = Field(default=ContentType.TEXT, alias="contentType")
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = Field(default=None, alias="userId")

    class Config:
        populate_by_name = True


class CheckResponse(BaseModel):
    """Response from content moderation check."""

    id: str
    safe: bool
    flagged: bool
    action: Action
    categories: List[CategoryResult]
    latency_ms: int = Field(alias="latencyMs")
    policy_id: str = Field(alias="policyId")
    provider: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")

    class Config:
        populate_by_name = True


class Decision(BaseModel):
    """A moderation decision record."""

    id: str
    content: str
    content_type: ContentType = Field(alias="contentType")
    policy_id: str = Field(alias="policyId")
    action: Action
    categories: List[CategoryResult]
    provider: str
    latency_ms: int = Field(alias="latencyMs")
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(alias="createdAt")

    class Config:
        populate_by_name = True


class Policy(BaseModel):
    """A moderation policy configuration."""

    id: str
    name: str
    description: Optional[str] = None
    yaml_content: str = Field(alias="yamlContent")
    user_id: Optional[str] = Field(default=None, alias="userId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True


class Webhook(BaseModel):
    """A webhook endpoint configuration."""

    id: str
    url: str
    events: List[str]
    description: Optional[str] = None
    enabled: bool = True
    secret: Optional[str] = None
    created_at: datetime = Field(alias="createdAt")

    class Config:
        populate_by_name = True


class WebhookDelivery(BaseModel):
    """A webhook delivery log entry."""

    id: str
    webhook_id: str = Field(alias="webhookId")
    event_type: str = Field(alias="eventType")
    payload: Dict[str, Any]
    status_code: Optional[int] = Field(default=None, alias="statusCode")
    success: bool
    error: Optional[str] = None
    delivered_at: datetime = Field(alias="deliveredAt")

    class Config:
        populate_by_name = True


class BatchItem(BaseModel):
    """A single item in a batch check request."""

    id: str
    content: str
    content_type: ContentType = Field(default=ContentType.TEXT, alias="contentType")
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True


class BatchResult(BaseModel):
    """Result for a single item in a batch check."""

    id: str
    safe: bool
    flagged: bool
    action: Action
    categories: List[CategoryResult]
    error: Optional[str] = None


class BatchCheckRequest(BaseModel):
    """Request for batch content moderation."""

    policy_id: str = Field(alias="policyId")
    items: List[BatchItem]
    webhook_url: Optional[str] = Field(default=None, alias="webhookUrl")

    class Config:
        populate_by_name = True


class BatchCheckResponse(BaseModel):
    """Response from batch content moderation."""

    batch_id: str = Field(alias="batchId")
    results: Optional[List[BatchResult]] = None
    status: str = "pending"
    total: int
    completed: int = 0
    failed: int = 0

    class Config:
        populate_by_name = True
