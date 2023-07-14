import uuid

import pytest

from auth_service.entities import encode
from auth_service.entities.user import User
from auth_service.usecases.create_user import CreateUserUsecase
from tests import factories as fty


@pytest.fixture
def uuid_patch(mocker):
    return mocker.patch(
        "auth_service.usecases.create_user.uuid", return_value=mocker.Mock(spec=uuid)
    )


@pytest.mark.asyncio
async def test_save_user(user_store, uuid_patch):
    # given
    uuid = "uuid-123"
    uuid_patch.uuid4.return_value = uuid
    req = fty.CreateUserDataFactory()
    expected_user = User(
        id=uuid,
        email=req.email,
        password=encode(req.password),
        name=req.name,
        last_name=req.last_name,
        two_factor_auth_enabled=req.two_factor_auth_enabled,
    )
    user_store.save.return_value = expected_user
    # when
    res = await CreateUserUsecase(user_store=user_store).execute(req=req)
    # then
    assert res == expected_user
    user_store.save.assert_called_once_with(user=expected_user)
