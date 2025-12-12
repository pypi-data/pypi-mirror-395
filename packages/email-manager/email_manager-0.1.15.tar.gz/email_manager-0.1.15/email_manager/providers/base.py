# email_manager/providers/base.py
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseEmailProvider(ABC):
    @abstractmethod
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        **kwargs
    ) -> bool:
        """
        Envía un correo electrónico a un destinatario.
        """
        pass

    @abstractmethod
    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        **kwargs
    ) -> dict:
        """
        Envía correos electrónicos a múltiples destinatarios.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Devuelve el nombre del proveedor (por ejemplo, 'SMTPProvider').
        """
        pass

    def _handle_error(self, error: Exception):
        """
        Manejo genérico de errores.
        """
        print(f"[{self.get_provider_name()} Error] {error}")
