import pytest

from auth_service.entities.user import User
from tests import factories as fty

from auth_service.entities import encode


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user(controller):
    #given
    req = fty.CreateUserDataFactory()
    #when
    res = await controller.create_user(req=req)
    #then
    expected_user = User(
        email = req.email,
        password= encode(req.password),
        name= req.name,
        last_name= req.last_name,
        two_factor_auth_enabled= req.two_factor_auth_enabled,
    )
    assert res == expected_user