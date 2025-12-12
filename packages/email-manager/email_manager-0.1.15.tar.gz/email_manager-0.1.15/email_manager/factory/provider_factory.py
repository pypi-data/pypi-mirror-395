# email_system/factory/provider_factory.py

from email_manager.providers.mailgun_provider import MailgunProvider
from email_manager.providers.smtp_provider import SMTPProvider
from email_manager.providers.mailtrap_provider import MailtrapProvider
from email_manager.providers.base import BaseEmailProvider
from email_manager.config.email_config import EmailConfig



class ProviderFactory:
    _provider_map = {
        "mailgun": lambda config: MailgunProvider(mailgun_params=config.mailgun_params, config=config),
        "smtp": lambda config: SMTPProvider(smtp_params=config.smtp_params, config=config),
        "mailtrap": lambda config: MailtrapProvider(mailtrap_params=config.mailtrap_params, config=config)
    }

    @staticmethod
    def create_provider(config: EmailConfig, override: str = None) -> BaseEmailProvider:
        provider_key = (override or config.provider_type).lower()
        try:
            if not config.mailtrap_params and config.provider_type == 'mailtrap': 
                raise ValueError('provider_type = mailtrap y no esta mailtrap_params')
        
            if not config.mailgun_params and config.provider_type == 'mailgun': 
                raise ValueError('provider_type = mailgun y no esta mailgun_params')
            
            if config.fallback and not config.smtp_params: 
                print('No se puede usar fallback sin smtp_params, si falla no se reintentará con SMTP')
                
            return ProviderFactory._provider_map[provider_key](config)
        except KeyError:
            raise ValueError(f"Unsupported provider type: {provider_key}")
        except Exception as e:
            raise RuntimeError(f"Error creating provider '{provider_key}': {e}")

