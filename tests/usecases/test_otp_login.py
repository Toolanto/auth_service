from datetime import datetime, timedelta, timezone

import pytest

from auth_service.entities.store import OtpStoreErrors
from auth_service.usecases.otp_login import OtpLoginErrors, OtpLoginUsecase
from tests import factories as fty


@pytest.fixture
def datetime_patch(mocker):
    return mocker.patch(
        "auth_service.usecases.otp_login.datetime", return_value=mocker.Mock(spec=datetime)
    )


@pytest.fixture
def uc(user_store, otp_store):
    return OtpLoginUsecase(
        user_store=user_store,
        otp_store=otp_store,
    )


@pytest.mark.asyncio
async def test_otp_login_return_jwt(uc, user_store, otp_store, jwt_patch):
    # given
    req = fty.OtpLoginDataFactory()
    otp = fty.OtpFactory(id=req.otp_id, value=req.otp_value)
    user = fty.UserFactory(
        id=otp.user_id,
        two_factor_auth_enabled=True,
    )
    otp_store.get.return_value = otp
    user_store.get_by_id.return_value = user
    jwt_patch.encode.return_value = "token"
    # when
    res = await uc.execute(req=req)
    # then
    assert res == "token"
    otp_store.get.assert_called_once_with(id=req.otp_id)
    user_store.get_by_id.assert_called_once_with(id=otp.user_id)
    otp_store.mark_checked.assert_called_once_with(otp=otp)


@pytest.mark.asyncio
async def test_otp_not_found(uc, user_store, otp_store):
    # given
    req = fty.OtpLoginDataFactory()
    otp_store.get.side_effect = OtpStoreErrors.NotFoundError
    # when
    with pytest.raises(OtpLoginErrors.InvalidCredentials):
        await uc.execute(req=req)
    # then
    otp_store.get.assert_called_once_with(id=req.otp_id)
    user_store.get_by_id.assert_not_called()
    otp_store.mark_checked.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "req,otp,current_time",
    [
        pytest.param(
            fty.OtpLoginDataFactory(otp_id="id-123", otp="otp-123"),
            fty.OtpFactory(id="id-123", value="otp-124"),
            datetime.now(tz=timezone.utc),
            id="invalid value",
        ),
        pytest.param(
            fty.OtpLoginDataFactory(otp_id="di-123", otp="otp-123"),
            fty.OtpFactory(id="id-123", value="otp-122"),
            datetime.now(tz=timezone.utc) - timedelta(days=1),
            id="expired",
        ),
        pytest.param(
            fty.OtpLoginDataFactory(otp_id="id-123", otp="otp-123"),
            fty.OtpFactory(id="id-123", value="otp-122", checked=True),
            datetime.now(tz=timezone.utc),
            id="already checked",
        ),
    ],
)
async def test_otp_login_with_invalid_otp(
    uc, user_store, otp_store, datetime_patch, req, otp, current_time
):
    # given
    otp_store.get.return_value = otp
    datetime_patch.now.return_value = current_time
    # when
    with pytest.raises(OtpLoginErrors.InvalidCredentials):
        await uc.execute(req=req)
    # then
    otp_store.get.assert_called_once_with(id=req.otp_id)
    user_store.get_by_id.assert_not_called()
    otp_store.mark_checked.assert_not_called()
