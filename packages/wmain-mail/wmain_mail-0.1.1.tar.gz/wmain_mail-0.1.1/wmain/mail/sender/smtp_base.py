import asyncio
from smtplib import SMTP_SSL, SMTP

import aiosmtplib

from wmain.mail.email import MailContent, MailHeader, build_email_message


class SmtpMailSender:
    """
    使用 SMTP 协议发送邮件的实现类。
    """

    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 use_tls: bool = None,
                 start_tls: bool = None) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        if port == 465:
            self.use_tls = True if use_tls is None else use_tls
            self.start_tls = False if start_tls is None else start_tls
        elif port == 587:
            self.use_tls = False if use_tls is None else use_tls
            self.start_tls = True if start_tls is None else start_tls
        elif port == 25:
            self.use_tls = False if use_tls is None else use_tls
            self.start_tls = False if start_tls is None else start_tls
        else:
            if self.use_tls is None or self.start_tls is None:
                raise ValueError("请指定使用 TLS 或 STARTTLS 协议")
            self.use_tls = use_tls
            self.start_tls = start_tls

    def send(self, header: MailHeader, content: MailContent):
        if self.use_tls:
            smtp = SMTP_SSL(self.host, self.port)
        else:
            smtp = SMTP(self.host, self.port)
            if self.start_tls:
                smtp.starttls()
        smtp.login(self.username, self.password)
        smtp.sendmail(*build_email_message(header, content))

    async def async_send(
            self,
            header: MailHeader,
            content: MailContent,
            timeout: int = 10
    ):
        smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=self.start_tls,
                use_tls=self.use_tls,
                timeout=timeout
        )
        await smtp.connect()
        email = build_email_message(header, content)
        print(email)
        await smtp.sendmail(email[0], email[1], email[2])


async def test_async():
    smtp = SmtpMailSender(
        host="mail.terraria.center",
        port=465,
        username="notifications@terraria.center",
        password="5438asdwASDW.",
    )

    header = MailHeader(
        display_name="泰拉瑞亚服务器",
        from_addr="notifications@terraria.center",
        to_addrs=["<heiwynhhh@gmail.com>"],
        subject="退订链接",
        list_unsubscribe="<http://sub.terraria.center>",
        list_unsubscribe_post="List-Unsubscribe=One-Click",
        precedence="bulk",
    )

    content = MailContent(
        html="""
        <html>
        <body>
        <p>
           验证码：<span style="color: red;">123456</span>
        </p>
        </body>
        </html>
        """
    )
    await smtp.async_send(header, content)


if __name__ == "__main__":
    asyncio.run(test_async())
