from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_manager.providers.base import BaseEmailProvider
from email import encoders


class SMTPProvider(BaseEmailProvider):
    def __init__(self, smtp_params: dict, config):
        self.host = smtp_params.get("host")
        self.port = smtp_params.get("port")
        self.from_email = smtp_params.get("from_email")
        self.password = smtp_params.get("psw")
        self.use_tls = smtp_params.get("use_tls")
        self.timeout = config.timeout

    def send_email(self, to: str, subject: str, body: str, reply_to:str, bcc: list = None, attachments: list = None, **kwargs) -> bool:
        try:
            message, recipients = self._create_message(to, subject, body, reply_to, bcc, attachments)
            smtp = self._connect_smtp()
            smtp.send_message(message, to_addrs=recipients)
            smtp.quit()
            print('El correo fue enviado mediante el fallback SMTP')
        except Exception as e:
            self._handle_error(e)
            

    def send_bulk_email(self, recipients: list, subject: str, body: str, bcc: list = None, attachments: list = None) -> dict:
        return {
            recipient: self.send_email(recipient, subject, body, bcc=bcc, attachments=attachments)
            for recipient in recipients
        }


    def _create_message(self, to: str, subject: str, body: str, reply_to: str = None, bcc: list = None, attachments: list = None) -> tuple:
        bcc = bcc or []
        attachments = attachments or []

        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = ', '.join(to) if isinstance(to, list) else to
        msg["Subject"] = subject
        msg['reply-to'] = reply_to
        msg['Bcc'] = ", ".join(bcc)
        
        msg.attach(MIMEText(body, "html"))

        for attachment in attachments:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment, 'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment.split('/')[-1])
            msg.attach(part)

        recipients = [to] if isinstance(to, str) else to
        recipients += bcc
        return msg, recipients


    def _connect_smtp(self) -> smtplib.SMTP:
        try:
            smtp = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                smtp.starttls()
            smtp.login(self.from_email, self.password)
            return smtp
        except Exception as error:
            self._handle_error(error)
            
            
    def _handle_error(self, error: Exception):
        raise RuntimeError(f"[SMTP Error] {error}")

    def get_provider_name(self) -> str:
        return "SMTPProvider"