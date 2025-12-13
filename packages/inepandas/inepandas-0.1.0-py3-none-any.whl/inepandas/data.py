"""Functions for retrieving statistical data from the INE API."""

from typing import Any

import pandas as pd

from .client import INEClient
from .exceptions import DataParsingError, ValidationError


def _parse_date_param(
    date_start: str | None,
    date_end: str | None,
) -> str | None:
    """
    Parse date parameters into API format.

    Parameters
    ----------
    date_start : str | None
        Start date in format "YYYY/MM/DD" or "YYYYMMDD".
    date_end : str | None
        End date in format "YYYY/MM/DD" or "YYYYMMDD".

    Returns
    -------
    str | None
        Date parameter in API format "YYYYMMDD:YYYYMMDD" or None.
    """
    if date_start is None and date_end is None:
        return None

    def normalize_date(date_str: str | None) -> str:
        if date_str is None:
            return ""
        # Remove slashes and dashes
        return date_str.replace("/", "").replace("-", "")

    start = normalize_date(date_start)
    end = normalize_date(date_end)

    return f"{start}:{end}"


def _flatten_series_data(data: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Flatten nested series data into a single DataFrame.

    The API returns data with nested 'Data' arrays. This function
    flattens them into a single DataFrame with series metadata
    repeated for each data point.

    Parameters
    ----------
    data : list[dict[str, Any]]
        Raw API response data.

    Returns
    -------
    pd.DataFrame
        Flattened DataFrame with all data points.
    """
    rows = []

    for series in data:
        # Extract series-level metadata
        series_meta = {
            k: v for k, v in series.items()
            if k != "Data" and not isinstance(v, (list, dict))
        }

        # Get the nested data
        series_data = series.get("Data", [])

        if isinstance(series_data, list):
            for point in series_data:
                row = {**series_meta, **point}
                rows.append(row)
        elif isinstance(series_data, dict):
            # Single data point
            row = {**series_meta, **series_data}
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def _process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process and clean the DataFrame.

    - Convert date columns to datetime
    - Convert numeric columns to appropriate types
    - Rename columns for clarity

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame.

    Returns
    -------
    pd.DataFrame
        Processed DataFrame.
    """
    if df.empty:
        return df

    df = df.copy()

    # Try to convert 'Fecha' column to datetime
    if "Fecha" in df.columns:
        try:
            # API returns timestamps in milliseconds or ISO format
            if df["Fecha"].dtype == "object":
                df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            else:
                # Numeric timestamp (milliseconds since epoch)
                df["Fecha"] = pd.to_datetime(df["Fecha"], unit="ms", errors="coerce")
        except Exception:
            pass  # Keep original if conversion fails

    # Convert 'Valor' to numeric if present
    if "Valor" in df.columns:
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    # Convert 'Anyo' to int if present
    if "Anyo" in df.columns:
        df["Anyo"] = pd.to_numeric(df["Anyo"], errors="coerce").astype("Int64")

    return df


def get_table_data(
    table_id: int,
    client: INEClient | None = None,
    nlast: int | None = None,
    date_start: str | None = None,
    date_end: str | None = None,
    detail: int = 0,
    friendly: bool = True,
    metadata: bool = False,
    filters: dict[int, int] | None = None,
) -> pd.DataFrame:
    """
    Get data from a statistical table.

    Parameters
    ----------
    table_id : int
        The table identifier.
    client : INEClient | None, optional
        An existing INEClient instance.
    nlast : int | None, optional
        Number of last periods to retrieve.
    date_start : str | None, optional
        Start date in format "YYYY/MM/DD" or "YYYYMMDD".
    date_end : str | None, optional
        End date in format "YYYY/MM/DD" or "YYYYMMDD".
    detail : int, optional
        Level of detail (0, 1, or 2).
    friendly : bool, optional
        Whether to use friendly output format. Defaults to True.
    metadata : bool, optional
        Whether to include metadata. Defaults to False.
    filters : dict[int, int] | None, optional
        Dictionary mapping variable IDs to value IDs for filtering.
        Example: {115: 29} filters to province Madrid (variable 115, value 29).

    Returns
    -------
    pd.DataFrame
        DataFrame with the table data.

    Examples
    --------
    >>> # Get last 5 periods of CPI table
    >>> df = get_table_data(50902, nlast=5)

    >>> # Get data for 2024
    >>> df = get_table_data(50902, date_start="2024/01/01", date_end="2024/12/31")

    >>> # Get data filtered by province
    >>> df = get_table_data(50913, nlast=1, filters={70: 9027})  # Catalonia
    """
    _client = client or INEClient()

    # Build parameters
    params: dict[str, Any] = {"det": detail}

    if nlast is not None:
        params["nult"] = nlast

    date_param = _parse_date_param(date_start, date_end)
    if date_param:
        params["date"] = date_param

    # Build tip parameter
    tip_parts = []
    if friendly:
        tip_parts.append("A")
    if metadata:
        tip_parts.append("M")
    if tip_parts:
        params["tip"] = "".join(tip_parts)

    # Add filters
    if filters:
        for var_id, val_id in filters.items():
            params[f"tv"] = f"{var_id}:{val_id}"

    try:
        data = _client.get("DATOS_TABLA", table_id, **params)
    finally:
        if client is None:
            _client.close()

    if not data:
        return pd.DataFrame()

    # Flatten and process the data
    df = _flatten_series_data(data)
    df = _process_dataframe(df)

    return df


def get_series_data(
    series_code: str,
    client: INEClient | None = None,
    nlast: int | None = None,
    date_start: str | None = None,
    date_end: str | None = None,
    detail: int = 0,
    friendly: bool = True,
    metadata: bool = False,
) -> pd.DataFrame:
    """
    Get data from a specific series.

    Parameters
    ----------
    series_code : str
        The series code (e.g., "IPC251856").
    client : INEClient | None, optional
        An existing INEClient instance.
    nlast : int | None, optional
        Number of last periods to retrieve.
    date_start : str | None, optional
        Start date in format "YYYY/MM/DD" or "YYYYMMDD".
    date_end : str | None, optional
        End date in format "YYYY/MM/DD" or "YYYYMMDD".
    detail : int, optional
        Level of detail (0, 1, or 2).
    friendly : bool, optional
        Whether to use friendly output format. Defaults to True.
    metadata : bool, optional
        Whether to include metadata. Defaults to False.

    Returns
    -------
    pd.DataFrame
        DataFrame with the series data.

    Examples
    --------
    >>> # Get last 12 months of CPI annual variation
    >>> df = get_series_data("IPC251856", nlast=12)

    >>> # Get 2023 data
    >>> df = get_series_data("IPC251856", date_start="2023/01/01", date_end="2023/12/31")
    """
    _client = client or INEClient()

    # Build parameters
    params: dict[str, Any] = {"det": detail}

    if nlast is not None:
        params["nult"] = nlast

    date_param = _parse_date_param(date_start, date_end)
    if date_param:
        params["date"] = date_param

    # Build tip parameter
    tip_parts = []
    if friendly:
        tip_parts.append("A")
    if metadata:
        tip_parts.append("M")
    if tip_parts:
        params["tip"] = "".join(tip_parts)

    try:
        data = _client.get("DATOS_SERIE", series_code, **params)
    finally:
        if client is None:
            _client.close()

    if not data:
        return pd.DataFrame()

    # Series data comes as a single object with nested Data
    if isinstance(data, dict):
        data = [data]

    df = _flatten_series_data(data)
    df = _process_dataframe(df)

    return df


def get_operation_data(
    operation: str | int,
    client: INEClient | None = None,
    periodicity: int | None = None,
    nlast: int | None = None,
    detail: int = 0,
    friendly: bool = True,
    metadata: bool = False,
    **filters: int | None,
) -> pd.DataFrame:
    """
    Get data from an operation using metadata filters.

    This function allows flexible querying of operation data by
    specifying variable-value pairs as filters.

    Parameters
    ----------
    operation : str | int
        The operation identifier (e.g., "IPC" or 25).
    client : INEClient | None, optional
        An existing INEClient instance.
    periodicity : int | None, optional
        Periodicity ID (1=monthly, 3=quarterly, 6=semi-annual, 12=annual).
    nlast : int | None, optional
        Number of last periods to retrieve.
    detail : int, optional
        Level of detail (0, 1, or 2).
    friendly : bool, optional
        Whether to use friendly output format. Defaults to True.
    metadata : bool, optional
        Whether to include metadata. Defaults to False.
    **filters : int | None
        Filter groups as g1, g2, g3, etc.
        Format: g1="variable_id:value_id" or g1="variable_id:" for all values.

    Returns
    -------
    pd.DataFrame
        DataFrame with the filtered operation data.

    Examples
    --------
    >>> # Get CPI monthly variation for Madrid province, all ECOICOP groups
    >>> df = get_operation_data(
    ...     "IPC",
    ...     periodicity=1,
    ...     nlast=1,
    ...     g1="115:29",    # Province: Madrid
    ...     g2="3:84",      # Data type: monthly variation
    ...     g3="762:",      # ECOICOP groups: all
    ... )
    """
    _client = client or INEClient()

    params: dict[str, Any] = {"det": detail}

    if periodicity is not None:
        params["p"] = periodicity

    if nlast is not None:
        params["nult"] = nlast

    # Build tip parameter
    tip_parts = []
    if friendly:
        tip_parts.append("A")
    if metadata:
        tip_parts.append("M")
    if tip_parts:
        params["tip"] = "".join(tip_parts)

    # Add filter groups
    for key, value in filters.items():
        if value is not None:
            params[key] = value

    try:
        data = _client.get("DATOS_METADATAOPERACION", operation, **params)
    finally:
        if client is None:
            _client.close()

    if not data:
        return pd.DataFrame()

    df = _flatten_series_data(data)
    df = _process_dataframe(df)

    return df
