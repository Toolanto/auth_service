from typing import Annotated

from fastapi import Depends

from auth_service.controller import Controller
from auth_service.dependencies.email import get_email_gateway
from auth_service.dependencies.repositories import get_otp_store, get_user_store
from auth_service.repositories import OtpStore, UserStore


def get_controller(
    user_store: Annotated[UserStore, Depends(get_user_store)],
    otp_store: Annotated[OtpStore, Depends(get_otp_store)],
    email_gateway: Annotated[OtpStore, Depends(get_email_gateway)],
):
    return Controller(
        user_store=user_store,
        otp_store=otp_store,
        email_gateway=email_gateway,
    )
