"""
Common error types for libMyCarrier
"""

class MyCarrierError(Exception):
    """Base exception for all libMyCarrier errors"""
    pass

class VaultError(MyCarrierError):
    """Exception raised for HashiCorp Vault errors"""
    pass

class DatabaseError(MyCarrierError):
    """Exception raised for database-related errors"""
    pass

class GitHubError(MyCarrierError):
    """Exception raised for GitHub API errors"""
    pass

class StorageError(MyCarrierError):
    """Exception raised for storage-related errors"""
    pass

class KafkaError(MyCarrierError):
    """Exception raised for Kafka-related errors"""
    pass

class ConfigError(MyCarrierError):
    """Exception raised for configuration errors"""
    pass
