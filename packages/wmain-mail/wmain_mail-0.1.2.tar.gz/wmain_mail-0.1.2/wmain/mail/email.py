import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, parseaddr, formatdate, make_msgid
from typing import Dict

from typing import List, Optional, Union


class MailHeader:
    """
    Represents email header information.
    Covers common and standard fields according to RFC 5322, RFC 2045, RFC 2369, RFC 8058.
    """

    def __init__(
            self,
            # Basic information
            display_name: Optional[str] = None,  # Display name of sender
            from_addr: Optional[str] = None,  # Sender email address
            to_addrs: Optional[Union[str, List[str]]] = None,  # Recipient(s)
            cc_addrs: Optional[Union[str, List[str]]] = None,  # CC recipient(s)
            bcc_addrs: Optional[Union[str, List[str]]] = None,  # BCC recipient(s), not displayed in headers
            subject: Optional[str] = None,  # Email subject
            reply_to: Optional[Union[str, List[str]]] = None,  # Reply-to address
            date: Optional[str] = None,  # Email sending date, RFC 5322 format
            message_id: Optional[str] = None,  # Unique email ID, RFC 5322

            # Advanced / threading
            sender: Optional[str] = None,  # Sender when acting as agent
            in_reply_to: Optional[str] = None,  # References previous email Message-ID
            references: Optional[List[str]] = None,  # List of referenced Message-IDs
            mime_version: str = "1.0",  # MIME version, usually 1.0
            content_type: Optional[str] = None,  # e.g. text/plain; charset="utf-8" or multipart/mixed
            content_transfer_encoding: Optional[str] = None,  # base64, 7bit, 8bit

            # List-Unsubscribe (anti-spam)
            list_unsubscribe: Optional[str] = None,  # URL or mailto link
            list_unsubscribe_post: Optional[str] = None,  # POST method for unsubscribe

            # Optional corporate / marketing headers
            precedence: Optional[str] = None,  # bulk, list, junk
            auto_submitted: Optional[str] = None,  # auto-generated, auto-replied
            priority: Optional[str] = None,  # high, normal, low
            importance: Optional[str] = None,  # high, normal, low

            # Custom headers
            custom_headers: Optional[dict] = None  # any additional headers
    ):
        # Basic
        self.display_name = display_name
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.cc_addrs = cc_addrs
        self.bcc_addrs = bcc_addrs
        self.subject = subject
        self.reply_to = reply_to
        self.date = date
        self.message_id = message_id

        # Threading / advanced
        self.sender = sender
        self.in_reply_to = in_reply_to
        self.references = references or []
        self.mime_version = mime_version
        self.content_type = content_type
        self.content_transfer_encoding = content_transfer_encoding

        # List-Unsubscribe / anti-spam
        self.list_unsubscribe = list_unsubscribe
        self.list_unsubscribe_post = list_unsubscribe_post

        # Optional headers
        self.precedence = precedence
        self.auto_submitted = auto_submitted
        self.priority = priority
        self.importance = importance

        # Custom headers
        self.custom_headers = custom_headers or {}

    def to_dict(self) -> Dict[str, str]:
        """
        Convert MailHeader instance to a dictionary suitable for MIMEMultipart.
        Automatically handles encoding, display name, Date, Message-ID, etc.
        """
        headers: Dict[str, str] = {}

        # From
        if self.from_addr:
            display_name = str(Header(self.display_name, 'utf-8')) if self.display_name else ""
            headers['From'] = formataddr((display_name, self.from_addr))

        # To
        if self.to_addrs:
            headers['To'] = ", ".join(self.to_addrs) if isinstance(self.to_addrs, list) else self.to_addrs

        # CC
        if self.cc_addrs:
            headers['Cc'] = ", ".join(self.cc_addrs) if isinstance(self.cc_addrs, list) else self.cc_addrs

        # BCC is not included in headers, handled in sending function

        # Subject
        if self.subject:
            headers['Subject'] = str(Header(self.subject, 'utf-8'))

        # Reply-To
        if self.reply_to:
            headers['Reply-To'] = ", ".join(self.reply_to) if isinstance(self.reply_to, list) else self.reply_to

        # Sender
        if self.sender:
            headers['Sender'] = self.sender

        # Date
        headers['Date'] = self.date or formatdate(localtime=True)

        # Message-ID
        headers['Message-ID'] = self.message_id or make_msgid(domain=self.sender)

        # Threading
        if self.in_reply_to:
            headers['In-Reply-To'] = self.in_reply_to
        if self.references:
            headers['References'] = " ".join(self.references)

        # MIME / content
        headers['MIME-Version'] = self.mime_version
        if self.content_type:
            headers['Content-Type'] = self.content_type
        if self.content_transfer_encoding:
            headers['Content-Transfer-Encoding'] = self.content_transfer_encoding

        # Anti-spam / unsubscribe
        if self.list_unsubscribe:
            headers['List-Unsubscribe'] = self.list_unsubscribe
        if self.list_unsubscribe_post:
            headers['List-Unsubscribe-Post'] = self.list_unsubscribe_post
        if self.precedence:
            headers['Precedence'] = self.precedence
        if self.auto_submitted:
            headers['Auto-Submitted'] = self.auto_submitted
        if self.priority:
            headers['Priority'] = self.priority
        if self.importance:
            headers['Importance'] = self.importance

        # Custom headers
        for k, v in self.custom_headers.items():
            headers[k] = v

        return headers


