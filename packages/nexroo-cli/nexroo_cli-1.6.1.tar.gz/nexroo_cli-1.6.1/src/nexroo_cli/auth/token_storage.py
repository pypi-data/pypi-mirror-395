import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from loguru import logger


class TokenStorage:
    def __init__(self, storage_dir: Optional[Path] = None):
        if storage_dir is None:
            storage_dir = Path.home() / ".nexroo"

        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.token_file = self.storage_dir / "auth_token.enc"
        self.key_file = self.storage_dir / ".key"

        self._ensure_encryption_key()

    def _ensure_encryption_key(self):
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            os.chmod(self.key_file, 0o600)

        self.cipher = Fernet(self.key_file.read_bytes())

    def save_token(self, token_data: Dict[str, Any]):
        token_data['stored_at'] = datetime.utcnow().isoformat()

        json_data = json.dumps(token_data)
        encrypted_data = self.cipher.encrypt(json_data.encode())

        self.token_file.write_bytes(encrypted_data)
        os.chmod(self.token_file, 0o600)

        logger.info(f"Token saved to {self.token_file}")

    def load_token(self) -> Optional[Dict[str, Any]]:
        if not self.token_file.exists():
            return None

        try:
            encrypted_data = self.token_file.read_bytes()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            token_data = json.loads(decrypted_data.decode())

            return token_data
        except Exception as e:
            logger.error(f"Failed to load token: {e}")
            return None

    def clear_token(self):
        if self.token_file.exists():
            self.token_file.unlink()
            logger.info("Token cleared")

    def is_token_valid(self, grace_days: int = 30) -> bool:
        token_data = self.load_token()
        if not token_data:
            return False

        stored_at = datetime.fromisoformat(token_data.get('stored_at'))
        grace_period = timedelta(days=grace_days)

        if datetime.utcnow() > stored_at + grace_period:
            logger.warning("Token expired (beyond grace period)")
            return False

        expires_at = token_data.get('expires_at')
        if expires_at:
            if datetime.utcnow() > datetime.fromisoformat(expires_at):
                logger.info("Token expired but within grace period")
                return True

        return True

    def get_access_token(self) -> Optional[str]:
        token_data = self.load_token()
        if token_data:
            return token_data.get('access_token')
        return None
