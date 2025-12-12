from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from elluminate.schemas.organization import Organization


class Project(BaseModel):
    """Project model."""

    id: int
    name: str
    description: str
    organization: Organization
    created_at: datetime
    updated_at: datetime
