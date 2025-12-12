from functools import lru_cache

from moysklad_api.exceptions import TokenValidationError


@lru_cache
def validate_token(token: str) -> bool:
    """
    Validate Moy Sklad token

    :param token:
    :return:
    """
    if not isinstance(token, str):
        msg = f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        raise TokenValidationError(msg)

    if any(x.isspace() for x in token):
        message = "Token is invalid! It can't contains spaces."
        raise TokenValidationError(message)

    return True
