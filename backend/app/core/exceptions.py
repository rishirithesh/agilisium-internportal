class AIRPException(Exception):
    """Base class for all domain-level exceptions in AIRP."""

    status_code = 400
    error_code = "AIRP_ERROR"

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(message)


class NotFoundError(AIRPException):
    status_code = 404
    error_code = "NOT_FOUND"


class ValidationError(AIRPException):
    status_code = 422
    error_code = "VALIDATION_ERROR"


class AuthenticationError(AIRPException):
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"


class AuthorizationError(AIRPException):
    status_code = 403
    error_code = "AUTHORIZATION_ERROR"


class ConflictError(AIRPException):
    status_code = 409
    error_code = "CONFLICT"


class InvalidStateTransitionError(AIRPException):
    status_code = 409
    error_code = "INVALID_STATE_TRANSITION"
