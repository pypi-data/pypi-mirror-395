import time
import requests
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class githubAuth:
    """
    Class for authenticating and retrieving auth token from GitHub.

    Args:
        private_key_pem (str): Private Key PEM for GitHub authentication
        app_id (str): GitHub App id
        installation_id (str): GitHub App installation id

    Methods:
        get_auth_token: Get auth token from GitHub for the GitHub App

    Examples:
        # Get auth token from GitHub
        github_auth = githubAuth(private_key_pem, app_id, installation_id)
        
        # The returned token could be used with PyGithub API: https://github.com/PyGithub/PyGithub/tree/main/doc/examples
        g = Github(login_or_token=github_auth.token)
        org = g.get_organization("ORGNAME")
        repo = org.get_repo("REPONAME")
        
    """
    def __init__ (self, private_key_pem: str, app_id: str, installation_id: str):
        self.installation_id = installation_id
        self.private_key = load_pem_private_key(
            str.encode(private_key_pem),
            password=None
        )

        self.payload = {
            # Issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minutes maximum)
            'exp': int(time.time()) + 600,
            # GitHub App's identifier
            'iss': app_id
        }

        self.token = self.get_auth_token()

    def _base64url_encode(self, data):
        """Encode data using base64url encoding (RFC 7515)"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        encoded = base64.urlsafe_b64encode(data).decode('utf-8')
        return encoded.rstrip('=')  # Remove padding
        
    def _generate_jwt(self):
        """Generate a JWT token signed with RS256 algorithm"""
        header = {
            "alg": "RS256",
            "typ": "JWT"
        }
        
        # Encode header and payload
        encoded_header = self._base64url_encode(json.dumps(header))
        encoded_payload = self._base64url_encode(json.dumps(self.payload))
        
        # Create message to sign
        message = f"{encoded_header}.{encoded_payload}"
        
        # Sign the message
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        encoded_signature = self._base64url_encode(signature)
        
        # Create the JWT token
        jwt_token = f"{message}.{encoded_signature}"
        return jwt_token

    def get_auth_token(self):
        try:
            encoded_jwt = self._generate_jwt()
            # Set Headers
            headers = {"Authorization": f"Bearer {encoded_jwt}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28" }
            # Get Access Token
            resp = requests.post(f'https://api.github.com/app/installations/{self.installation_id}/access_tokens', 
                                headers=headers)
            # Add response validation
            resp.raise_for_status()
            
            # Parse response and get token
            response_data = json.loads(resp.content.decode())
            if 'token' not in response_data:
                raise KeyError("Token not found in GitHub API response")
                
            return response_data['token']
        except Exception as error:  # Use a general exception handler for all errors
            if isinstance(error, (KeyError, json.JSONDecodeError)):
                raise RuntimeError(f"Failed to parse GitHub response: {error}") from error
            else:
                raise RuntimeError(f"GitHub API request failed: {error}") from error
