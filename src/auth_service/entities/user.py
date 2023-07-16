from typing import Optional

from pydantic import BaseModel

from . import encode


class User(BaseModel):
    id: str
    email: str
    password: str
    name: str = None
    last_name: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = False

    class Config:
        from_attributes = True

    def is_valid_password(self, password: str) -> bool:
        return encode(password) == self.password
