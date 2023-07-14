from datetime import datetime, timedelta, timezone

import pytest
from tests import factories as fty

def test_otp_is_valid():
    #given
    value = "12345"
    otp = fty.OtpFactory(value=value)
    now = datetime.now(tz=timezone.utc)
    #when
    res = otp.is_valid_otp(value, now)
    #then
    assert res is True

@pytest.mark.parametrize("otp_value,otp_checked,value,current_time",[
    pytest.param("12345", False, "00000", datetime.now(tz=timezone.utc)),
    pytest.param("12345", True, "12345", datetime.now(tz=timezone.utc)),
    pytest.param("12345", False, "12345", datetime.now(tz=timezone.utc) + timedelta(days=1)),
])
def test_is_invalid(otp_value,otp_checked,value,current_time):
    #given
    otp = fty.OtpFactory(value=otp_value, checked=otp_checked)
    #when
    res = otp.is_valid_otp(value, current_time)
    #then
    assert res is False