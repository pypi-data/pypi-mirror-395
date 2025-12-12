import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock, call
import types

# Import the module to be tested
from libMyCarrier.utilities.message import KafkaMessageProducer, create_producer, main


class TestKafkaMessageProducer(unittest.TestCase):
    def setUp(self):
        """Save original modules and environment before each test"""
        self.original_modules = sys.modules.copy()
        self.original_env = os.environ.copy()
        
        # Set up environment variables needed for testing
        os.environ["BROKER_ADDR"] = "test-broker:9092"
        os.environ["SASL_UN"] = "test-username"
        os.environ["SASL_PW"] = "test-password"

    def tearDown(self):
        """Restore original modules and environment after each test"""
        sys.modules.clear()
        sys.modules.update(self.original_modules)
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_init(self, mock_kafka_producer, mock_ssl_context):
        mock_ssl_context.return_value = "mock_context"
        mock_producer = MagicMock()
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        
        mock_kafka_producer.assert_called_once_with(
            bootstrap_servers="test-broker:9092",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username="test-username",
            sasl_plain_password="test-password",
            security_protocol="SASL_SSL",
            ssl_context="mock_context"
        )
        self.assertEqual(producer.broker, "test-broker:9092")
        self.assertEqual(producer.sasl_un, "test-username")
        self.assertEqual(producer.sasl_pw, "test-password")
        self.assertEqual(producer.producer, mock_producer)

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_is_connected_true(self, mock_kafka_producer, mock_ssl_context):
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.return_value = True
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        self.assertTrue(producer.is_connected())
        mock_producer.bootstrap_connected.assert_called_once()

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_is_connected_false(self, mock_kafka_producer, mock_ssl_context):
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.return_value = False
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        self.assertFalse(producer.is_connected())

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_is_connected_exception(self, mock_kafka_producer, mock_ssl_context):
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.side_effect = Exception("Connection error")
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        self.assertFalse(producer.is_connected())

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    @patch("libMyCarrier.utilities.message.CloudEvent")  # Fixed patch path to match the actual import
    @patch("libMyCarrier.utilities.message.to_json")     # Fixed patch path to match the actual import
    def test_send_message(self, mock_to_json, mock_cloud_event, mock_kafka_producer, mock_ssl_context):
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.return_value = True
        mock_kafka_producer.return_value = mock_producer
        
        mock_event = MagicMock()
        mock_cloud_event.return_value = mock_event
        mock_to_json.return_value = '{"mock": "event"}'
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        producer.send_message("test-topic", "test-event", "test-source", {"test": "data"})
        
        # Test CloudEvent is constructed with correct attributes
        mock_cloud_event.assert_called_once_with(
            {"type": "test-event", "source": "test-source"},
            {"test": "data"}
        )
        mock_to_json.assert_called_once_with(mock_event)
        
        # Test message is properly encoded to bytes before sending
        # This is the key change to validate encoding happens correctly
        mock_producer.send.assert_called_once_with("test-topic", '{"mock": "event"}'.encode('utf-8'))
        mock_producer.flush.assert_called_once()

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_send_message_with_json_payload(self, mock_kafka_producer, mock_ssl_context):
        """Test that complex JSON data is properly converted to CloudEvent format"""
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.return_value = True
        mock_kafka_producer.return_value = mock_producer
        
        complex_data = {
            "id": 12345,
            "customer": {
                "name": "Test Customer",
                "email": "test@example.com"
            },
            "items": [
                {"product": "A", "quantity": 2},
                {"product": "B", "quantity": 1}
            ]
        }
        
        with patch("libMyCarrier.utilities.message.CloudEvent") as mock_cloud_event, \
             patch("libMyCarrier.utilities.message.to_json") as mock_to_json:
             
            mock_event = MagicMock()
            mock_cloud_event.return_value = mock_event
            mock_to_json.return_value = json.dumps(complex_data)
            
            producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
            producer.send_message("test-topic", "test-event", "test-source", complex_data)
            
            # Verify the complex data was passed correctly
            mock_cloud_event.assert_called_once_with(
                {"type": "test-event", "source": "test-source"},
                complex_data
            )
            mock_to_json.assert_called_once_with(mock_event)
            mock_producer.send.assert_called_once()

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_send_message_connection_failure(self, mock_kafka_producer, mock_ssl_context):
        """Test behavior when connection fails and cannot be recovered"""
        mock_producer = MagicMock()
        # Both initial and retry connection attempts fail
        mock_producer.bootstrap_connected.return_value = False
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        
        with self.assertRaises(ConnectionError) as context:
            producer.send_message("test-topic", "test-event", "test-source", {"test": "data"})
            
        self.assertIn("Failed to connect to Kafka broker", str(context.exception))

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    def test_send_message_reconnect(self, mock_kafka_producer, mock_ssl_context):
        mock_producer = MagicMock()
        # First call to bootstrap_connected returns False, second call returns True
        mock_producer.bootstrap_connected.side_effect = [False, True]
        mock_kafka_producer.return_value = mock_producer
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        
        # Reset the mock to set up the behavior for the send_message call
        mock_kafka_producer.reset_mock()
        mock_producer.bootstrap_connected.side_effect = [False, True]
        
        with patch("libMyCarrier.utilities.message.CloudEvent") as mock_cloud_event, \
             patch("libMyCarrier.utilities.message.to_json") as mock_to_json:  # Fixed patch paths
             
            mock_event = MagicMock()
            mock_cloud_event.return_value = mock_event
            mock_to_json.return_value = '{"mock": "event"}'
            
            producer.send_message("test-topic", "test-event", "test-source", {"test": "data"})
            
            # Verify producer was recreated
            self.assertEqual(mock_kafka_producer.call_count, 1)
            mock_producer.send.assert_called_once()
            mock_producer.flush.assert_called_once()

    @patch("ssl._create_unverified_context")
    @patch("kafka.KafkaProducer")
    @patch("libMyCarrier.utilities.message.CloudEvent")
    @patch("libMyCarrier.utilities.message.to_json")
    def test_send_message_handles_string_and_bytes(self, mock_to_json, mock_cloud_event, mock_kafka_producer, mock_ssl_context):
        """Test that send_message correctly handles both string and bytes message formats"""
        mock_producer = MagicMock()
        mock_producer.bootstrap_connected.return_value = True
        mock_kafka_producer.return_value = mock_producer
        
        mock_event = MagicMock()
        mock_cloud_event.return_value = mock_event
        
        producer = KafkaMessageProducer("test-broker:9092", "test-username", "test-password")
        
        # Test scenario 1: to_json returns a string
        mock_to_json.return_value = '{"mock": "string_event"}'
        producer.send_message("test-topic", "test-event", "test-source", {"test": "data"})
        
        # Verify string was properly encoded to bytes
        mock_producer.send.assert_called_with("test-topic", '{"mock": "string_event"}'.encode('utf-8'))
        
        # Test scenario 2: to_json already returns bytes
        mock_to_json.return_value = b'{"mock": "bytes_event"}'
        producer.send_message("test-topic", "test-event", "test-source", {"test": "data"})
        
        # Verify bytes were sent without additional encoding
        mock_producer.send.assert_called_with("test-topic", b'{"mock": "bytes_event"}')
        
        # Verify flush was called after each send
        self.assertEqual(mock_producer.flush.call_count, 2)


