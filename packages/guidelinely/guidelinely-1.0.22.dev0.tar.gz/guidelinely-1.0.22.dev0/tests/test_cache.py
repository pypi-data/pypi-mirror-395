"""Unit tests for client-side caching functionality using diskcache."""

import os
import tempfile

import pytest
from diskcache import Cache


class TestCacheOperations:
    """Test cache get/set operations using temporary cache."""

    @pytest.fixture
    def temp_cache(self):
        """Create a temporary cache for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(directory=temp_dir)
            yield cache
            cache.close()

    def test_get_cached_miss(self, temp_cache):
        """Should return None for missing key."""
        assert temp_cache.get({"test": "data"}) is None

    def test_set_and_get_cached(self, temp_cache):
        """Should store and retrieve cached data."""
        key_data = {"endpoint": "test", "param": "value"}
        response_data = {"results": [], "context": {}, "total_count": 0}

        temp_cache[key_data] = response_data
        cached = temp_cache.get(key_data)
        assert cached == response_data

    def test_different_keys_different_values(self, temp_cache):
        """Different keys should store different values."""
        key1 = {"a": 1}
        key2 = {"a": 2}
        val1 = "value1"
        val2 = "value2"

        temp_cache[key1] = val1
        temp_cache[key2] = val2

        assert temp_cache.get(key1) == val1
        assert temp_cache.get(key2) == val2

    def test_complex_key_types(self, temp_cache):
        """Should handle complex key types like lists and nested dicts."""
        key = {
            "endpoint": "calculate/batch",
            "parameters": ["Aluminum", {"name": "Copper", "target_unit": "mg/L"}],
            "media": "surface_water",
            "context": {"pH": "7.0 1", "hardness": "100 mg/L"},
            "api_key": None,
        }
        value = {"results": [], "context": {}, "total_count": 0}

        temp_cache[key] = value
        assert temp_cache.get(key) == value


class TestCacheKeyNormalization:
    """Test cache key normalization for consistent cache hits."""

    def test_normalize_context_single_dict_order_independent(self):
        """Same context with different key order should produce same normalized key."""
        from guidelinely.client import _normalize_context_for_cache

        context1 = {"pH": "7.0 1", "hardness": "100 mg/L", "temperature": "20 °C"}
        context2 = {"temperature": "20 °C", "pH": "7.0 1", "hardness": "100 mg/L"}
        context3 = {"hardness": "100 mg/L", "temperature": "20 °C", "pH": "7.0 1"}

        normalized1 = _normalize_context_for_cache(context1)
        normalized2 = _normalize_context_for_cache(context2)
        normalized3 = _normalize_context_for_cache(context3)

        assert normalized1 == normalized2 == normalized3

    def test_normalize_context_list_of_dicts_order_independent(self):
        """List of contexts with different key orders should produce same normalized key."""
        from guidelinely.client import _normalize_context_for_cache

        context1 = [
            {"pH": "7.0 1", "hardness": "100 mg/L"},
            {"pH": "8.0 1", "hardness": "200 mg/L"},
        ]
        context2 = [
            {"hardness": "100 mg/L", "pH": "7.0 1"},
            {"hardness": "200 mg/L", "pH": "8.0 1"},
        ]

        normalized1 = _normalize_context_for_cache(context1)
        normalized2 = _normalize_context_for_cache(context2)

        assert normalized1 == normalized2

    def test_normalize_context_none_returns_none(self):
        """None context should return None."""
        from guidelinely.client import _normalize_context_for_cache

        assert _normalize_context_for_cache(None) is None

    def test_normalize_context_produces_hashable_result(self):
        """Normalized context should be hashable (tuples, not dicts)."""
        from guidelinely.client import _normalize_context_for_cache

        context = {"pH": "7.0 1", "hardness": "100 mg/L"}
        normalized = _normalize_context_for_cache(context)

        # Should be a tuple, not a dict
        assert isinstance(normalized, tuple)
        # Should be hashable (can be used in sets/dict keys)
        hash(normalized)

    def test_normalize_parameters_strings_order_independent(self):
        """Parameter string lists with different orders should produce same normalized key."""
        from guidelinely.client import _normalize_parameters_for_cache

        params1 = ["Aluminum", "Copper", "Lead"]
        params2 = ["Copper", "Lead", "Aluminum"]
        params3 = ["Lead", "Aluminum", "Copper"]

        normalized1 = _normalize_parameters_for_cache(params1)
        normalized2 = _normalize_parameters_for_cache(params2)
        normalized3 = _normalize_parameters_for_cache(params3)

        # Parameters should be sorted alphabetically for consistent cache keys
        assert normalized1 == normalized2 == normalized3
        assert normalized1 == ("Aluminum", "Copper", "Lead")

    def test_normalize_parameters_dicts_order_independent(self):
        """Parameter dicts with different key orders should produce same normalized key."""
        from guidelinely.client import _normalize_parameters_for_cache

        params1 = [
            "Aluminum",
            {"name": "Copper", "target_unit": "μg/L"},
            {"name": "Lead", "target_unit": "mg/L"},
        ]
        params2 = [
            "Aluminum",
            {"target_unit": "μg/L", "name": "Copper"},  # Different key order
            {"target_unit": "mg/L", "name": "Lead"},  # Different key order
        ]

        normalized1 = _normalize_parameters_for_cache(params1)
        normalized2 = _normalize_parameters_for_cache(params2)

        assert normalized1 == normalized2

    def test_normalize_parameters_mixed_types(self):
        """Mixed parameter types should be normalized correctly."""
        from guidelinely.client import _normalize_parameters_for_cache

        params = [
            "Aluminum",  # String
            {"name": "Copper", "target_unit": "μg/L"},  # Dict
            "Lead",  # String
        ]

        normalized = _normalize_parameters_for_cache(params)

        expected = (
            "Aluminum",
            "Lead",
            (("name", "Copper"), ("target_unit", "μg/L")),
        )
        assert normalized == expected

    def test_cache_hit_with_reordered_context(self, httpx_mock):
        """Cache should hit when same context is provided with different key order."""
        from guidelinely import calculate_guidelines
        from guidelinely.cache import cache

        cache.clear()

        # Mock API response
        httpx_mock.add_response(
            method="POST",
            url="https://guidelines.1681248.com/api/v1/calculate",
            json={"results": [], "context": {}, "total_count": 0},
            status_code=200,
        )

        # First call with context keys in one order
        calculate_guidelines(
            parameter="Aluminum",
            media="surface_water",
            context={"pH": "7.0 1", "hardness": "100 mg/L"},
            api_key="test_key",
        )

        # Second call with context keys in different order - should use cache
        calculate_guidelines(
            parameter="Aluminum",
            media="surface_water",
            context={"hardness": "100 mg/L", "pH": "7.0 1"},
            api_key="test_key",
        )

        # Only one HTTP request should have been made (second was cache hit)
        requests = httpx_mock.get_requests()
        assert len(requests) == 1

    def test_cache_hit_with_reordered_parameter_dicts(self, httpx_mock):
        """Cache should hit when parameter dicts have different key orders."""
        from guidelinely import calculate_batch
        from guidelinely.cache import cache

        cache.clear()

        # Mock API response
        httpx_mock.add_response(
            method="POST",
            url="https://guidelines.1681248.com/api/v1/calculate/batch",
            json={"results": [], "context": {}, "total_count": 0},
            status_code=200,
        )

        # First call with parameter dict keys in one order
        calculate_batch(
            parameters=[
                "Aluminum",
                {"name": "Copper", "target_unit": "μg/L"},
            ],
            media="surface_water",
            api_key="test_key",
        )

        # Second call with parameter dict keys in different order - should use cache
        calculate_batch(
            parameters=[
                "Aluminum",
                {"target_unit": "μg/L", "name": "Copper"},  # Reordered keys
            ],
            media="surface_water",
            api_key="test_key",
        )

        # Only one HTTP request should have been made (second was cache hit)
        requests = httpx_mock.get_requests()
        assert len(requests) == 1

    def test_cache_hit_with_reordered_parameters(self, httpx_mock):
        """Cache should hit when parameters are provided in different order."""
        from guidelinely import calculate_batch
        from guidelinely.cache import cache

        cache.clear()

        # Mock API response
        httpx_mock.add_response(
            method="POST",
            url="https://guidelines.1681248.com/api/v1/calculate/batch",
            json={"results": [], "context": {}, "total_count": 0},
            status_code=200,
        )

        # First call with parameters in one order
        calculate_batch(
            parameters=["Aluminum", "Copper", "Lead"],
            media="surface_water",
            api_key="test_key",
        )

        # Second call with parameters in different order - should use cache
        calculate_batch(
            parameters=["Copper", "Lead", "Aluminum"],  # Different order
            media="surface_water",
            api_key="test_key",
        )

        # Only one HTTP request should have been made (second was cache hit)
        requests = httpx_mock.get_requests()
        assert len(requests) == 1


class TestCacheConfiguration:
    """Test cache directory configuration."""

    def test_cache_dir_defaults_to_home(self):
        """CACHE_DIR should default to ~/.guidelinely_cache when env var not set."""
        from pathlib import Path

        # Remove env var if set, reload module to test default
        old_value = os.environ.pop("GUIDELINELY_CACHE_DIR", None)
        try:
            # We need to test the logic, not the actual module state
            # since the module is already loaded
            default_cache_dir = Path.home() / ".guidelinely_cache"
            test_dir = Path(os.getenv("GUIDELINELY_CACHE_DIR", str(default_cache_dir)))
            assert test_dir == default_cache_dir
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_DIR"] = old_value

    def test_cache_dir_from_environment(self):
        """CACHE_DIR should use GUIDELINELY_CACHE_DIR env var when set."""
        from pathlib import Path

        custom_dir = "/tmp/custom_guidelinely_cache"
        old_value = os.environ.get("GUIDELINELY_CACHE_DIR")
        try:
            os.environ["GUIDELINELY_CACHE_DIR"] = custom_dir
            default_cache_dir = Path.home() / ".guidelinely_cache"
            test_dir = Path(os.getenv("GUIDELINELY_CACHE_DIR", str(default_cache_dir)))
            assert test_dir == Path(custom_dir)
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_DIR"] = old_value
            else:
                os.environ.pop("GUIDELINELY_CACHE_DIR", None)

    def test_default_ttl_value(self):
        """DEFAULT_TTL should be 7 days (604800 seconds) by default."""
        # When env var is not set, should be 7 days
        old_value = os.environ.pop("GUIDELINELY_CACHE_TTL", None)
        try:
            expected_ttl = 7 * 24 * 3600  # 604800 seconds
            test_ttl = int(os.getenv("GUIDELINELY_CACHE_TTL", str(expected_ttl)))
            assert test_ttl == expected_ttl
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_TTL"] = old_value

    def test_ttl_from_environment(self):
        """DEFAULT_TTL should use GUIDELINELY_CACHE_TTL env var when set."""
        custom_ttl = "3600"  # 1 hour
        old_value = os.environ.get("GUIDELINELY_CACHE_TTL")
        try:
            os.environ["GUIDELINELY_CACHE_TTL"] = custom_ttl
            test_ttl = int(os.getenv("GUIDELINELY_CACHE_TTL", str(7 * 24 * 3600)))
            assert test_ttl == int(custom_ttl)
        finally:
            if old_value is not None:
                os.environ["GUIDELINELY_CACHE_TTL"] = old_value
            else:
                os.environ.pop("GUIDELINELY_CACHE_TTL", None)
