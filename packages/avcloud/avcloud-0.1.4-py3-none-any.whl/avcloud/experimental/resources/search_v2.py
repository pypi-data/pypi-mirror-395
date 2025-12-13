"""
Search V2 - Proto-based Search API Support

This module provides search query capabilities with proto-based format including:
- Query types: term, terms, range, exists
- Boolean logic: must, should, must_not
- Sorting and pagination (limit, offset, search_after)
- Comprehensive input validation with clear error messages
- Automatic timestamp conversion to "timestamp 'YYYY-MM-DD HH:MM:SS'" format
- Type-safe query builders that generate proto-compatible JSON

All query builders validate their inputs and raise SearchV2ValidationError
for invalid parameters, catching errors early before API calls.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from avcloud.experimental.resources.entity import SummaryItem

# Re-export for convenience
__all__ = [
    "SearchV2ValidationError",
    "TermQuery",
    "TermsQuery",
    "RangeQuery",
    "ExistsQuery",
    "BoolQuery",
    "Sort",
    "SearchRequest",
    "SearchResponse",
    "SummaryItem",  # Re-exported from entity
]


class SearchV2ValidationError(ValueError):
    """Raised when search parameters are invalid."""

    pass


# Query Builder Classes
@dataclass
class TermQuery:
    """Match documents that contain an exact term in a field.

    Example:
        TermQuery(field="status", value="active")
    """

    field: str
    value: str | int | float | bool

    def __post_init__(self):
        """Validate the query parameters."""
        if not self.field or not isinstance(self.field, str):
            raise SearchV2ValidationError(
                f"TermQuery 'field' must be a non-empty string, got: {self.field!r}"
            )
        if self.value is None:
            raise SearchV2ValidationError(
                f"TermQuery 'value' cannot be None for field '{self.field}'"
            )

    def to_dict(self) -> dict:
        return {"term": {"field": self.field, "value": _wrap_value_with_type(self.value)}}


@dataclass
class TermsQuery:
    """Match documents that contain any of the exact terms in a field.

    Example:
        TermsQuery(field="status", values=["active", "pending"])
    """

    field: str
    values: list[str | int | float | bool]

    def __post_init__(self):
        """Validate the query parameters."""
        if not self.field or not isinstance(self.field, str):
            raise SearchV2ValidationError(
                f"TermsQuery 'field' must be a non-empty string, got: {self.field!r}"
            )
        if not isinstance(self.values, list):
            raise SearchV2ValidationError(
                f"TermsQuery 'values' must be a list for field '{self.field}', got: {type(self.values).__name__}"
            )
        if not self.values:
            raise SearchV2ValidationError(
                f"TermsQuery 'values' cannot be empty for field '{self.field}'. Use at least one value."
            )

    def to_dict(self) -> dict:
        # Wrap each value with its type
        wrapped_values = [_wrap_value_with_type(v) for v in self.values]

        return {
            "terms": {
                "terms": {self.field: {"field_value_array": {"field_value_array": wrapped_values}}}
            }
        }


@dataclass
class RangeQuery:
    """Match documents where field values fall within a range.

    Timestamp fields are automatically converted to "timestamp 'YYYY-MM-DD HH:MM:SS'" format.
    Supported timestamp formats:
    - ISO 8601: "2024-01-01T10:30:00Z", "2024-01-01T10:30:00"
    - Date only: "2024-01-01"
    - datetime objects
    - Pre-formatted: "timestamp '2024-01-01 00:00:00'"

    Example:
        RangeQuery(field="age", gte=18, lte=65)
        RangeQuery(field="scene_start_timestamp", gte="2024-01-01", lte="2024-12-31")

        # With datetime objects
        from datetime import datetime
        RangeQuery(field="scene_start_timestamp", gte=datetime(2024, 1, 1))
    """

    field: str
    gte: str | int | float | datetime | None = None  # Greater than or equal
    gt: str | int | float | datetime | None = None  # Greater than
    lte: str | int | float | datetime | None = None  # Less than or equal
    lt: str | int | float | datetime | None = None  # Less than

    def __post_init__(self):
        """Validate the query parameters."""
        if not self.field or not isinstance(self.field, str):
            raise SearchV2ValidationError(
                f"RangeQuery 'field' must be a non-empty string, got: {self.field!r}"
            )
        if all(v is None for v in [self.gte, self.gt, self.lte, self.lt]):
            raise SearchV2ValidationError(
                f"RangeQuery for field '{self.field}' must specify at least one condition: gte, gt, lte, or lt"
            )

    def to_dict(self) -> dict:
        range_params = {"field": self.field}

        # Add range conditions
        if self.gte is not None:
            range_params["gte"] = self.gte
        if self.gt is not None:
            range_params["gt"] = self.gt
        if self.lte is not None:
            range_params["lte"] = self.lte
        if self.lt is not None:
            range_params["lt"] = self.lt

        # Determine if this is a date or number range based on value types
        # If any value is a string or datetime, use date_range_query
        is_date_range = any(
            isinstance(v, (str, datetime))
            for v in [self.gte, self.gt, self.lte, self.lt]
            if v is not None
        )

        if is_date_range:
            return {"range": {"date_range_query": range_params}}
        else:
            return {"range": {"number_range_query": range_params}}


@dataclass
class ExistsQuery:
    """Match documents that have a non-null value for the field.

    Example:
        ExistsQuery(field="email")
    """

    field: str

    def __post_init__(self):
        """Validate the query parameters."""
        if not self.field or not isinstance(self.field, str):
            raise SearchV2ValidationError(
                f"ExistsQuery 'field' must be a non-empty string, got: {self.field!r}"
            )

    def to_dict(self) -> dict:
        return {"exists": {"field": self.field}}


@dataclass
class BoolQuery:
    """Combine multiple queries using boolean logic.

    Example:
        BoolQuery(
            must=[TermQuery(field="status", value="active")],
            must_not=[TermQuery(field="deleted", value=True)]
        )
    """

    must: list[TermQuery | TermsQuery | RangeQuery | ExistsQuery | BoolQuery] = field(
        default_factory=list
    )
    should: list[TermQuery | TermsQuery | RangeQuery | ExistsQuery | BoolQuery] = field(
        default_factory=list
    )
    must_not: list[TermQuery | TermsQuery | RangeQuery | ExistsQuery | BoolQuery] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        bool_clause = {}
        if self.must:
            bool_clause["must"] = [q.to_dict() for q in self.must]
        if self.should:
            bool_clause["should"] = [q.to_dict() for q in self.should]
        if self.must_not:
            bool_clause["must_not"] = [q.to_dict() for q in self.must_not]
        return {"bool": bool_clause}


# Type aliases
Query = TermQuery | TermsQuery | RangeQuery | ExistsQuery | BoolQuery
SortOrder = Literal["asc", "desc"]


@dataclass
class Sort:
    """Define sort order for search results.

    Example:
        Sort(field="created_at", order="desc")
        Sort(field="_score", order="desc")  # Sort by relevance score
    """

    field: str
    order: SortOrder = "asc"

    def __post_init__(self):
        """Validate the sort parameters."""
        if not self.field or not isinstance(self.field, str):
            raise SearchV2ValidationError(
                f"Sort 'field' must be a non-empty string, got: {self.field!r}"
            )
        if self.order not in ("asc", "desc"):
            raise SearchV2ValidationError(
                f"Sort 'order' must be 'asc' or 'desc', got: {self.order!r}"
            )

    def to_dict(self) -> dict:
        # Convert "asc"/"desc" to proto enum format
        order_enum = "SORT_ORDER_ASC" if self.order == "asc" else "SORT_ORDER_DESC"

        return {"field_with_direction": {"sort_order_map": {self.field: order_enum}}}


@dataclass
class SearchResponse:
    """Response from search operation."""

    items: list[SummaryItem]
    next_page_token: str


@dataclass
class SearchRequest:
    """Type-safe search request with query builders.

    Use this to build searches with type-safe query builders, or use
    raw dict body for maximum flexibility.

    Example:
        request = SearchRequest(
            query=TermQuery(field="device_type", value="LUCID_AIR"),
            sort=[Sort(field="scene_start_timestamp", order="desc")],
            limit=20,
            offset=0
        )
        results = client.search_v2.search(request=request)
    """

    query: Query | None = None
    sort: list[Sort] | None = None
    limit: int = 10
    offset: int = 0
    next_page_token: str | None = None

    def __post_init__(self):
        """Validate the request parameters."""
        # Validate pagination parameters
        if not isinstance(self.limit, int) or self.limit < 1:
            raise SearchV2ValidationError(
                f"SearchRequest 'limit' must be a positive integer, got: {self.limit!r}"
            )
        if self.limit > 10000:
            raise SearchV2ValidationError(
                f"SearchRequest 'limit' cannot exceed 10000, got: {self.limit}. Use pagination for large result sets."
            )
        if not isinstance(self.offset, int) or self.offset < 0:
            raise SearchV2ValidationError(
                f"SearchRequest 'offset' must be a non-negative integer, got: {self.offset!r}"
            )

        # Validate sort if provided
        if self.sort is not None:
            if not isinstance(self.sort, list):
                raise SearchV2ValidationError(
                    f"SearchRequest 'sort' must be a list of Sort objects, got: {type(self.sort).__name__}"
                )
            if not self.sort:
                raise SearchV2ValidationError(
                    "SearchRequest 'sort' cannot be an empty list. Either provide Sort objects or omit the parameter."
                )

    def to_dict(self) -> dict[str, Any]:
        """Convert SearchRequest to proto-based search request body."""
        body: dict[str, Any] = {
            "size": self.limit,
        }

        # Add offset if non-zero
        if self.offset > 0:
            body["from"] = self.offset

        # Add query if provided
        if self.query:
            body["query"] = self.query.to_dict()

        # Add sort if provided
        if self.sort:
            body["sort"] = [s.to_dict() for s in self.sort]

        full_request = {"request": {"search_request_body": body}}
        if self.next_page_token:
            full_request["after"] = self.next_page_token
        return full_request


def _wrap_value_with_type(value: str | int | float | bool) -> dict:
    """Wrap a value with its type for proto-based API.

    Args:
        value: The value to wrap (string, int, float, or bool)

    Returns:
        Dict with type wrapper, e.g., {"string": "value"} or {"general_number": {"int32_value": 1}}
    """
    if isinstance(value, bool):
        return {"bool": value}
    elif isinstance(value, str):
        return {"string": value}
    elif isinstance(value, int):
        # Use int64 for integers to handle large values
        return {"general_number": {"int64_value": value}}
    elif isinstance(value, float):
        return {"general_number": {"double_value": value}}
    else:
        # Fallback - treat as string
        return {"string": str(value)}


def _convert_timestamp_to_string(value: Any) -> str:
    """Convert datetime or date string to timestamp string format for proto API.

    The proto API expects timestamps in the format: "timestamp 'YYYY-MM-DD HH:MM:SS'"

    Args:
        value: Can be a datetime object, ISO date string, or timestamp string

    Returns:
        Timestamp string in format "timestamp 'YYYY-MM-DD HH:MM:SS'" or original value
    """
    if isinstance(value, datetime):
        # Convert datetime to timestamp string format
        # Format: "timestamp 'YYYY-MM-DD HH:MM:SS.ffffff'" (with microseconds if present)
        if value.microsecond:
            formatted = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
        else:
            formatted = value.strftime("%Y-%m-%d %H:%M:%S")
        return f"timestamp '{formatted}'"
    elif isinstance(value, str):
        # If already in timestamp format, return as-is
        if value.startswith("timestamp '"):
            return value

        # Try to parse ISO date string and convert to timestamp format
        try:
            # Try parsing ISO format with various levels of precision
            for fmt in [
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
            ]:
                try:
                    dt = datetime.strptime(value, fmt)
                    if dt.microsecond:
                        formatted = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")
                    else:
                        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
                    return f"timestamp '{formatted}'"
                except ValueError:
                    continue
            # If no format matches, assume it's already a valid timestamp string
            # Wrap it in timestamp format if it looks like a date
            if any(c in value for c in ["-", ":", "T"]):
                return f"timestamp '{value}'"
            return value
        except Exception:
            return value
    else:
        # Return as-is if it's already a number or other type
        return value


def _convert_timestamps_in_dict(data: dict) -> dict:
    """Recursively convert all timestamp values in a dictionary to timestamp string format.

    This looks for common timestamp field names and converts their values to the
    proto API format: "timestamp 'YYYY-MM-DD HH:MM:SS'".
    Also handles range query comparisons (gte, gt, lte, lt) for timestamp fields.
    Supports proto-based format with date_range_query and number_range_query.

    Args:
        data: Dictionary that may contain timestamp fields

    Returns:
        Dictionary with timestamps converted to "timestamp '...'" format
    """
    timestamp_fields = {
        "create_timestamp",
        "update_timestamp",
        "delete_timestamp",
        "scene_start_timestamp",
        "scene_end_timestamp",
        "timestamp",
        "created_at",
        "updated_at",
    }

    # Range comparison operators that might contain timestamps
    range_operators = {"gte", "gt", "lte", "lt"}

    result = {}
    for key, value in data.items():
        if key in timestamp_fields:
            # Direct timestamp field
            result[key] = _convert_timestamp_to_string(value)
        elif key in range_operators and isinstance(value, (str, datetime)):
            # Range operator with potential timestamp value
            result[key] = _convert_timestamp_to_string(value)
        elif isinstance(value, dict):
            # Check if this is a "date_range_query" (proto format)
            if key == "date_range_query":
                # This is a date range query - convert all range operator values
                nested_result = {}
                for field_key, field_value in value.items():
                    if field_key in range_operators and isinstance(field_value, (str, datetime)):
                        nested_result[field_key] = _convert_timestamp_to_string(field_value)
                    else:
                        nested_result[field_key] = field_value
                result[key] = nested_result
            # Check if this is a "range" query (legacy OpenSearch format)
            elif key == "range":
                # For range queries, check if the field being ranged is a timestamp
                nested_result = {}
                for field_name, range_conditions in value.items():
                    # Proto format uses date_range_query/number_range_query wrappers
                    if field_name in ("date_range_query", "number_range_query"):
                        nested_result[field_name] = _convert_timestamps_in_dict(range_conditions)
                    elif field_name in timestamp_fields and isinstance(range_conditions, dict):
                        # This is a timestamp field with range conditions
                        nested_result[field_name] = {
                            op: _convert_timestamp_to_string(val) if op in range_operators else val
                            for op, val in range_conditions.items()
                        }
                    else:
                        nested_result[field_name] = (
                            _convert_timestamps_in_dict(range_conditions)
                            if isinstance(range_conditions, dict)
                            else range_conditions
                        )
                result[key] = nested_result
            else:
                # Recursively convert nested dicts
                result[key] = _convert_timestamps_in_dict(value)
        elif isinstance(value, list):
            # Sort is not a timestamp filter, so we don't need to convert it
            if key == "sort":
                result[key] = value
            else:
                # Convert each item in lists
                result[key] = [
                    _convert_timestamps_in_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
        else:
            result[key] = value
    return result


class SearchV2:
    """Proto-based Search V2 API client with support for term, terms, range, exists queries.

    This class provides a clean interface to build and execute search queries using
    proto-based format with support for filtering, sorting, and pagination.

    Automatic timestamp conversion:
    - Date strings and datetime objects are automatically converted to "timestamp '...'" format
    - Applies to timestamp fields: *_timestamp, created_at, updated_at, etc.
    - Supports ISO 8601 formats and simple date strings like "2024-01-01"
    - Output format: "timestamp 'YYYY-MM-DD HH:MM:SS'" or "timestamp 'YYYY-MM-DDTHH:MM:SS.ffffff'"

    Example usage:
        # Simple term query
        results = client.search_v2.search(
            SearchRequest(
                query=TermQuery(field="device_type", value="LUCID_AIR"),
                limit=10
            )
        )
        print(f"Found {len(results.items)} scenes")

        # Complex boolean query with filters
        results = client.search_v2.search(
            SearchRequest(
                query=BoolQuery(
                    must=[TermQuery(field="device_type", value="LUCID_AIR")]
                ),
                sort=[Sort(field="scene_start_timestamp", order="desc")],
                limit=20,
                offset=0
            )
        )
        for item in results.items:
            print(f"Scene: {item.scene_id}, City: {item.city}")
    """

    def __init__(self, client: Any):
        """Initialize SearchV2.

        Args:
            client: The HTTP client instance
        """
        self.client = client

    def search(
        self,
        request: SearchRequest | dict[str, Any],
    ) -> SearchResponse:
        """Execute a search query using proto-based API format.

        Args:
            request: Either a SearchRequest (type-safe with query builders) or
                    a raw dict (for maximum flexibility with proto-based format)

        Returns:
            SearchResponse containing:
                - items: List of SummaryItem objects describing scenes
                - next_page_token: Token for pagination

        Raises:
            SearchV2ValidationError: If parameters are invalid

        Examples:
            Type-safe SearchRequest approach (recommended):
            >>> from avcloud.experimental.resources.search_v2 import SearchRequest, TermQuery, Sort
            >>> request = SearchRequest(
            ...     query=TermQuery(field="device_type", value="LUCID_AIR"),
            ...     sort=[Sort(field="scene_start_timestamp", order="desc")],
            ...     limit=50
            ... )
            >>> results = client.search_v2.search(request)
            >>> print(f"Found {len(results.items)} scenes")

            Raw dict approach (proto format):
            >>> results = client.search_v2.search({
            ...     "request": {
            ...         "search_request_body": {
            ...             "query": {
            ...                 "bool": {
            ...                     "must": [{
            ...                         "term": {
            ...                             "field": "device_type",
            ...                             "value": {"string": "LUCID_AIR"}
            ...                         }
            ...                     }]
            ...                 }
            ...             },
            ...             "sort": [{
            ...                 "field_with_direction": {
            ...                     "sort_order_map": {
            ...                         "scene_start_timestamp": "SORT_ORDER_DESC"
            ...                     }
            ...                 }
            ...             }],
            ...             "from": 0,
            ...             "size": 10
            ...         }
            ...     }
            ... })
        """
        # Build the request body based on input type
        if isinstance(request, SearchRequest):
            # Use SearchRequest (validation already done in __post_init__)
            request_body = request.to_dict()
        elif isinstance(request, dict):
            # Raw dict - use as-is
            request_body = request
        else:
            raise SearchV2ValidationError(
                f"'request' must be either SearchRequest or dict, got: {type(request).__name__}"
            )

        # Convert all timestamp strings/datetime objects to "timestamp '...'" format
        request_body = _convert_timestamps_in_dict(request_body)

        # Execute the search request via the API
        # request_body already contains the full structure with "request.search_request_body"

        response = self.client.post(
            "/avcloud/api/v2/genericrpc",
            json={"method": "SearchService.Search", "request_json": json.dumps(request_body)},
        )

        return self._parse_response(response.json())

    def _parse_response(self, response: dict) -> SearchResponse:
        """Parse API response into SearchResponse format.

        Args:
            response: Raw API response containing items and next_page_token

        Returns:
            SearchResponse with items (list of SummaryItem objects) and next_page_token
        """
        # Convert raw dict items to SummaryItem objects
        response_json = json.loads(response.get("responseJson", "{}"))
        items = [SummaryItem.from_dict(item) for item in response_json.get("items", [])]
        return SearchResponse(
            items=items, next_page_token=response_json.get("pagination", {}).get("next", "")
        )
