import base64
import json
import os
import time
from pathlib import Path

import requests
from pydantic import BaseModel

from common.constants import AUTH_CLIENT_ID, AUTH_DOMAIN, get_auth_dir

# Authentication routes
AUTH_TOKEN_URL = f"{AUTH_DOMAIN}/oauth/token"
DEVICE_CODE_URL = f"{AUTH_DOMAIN}/oauth/device/code"

# Authentication constants
ALGORITHMS = ["RS256"]
AUDIENCE = "https://sessions.antioch.com"
AUTH_SCOPE = "openid profile email"
AUTH_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
AUTH_TIMEOUT_SECONDS = 120

# Authentication claims
AUTH_ORG_ID_CLAIM = "https://antioch.com/org_id"
AUTH_ORG_NAME_CLAIM = "https://antioch.com/org_name"
AUTH_ORGANIZATIONS_CLAIM = "https://antioch.com/organizations"


class AuthError(Exception):
    """
    Authentication error.
    """


class Organization(BaseModel):
    """
    Organization information.
    """

    org_id: str
    org_name: str


class AuthHandler:
    """
    Client for handling authentication.

    Auth is used for:
    - Pulling artifacts from the remote Ark registry
    - Pulling assets from the remote asset registry
    """

    def __init__(self):
        """
        Initialize the auth handler.
        """

        self._token: str | None = None
        self._user_id: str | None = None
        self._current_org: Organization | None = None
        self._available_orgs: list[Organization] = []
        self._load_local_token()

    def login(self) -> None:
        """
        Authenticate the user via device code flow.

        :raises AuthError: If authentication fails.
        """

        if self.is_authenticated():
            print("Already authenticated")
            return

        # Request device code
        device_code_payload = {
            "client_id": AUTH_CLIENT_ID,
            "scope": AUTH_SCOPE,
            "audience": AUDIENCE,
        }

        device_code_response = requests.post(DEVICE_CODE_URL, data=device_code_payload)
        device_code_data = device_code_response.json()
        if device_code_response.status_code != 200:
            raise AuthError("Error generating the device code") from Exception(device_code_data)

        print(f"You have {AUTH_TIMEOUT_SECONDS} seconds to complete the following:")
        print(f"  1. Navigate to: {device_code_data['verification_uri_complete']}")
        print(f"  2. Enter the code: {device_code_data['user_code']}")

        # Poll for token
        token_payload = {
            "grant_type": AUTH_GRANT_TYPE,
            "device_code": device_code_data["device_code"],
            "client_id": AUTH_CLIENT_ID,
        }

        authenticated = False
        start_time = time.time()
        while not authenticated:
            token_response = requests.post(AUTH_TOKEN_URL, data=token_payload)
            token_data = token_response.json()
            if token_response.status_code == 200:
                print("Authenticated!")
                authenticated = True
            elif token_data["error"] not in ("authorization_pending", "slow_down"):
                print(token_data["error_description"])
                raise AuthError("Error authenticating the user") from Exception(token_data)
            else:
                if time.time() - start_time > AUTH_TIMEOUT_SECONDS:
                    raise AuthError("Timeout waiting for authentication")
                time.sleep(device_code_data["interval"])

        # Save token
        self._token = token_data["access_token"]
        if self._token is None:
            raise AuthError("No token received")
        self._validate_token_claims(self._token)
        self.save_token()

    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.

        :return: True if authenticated, False otherwise.
        """

        return self._current_org is not None

    def select_organization(self, org_id: str):
        """
        Select the organization to use for the session.

        :param org_id: The ID of the organization to select.
        :raises AuthError: If the user is not authenticated.
        """

        if not self.is_authenticated():
            raise AuthError("Not authenticated. Please login first")

        for org in self._available_orgs:
            if org.org_id == org_id:
                self._current_org = org
                return

        raise AuthError(f"Organization '{org_id}' is not in your available organizations")

    def get_current_org(self) -> Organization | None:
        """
        Get the current organization.

        :return: The current organization.
        :raises AuthError: If the user is not authenticated.
        """

        if not self.is_authenticated():
            raise AuthError("Not authenticated. Please login first")

        return self._current_org

    def get_user_id(self) -> str | None:
        """
        Get the user ID.

        :return: The user ID.
        """

        return self._user_id

    def get_available_orgs(self) -> list[Organization]:
        """
        Get the available organizations.

        :return: The available organizations.
        """

        return self._available_orgs

    def get_token(self) -> str | None:
        """
        Get the token.

        :return: The token.
        :raises AuthError: If the user is not authenticated.
        """

        if not self.is_authenticated():
            raise AuthError("Not authenticated. Please login first")
        return self._token

    def save_token(self) -> None:
        """
        Save the authentication token and organization data to disk.

        :raises AuthError: If not authenticated.
        """

        if not self.is_authenticated():
            raise AuthError("Not authenticated. Please login first")

        stored_data = {
            "token": self._token,
            "current_org": self._current_org.model_dump() if self._current_org else None,
            "available_orgs": [org.model_dump() for org in self._available_orgs],
        }

        token_path = self._get_token_path()

        # Create file with restrictive permissions (owner read/write only)
        # Use os.open to atomically create file with 0o600 permissions
        fd = os.open(token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(stored_data, f, indent=2)

    def clear_token(self) -> None:
        """
        Clear the stored authentication token from disk.
        """

        token_path = self._get_token_path()
        if token_path.exists():
            token_path.unlink()

    def _load_local_token(self) -> None:
        """
        Load the authentication token and organization data from disk.

        Silently returns if no token exists or if loading fails. Clears invalid tokens.
        """

        token_path = self._get_token_path()
        if not token_path.exists():
            return

        try:
            with open(token_path, "r") as f:
                stored_data = json.load(f)

            self._token = stored_data.get("token")
            if not self._token:
                return

            # Validate and extract all claims from token
            self._validate_token_claims(self._token)
        except Exception as e:
            print(f"Error loading local token: {e}")

            # Clear invalid or expired tokens
            self._token = None
            self.clear_token()
            return

    def _validate_token_claims(self, token: str):
        """
        Validate the token and extract all claims including user ID and organization information.

        :param token: The JWT token to validate.
        :raises AuthError: If the token is invalid, expired, or missing required claims.
        """

        parts = token.split(".")
        if len(parts) != 3:
            raise AuthError("Invalid token format")

        # Decode the payload (middle part)
        payload_encoded = parts[1]
        padding = len(payload_encoded) % 4
        if padding:
            payload_encoded += "=" * (4 - padding)
        payload_bytes = base64.urlsafe_b64decode(payload_encoded)
        payload = json.loads(payload_bytes)

        # Check expiration
        exp = payload.get("exp")
        if exp and time.time() > exp:
            raise AuthError("Token has expired")

        # Extract user ID
        self._user_id = payload.get("sub")
        if self._user_id is None:
            raise AuthError("User ID not found in token claims")

        # Extract current organization
        self._current_org = Organization(
            org_id=payload.get(AUTH_ORG_ID_CLAIM),
            org_name=payload.get(AUTH_ORG_NAME_CLAIM),
        )

        # Extract available organizations
        # Note: Auth0 returns organizations with "id" and "name" keys, not "org_id" and "org_name"
        self._available_orgs = [
            Organization(org_id=org.get("id") or org.get("org_id"), org_name=org.get("name") or org.get("org_name"))
            for org in payload.get(AUTH_ORGANIZATIONS_CLAIM, [])
        ]

    def _get_token_path(self) -> Path:
        """
        Get the token file path.

        :return: Path to the token file.
        """

        return get_auth_dir() / "token.json"
