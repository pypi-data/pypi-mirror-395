# -*- coding: utf-8 -*-
"""Custom exceptions for the 24SEA API."""
import logging
from typing import Optional

from httpx import Request


class AuthenticationError(Exception):
    """An exception to raise when the user is not authenticated."""

    pass


class ProfileError(Exception):
    """An exception to raise when the user is authenticated, but its profile
    is not properly configured."""

    pass


class DataSignalsError(Exception):
    """An exception to raise when the data signals are not properly
    configured."""

    pass


class HTTPError(Exception):
    """
    Base class for ``RequestError`` and ``HTTPStatusError``.

    Useful for  ``try...except`` blocks when issuing a request,
    and then calling ``.raise_for_status()``.

    For example:

    >>> try:
    ...     response = httpx.get("https://www.example.com")
    ...     response.raise_for_status()
    ... except httpx.HTTPError as exc:
    ...     print(f"HTTP Exception for {exc.request.url} - {exc}")
    """

    def __init__(self, message: str, text: str = "") -> None:
        """Initialize the HTTPError."""
        super().__init__(message, text)
        self.text = text
        self._request: Optional[Request] = None

    @property
    def request(self) -> Request:
        if self._request is None:
            raise RuntimeError("The .request property has not been set.")
        return self._request

    @request.setter
    def request(self, request: Request) -> None:
        self._request = request

    def __repr__(self) -> str:
        """Return the representation of the HTTPError."""
        return f"HTTPError({self.args[0]!r}, text={self.text!r})"

    def __str__(self) -> str:
        """Return the string representation of the HTTPError."""
        return str(self.args[0]) + (f" (text={self.text})" if self.text else "")


def raise_for_status(response) -> None:
    """
    Raise an HTTPError if the response status code indicates an error.

    This function checks the status code of the provided HTTP response. If the
    status code is in the 4xx or 5xx range, it raises an HTTPError with a
    descriptive message including the status code and URL.

    Parameters
    ----------
    response : httpx.Response
        The HTTP response object to check for errors.

    Raises
    ------
    HTTPError
        If the response status code is between 400 and 599 (inclusive),
        indicating a client or server error.
    """
    if 400 <= response.status_code < 600:
        http_error_msg = f"\033[1;31m{response.status_code}\n"
        http_error_msg += f"Error for url: {response.url}\033[0m"
        if response.status_code == 500:
            http_error_msg += (
                "\nThe server encountered an internal error and was "
                "unable to complete your request. Please try again later, "
                "or contact support at \033[32;1;4msupport.api@24sea.eu\033[0m "
                "if the problem persists."
            )
        logging.error(http_error_msg)
        raise HTTPError(http_error_msg, text=response.text) from None
