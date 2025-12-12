class MsApiError(Exception):
    """
    Base exception for all ms api errors.
    """


class DetailedMsApiError(MsApiError):
    """
    Base exception for all ms api errors with detailed message.
    """

    url: str | None = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class NotAuthorizedError(DetailedMsApiError):
    url = "https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-autentifikaciq"


class TokenValidationError(Exception):
    pass


class MSApiError(DetailedMsApiError):
    def __init__(self, message: str, url: str | None = None) -> None:
        super().__init__(message)
        self.url = url
