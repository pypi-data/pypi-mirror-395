from typing import Literal

from pydantic import BaseModel, Field, model_validator


class GenerationParams(BaseModel):
    """Generation parameters for experiment level overrides.

    All 6 sampling parameters are stored, providing a snapshot
    of the advanced generation settings used for an experiment.

    Supported fields:
    - temperature: Controls randomness (mutually exclusive with reasoning_effort)
    - reasoning_effort: For o-series models (mutually exclusive with temperature)
    - verbosity: Response detail level (GPT-5+)
    - top_p: Nucleus sampling threshold
    - max_tokens: Maximum tokens in response
    - max_connections: Maximum concurrent connections
    """

    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Controls randomness in generation. Higher values = more random. Null if using reasoning_effort.",
    )
    reasoning_effort: Literal["minimal", "low", "medium", "high"] | None = Field(
        default=None,
        description="Reasoning effort for OpenAI o-series models. Null if using temperature.",
    )
    verbosity: Literal["low", "medium", "high"] | None = Field(
        default=None,
        description="Verbosity level for OpenAI models (GPT-5 and newer).",
    )
    top_p: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling threshold. Only tokens with cumulative probability <= top_p are considered.",
    )
    max_tokens: int | None = Field(
        default=None,
        ge=1,
        description="Maximum number of tokens in the response.",
    )
    max_connections: int = Field(
        default=10,
        ge=1,
        description="Maximum number of concurrent connections for generation.",
    )

    @model_validator(mode="after")
    def validate_temperature_or_reasoning_effort(self) -> "GenerationParams":
        """Ensure temperature and reasoning_effort are not both set."""
        if self.temperature is not None and self.reasoning_effort is not None:
            raise ValueError("Cannot set both temperature and reasoning_effort")
        return self
