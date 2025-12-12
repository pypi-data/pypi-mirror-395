"""Python client for the Guidelinely Environmental Guidelines API.

Provides programmatic access to environmental guideline calculations and searches
for chemical parameters in various media (water, soil, sediment).
"""

import logging
import os
from typing import Any, Optional, Union, cast

import httpx

from guidelinely.auth import get_api_key
from guidelinely.cache import get_cached, set_cached
from guidelinely.exceptions import (
    GuidelinelyAPIError,
    GuidelinelyConnectionError,
    GuidelinelyTimeoutError,
)
from guidelinely.models import (
    CalculationResponse,
    GuidelineSearchResult,
    SourceResponse,
    StatsResponse,
)

# Module logger for debugging API calls
logger = logging.getLogger("guidelinely")

# API base URL
GUIDELINELY_API_BASE = "https://guidelines.1681248.com/api/v1"

# Default timeout for HTTP requests (in seconds), configurable via environment variable
DEFAULT_TIMEOUT = float(os.getenv("GUIDELINELY_TIMEOUT", "30.0"))

# Package version for User-Agent header
try:
    from guidelinely import __version__
except ImportError:
    __version__ = "0.0.0"

# User-Agent header for API request identification
USER_AGENT = f"guidelinely-python/{__version__}"


def _handle_error(response: httpx.Response) -> None:
    """Extract error message from API response and raise appropriate exception.

    Args:
        response: HTTP response object with non-2xx status code.

    Raises:
        GuidelinelyAPIError: Always raised with extracted message and status code.
    """
    try:
        error_body = response.json()
        message = error_body.get("detail") or error_body.get("message") or "API request failed"
    except Exception:
        message = "API request failed"
    raise GuidelinelyAPIError(message, response.status_code)


def _sort_data_structure(obj: Any) -> str:
    """Recursively sort dictionaries and lists for consistent cache key generation.

    Args:
        obj: Input data structure (dict, list, or other).
    Returns:
        A string representation of the sorted data structure.
    """
    if isinstance(obj, dict):
        return str(sorted((k, _sort_data_structure(v)) for k, v in obj.items()))
    elif isinstance(obj, list):
        return str(sorted(_sort_data_structure(item) for item in obj))
    elif isinstance(obj, float):
        return f"{obj:f}"
    elif isinstance(obj, int):
        return str(obj)
    elif isinstance(obj, str):
        return str(obj)
    elif obj is None:
        return "None"
    else:
        raise TypeError(f"Unsupported data type for cache key: {type(obj)}")


def _get_cache_key(data: Any) -> str:
    """Generate a consistent cache key string from input data.

    Args:
        data: Input data structure (dict, list, or other).
    Returns:
        A string representation suitable for use as a cache key.
    """
    return _sort_data_structure(data)


