import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.error import (
    MyCarrierError, VaultError, DatabaseError, GitHubError, 
    StorageError, KafkaError, ConfigError
)


class TestError(unittest.TestCase):

    def test_error_inheritance(self):
        """Test that all error classes inherit from MyCarrierError"""
        self.assertTrue(issubclass(VaultError, MyCarrierError))
        self.assertTrue(issubclass(DatabaseError, MyCarrierError))
        self.assertTrue(issubclass(GitHubError, MyCarrierError))
        self.assertTrue(issubclass(StorageError, MyCarrierError))
        self.assertTrue(issubclass(KafkaError, MyCarrierError))
        self.assertTrue(issubclass(ConfigError, MyCarrierError))
        
    def test_error_instantiation(self):
        """Test that error classes can be instantiated with a message"""
        msg = "Test error message"
        
        # Base error
        error = MyCarrierError(msg)
        self.assertEqual(str(error), msg)
        
        # Specific errors
        errors = [
            VaultError(msg),
            DatabaseError(msg),
            GitHubError(msg),
            StorageError(msg),
            KafkaError(msg),
            ConfigError(msg)
        ]
        
        for error in errors:
            self.assertEqual(str(error), msg)
            self.assertIsInstance(error, MyCarrierError)


if __name__ == '__main__':
    unittest.main()
