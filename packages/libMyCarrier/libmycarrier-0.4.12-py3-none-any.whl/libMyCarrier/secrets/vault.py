from typing import Dict, Optional, Any, Union
import time
import struct
import hvac
from azure.identity import ClientSecretCredential

class Vault:
    """
    The Vault class provides methods to authenticate and interact with Vault.

    Methods:
        - __init__(role_id, secret_id):
            Initializes the Vault class instance.

            :param role_id: The role ID to authenticate with.
            :param secret_id: The secret ID to authenticate with.

        - get_kv_secret(path, mount_point='secret', version=None):
            Retrieves a key-value secret from Vault.

            :param path: The path of the secret.
            :param mount_point: The mount point for the secret engine. Default is 'secret'.
            :param version: The version of the secret. Default is None.
            :return: The secret value.

        - get_dynamic_credentials(mount_point, database):
            Generates dynamic credentials for a database from Vault.

            :param mount_point: The mount point for the database engine.
            :param database: The name of the database.
            :return: The generated credentials (username and password).
    """
    
    def __init__(self, role_id: Optional[str] = None, secret_id: Optional[str] = None, 
                token: Optional[str] = None, vault_url: str = 'https://vault.mycarrier.tech'):
        """
        Initialize the class instance.

        Args:
            role_id: The role ID to authenticate with
            secret_id: The secret ID to authenticate with
            token: Direct Vault token to use for authentication
            vault_url: URL of the Vault server
            
        Raises:
            ValueError: If authentication parameters are invalid
            Exception: If authentication fails
        """
        self.Client = hvac.Client(url=vault_url)
        self.SourceCredentials = None
        
        if token is not None:
            self.Client.token = token.replace("'",'').replace('"','')
            try:
                if not self.Client.is_authenticated():
                    raise ValueError("Vault token is invalid")
            except Exception as error:
                raise ValueError(f"Vault token authentication error: {error}")
                
        elif role_id is not None and secret_id is not None:
            try:
                self.Client.auth.approle.login(
                    role_id=role_id,
                    secret_id=secret_id,
                )
            except Exception as error:
                raise Exception(f"AppRole authentication error: {error}")
        else:
            raise ValueError('Role ID and Secret ID or Vault Token are required')
            
        self.ServicePrincipalCredentials = None

    def kv_secret(self, path: str, mount_point: str = 'secrets', version: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a secret from the KV2 secret engine.
        
        Args:
            path: Path to the secret
            mount_point: Mount point of the KV2 secret engine
            version: Version of the secret to retrieve
            
        Returns:
            Dict containing the secret data
            
        Raises:
            Exception: If the secret retrieval fails
        """
        try:
            if version is None:
                output = self.Client.secrets.kv.v2.read_secret_version(
                    path=path, mount_point=mount_point)
            else:
                output = self.Client.secrets.kv.v2.read_secret_version(
                    path=path, mount_point=mount_point, version=version)
            return output
        except Exception as e:
            raise Exception(f"Failed to retrieve secret at {path}: {e}")

    def create_kv_secret(self, path: str, mount_point: str = 'secrets', **kwargs: Any) -> Dict[str, Any]:
        """
        Create or update a secret in the KV2 secret engine.
        
        Args:
            path: Path to the secret
            mount_point: Mount point of the KV2 secret engine
            kwargs: Additional data to store in the secret
            
        Returns:
            Dict containing the secret data
            
        Raises:
            Exception: If the secret creation/update fails
        """
        try:
            output = self.Client.secrets.kv.v2.create_or_update_secret(
                path=path, mount_point=mount_point, **kwargs)
            return output
        except Exception as e:
            raise Exception(f"Failed to create/update secret at {path}: {e}")

    def db_basic(self, mount_point: str, database: str) -> Dict[str, str]:
        """
        Generate basic database credentials.
        
        Args:
            mount_point: Mount point of the database secret engine
            database: Name of the database
            
        Returns:
            Dict containing the username and password
            
        Raises:
            Exception: If the credential generation fails
        """
        try:
            credentials = self.Client.secrets.database.generate_credentials(
                name=database,
                mount_point=mount_point
            )
            output = {
                'username': credentials['username'],
                'password': credentials['password']
            }
            return output
        except Exception as e:
            raise Exception(f"Failed to generate credentials for database {database}: {e}")

    def db_oauth(self, mount_point: str, role: str) -> Union[bytes, None]:
        """
        Generate OAuth database credentials.
        
        Args:
            mount_point: Mount point of the database secret engine
            role: Role name for the OAuth credentials
            
        Returns:
            Struct containing the OAuth token
            
        Raises:
            Exception: If the credential generation fails
        """
        vaultspnCreds = self.Client.secrets.azure.generate_credentials(
            name=role,
            mount_point=mount_point
        )
        i = 0
        while i < 10:
            i += 1
            try:
                spnCreds = ClientSecretCredential(client_id=vaultspnCreds['client_id'],
                                                  client_secret=vaultspnCreds['client_secret'],
                                                  tenant_id="033c43bf-e5b3-42d4-93d2-e7e0fd5e2d3d")
                time.sleep(10)
                token_bytes = spnCreds.get_token(
                    "https://database.windows.net/.default").token.encode("UTF-16-LE")
                token_struct = struct.pack(
                    f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
                return token_struct
            except Exception as e:
                print(e)
            print('SPN not ready, sleeping 30s')
            time.sleep(30)
        return None

    def azure(self, mount_point: str, role: str) -> Dict[str, Any]:
        """
        Generate Azure credentials.
        
        Args:
            mount_point: Mount point of the Azure secret engine
            role: Role name for the Azure credentials
            
        Returns:
            Dict containing the Azure credentials
            
        Raises:
            Exception: If the credential generation fails
        """
        max_retries = 5
        retry_delay = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                creds = self.Client.secrets.azure.generate_credentials(
                    name=role,
                    mount_point=mount_point
                )
                return creds
            except hvac.exceptions.InternalServerError as e:
                if "deadlocked on lock resources" in str(e):
                    print(
                        f"Deadlock detected when getting SQL dynamic creds, retrying... ({retry_count + 1}/{max_retries})")
                    retry_count += 1
                    time.sleep(retry_delay)
                else:
                    raise
        raise Exception(
            "Max retries reached for generating credentials due to deadlock")