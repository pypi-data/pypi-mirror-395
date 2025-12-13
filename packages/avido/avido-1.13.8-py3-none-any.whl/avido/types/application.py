# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Application"]


class Application(BaseModel):
    id: str
    """Unique identifier of the application"""

    context: str
    """Context/instructions for the application"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the application was created"""

    description: str
    """Description of the application"""

    environment: Literal["DEV", "PROD"]
    """Environment of the application. Defaults to DEV."""

    language: str
    """Language of the application"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the application was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this application"""

    slug: str
    """URL-friendly slug for the application"""

    title: str
    """Title of the application"""

    type: Literal["CHATBOT", "AGENT"]
    """Type of the application. Valid values are CHATBOT or AGENT."""
