"""Core HTTP client for INE API communication."""

from typing import Any
from urllib.parse import urlencode

import requests

from .exceptions import APIError, NotFoundError, RateLimitError

# Base URL for the INE API
BASE_URL = "https://servicios.ine.es/wstempus/js"

# Supported languages
LANGUAGES = ("ES", "EN")

# Default timeout for requests (seconds)
DEFAULT_TIMEOUT = 30


class INEClient:
    """
    HTTP client for communicating with the INE JSON API.

    This class handles all HTTP communication with the INE API,
    including request construction, error handling, and response parsing.

    Parameters
    ----------
    language : str, optional
        Language for API responses. Either "ES" (Spanish) or "EN" (English).
        Defaults to "ES".
    timeout : int, optional
        Request timeout in seconds. Defaults to 30.

    Examples
    --------
    >>> client = INEClient()
    >>> operations = client.get("OPERACIONES_DISPONIBLES")

    >>> client = INEClient(language="EN")
    >>> operations = client.get("OPERACIONES_DISPONIBLES")
    """

    def __init__(
        self,
        language: str = "ES",
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        if language.upper() not in LANGUAGES:
            raise ValueError(f"Language must be one of {LANGUAGES}, got '{language}'")

        self.language = language.upper()
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "inepandas/0.1.0",
            }
        )

    def _build_url(
        self,
        function: str,
        input_id: str | int | None = None,
        params: dict[str, Any] | None = None,
    ) -> str:
        """
        Build the full URL for an API request.

        Parameters
        ----------
        function : str
            The API function name (e.g., "DATOS_TABLA", "OPERACIONES_DISPONIBLES").
        input_id : str | int | None, optional
            The input identifier for the function.
        params : dict[str, Any] | None, optional
            Query parameters to include in the URL.

        Returns
        -------
        str
            The complete URL for the API request.
        """
        url_parts = [BASE_URL, self.language, function]

        if input_id is not None:
            url_parts.append(str(input_id))

        url = "/".join(url_parts)

        if params:
            # Filter out None values and convert to string
            filtered_params = {
                k: str(v) for k, v in params.items() if v is not None
            }
            if filtered_params:
                url = f"{url}?{urlencode(filtered_params)}"

        return url

    def get(
        self,
        function: str,
        input_id: str | int | None = None,
        **params: Any,
    ) -> Any:
        """
        Make a GET request to the INE API.

        Parameters
        ----------
        function : str
            The API function name.
        input_id : str | int | None, optional
            The input identifier for the function.
        **params : Any
            Additional query parameters.

        Returns
        -------
        Any
            The parsed JSON response.

        Raises
        ------
        NotFoundError
            If the requested resource is not found (404).
        RateLimitError
            If the API rate limit is exceeded (429).
        APIError
            For other API errors.
        """
        url = self._build_url(function, input_id, params if params else None)

        try:
            response = self._session.get(url, timeout=self.timeout)
        except requests.exceptions.Timeout as e:
            raise APIError(f"Request timed out after {self.timeout} seconds") from e
        except requests.exceptions.ConnectionError as e:
            raise APIError(f"Connection error: {e}") from e
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}") from e

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle the API response and raise appropriate exceptions.

        Parameters
        ----------
        response : requests.Response
            The response object from the request.

        Returns
        -------
        Any
            The parsed JSON response.

        Raises
        ------
        NotFoundError
            If the resource is not found (404).
        RateLimitError
            If rate limit is exceeded (429).
        APIError
            For other HTTP errors.
        """
        if response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {response.url}",
                status_code=404,
            )

        if response.status_code == 429:
            raise RateLimitError(
                "API rate limit exceeded. Please try again later.",
                status_code=429,
            )

        if response.status_code >= 400:
            raise APIError(
                f"API error: {response.status_code} - {response.text}",
                status_code=response.status_code,
            )

        try:
            return response.json()
        except ValueError as e:
            raise APIError(f"Failed to parse JSON response: {e}") from e

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self) -> "INEClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()
