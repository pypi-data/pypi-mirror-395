import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.storage.blob import Blob


class TestBlob(unittest.TestCase):
    
    def setUp(self):
        # Patch Azure Identity and Storage modules
        azure_identity_patcher = patch('libMyCarrier.storage.blob.DefaultAzureCredential')
        self.mock_default_credential = azure_identity_patcher.start()
        self.addCleanup(azure_identity_patcher.stop)
        
        blob_service_patcher = patch('libMyCarrier.storage.blob.BlobServiceClient')
        self.mock_blob_service_client_class = blob_service_patcher.start()
        self.addCleanup(blob_service_patcher.stop)
        
        # Create mock blob service client
        self.mock_blob_service_client = MagicMock()
        self.mock_blob_service_client_class.return_value = self.mock_blob_service_client
        
        # Create mock credential
        self.mock_credential = MagicMock()
        self.mock_default_credential.return_value = self.mock_credential

    def test_init(self):
        """Test initialization of Blob class"""
        blob = Blob("https://test.blob.core.windows.net")
        
        # Check DefaultAzureCredential was used
        self.mock_default_credential.assert_called_once()
        
        # Check BlobServiceClient was initialized correctly
        self.mock_blob_service_client_class.assert_called_once_with(
            "https://test.blob.core.windows.net", 
            credential=self.mock_credential
        )

    def test_download_blob(self):
        """Test downloading a blob"""
        # Mock blob client
        mock_blob_client = MagicMock()
        self.mock_blob_service_client.get_blob_client.return_value = mock_blob_client
        
        # Mock download_blob method
        mock_downloaded = MagicMock()
        mock_blob_client.download_blob.return_value = mock_downloaded
        
        # Create Blob instance and call download_blob
        blob = Blob("https://test.blob.core.windows.net")
        result = blob.download_blob("test-container", "test-blob")
        
        # Check result
        self.assertEqual(result, mock_downloaded)
        
        # Check blob client was created correctly
        self.mock_blob_service_client.get_blob_client.assert_called_once_with(
            container="test-container", 
            blob="test-blob"
        )
        
        # Check download_blob was called correctly
        mock_blob_client.download_blob.assert_called_once_with(
            max_concurrency=1, 
            encoding="UTF-8"
        )

    def test_download_blob_error(self):
        """Test error handling when downloading a blob"""
        # Mock blob client to raise exception
        mock_blob_client = MagicMock()
        self.mock_blob_service_client.get_blob_client.return_value = mock_blob_client
        mock_blob_client.download_blob.side_effect = Exception("Blob error")
        
        # Create Blob instance and call download_blob
        blob = Blob("https://test.blob.core.windows.net")
        
        with self.assertRaises(Exception) as context:
            blob.download_blob("test-container", "test-blob")
            
        self.assertEqual(str(context.exception), "Blob error")

    def test_delete_blob_exists(self):
        """Test deleting a blob that exists"""
        # Mock blob client
        mock_blob_client = MagicMock()
        self.mock_blob_service_client.get_blob_client.return_value = mock_blob_client
        mock_blob_client.exists.return_value = True
        
        # Create Blob instance and call delete_blob
        blob = Blob("https://test.blob.core.windows.net")
        blob.delete_blob("test-container", "test-blob")
        
        # Check blob client was created correctly
        self.mock_blob_service_client.get_blob_client.assert_called_once_with(
            container="test-container", 
            blob="test-blob"
        )
        
        # Check exists and delete_blob were called
        mock_blob_client.exists.assert_called_once()
        mock_blob_client.delete_blob.assert_called_once()

    def test_delete_blob_not_exists(self):
        """Test deleting a blob that doesn't exist"""
        # Mock blob client
        mock_blob_client = MagicMock()
        self.mock_blob_service_client.get_blob_client.return_value = mock_blob_client
        mock_blob_client.exists.return_value = False
        
        # Create Blob instance and call delete_blob
        blob = Blob("https://test.blob.core.windows.net")
        blob.delete_blob("test-container", "test-blob")
        
        # Check blob client was created correctly
        self.mock_blob_service_client.get_blob_client.assert_called_once_with(
            container="test-container", 
            blob="test-blob"
        )
        
        # Check exists was called and delete_blob was not called
        mock_blob_client.exists.assert_called_once()
        mock_blob_client.delete_blob.assert_not_called()

    def test_delete_blob_error(self):
        """Test error handling when deleting a blob"""
        # Mock blob client to raise exception
        mock_blob_client = MagicMock()
        self.mock_blob_service_client.get_blob_client.return_value = mock_blob_client
        mock_blob_client.exists.return_value = True
        mock_blob_client.delete_blob.side_effect = Exception("Delete error")
        
        # Create Blob instance and call delete_blob
        blob = Blob("https://test.blob.core.windows.net")
        
        with self.assertRaises(Exception) as context:
            blob.delete_blob("test-container", "test-blob")
            
        self.assertEqual(str(context.exception), "Delete error")


if __name__ == '__main__':
    unittest.main()
