# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ValidateWebhookValidateParams", "Body", "BodyExperiment"]


class ValidateWebhookValidateParams(TypedDict, total=False):
    body: Required[Body]
    """Payload sent to the configured webhook whenever a task test is triggered."""

    signature: Required[str]
    """HMAC signature for the request body."""

    timestamp: Required[int]
    """Timestamp (in milliseconds) for the request."""


class BodyExperiment(TypedDict, total=False):
    experiment_id: Required[Annotated[str, PropertyInfo(alias="experimentId")]]
    """The unique identifier of the experiment"""

    experiment_variant_id: Required[Annotated[str, PropertyInfo(alias="experimentVariantId")]]
    """The unique identifier of the experiment variant"""

    overrides: Required[Dict[str, Dict[str, object]]]


class Body(TypedDict, total=False):
    prompt: Required[Union[str, Dict[str, object]]]
    """The user prompt that triggered the test run."""

    test_id: Required[Annotated[str, PropertyInfo(alias="testId")]]
    """The unique identifier for the test run."""

    experiment: BodyExperiment
    """Payload containing the experiment details."""

    metadata: Dict[str, object]
    """Metadata from the originating task. Only included when metadata is available."""
