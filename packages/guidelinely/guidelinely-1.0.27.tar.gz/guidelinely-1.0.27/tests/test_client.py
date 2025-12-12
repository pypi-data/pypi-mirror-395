"""Tests for API client functions."""

import pytest

from guidelinely import (
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
from guidelinely.cache import cache
from guidelinely.exceptions import GuidelinelyAPIError

API_BASE = "https://guidelines.1681248.com/api/v1"


def test_health_check(httpx_mock):
    """Test health check endpoint."""
    httpx_mock.add_response(
        method="GET", url=f"{API_BASE}/health", json={"status": "healthy"}, status_code=200
    )

    result = health_check()
    assert result["status"] == "healthy"


def test_readiness_check(httpx_mock):
    """Test readiness check endpoint."""
    httpx_mock.add_response(
        method="GET", url=f"{API_BASE}/ready", json={"status": "ready"}, status_code=200
    )

    result = readiness_check()
    assert result["status"] == "ready"


def test_list_parameters(httpx_mock):
    """Test listing all parameters."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters",
        json=["Aluminum", "Copper", "Lead", "Zinc"],
        status_code=200,
    )

    params = list_parameters()
    assert len(params) == 4
    assert "Aluminum" in params
    assert "Copper" in params


def test_search_parameters(httpx_mock):
    """Test parameter search."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters/search?q=ammon",
        json=["Ammonia", "Ammonium"],
        status_code=200,
    )

    results = search_parameters("ammon")
    assert len(results) == 2
    assert "Ammonia" in results


def test_search_parameters_with_media_filter(httpx_mock):
    """Test parameter search with media filter."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters/search?q=copper&media=surface_water",
        json=["Copper"],
        status_code=200,
    )

    results = search_parameters("copper", media=["surface_water"])
    assert len(results) == 1
    assert "Copper" in results


def test_search_parameters_with_source_filter(httpx_mock):
    """Test parameter search with source filter."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters/search?q=aluminum&source=AEPA",
        json=["Aluminum"],
        status_code=200,
    )

    results = search_parameters("aluminum", source=["AEPA"])
    assert len(results) == 1
    assert "Aluminum" in results


def test_search_parameters_with_document_filter(httpx_mock):
    """Test parameter search with document filter."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters/search?q=zinc&document=PAL",
        json=["Zinc"],
        status_code=200,
    )

    results = search_parameters("zinc", document=["PAL"])
    assert len(results) == 1
    assert "Zinc" in results


def test_search_parameters_with_all_filters(httpx_mock):
    """Test parameter search with media, source, and document filters combined."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/parameters/search?q=aluminum&media=groundwater&source=AEPA&document=PAL",
        json=["Aluminum"],
        status_code=200,
    )

    results = search_parameters(
        "aluminum", media=["groundwater"], source=["AEPA"], document=["PAL"]
    )
    assert len(results) == 1
    assert "Aluminum" in results


def test_list_media(httpx_mock):
    """Test listing media types."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/media",
        json={"surface_water": "Surface Water", "groundwater": "Groundwater", "soil": "Soil"},
        status_code=200,
    )

    media = list_media()
    assert "surface_water" in media
    assert media["surface_water"] == "Surface Water"


def test_list_sources(httpx_mock):
    """Test listing guideline sources."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/sources",
        json=[
            {
                "id": 1,
                "name": "CCME",
                "abbreviation": "CCME",
                "documents": [
                    {"id": 1, "name": "Canadian Water Quality Guidelines", "abbreviation": "CWQG"}
                ],
            }
        ],
        status_code=200,
    )

    sources = list_sources()
    assert len(sources) == 1
    assert sources[0].name == "CCME"
    assert sources[0].abbreviation == "CCME"
    assert len(sources[0].documents) == 1
    assert sources[0].documents[0].name == "Canadian Water Quality Guidelines"


def test_get_stats(httpx_mock):
    """Test getting database statistics."""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_BASE}/stats",
        json={
            "parameters": 50,
            "guidelines": 1000,
            "sources": 10,
            "documents": 25,
        },
        status_code=200,
    )

    stats = get_stats()
    assert stats.parameters == 50
    assert stats.guidelines == 1000
    assert stats.sources == 10
    assert stats.documents == 25


def test_calculate_guidelines(httpx_mock):
    """Test calculating guidelines for a single parameter."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate",
        json={
            "results": [
                {
                    "id": 1,
                    "parameter": "Aluminum",
                    "parameter_specification": "Aluminum, Dissolved",
                    "media": "surface_water",
                    "value": "[87.0 μg/L,100 μg/L]",
                    "lower": 87.0,
                    "upper": 100.0,
                    "unit": "μg/L",
                    "is_calculated": True,
                    "source": "CCME",
                    "receptor": "Aquatic Life",
                    "exposure_duration": "chronic",
                    "purpose": "long_term",
                    "table": "Table 1",
                    "application": "Freshwater guidelines",
                    "basis": "Chronic toxicity",
                    "use_case": "Protection",
                    "document": "CCME Water Quality Guidelines",
                }
            ],
            "context": {"pH": "7.0 1", "hardness": "100 mg/L"},
            "total_count": 1,
        },
        status_code=200,
    )

    result = calculate_guidelines(
        parameter="Aluminum",
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
        api_key="dummy",
    )

    assert result.total_count == 1
    assert len(result.results) == 1
    assert result.results[0].parameter_specification == "Aluminum, Dissolved"
    assert result.results[0].is_calculated is True
    assert result.context["pH"] == "7.0 1"
    # Verify use_case is present and correctly parsed
    assert result.results[0].use_case == "Protection"


def test_calculate_guidelines_with_api_key(httpx_mock):
    """Test calculating guidelines with API key."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate",
        json={"results": [], "context": {}, "total_count": 0},
        status_code=200,
    )

    calculate_guidelines(parameter="Aluminum", media="surface_water", api_key="test_key")

    # Verify API key was sent in headers
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers.get("X-API-KEY") == "test_key"


