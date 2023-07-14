import uuid

import jwt
import pytest

from auth_service.entities.gateway import EmailGateway
from auth_service.entities.store import OtpStore, UserStore


@pytest.fixture
def user_store(mocker):
    return mocker.Mock(spec=UserStore)


@pytest.fixture
def otp_store(mocker):
    return mocker.Mock(spec=OtpStore)


@pytest.fixture
def email_gateway(mocker):
    return mocker.Mock(spec=EmailGateway)


@pytest.fixture
def jwt_patch(mocker):
    return mocker.patch("auth_service.usecases.jwt", return_value=mocker.Mock(spec=jwt))


@pytest.fixture
def uuid_patch(mocker):
    return mocker.patch("auth_service.usecases.uuid", return_value=mocker.Mock(spec=uuid))
