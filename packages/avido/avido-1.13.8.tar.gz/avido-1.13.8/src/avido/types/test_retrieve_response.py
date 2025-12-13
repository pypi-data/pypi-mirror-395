# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .test import Test
from .._models import BaseModel

__all__ = ["TestRetrieveResponse"]


class TestRetrieveResponse(BaseModel):
    __test__ = False
    test: Test
    """A Test represents a single test applying all the linked evals on a Trace"""
