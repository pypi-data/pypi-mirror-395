from typing import List

from .ports import MailSender


class BrevoSmtpMailSender(MailSender):
    """
    使用 SMTP 协议发送邮件的实现类。
    """

    def __init__(self,
                 username: str,
                 password: str,
                 from_addr: str) -> None:
        """

        :param username: Login xxxxxx@smtp-brevo.com
        :param password: SMTP key value
        :param from_addr: Sender
        """
        self._smtp = SmtpMailSender(
            "smtp-relay.brevo.com",
            587,
            username,
            password
        )
        self.username = username
        self.password = password
        self.from_addr = from_addr

    def set_from_addr(self, from_addr: str) -> None:
        self.from_addr = from_addr

    def send(self, to_addrs: str | List[str], subject: str, body: str) -> None:
        self._smtp.send(self.from_addr, to_addrs, subject, body)

    async def async_send(self, to_addrs: str | List[str], subject: str, body: str) -> None:
        await self._smtp.async_send(self.from_addr, to_addrs, subject, body)
