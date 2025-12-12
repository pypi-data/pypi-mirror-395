from elluminate.schemas.conversation import (
    ResolvedPromptContext,
    ResponseFormat,
    UCEInput,
    UCEPayloadV1,
)
from elluminate.schemas.criterion import (
    CreateCriteriaRequest,
    Criterion,
)
from elluminate.schemas.criterion_set import (
    CreateCriterionSetRequest,
    CriterionSet,
)
from elluminate.schemas.experiments import (
    CreateExperimentRequest,
    Experiment,
    ExperimentFilter,
    ExperimentGenerationStatus,
    ExperimentResults,
    MeanRating,
)
from elluminate.schemas.generation_metadata import GenerationMetadata
from elluminate.schemas.generation_params import GenerationParams
from elluminate.schemas.llm_config import InferenceType, LLMConfig
from elluminate.schemas.organization import Organization
from elluminate.schemas.project import Project
from elluminate.schemas.prompt import Prompt
from elluminate.schemas.prompt_template import (
    CreatePromptTemplateRequest,
    PromptTemplate,
    PromptTemplateFilter,
    TemplateString,
)
from elluminate.schemas.rating import (
    BatchCreateRatingRequest,
    BatchCreateRatingResponseStatus,
    CreateRatingRequest,
    Rating,
    RatingMode,
)
from elluminate.schemas.response import (
    BatchCreatePromptResponseRequest,
    BatchCreatePromptResponseStatus,
    CreatePromptResponseRequest,
    DailyUsageStats,
    PromptResponse,
    PromptResponseFilter,
    RatingValue,
    ResponsesSample,
    ResponsesSampleFilter,
    ResponsesSampleSortBy,
    ResponsesStats,
)
from elluminate.schemas.template_variables import (
    CreateTemplateVariablesRequest,
    TemplateVariables,
)
from elluminate.schemas.template_variables_collection import (
    CollectionColumn,
    ColumnTypeEnum,
    CreateCollectionRequest,
    TemplateVariablesCollection,
    TemplateVariablesCollectionFilter,
    TemplateVariablesCollectionSort,
    TemplateVariablesCollectionWithEntries,
    UpdateCollectionRequest,
)

# Rebuild models to handle circular references.
# 1. First rebuild TemplateVariables since it references the base TemplateVariablesCollection
# 2. Then rebuild TemplateVariablesCollectionWithEntries since it contains TemplateVariables
# 3. Rebuild Experiment since it references CriterionSet
TemplateVariables.model_rebuild()
TemplateVariablesCollectionWithEntries.model_rebuild()
Experiment.model_rebuild()

__all__ = [
    "Organization",
    "Project",
    "PromptTemplate",
    "CreatePromptTemplateRequest",
    "CreateTemplateVariablesRequest",
    "TemplateVariables",
    "TemplateVariablesCollection",
    "CreateCollectionRequest",
    "UpdateCollectionRequest",
    "CollectionColumn",
    "ColumnTypeEnum",
    "TemplateVariablesCollectionFilter",
    "TemplateVariablesCollectionSort",
    "BatchCreatePromptResponseStatus",
    "PromptResponse",
    "PromptResponseFilter",
    "ResponsesSample",
    "ResponsesSampleFilter",
    "ResponsesSampleSortBy",
    "ResponsesStats",
    "DailyUsageStats",
    "RatingValue",
    "CreatePromptResponseRequest",
    "BatchCreatePromptResponseRequest",
    "LLMConfig",
    "InferenceType",
    "GenerationMetadata",
    "GenerationParams",
    "Criterion",
    "CriterionSet",
    "CreateCriterionSetRequest",
    "Rating",
    "Prompt",
    "Experiment",
    "ExperimentGenerationStatus",
    "ExperimentResults",
    "MeanRating",
    "BatchCreateRatingRequest",
    "BatchCreateRatingResponseStatus",
    "CreateRatingRequest",
    "RatingMode",
    "TemplateString",
    "CreateExperimentRequest",
    "CreateCriteriaRequest",
    "PromptTemplateFilter",
    "ExperimentFilter",
    "TemplateVariablesCollectionWithEntries",
    "UCEPayloadV1",
    "UCEInput",
    "ResponseFormat",
    "ResolvedPromptContext",
]
