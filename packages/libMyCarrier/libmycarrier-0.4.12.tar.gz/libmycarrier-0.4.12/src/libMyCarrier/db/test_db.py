import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import sys
import os
import contextlib

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from libMyCarrier.db.db import dbConnection


class TestDbConnection(unittest.TestCase):

    def setUp(self):
        # Create mock for pyodbc and snowflake.connector
        pyodbc_patcher = patch('libMyCarrier.db.db.dbConnection.pyodbc')
        self.mock_pyodbc = pyodbc_patcher.start()
        self.addCleanup(pyodbc_patcher.stop)
        
        snowflake_patcher = patch('libMyCarrier.db.db.dbConnection.snowflake')
        self.mock_snowflake = snowflake_patcher.start()
        self.addCleanup(snowflake_patcher.stop)
        
        # Create a mock connection for testing
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    def test_init(self):
        """Test that dbConnection initializes correctly"""
        db_conn = dbConnection(self.mock_connection)
        self.assertEqual(db_conn.connection, self.mock_connection)

    def test_cursor_property(self):
        """Test the cursor property"""
        db_conn = dbConnection(self.mock_connection)
        db_conn.cursor()
        self.mock_connection.cursor.assert_called_once()

    def test_from_sql_token_auth(self):
        """Test from_sql factory method with token auth"""
        self.mock_pyodbc.connect.return_value = self.mock_connection
        
        # Test token authentication
        db_conn = dbConnection.from_sql(
            server="test-server",
            port=1433,
            db_name="test-db",
            auth_method="token",
            token="test-token"
        )
        
        self.assertEqual(db_conn.connection, self.mock_connection)
        self.mock_pyodbc.connect.assert_called_once()
        # Check that token was used in the connection
        self.assertIn(1256, self.mock_pyodbc.connect.call_args[1]['attrs_before'])
        
    def test_from_sql_basic_auth(self):
        """Test from_sql factory method with basic auth"""
        self.mock_pyodbc.connect.return_value = self.mock_connection
        
        # Test basic authentication
        db_conn = dbConnection.from_sql(
            server="test-server",
            port=1433,
            db_name="test-db",
            auth_method="basic",
            username="test-user",
            password="test-pass"
        )
        
        self.assertEqual(db_conn.connection, self.mock_connection)
        self.mock_pyodbc.connect.assert_called_once()
        # Check that username and password were used in the connection string
        conn_string = self.mock_pyodbc.connect.call_args[0][0]
        self.assertIn("UID=test-user", conn_string)
        self.assertIn("PWD=test-pass", conn_string)

    def test_from_sql_invalid_auth(self):
        """Test from_sql factory method with invalid auth"""
        with self.assertRaises(ValueError) as context:
            dbConnection.from_sql(
                server="test-server",
                port=1433,
                db_name="test-db",
                auth_method="invalid"
            )
        self.assertIn("Invalid auth_method", str(context.exception))

    def test_from_snowflake(self):
        """Test from_snowflake factory method"""
        self.mock_snowflake.connector.connect.return_value = self.mock_connection
        
        db_conn = dbConnection.from_snowflake(
            user="test-user",
            password="test-pass",
            role="test-role",
            account="test-account",
            warehouse="test-warehouse",
            database="test-db",
            schema="test-schema"
        )
        
        self.assertEqual(db_conn.connection, self.mock_connection)
        self.mock_snowflake.connector.connect.assert_called_once_with(
            user="test-user",
            password="test-pass",
            role="test-role",
            account="test-account",
            warehouse="test-warehouse",
            database="test-db",
            schema="test-schema"
        )

    def test_query_fetch_one(self):
        """Test query method with fetch one"""
        db_conn = dbConnection(self.mock_connection)
        expected_result = {"col1": "val1"}
        self.mock_cursor.fetchone.return_value = expected_result
        
        result = db_conn.query("SELECT * FROM test", outputResults="one")
        
        self.assertEqual(result, expected_result)
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM test", ())
        self.mock_cursor.fetchone.assert_called_once()

    def test_query_fetch_all(self):
        """Test query method with fetch all"""
        db_conn = dbConnection(self.mock_connection)
        expected_result = [{"col1": "val1"}, {"col1": "val2"}]
        self.mock_cursor.fetchall.return_value = expected_result
        
        result = db_conn.query("SELECT * FROM test", outputResults="all")
        
        self.assertEqual(result, expected_result)
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM test", ())
        self.mock_cursor.fetchall.assert_called_once()

    def test_query_with_params(self):
        """Test query method with parameters"""
        db_conn = dbConnection(self.mock_connection)
        params = (1, 'test')
        
        db_conn.query("INSERT INTO test VALUES (?, ?)", params=params)
        
        self.mock_cursor.execute.assert_called_once_with("INSERT INTO test VALUES (?, ?)", params)

    def test_close(self):
        """Test close method"""
        db_conn = dbConnection(self.mock_connection)
        
        db_conn.close()
        
        self.mock_connection.close.assert_called_once()

    def test_transaction_commit(self):
        """Test transaction context manager with successful commit"""
        db_conn = dbConnection(self.mock_connection)
        
        with db_conn.transaction():
            pass  # No operations
            
        self.mock_connection.commit.assert_called_once()
        self.mock_connection.rollback.assert_not_called()

    def test_transaction_rollback(self):
        """Test transaction context manager with rollback on exception"""
        db_conn = dbConnection(self.mock_connection)
        
        try:
            with db_conn.transaction():
                raise Exception("Test exception")
        except Exception:
            pass
            
        self.mock_connection.commit.assert_not_called()
        self.mock_connection.rollback.assert_called_once()


if __name__ == '__main__':
    unittest.main()
