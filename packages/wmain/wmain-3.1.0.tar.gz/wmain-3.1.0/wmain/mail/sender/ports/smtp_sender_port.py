from typing import Protocol, List


class MailSender(Protocol):

    def send(self, to_addrs: str | List[str], subject: str, body: str) -> None:
        ...

    async def async_send(self, to_addrs: str | List[str], subject: str, body: str) -> None:
        ...
