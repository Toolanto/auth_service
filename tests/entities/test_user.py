from auth_service.entities import encode
from tests import factories as fty


def test_encode_password():
    assert encode("test-42") == "dGVzdC00Mg=="


def test_check_correct_password():
    # given
    encoded_pwd = encode("test-42")
    user = fty.UserFactory(password=encoded_pwd)
    # when
    res = user.is_valid_password("test-42")
    # then
    assert res is True


def test_check_invalid_password():
    # given
    user = fty.UserFactory()
    # when
    res = user.is_valid_password("test-42")
    # then
    assert res is False
