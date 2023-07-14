import re
import uuid
from typing import Optional

from pydantic import BaseModel, Field, constr, field_validator

from auth_service.entities import encode
from auth_service.entities.store import UserStore
from auth_service.entities.user import User


class CreateUserData(BaseModel):
    email: str = Field(..., description="The user email")
    password: constr(min_length=8, strip_whitespace=True) = Field(
        ..., description="The user pasword"
    )
    name: constr(min_length=1, strip_whitespace=True) = Field(..., description="The user name")
    last_name: Optional[constr(min_length=1, strip_whitespace=True)] = Field(
        None, description="The user last name"
    )
    two_factor_auth_enabled: Optional[bool] = Field(False, description="Set the 2FA login flow")

    @field_validator("email")
    def email_validation(cls, v):
        regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        if not re.fullmatch(regex, v):
            raise ValueError("Invalid email")
        return v


class CreateUserUsecase(BaseModel):
    user_store: UserStore

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, req: CreateUserData) -> User:
        user = User(
            id=str(uuid.uuid4()),
            email=req.email,
            password=encode(req.password),
            name=req.name,
            last_name=req.last_name,
            two_factor_auth_enabled=req.two_factor_auth_enabled,
        )
        user = await self.user_store.save(user=user)
        return user
