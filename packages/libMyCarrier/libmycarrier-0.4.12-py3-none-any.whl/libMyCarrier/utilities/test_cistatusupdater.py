import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.utilities.cistatusupdater import (
    setup_logging, clickhouse_insert, ci_build_info, ci_deploy_info, 
    get_env_var, main
)


class TestCIStatusUpdater(unittest.TestCase):

    def setUp(self):
        # Patch clickhouse_connect
        ch_patcher = patch('libMyCarrier.utilities.cistatusupdater.clickhouse_connect')
        self.mock_clickhouse = ch_patcher.start()
        self.addCleanup(ch_patcher.stop)
        
        # Create mock client
        self.mock_client = MagicMock()
        self.mock_clickhouse.get_client.return_value = self.mock_client

    def test_setup_logging(self):
        """Test logging setup"""
        with patch('libMyCarrier.utilities.cistatusupdater.logging.basicConfig') as mock_basic_config:
            setup_logging(level=logging.DEBUG)
            mock_basic_config.assert_called_once()
            self.assertEqual(mock_basic_config.call_args[1]['level'], logging.DEBUG)

    def test_clickhouse_insert(self):
        """Test clickhouse insert function"""
        # Sample data
        test_data = [["2023-01-01", "service1", "component1", "repo", "main", "image", "1.0", "OK"]]
        
        # Call the function
        clickhouse_insert("test-host", "test-user", "test-pass", "ci.test", test_data)
        
        # Check client was created correctly
        self.mock_clickhouse.get_client.assert_called_once_with(
            host="test-host",
            port=8443,
            username="test-user",
            password="test-pass"
        )
        
        # Check insert was called correctly
        self.mock_client.insert.assert_called_once_with("ci.test", test_data, column_names='*')

    def test_clickhouse_insert_error(self):
        """Test error handling in clickhouse insert function"""
        # Make client.insert raise an exception
        self.mock_client.insert.side_effect = Exception("Insert error")
        
        # Call the function and check it raises the exception
        with self.assertRaises(Exception) as context:
            clickhouse_insert("test-host", "test-user", "test-pass", "ci.test", [])
            
        self.assertIn("Failed to insert data into ClickHouse", str(context.exception))

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_build_info_mc_format(self, mock_datetime):
        """Test ci_build_info with MC format tag"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call with MC format tag
        result = ci_build_info(
            tag="src/MC.service1.component1",
            version="1.0.0",
            branch="main",
            repo="https://github.com/org/repo.git",
            job_status="OK"
        )
        
        # Check the result
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], "2023-01-01T12:00:00.000000Z")  # timestamp
        self.assertEqual(row[1], "service1")  # service
        self.assertEqual(row[2], "component1")  # component
        self.assertEqual(row[3], "github.com/org/repo")  # build_repository
        self.assertEqual(row[4], "main")  # build_branch
        self.assertEqual(row[5], "appstack/service1/component1")  # image_repository
        self.assertEqual(row[6], "1.0.0")  # image_tag
        self.assertEqual(row[7], "OK")  # status

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_build_info_standard_format(self, mock_datetime):
        """Test ci_build_info with standard format tag"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call with standard format tag
        result = ci_build_info(
            tag="service1/component1",
            version="1.0.0",
            branch="main",
            repo="https://github.com/org/repo.git",
            job_status="OK"
        )
        
        # Check the result
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], "2023-01-01T12:00:00.000000Z")  # timestamp
        self.assertEqual(row[1], "service1")  # service
        self.assertEqual(row[2], "component1")  # component
        self.assertEqual(row[3], "github.com/org/repo")  # build_repository
        self.assertEqual(row[4], "main")  # build_branch
        self.assertEqual(row[5], "service1/component1")  # image_repository
        self.assertEqual(row[6], "1.0.0")  # image_tag
        self.assertEqual(row[7], "OK")  # status

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_deploy_info(self, mock_datetime):
        """Test ci_deploy_info function"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call the function
        result = ci_deploy_info(
            environment="prod",
            repository="https://github.com/org/service.git",
            branch="main",
            sha="abcdef123456",
            job_status="OK",
            render_status="OK",
            deploy_status="OK",
            gitops_commit="Updated config"
        )
        
        # Check the result
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], "2023-01-01T12:00:00.000000Z")  # timestamp
        self.assertEqual(row[1], "prod")  # environment
        self.assertEqual(row[2], "service")  # repository
        self.assertEqual(row[3], "main")  # branch
        self.assertEqual(row[4], "abcdef123456")  # sha
        self.assertEqual(row[5], "OK")  # status
        self.assertEqual(row[6], "GitOps-prod")  # gitops_repository
        self.assertEqual(row[7], "Updated config")  # gitops_commit

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_deploy_info_dev_env(self, mock_datetime):
        """Test ci_deploy_info function with dev environment"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call the function with dev environment
        result = ci_deploy_info(
            environment="dev",
            repository="https://github.com/org/service.git",
            branch="feature/test",
            sha="abcdef123456",
            job_status="OK",
            render_status="OK",
            deploy_status="OK",
            gitops_commit="Updated config"
        )
        
        # Check the dev environment uses different GitOps repo
        self.assertEqual(result[0][6], "GitOps-dev")  # gitops_repository

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_deploy_info_nothing_to_commit(self, mock_datetime):
        """Test ci_deploy_info function with 'Nothing to commit' message"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call the function with 'Nothing to commit'
        result = ci_deploy_info(
            environment="prod",
            repository="https://github.com/org/service.git",
            branch="main",
            sha="abcdef123456",
            job_status="OK",
            render_status="OK",
            deploy_status="OK",
            gitops_commit="Nothing to commit"
        )
        
        # Check gitops_commit is None
        self.assertIsNone(result[0][7])  # gitops_commit

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_deploy_info_in_progress(self, mock_datetime):
        """Test ci_deploy_info function with in-progress status"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call the function with in-progress status
        result = ci_deploy_info(
            environment="prod",
            repository="https://github.com/org/service.git",
            branch="main",
            sha="abcdef123456",
            job_status="IN_PROGRESS",
            render_status="OK",
            deploy_status="OK",
            gitops_commit="Updated config"
        )
        
        # Check status is IN_PROGRESS and gitops_commit is None
        self.assertEqual(result[0][5], "IN_PROGRESS")  # status
        self.assertIsNone(result[0][7])  # gitops_commit

    @patch('libMyCarrier.utilities.cistatusupdater.datetime')
    def test_ci_deploy_info_error(self, mock_datetime):
        """Test ci_deploy_info function with error status"""
        # Mock datetime to return fixed timestamp
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01T12:00:00.000000Z"
        mock_datetime.now.return_value = mock_now
        
        # Call the function with render error
        result = ci_deploy_info(
            environment="prod",
            repository="https://github.com/org/service.git",
            branch="main",
            sha="abcdef123456",
            job_status="OK",
            render_status="ERROR",
            deploy_status="OK",
            gitops_commit="Updated config"
        )
        
        # Check overall status is ERROR
        self.assertEqual(result[0][5], "ERROR")  # status

    def test_get_env_var_exists(self):
        """Test get_env_var when variable exists"""
        with patch.dict('os.environ', {'TEST_VAR': 'test_value'}):
            value = get_env_var('TEST_VAR')
            self.assertEqual(value, 'test_value')

    def test_get_env_var_missing_required(self):
        """Test get_env_var when required variable is missing"""
        with patch.dict('os.environ', {}):
            with self.assertRaises(ValueError) as context:
                get_env_var('TEST_VAR', required=True)
                
            self.assertIn("Required environment variable", str(context.exception))

    def test_get_env_var_missing_not_required(self):
        """Test get_env_var when non-required variable is missing"""
        with patch.dict('os.environ', {}):
            value = get_env_var('TEST_VAR', required=False)
            self.assertIsNone(value)

    @patch('libMyCarrier.utilities.cistatusupdater.get_env_var')
    @patch('libMyCarrier.utilities.cistatusupdater.ci_build_info')
    @patch('libMyCarrier.utilities.cistatusupdater.clickhouse_insert')
    @patch('libMyCarrier.utilities.cistatusupdater.setup_logging')
    def test_main_build_job(self, mock_setup_logging, mock_ch_insert, mock_build_info, mock_get_env):
        """Test main function with build job type"""
        # Mock environment variables
        mock_get_env.side_effect = lambda name, required=True: {
            'CH_HOST': 'test-host',
            'CH_USER': 'test-user',
            'CH_PASS_SECRET': 'test-pass',
            'JOB_TYPE': 'build',
            'JOB_STATUS': 'OK',
            'BRANCH': 'main',
            'CLONE_URL': 'https://github.com/org/repo.git',
            'TAG': 'service/component',
            'VERSION': '1.0.0'
        }.get(name)
        
        # Mock build info response
        mock_build_info.return_value = [["timestamp", "service", "component", "repo", "branch", "image", "tag", "OK"]]
        
        # Call main
        result = main()
        
        # Check setup_logging was called
        mock_setup_logging.assert_called_once()
        
        # Check ci_build_info was called with correct params
        mock_build_info.assert_called_once_with(
            'service/component', '1.0.0', 'main', 'https://github.com/org/repo.git', 'OK'
        )
        
        # Check clickhouse_insert was called with correct params
        mock_ch_insert.assert_called_once_with(
            'test-host', 'test-user', 'test-pass', 'ci.buildinfo',
            [["timestamp", "service", "component", "repo", "branch", "image", "tag", "OK"]]
        )
        
        # Check return value is 0 (success)
        self.assertEqual(result, 0)

    @patch('libMyCarrier.utilities.cistatusupdater.get_env_var')
    @patch('libMyCarrier.utilities.cistatusupdater.ci_deploy_info')
    @patch('libMyCarrier.utilities.cistatusupdater.clickhouse_insert')
    @patch('libMyCarrier.utilities.cistatusupdater.setup_logging')
    def test_main_render_job(self, mock_setup_logging, mock_ch_insert, mock_deploy_info, mock_get_env):
        """Test main function with render job type"""
        # Mock environment variables
        mock_get_env.side_effect = lambda name, required=True: {
            'CH_HOST': 'test-host',
            'CH_USER': 'test-user',
            'CH_PASS_SECRET': 'test-pass',
            'JOB_TYPE': 'render',
            'JOB_STATUS': 'OK',
            'BRANCH': 'main',
            'CLONE_URL': 'https://github.com/org/repo.git',
            'RENDER_STATUS': 'OK',
            'DEPLOY_STATUS': 'OK',
            'SHA': 'abcdef123456',
            'ENVIRONMENT': 'prod',
            'GITOPS_COMMIT': 'Updated config'
        }.get(name)
        
        # Mock deploy info response
        mock_deploy_info.return_value = [["timestamp", "prod", "repo", "main", "sha", "OK", "gitops", "commit"]]
        
        # Call main
        result = main()
        
        # Check setup_logging was called
        mock_setup_logging.assert_called_once()
        
        # Check ci_deploy_info was called with correct params
        mock_deploy_info.assert_called_once_with(
            'prod', 'https://github.com/org/repo.git', 'main', 'abcdef123456',
            'OK', 'OK', 'OK', 'Updated config'
        )
        
        # Check clickhouse_insert was called with correct params
        mock_ch_insert.assert_called_once_with(
            'test-host', 'test-user', 'test-pass', 'ci.deployinfo',
            [["timestamp", "prod", "repo", "main", "sha", "OK", "gitops", "commit"]]
        )
        
        # Check return value is 0 (success)
        self.assertEqual(result, 0)

    @patch('libMyCarrier.utilities.cistatusupdater.get_env_var')
    @patch('libMyCarrier.utilities.cistatusupdater.setup_logging')
    def test_main_invalid_job_type(self, mock_setup_logging, mock_get_env):
        """Test main function with invalid job type"""
        # Mock environment variables
        mock_get_env.side_effect = lambda name, required=True: {
            'CH_HOST': 'test-host',
            'CH_USER': 'test-user',
            'CH_PASS_SECRET': 'test-pass',
            'JOB_TYPE': 'invalid',
            'JOB_STATUS': 'OK',
            'BRANCH': 'main',
            'CLONE_URL': 'https://github.com/org/repo.git'
        }.get(name)
        
        # Call main
        result = main()
        
        # Check setup_logging was called
        mock_setup_logging.assert_called_once()
        
        # Check return value is 1 (error)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
