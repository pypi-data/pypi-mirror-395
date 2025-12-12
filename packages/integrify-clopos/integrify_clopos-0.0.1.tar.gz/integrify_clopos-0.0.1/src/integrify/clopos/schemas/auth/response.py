from typing import Literal

from pydantic import BaseModel


class AuthResponse(BaseModel):
    success: Literal[True]
    token: str
    token_type: str
    expires_in: int
    message: str
