import uuid

import pytest

from auth_service.entities import encode
from auth_service.entities.user import User
from tests import factories as fty


@pytest.fixture
def uuid_patch(mocker):
    return mocker.patch(
        "auth_service.usecases.create_user.uuid", return_value=mocker.Mock(spec=uuid)
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user(controller, uuid_patch):
    # given
    uuid = "uuid-123"
    uuid_patch.uuid4.return_value = uuid
    req = fty.CreateUserDataFactory()
    # when
    res = await controller.create_user(req=req)
    # then
    expected_user = User(
        id=uuid,
        email=req.email,
        password=encode(req.password),
        name=req.name,
        last_name=req.last_name,
        two_factor_auth_enabled=req.two_factor_auth_enabled,
    )
    assert res == expected_user
