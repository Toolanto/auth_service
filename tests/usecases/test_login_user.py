import uuid
import jwt
import pytest

from auth_service.entities.user import User
from auth_service.usecases.login_user import LoginUserRes, LoginUserUsecase
from tests import factories as fty
from auth_service.entities import encode

@pytest.fixture
def jwt_patch(mocker):
    return mocker.patch("auth_service.usecases.login_user.jwt", return_value=mocker.Mock(spec=jwt))


@pytest.fixture
def uuid_patch(mocker):
    return mocker.patch("auth_service.usecases.login_user.uuid", return_value=mocker.Mock(spec=uuid))


@pytest.fixture
def uc(user_store, otp_store, email_gateway):
    return LoginUserUsecase(
        user_store=user_store,
        otp_store=otp_store,
        email_gateway=email_gateway
    )

@pytest.mark.asyncio
async def test_login_user_return_jwt(uc, user_store, otp_store,email_gateway, jwt_patch):
    #given
    req = fty.LoginUserDataFactory()
    user = User(
        email = req.email,
        password= encode(req.password),
        two_factor_auth_enabled= False,
    )
    user_store.get.return_value = user
    jwt_patch.encode.return_value = "token"
    #when
    res = await uc.execute(req=req)
    #then
    assert res ==  LoginUserRes(token = "token")
    user_store.get.assert_called_once_with(email=user.email)
    otp_store.save.assert_not_called()
    email_gateway.send.assert_not_called()

@pytest.mark.asyncio
async def test_login_user_return_session_id(uc, user_store, otp_store,email_gateway, jwt_patch, uuid_patch):
    #given
    req = fty.LoginUserDataFactory()
    user = User(
        email = req.email,
        password= encode(req.password),
        two_factor_auth_enabled= True,
    )
    user_store.get.return_value = user
    uuid_patch.uuid4.return_value = "uuid"
    #when
    res = await uc.execute(req=req)
    #then
    assert res ==  LoginUserRes(session_id = "uuid")
    user_store.get.assert_called_once_with(email=user.email)
    jwt_patch.encode.assert_not_called()
    otp_store.save.assert_called_once()
    email_gateway.send.assert_called_once()