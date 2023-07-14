import base64
from typing import Optional
from pydantic import BaseModel
from . import encode

class User(BaseModel):
    email: str
    password: str
    name: str = None
    last_name: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = False

    def is_valid_password(self, password: str) -> bool:
        return encode(password) == self.password
    

