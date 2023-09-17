from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from auth_service.adapters.http.routers.schemas import Authentication
from auth_service.controller import Controller
from auth_service.dependencies.controller import get_controller
from auth_service.repositories import UserStoreErrors
from auth_service.usecases.login_user import LoginUserData, LoginUserErrors
from auth_service.usecases.otp_login import OtpLoginData, OtpLoginErrors

router = APIRouter()


@router.post("/login", response_model=Authentication, status_code=200)
async def login(
    req: LoginUserData, controller: Annotated[Controller, Depends(get_controller)]
) -> Authentication:
    """
    Endpoint to authenticate a user.
    If 2FA is enabled: an email is sent and the response contains the otp_id to verify the OTP.
    Otherwise the JWT token is returned.
    """
    try:
        res = await controller.login_user(req=req)
        return Authentication(token=res.token, otp_id=res.otp_id)
    except LoginUserErrors.InvalidCredentials as err:
        raise HTTPException(status_code=401, detail=f"{err}")
    except UserStoreErrors.NotFoundError as err:
        raise HTTPException(status_code=422, detail=f"{err}")


@router.post("/otp-login", response_model=Authentication, status_code=200)
async def otp_login(
    req: OtpLoginData, controller: Annotated[Controller, Depends(get_controller)]
) -> Authentication:
    """
    Endpoint to get a token by an OTP.
    Given an OTP ID and the OTP code checks if they are correct and return a JWT token.
    OTP are valid only for 5 minutes.
    """
    try:
        token = await controller.otp_login(req=req)
        return Authentication(token=token)
    except OtpLoginErrors.InvalidCredentials as err:
        raise HTTPException(status_code=401, detail=f"{err}")
    except UserStoreErrors.NotFoundError as err:
        raise HTTPException(status_code=422, detail=f"{err}")
