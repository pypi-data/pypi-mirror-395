# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .annotation import Annotation

__all__ = ["AnnotationResponse"]


class AnnotationResponse(BaseModel):
    data: Annotation
    """A single annotation indicating a change in the AI application configuration"""
