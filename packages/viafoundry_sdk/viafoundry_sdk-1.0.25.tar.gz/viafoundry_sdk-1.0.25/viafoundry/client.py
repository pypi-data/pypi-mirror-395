import requests
from viafoundry.auth import Auth
from requests.exceptions import RequestException, MissingSchema
from viafoundry.reports import Reports
from viafoundry.process import Process
from viafoundry.metadata import Metadata 
import logging
from typing import Optional, Union, Dict

# Configure logging
logging.basicConfig(filename="viafoundry_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


class ViaFoundryClient:
    """
    A client for interacting with the ViaFoundry API.

    Attributes:
        auth (Auth): The authentication handler.
        reports (Reports): The reports handler.
        process (Process): The process handler.
        metadata (Metadata): The metadata handler.  # <-- Add this line
        endpoints_cache (Optional[Dict]): Cache for discovered endpoints.
    """

    def __init__(self, config_path: Optional[str] = None, enable_session_history: bool = False) -> None:
        """
        Initializes the ViaFoundryClient.

        Args:
            config_path (Optional[str]): Path to the configuration file. Defaults to None.
            enable_session_history (bool): Whether to enable session history for reports. Defaults to False.

        Raises:
            RuntimeError: If initialization fails.
        """
        try:
            self.auth = Auth(config_path)
            logging.info("Authentication initialized successfully.")
            self.reports = Reports(self, enable_session_history=enable_session_history)
            logging.info("Reports functionality initialized successfully.")
            self.process = Process(self) # Process handler initialization
            logging.info("Process functionality initialized successfully.")
            self.metadata = Metadata(self)  # Metadata handler initialization
            logging.info("Metadata functionality initialized successfully.")

        except Exception as e:
            logging.error("Initialization error", exc_info=True)
            self._raise_error(101, "Failed to initialize authentication. Check your configuration file.")
        self.endpoints_cache = None  # Cache for discovered endpoints

    def configure_auth(self, hostname: str, username: str = None, password: str = None, token: str = None, identity_type: int = 1, redirect_uri: str = "http://localhost/user") -> None:
        """
        Configures authentication by setting up the token.

        Args:
            hostname (str): The hostname for authentication.
            username (str, optional): The username for authentication.
            password (str, optional): The password for authentication.
            token (str, optional): Pre-generated personal access token.
            identity_type (int): The identity type. Defaults to 1.
            redirect_uri (str): The redirect URI. Defaults to "http://localhost/user".

        Raises:
            RuntimeError: If authentication configuration fails.
        
        Examples:
            Using username and password:
                client.configure_auth(hostname="https://api.example.com", username="user", password="pass")
            
            Using personal access token:
                client.configure_auth(hostname="https://api.example.com", token="your_pat_token")
        """
        try:
            self.auth.configure(hostname, username, password, token, identity_type, redirect_uri)
        except MissingSchema:
            self._raise_error(104, f"Invalid hostname '{hostname}'. No scheme supplied. Did you mean 'https://{hostname}'?")
        except RequestException:
            self._raise_error(102, "Failed to configure authentication. Check your hostname and credentials.")
        except Exception:
            self._raise_error(999, "An unexpected error occurred while configuring authentication.")
    
    def configure_auth_token(self, hostname: str, token: str) -> None:
        """
        Configures authentication using a pre-generated personal access token.
        This is a convenience method for token-only authentication.

        Args:
            hostname (str): The hostname for authentication.
            token (str): Pre-generated personal access token.

        Raises:
            RuntimeError: If authentication configuration fails.
        
        Examples:
            client.configure_auth_token(hostname="https://api.example.com", token="your_pat_token")
        """
        try:
            self.auth.configure_token(hostname, token)
        except MissingSchema:
            self._raise_error(104, f"Invalid hostname '{hostname}'. No scheme supplied. Did you mean 'https://{hostname}'?")
        except Exception:
            self._raise_error(999, "An unexpected error occurred while configuring authentication.")

    def discover(self, search: Optional[str] = None, as_json: bool = False) -> Union[Dict, str]:
        """
        Fetches all available endpoints from Swagger.

        Args:
            search (Optional[str]): Filter endpoints containing a search string or in `key=value` format.
            as_json (bool): Whether to return the output as a JSON-formatted string. Defaults to False.

        Returns:
            Union[Dict, str]: A dictionary or JSON-formatted string of endpoints.

        Raises:
            RuntimeError: If endpoint discovery fails.
        """
        if self.endpoints_cache:
            endpoints = self.endpoints_cache
        else:
            hostname = self.auth.hostname
            if not hostname:
                self._raise_error(201, "Hostname is not configured. Please run the configuration setup.")

            url = f"{hostname}/swagger.json"
            headers = self.auth.get_headers()

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                if "application/json" not in response.headers.get("Content-Type", ""):
                    self._raise_error(203, f"Non-JSON response received from: {url}.")
                self.endpoints_cache = response.json().get("paths", {})
                endpoints = self.endpoints_cache
            except MissingSchema:
                self._raise_error(104, f"Invalid URL '{url}'. No scheme supplied. Did you mean 'https://{url}'?")
            except RequestException:
                self._raise_error(202, "Failed to fetch endpoints. Please verify your configuration.")
            except requests.exceptions.JSONDecodeError:
                self._raise_error(203, f"Failed to parse JSON response. Check the Swagger endpoint at: {url}.")
            except Exception:
                self._raise_error(999, "An unexpected error occurred while discovering endpoints.")

        # Filter by search string or key=value
        if search:
            if "=" in search:
                key, value = search.split("=", 1)
                if key == "endpoint":
                    # Special case for 'endpoint', match against endpoint keys
                    filtered_endpoints = {
                        endpoint: details
                        for endpoint, details in endpoints.items()
                        if value.lower() in endpoint.lower()
                    }
                else:
                    # General key=value filtering
                    filtered_endpoints = {
                        endpoint: details
                        for endpoint, details in endpoints.items()
                        if any(value.lower() in str(detail.get(key, "")).lower() for method, detail in details.items())
                    }
            else:
                # General substring filtering
                filtered_endpoints = {
                    endpoint: details
                    for endpoint, details in endpoints.items()
                    if search.lower() in endpoint.lower()
                }
        else:
            filtered_endpoints = endpoints

        # Return as JSON string if requested
        if as_json:
            import json
            return json.dumps(filtered_endpoints, indent=4)

        return filtered_endpoints

    def call(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Union[Dict, str]:
        """
        Sends a request to a specific endpoint.

        Args:
            method (str): The HTTP method to use for the request.
            endpoint (str): The endpoint to call.
            params (Optional[Dict]): Query parameters for the request. Defaults to None.
            data (Optional[Dict]): Data to send in the request body. Defaults to None.
            files (Optional[Dict]): Files to upload. Defaults to None.

        Returns:
            Union[Dict, str]: The response data as a dictionary or raw text.

        Raises:
            RuntimeError: If the request fails.
        """
        hostname = self.auth.hostname
        if not hostname:
            self._raise_error(201, "Hostname is not configured. Please run the configuration setup.")

        url = f"{hostname}{endpoint}"
        headers = self.auth.get_headers()

        try:
            if files:
                # Use 'data' for form-encoded fields and 'files' for file uploads
                response = requests.request(
                    method.upper(), url, params=params, data=data, files=files, headers=headers
                )
            else:
                # Standard request with JSON data
                response = requests.request(
                    method.upper(), url, params=params, json=data, headers=headers
                )

            response.raise_for_status()
            if "application/json" not in response.headers.get("Content-Type", ""):
                return response.text.strip()  # Return raw text response

            return response.json()
        except MissingSchema:
            self._raise_error(104, f"Invalid URL '{url}'. No scheme supplied. Did you mean 'https://{url}'?")
        except requests.exceptions.HTTPError:
            self._handle_http_error(response)
        except requests.exceptions.JSONDecodeError:
            self._raise_error(205, f"Failed to parse JSON response from endpoint: {endpoint}.")
        except RequestException:
            self._raise_error(206, "Request to endpoint failed. Please check your parameters or server configuration.")
        except Exception:
            self._raise_error(999, "An unexpected error occurred while calling the endpoint.")

    def _handle_http_error(self, response: requests.Response) -> None:
        """
        Categorizes HTTP errors based on status codes.

        Args:
            response (requests.Response): The response object from the request.

        Raises:
            RuntimeError: If an HTTP error occurs.
        """
        status_code = response.status_code
        if status_code == 400:
            self._raise_error(302, "Bad Request: Check the request parameters or payload.")
        elif status_code == 401:
            self._raise_error(303, "Unauthorized: Ensure proper authentication.")
        elif status_code == 403:
            self._raise_error(304, "Forbidden: You do not have permission to access this resource.")
        elif status_code == 404:
            self._raise_error(305, "Not Found: The requested resource does not exist.")
        elif status_code == 500:
            self._raise_error(306, "Internal Server Error: Something went wrong on the server.")
        else:
            self._raise_error(307, f"Unexpected HTTP error occurred. Status code: {status_code}.")

    def _raise_error(self, code: int, message: str) -> None:
        """
        Raises a categorized error with a specific code and message.

        Args:
            code (int): The error code.
            message (str): The error message.

        Raises:
            RuntimeError: The categorized error.
        """
        logging.error(f"Error {code}: {message}")  # Log the error
        raise RuntimeError(f"Error {code}: {message}")
