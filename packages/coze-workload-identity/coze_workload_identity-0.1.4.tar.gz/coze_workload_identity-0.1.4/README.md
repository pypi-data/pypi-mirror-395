# Coze Workload Identity SDK

A Python SDK for Coze workload identity authentication using OAuth2.0 token exchange.

## Features

- 🔐 Secure OAuth2.0 token exchange flow
- 🚀 Thread-safe token caching with automatic expiration
- 📝 Comprehensive error handling
- 🧪 Fully tested with high coverage
- 📦 Easy to install and use
- 🏊‍♂️ Lane support (泳道) for different environments (BOE, PPE, custom)
- 🔑 Integration credential management
- 📋 Project environment variables retrieval

## Installation

```bash
pip install coze-workload-identity
```

## Quick Start

1. Set up environment variables:
```bash
export COZE_WORKLOAD_IDENTITY_CLIENT_ID="your_client_id"
export COZE_WORKLOAD_IDENTITY_CLIENT_SECRET="your_client_secret"
export COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT="https://auth.example.com/token"
export COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT="https://auth.example.com/access-token"
```

2. Use the SDK (Recommended approach with env_keys):
```python
from coze_workload_identity import Client
from coze_workload_identity.env_keys import *

# Create client
client = Client()

# Get access token
token = client.get_access_token()
print(f"Access token: {token}")

# Get integration credential (if configured)
# credential = client.get_integration_credential("my_integration")

# Get project environment variables (if configured)
# project_env_vars = client.get_project_env_vars()
# for env_var in project_env_vars:
#     print(f"{env_var.key}: {env_var.value}")

# Use as context manager
with Client() as client:
    token = client.get_access_token()
    # Use the token for API calls
```

**Alternative: Set environment variables in Python:**
```python
import os
from coze_workload_identity.env_keys import *

# Set environment variables using constants
os.environ[COZE_WORKLOAD_IDENTITY_CLIENT_ID] = "your_client_id"
os.environ[COZE_WORKLOAD_IDENTITY_CLIENT_SECRET] = "your_client_secret"
os.environ[COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT] = "https://auth.example.com/token"
os.environ[COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT] = "https://auth.example.com/access-token"

# Optional: Configure lane and integration endpoints
os.environ[COZE_SERVER_ENV] = "boe_test_lane"
os.environ[COZE_OUTBOUND_AUTH_ENDPOINT] = "https://auth.example.com/integration-credential"

# Now use the client
from coze_workload_identity import Client

with Client() as client:
    token = client.get_access_token()
    credential = client.get_integration_credential("my_integration")

    # Get project environment variables (if configured)
    # project_env_vars = client.get_project_env_vars()
    # for env_var in project_env_vars:
    #     print(f"{env_var.key}: {env_var.value}")
```

## Configuration

The SDK requires the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `COZE_WORKLOAD_IDENTITY_CLIENT_ID` | Client ID for authentication | ✅ |
| `COZE_WORKLOAD_IDENTITY_CLIENT_SECRET` | Client secret for authentication | ✅ |
| `COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT` | Token endpoint for ID token | ✅ |
| `COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT` | Access token endpoint for token exchange | ✅ |
| `COZE_OUTBOUND_AUTH_ENDPOINT` | Integration credential endpoint (required for get_integration_credential and get_project_env_vars) | ❌ |
| `COZE_SERVER_ENV` | Lane environment (optional, default: NONE) | ❌ |

### Using Environment Variable Keys (Recommended)

Instead of hardcoding environment variable names, use the provided environment variable keys:

```python
from coze_workload_identity.env_keys import *

# Set environment variables using constants
os.environ[COZE_WORKLOAD_IDENTITY_CLIENT_ID] = "your_client_id"
os.environ[COZE_WORKLOAD_IDENTITY_CLIENT_SECRET] = "your_client_secret"
os.environ[COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT] = "https://auth.example.com/token"
os.environ[COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT] = "https://auth.example.com/access-token"

# Optional: Set lane environment
os.environ[COZE_SERVER_ENV] = "boe_test_lane"

# Optional: Set integration credential endpoint
os.environ[COZE_OUTBOUND_AUTH_ENDPOINT] = "https://auth.example.com/integration-credential"
```

**Benefits of using env_keys:**
- ✅ Avoid typos in environment variable names
- ✅ IDE autocomplete and error checking
- ✅ Centralized management of all Coze platform variables
- ✅ Type safety and better code maintainability
- ✅ Easy to refactor and update variable names

### Lane Support (泳道支持)

The SDK supports lane environments through the `COZE_SERVER_ENV` environment variable:

- **NONE** (default): No lane headers are added
- **boe_***: Adds `x-tt-env: boe_<lane>` header
- **ppe_***: Adds `x-tt-env: ppe_<lane>` and `x-use-ppe: 1` headers
- **custom**: Adds `x-tt-env: <custom>` header

**Examples:**
```bash
# BOE lane
export COZE_SERVER_ENV="boe_test_lane"

# PPE lane
export COZE_SERVER_ENV="ppe_production_lane"

# Custom lane
export COZE_SERVER_ENV="my_custom_lane"
```

## API Reference

### Client

The main class for interacting with the workload identity service.

#### Constructor
```python
Client()
```

Creates a new client instance. Configuration is loaded from environment variables.

#### Methods

##### `get_access_token()`

Retrieves an access token using the OAuth2.0 token exchange flow.

**Returns:** `str` - The access token

**Raises:**
- `ConfigurationError` - If required configuration is missing
- `TokenRetrievalError` - If ID token retrieval fails
- `TokenExchangeError` - If token exchange fails

