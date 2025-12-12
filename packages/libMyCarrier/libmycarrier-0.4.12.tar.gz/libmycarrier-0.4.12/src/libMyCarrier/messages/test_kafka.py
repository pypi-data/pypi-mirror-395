"""
Test suite for Kafka messaging module.

This module mirrors the test coverage from the Go implementation,
ensuring comprehensive validation of all functionality.
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from libMyCarrier.messages.kafka import (
    KafkaConfig,
    load_config,
    _validate_config,
    initialize_kafka_reader,
    initialize_kafka_writer,
)


class TestLoadConfig:
    """Test suite for load_config function."""

    def test_load_config(self, monkeypatch):
        """Test successful configuration loading with all environment variables."""
        monkeypatch.setenv("KAFKA_ADDRESS", "localhost:9092")
        monkeypatch.setenv("KAFKA_TOPIC", "test-topic")
        monkeypatch.setenv("KAFKA_USERNAME", "test-user")
        monkeypatch.setenv("KAFKA_PASSWORD", "test-password")
        monkeypatch.setenv("KAFKA_GROUPID", "test-group")
        monkeypatch.setenv("KAFKA_PARTITION", "1")
        monkeypatch.setenv("KAFKA_INSECURE_SKIP_VERIFY", "true")

        config = load_config()

        assert config is not None
        assert config.address == "localhost:9092"
        assert config.topic == "test-topic"
        assert config.username == "test-user"
        assert config.password == "test-password"
        assert config.groupid == "test-group"
        assert config.partition == "1"
        assert config.insecure_skip_verify == "true"

    def test_load_config_missing_required_fields(self, monkeypatch):
        """Test configuration loading fails when required fields are missing."""
        monkeypatch.setenv("KAFKA_ADDRESS", "")
        monkeypatch.setenv("KAFKA_TOPIC", "")
        monkeypatch.setenv("KAFKA_USERNAME", "")
        monkeypatch.setenv("KAFKA_PASSWORD", "")
        monkeypatch.setenv("KAFKA_INSECURE_SKIP_VERIFY", "")

        with pytest.raises(ValueError) as exc_info:
            load_config()

        assert "kafka address is required" in str(exc_info.value)


class TestInitializeKafkaReader:
    """Test suite for initialize_kafka_reader function."""

    def test_initialize_kafka_reader_invalid_partition(self):
        """Test reader initialization fails with invalid partition."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="",  # No GroupID to trigger partition validation
            partition="invalid",
        )

        with pytest.raises(ValueError) as exc_info:
            initialize_kafka_reader(config)

        assert "kafka partition must be a valid numeric value" in str(exc_info.value)


class TestInitializeKafkaWriter:
    """Test suite for initialize_kafka_writer function."""

    @patch('kafka.KafkaProducer')
    def test_initialize_kafka_writer(self, mock_producer):
        """Test successful writer initialization."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="1",
        )

        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance

        writer = initialize_kafka_writer(config)

        assert writer is not None
        mock_producer.assert_called_once()

        # Verify producer was called with correct configuration
        call_kwargs = mock_producer.call_args.kwargs
        assert call_kwargs['bootstrap_servers'] == "localhost:9092"
        assert call_kwargs['security_protocol'] == 'SASL_SSL'
        assert call_kwargs['sasl_mechanism'] == 'SCRAM-SHA-512'
        assert call_kwargs['sasl_plain_username'] == "test-user"
        assert call_kwargs['sasl_plain_password'] == "test-password"


class TestValidateConfig:
    """Test suite for _validate_config function."""

    def test_validate_config_missing_address(self):
        """Test validation fails when address is missing."""
        config = KafkaConfig(
            address="",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="1",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert str(exc_info.value) == "kafka address is required"

    def test_validate_config_missing_topic(self):
        """Test validation fails when topic is missing."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="1",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert str(exc_info.value) == "kafka topic is required"

    def test_validate_config_missing_username(self):
        """Test validation fails when username is missing but password is provided."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="",
            password="test-password",
            groupid="test-group",
            partition="1",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert str(exc_info.value) == "kafka username and password must both be provided or both be empty"

    def test_validate_config_missing_password(self):
        """Test validation fails when password is missing but username is provided."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="",
            groupid="test-group",
            partition="1",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert str(exc_info.value) == "kafka username and password must both be provided or both be empty"

    def test_validate_config_invalid_partition(self):
        """Test validation fails when partition is not numeric."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="invalid",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert "kafka partition must be a valid numeric value" in str(exc_info.value)

    def test_validate_config_invalid_insecure_skip_verify(self):
        """Test validation fails when insecure_skip_verify is not 'true' or 'false'."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="1",
            insecure_skip_verify="invalid",
        )

        with pytest.raises(ValueError) as exc_info:
            _validate_config(config)

        assert str(exc_info.value) == "kafka insecure_skip_verify must be true or false"

    def test_validate_config_default_insecure_skip_verify(self):
        """Test validation sets default insecure_skip_verify to 'false'."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="1",
            insecure_skip_verify="",
        )

        _validate_config(config)

        assert config.insecure_skip_verify == "false"

    def test_validate_config_default_groupid(self):
        """Test validation sets default groupid to 'default-group'."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="",
            partition="1",
        )

        _validate_config(config)

        assert config.groupid == "default-group"

    def test_validate_config_default_partition(self):
        """Test validation sets default partition to '0'."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="test-user",
            password="test-password",
            groupid="test-group",
            partition="",
        )

        _validate_config(config)

        assert config.partition == "0"

    def test_validate_config_empty_credentials_allowed(self):
        """Test validation allows empty username and password for local development."""
        config = KafkaConfig(
            address="localhost:9092",
            topic="test-topic",
            username="",
            password="",
            groupid="test-group",
            partition="1",
        )

        # Should not raise an error
        _validate_config(config)

        assert config.username == ""
        assert config.password == ""
