"""Functions for retrieving metadata from the INE API."""

from typing import Any

import pandas as pd

from .client import INEClient


def get_operations(
    client: INEClient | None = None,
    detail: int = 0,
    geo: int | None = None,
) -> pd.DataFrame:
    """
    Get all available statistical operations.

    Parameters
    ----------
    client : INEClient | None, optional
        An existing INEClient instance. If None, creates a new one.
    detail : int, optional
        Level of detail (0, 1, or 2). Defaults to 0.
    geo : int | None, optional
        Geographic scope filter:
        - None: all operations
        - 0: national results only
        - 1: regional/provincial/municipal results

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Id, Cod_IOE, Nombre, Codigo, Url (if available)

    Examples
    --------
    >>> ops = get_operations()
    >>> ops.head()
    """
    _client = client or INEClient()

    params: dict[str, Any] = {"det": detail}
    if geo is not None:
        params["geo"] = geo

    data = _client.get("OPERACIONES_DISPONIBLES", **params)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_operation(
    operation: str | int,
    client: INEClient | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get information about a specific operation.

    Parameters
    ----------
    operation : str | int
        Operation identifier. Can be:
        - Numeric ID (e.g., 25)
        - Alphabetic code (e.g., "IPC")
        - IOE code (e.g., "IOE30138")
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with operation information.
    """
    _client = client or INEClient()

    data = _client.get("OPERACION", operation, det=detail)

    if client is None:
        _client.close()

    # API returns a single object, wrap in list for DataFrame
    if isinstance(data, dict):
        data = [data]

    return pd.DataFrame(data)


def get_variables(
    client: INEClient | None = None,
    operation: str | int | None = None,
) -> pd.DataFrame:
    """
    Get available variables, optionally filtered by operation.

    Parameters
    ----------
    client : INEClient | None, optional
        An existing INEClient instance.
    operation : str | int | None, optional
        If provided, only return variables used in this operation.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Id, Nombre, Codigo
    """
    _client = client or INEClient()

    if operation is not None:
        data = _client.get("VARIABLES_OPERACION", operation)
    else:
        data = _client.get("VARIABLES")

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_values(
    variable: int,
    client: INEClient | None = None,
    operation: str | int | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get all values for a specific variable.

    Parameters
    ----------
    variable : int
        The variable ID.
    client : INEClient | None, optional
        An existing INEClient instance.
    operation : str | int | None, optional
        If provided, only return values used in this operation.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Id, Fk_Variable, Nombre, Codigo
    """
    _client = client or INEClient()

    if operation is not None:
        data = _client.get(
            "VALORES_VARIABLEOPERACION",
            f"{variable}/{operation}",
            det=detail,
        )
    else:
        data = _client.get("VALORES_VARIABLE", variable, det=detail)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_tables(
    operation: str | int,
    client: INEClient | None = None,
    detail: int = 0,
    geo: int | None = None,
) -> pd.DataFrame:
    """
    Get all tables for a specific operation.

    Parameters
    ----------
    operation : str | int
        The operation identifier.
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).
    geo : int | None, optional
        Geographic scope filter (0=national, 1=regional).

    Returns
    -------
    pd.DataFrame
        DataFrame with table information.
    """
    _client = client or INEClient()

    params: dict[str, Any] = {"det": detail}
    if geo is not None:
        params["geo"] = geo

    data = _client.get("TABLAS_OPERACION", operation, **params)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_table_groups(
    table_id: int,
    client: INEClient | None = None,
) -> pd.DataFrame:
    """
    Get the selection groups (combos) that define a table.

    Parameters
    ----------
    table_id : int
        The table identifier.
    client : INEClient | None, optional
        An existing INEClient instance.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Id, Nombre
    """
    _client = client or INEClient()

    data = _client.get("GRUPOS_TABLA", table_id)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_table_group_values(
    table_id: int,
    group_id: int,
    client: INEClient | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get all values for a specific group within a table.

    Parameters
    ----------
    table_id : int
        The table identifier.
    group_id : int
        The group identifier.
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with value information.
    """
    _client = client or INEClient()

    data = _client.get(
        "VALORES_GRUPOSTABLA",
        f"{table_id}/{group_id}",
        det=detail,
    )

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_series_metadata(
    series_code: str,
    client: INEClient | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get metadata for a specific series.

    Parameters
    ----------
    series_code : str
        The series code (e.g., "IPC251856").
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with series metadata.
    """
    _client = client or INEClient()

    data = _client.get("SERIE", series_code, det=detail)

    if client is None:
        _client.close()

    if isinstance(data, dict):
        data = [data]

    return pd.DataFrame(data)


def get_series_values(
    series_code: str,
    client: INEClient | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get the variables and values that define a series.

    Parameters
    ----------
    series_code : str
        The series code (e.g., "IPC251856").
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with the values defining the series.
    """
    _client = client or INEClient()

    data = _client.get("VALORES_SERIE", series_code, det=detail)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_table_series(
    table_id: int,
    client: INEClient | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get all series contained in a table.

    Parameters
    ----------
    table_id : int
        The table identifier.
    client : INEClient | None, optional
        An existing INEClient instance.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with series information.
    """
    _client = client or INEClient()

    data = _client.get("SERIES_TABLA", table_id, det=detail)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_periodicities(
    client: INEClient | None = None,
) -> pd.DataFrame:
    """
    Get all available periodicities.

    Common periodicities:
    - 1: monthly
    - 3: quarterly
    - 6: semi-annual
    - 12: annual

    Parameters
    ----------
    client : INEClient | None, optional
        An existing INEClient instance.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Id, Nombre, Codigo
    """
    _client = client or INEClient()

    data = _client.get("PERIODICIDADES")

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_publications(
    client: INEClient | None = None,
    operation: str | int | None = None,
    detail: int = 0,
) -> pd.DataFrame:
    """
    Get available publications, optionally filtered by operation.

    Parameters
    ----------
    client : INEClient | None, optional
        An existing INEClient instance.
    operation : str | int | None, optional
        If provided, only return publications for this operation.
    detail : int, optional
        Level of detail (0, 1, or 2).

    Returns
    -------
    pd.DataFrame
        DataFrame with publication information.
    """
    _client = client or INEClient()

    if operation is not None:
        data = _client.get("PUBLICACIONES_OPERACION", operation, det=detail)
    else:
        data = _client.get("PUBLICACIONES", det=detail)

    if client is None:
        _client.close()

    return pd.DataFrame(data)


def get_classifications(
    client: INEClient | None = None,
    operation: str | int | None = None,
) -> pd.DataFrame:
    """
    Get available classifications, optionally filtered by operation.

    Parameters
    ----------
    client : INEClient | None, optional
        An existing INEClient instance.
    operation : str | int | None, optional
        If provided, only return classifications for this operation.

    Returns
    -------
    pd.DataFrame
        DataFrame with classification information.
    """
    _client = client or INEClient()

    if operation is not None:
        data = _client.get("CLASIFICACIONES_OPERACION", operation)
    else:
        data = _client.get("CLASIFICACIONES")

    if client is None:
        _client.close()

    return pd.DataFrame(data)
