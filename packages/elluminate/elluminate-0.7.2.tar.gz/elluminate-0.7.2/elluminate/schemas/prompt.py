from datetime import datetime
from typing import Any, List

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from elluminate.schemas.prompt_template import PromptTemplate
from elluminate.schemas.template_variables import TemplateVariables


class Prompt(BaseModel):
    """New prompt model."""

    id: int
    prompt_template: PromptTemplate | None = None
    template_variables: TemplateVariables
    messages: List[ChatCompletionMessageParam] = []
    created_at: datetime
    resolved_tools: List[dict[str, Any]] | None = None
    resolved_tool_choice: dict[str, Any] | str | None = None
    resolved_response_format: dict[str, Any] | None = None
    is_stale: bool = False
