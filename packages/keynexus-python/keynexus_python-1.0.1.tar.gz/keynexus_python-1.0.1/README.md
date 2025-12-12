# KeyNexus Python SDK

Official Python client for KeyNexus License Management System.

## Installation

### From PyPI (Recommended)

```bash
pip install keynexus-python
```

### From Source

```bash
# Clone repository
git clone https://github.com/keynexus/keynexus-python
cd keynexus-python

# Install
pip install -e .
```

## Quick Start

```python
from keynexus import KeyNexusClient

# Initialize client
client = KeyNexusClient(
    app_id="app_xxxxxxxxxxxx",
    secret_key="sk_xxxxxxxxxxxxxxxxxxxx"
)

# Validate license
try:
    result = client.validate_license("XXXXX-XXXXX-XXXXX-XXXXX")
    print(f"✅ License valid!")
    print(f"Type: {result['license']['type']}")
    print(f"Expires: {result['license']['expiresAt']}")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Features

- ✅ License validation with automatic HWID generation
- ✅ Username/password authentication
- ✅ Session management
- ✅ Automatic error handling
- ✅ Type hints for better IDE support

## Documentation

Full documentation available at: https://keynexus.es/docs

## Examples

### Validate License

```python
client = KeyNexusClient(app_id="...", secret_key="...")

result = client.validate_license("XXXXX-XXXXX-XXXXX-XXXXX")
if result['success']:
    print("Access granted!")
```

### Login with Password

```python
result = client.login_with_password("username", "password")
print(f"Welcome {result['user']['username']}!")
```

### Get User Info

```python
user = client.get_user_info()
print(f"Subscription expires: {user['user']['subscriptionExpiry']}")
```

## License

MIT License - see LICENSE file for details
