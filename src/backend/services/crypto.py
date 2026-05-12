import os
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

_fernet: Fernet | None = None

def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            logger.warning(
                "ENCRYPTION_KEY is not set. Generating a temporary key — "
                "stored API keys will not survive a restart. Set ENCRYPTION_KEY in .env to persist them."
            )
            key = Fernet.generate_key().decode()
            os.environ["ENCRYPTION_KEY"] = key
        _fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return _fernet

def encrypt(value: str) -> str:
    return _get_fernet().encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return _get_fernet().decrypt(value.encode()).decode()
