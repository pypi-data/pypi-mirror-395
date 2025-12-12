from .base import CustomException


class MalformedAuditLogException(CustomException):
    status_code = 400
    error_code = "COULD_NOT_READ_AUDIT_LOG"
    message = "THe audit log is malformed for the invoked method"
