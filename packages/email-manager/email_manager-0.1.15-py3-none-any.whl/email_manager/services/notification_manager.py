
from email_manager.factory.provider_factory import ProviderFactory
from email_manager.providers.exceptions import EmailSendError

class EmailNotificationManager:
    def __init__(self, config, logger=None,):
        self.logger = logger
        self.config = config
        self.provider_type = config.provider_type.lower()
        self.fallback = config.fallback
            
        if self.provider_type == 'mailtrap':
            self.provider = ProviderFactory.create_provider(config, override="mailtrap")
            self.fallback_provider = None
        else:
            self.provider = ProviderFactory.create_provider(config, override="mailgun")
            self.fallback_provider = ProviderFactory.create_provider(config, override="smtp")

    def send_notification(self, to: str, subject: str, body: str, reply_to, bcc, attachments: list = None) -> bool:
        try:
            
            return self.provider.send_email(to, subject, body, reply_to, bcc, attachments)
        
        except EmailSendError as e:
            print(f"⚠️ Fallback [SMTP] activado por error en {e.provider_name}: {e}")
            try:
                if self.fallback:
                    return self.fallback_provider.send_email(to, subject, body, reply_to, bcc, attachments)
                else:
                    raise RuntimeError("❌ Fallo el envio del correo y Fallback desactivado.")
            except EmailSendError as fallback_error:
                raise RuntimeError("❌ Fallo el envio del correo incluso con Fallback.") from fallback_error
