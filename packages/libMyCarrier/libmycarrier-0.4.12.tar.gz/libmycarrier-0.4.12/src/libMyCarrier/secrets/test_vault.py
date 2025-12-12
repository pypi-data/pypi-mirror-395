import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import hvac

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.secrets.vault import Vault


class TestVault(unittest.TestCase):
    
    def setUp(self):
        # Patch hvac client
        hvac_patcher = patch('libMyCarrier.secrets.vault.hvac.Client')
        self.mock_hvac_client = hvac_patcher.start()
        self.addCleanup(hvac_patcher.stop)
        
        # Create mock client instance
        self.mock_client = MagicMock()
        self.mock_hvac_client.return_value = self.mock_client
        
        # Mock is_authenticated to return True by default
        self.mock_client.is_authenticated.return_value = True

    def test_init_with_token(self):
        """Test initialization with token"""
        vault = Vault(token="test-token")
        
        self.assertEqual(self.mock_client.token, "test-token")
        self.mock_client.is_authenticated.assert_called_once()

    def test_init_with_token_quotes(self):
        """Test initialization with token containing quotes"""
        vault = Vault(token="'test-token'")
        
        self.assertEqual(self.mock_client.token, "test-token")
        self.mock_client.is_authenticated.assert_called_once()
        
        # Test double quotes too
        vault = Vault(token='"test-token"')
        self.assertEqual(self.mock_client.token, "test-token")

    def test_init_with_invalid_token(self):
        """Test initialization with invalid token"""
        self.mock_client.is_authenticated.return_value = False
        
        with self.assertRaises(ValueError) as context:
            vault = Vault(token="invalid-token")
            
        self.assertIn("Vault token is invalid", str(context.exception))

    def test_init_with_token_auth_error(self):
        """Test initialization with token that causes an authentication error"""
        self.mock_client.is_authenticated.side_effect = Exception("Auth error")
        
        with self.assertRaises(ValueError) as context:
            vault = Vault(token="test-token")
            
        self.assertIn("Vault token authentication error", str(context.exception))

    def test_init_with_approle(self):
        """Test initialization with AppRole"""
        vault = Vault(role_id="test-role", secret_id="test-secret")
        
        self.mock_client.auth.approle.login.assert_called_once_with(
            role_id="test-role",
            secret_id="test-secret"
        )

    def test_init_with_approle_error(self):
        """Test initialization with AppRole that fails"""
        self.mock_client.auth.approle.login.side_effect = Exception("AppRole error")
        
        with self.assertRaises(Exception) as context:
            vault = Vault(role_id="test-role", secret_id="test-secret")
            
        self.assertIn("AppRole authentication error", str(context.exception))

    def test_init_missing_auth(self):
        """Test initialization without required auth parameters"""
        with self.assertRaises(ValueError) as context:
            vault = Vault()
            
        self.assertIn("Role ID and Secret ID or Vault Token are required", str(context.exception))

    def test_kv_secret(self):
        """Test retrieving KV secret"""
        # Mock the read_secret_version method
        mock_output = {"data": {"data": {"key": "value"}}}
        self.mock_client.secrets.kv.v2.read_secret_version.return_value = mock_output
        
        vault = Vault(token="test-token")
        result = vault.kv_secret("test-path")
        
        self.assertEqual(result, mock_output)
        self.mock_client.secrets.kv.v2.read_secret_version.assert_called_once_with(
            path="test-path", mount_point="secrets"
        )

    def test_kv_secret_with_version(self):
        """Test retrieving KV secret with specific version"""
        # Mock the read_secret_version method
        mock_output = {"data": {"data": {"key": "value"}}}
        self.mock_client.secrets.kv.v2.read_secret_version.return_value = mock_output
        
        vault = Vault(token="test-token")
        result = vault.kv_secret("test-path", version=2)
        
        self.assertEqual(result, mock_output)
        self.mock_client.secrets.kv.v2.read_secret_version.assert_called_once_with(
            path="test-path", mount_point="secrets", version=2
        )

    def test_kv_secret_error(self):
        """Test error handling when retrieving KV secret"""
        # Make read_secret_version raise an exception
        self.mock_client.secrets.kv.v2.read_secret_version.side_effect = Exception("KV error")
        
        vault = Vault(token="test-token")
        with self.assertRaises(Exception) as context:
            vault.kv_secret("test-path")
            
        self.assertIn("Failed to retrieve secret", str(context.exception))

    def test_create_kv_secret(self):
        """Test creating KV secret"""
        # Mock the create_or_update_secret method
        mock_output = {"data": {"created_time": "now"}}
        self.mock_client.secrets.kv.v2.create_or_update_secret.return_value = mock_output
        
        vault = Vault(token="test-token")
        result = vault.create_kv_secret("test-path", secret={"key": "value"})
        
        self.assertEqual(result, mock_output)
        self.mock_client.secrets.kv.v2.create_or_update_secret.assert_called_once_with(
            path="test-path", mount_point="secrets", secret={"key": "value"}
        )

    def test_create_kv_secret_error(self):
        """Test error handling when creating KV secret"""
        # Make create_or_update_secret raise an exception
        self.mock_client.secrets.kv.v2.create_or_update_secret.side_effect = Exception("Create error")
        
        vault = Vault(token="test-token")
        with self.assertRaises(Exception) as context:
            vault.create_kv_secret("test-path", secret={"key": "value"})
            
        self.assertIn("Failed to create/update secret", str(context.exception))

    def test_db_basic(self):
        """Test generating basic database credentials"""
        # Mock the generate_credentials method
        mock_creds = {"username": "test-user", "password": "test-pass"}
        self.mock_client.secrets.database.generate_credentials.return_value = mock_creds
        
        vault = Vault(token="test-token")
        result = vault.db_basic("database", "test-db")
        
        self.assertEqual(result, mock_creds)
        self.mock_client.secrets.database.generate_credentials.assert_called_once_with(
            name="test-db", mount_point="database"
        )

    def test_db_basic_error(self):
        """Test error handling when generating database credentials"""
        # Make generate_credentials raise an exception
        self.mock_client.secrets.database.generate_credentials.side_effect = Exception("DB error")
        
        vault = Vault(token="test-token")
        with self.assertRaises(Exception) as context:
            vault.db_basic("database", "test-db")
            
        self.assertIn("Failed to generate credentials", str(context.exception))

    @patch('libMyCarrier.secrets.vault.ClientSecretCredential')
    @patch('libMyCarrier.secrets.vault.struct')
    @patch('libMyCarrier.secrets.vault.time.sleep')
    def test_db_oauth(self, mock_sleep, mock_struct, mock_client_secret):
        """Test generating OAuth database credentials"""
        # Mock Azure generate_credentials
        mock_azure_creds = {"client_id": "test-id", "client_secret": "test-secret"}
        self.mock_client.secrets.azure.generate_credentials.return_value = mock_azure_creds
        
        # Mock ClientSecretCredential and token
        mock_spn = MagicMock()
        mock_client_secret.return_value = mock_spn
        mock_token = MagicMock()
        mock_token.token = "test-token"
        mock_spn.get_token.return_value = mock_token
        
        # Mock struct.pack
        mock_struct.pack.return_value = b"packed-token"
        
        vault = Vault(token="test-token")
        result = vault.db_oauth("azure", "test-role")
        
        self.assertEqual(result, b"packed-token")
        
        # Check Azure credentials were generated
        self.mock_client.secrets.azure.generate_credentials.assert_called_once_with(
            name="test-role", mount_point="azure"
        )
        
        # Check ClientSecretCredential was initialized correctly
        mock_client_secret.assert_called_once_with(
            client_id="test-id",
            client_secret="test-secret",
            tenant_id="033c43bf-e5b3-42d4-93d2-e7e0fd5e2d3d"
        )
        
        # Check token was requested and packed
        mock_spn.get_token.assert_called_once_with("https://database.windows.net/.default")
        mock_struct.pack.assert_called()

    def test_azure(self):
        """Test generating Azure credentials"""
        # Mock the generate_credentials method
        mock_creds = {"client_id": "test-id", "client_secret": "test-secret"}
        self.mock_client.secrets.azure.generate_credentials.return_value = mock_creds
        
        vault = Vault(token="test-token")
        result = vault.azure("azure", "test-role")
        
        self.assertEqual(result, mock_creds)
        self.mock_client.secrets.azure.generate_credentials.assert_called_once_with(
            name="test-role", mount_point="azure"
        )

    def test_azure_deadlock_retry(self):
        """Test retrying on deadlock when generating Azure credentials"""
        # Mock generate_credentials to fail with deadlock once then succeed
        mock_creds = {"client_id": "test-id", "client_secret": "test-secret"}
        deadlock_error = hvac.exceptions.InternalServerError("deadlocked on lock resources")
        self.mock_client.secrets.azure.generate_credentials.side_effect = [
            deadlock_error, mock_creds
        ]
        
        # Mock time.sleep to avoid delays in test
        with patch('libMyCarrier.secrets.vault.time.sleep') as mock_sleep:
            vault = Vault(token="test-token")
            result = vault.azure("azure", "test-role")
            
            self.assertEqual(result, mock_creds)
            self.assertEqual(
                self.mock_client.secrets.azure.generate_credentials.call_count, 2
            )
            mock_sleep.assert_called_once()

    def test_azure_max_retries(self):
        """Test max retries exceeded when generating Azure credentials"""
        # Mock generate_credentials to always fail with deadlock
        deadlock_error = hvac.exceptions.InternalServerError("deadlocked on lock resources")
        self.mock_client.secrets.azure.generate_credentials.side_effect = deadlock_error
        
        # Mock time.sleep to avoid delays in test
        with patch('libMyCarrier.secrets.vault.time.sleep'):
            vault = Vault(token="test-token")
            
            with self.assertRaises(Exception) as context:
                result = vault.azure("azure", "test-role")
                
            self.assertIn("Max retries reached", str(context.exception))
            self.assertEqual(
                self.mock_client.secrets.azure.generate_credentials.call_count, 5
            )


if __name__ == '__main__':
    unittest.main()
