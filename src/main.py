import logging

from auth_service.adapters import endpoints as ep
from auth_service.adapters.email_gateway import FakeEmailGateway
from auth_service.adapters.repositories.repos import (
    DbConfig,
    PostgresOtpStore,
    PostgresUserStore,
)
from auth_service.config import load
from auth_service.controller import Controller

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s  %(message)s",
    handlers=[logging.StreamHandler()],
)
configs = load()
controller = Controller(
    user_store=PostgresUserStore(config=DbConfig(**configs.db_config.model_dump())),
    otp_store=PostgresOtpStore(config=DbConfig(**configs.db_config.model_dump())),
    email_gateway=FakeEmailGateway(),
)
web = ep.create_app(controller=controller)
