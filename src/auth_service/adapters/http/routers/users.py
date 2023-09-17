from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from auth_service.adapters.http.routers.schemas import UserRes
from auth_service.controller import Controller
from auth_service.dependencies.controller import get_controller
from auth_service.repositories import UserStoreErrors
from auth_service.usecases.create_user import CreateUserData

router = APIRouter()


@router.post("/users", response_model=UserRes, status_code=201)
async def register(
    req: CreateUserData, controller: Annotated[Controller, Depends(get_controller)]
) -> UserRes:
    """Endpoint to register a user"""
    try:
        user = await controller.create_user(req=req)
        return UserRes(**user.model_dump())
    except UserStoreErrors.AlreadyExists as err:
        raise HTTPException(status_code=409, detail=f"{err}")
