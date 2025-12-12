from http import HTTPStatus


class CustomException(Exception):
    status_code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description
    level = 40

    def __init__(self, message: str = None, level: int = None):
        if message:
            self.message = message
        if level:
            self.level = level

    def __str__(self) -> str:
        return str(self.error_code)
