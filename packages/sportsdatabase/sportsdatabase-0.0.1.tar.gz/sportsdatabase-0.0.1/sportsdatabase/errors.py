from typing import Any, Dict


class SportsDatabaseError(Exception):
    def __init__(self, message: str, *, status: int | None = None, code: str | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.details = details or {}


class ApiError(SportsDatabaseError):
    pass


class RateLimitError(SportsDatabaseError):
    def __init__(self, message: str, *, status: int, reset_at: float | None = None, details: Dict[str, Any] | None = None):
        super().__init__(message, status=status, code="rate_limit_exceeded", details=details)
        self.reset_at = reset_at


class NetworkError(SportsDatabaseError):
    pass
