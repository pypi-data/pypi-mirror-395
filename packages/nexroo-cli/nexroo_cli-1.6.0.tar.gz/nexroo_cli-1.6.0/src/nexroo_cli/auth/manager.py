from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger
from .config import ZitadelConfig
from .token_storage import TokenStorage
from .oidc_client import OIDCClient
from .jwt_verifier import JWTVerifier


class AuthManager:
    def __init__(self, config: Optional[ZitadelConfig] = None):
        if config is None:
            config = ZitadelConfig.load()

        self.config = config
        self.storage = TokenStorage()
        self.oidc_client = OIDCClient(config)
        self.jwt_verifier = JWTVerifier(config)

    async def login(self) -> Dict[str, Any]:
        logger.info("Starting authentication flow...")

        try:
            auth_data = self.oidc_client.start_auth_flow()

            logger.info("Exchanging authorization code for token...")
            token_response = await self.oidc_client.exchange_code_for_token(
                auth_data['code'],
                auth_data['code_verifier'],
                auth_data['redirect_uri']
            )

            expires_in = token_response.get('expires_in', 3600)
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

            token_data = {
                'access_token': token_response['access_token'],
                'refresh_token': token_response.get('refresh_token'),
                'expires_at': expires_at.isoformat(),
                'token_type': token_response.get('token_type', 'Bearer'),
            }

            self.storage.save_token(token_data)

            claims = await self.jwt_verifier.verify_token(token_response['access_token'])

            logger.info(f"Authentication successful! User: {claims.get('sub')}")

            return {
                'status': 'success',
                'user_id': claims.get('sub'),
                'email': claims.get('email'),
                'expires_at': expires_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    async def logout(self):
        self.storage.clear_token()
        logger.info("Logged out successfully")

    async def verify_authentication(self, require_valid: bool = False) -> bool:
        if not self.storage.is_token_valid(grace_days=30):
            logger.warning("No valid token found")
            return False

        token_data = self.storage.load_token()
        if not token_data:
            return False

        access_token = token_data.get('access_token')
        if not access_token:
            return False

        try:
            expires_at_str = token_data.get('expires_at')
            token_expired = False

            if expires_at_str:
                expires_at = datetime.fromisoformat(expires_at_str)
                token_expired = datetime.utcnow() > expires_at

            if token_expired and not require_valid:
                logger.info("Token expired, attempting refresh...")
                await self._try_refresh_token()
                token_data = self.storage.load_token()
                access_token = token_data.get('access_token') if token_data else None

            if not access_token:
                return False

            grace_mode = token_expired and not require_valid
            await self.jwt_verifier.verify_token(access_token, grace_period=grace_mode)

            logger.info("Authentication verified successfully")
            return True

        except Exception as e:
            logger.error(f"Token verification failed: {e}")

            if not require_valid:
                logger.info("Attempting token refresh...")
                try:
                    await self._try_refresh_token()
                    return True
                except Exception as refresh_error:
                    logger.error(f"Token refresh failed: {refresh_error}")

            return False

    async def _try_refresh_token(self):
        token_data = self.storage.load_token()
        if not token_data or not token_data.get('refresh_token'):
            raise Exception("No refresh token available")

        logger.info("Refreshing access token...")
        token_response = await self.oidc_client.refresh_token(token_data['refresh_token'])

        expires_in = token_response.get('expires_in', 3600)
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        new_token_data = {
            'access_token': token_response['access_token'],
            'refresh_token': token_response.get('refresh_token', token_data['refresh_token']),
            'expires_at': expires_at.isoformat(),
            'token_type': token_response.get('token_type', 'Bearer'),
        }

        self.storage.save_token(new_token_data)
        logger.info("Token refreshed successfully")

    def get_token(self) -> Optional[str]:
        return self.storage.get_access_token()

    def is_authenticated(self) -> bool:
        return self.storage.is_token_valid(grace_days=30)
