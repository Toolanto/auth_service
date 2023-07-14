from datetime import datetime, timezone, timedelta
import jwt
import pytest
from auth_service.entities.store import OtpStoreErrors

from auth_service.usecases.otp_login import OtpLoginErrors, OtpLoginUsecase
from tests import factories as fty

@pytest.fixture
def jwt_patch(mocker):
    return mocker.patch("auth_service.usecases.otp_login.jwt", return_value=mocker.Mock(spec=jwt))

@pytest.fixture
def datetime_patch(mocker):
    return mocker.patch("auth_service.usecases.otp_login.datetime", return_value=mocker.Mock(spec=datetime))


@pytest.fixture
def uc(user_store, otp_store):
    return OtpLoginUsecase(
        user_store=user_store,
        otp_store=otp_store,
    )

@pytest.mark.asyncio
async def test_otp_login_return_jwt(uc, user_store, otp_store, jwt_patch):
    #given
    req = fty.OtpLoginDataFactory()
    otp = fty.OtpFactory(session_id=req.session_id, value=req.otp)
    user = fty.UserFactory(
        email = otp.email,
        two_factor_auth_enabled= True,
    )
    otp_store.get.return_value = otp 
    user_store.get.return_value = user
    jwt_patch.encode.return_value = "token"
    #when
    res = await uc.execute(req=req)
    #then
    assert res ==  "token"
    otp_store.get.assert_called_once_with(session_id=req.session_id)
    user_store.get.assert_called_once_with(email=otp.email)
    otp_store.mark_checked.assert_called_once_with(otp=otp)


@pytest.mark.asyncio
async def test_otp_not_found(uc, user_store, otp_store):
    #given
    req = fty.OtpLoginDataFactory()
    otp_store.get.side_effect = OtpStoreErrors.NotFoundError 
    #when
    with pytest.raises(OtpLoginErrors.InvalidCredentials):
        await uc.execute(req=req)
    #then
    otp_store.get.assert_called_once_with(session_id=req.session_id)
    user_store.get.assert_not_called()
    otp_store.mark_checked.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "req,otp,current_time",
        [
            pytest.param(
                fty.OtpLoginDataFactory(session_id="s-123", otp="otp-123"),
                fty.OtpFactory(session_id="s-123", value="otp-124"),
                datetime.now(tz=timezone.utc),
                id="invalid value"
            ),
            pytest.param(
                fty.OtpLoginDataFactory(session_id="s-123", otp="otp-123"),
                fty.OtpFactory(session_id="s-123", value="otp-122"),
                datetime.now(tz=timezone.utc) - timedelta(days=1),
                id="expired"
            ),
            pytest.param(
                fty.OtpLoginDataFactory(session_id="s-123", otp="otp-123"),
                fty.OtpFactory(session_id="s-123", value="otp-122", checked=True),
                datetime.now(tz=timezone.utc),
                id="already checked"
            )
        ]
    
)
async def test_otp_login_with_invalid_otp(uc, user_store, otp_store, datetime_patch, req,otp,current_time):
    #given
    otp_store.get.return_value = otp 
    datetime_patch.now.return_value = current_time
    #when
    with pytest.raises(OtpLoginErrors.InvalidCredentials):
        await uc.execute(req=req)
    #then
    otp_store.get.assert_called_once_with(session_id=req.session_id)
    user_store.get.assert_not_called()
    otp_store.mark_checked.assert_not_called()


