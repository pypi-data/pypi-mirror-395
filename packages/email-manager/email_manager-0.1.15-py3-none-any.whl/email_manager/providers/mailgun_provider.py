import requests
from email_manager.providers.base import BaseEmailProvider
from email_manager.providers.exceptions import EmailSendError

SEND_MESSAGE_MAILGUN = "https://api.mailgun.net/v3/{domain}"


class MailgunProvider(BaseEmailProvider):
    def __init__(self, mailgun_params: dict, config):
        
        self.api_key = mailgun_params.get("api_key")
        self.domain = mailgun_params.get("domain")
        self.base_url = SEND_MESSAGE_MAILGUN.format(domain=self.domain)
        self.from_email = mailgun_params.get("from_email")
        self.timeout = config.timeout
        self.max_retries = config.max_retries

    def send_email(self, to: str, subject: str, body: str, reply_to: str, bcc: list =None, attachments: list = None, **kwargs) -> bool:
        payload = self._build_mailgun_payload(to, subject, body, reply_to, bcc, **kwargs)
        try:
            response = self._make_request("/messages", payload, attachments)
            if not self._validate_response(response):
                raise EmailSendError(self.get_provider_name(), f"Respuesta inválida: {response.status_code}")
            return True
        except Exception as e:
            raise EmailSendError(self.get_provider_name(), str(e))


    def send_bulk_email(self, recipients: list, subject: str, body: str) -> dict:
        results = {}
        for recipient in recipients:
            results[recipient] = self.send_email(recipient, subject, body)
        return results

    def _build_mailgun_payload(self, to: str, subject: str, body: str, reply_to: str, bcc: list = None, **kwargs) -> dict:
        return {
            "from": self.from_email,
            "to": to,
            "subject": subject,
            "html": body,
            "h:Reply-To":reply_to,
            "bcc":bcc,
        }

    def _make_request(self, endpoint: str, data: dict, attachments: list):
        files = []
        file_handles = []
        try:
            if attachments:
                for attachment in attachments:
                    f = open(attachment, 'rb')
                    file_handles.append(f)
                    files.append(('attachment', f))
            response = requests.post(
                f"{self.base_url}{endpoint}",
                auth=("api", self.api_key),
                data=data,
                files=files if files else None,
                timeout=self.timeout
            )
            return response
        finally:
            for f in file_handles:
                f.close()


    def _validate_response(self, response) -> bool:
        return response.status_code == 200

    def _handle_error(self, error: Exception):
        raise RuntimeError(f"[Mailgun Error] {error}")

    def get_provider_name(self) -> str:
        return "MailgunProvider"