**Example:**
```python
try:
    token = client.get_access_token()
    # Use the token for API calls
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except TokenRetrievalError as e:
    print(f"Token retrieval error: {e}")
except TokenExchangeError as e:
    print(f"Token exchange error: {e}")
```

##### `close()`

Closes the client and cleans up resources.

**Example:**
```python
client = Client()
try:
    token = client.get_access_token()
finally:
    client.close()
```

##### `get_integration_credential(integration_name)`

Retrieves integration credentials for the specified integration name.

**Args:**
- `integration_name` (str): Name of the integration

**Returns:** `str` - The integration credential

**Raises:**
- `ConfigurationError` - If COZE_OUTBOUND_AUTH_ENDPOINT is not configured
- `TokenRetrievalError` - If access token retrieval fails
- `Exception` - If integration credential API returns non-200 status or invalid response

**Example:**
```python
try:
    credential = client.get_integration_credential("my_integration")
    # Use the credential for integration API calls
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Integration error: {e}")
```

**API Response Format:**
The integration credential endpoint should return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "credential": "integration_credential_string"
    }
}
```

**Error Handling:**
- 4xx errors: Client errors (e.g., invalid integration name)
- 5xx errors: Server errors
- Non-zero code: API business logic errors

##### `get_project_env_vars()`

Retrieves project environment variables.

**Returns:** `ProjectEnvVars` - Object containing project environment variables

**Raises:**
- `ConfigurationError` - If COZE_OUTBOUND_AUTH_ENDPOINT is not configured
- `TokenRetrievalError` - If access token retrieval fails
- `Exception` - If project environment variables API returns non-200 status or invalid response

**Example:**
```python
try:
    project_env_vars = client.get_project_env_vars()
    # Access environment variables
    for env_var in project_env_vars:
        print(f"{env_var.key}: {env_var.value}")

    # Or get specific variable
    db_url = project_env_vars.get("DATABASE_URL")
    if db_url:
        print(f"Database URL: {db_url}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Project env vars error: {e}")
```

**API Response Format:**
The project environment variables endpoint should return:
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "secrets": [
            {
                "key": "DATABASE_URL",
                "value": "postgresql://localhost:5432/mydb"
            },
            {
                "key": "API_KEY",
                "value": "secret_api_key_123"
            }
        ]
    }
}
```

**Error Handling:**
- 4xx errors: Client errors
- 5xx errors: Server errors
- Non-zero code: API business logic errors

### Exceptions

#### `WorkloadIdentityError`
Base exception for all workload identity SDK errors.

#### `ConfigurationError`
Raised when required configuration is missing or invalid.

#### `TokenRetrievalError`
Raised when ID token retrieval fails.

#### `TokenExchangeError`
Raised when token exchange fails.

### Data Models

#### `ProjectEnvVar`
Represents a single project environment variable.

**Attributes:**
- `key` (str): The environment variable key
- `value` (str): The environment variable value

#### `ProjectEnvVars`
Represents a collection of project environment variables.

**Attributes:**
- `vars` (List[ProjectEnvVar]): List of ProjectEnvVar objects

**Methods:**
- `get(key, default=None)`: Get environment variable value by key
- `__len__()`: Return the number of environment variables
- `__iter__()`: Iterate over the environment variables
- `__getitem__(key)`: Get environment variable value by key using bracket notation
- `__contains__(key)`: Check if environment variable exists

**Example:**
```python
from coze_workload_identity import Client, ProjectEnvVar, ProjectEnvVars

client = Client()
project_env_vars = client.get_project_env_vars()

# Iterate over all environment variables
for env_var in project_env_vars:
    print(f"{env_var.key}: {env_var.value}")

# Get specific variable
api_key = project_env_vars.get("API_KEY")
if api_key:
    print(f"API Key: {api_key}")

# Check if variable exists
if "DATABASE_URL" in project_env_vars:
    db_url = project_env_vars["DATABASE_URL"]
    print(f"Database URL: {db_url}")

# Get with default value
port = project_env_vars.get("PORT", "8080")
print(f"Port: {port}")
```

## Token Caching

The SDK automatically caches tokens to avoid unnecessary HTTP requests:

- **ID tokens** are cached based on their `expires_in` value
- **Access tokens** are cached based on their `expires_in` value
- A 1-minute buffer is applied to prevent using tokens that are about to expire
- The cache is thread-safe and supports concurrent access

## Thread Safety

The SDK is designed to be thread-safe:

- Token cache operations are protected by locks
- Multiple threads can safely call `get_access_token()` concurrently
- The HTTP session is shared across threads

## Error Handling

The SDK provides detailed error information:

```python
from coze_workload_identity import Client, ConfigurationError, TokenRetrievalError, TokenExchangeError

client = Client()
try:
    token = client.get_access_token()
except ConfigurationError as e:
    # Handle missing or invalid configuration
    print(f"Configuration error: {e}")
except TokenRetrievalError as e:
    # Handle ID token retrieval failures
    print(f"Token retrieval error: {e}")
except TokenExchangeError as e:
    # Handle token exchange failures
    print(f"Token exchange error: {e}")
except Exception as e:
    # Handle other unexpected errors
    print(f"Unexpected error: {e}")
finally:
    client.close()
```

## Logging

The SDK uses Python's logging module. To enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('workload_identity')
logger.setLevel(logging.DEBUG)
```

## Development

### Setting up for development

```bash
git clone <repository-url>
cd workload-identity-sdk
pip install -e .[dev]
```

### Running tests

```bash
pytest tests/ -v --cov=workload_identity
```

### Code formatting

```bash
black workload_identity/ tests/
```

### Type checking

```bash
mypy workload_identity/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check existing issues for solutions
- Review the documentation and examples