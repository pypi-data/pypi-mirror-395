"""
Kafka messaging module for libMyCarrier.

This module provides utilities to interact with Kafka, including configuration
management, message production, and message consumption. It supports SASL/SCRAM
authentication and follows enterprise-grade best practices.
"""

import os
import ssl
from dataclasses import dataclass


@dataclass
class KafkaConfig:
    """
    Configuration for Kafka connection and authentication.

    Attributes:
        address: Kafka broker address
        topic: Kafka topic name
        username: SASL username for authentication
        password: SASL password for authentication
        groupid: Consumer group ID (default: 'default-group')
        partition: Partition number as string (default: '0')
        insecure_skip_verify: Skip TLS verification as string 'true'/'false' (default: 'false')
    """
    address: str
    topic: str
    username: str
    password: str
    groupid: str = "default-group"
    partition: str = "0"
    insecure_skip_verify: str = "false"


def load_config() -> KafkaConfig:
    """
    Load Kafka configuration from environment variables.

    Environment variables:
        KAFKA_ADDRESS: Kafka broker address (required)
        KAFKA_TOPIC: Kafka topic name (required)
        KAFKA_USERNAME: SASL username (required)
        KAFKA_PASSWORD: SASL password (required)
        KAFKA_GROUPID: Consumer group ID (optional, default: 'default-group')
        KAFKA_PARTITION: Partition number (optional, default: '0')
        KAFKA_INSECURE_SKIP_VERIFY: Skip TLS verification (optional, default: 'false')

    Returns:
        KafkaConfig: Validated Kafka configuration

    Raises:
        ValueError: If required configuration is missing or invalid
    """
    config = KafkaConfig(
        address=os.getenv("KAFKA_ADDRESS", ""),
        topic=os.getenv("KAFKA_TOPIC", ""),
        username=os.getenv("KAFKA_USERNAME", ""),
        password=os.getenv("KAFKA_PASSWORD", ""),
        groupid=os.getenv("KAFKA_GROUPID", "default-group"),
        partition=os.getenv("KAFKA_PARTITION", "0"),
        insecure_skip_verify=os.getenv("KAFKA_INSECURE_SKIP_VERIFY", "false")
    )

    _validate_config(config)
    return config


def _validate_config(config: KafkaConfig) -> None:
    """
    Validate Kafka configuration.

    Args:
        config: KafkaConfig instance to validate

    Raises:
        ValueError: If configuration is invalid
    """
    if not config.address:
        raise ValueError("kafka address is required")

    if not config.topic:
        raise ValueError("kafka topic is required")

    # Username and password are optional (for local dev without auth)
    # If one is provided, both must be provided
    if bool(config.username) != bool(config.password):
        raise ValueError("kafka username and password must both be provided or both be empty")

    if not config.groupid:
        config.groupid = "default-group"

    if not config.partition:
        config.partition = "0"
    else:
        _validate_partition(config.partition)

    if not config.insecure_skip_verify:
        config.insecure_skip_verify = "false"
    elif config.insecure_skip_verify not in ("true", "false"):
        raise ValueError("kafka insecure_skip_verify must be true or false")


def _validate_partition(partition: str) -> int:
    """
    Validate and convert partition string to integer.

    Args:
        partition: Partition number as string

    Returns:
        int: Validated partition number

    Raises:
        ValueError: If partition is not a valid numeric value
    """
    try:
        return int(partition)
    except ValueError:
        raise ValueError("kafka partition must be a valid numeric value")


def initialize_kafka_reader(kafka_config: KafkaConfig):
    """
    Initialize a Kafka consumer with the provided configuration.

    This function creates a Kafka consumer configured with SASL/SCRAM-SHA-512
    authentication and TLS security.

    Args:
        kafka_config: KafkaConfig instance with connection details

    Returns:
        KafkaConsumer: Configured Kafka consumer instance

    Raises:
        ValueError: If partition value is invalid when GroupID is not set
        Exception: If consumer initialization fails
    """
    from kafka import KafkaConsumer, TopicPartition

    # Build consumer configuration
    consumer_config = {
        'bootstrap_servers': kafka_config.address,
        'group_id': kafka_config.groupid or None,
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': True,
        'max_poll_records': 500,
    }

    # Add authentication if credentials are provided
    if kafka_config.username and kafka_config.password:
        # Create SSL context
        ssl_context = ssl.create_default_context()
        if kafka_config.insecure_skip_verify == "true":
            # Only disable verification for development environments
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        consumer_config.update({
            'security_protocol': 'SASL_SSL',
            'sasl_mechanism': 'SCRAM-SHA-512',
            'sasl_plain_username': kafka_config.username,
            'sasl_plain_password': kafka_config.password,
            'ssl_context': ssl_context,
        })
    else:
        # No authentication - use PLAINTEXT (for local dev)
        consumer_config['security_protocol'] = 'PLAINTEXT'

    # Handle partition assignment when no group_id is set
    if not kafka_config.groupid:
        partition = _validate_partition(kafka_config.partition)
        consumer = KafkaConsumer(**consumer_config)
        consumer.assign([TopicPartition(kafka_config.topic, partition)])
        return consumer
    else:
        # Subscribe to topic with consumer group
        consumer = KafkaConsumer(kafka_config.topic, **consumer_config)
        return consumer


def initialize_kafka_writer(kafka_config: KafkaConfig):
    """
    Initialize a Kafka producer with the provided configuration.

    This function creates a Kafka producer configured with SASL/SCRAM-SHA-512
    authentication and TLS security. The producer is configured for async writes
    with automatic retries.

    Args:
        kafka_config: KafkaConfig instance with connection details

    Returns:
        KafkaProducer: Configured Kafka producer instance

    Raises:
        Exception: If producer initialization fails
    """
    from kafka import KafkaProducer

    # Build producer configuration
    producer_config = {
        'bootstrap_servers': kafka_config.address,
        'acks': 'all',  # Wait for all in-sync replicas
        'retries': 5,   # Retry up to 5 times
        'max_in_flight_requests_per_connection': 1,  # Ensure ordering
    }

    # Add authentication if credentials are provided
    if kafka_config.username and kafka_config.password:
        # Create SSL context
        ssl_context = ssl.create_default_context()
        if kafka_config.insecure_skip_verify == "true":
            # Only disable verification for development environments
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        producer_config.update({
            'security_protocol': 'SASL_SSL',
            'sasl_mechanism': 'SCRAM-SHA-512',
            'sasl_plain_username': kafka_config.username,
            'sasl_plain_password': kafka_config.password,
            'ssl_context': ssl_context,
        })
    else:
        # No authentication - use PLAINTEXT (for local dev)
        producer_config['security_protocol'] = 'PLAINTEXT'

    # Create producer with configuration
    producer = KafkaProducer(**producer_config)

    return producer
