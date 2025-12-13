# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .application import Application

__all__ = [
    "Eval",
    "Definition",
    "DefinitionGlobalConfig",
    "DefinitionGlobalConfigCriterion",
    "DefinitionGlobalConfigGroundTruth",
    "DefinitionGlobalConfigOutputMatchStringConfig",
    "DefinitionGlobalConfigOutputMatchStringConfigExtract",
    "DefinitionGlobalConfigOutputMatchListConfig",
    "DefinitionGlobalConfigOutputMatchListConfigExtract",
]


class DefinitionGlobalConfigCriterion(BaseModel):
    criterion: str
    """The criterion describes what our evaluation LLM must look for in the response.

    Remember that the answer to the criterion must be as a pass/fail.
    """


class DefinitionGlobalConfigGroundTruth(BaseModel):
    ground_truth: str = FieldInfo(alias="groundTruth")
    """
    The ground truth is the most correct answer to the task that we measure the
    response against
    """


class DefinitionGlobalConfigOutputMatchStringConfigExtract(BaseModel):
    flags: str

    group: int

    pattern: str


class DefinitionGlobalConfigOutputMatchStringConfig(BaseModel):
    type: Literal["string"]

    extract: Optional[DefinitionGlobalConfigOutputMatchStringConfigExtract] = None


class DefinitionGlobalConfigOutputMatchListConfigExtract(BaseModel):
    flags: str

    group: int

    pattern: str


class DefinitionGlobalConfigOutputMatchListConfig(BaseModel):
    match_mode: Literal["exact_unordered", "contains"] = FieldInfo(alias="matchMode")

    type: Literal["list"]

    extract: Optional[DefinitionGlobalConfigOutputMatchListConfigExtract] = None


DefinitionGlobalConfig: TypeAlias = Union[
    DefinitionGlobalConfigCriterion,
    DefinitionGlobalConfigGroundTruth,
    DefinitionGlobalConfigOutputMatchStringConfig,
    DefinitionGlobalConfigOutputMatchListConfig,
]


class Definition(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the eval definition was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the eval definition was last modified"""

    name: str

    type: Literal["NATURALNESS", "STYLE", "RECALL", "CUSTOM", "FACT", "OUTPUT_MATCH"]
    """The type of evaluation"""

    application: Optional[Application] = None
    """Application configuration and metadata"""

    global_config: Optional[DefinitionGlobalConfig] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class Eval(BaseModel):
    id: str
    """Unique identifier of the evaluation"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the evaluation was created"""

    definition: Definition

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the evaluation was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this evaluation"""

    passed: bool
    """Whether the evaluation passed"""

    results: Dict[str, object]
    """Results of the evaluation (structure depends on eval type)."""

    score: float
    """Overall score of the evaluation"""

    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]
    """Status of the evaluation/test"""
