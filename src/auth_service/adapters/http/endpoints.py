from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from auth_service.controller import Controller
from auth_service.repositories import UserStoreErrors
from auth_service.usecases.create_user import CreateUserData
from auth_service.usecases.login_user import LoginUserData, LoginUserErrors
from auth_service.usecases.otp_login import OtpLoginData, OtpLoginErrors


class Responses:
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


def create_app(controller: Controller):
    app = FastAPI(title="Auth Service")

    @app.post("/users", response_model=Responses.UserRes, status_code=201)
    async def register(req: CreateUserData) -> Responses.UserRes:
        """Endpoint to register a user"""
        try:
            user = await controller.create_user(req=req)
            return Responses.UserRes(**user.model_dump())
        except UserStoreErrors.AlreadyExists as err:
            raise HTTPException(status_code=409, detail=f"{err}")

    @app.post("/login", response_model=Responses.Authentication, status_code=200)
    async def login(req: LoginUserData) -> Responses.Authentication:
        """
        Endpoint to authenticate a user.
        If 2FA is enabled: an email is sent and the response contains the otp_id to verify the OTP.
        Otherwise the JWT token is returned.
        """
        try:
            res = await controller.login_user(req=req)
            return Responses.Authentication(token=res.token, otp_id=res.otp_id)
        except LoginUserErrors.InvalidCredentials as err:
            raise HTTPException(status_code=401, detail=f"{err}")
        except UserStoreErrors.NotFoundError as err:
            raise HTTPException(status_code=422, detail=f"{err}")

    @app.post("/otp-login", response_model=Responses.Authentication, status_code=200)
    async def otp_login(req: OtpLoginData) -> Responses.Authentication:
        """
        Endpoint to get a token by an OTP.
        Given an OTP ID and the OTP code checks if they are correct and return a JWT token.
        OTP are valid only for 5 minutes.
        """
        try:
            token = await controller.otp_login(req=req)
            return Responses.Authentication(token=token)
        except OtpLoginErrors.InvalidCredentials as err:
            raise HTTPException(status_code=401, detail=f"{err}")
        except UserStoreErrors.NotFoundError as err:
            raise HTTPException(status_code=422, detail=f"{err}")

    return app
