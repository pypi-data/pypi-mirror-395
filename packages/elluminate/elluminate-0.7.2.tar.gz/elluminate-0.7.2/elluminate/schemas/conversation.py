"""Unified conversation envelope schemas for prompt payloads."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ResponseFormat(BaseModel):
    """Unified structure for response format hints or schemas."""

    response_schema: dict[str, Any] | None = Field(None, alias="json_schema")
    hint: Literal["json_object", "text"] | None = None


class UCEInput(BaseModel):
    """Per-run overrides bundled into template variables payloads."""

    messages: list[dict[str, Any]] = Field(default_factory=list)
    tools: list[dict[str, Any]] | None = None
    tool_choice: str | dict[str, Any] | None = None
    response_format: ResponseFormat | None = None
    attachments: list[dict[str, Any]] | None = None
    metadata: dict[str, Any] | None = None


class UCEPayloadV1(BaseModel):
    """Schema-versioned payload for unified conversation envelopes."""

    schema_version: Literal["elluminate.uce/1"] = "elluminate.uce/1"
    input: UCEInput


class ResolvedPromptContext(BaseModel):
    """Runtime prompt configuration after merging template and payload."""

    messages: list[dict[str, Any]] = Field(default_factory=list)
    tools: list[dict[str, Any]] | None = None
    tool_choice: dict[str, Any] | str | None = None
    response_format: dict[str, Any] | None = None
