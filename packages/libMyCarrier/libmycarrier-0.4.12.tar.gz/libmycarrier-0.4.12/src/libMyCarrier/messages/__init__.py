"""
Messages module for libMyCarrier.

This module provides technology-agnostic messaging utilities,
currently supporting Kafka with SASL/SCRAM authentication.
"""

from .kafka import (
    KafkaConfig,
    load_config,
    initialize_kafka_reader,
    initialize_kafka_writer,
)

__all__ = [
    "KafkaConfig",
    "load_config",
    "initialize_kafka_reader",
    "initialize_kafka_writer",
]