class MailContent:
    """
    Represents email content.
    可以自动处理:
    - Plain text
    - HTML
    - Attachments (常规附件)
    - Inline Images (内嵌图片)
    """

    def __init__(
            self,
            text: Optional[str] = None,
            html: Optional[str] = None,
            attachments: Optional[List[Union[str, bytes]]] = None,
            filenames: Optional[List[str]] = None,  # optional custom filenames for bytes attachments
            inline_images: Optional[List[Union[str, bytes]]] = None,  # 新增: 内嵌图片 (文件路径或字节)
            image_cids: Optional[List[str]] = None  # 新增: 内嵌图片的 Content-ID (用于HTML引用)
    ):
        self.text = text
        self.html = html
        self.attachments = attachments or []
        self.filenames = filenames or []
        self.inline_images = inline_images or []
        self.image_cids = image_cids or []

        # 确保 inline_images 和 image_cids 数量匹配
        if self.inline_images and len(self.inline_images) != len(self.image_cids):
            raise ValueError("The number of inline_images must match the number of image_cids.")

    def build(self) -> MIMEMultipart:
        """
        Build MIMEMultipart message automatically.
        根结构: multipart/mixed (用于常规附件)
        混合结构: multipart/related (用于内嵌资源) -> multipart/alternative (用于文本/HTML)
        """
        # Outer container: mixed for regular attachments
        msg_root = MIMEMultipart("mixed")

        # --- 1. related/alternative container (Text, HTML, Inline Images) ---

        # related: 用于处理 HTML 和其内嵌资源
        msg_related = MIMEMultipart("related")
        msg_root.attach(msg_related)

        # alternative: 用于处理 Text 和 HTML (二选一显示)
        if self.text or self.html:
            msg_alt = MIMEMultipart("alternative")
            msg_related.attach(msg_alt)  # 嵌入到 related 中

            if self.text:
                msg_alt.attach(MIMEText(self.text, "plain", "utf-8"))

            # HTML 内容应放在最后，因为它引用了后续的内嵌图片
            if self.html:
                msg_alt.attach(MIMEText(self.html, "html", "utf-8"))

        # --- 2. Inline Images (内嵌图片) ---
        for idx, img_source in enumerate(self.inline_images):
            cid = self.image_cids[idx]

            if isinstance(img_source, str):
                # assume file path
                with open(img_source, "rb") as f:
                    content = f.read()
                img_name = os.path.basename(img_source)
            else:
                # assume bytes content
                content = img_source
                img_name = f"inline_image_{cid}.dat"

            # 确定 MIME 类型，简化处理：假设是常见的 jpeg 或 png
            import imghdr
            img_type = imghdr.what(None, h=content)
            subtype = img_type if img_type in ['png', 'jpeg', 'gif'] else 'octet-stream'

            mime_img = MIMEApplication(content, _subtype=subtype)
            mime_img.add_header("Content-Disposition", "inline", filename=str(Header(img_name, "utf-8")))
            mime_img.add_header("Content-ID", f"<{cid}>")  # 核心：设置 Content-ID
            msg_related.attach(mime_img)

        # --- 3. Regular Attachments (常规附件) ---
        for idx, att in enumerate(self.attachments):
            if isinstance(att, str):
                # assume file path
                with open(att, "rb") as f:
                    content = f.read()
                filename = os.path.basename(att)
            else:
                # assume bytes content
                content = att
                filename = self.filenames[idx] if idx < len(self.filenames) else f"attachment_{idx}"

            mime_att = MIMEApplication(content, _subtype="octet-stream")
            # 核心：设置为 attachment
            mime_att.add_header("Content-Disposition", "attachment", filename=str(Header(filename, "utf-8")))
            msg_root.attach(mime_att)

        return msg_root


