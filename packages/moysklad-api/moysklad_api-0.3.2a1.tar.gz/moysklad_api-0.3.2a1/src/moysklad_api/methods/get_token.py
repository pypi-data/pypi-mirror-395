from pydantic import Field

from moysklad_api.methods.base import MSMethod
from moysklad_api.types.token import Token


class GetToken(MSMethod[Token]):
    __return__ = Token
    __api_method__ = "security/token"

    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
