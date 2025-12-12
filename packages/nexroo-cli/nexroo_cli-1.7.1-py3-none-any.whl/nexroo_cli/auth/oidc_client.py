import hashlib
import base64
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from typing import Optional, Dict, Any
import httpx
from loguru import logger
from .config import ZitadelConfig


class CallbackHandler(BaseHTTPRequestHandler):
    auth_code: Optional[str] = None
    error: Optional[str] = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if 'code' in query_params:
            CallbackHandler.auth_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head><title>Authentication Success</title></head>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                    <script>window.close();</script>
                </body>
                </html>
            """)
        elif 'error' in query_params:
            CallbackHandler.error = query_params['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
                <html>
                <head><title>Authentication Error</title></head>
                <body>
                    <h1>Authentication Failed</h1>
                    <p>Error: {query_params.get('error_description', ['Unknown error'])[0]}</p>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """.encode())
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass


class OIDCClient:
    def __init__(self, config: ZitadelConfig):
        self.config = config
        self.token_endpoint = f"{config.authority}/oauth/v2/token"
        self.authorize_endpoint = f"{config.authority}/oauth/v2/authorize"
        self.jwks_uri = f"{config.authority}/oauth/v2/keys"

    def _generate_code_verifier(self) -> str:
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

    def _generate_code_challenge(self, verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')

    def start_auth_flow(self) -> Dict[str, Any]:
        server = HTTPServer(('localhost', 0), CallbackHandler)
        port = server.server_address[1]
        redirect_uri = f"http://localhost:{port}/callback"

        code_verifier = self._generate_code_verifier()
        code_challenge = self._generate_code_challenge(code_verifier)

        auth_params = {
            'client_id': self.config.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': f'openid profile email urn:zitadel:iam:org:project:id:{self.config.project_id}:aud offline_access',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        }

        auth_url = f"{self.authorize_endpoint}?{urlencode(auth_params)}"

        logger.info(f"Opening browser for authentication...")
        logger.info(f"If the browser doesn't open, visit: {auth_url}")

        webbrowser.open(auth_url)

        logger.info(f"Waiting for callback on port {port}...")
        server.handle_request()

        if CallbackHandler.error:
            raise Exception(f"Authentication error: {CallbackHandler.error}")

        if not CallbackHandler.auth_code:
            raise Exception("No authorization code received")

        auth_code = CallbackHandler.auth_code
        CallbackHandler.auth_code = None

        return {
            'code': auth_code,
            'code_verifier': code_verifier,
            'redirect_uri': redirect_uri
        }

    async def exchange_code_for_token(self, code: str, code_verifier: str, redirect_uri: str) -> Dict[str, Any]:
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': self.config.client_id,
            'code': code,
            'code_verifier': code_verifier,
            'redirect_uri': redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_endpoint,
                data=token_params,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code != 200:
                logger.error(f"Token exchange failed: {response.text}")
                raise Exception(f"Failed to exchange code for token: {response.status_code}")

            return response.json()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        token_params = {
            'grant_type': 'refresh_token',
            'client_id': self.config.client_id,
            'refresh_token': refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_endpoint,
                data=token_params,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code != 200:
                logger.error(f"Token refresh failed: {response.text}")
                raise Exception(f"Failed to refresh token: {response.status_code}")

            return response.json()

    async def fetch_jwks(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.jwks_uri)
            response.raise_for_status()
            return response.json()
