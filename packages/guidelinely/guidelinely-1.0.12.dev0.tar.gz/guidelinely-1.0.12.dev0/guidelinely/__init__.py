"""Guidelinely - Python client for the Guidelinely Environmental Guidelines API.

Provides programmatic access to environmental guideline calculations and searches
for chemical parameters in various media (water, soil, sediment).
"""

from guidelinely.auth import get_api_key
from guidelinely.client import (
    calculate_batch,
    calculate_guidelines,
    get_stats,
    health_check,
    list_media,
    list_parameters,
    list_sources,
    readiness_check,
    search_parameters,
)
from guidelinely.exceptions import (
    GuidelinelyAPIError,
    GuidelinelyConnectionError,
    GuidelinelyError,
    GuidelinelyTimeoutError,
)
from guidelinely.models import (
    CalculationResponse,
    GuidelineResponse,
    SourceDocument,
    SourceResponse,
    StatsResponse,
)

try:
    from guidelinely._version import __version__
except ImportError:
    __version__ = "0.0.0"  # Fallback for editable installs without build

__all__ = [
    # Client functions
    "health_check",
    "readiness_check",
    "list_parameters",
    "search_parameters",
    "list_media",
    "list_sources",
    "get_stats",
    "calculate_guidelines",
    "calculate_batch",
    # Models
    "GuidelineResponse",
    "CalculationResponse",
    "SourceResponse",
    "SourceDocument",
    "StatsResponse",
    # Exceptions
    "GuidelinelyError",
    "GuidelinelyAPIError",
    "GuidelinelyConnectionError",
    "GuidelinelyTimeoutError",
    # Auth
    "get_api_key",
]
