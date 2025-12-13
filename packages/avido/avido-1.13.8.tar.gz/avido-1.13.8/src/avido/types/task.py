# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .application import Application

__all__ = [
    "Task",
    "EvalDefinition",
    "EvalDefinitionEvalDefinition",
    "EvalDefinitionEvalDefinitionGlobalConfig",
    "EvalDefinitionEvalDefinitionGlobalConfigCriterion",
    "EvalDefinitionEvalDefinitionGlobalConfigGroundTruth",
    "EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfig",
    "EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfigExtract",
    "EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfig",
    "EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfigExtract",
    "EvalDefinitionConfig",
    "TaskSchedule",
]


class EvalDefinitionEvalDefinitionGlobalConfigCriterion(BaseModel):
    criterion: str
    """The criterion describes what our evaluation LLM must look for in the response.

    Remember that the answer to the criterion must be as a pass/fail.
    """


class EvalDefinitionEvalDefinitionGlobalConfigGroundTruth(BaseModel):
    ground_truth: str = FieldInfo(alias="groundTruth")
    """
    The ground truth is the most correct answer to the task that we measure the
    response against
    """


class EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfigExtract(BaseModel):
    flags: str

    group: int

    pattern: str


class EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfig(BaseModel):
    type: Literal["string"]

    extract: Optional[EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfigExtract] = None


class EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfigExtract(BaseModel):
    flags: str

    group: int

    pattern: str


class EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfig(BaseModel):
    match_mode: Literal["exact_unordered", "contains"] = FieldInfo(alias="matchMode")

    type: Literal["list"]

    extract: Optional[EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfigExtract] = None


EvalDefinitionEvalDefinitionGlobalConfig: TypeAlias = Union[
    EvalDefinitionEvalDefinitionGlobalConfigCriterion,
    EvalDefinitionEvalDefinitionGlobalConfigGroundTruth,
    EvalDefinitionEvalDefinitionGlobalConfigOutputMatchStringConfig,
    EvalDefinitionEvalDefinitionGlobalConfigOutputMatchListConfig,
]


class EvalDefinitionEvalDefinition(BaseModel):
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

    global_config: Optional[EvalDefinitionEvalDefinitionGlobalConfig] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class EvalDefinitionConfig(BaseModel):
    expected: Union[str, List[str]]


class EvalDefinition(BaseModel):
    eval_definition: EvalDefinitionEvalDefinition = FieldInfo(alias="evalDefinition")

    config: Optional[EvalDefinitionConfig] = None


class TaskSchedule(BaseModel):
    criticality: Literal["LOW", "MEDIUM", "HIGH"]

    cron: str

    task_id: str = FieldInfo(alias="taskId")

    last_run_at: Optional[datetime] = FieldInfo(alias="lastRunAt", default=None)

    next_run_at: Optional[datetime] = FieldInfo(alias="nextRunAt", default=None)


class Task(BaseModel):
    id: str
    """The unique identifier of the task"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the task was created"""

    description: str
    """The task description"""

    eval_definitions: List[EvalDefinition] = FieldInfo(alias="evalDefinitions")

    input_examples: List[str] = FieldInfo(alias="inputExamples")
    """Example inputs for the task"""

    metadata: Dict[str, object]
    """Optional metadata associated with the task.

    Returns null when no metadata is stored.
    """

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the task was last modified"""

    pass_rate: float = FieldInfo(alias="passRate")
    """The 30 day pass rate for the task measured in percentage"""

    title: str
    """The title of the task"""

    type: Literal["STATIC", "NORMAL"]
    """The type of task.

    Normal tasks have a dynamic user prompt, while adversarial tasks have a fixed
    user prompt.
    """

    last_test: Optional[datetime] = FieldInfo(alias="lastTest", default=None)
    """The date and time this task was last tested"""

    simulated_prompt_schema: Optional[Dict[str, object]] = FieldInfo(alias="simulatedPromptSchema", default=None)
    """
    JSON schema that defines the structure for user prompts that should be generated
    for tests
    """

    task_schedule: Optional[TaskSchedule] = FieldInfo(alias="taskSchedule", default=None)
    """Task schedule schema"""

    topic_id: Optional[str] = FieldInfo(alias="topicId", default=None)
    """The ID of the topic this task belongs to"""
