import typing

from py_jsearch._types import APIResponse


__all__ = [
    "JSearchClientError",
    "JSearchAuthError",
    "JSearchResponseError",
]


class JSearchClientError(Exception):
    """Custom exception for JSearchClient errors."""

    def __init__(
        self,
        message: typing.Optional[str] = None,
        code: typing.Optional[int] = None,
        response: typing.Optional[APIResponse] = None,
    ):
        if message is None and code is not None:
            if response is not None and response.status != "ok":
                message = f"JSearch API returned status '{response.status}' for request '{response.request_id}' with code {code}"
            else:
                message = f"JSearch API Error with status code {code}"

        super().__init__(message)
        self.code = code
        self.response = response


class JSearchAuthError(JSearchClientError):
    """Exception for authentication errors."""


class JSearchResponseError(JSearchClientError):
    """Exception for response parsing errors."""
