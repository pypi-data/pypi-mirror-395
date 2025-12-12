import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from typing import Dict, List, Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.utilities.tags import pull_tags
from libMyCarrier.error import DatabaseError


class TestTags(unittest.TestCase):

    @patch('libMyCarrier.utilities.tags.clickhouse_connect')
    def test_pull_tags_success(self, mock_clickhouse):
        # Setup mock response
        mock_client = MagicMock()
        mock_clickhouse.get_client.return_value = mock_client
        
        # Sample query result that would be returned by ClickHouse
        expected_data = [
            {'Service': 'service1', 'Component': 'component1', 'ImageTag': 'tag1'},
            {'Service': 'service2', 'Component': 'component2', 'ImageTag': 'tag2'}
        ]
        mock_client.query.return_value = expected_data
        
        # Test the function
        result = pull_tags('host', 'user', 'password', 'main', 'myrepo')
        
        # Verify the result
        self.assertEqual(result, expected_data)
        
        # Verify the correct parameters were used
        mock_clickhouse.get_client.assert_called_once_with(
            host='host', port=8443, username='user', password='password'
        )
        mock_client.query.assert_called_once()
        # Check that the query contains our branch and repo
        query_arg = mock_client.query.call_args[0][0]
        self.assertIn("%main", query_arg)
        self.assertIn("'myrepo'", query_arg)

    @patch('libMyCarrier.utilities.tags.clickhouse_connect')
    def test_pull_tags_exception(self, mock_clickhouse):
        # Setup mock to raise exception
        mock_client = MagicMock()
        mock_clickhouse.get_client.return_value = mock_client
        mock_client.query.side_effect = Exception("Database error")
        
        # Test that the function raises an exception
        with self.assertRaises(Exception) as context:
            pull_tags('host', 'user', 'password', 'main', 'myrepo')
        
        self.assertIn("Failed to pull tags from ClickHouse", str(context.exception))


if __name__ == '__main__':
    unittest.main()