class TestCreateProducer(unittest.TestCase):
    def setUp(self):
        self.original_env = os.environ.copy()
        self.original_modules = sys.modules.copy()
        
    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)
        sys.modules.clear()
        sys.modules.update(self.original_modules)

    @patch("libMyCarrier.utilities.message.KafkaMessageProducer")
    def test_create_producer_success(self, mock_kafka_producer_class):
        # Set up test environment
        os.environ["BROKER_ADDR"] = "test-broker:9092"
        os.environ["SASL_UN"] = "test-username"
        os.environ["SASL_PW"] = "test-password"
        
        mock_kafka_producer = MagicMock()
        mock_kafka_producer_class.return_value = mock_kafka_producer
        
        result = create_producer()
        
        mock_kafka_producer_class.assert_called_once_with(
            "test-broker:9092", "test-username", "test-password"
        )
        self.assertEqual(result, mock_kafka_producer)

    def test_create_producer_missing_env(self):
        # Clear environment variables
        os.environ.clear()
        
        with self.assertRaises(ValueError) as context:
            create_producer()
        
        self.assertIn("Missing required environment variables", str(context.exception))


class TestMain(unittest.TestCase):
    def setUp(self):
        self.original_argv = sys.argv
        self.original_modules = sys.modules.copy()
        
    def tearDown(self):
        sys.argv = self.original_argv
        sys.modules.clear()
        sys.modules.update(self.original_modules)

    @patch("libMyCarrier.utilities.message.create_producer")
    @patch("sys.stdout")
    def test_main_success(self, mock_stdout, mock_create_producer):
        mock_producer = MagicMock()
        mock_create_producer.return_value = mock_producer
        
        sys.argv = [
            "message.py",
            "test-topic",
            "--type", "test-event",
            "--source", "test-source",
            "--data", '{"test": "data"}'
        ]
        
        result = main()
        
        mock_producer.send_message.assert_called_once_with(
            "test-topic", "test-event", "test-source", {"test": "data"}
        )
        self.assertEqual(result, 0)

    @patch("sys.stdout")
    def test_main_invalid_json(self, mock_stdout):
        sys.argv = [
            "message.py",
            "test-topic",
            "--type", "test-event",
            "--source", "test-source",
            "--data", 'invalid-json'
        ]
        
        result = main()
        
        self.assertEqual(result, 1)

    @patch("libMyCarrier.utilities.message.create_producer")
    @patch("sys.stdout")
    def test_main_value_error(self, mock_stdout, mock_create_producer):
        mock_create_producer.side_effect = ValueError("Test error")
        
        sys.argv = [
            "message.py",
            "test-topic",
            "--type", "test-event",
            "--source", "test-source",
            "--data", '{"test": "data"}'
        ]
        
        result = main()
        
        self.assertEqual(result, 1)

    @patch("libMyCarrier.utilities.message.create_producer")
    @patch("sys.stdout")
    def test_main_generic_exception(self, mock_stdout, mock_create_producer):
        mock_producer = MagicMock()
        mock_producer.send_message.side_effect = Exception("Test exception")
        mock_create_producer.return_value = mock_producer
        
        sys.argv = [
            "message.py",
            "test-topic",
            "--type", "test-event",
            "--source", "test-source",
            "--data", '{"test": "data"}'
        ]
        
        result = main()
        
        self.assertEqual(result, 1)

    @patch("libMyCarrier.utilities.message.create_producer")
    def test_main_with_special_characters(self, mock_create_producer):
        """Test handling of special characters in JSON data"""
        mock_producer = MagicMock()
        mock_create_producer.return_value = mock_producer
        
        # Test with data containing special characters
        sys.argv = [
            "message.py",
            "test-topic",
            "--type", "test-event",
            "--source", "test-source",
            "--data", '{"message": "Special: üñîçøðé & symbols: ®©™!@#$%^&*"}'
        ]
        
        result = main()
        
        expected_data = {"message": "Special: üñîçøðé & symbols: ®©™!@#$%^&*"}
        mock_producer.send_message.assert_called_once_with(
            "test-topic", "test-event", "test-source", expected_data
        )
        self.assertEqual(result, 0)

    @patch("argparse.ArgumentParser.parse_args")
    def test_main_missing_required_args(self, mock_parse_args):
        """Test behavior when required arguments are missing"""
        mock_parse_args.side_effect = SystemExit(2)
        
        with self.assertRaises(SystemExit) as context:
            main()
            
        self.assertEqual(context.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
