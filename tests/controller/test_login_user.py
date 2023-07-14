import uuid

import jwt
import pytest

from auth_service.entities import encode
from auth_service.usecases.login_user import LoginUserData, LoginUserRes
from tests import factories as fty


@pytest.fixture
def jwt_patch(mocker):
    return mocker.patch("auth_service.usecases.jwt", return_value=mocker.Mock(spec=jwt))


@pytest.fixture
def uuid_patch(mocker):
    return mocker.patch("auth_service.usecases.uuid", return_value=mocker.Mock(spec=uuid))


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_user_returns_jwt(controller, user_store, jwt_patch):
    # given
    password = "password123"
    user = fty.UserFactory(password=encode(password))
    await user_store.save(user=user)
    jwt_patch.encode.return_value = "token"
    # when
    res = await controller.login_user(req=LoginUserData(email=user.email, password=password))
    # then
    assert res == LoginUserRes(token="token")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_user_returns_otp_id(controller, user_store, uuid_patch):
    # given
    password = "password123"
    user = fty.UserFactory(password=encode(password), two_factor_auth_enabled=True)
    await user_store.save(user=user)
    uuid_patch.uuid4.return_value = "uuid"
    # when
    res = await controller.login_user(req=LoginUserData(email=user.email, password=password))
    # then
    assert res == LoginUserRes(otp_id="uuid")
