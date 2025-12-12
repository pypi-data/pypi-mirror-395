import ssl
from typing import NamedTuple, Optional, Any

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

from email.header import Header
from email.utils import formatdate
from smtplib import SMTP, SMTPConnectError, SMTPAuthenticationError, SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError, SMTPException

from robertcommonbasic.basic.os.file import check_file_exist, get_file_name


class EmailConfig(NamedTuple):
    HOST: str
    PORT: int
    USER: str
    PSW: str
    FROM: str
    TIMEOUT: int = 60
    ENABLE_SSL: bool = True


class EmailAccessor:

    def __init__(self, config: EmailConfig):
        self.config = config

    def _send(self, recipients: str, smtp_msg: Any):
        try:
            with SMTP(self.config.HOST, self.config.PORT, self.config.TIMEOUT) as smtp_handle:
                if self.config.ENABLE_SSL is True:
                    # python 3.10/3.11新版本若出现ssl握手失败,请使用下列方式处理
                    ctxt = ssl.create_default_context()
                    ctxt.set_ciphers('DEFAULT')
                    smtp_handle.starttls(context=ctxt)
                smtp_handle.login(self.config.USER, self.config.PSW)
                smtp_handle.sendmail(self.config.FROM, recipients.split(','), smtp_msg.as_string())
                smtp_handle.quit()
            return True
        except SMTPConnectError as e:
            raise Exception(f"connect error({e.__str__()})")
        except SMTPAuthenticationError as e:
            raise Exception(f"auth error({e.__str__()})")
        except (SMTPSenderRefused, SMTPRecipientsRefused) as e:
            raise Exception(f"send or recv error({e.__str__()})")
        except Exception as e:
            raise e

    def crate_email(self, sender: str, recipients: str, datas: list, title: str = '', ccs: str = ''):
        smtp_msg = MIMEMultipart('alternative')
        smtp_msg['From'] = sender
        smtp_msg['To'] = recipients
        if isinstance(ccs, str) and len(ccs) > 0:
            smtp_msg['Cc'] = ccs  # 接收者账号列表
        if isinstance(title, str) and len(title) > 0:
            smtp_msg['Subject'] = Header(title, 'utf-8')
        smtp_msg['Date'] = formatdate(localtime=True)

        text_content = ''
        for data in datas:
            if isinstance(data, tuple) and len(data) == 2:
                if data[0] == 'html':
                    text_content = f"{text_content}<p>{data[1]}</p>"
                elif data[0] == 'text':
                    text_content = f"{text_content}<p>{data[1]}</p>"
                elif data[0] == 'image':
                    if check_file_exist(data[1]):
                        smtp_msg.attach(MIMEImage(open(data[1], 'rb').read()))
                elif data[0] == 'file':
                    if check_file_exist(data[1]):
                        file = MIMEApplication(open(data[1], 'rb').read())
                        file.add_header('Content-Disposition', 'attachment', filename=get_file_name(data[1]))
                        smtp_msg.attach(file)
                elif data[0] == 'table':
                    if isinstance(data[1], list):
                        text_content = f"{text_content}<p>{self.generate_table_html(data[1])}</p>"
        if len(text_content) > 0:
            smtp_msg.attach(MIMEText(text_content, 'HTML', 'utf-8'))
        return smtp_msg

    def send_email(self, recipients: str, datas: list, title: str = '', ccs: str = ''):
        return self._send(recipients, self.crate_email(self.config.FROM, recipients, datas, title, ccs))

    def generate_table_html(self, values: list) -> str:
        body = ''
        for vs in values:
            body = f'{body}<tr>'
            for v in vs:
                body = f"""{body}<td text-align="center"{f' style="{v[1]}"' if isinstance(v, tuple) else ''}>{v[0] if isinstance(v, tuple) else v}</td>"""
            body = f'{body}</tr>'
        body = f'<table border="1" cellspacing="0" cellpadding="7" text-align="center">{body}</table>'
        return body
