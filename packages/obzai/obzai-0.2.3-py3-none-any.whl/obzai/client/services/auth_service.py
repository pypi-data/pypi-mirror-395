# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional
from pathlib import Path
import httpx
import netrc
import stat
import os

# API Config
from obzai.client.configs.api_config import APIConfig

# Custom Exceptions
from obzai.client.schemas.exceptions import APIKeyNotFoundError, APIKeyVerificationError, WrongAPIKey, SavingCredentialsFailed


NETRC_MACHINE: str = "api.obz.ai"
NETRC_LOGIN: str = "user"
NETRC_PATH: Path = Path.home() / ".netrc"


class _AuthService:
    """
    The service handles users authentication.
    """
    def __init__(self, session: httpx.Client) -> None:
        """
        Initializes an authentication service instance.

        Args:
            session: A session object from the ObzClient.
        """
        self.session = session
        self._api_key = None
        self._authenticated = False
    
    @property
    def authenticated(self) -> bool:
        """Return whether the service is currently authenticated."""
        return bool(self._authenticated)

    @property
    def api_key(self) -> str:
        """Return API key."""
        return self._api_key
    
    def _load_api_key(self) -> str:
        """
        The method attempts to load API key from a local evironment and local .netrc file.
        If not succesfull, raises APIKeyNotFoundError.
        """
        # (1) Try to load API key from local environment
        api_key = os.getenv("OBZAI_API_KEY", default=None)

        # (2) If not found or not string, read .netrc file
        if not isinstance(api_key, str):
            api_key = self._read_netrc_file()
            # (2.1) If still not found, raise error
            if not isinstance(api_key, str):
                raise APIKeyNotFoundError("API key wasn't found in evironment, nor in .netrc file.")
        
        # (3) API key found, return it
        return api_key
    
    def _verify_api_key(self, api_key: str) -> bool:
        """
        The private method which checks whether provided API key is valid.
        It calls ObzAI backend to check the provided API key.

        Args:
            api_key: A string containing API key.
        
        Returns:
            is_valid: A flag indicating whether provided API key is valid or not.
        
        Raises:
            APIKeyVerificationError when API key verification fails
        """

        # (1) Send request to the backend
        try:
            resp = self.session.post(APIConfig.get_url("auth"), json={"api_token": api_key}, timeout=50)
            resp.raise_for_status()  
        except httpx.HTTPStatusError as e:
            raise APIKeyVerificationError(f"API key verification failed with status code {e.response.status_code}.")
        except Exception as e:
            raise APIKeyVerificationError(f"API key verification failed: {e}")
        
        # (2) Convert response to a dictionary and return success info
        data = resp.json()
        if "success" in data:
            return bool(data.get("success"))
        else:
            raise KeyError("Expected response to has 'success' attribute.")

    def _save_api_key(self, api_key: str, override_credentials: bool = False) -> None:
        """
        The method saves API key in local .netrc file at home directory.
        If API key is already present in .netrc file, it doesn't override credentials by default.
        To ensure that credentials are overriden, 'override_credentials' flag must be True.

        Args:
            api_key: A API key to be cached.
            override_credentials: A bool flag which control overriding.
        
        Raises:
            SavingAPIKeyFailed when saving an API key fails.
        """
        try:
            self._write_netrc_key(api_key, override_credentials)
        except Exception as e:
            raise SavingCredentialsFailed(f"An error occured during saving API key locally: {e}")

    def authenticate(
            self, api_key: Optional[str] = None, override_credentials: bool = False
            ) -> None:
        """
        The method authenticates a user based on provided API key.
        If not provided attempts to load API key from environment variables and
        from a local .netrc file.

        Args:
            api_key: An API key string. (Optional)
            override_credentials: A bool flag ensuring overriding old credentials.
        
        Raises:
            WrongAPIKey if provided API key wasn't recognized.
        """
        # (1) First check if an API key is provided.
        if not isinstance(api_key, str):
            api_key = self._load_api_key()

        # (2) Verify whether provided or loaded API key is valid
        is_valid = self._verify_api_key(api_key)

        # (3) Save API key in local credentials
        if is_valid:
            self._save_api_key(api_key, override_credentials)
            self._api_key = api_key
            self._authenticated = True
        else:
            self._api_key = None
            self._authenticated = False
            raise WrongAPIKey("Provided API key is not valid. Authentication failed.")
    
    @staticmethod
    def _read_netrc_file(
        netrc_path: str | Path = NETRC_PATH, netrc_machine: str = NETRC_MACHINE
        ) -> Optional[str]:
        """
        Reads .netrc file from the provided path and load cached API key if available.

        Args:
            netrc_path: A path-like object to a .netrc file. Default to NETRC_PATH.
            netrc_machine: A name of machine. Default to NETRC_MACHINE.
        
        Returns:
            Returns API Key string If found in .netrc file. If not returns None.
        """
        try:
            auth = netrc.netrc(netrc_path).authenticators(netrc_machine)
            return str(auth[2]) if auth else None
        except FileNotFoundError:
            return None
        except netrc.NetrcParseError:
            return None

    @staticmethod
    def _write_netrc_key(
        api_key: str, 
        override_credentials: bool = False,
        netrc_path: str | Path = NETRC_PATH, 
        netrc_machine: str = NETRC_MACHINE, 
        netrc_login: str = NETRC_LOGIN
        ) -> None:
        """
        Write or update a single-line .netrc entry for the given machine.

        Args:
            api_key: A string containing API key
            override_credentials: A bool flag controlling overriding
            netrc_path: A path-like object. Default to NETRC_PATH.
            netrc_machine: A string with machine name. Default to NETRC_MACHINE.
            netrc_login: A string with login. Default to NETRC_LOGIN.
        """
        def _ensure_permissions(filepath: Path) -> None:
            """
            Checks current file permissions and if needed
            set read/write permissions only for a user.
            """
            current_mode = stat.S_IMODE(filepath.stat().st_mode)
            desired = stat.S_IRUSR | stat.S_IWUSR
            if current_mode != desired:
                os.chmod(filepath, desired)

        # (1) Ensure correct path format
        netrc_path = Path(netrc_path) if isinstance(netrc_path, str) else netrc_path

        # (2) Create a new entry string
        new_entry = f"machine {netrc_machine} login {netrc_login} password {api_key}\n"

        # (3) If .netrc file doesn't exist, create it and save a new entry
        if not netrc_path.exists():
            netrc_path.parent.mkdir(parents=True, exist_ok=True)
            with netrc_path.open("w") as f:
                f.write(new_entry)
            _ensure_permissions(netrc_path)
            return
    
        # (4) If .netrc exists, ensure strict permissions
        _ensure_permissions(netrc_path)
        
        # (5) Check whether entry exists. Append if not, skip/override if present
        existing_entry = netrc.netrc(netrc_path).authenticators(netrc_machine)
        if existing_entry is not None:
            # (5.1) The entry already exists, override or skip
            if override_credentials:
                # Read all lines and replace the entry for netrc_machine
                with netrc_path.open("r") as f:
                    lines = f.readlines()
                with netrc_path.open("w") as f:
                    for line in lines:
                        if line.strip().startswith(f"machine {netrc_machine} "):
                            f.write(new_entry)
                        else:
                            f.write(line)
                _ensure_permissions(netrc_path)
            else:
                return
        else:
            # (5.2) The entry not exists, append a new one
            with netrc_path.open("a") as f:
                f.write("\n" + new_entry)