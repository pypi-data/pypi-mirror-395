import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.viaenv")

class Auth:
    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialize the Auth class.

        Args:
            config_path (str, optional): Path to the configuration file. Defaults to None.
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self.load_config()
        self.hostname = self.config.get("hostname")  # Initialize hostname
        self.bearer_token = self.config.get("bearer_token")  # Bearer token

    def load_config(self) -> Dict:
        """Load configuration from the config file.

        Returns:
            Dict: The loaded configuration.
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def save_config(self) -> None:
        """Save hostname and bearer token to the config file.
        """
        config = {
            "hostname": self.hostname,
            "bearer_token": self.bearer_token  # Save only the bearer token
        }
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)

    def configure(self, hostname: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None, identity_type: int = 1, redirect_uri: str = "https://viafoundry.com/user") -> None:
        """Prompt user for credentials if necessary and authenticate.

        Args:
            hostname (str): The hostname for authentication.
            username (str, optional): The username for authentication. Defaults to None.
            password (str, optional): The password for authentication. Defaults to None.
            token (str, optional): Pre-generated personal access token. Defaults to None.
            identity_type (int, optional): The identity type. Defaults to 1.
            redirect_uri (str, optional): The redirect URI. Defaults to "https://viafoundry.com/user".
        
        Raises:
            ValueError: If hostname or token is empty.
        """
        if not hostname or not hostname.strip():
            raise ValueError("Hostname cannot be empty")
        
        self.hostname = hostname
        
        # If token is provided, use it directly
        if token:
            if not token.strip():
                raise ValueError("Token cannot be empty")
            self.bearer_token = token
            self.save_config()
            return
        
        # Otherwise, use username/password authentication
        if not username or not password:
            username = input("Username: ")
            password = input("Password: ")
        
        # Validate username and password
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")

        # Authenticate and retrieve the cookie token
        cookie_token = self.login(username, password, identity_type, redirect_uri)
        # Use cookie token to get bearer token
        self.bearer_token = self.get_bearer_token(cookie_token)
        self.save_config()
    
    def configure_token(self, hostname: str, token: str) -> None:
        """Configure authentication using a pre-generated personal access token.

        Args:
            hostname (str): The hostname for authentication.
            token (str): Pre-generated personal access token.
        
        Raises:
            ValueError: If hostname or token is empty.
        """
        if not hostname or not hostname.strip():
            raise ValueError("Hostname cannot be empty")
        if not token or not token.strip():
            raise ValueError("Token cannot be empty")
        
        self.hostname = hostname
        self.bearer_token = token
        self.save_config()

    def login(self, username: str, password: str, identity_type: int = 1, redirect_uri: str = "https://viafoundry.com/user") -> str:
        """Authenticate and get the token from the Set-Cookie header.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
            identity_type (int, optional): The identity type. Defaults to 1.
            redirect_uri (str, optional): The redirect URI. Defaults to "https://viafoundry.com/user".

        Returns:
            str: The authentication token.
        """
        if not self.hostname:
            raise ValueError("Hostname is not set. Please configure the SDK.")
        
        url = f"{self.hostname}/api/auth/v1/login"
        payload = {
            "username": username,
            "password": password,
            "identityType": identity_type,
            "redirectUri": redirect_uri
        }

        # Send POST request to authenticate
        response = requests.post(url, json=payload)
        response.raise_for_status()

        # Extract the 'Set-Cookie' header
        cookie_header = response.headers.get("Set-Cookie")
        if not cookie_header:
            raise ValueError(f"Cookie not found in response headers: {response.headers}")
        
        # Extract the token value from the cookie
        cookie_key = "viafoundry-cookie="
        start_index = cookie_header.find(cookie_key) + len(cookie_key)
        end_index = cookie_header.find(";", start_index)
        token = cookie_header[start_index:end_index]
        
        if not token:
            raise ValueError(f"Token not found in cookie: {cookie_header}")
        
        return token

    def calculate_expiration_date(self) -> str:
        """Calculate an expiration date one month from now.

        Returns:
            str: The expiration date in YYYY-MM-DD format.
        """
        return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    def get_bearer_token(self, cookie_token: str, name: str = "token") -> str:
        """Request a bearer token using the existing cookie token.

        Args:
            cookie_token (str): The cookie token for authentication.
            name (str, optional): The name of the token. Defaults to "token".

        Returns:
            str: The bearer token.
        """
        if not self.hostname:
            raise ValueError("Hostname is missing. Please configure the SDK.")

        url = f"{self.hostname}/api/auth/v1/personal-access-token"
        headers = {"Cookie": f"viafoundry-cookie={cookie_token}"}
        payload = {"name": name, "expiresAt": self.calculate_expiration_date()}

        # Send POST request to get the bearer token
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        bearer_token = data.get("token")
        if not bearer_token:
            raise ValueError(f"Bearer token not found in response: {data}")
        
        return bearer_token

    def get_headers(self) -> Dict:
        """Return headers with the bearer token.

        Returns:
            Dict: Headers containing the bearer token.
        """
        if not self.bearer_token:
            raise ValueError("Bearer token is missing. Please configure the SDK.")
        return {"Authorization": f"Bearer {self.bearer_token}"}
