"""
inepandas - A Python wrapper for the Spanish National Statistics Institute (INE) API.

This package provides convenient access to all statistical data and metadata
published by the Instituto Nacional de Estadística (INE) of Spain.

Basic usage:

    >>> import inepandas
    >>>
    >>> # Get available operations
    >>> operations = inepandas.get_operations()
    >>>
    >>> # Get CPI data
    >>> cpi = inepandas.get_table_data(50902, nlast=5)
    >>>
    >>> # Get specific series
    >>> series = inepandas.get_series_data("IPC251856", nlast=12)

For more control, use the INEClient directly:

    >>> from inepandas import INEClient
    >>>
    >>> with INEClient(language="EN") as client:
    ...     ops = inepandas.get_operations(client=client)
"""

from .client import INEClient
from .data import get_operation_data, get_series_data, get_table_data
from .exceptions import (
    APIError,
    DataParsingError,
    NotFoundError,
    PyINEError,
    RateLimitError,
    ValidationError,
)
from .metadata import (
    get_classifications,
    get_operation,
    get_operations,
    get_periodicities,
    get_publications,
    get_series_metadata,
    get_series_values,
    get_table_group_values,
    get_table_groups,
    get_table_series,
    get_tables,
    get_values,
    get_variables,
)

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Client
    "INEClient",
    # Data functions
    "get_table_data",
    "get_series_data",
    "get_operation_data",
    # Metadata functions
    "get_operations",
    "get_operation",
    "get_variables",
    "get_values",
    "get_tables",
    "get_table_groups",
    "get_table_group_values",
    "get_table_series",
    "get_series_metadata",
    "get_series_values",
    "get_periodicities",
    "get_publications",
    "get_classifications",
    # Exceptions
    "PyINEError",
    "APIError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "DataParsingError",
]
