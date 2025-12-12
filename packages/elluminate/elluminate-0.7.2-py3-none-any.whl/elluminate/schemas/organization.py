from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Organization(BaseModel):
    """Organization model."""

    id: int
    name: str
    domain: str
    stripe_subscription_id: str | None
    created_at: datetime
    updated_at: datetime
