"""Custom exceptions for VirtualDojo CLI."""

from typing import Optional


class VirtualDojoError(Exception):
    """Base exception for VirtualDojo CLI."""

    def __init__(self, message: str, hint: Optional[str] = None):
        self.message = message
        self.hint = hint
        super().__init__(message)


class AuthenticationError(VirtualDojoError):
    """Raised when authentication fails."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when the JWT token has expired."""

    def __init__(self):
        super().__init__(
            message="Your session has expired.",
            hint="Run 'vdojo login' to authenticate again.",
        )


class TokenRefreshedError(VirtualDojoError):
    """Raised internally when token was refreshed and request should be retried."""

    pass


class ConfigurationError(VirtualDojoError):
    """Raised when there's a configuration issue."""

    pass


class NotLoggedInError(ConfigurationError):
    """Raised when user is not logged in."""

    def __init__(self):
        super().__init__(
            message="You are not logged in.",
            hint="Run 'vdojo login' to authenticate.",
        )


class ProfileNotFoundError(ConfigurationError):
    """Raised when the specified profile doesn't exist."""

    def __init__(self, profile_name: str):
        super().__init__(
            message=f"Profile '{profile_name}' not found.",
            hint="Run 'vdojo config profile list' to see available profiles.",
        )


class APIError(VirtualDojoError):
    """Raised when the API returns an error."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(
            message=f"API Error ({status_code}): {detail}",
            hint=self._get_hint(status_code),
        )

    @staticmethod
    def _get_hint(status_code: int) -> Optional[str]:
        hints = {
            400: "Check your request parameters.",
            401: "Your session may have expired. Run 'vdojo login'.",
            403: "You don't have permission for this action.",
            404: "The requested resource was not found.",
            429: "Rate limit exceeded. Wait a moment and try again.",
            500: "Server error. Try again later or contact support.",
        }
        return hints.get(status_code)


class NetworkError(VirtualDojoError):
    """Raised when there's a network connectivity issue."""

    def __init__(self, detail: str):
        super().__init__(
            message=f"Network error: {detail}",
            hint="Check your internet connection and server URL.",
        )


class ValidationError(VirtualDojoError):
    """Raised when input validation fails."""

    pass
