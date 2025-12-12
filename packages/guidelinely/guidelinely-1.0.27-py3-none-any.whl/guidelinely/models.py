"""Pydantic models for Guidelinely API requests and responses."""

from typing import Any, Optional, Union

from pydantic import BaseModel, model_validator

__all__ = [
    # Response models
    "GuidelineResponse",
    "CalculationResponse",
    "SourceResponse",
    "SourceDocument",
    "StatsResponse",
    "MediaResponse",
    "GuidelineSearchResult",
    # Request models
    "CalculateRequest",
    "BatchCalculateRequest",
    "ParameterWithUnit",
    "SearchParametersRequest",
]


class GuidelineSearchResult(BaseModel):
    """Result from guideline search endpoint.

    Contains guideline metadata without calculated values.
    """

    parameter: str
    parameter_specification: Optional[str] = None
    receptor: Optional[str] = None
    media: Optional[str] = None
    purpose: Optional[str] = None
    exposure_duration: Optional[str] = None
    table: Optional[str] = None
    application: Optional[str] = None
    basis: Optional[str] = None
    modifier: Optional[str] = None
    sector: Optional[str] = None
    grouping: Optional[str] = None
    use_case: Optional[str] = None
    sample_fraction: Optional[str] = None
    method_speciation: Optional[str] = None
    season: Optional[str] = None
    location: Optional[str] = None
    narrative: Optional[str] = None
    comment: Optional[str] = None
    source_name: Optional[str] = None
    source_abbreviation: Optional[str] = None
    document_name: Optional[str] = None
    document_abbreviation: Optional[str] = None
    document_url: Optional[str] = None


class GuidelineResponse(GuidelineSearchResult):
    """Single guideline result with calculated or static value.

    Represents a guideline value in PostgreSQL unitrange format (e.g., '[10 μg/L,100 μg/L]').
    """

    value: str  # PostgreSQL unitrange format: '[10 μg/L,100 μg/L]', '(,87.0 μg/L]', '[5.0 mg/L,)'
    lower: Optional[float] = None  # Parsed lower bound or None if unbounded
    upper: Optional[float] = None  # Parsed upper bound or None if unbounded
    unit: str
    is_calculated: bool
    calculation_used: Optional[str] = None
    formula_svg: Optional[str] = None
    use_case: Optional[str] = None
    error: Optional[str] = None  # Error message if resolution failed
    error_type: Optional[str] = None  # Error type: validation, lookup, or unexpected
    context_index: Optional[int] = None  # Index of context used when multiple contexts provided


class CalculationResponse(BaseModel):
    """Response from calculation endpoints (/calculate and /calculate/batch)."""

    results: list[GuidelineResponse]
    context: dict[str, Any]  # Environmental context used for calculation
    contexts: Optional[list[dict[str, Any]]] = None  # List of contexts when multiple provided
    total_count: int


class CalculateRequest(BaseModel):
    """Request body for single parameter calculation."""

    parameter: str
    media: str
    # Single context dict or list of dicts for multiple contexts
    context: Optional[Union[dict[str, str], list[dict[str, str]]]] = None
    target_unit: Optional[str] = None  # Optional unit conversion
    include_formula_svg: bool = False  # Whether to include SVG formula representations


class ParameterWithUnit(BaseModel):
    """Parameter specification with optional target unit for batch requests."""

    name: str
    target_unit: Optional[str] = None


class BatchCalculateRequest(BaseModel):
    """Request body for batch parameter calculation."""

    parameters: list[Union[str, ParameterWithUnit]]  # Mix of strings and objects
    media: str
    # Single context dict or list of dicts for multiple contexts
    context: Optional[Union[dict[str, str], list[dict[str, str]]]] = None
    include_formula_svg: bool = False  # Whether to include SVG formula representations

    @model_validator(mode="after")
    def validate_parameter_count(self) -> "BatchCalculateRequest":
        """Ensure batch doesn't exceed 50 parameters.

        This validation runs automatically when the model is instantiated,
        raising ValueError if more than 50 parameters are provided.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If parameters list contains more than 50 items.
        """
        if len(self.parameters) > 50:
            raise ValueError("Maximum 50 parameters per batch request")
        return self


class SearchParametersRequest(BaseModel):
    """Request body for parameter search with optional filters."""

    media: Optional[list[str]] = None
    source: Optional[list[str]] = None  # Filter by source abbreviation (e.g., AEPA, CCME)
    document: Optional[list[str]] = None  # Filter by document abbreviation (e.g., PAL, MDMER)


class MediaResponse(BaseModel):
    """Response from /media endpoint mapping enum names to display names."""

    # Dynamic keys, so use dict directly in practice
    pass


class SourceDocument(BaseModel):
    """Nested document information within a source."""

    id: int
    name: str
    url: Optional[str] = None
    abbreviation: Optional[str] = None


class SourceResponse(BaseModel):
    """Guideline source with nested documents."""

    id: int
    name: str
    abbreviation: str
    documents: list[SourceDocument]


class StatsResponse(BaseModel):
    """Database statistics response."""

    parameters: int
    guidelines: int
    sources: int
    documents: int
