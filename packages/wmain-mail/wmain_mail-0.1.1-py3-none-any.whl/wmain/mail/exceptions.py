class MailException(Exception):
    """
    邮件发送异常
    """
    pass


class BrevoNoCustomerException(MailException):
    """
    用户不存在
    """
    pass


class NotChooseTls(MailException):
    """
    没有指定tls连接方式
    """
    pass
