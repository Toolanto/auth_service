from typing import Optional

from pydantic import BaseModel, Field


class UserRes(BaseModel):
    email: str = Field(..., description="The user email.")
    name: Optional[str] = Field(None, description="The user name.")
    last_name: Optional[str] = Field(None, description="The user last name.")
    two_factor_auth_enabled: bool = Field(..., description="The 2FA option.")


class Authentication(BaseModel):
    token: Optional[str] = Field(None, description="The JWT token.")
    otp_id: Optional[str] = Field(
        None,
        description=(
            "The OTP id. This field will be returned "
            "during the login process only for users with 2FA enabled."
        ),
    )
