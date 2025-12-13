# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["IngestCreateResponse", "Data"]


class Data(BaseModel):
    success: bool
    """Whether the event(s) were successfully ingested."""

    id: Optional[str] = None
    """Thread ID if the event was a trace. Not returned for steps."""

    error: Optional[str] = None
    """Error message if ingestion failed."""


class IngestCreateResponse(BaseModel):
    data: List[Data]
    """Array of results for each ingested event."""
