import platform
import time
import re
from typing import Dict
import requests
import json
import jwt
import warnings
from uuid import uuid4
from IPython import get_ipython
from .client import get_nic_id
from .config.config import config
from .utils.logger import get_logger

logger = get_logger()

if get_ipython():
    from .magics.magics import AGMagic
def login_sql(
    api_key: str = None,
    profile: str = "default",
    params: dict | None = None,
    headers: dict | None = None,
    **kwargs,
):
    """
    Args:
        profile: The profile to load the configuration from.
        api_key (str): The API key for authentication.
        params (dict): Connection parameters for the connection.

    Returns:

    """
    logger.info(f"Initiating SQL login with profile: {profile}")
    config.load_config(profile=profile)
    if not params:
        params = {}
    console_url = config.AGENT_CONSOLE_URL
    base_url = config.AGENT_SQL_SERVER_URL
    if not console_url or not base_url:
        logger.error("Console URL or SQL Server URL not configured")
        raise ValueError("Please load the configuration file using the 'load_config' method before calling this "
                         "function.")
    token = kwargs.pop('token', None)
    if token is not None:
        logger.warning("Deprecated 'token' argument used in login_sql()")
        warnings.warn(
            "'token' argument to login_sql() is deprecated and will be removed. Use headers instead.",
            DeprecationWarning,
            stacklevel=2,
        )
    return AGSQLClient(console_url, base_url, api_key, headers, params, _deprecated_token=token, **kwargs)


