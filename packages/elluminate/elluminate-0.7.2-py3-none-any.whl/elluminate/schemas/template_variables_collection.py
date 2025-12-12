from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from elluminate.schemas.template_variables import TemplateVariables


class ColumnTypeEnum(str, Enum):
    # these mirror the supported backend types, not actively used yet
    TEXT = "text"
    CONVERSATION = "conversation"
    RAW_INPUT = "raw_input"
    CATEGORY = "category"


class CollectionColumn(BaseModel):
    """Column definition for a template variables collection."""

    id: int | None = None
    name: str | None = None
    column_type: ColumnTypeEnum = Field(default=ColumnTypeEnum.TEXT)
    default_value: str | None = Field(default="")
    column_position: int | None = Field(default=0)


class TemplateVariablesCollection(BaseModel):
    """Collection of template variables."""

    id: int
    name: str
    description: str
    columns: list[CollectionColumn] = Field(default_factory=list)
    variables_count: int = 0
    read_only: bool = False
    created_at: datetime
    updated_at: datetime
    version: str | None = None


class TemplateVariablesCollectionWithEntries(TemplateVariablesCollection):
    """Template variables collection with entries."""

    variables: list[TemplateVariables]


class CreateCollectionRequest(BaseModel):
    """Request to create a new template variables collection."""

    name: str | None = None
    description: str = ""
    variables: list[dict[str, Any]] | None = None
    columns: list[CollectionColumn] | None = None
    read_only: bool = False


class TemplateVariablesCollectionFilter(BaseModel):
    """Filter for template variables collections."""

    name: str | None = None
    name_search: str | None = None
    has_entries: bool | None = None


class TemplateVariablesCollectionSort(BaseModel):
    """Sort for template variables collections."""

    sort: Literal["name", "-name", "created_at", "-created_at", "updated_at", "-updated_at"] | None = None


class UpdateCollectionRequest(BaseModel):
    """Request to update a template variables collection."""

    name: str = Field(..., min_length=1)
    description: str | None = None
    read_only: bool | None = None
    columns: list[CollectionColumn] | None = Field(
        None,
        description="List of columns in the desired order. Missing columns are deleted, new columns are created as TEXT with default='', existing columns are reordered.",
    )
