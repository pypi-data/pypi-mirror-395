import base64

import keyring
from cryptography.fernet import Fernet

from plexutil.exception.server_config_error import ServerConfigError


class TokenManager:
    @staticmethod
    def encrypt(token: str) -> str:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_token = fernet.encrypt(token.encode()).decode()
        keyring.set_password(
            "plexutil",
            "key",
            base64.urlsafe_b64encode(key).decode(),
        )
        return encrypted_token

    @staticmethod
    def decrypt(encrypted_token: str) -> str:
        key = keyring.get_password("plexutil", "key")
        if key:
            fernet = Fernet(base64.urlsafe_b64decode(key.encode()))
            return fernet.decrypt(encrypted_token.encode()).decode()

        description = "Decode key could not be retrieved from keyring"
        raise ServerConfigError(description)
