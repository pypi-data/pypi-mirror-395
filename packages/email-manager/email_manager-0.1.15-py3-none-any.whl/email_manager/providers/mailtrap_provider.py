from email import encoders
from email.mime.base import MIMEBase
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_manager.providers.base import BaseEmailProvider
import os

class MailtrapProvider(BaseEmailProvider):
    def __init__(self, mailtrap_params: dict, config):
        self.host = mailtrap_params["host"]
        self.port = mailtrap_params["port"]
        self.password = mailtrap_params["psw"]
        self.from_email = mailtrap_params["from_email"]
        self.timeout = config.timeout

    def send_email(self, to: str, subject: str, body: str, reply_to: str = None, bcc: list = None, attachments: list = None, **kwargs) -> bool:
        try:
            to = [i.strip() for i in to.split(',')] if isinstance(to, str) else to
            bcc = bcc or []
            attachments = attachments or []

            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = ", ".join(to)
            msg["Subject"] = subject
            msg['reply-to'] = reply_to
            msg['Bcc'] = ", ".join(bcc)

            msg.attach(MIMEText(body, "html"))

            for attachment in attachments:
                if not os.path.isfile(attachment):
                    raise FileNotFoundError(f"Archivo no encontrado: {attachment}")
                part = MIMEBase('application', 'octet-stream')
                with open(attachment, 'rb') as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                msg.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as server:
                server.starttls(context=context)
                server.login(self.from_email, self.password)
                recipients = to + bcc
                server.sendmail(self.from_email, recipients, msg.as_string())

            return True
        except Exception as e:
            self._handle_error(e)
            


    def send_bulk_email(self, recipients: list, subject: str, body: str) -> dict:
        return {recipient: self.send_email(recipient, subject, body) for recipient in recipients}

    def _handle_error(self, error: Exception):
        raise RuntimeError(f"[Mailtrap Error] {error}")

    def get_provider_name(self) -> str:
        return "MailtrapProvider"