class AGSQLClient:
    _DEFAULT_HEADER = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    _UUID = str(uuid4())
    _os = platform.platform()
    _nic_id = get_nic_id()

    def __init__(self, console_url: str, base_url: str, api_key: str, headers: dict | None, params: dict | None, **kwargs):
        """Initialize a new connection.
        Args:
            console_url (str): The URL of the running console server
            base_url (str): The URL of the running SQL server
            api_key (str): The API key for authentication.
            params (dict): Connection parameters for the connection.
        """
        logger.info("Initializing AGSQLClient")
        if params is None:
            params = {}

        # Dynamic header names similar to AGClient
        self.client_auth_header = getattr(config, 'CLIENT_AUTH_HEADER', None) or 'Authorization'
        self.oblv_auth_header = getattr(config, 'OBLV_AUTH_HEADER', None) or 'X-Authorization'

        # Consolidated headers store (will contain both external and internal tokens)
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if headers:
            self._headers.update(headers)

        deprecated_token = kwargs.pop('_deprecated_token', None)
        token_kw = kwargs.pop('token', None)
        actual_token = deprecated_token if deprecated_token is not None else token_kw
        if actual_token is not None:
            warnings.warn(
                "'token' parameter is deprecated and will be removed. Provide the external token via headers instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            if self.client_auth_header not in self._headers:
                self._headers[self.client_auth_header] = actual_token

        self.console_url = console_url
        self._base_url = base_url

        external_header_token = self._headers.get(self.client_auth_header, '')

        # Path 1: API key login flow
        if api_key:
            logger.debug("Using API key authentication for SQL client")
            self.api_key = api_key
            self._set_tokens()  # will populate _access_token/_refresh_token in _process_message
            if hasattr(self, '_access_token') and getattr(self, '_access_token', None):
                self._headers[self.oblv_auth_header] = self._access_token
                if getattr(self, '_refresh_token', ''):
                    self._headers['refresh_token'] = self._refresh_token
        # Path 2: External token provided via header -> exchange
        elif isinstance(external_header_token, str) and external_header_token.strip() != '':
            try:
                logger.info("Attempting token exchange for SQL client")
                exchanged_token = self.__exchange_token()
                self._access_token = f"Bearer {exchanged_token['access_token']}"
                self._refresh_token = exchanged_token.get('refresh_token', '')
                self._headers[self.client_auth_header] = external_header_token
                self._headers[self.oblv_auth_header] = self._access_token
                if self._refresh_token:
                    self._headers['refresh_token'] = self._refresh_token
                logger.info("Token exchange successful for SQL client")
            except Exception as e:
                logger.error(f"Token exchange failed for SQL client: {str(e)}")
                raise ConnectionError(f"Token exchange failed: {str(e)}")
        else:
            logger.error("No authentication method provided for SQL client")
            raise ValueError("Authentication failed: either api_key, or authorization header must be provided.")

        # Keep legacy _DEFAULT_HEADER synchronized for backward compatibility
        self._DEFAULT_HEADER.update(self._headers)
        self._session_id = str(uuid4())
        logger.debug(f"SQL session ID created: {self._session_id}")
        if not self._validate_params(params):
            raise ValueError("The parameters keys shouldn't repeat in any case(lower/upper) to avoid ambiguity")

        params = {k.lower(): v for k, v in params.items()}
        self._team_name = params.get("team_name", None)
        if hasattr(self, '_access_token') and self._access_token:
            logger.debug("Starting SQL session")
            self._start_sql_session(params)
            if get_ipython():
                AGMagic.load_ag_magic()
                AGMagic.load_oblv_client(sql_server=self)
                print("%%sql magic registered successfully! Use %%sql and write a sql query to execute it on the AGENT "
                    "SQL server")
                logger.debug("SQL magic loaded successfully")
        else:
            logger.error("Authentication failed for SQL client")
            print("Failed to authenticate. Please check your API key / auth headers / username-password and try again.")

    def _start_sql_session(self, params):
        logger.debug(f"Starting SQL session with params: {params}")
        epsilon = params.get("eps", params.get("epsilon", float(config.SQL_DEFAULT_EPSILON)))
        delta = params.get("del", params.get("delta", float(config.SQL_DEFAULT_DELTA)))
        cache_invalidation_interval = params.get("cache_timeout", int(config.SQL_CACHE_TTL_SECONDS))
        skip_cache = params.get("skip_cache", False)
        noise_mechanism = params.get("noise_mechanism", "laplace")
        payload = {
            "connection_id": self._session_id
        }
        payload["skip_cache"] = skip_cache
        payload["delta"] = delta

        if epsilon:
            payload["epsilon"] = epsilon
            if not isinstance(epsilon, float) and not isinstance(epsilon, int):
                raise ValueError("Epsilon should be a number!")
        if not isinstance(delta, float) and not isinstance(delta, int):
            raise ValueError("Delta should be a number!")
        if cache_invalidation_interval:
            payload["cache_invalidation_interval"] = cache_invalidation_interval
            if not isinstance(cache_invalidation_interval, int):
                raise ValueError("Cache invalidation interval should be a non-negative integer!")
            
        if not isinstance(skip_cache, bool):
            raise ValueError("Skip cache should be a boolean!")
        if noise_mechanism:
            payload["noise_mechanism"] = noise_mechanism
            if not isinstance(noise_mechanism, str) or noise_mechanism.lower() not in ["laplace", "gaussian"]:
                raise ValueError("Noise mechanism should be either laplace or gaussian!")

        response = self._post(endpoint=config.START_SQL_ENDPOINT, base_url=self._base_url, data=payload,
                              access_token=self._access_token, refresh_token=self._refresh_token)
        logger.debug(f"SQL session start response: {response}")
        if response.get("status") != "Success":
            logger.error(f"Failed to start SQL session: {response.get('error')}")
            raise ValueError("Failed to start SQL session. Please check the parameters.")
        logger.info("SQL session started successfully")

    @staticmethod
    def _validate_params(params: dict):
        """ Check if there is an ambiguity in the params
        :param params: The dictionary that denotes the connection parameters
        :return: True/False
        """

        for key in params:
            if key != key.lower() and key.lower() in params:
                return False
        return True

    def _convert_params_case(self, params: dict, type: str = 'request') -> dict:
        """
        Convert parameter keys to the specified case format based on config.
        
        Args:
            params (dict): The dictionary containing parameters to convert
            
        Returns:
            dict: Dictionary with keys converted to the specified case format
        """
            
        # Get case format from config, default to snake_case for SQL
        case_format = getattr(config, 'PARAMS_CASE', 'snake_case').lower()
        if case_format == 'snake_case':
            return params  # No conversion needed for snake_case
        if type == 'response' and case_format == 'camel_case':
            case_format = 'snake_case' # convert to snake_case for response
        
        converted_params = {}
        
        for key, value in params.items():
            if case_format == 'camel_case':
                # Convert to camelCase
                converted_key = self._to_camel_case(key)
            else:
                # Default to snake_case
                converted_key = self._to_snake_case(key)
            
            converted_params[converted_key] = value
            
        return converted_params
    
    def _to_snake_case(self, name: str) -> str:
        """Convert string to snake_case."""
        # Add an underscore before any uppercase letter (except the first character)
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Add an underscore before a sequence of uppercase letters followed by a lowercase one
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _to_camel_case(self, name: str) -> str:
        """Convert string to camelCase."""
        # Split by underscore and capitalize each word except the first
        parts = name.lower().split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    def _set_tokens(self):
        """
        Retrieves and sets access and refresh tokens from the console server.

        This method sends a login request to the console server using the API key,
        machine UUID, and OS information. It then processes the server's response
        to extract and set the access and refresh tokens.

        Raises:
            Exception: If any error occurs during the token retrieval process.
        """
        try:
            payload = {
                "apikey": self.api_key,
                "machine_uuid": self._UUID,
                "os": self._os,
            }
            if self._nic_id:
                payload["nic_id"] = self._nic_id
            
            logger.info(f"SQL login - requesting token from console")
            logger.debug(f"SQL login - payload: {payload}")
            print("Please approve the token request from the console", flush=True)
            if get_ipython():
                response = self._post(endpoint=config.JUPYTER_LOGIN_REQUEST_ENDPOINT, base_url=self.console_url, data=payload, stream=True)  
                skipped_first = False
                for line in response.split("\n"):
                    if line.strip().startswith('data: '):
                        json_obj = line.strip()
                        if not skipped_first:
                            skipped_first = True
                            continue
                        try:
                            data = json.loads(json_obj[6:])  # Parse JSON directly from the sliced string
                            data = self._convert_params_case(data, type='response')
                            self.__process_message(data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}")
            else:
                response = self._get(endpoint=config.JUPYTER_LOGIN_REQUEST_ENDPOINT, base_url=self.console_url, params=payload, stream=True)
                response = self._convert_params_case(response, type='response')
                self.__process_message(response)

        except Exception as e:
            raise

    def _is_token_expired(self):
        """
        Checks if the access token is expired.

        This method decodes the access token and compares its expiration time
        with the current time to determine if it has expired.

        Returns:
            bool: True if the token is expired, False otherwise.
        """
        try:
            token = self._access_token
            if token.lower().startswith("bearer "):
                token = token.split("Bearer ")[-1]
            payload = jwt.decode(token, options={"verify_signature": False})
            current_time = time.time() + 10  # 10 seconds for network latency
            return payload.get('exp', 0) < current_time
        except Exception as e:
            print(f"Error while checking token expiry: {str(e)}")

    def _get_refresh_token(self):
        try:
            if not self._is_token_expired():
                return
            payload = {
                "refresh_token": self._refresh_token
            }
            response = self._post(endpoint=config.JUPYTER_TOKEN_REFRESH_ENDPOINT, base_url=self.console_url, data=payload)
            self._access_token = f"Bearer {response.get('access_token')}"
            self._refresh_token = response.get("refresh_token")
            # Keep consolidated headers updated
            if getattr(self, '_access_token', None):
                self._headers[self.oblv_auth_header] = self._access_token
            if getattr(self, '_refresh_token', None):
                self._headers['refresh_token'] = self._refresh_token
        except Exception as e:
            raise

    def _make_request(self, method, endpoint, base_url=None, params=None, data=None, headers=None, stream=False):
        """
        Make a HTTP request to the specified endpoint.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint.
            params (dict, optional): URL parameters. Defaults to None.
            data (dict, optional): Request body for POST/PUT requests. Defaults to None.
            headers (dict, optional): HTTP headers. Defaults to None.

        Returns:
            dict or str: JSON response or text from the API.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{base_url or self._base_url}{endpoint}"
        headers = headers.copy() if headers else self._headers.copy()

        logger.info(f"Making {method} request to: {url}")
        logger.debug(f"Request headers: {headers}")
        
        try:
            params = self._convert_params_case(params) if params else {}
            data = self._convert_params_case(data) if data else {}
            
            logger.debug(f"Request params: {params}")
            logger.debug(f"Request data/body: {data}")

            # Inject internal tokens if available
            if hasattr(self, '_access_token') and getattr(self, '_access_token', None):
                headers[self.oblv_auth_header] = self._access_token
            if getattr(self, '_refresh_token', ''):
                headers['refresh_token'] = self._refresh_token
            
            logger.debug(f"Final request headers (with tokens): {headers}")
            response = requests.request(
                method,
                url,
                params=params,
                data=json.dumps(data),
                headers=headers,
                stream=stream
            )
            response.raise_for_status()
            
            logger.debug(f"Response status code: {response.status_code}")

            try:
                response_json = response.json()
                if isinstance(response_json, list):
                    response_json = [self._convert_params_case(item, type='response') for item in response_json]
                else:
                    response_json = self._convert_params_case(response_json, type='response')
                return response_json
            except:
                response_text = response.text
                return response_text

        except requests.exceptions.HTTPError as e:
            raise
        except requests.exceptions.ConnectionError as e:
            raise
        except requests.exceptions.Timeout as e:
            raise
        except Exception as e:
            raise

    def _get(self, endpoint, params=None, base_url=None, access_token=None, refresh_token=None):
        """
        Make a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): URL parameters. Defaults to None.
            base_url (str, optional): Base URL for the request. Defaults to None.
            access_token (str, optional): Access token for authorization. Defaults to None.
            refresh_token (str, optional): Refresh token for authorization. Defaults to None.

        Returns:
            dict: JSON response from the API.

        Raises:
            Exception: If the API request fails.
        """
        headers = self._headers.copy()
        if access_token:
            self._get_refresh_token()
            headers[self.oblv_auth_header] = self._access_token
            # Preserve external token header if it exists
            if self.client_auth_header in self._headers:
                headers[self.client_auth_header] = self._headers[self.client_auth_header]
        if refresh_token:
            headers['refresh_token'] = f'{self._refresh_token}'
        return self._make_request('GET', endpoint, base_url, params=params, headers=headers)

    def _post(self, endpoint, data=None, base_url=None, access_token=None, refresh_token=None, stream = False):
        """
        Make a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): Request body. Defaults to None.
            base_url (str, optional): Base URL for the request. Defaults to None.
            access_token (str, optional): Access token for authorization. Defaults to None.
            refresh_token (str, optional): Refresh token for authorization. Defaults to None.

        Returns:
            dict: JSON response from the API.

        Raises:
            Exception: If the API request fails.
        """
        headers = self._headers.copy()
        if access_token:
            self._get_refresh_token()
            headers[self.oblv_auth_header] = self._access_token
            if self.client_auth_header in self._headers:
                headers[self.client_auth_header] = self._headers[self.client_auth_header]
        if refresh_token:
            headers['refresh_token'] = f'{self._refresh_token}'
        return self._make_request('POST', endpoint, base_url, data=data, headers=headers, stream=stream)

    def __process_message(self, data):
        """
        Processes a message received from the console server.

        This method handles different approval statuses (approved, pending, expired, failed)
        and extracts relevant information such as access tokens and approval URLs.

        Args:
            data (dict): The message data received from the console server.

        Raises:
            ValueError: If the access token cannot be retrieved or the approval status
                is unexpected.
        """
        approval_status = data.get('approval_status')
        if approval_status == 'approved':
            token = data.get('access_token')
            if token:
                self._access_token = f"Bearer {token}"
                self._refresh_token = data.get('refresh_token', None)
                self._headers[self.oblv_auth_header] = self._access_token
                if self._refresh_token:
                    self._headers['refresh_token'] = self._refresh_token
                return
            else:
                print("Access token not found in the response")
        elif approval_status == 'pending':
            print("Please approve the token request in the console")
        elif approval_status == 'expired':
            print("The token request has expired. Please try again")
        elif approval_status == 'failed':
            print("Token request failed. Contact support")
        raise ValueError("Failed to get access token")

    def execute(self, sql):
        """Execute an SQL query."""
        logger.debug(f"Executing SQL query: {sql[:100]}...")  # Log first 100 chars
        payload = {
            "sql": sql,
            "connection_id": self._session_id,
            "team_name": self._team_name or "",
            "client_name": "AGENT_Client",
        }
        logger.debug(f"SQL execution payload: {payload}")
        try:
            response = self._post(endpoint=config.EXECUTE_SQL_ENDPOINT, data=payload, access_token=self._access_token, refresh_token=self._refresh_token)
        except Exception as e:
            logger.error(f"Error executing SQL: {str(e)}")
            raise ValueError(f"Error executing SQL: {sql}. Error: {str(e)}")
        if response.get("status") != "success":
            logger.error(f"SQL execution failed: {response.get('error')}")
            raise ValueError(f"Error executing SQL: {response.get('error')}")
        logger.debug("SQL query executed successfully")
        # Parse JDBC JSON response
        result_set = []
        column_info = "column_info"
        if hasattr(config, 'MIDDLEWARE_ENABLED'):
            MIDDLEWARE_ENABLED = config.MIDDLEWARE_ENABLED.lower() == "true"
            if not MIDDLEWARE_ENABLED:
                column_info = "columnInfo"
        result_set.append(response.get(column_info, {}).get("names", []))
        for row in response.get("rows", []):
            result_set.append(row)
        return result_set

    def __exchange_token(self) -> Dict[str, str]:
        """
        Exchange an external token for internal tokens using OAuth 2.0 token exchange flow.
        
        Uses the externally supplied gateway token already present under
        client_auth_header to obtain an internal execution token.
        
        Returns:
            Dict[str, str]: Dictionary containing access_token and refresh_token
            
        Raises:
            ConnectionError: If there is an error during token exchange
        """
        try:
            token_exchange_url = config.AGENT_CONSOLE_URL + '/auth/exchange_token'
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            headers.update(self._headers)
            
            logger.info(f"SQL Token exchange - calling URL: {token_exchange_url}")
            logger.debug(f"SQL Token exchange - headers: {headers}")
            response = requests.post(
                token_exchange_url,
                headers=headers,
                timeout=15,  # Add timeout for the request
                stream=True
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            logger.debug(f"SQL Token exchange response status: {response.status_code}")
            logger.debug(f"SQL Token exchange response keys: {token_data.keys()}")
            
            # Validate response contains required tokens
            if "access_token" not in token_data:
                raise ValueError("Token exchange response missing access_token")
                
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token", ""),
                "token_type": token_data.get("token_type", "Bearer")
            }
            
        except requests.exceptions.HTTPError as e:
            error_details = ""
            try:
                error_response = e.response.json()
                error_details = f" - {error_response.get('error_description', error_response.get('error', ''))}"
            except Exception:
                error_details = f" - {e.response.text}"
            raise ConnectionError(f"Token exchange failed with HTTP {e.response.status_code}{error_details}")
        except requests.exceptions.Timeout:
            raise ConnectionError("Token exchange request timed out")
        except Exception as e:
            raise ConnectionError(f"Error during token exchange.")