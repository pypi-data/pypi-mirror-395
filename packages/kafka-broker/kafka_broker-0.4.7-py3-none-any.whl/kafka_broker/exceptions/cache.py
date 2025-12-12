from http import HTTPStatus
from .base import CustomException


class ConnectionException(CustomException):
    status_code = 500
    error_code = "COULD_NOT_INNITIALIZE_CONNECTION"
    message = "The connection could not be established"


class KeyNotFoundException(CustomException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "KEY_NOT_FOUND"
    message = "key not found in memcached"


class CouldNotEditMemcache(CustomException):
    status_code = 400
    error_code = "COULD_NOT_EDIT_MEMCACHED"
    message = "could not add, update or delete the entity in memcached"