def health_check() -> dict[str, Any]:
    """Check if the API service is running.

    Lightweight health check that returns 200 OK if the service is running.
    Does not check dependencies.

    Returns:
        Dictionary with health status.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        status = health_check()
        print(status)
    """
    logger.debug("Performing health check")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/health")
            logger.debug(f"Health check response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return cast(dict[str, Any], response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"Health check timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Health check connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def readiness_check() -> dict[str, Any]:
    """Check if the API is ready to handle requests.

    Readiness check that verifies the service can handle requests
    (database is accessible).

    Returns:
        Dictionary with readiness status.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        status = readiness_check()
        print(status)
    """
    logger.debug("Performing readiness check")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/ready")
            logger.debug(f"Readiness check response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return cast(dict[str, Any], response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"Readiness check timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Readiness check connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def list_parameters() -> list[str]:
    """List all available chemical parameters.

    Get complete list of all available chemical parameters in the database.

    Returns:
        List of parameter names.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        params = list_parameters()
        print(params[:5])  # ['Aluminum', 'Ammonia', 'Arsenic', 'Cadmium', 'Copper']
    """
    logger.debug("Listing all parameters")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/parameters")
            logger.debug(f"List parameters response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return cast(list[str], response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"List parameters timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"List parameters connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def search_parameters(
    q: str = "",
    media: Optional[list[str]] = None,
    source: Optional[list[str]] = None,
    document: Optional[list[str]] = None,
) -> list[str]:
    """Search for chemical parameters.

    Search for chemical parameters using case-insensitive substring matching.

    Args:
        q: Search query string. Empty string returns all parameters.
        media: Optional list of media types to filter by (e.g., ["surface_water", "soil"]).
        source: Optional list of source abbreviations to filter by (e.g., ["AEPA", "CCME"]).
        document: Optional list of document abbreviations to filter by (e.g., ["PAL", "MDMER"]).

    Returns:
        List of matching parameter names.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        # Find all ammonia-related parameters
        ammonia = search_parameters("ammon")
        print(ammonia)

        # Find copper in surface water
        copper_sw = search_parameters("copper", media=["surface_water"])

        # Find aluminum in groundwater from AEPA PAL document
        aluminum = search_parameters(
            "aluminum", media=["groundwater"], source=["AEPA"], document=["PAL"]
        )
    """
    logger.debug(
        f"Searching parameters with q={q!r}, media={media!r}, "
        f"source={source!r}, document={document!r}"
    )
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            params: dict[str, Any] = {"q": q}
            if media:
                params["media"] = media
            if source:
                params["source"] = source
            if document:
                params["document"] = document

            response = client.get(
                f"{GUIDELINELY_API_BASE}/parameters/search",
                params=params,
            )
            logger.debug(f"Search parameters response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return cast(list[str], response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"Search parameters timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Search parameters connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def list_media() -> dict[str, str]:
    """List all environmental media types.

    Get list of all available environmental media types (water, soil, sediment, etc.).

    Returns:
        Dictionary mapping enum names to display names.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        media = list_media()
        print(media)
    """
    logger.debug("Listing all media types")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/media")
            logger.debug(f"List media response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return cast(dict[str, str], response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"List media timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"List media connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def list_sources() -> list[SourceResponse]:
    """List all guideline sources and documents.

    Get list of all guideline sources and their associated documents.

    Returns:
        List of SourceResponse objects with nested document information.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        sources = list_sources()
        print(sources[0].name)  # e.g., 'CCME'
        print(sources[0].documents[0].name)
    """
    logger.debug("Listing all sources")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/sources")
            logger.debug(f"List sources response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return [SourceResponse(**source) for source in response.json()]
    except httpx.TimeoutException as e:
        logger.warning(f"List sources timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"List sources connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def get_stats() -> StatsResponse:
    """Get database statistics.

    Get statistics about the guideline database (counts of sources, documents, etc.).

    Returns:
        StatsResponse with parameters, guidelines, sources, documents counts.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        stats = get_stats()
        print(f"Total parameters: {stats.parameters}")
        print(f"Total guidelines: {stats.guidelines}")
    """
    logger.debug("Getting database statistics")
    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(f"{GUIDELINELY_API_BASE}/stats")
            logger.debug(f"Get stats response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return StatsResponse(**response.json())
    except httpx.TimeoutException as e:
        logger.warning(f"Get stats timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Get stats connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def calculate_guidelines(
    parameter: str,
    media: str,
    context: Optional[Union[dict[str, str], list[dict[str, str]]]] = None,
    target_unit: Optional[str] = None,
    include_formula_svg: bool = False,
    api_key: Optional[str] = None,
) -> CalculationResponse:
    """Calculate guidelines for a parameter.

    Calculate guideline values for a specific parameter in a given media type
    with environmental context.

    Args:
        parameter: Chemical parameter name (e.g., "Aluminum", "Copper").
        media: Media type (e.g., "surface_water", "soil", "sediment").
        context: Environmental parameters as strings with units. Can be a single dict
            or a list of dicts for multiple calculations with different contexts.
            For water: pH ("7.0 1"), hardness ("100 mg/L"), temperature ("20 °C"),
                      chloride ("50 mg/L")
            For soil: pH ("6.5 1"), organic_matter ("3.5 %"),
                     cation_exchange_capacity ("15 meq/100g")
        target_unit: Optional unit to convert result to (e.g., "mg/L", "μg/L").
        include_formula_svg: Whether to include SVG formula representations in the response.
            Default is False to reduce response size.
        api_key: Optional API key. If None, will use GUIDELINELY_API_KEY environment variable.

    Returns:
        CalculationResponse with results, context, contexts (if multiple), and total_count.
        When multiple contexts are provided, results include context_index indicating
        which context was used.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        ::

            import os
            os.environ["GUIDELINELY_API_KEY"] = "your_key"

            # Single context
            result = calculate_guidelines(
                parameter="Aluminum",
                media="surface_water",
                context={"pH": "7.0 1", "hardness": "100 mg/L"}
            )

            # Multiple contexts - compare across conditions
            result = calculate_guidelines(
                parameter="Aluminum",
                media="surface_water",
                context=[
                    {"pH": "7.0 1", "hardness": "100 mg/L"},
                    {"pH": "8.0 1", "hardness": "200 mg/L"}
                ]
            )

            print(f"Total: {result.total_count}")
            for guideline in result.results:
                print(f"{guideline.parameter}: {guideline.value} ({guideline.source})")
    """
    key = get_api_key(api_key)
    logger.debug(f"Calculating guidelines for {parameter} in {media}")

    # Prepare cache key (excludes api_key for security - keys should not be stored on disk)
    # Context is normalized (sorted) to ensure consistent cache hits regardless of key order
    cache_key_dict = {
        "endpoint": "calculate",
        "parameter": parameter,
        "media": media,
        "context": _get_cache_key(context),
        "target_unit": target_unit,
        "include_formula_svg": include_formula_svg,
    }
    # Normalize the entire cache key to ensure consistent serialization
    cache_key = _get_cache_key(cache_key_dict)

    # Check cache first
    cached_response = get_cached(cache_key)
    if cached_response:
        logger.debug("Returning cached response")
        return CalculationResponse(**cached_response)
    else:
        logger.warning(f"No cached response found for key {cache_key}")

    body: dict[str, Any] = {
        "parameter": parameter,
        "media": media,
    }

    if context:
        body["context"] = context
    if target_unit:
        body["target_unit"] = target_unit
    if include_formula_svg:
        body["include_formula_svg"] = include_formula_svg

    headers: dict[str, str] = {}
    if key:
        headers["X-API-KEY"] = key

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.post(
                f"{GUIDELINELY_API_BASE}/calculate",
                json=body,
                headers=headers if headers else None,
            )
            logger.debug(f"Calculate response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)

            data = response.json()
            # Cache the response
            set_cached(cache_key, data)
            return CalculationResponse(**data)
    except httpx.TimeoutException as e:
        logger.warning(f"Calculate guidelines timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Calculate guidelines connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def calculate_batch(
    parameters: list[Union[str, dict[str, Any]]],
    media: str,
    context: Optional[Union[dict[str, str], list[dict[str, str]]]] = None,
    include_formula_svg: bool = False,
    api_key: Optional[str] = None,
) -> CalculationResponse:
    """Batch calculate guidelines for multiple parameters.

    Calculate guideline values for multiple parameters in a given media type
    with shared environmental context. More efficient than multiple individual calls.

    Args:
        parameters: List of parameter names (strings), or list mixing strings and dicts
            with 'name' and 'target_unit' fields. Maximum 50 parameters.
        media: Media type (e.g., "surface_water", "soil").
        context: Environmental parameters as strings with units. Can be a single dict
            or a list of dicts for multiple calculations with different contexts.
        include_formula_svg: Whether to include SVG formula representations in the response.
            Default is False to reduce response size.
        api_key: Optional API key. If None, will use GUIDELINELY_API_KEY environment variable.

    Returns:
        CalculationResponse with results, context, contexts (if multiple), and total_count.
        When multiple contexts are provided, results include context_index indicating
        which context was used.

    Raises:
        ValueError: If more than 50 parameters provided.
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.

    Example:
        ::

            import os
            os.environ["GUIDELINELY_API_KEY"] = "your_key"

            # Calculate multiple metals in surface water
            results = calculate_batch(
                parameters=["Aluminum", "Copper", "Lead"],
                media="surface_water",
                context={"pH": "7.0 1", "hardness": "100 mg/L"}
            )

            # Multiple contexts - compare across conditions
            results = calculate_batch(
                parameters=["Aluminum", "Copper"],
                media="surface_water",
                context=[
                    {"pH": "7.0 1", "hardness": "100 mg/L"},
                    {"pH": "8.0 1", "hardness": "200 mg/L"}
                ]
            )

            # With per-parameter unit conversion
            results = calculate_batch(
                parameters=[
                    "Aluminum",
                    {"name": "Copper", "target_unit": "μg/L"},
                    {"name": "Lead", "target_unit": "mg/L"}
                ],
                media="surface_water",
                context={"pH": "7.5 1", "hardness": "150 mg/L", "temperature": "15 °C"}
            )
    """
    if len(parameters) > 50:
        raise ValueError("Maximum 50 parameters per batch request")

    key = get_api_key(api_key)
    logger.debug(f"Batch calculating {len(parameters)} parameters in {media}")

    # Prepare cache key (excludes api_key for security - keys should not be stored on disk)
    # Context and parameters are normalized (sorted) to ensure consistent cache hits
    # regardless of key order
    cache_key_dict = {
        "endpoint": "calculate/batch",
        "parameters": _get_cache_key(parameters),
        "media": media,
        "context": _get_cache_key(context),
        "include_formula_svg": include_formula_svg,
    }
    # Normalize the entire cache key to ensure consistent serialization
    cache_key = _get_cache_key(cache_key_dict)

    # Check cache first
    cached_response = get_cached(cache_key)
    if cached_response:
        logger.debug("Returning cached response")
        return CalculationResponse(**cached_response)

    body: dict[str, Any] = {
        "parameters": parameters,
        "media": media,
    }

    if context:
        body["context"] = context
    if include_formula_svg:
        body["include_formula_svg"] = include_formula_svg

    headers: dict[str, str] = {}
    if key:
        headers["X-API-KEY"] = key

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.post(
                f"{GUIDELINELY_API_BASE}/calculate/batch",
                json=body,
                headers=headers if headers else None,
            )
            logger.debug(f"Batch calculate response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)

            data = response.json()
            # Cache the response
            set_cached(cache_key, data)
            return CalculationResponse(**data)
    except httpx.TimeoutException as e:
        logger.warning(f"Batch calculate timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Batch calculate connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e


def search_guidelines(
    *,
    parameter: Optional[str] = None,
    parameter_specification: Optional[str] = None,
    receptor: Optional[str] = None,
    media: Optional[str] = None,
    purpose: Optional[str] = None,
    exposure_duration: Optional[str] = None,
    table: Optional[str] = None,
    application: Optional[str] = None,
    basis: Optional[str] = None,
    modifier: Optional[str] = None,
    sector: Optional[str] = None,
    grouping: Optional[str] = None,
    use_case: Optional[str] = None,
    sample_fraction: Optional[str] = None,
    method_speciation: Optional[str] = None,
    season: Optional[str] = None,
    location: Optional[str] = None,
    narrative: Optional[str] = None,
    comment: Optional[str] = None,
    source_name: Optional[str] = None,
    source_abbreviation: Optional[str] = None,
    document_name: Optional[str] = None,
    document_abbreviation: Optional[str] = None,
    limit: int = 100,
) -> list[GuidelineSearchResult]:
    """Search for guidelines using flexible field-based filtering.

    Search for guidelines across multiple fields using case-insensitive substring matching.
    All parameters are keyword-only to ensure clarity.

    Args:
        parameter: Filter by chemical parameter name (e.g., "aluminum").
        parameter_specification: Filter by full parameter specification.
        receptor: Filter by receptor type (e.g., "aquatic_life", "human_health").
        media: Filter by environmental media (e.g., "surface_water", "groundwater", "soil").
        purpose: Filter by guideline purpose (e.g., "protection", "remediation").
        exposure_duration: Filter by exposure duration (e.g., "acute", "chronic").
        table: Filter by table identifier from source document.
        application: Filter by application context.
        basis: Filter by basis or rationale.
        modifier: Filter by modifier text.
        sector: Filter by sector classification.
        grouping: Filter by parameter grouping.
        use_case: Filter by use case description.
        sample_fraction: Filter by sample fraction.
        method_speciation: Filter by method speciation.
        season: Filter by seasonal applicability (e.g., "winter", "summer").
        location: Filter by location applicability (e.g., "alberta").
        narrative: Filter by narrative guidance text.
        comment: Filter by additional comments.
        source_name: Filter by source organization name.
        source_abbreviation: Filter by source abbreviation (e.g., "AEPA", "CCME").
        document_name: Filter by document title.
        document_abbreviation: Filter by document abbreviation (e.g., "PAL", "MDMER").
        limit: Maximum number of results to return (1-500, default 100).

    Returns:
        List of GuidelineSearchResult objects matching the search criteria.

    Raises:
        GuidelinelyAPIError: If the API returns an error response.
        GuidelinelyTimeoutError: If the request times out.
        GuidelinelyConnectionError: If unable to connect to the API.

    Example:
        # Find all aluminum guidelines
        results = search_guidelines(parameter="aluminum")

        # Find surface water guidelines for aquatic life
        results = search_guidelines(media="surface_water", receptor="aquatic_life")

        # Find protection guidelines from AEPA
        results = search_guidelines(source_abbreviation="AEPA", purpose="protection")

        # Find guidelines applicable in winter
        results = search_guidelines(season="winter")
    """
    logger.debug("Searching guidelines with filters")

    # Build query parameters, excluding None values
    params: dict[str, Any] = {}
    if parameter is not None:
        params["parameter"] = parameter
    if parameter_specification is not None:
        params["parameter_specification"] = parameter_specification
    if receptor is not None:
        params["receptor"] = receptor
    if media is not None:
        params["media"] = media
    if purpose is not None:
        params["purpose"] = purpose
    if exposure_duration is not None:
        params["exposure_duration"] = exposure_duration
    if table is not None:
        params["table"] = table
    if application is not None:
        params["application"] = application
    if basis is not None:
        params["basis"] = basis
    if modifier is not None:
        params["modifier"] = modifier
    if sector is not None:
        params["sector"] = sector
    if grouping is not None:
        params["grouping"] = grouping
    if use_case is not None:
        params["use_case"] = use_case
    if sample_fraction is not None:
        params["sample_fraction"] = sample_fraction
    if method_speciation is not None:
        params["method_speciation"] = method_speciation
    if season is not None:
        params["season"] = season
    if location is not None:
        params["location"] = location
    if narrative is not None:
        params["narrative"] = narrative
    if comment is not None:
        params["comment"] = comment
    if source_name is not None:
        params["source_name"] = source_name
    if source_abbreviation is not None:
        params["source_abbreviation"] = source_abbreviation
    if document_name is not None:
        params["document_name"] = document_name
    if document_abbreviation is not None:
        params["document_abbreviation"] = document_abbreviation
    params["limit"] = limit

    logger.debug(f"Search guidelines params: {params}")

    try:
        with httpx.Client(timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(
                f"{GUIDELINELY_API_BASE}/guidelines/search",
                params=params,
            )
            logger.debug(f"Search guidelines response: {response.status_code}")
            if response.status_code != 200:
                _handle_error(response)
            return [GuidelineSearchResult(**item) for item in response.json()]
    except httpx.TimeoutException as e:
        logger.warning(f"Search guidelines timed out: {e}")
        raise GuidelinelyTimeoutError(f"Request timed out: {e}") from e
    except httpx.TransportError as e:
        logger.warning(f"Search guidelines connection failed: {e}")
        raise GuidelinelyConnectionError(f"Connection failed: {e}") from e
