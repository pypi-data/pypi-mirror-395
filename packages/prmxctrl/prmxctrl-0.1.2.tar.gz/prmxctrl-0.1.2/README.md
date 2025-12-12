# prmxctrl - Proxmox VE Python SDK

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Type Checking](https://img.shields.io/badge/mypy-strict-green.svg)](https://mypy-lang.org/)
[![Linting](https://img.shields.io/badge/ruff-passing-green.svg)](https://github.com/astral-sh/ruff)

A fully type-safe, auto-generated Python SDK for the Proxmox Virtual Environment (VE) API. Built with Pydantic v2, httpx, and modern Python async patterns.

## Features

- **100% Type Safe**: Full type hints with mypy --strict compliance
- **Auto-Generated**: Complete SDK generated from Proxmox API schema
- **Async/Await**: Modern async HTTP client with connection pooling
- **Hierarchical API**: Navigate the API like `client.nodes("pve1").qemu(100).config.get()`
- **Authentication**: Support for both password and API token authentication
- **Validation**: Pydantic models ensure request/response data integrity
- **Comprehensive**: 284 endpoints covering the full Proxmox VE API

## Quick Start

### Installation

```bash
pip install prmxctrl
```

### Environment Setup

For security, it's recommended to use environment variables instead of hardcoding credentials. Copy the example file and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

The `.env` file supports both authentication methods:

```bash
# For password authentication
PROXMOX_USERNAME=your_username
PROXMOX_PASSWORD=your_password
PROXMOX_REALM=pam  # or pve for Proxmox realm

# For API token authentication (recommended)
PROXMOX_TOKEN_ID=your_token_name
PROXMOX_TOKEN_SECRET=your_token_uuid

# Required for both methods
PROXMOX_HOST=https://your-proxmox-server:8006
PROXMOX_NODE=your_node_name
PROXMOX_VMID=100
```

Then load the environment variables in your code:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use in client initialization
client = ProxmoxClient(
    host=os.getenv("PROXMOX_HOST"),
    user=f"{os.getenv('PROXMOX_USERNAME')}@{os.getenv('PROXMOX_REALM')}",
    password=os.getenv("PROXMOX_PASSWORD"),
    # OR for token auth:
    # token_name=os.getenv("PROXMOX_TOKEN_ID"),
    # token_value=os.getenv("PROXMOX_TOKEN_SECRET"),
)
```

### Basic Usage

```python
import asyncio
from prmxctrl import ProxmoxClient

async def main():
    # Method 1: Async context manager (recommended for production)
    async with ProxmoxClient(
        host="your-proxmox-host",
        user="your-username@pve",
        password="your-password"
    ) as client:
        # Get cluster status
        status = await client.cluster.status.get()
        print(f"Cluster status: {status}")

        # List all nodes
        nodes = await client.nodes.get()
        for node in nodes:
            print(f"Node: {node.node}")

        # Get VM configuration
        vm_config = await client.nodes("pve1").qemu(100).config.get()
        print(f"VM config: {vm_config}")

    # Method 2: Manual initialization (for better type hints in development)
    client = ProxmoxClient(
        host="your-proxmox-host",
        user="your-username@pve",
        password="your-password"
    )
    try:
        await client._setup_client()  # Manual setup
        # Get cluster status
        status = await client.cluster.status.get()
        print(f"Cluster status: {status}")
    finally:
        await client._cleanup_client()  # Manual cleanup

asyncio.run(main())
```

### Authentication

The SDK supports two authentication methods:

#### Password Authentication (Ticket-based)

```python
async with ProxmoxClient(
    host="https://your-proxmox-host:8006",
    user="your-username@pve",  # username@realm format
    password="your-password",
    verify_ssl=False  # Set to True for production with valid SSL certs
) as client:
    # Get cluster status
    status = await client.cluster.status.get()
    print(f"Cluster status: {status}")
```

#### API Token Authentication (Recommended)

```python
async with ProxmoxClient(
    host="https://your-proxmox-host:8006",
    user="your-username@pve",  # username@realm format (required for token auth)
    token_name="your-token-name",
    token_value="your-token-secret",
    verify_ssl=False  # Set to True for production with valid SSL certs
) as client:
    # Get cluster status
    status = await client.cluster.status.get()
    print(f"Cluster status: {status}")
```

**Authentication Notes:**
- **API Token Authentication is recommended** for production use (more secure, no password storage)
- **Password Authentication** uses Proxmox's ticket/CSRF token system
- Both methods require the `user` parameter in `username@realm` format
- Set `verify_ssl=True` in production environments with valid SSL certificates
- The SDK automatically handles CSRF tokens and session management

### Client Initialization Methods

The SDK supports two initialization patterns with different trade-offs:

#### Async Context Manager (Recommended)
```python
async with ProxmoxClient(...) as client:
    # Automatic resource cleanup
    result = await client.version.get()
```
- ✅ **Automatic resource management** - HTTP connections are properly cleaned up
- ✅ **Exception safety** - Resources are cleaned up even if errors occur
- ✅ **Production ready** - Follows Python best practices
- ❌ **Type hints may show as `Any`** - Due to context manager return type limitations

#### Manual Initialization (Development)
```python
client = ProxmoxClient(...)
try:
    await client._setup_client()
    result = await client.version.get()  # Full type hints available
finally:
    await client._cleanup_client()
```
- ✅ **Full type hints** - IDE shows complete endpoint types and methods
- ✅ **Better development experience** - Autocomplete and type checking work perfectly
- ❌ **Manual resource management** - Must remember to call setup/cleanup
- ❌ **Error prone** - Easy to forget cleanup, potentially leaking connections

**Recommendation**: Use the async context manager for production code. Use manual initialization during development when you need full type hint support for exploring the API.

## API Structure

The SDK mirrors the Proxmox API structure hierarchically:

- `client.cluster.*` - Cluster management
- `client.nodes(node).*` - Node-specific operations
- `client.nodes(node).qemu(vmid).*` - QEMU VM operations
- `client.nodes(node).lxc(vmid).*` - LXC container operations
- `client.access.*` - User and permission management
- `client.pools.*` - Pool management
- `client.storage.*` - Storage operations

## Advanced Usage

### Creating Resources

```python
# Create a new QEMU VM
vm_config = {
    "name": "test-vm",
    "memory": 2048,
    "cores": 2,
    "net0": "virtio,bridge=vmbr0",
    "ide2": "local:iso/ubuntu-22.04.iso,media=cdrom"
}

result = await client.nodes("pve1").qemu.create(
    node="pve1",
    vmid=100,
    **vm_config
)
```

### Error Handling

```python
from prmxctrl import ProxmoxAPIError, ProxmoxAuthError

try:
    result = await client.nodes("pve1").qemu(100).config.get()
except ProxmoxAuthError:
    print("Authentication failed")
except ProxmoxAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

### Working with Models

All request/response data is validated using Pydantic models:

```python
from prmxctrl.models.nodes import NodeListResponse

# Type-safe response handling
nodes: list[NodeListResponse] = await client.nodes.get()
for node in nodes:
    # IDE will show available fields with type hints
    print(f"Node {node.node}: {node.status} ({node.cpu:.1%} CPU)")
```

## Development

### Prerequisites

- Python 3.10+
- Access to Proxmox VE API documentation

### Setup

```bash
git clone https://github.com/your-repo/prmxctrl.git
cd prmxctrl
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

### Code Generation

The SDK is auto-generated from the Proxmox API schema:

```bash
# Generate the complete SDK
python tools/generate.py

# Validate the generated code
python tools/validate.py
```

### Testing

```bash
# Run the full test suite
pytest

# Run with coverage
pytest --cov=prmxctrl --cov-report=html

# Type checking
mypy --strict

# Linting
ruff check .
```

## Architecture

This SDK is built with a code generation approach:

1. **Schema Processing**: Parse Proxmox API schema from `apidata.js`
2. **Model Generation**: Create Pydantic v2 models for all request/response types
3. **Endpoint Generation**: Generate hierarchical endpoint classes
4. **Client Integration**: Tie everything together in the main `ProxmoxClient`

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design decisions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Disclaimer

This SDK is not officially affiliated with Proxmox Server Solutions GmbH. Use at your own risk.