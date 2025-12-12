class EmailConfig:
    def __init__(
        self,
        fallback: bool,
        provider_type: str,
        timeout: int = 10,
        max_retries: int = 3,
        mailgun_params: dict = None,
        smtp_params: dict = None,
        mailtrap_params: dict = None,
    ):
        self.fallback = fallback
        self.provider_type = provider_type.lower()
        self.timeout = timeout
        self.max_retries = max_retries
        self.mailgun_params = mailgun_params or {}
        self.smtp_params = smtp_params or {}
        self.mailtrap_params = mailtrap_params or {}
