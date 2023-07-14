import pytest
from auth_service.adapters.email_gateway import  FakeEmailGateway
from auth_service.adapters.otp_store import InMemoryOtpStore, InMemoryOtpStoreConf

from auth_service.adapters.user_store import InMemoryUserStore, InMemoryUserStoreConf
from auth_service.controller import Controller

WHITE_LIST = ["test@test.it"]
FROM_ADDRESS = "from@test.it"

@pytest.fixture
def user_file(tmp_path):
    user_file = (tmp_path / "users.jsonl")
    user_file.touch(exist_ok= True)
    return user_file

@pytest.fixture
def user_store(user_file):
    conf = InMemoryUserStoreConf(
        user_file= user_file
    )
    return InMemoryUserStore(config=conf)

@pytest.fixture
def otp_file(tmp_path):
    otp_file = (tmp_path / "users.jsonl")
    otp_file.touch(exist_ok= True)
    return otp_file

@pytest.fixture
def otp_store(otp_file):
    conf = InMemoryOtpStoreConf(
        otp_file= otp_file
    )
    return InMemoryOtpStore(config=conf)

@pytest.fixture
def email_gateway():
    return FakeEmailGateway()

@pytest.fixture
def controller(user_store, otp_store, email_gateway):
    return Controller(user_store=user_store, otp_store=otp_store,email_gateway=email_gateway)
