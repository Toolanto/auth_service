import jwt
import pytest

from auth_service.adapters.email.email_gateway import FakeEmailGateway
from auth_service.adapters.repositories.repos import PostgresOtpStore, PostgresUserStore
from auth_service.controller import Controller

WHITE_LIST = ["test@test.it"]
FROM_ADDRESS = "from@test.it"


@pytest.fixture
def user_store(db_config):
    return PostgresUserStore(config=db_config)


@pytest.fixture
def otp_store(db_config):
    return PostgresOtpStore(config=db_config)


@pytest.fixture
def email_gateway():
    return FakeEmailGateway()


@pytest.fixture
def controller(user_store, otp_store, email_gateway):
    return Controller(user_store=user_store, otp_store=otp_store, email_gateway=email_gateway)


@pytest.fixture
def jwt_patch(mocker):
    return mocker.patch("auth_service.usecases.jwt", return_value=mocker.Mock(spec=jwt))
