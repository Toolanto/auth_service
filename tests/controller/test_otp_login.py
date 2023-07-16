import pytest

from auth_service.usecases.otp_login import OtpLoginData
from tests import factories as fty


@pytest.mark.integration
@pytest.mark.asyncio
async def test_returns_jwt(controller, user_store, otp_store, jwt_patch):
    # given
    user = fty.UserFactory()
    await user_store.save(user=user)
    otp = fty.OtpFactory(user_id=user.id)
    await otp_store.save(otp=otp)
    jwt_patch.encode.return_value = "token"
    # when
    res = await controller.otp_login(req=OtpLoginData(otp_id=otp.id, otp_value=otp.value))
    # then
    assert res == "token"