def test_calculate_batch(httpx_mock):
    """Test batch calculation."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate/batch",
        json={
            "results": [
                {
                    "id": 1,
                    "parameter": "Aluminum",
                    "parameter_specification": "Aluminum, Dissolved",
                    "media": "surface_water",
                    "value": "[87.0 μg/L,100 μg/L]",
                    "lower": 87.0,
                    "upper": 100.0,
                    "unit": "μg/L",
                    "is_calculated": True,
                    "source": "CCME",
                    "receptor": "Aquatic Life",
                    "exposure_duration": "chronic",
                    "purpose": "long_term",
                    "table": "Table 1",
                    "application": "Freshwater guidelines",
                    "basis": "Chronic toxicity",
                    "use_case": "Protection",
                    "document": "CCME Water Quality Guidelines",
                },
                {
                    "id": 2,
                    "parameter": "Copper",
                    "parameter_specification": "Copper, Dissolved",
                    "media": "surface_water",
                    "value": "[2.0 μg/L,5.0 μg/L]",
                    "lower": 2.0,
                    "upper": 5.0,
                    "unit": "μg/L",
                    "is_calculated": True,
                    "source": "CCME",
                    "receptor": "Aquatic Life",
                    "exposure_duration": "chronic",
                    "purpose": "long_term",
                    "table": "Table 1",
                    "application": "Freshwater guidelines",
                    "basis": "Chronic toxicity",
                    "use_case": "Protection",
                    "document": "CCME Water Quality Guidelines",
                },
            ],
            "context": {"pH": "7.0 1", "hardness": "100 mg/L"},
            "total_count": 2,
        },
        status_code=200,
    )

    result = calculate_batch(
        parameters=["Aluminum", "Copper"],
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
        api_key="dummy",
    )

    assert result.total_count == 2
    assert len(result.results) == 2
    # Verify use_case is present in batch results
    assert result.results[0].use_case == "Protection"
    assert result.results[1].use_case == "Protection"


def test_calculate_batch_with_unit_conversion(httpx_mock):
    """Test batch calculation with per-parameter unit conversion."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate/batch",
        json={"results": [], "context": {}, "total_count": 0},
        status_code=200,
    )

    calculate_batch(
        parameters=[
            "Aluminum",
            {"name": "Copper", "target_unit": "μg/L"},
            {"name": "Lead", "target_unit": "mg/L"},
        ],
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
        api_key="dummy",
    )

    # Verify request was sent correctly
    requests = httpx_mock.get_requests()
    assert len(requests) == 1


def test_calculate_batch_parameter_limit():
    """Test that batch calculation enforces 50 parameter limit."""
    params = ["Aluminum"] * 51

    with pytest.raises(ValueError, match="Maximum 50 parameters"):
        calculate_batch(params, "surface_water")


def test_use_case_present_in_responses(httpx_mock):
    """Test that use_case field is present and correctly parsed in API responses."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate",
        json={
            "results": [
                {
                    "id": 1,
                    "parameter": "Aluminum",
                    "parameter_specification": "Aluminum, Dissolved",
                    "media": "surface_water",
                    "value": "[87.0 μg/L,100 μg/L]",
                    "lower": 87.0,
                    "upper": 100.0,
                    "unit": "μg/L",
                    "is_calculated": True,
                    "source": "CCME",
                    "receptor": "Aquatic Life",
                    "exposure_duration": "chronic",
                    "purpose": "long_term",
                    "table": "Table 1",
                    "application": "Freshwater guidelines",
                    "basis": "Chronic toxicity",
                    "use_case": "Protection",
                    "document": "CCME Water Quality Guidelines",
                }
            ],
            "context": {"pH": "7.0 1", "hardness": "100 mg/L"},
            "total_count": 1,
        },
        status_code=200,
    )

    result = calculate_guidelines(
        parameter="Aluminum",
        media="surface_water",
        context={"pH": "7.0 1", "hardness": "100 mg/L"},
        api_key="dummy",
    )

    # Verify use_case is present and has expected value
    assert hasattr(result.results[0], "use_case")
    assert result.results[0].use_case == "Protection"
    assert result.results[0].use_case is not None


def test_error_handling(httpx_mock):
    """Test error handling for API failures."""
    cache.clear()  # Clear cache to ensure HTTP call is made
    httpx_mock.add_response(
        method="POST",
        url=f"{API_BASE}/calculate",
        json={"detail": "Database connection failed"},
        status_code=500,
    )

    with pytest.raises(GuidelinelyAPIError) as exc_info:
        calculate_guidelines(
            parameter="Aluminum",
            media="surface_water",
            api_key="dummy",
        )

    assert exc_info.value.status_code == 500
    assert "Database connection failed" in str(exc_info.value)
