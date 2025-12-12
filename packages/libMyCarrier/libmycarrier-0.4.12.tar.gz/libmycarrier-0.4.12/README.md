# libMyCarrier

A comprehensive Python library for MyCarrier applications providing standardized interfaces for common operations including:
- Database connections (SQL Server, Snowflake)
- Secret management with HashiCorp Vault
- GitHub API integration
- Azure Blob Storage operations
- CI/CD status updates
- Kafka messaging (producers and consumers)
- Message publishing utilities

## Installation

```bash
# From PyPI (recommended)
pip install libMyCarrier

# From source
git clone https://github.com/mycarrier/libMyCarrier.git
cd libMyCarrier
pip install -e .
```

## Module Components

### Database Operations (`db`)

Provides a standardized interface for database connections and operations.

```python
from libMyCarrier.db.db import dbConnection

# SQL Server with token authentication
db_conn = dbConnection.from_sql(
    server="your-server.database.windows.net", 
    port=1433, 
    db_name="your-database",
    auth_method="token",
    token="your-access-token"
)

# SQL Server with username/password
db_conn = dbConnection.from_sql(
    server="your-server.database.windows.net", 
    port=1433, 
    db_name="your-database",
    auth_method="basic",
    username="your-username",
    password="your-password"
)

# Snowflake connection
db_conn = dbConnection.from_snowflake(
    user="your-user",
    password="your-password",
    role="your-role",
    account="your-account",
    warehouse="your-warehouse",
    database="your-database",
    schema="your-schema"
)

# Execute queries
results = db_conn.query("SELECT * FROM your_table", outputResults="all")

# Using transactions
with db_conn.transaction():
    db_conn.query("INSERT INTO table VALUES (1)")
    db_conn.query("UPDATE table SET value = 2")

# Close the connection when done
db_conn.close()
```

### Secret Management (`secrets`)

Interact with HashiCorp Vault for secure secret management.

```python
from libMyCarrier.secrets.vault import Vault

# Authenticate with AppRole
vault = Vault(role_id="your-role-id", secret_id="your-secret-id")

# Authenticate with token
vault = Vault(token="your-token")

# Get a secret from KV store
secret = vault.kv_secret("path/to/secret")
secret_value = secret["data"]["data"]

# Store a secret in KV store
vault.create_kv_secret("path/to/secret", secret={"key": "value"})

# Get database credentials
db_creds = vault.db_basic("database", "your-database-role")
username = db_creds["username"]
password = db_creds["password"]

# Get Azure credentials
azure_creds = vault.azure("azure", "your-azure-role")
```

### GitHub Integration (`git`)

Authenticate and interact with GitHub APIs.

```python
from libMyCarrier.git.github import githubAuth

# Load your private key from a secure location
with open("path/to/private-key.pem", "r") as file:
    private_key_pem = file.read()

# Authenticate with GitHub App
auth = githubAuth(
    private_key_pem=private_key_pem,
    app_id="your-app-id",
    installation_id="your-installation-id"
)

# The auth.token can be used with PyGithub
from github import Github
g = Github(login_or_token=auth.token)
org = g.get_organization("YOUR_ORG")
repo = org.get_repo("YOUR_REPO")
```

### Azure Blob Storage (`storage`)

Access and manage files in Azure Blob Storage.

```python
from libMyCarrier.storage.blob import Blob

# Initialize with your storage account URL
blob_client = Blob("https://youraccount.blob.core.windows.net")

# Download a blob
blob_content = blob_client.download_blob("container-name", "blob-name")
content_str = blob_content.readall()

# Delete a blob
blob_client.delete_blob("container-name", "blob-name")
```

### Utilities

#### CI Status Updates

Update ClickHouse tables with CI/CD build and deployment status.

