class EmailSendError(Exception):
    def __init__(self, provider_name: str, message: str):
        super().__init__(f"[{provider_name}] {message}")
        self.provider_name = provider_name
