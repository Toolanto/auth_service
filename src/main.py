import logging

from auth_service.adapters import endpoints as ep
from auth_service.adapters.email_gateway import FakeEmailGateway
from auth_service.adapters.otp_store import InMemoryOtpStore, InMemoryOtpStoreConf
from auth_service.adapters.user_store import InMemoryUserStore, InMemoryUserStoreConf
from auth_service.config import load
from auth_service.controller import Controller

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s  %(message)s",
    handlers=[logging.StreamHandler()],
)
configs = load()
controller = Controller(
    user_store=InMemoryUserStore(config=InMemoryUserStoreConf(**configs.user_store.model_dump())),
    otp_store=InMemoryOtpStore(config=InMemoryOtpStoreConf(**configs.otp_store.model_dump())),
    email_gateway=FakeEmailGateway(),
)
web = ep.create_app(controller=controller)
