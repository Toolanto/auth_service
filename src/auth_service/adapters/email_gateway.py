import logging
from typing import Any
from pydantic.dataclasses import dataclass

from auth_service.entities.gateway import EmailGateway

@dataclass
class FakeEmailGateway(EmailGateway):

    async def send(
        self, to_recipient: str, subject:str, body:str
    ) -> None:
        logging.info(f"Sent email to: {to_recipient} - subject: {subject} - body: {body}")