def build_email_message(header: MailHeader, content: MailContent) -> tuple[str, list[str], bytes]:
    """
    整合 MailHeader 和 MailContent，构建完整的邮件对象并转换为可发送的字节。

    Args:
        header: MailHeader 实例。
        content: MailContent 实例。

    Returns:
        Dict: 包含 'message_bytes', 'sender', 'recipients' 的字典，
              便于 smtplib.sendmail 调用。
    """

    # 1. 构建 MIME 邮件体
    msg_root = content.build()

    # 2. 获取头部信息
    headers_dict = header.to_dict()

    # 3. 添加头部到邮件对象
    for k, v in headers_dict.items():
        # 排除在 smtplib.sendmail 中单独处理的头部（通常是 From, To, CC, BCC）
        if k not in ['From', 'To', 'Cc']:
            msg_root[k] = v

    # 4. 特殊处理 From, To, CC 头部（通常由 build 的时候处理了，这里为了完整性，确保 From 在）
    # 在 Python 的 email 库中，如果你用 msg_root.as_bytes()，它会自动包含 From/To/Cc。
    # 但为了方便 smtplib.sendmail 获取发件人和收件人列表，我们再提取一次。
    if 'From' in headers_dict:
        msg_root['From'] = headers_dict['From']
    if 'To' in headers_dict:
        msg_root['To'] = headers_dict['To']
    if 'Cc' in headers_dict:
        msg_root['Cc'] = headers_dict['Cc']

    # 5. 准备 smtplib 需要的参数

    # 发件人地址 (Sender)
    if not header.from_addr:
        raise ValueError("From address (from_addr) is required.")

    sender_addr = parseaddr(msg_root['From'])[1]  # 使用 parseaddr 确保只获取邮件地址

    # 收件人列表 (Recipients)
    recipients: List[str] = []

    if header.to_addrs:
        # 使用 formataddr 和 parseaddr 来确保正确解析，这里简化一下：
        to_list = [addr.strip() for addr in (msg_root['To'].split(',') if msg_root.get('To') else [])]
        recipients.extend(to_list)

    if header.cc_addrs:
        cc_list = [addr.strip() for addr in (msg_root['Cc'].split(',') if msg_root.get('Cc') else [])]
        recipients.extend(cc_list)

    if header.bcc_addrs:
        # BCC 必须是 List[str] 或 str
        bcc_list = header.bcc_addrs if isinstance(header.bcc_addrs, list) else [header.bcc_addrs]
        recipients.extend(bcc_list)

    # 6. 转换为可发送的字节
    email_bytes = msg_root.as_bytes()

    return sender_addr, recipients, email_bytes