```python
from libMyCarrier.utilities.cistatusupdater import ci_build_info, ci_deploy_info, clickhouse_insert

# Record a build event
build_data = ci_build_info(
    tag="your/service",
    version="1.0.0",
    branch="main",
    repo="https://github.com/org/repo",
    job_status="OK"
)
clickhouse_insert("ch-host", "ch-user", "ch-password", "ci.buildinfo", build_data)

# Record a deployment event
deploy_data = ci_deploy_info(
    environment="prod",
    repository="https://github.com/org/repo",
    branch="main",
    sha="abc123",
    job_status="OK",
    render_status="OK",
    deploy_status="OK",
    gitops_commit="Updated deployment config"
)
clickhouse_insert("ch-host", "ch-user", "ch-password", "ci.deployinfo", deploy_data)
```

#### Kafka Messaging (`messages`)

Kafka messaging with SASL/SCRAM-SHA-512 authentication for producers and consumers.

```python
from libMyCarrier.messages import (
    KafkaConfig,
    load_config,
    initialize_kafka_reader,
    initialize_kafka_writer
)

# Load configuration from environment variables
config = load_config()

# Or create configuration manually
config = KafkaConfig(
    address="kafka:9092",
    topic="your-topic",
    username="your-username",  # Optional for local dev (both username and password must be empty)
    password="your-password",  # Optional for local dev (both username and password must be empty)
    groupid="your-consumer-group",  # Default: "default-group"
    partition="0",  # Default: "0"
    insecure_skip_verify="false"  # Default: "false"
)

# Initialize a Kafka consumer
consumer = initialize_kafka_reader(config)
for message in consumer:
    print(f"Received: {message.value}")
consumer.close()

# Initialize a Kafka producer
producer = initialize_kafka_writer(config)
producer.send(config.topic, b"Hello, Kafka!")
producer.flush()
producer.close()
```

**Environment Variables:**
- `KAFKA_ADDRESS`: Kafka broker address (required)
- `KAFKA_TOPIC`: Kafka topic name (required)
- `KAFKA_USERNAME`: SASL username (optional, for local development both username and password can be empty)
- `KAFKA_PASSWORD`: SASL password (optional, for local development both username and password can be empty)
- `KAFKA_GROUPID`: Consumer group ID (optional, default: "default-group")
- `KAFKA_PARTITION`: Partition number (optional, default: "0")
- `KAFKA_INSECURE_SKIP_VERIFY`: Skip TLS verification (optional, default: "false")

#### CloudEvents Message Publishing (Legacy)

Send CloudEvents-formatted messages to Kafka topics using the legacy utility.

```python
from libMyCarrier.utilities.message import KafkaMessageProducer

# Configure broker information
producer = KafkaMessageProducer(
    broker="kafka:9092",
    sasl_un="username",
    sasl_pw="password"
)

# Send a message
producer.send_message(
    topic="your-topic",
    event_type="com.mycarrier.event.type",
    source="your-service",
    data={"key": "value", "status": "complete"}
)
```

#### Tag Management

Pull service tags from ClickHouse.

```python
from libMyCarrier.utilities.tags import pull_tags

# Get the latest service tags for a repository and branch
tags = pull_tags(
    CH_HOST="clickhouse-host",
    CH_USER="clickhouse-user",
    CH_PASS_SECRET="clickhouse-password",
    BRANCH="main",
    REPO="github.com/org/repo"
)

# Tags will be a list of dictionaries with Service, Component, and ImageTag
```

### Error Handling

The library provides standardized error types:

```python
from libMyCarrier.error import (
    MyCarrierError,  # Base error class
    VaultError,      # Vault-related errors
    DatabaseError,   # Database-related errors
    GitHubError,     # GitHub API errors
    StorageError,    # Blob storage errors
    KafkaError,      # Kafka-related errors
    ConfigError      # Configuration errors
)

# Example usage
try:
    # Operations that may fail
    pass
except DatabaseError as e:
    # Handle database-specific errors
    pass
except MyCarrierError as e:
    # Handle any other library error
    pass
```

## Contributing

1. Clone the repository:
   ```
   git clone https://github.com/mycarrier/libMyCarrier.git
   ```

2. Set up your development environment:
   ```
   cd libMyCarrier
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```
   pytest
   ```

4. Submit a PR with your changes

## License

Copyright (c) MyCarrier. All rights reserved.