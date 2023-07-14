import abc


class EmailGateway(abc.ABC):

    @abc.abstractmethod
    async def send(
        self, to_recipient: str, subject:str, body:str
    ) -> None:
        pass # pragma: no cover
