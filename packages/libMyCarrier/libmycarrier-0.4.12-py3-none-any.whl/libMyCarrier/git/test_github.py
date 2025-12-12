import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
import time
import base64
import requests  # Add this import for the requests module
from cryptography.hazmat.primitives.asymmetric import rsa

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.git.github import githubAuth


class TestGitHubAuth(unittest.TestCase):
    
    def setUp(self):
        # Generate a private key for testing
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Mock the load_pem_private_key function to return our test key
        patcher = patch('libMyCarrier.git.github.load_pem_private_key')
        self.mock_load_key = patcher.start()
        self.mock_load_key.return_value = self.private_key
        self.addCleanup(patcher.stop)
        
        # Mock requests
        requests_patcher = patch('libMyCarrier.git.github.requests')
        self.mock_requests = requests_patcher.start()
        self.addCleanup(requests_patcher.stop)
        
        # Mock response with a token
        mock_response = MagicMock()
        mock_response.content = json.dumps({"token": "test_token"}).encode('utf-8')
        mock_response.raise_for_status = MagicMock()
        self.mock_requests.post.return_value = mock_response

    def test_base64url_encode(self):
        """Test the _base64url_encode method"""
        auth = githubAuth("test_pem", "test_app_id", "test_installation_id")
        
        # Test string input
        result = auth._base64url_encode("test-data")
        self.assertEqual(result, "dGVzdC1kYXRh")
        
        # Test bytes input
        result = auth._base64url_encode(b"test-data")
        self.assertEqual(result, "dGVzdC1kYXRh")
        
        # Test padding removal
        # "test" base64-encoded is "dGVzdA==" with padding
        result = auth._base64url_encode("test")
        self.assertEqual(result, "dGVzdA")  # No padding
    
    @patch('libMyCarrier.git.github.time')
    def test_generate_jwt(self, mock_time):
        """Test the _generate_jwt method"""
        # Mock time to get consistent JWT token
        mock_time.time.return_value = 1600000000
        
        auth = githubAuth("test_pem", "test_app_id", "test_installation_id")
        
        # Don't mock the sign method itself, but patch the parts we know
        # so we can test the method's actual signing logic
        with patch.object(auth, '_base64url_encode') as mock_encode:
            # Setup the encode method to return predictable values for header and payload
            mock_encode.side_effect = ["header_encoded", "payload_encoded", "signature_encoded"]
            
            jwt = auth._generate_jwt()
            
            # Check the final JWT format
            self.assertEqual(jwt, "header_encoded.payload_encoded.signature_encoded")
            
            # Verify encode was called with the right parameters
            calls = mock_encode.call_args_list
            self.assertEqual(len(calls), 3)  # Called three times
            
            # First call should be for header
            header_call = json.loads(calls[0][0][0])
            self.assertEqual(header_call, {"alg": "RS256", "typ": "JWT"})
            
            # Second call should be for payload
            payload_call = json.loads(calls[1][0][0])
            self.assertEqual(payload_call["iat"], 1600000000)
            self.assertEqual(payload_call["exp"], 1600000600)  # iat + 600
            self.assertEqual(payload_call["iss"], "test_app_id")

    def test_get_auth_token(self):
        """Test the get_auth_token method"""
        # Create a basic auth instance
        auth = githubAuth("test_pem", "test_app_id", "test_installation_id")
        
        # Reset mock to clear initialization call
        self.mock_requests.post.reset_mock()
        
        # Replace the internal _generate_jwt method
        auth._generate_jwt = MagicMock(return_value='test.jwt.token')
        
        # Call get_auth_token directly to test it
        token = auth.get_auth_token()
        
        # Check that the token was returned correctly
        self.assertEqual(token, "test_token")
        
        # Check that the correct API call was made
        self.mock_requests.post.assert_called_once()
        url = self.mock_requests.post.call_args[0][0]
        headers = self.mock_requests.post.call_args[1]['headers']
        
        self.assertEqual(url, "https://api.github.com/app/installations/test_installation_id/access_tokens")
        self.assertEqual(headers["Authorization"], "Bearer test.jwt.token")
        self.assertEqual(headers["Accept"], "application/vnd.github+json")
        self.assertEqual(headers["X-GitHub-Api-Version"], "2022-11-28")

    def test_get_auth_token_request_exception(self):
        """Test error handling for request exceptions"""
        # Use a standard Python exception that will definitely exist 
        self.mock_requests.post.side_effect = Exception("API error")
        
        with self.assertRaises(RuntimeError) as context:
            githubAuth("test_pem", "test_app_id", "test_installation_id")
            
        self.assertIn("GitHub API request failed", str(context.exception))

    def test_get_auth_token_json_exception(self):
        """Test error handling for JSON parsing exceptions"""
        # Make response.content be invalid JSON
        mock_response = MagicMock()
        mock_response.content = b"Not valid JSON"
        mock_response.raise_for_status = MagicMock()
        self.mock_requests.post.return_value = mock_response
        
        with self.assertRaises(RuntimeError) as context:
            githubAuth("test_pem", "test_app_id", "test_installation_id")
            
        self.assertIn("Failed to parse GitHub response", str(context.exception))

    def test_http_error_handling(self):
        """Test handling of HTTP errors"""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock(side_effect=requests.exceptions.HTTPError("404 Client Error"))
        self.mock_requests.post.return_value = mock_response
        
        with self.assertRaises(RuntimeError) as context:
            githubAuth("test_pem", "test_app_id", "test_installation_id")
            
        self.assertIn("GitHub API request failed", str(context.exception))

    def test_missing_token_in_response(self):
        """Test handling of missing token in the response"""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"not_token": "something_else"}).encode('utf-8')
        mock_response.raise_for_status = MagicMock()
        self.mock_requests.post.return_value = mock_response
        
        with self.assertRaises(RuntimeError) as context:
            githubAuth("test_pem", "test_app_id", "test_installation_id")
            
        self.assertIn("Failed to parse GitHub response", str(context.exception))


if __name__ == '__main__':
    unittest.main()
