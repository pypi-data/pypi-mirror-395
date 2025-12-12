from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
from jose import jwt, jwk
from jose.exceptions import JWTError, ExpiredSignatureError
from loguru import logger
from .config import ZitadelConfig


class JWTVerifier:
    def __init__(self, config: ZitadelConfig):
        self.config = config
        self.jwks_uri = f"{config.authority}/oauth/v2/keys"
        self._jwks_cache: Optional[Dict[str, Any]] = None
        self._jwks_cache_time: Optional[datetime] = None
        self._cache_duration = timedelta(hours=24)

    async def _get_jwks(self, force_refresh: bool = False) -> Dict[str, Any]:
        if (
            not force_refresh
            and self._jwks_cache is not None
            and self._jwks_cache_time is not None
            and datetime.utcnow() < self._jwks_cache_time + self._cache_duration
        ):
            return self._jwks_cache

        async with httpx.AsyncClient() as client:
            response = await client.get(self.jwks_uri)
            response.raise_for_status()
            self._jwks_cache = response.json()
            self._jwks_cache_time = datetime.utcnow()
            logger.info("JWKS refreshed from Zitadel")
            return self._jwks_cache

    def _get_signing_key(self, token: str, jwks: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')

            if not kid:
                logger.error("No 'kid' in token header")
                return None

            for key in jwks.get('keys', []):
                if key.get('kid') == kid:
                    return key

            logger.error(f"No matching key found for kid: {kid}")
            return None
        except Exception as e:
            logger.error(f"Error getting signing key: {e}")
            return None

    async def verify_token(self, token: str, grace_period: bool = False) -> Dict[str, Any]:
        jwks = await self._get_jwks()
        signing_key = self._get_signing_key(token, jwks)

        if not signing_key:
            jwks = await self._get_jwks(force_refresh=True)
            signing_key = self._get_signing_key(token, jwks)

            if not signing_key:
                raise ValueError("Unable to find matching signing key")

        try:
            public_key = jwk.construct(signing_key)

            options = {
                'verify_signature': True,
                'verify_aud': True,
                'verify_iat': True,
                'verify_exp': not grace_period,
                'verify_nbf': True,
                'verify_iss': True,
                'verify_sub': True,
                'require_aud': True,
                'require_iat': True,
                'require_exp': True,
                'require_nbf': False,
                'require_iss': True,
                'require_sub': True,
            }

            claims = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=f'urn:zitadel:iam:org:project:id:{self.config.project_id}:aud',
                issuer=self.config.authority,
                options=options
            )

            logger.info(f"Token verified successfully (grace_period={grace_period})")
            return claims

        except ExpiredSignatureError:
            if grace_period:
                logger.warning("Token expired but in grace period mode")
                options = {
                    'verify_signature': True,
                    'verify_aud': True,
                    'verify_exp': False,
                    'verify_iss': True,
                }
                claims = jwt.decode(
                    token,
                    public_key,
                    algorithms=['RS256'],
                    audience=f'urn:zitadel:iam:org:project:id:{self.config.project_id}:aud',
                    issuer=self.config.authority,
                    options=options
                )
                return claims
            else:
                logger.error("Token expired")
                raise

        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise
