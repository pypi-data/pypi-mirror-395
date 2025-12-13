# Coinbase International Exchange (INTX) Python SDK

## Overview

The *INTX Python SDK* is a sample library that demonstrates the usage of the [Coinbase International Exchange (INTX)](https://international.coinbase.com/) API via its [REST APIs](https://docs.cdp.coinbase.com/intx/reference). This SDK provides a structured way to integrate Coinbase INTX functionalities into your Python applications.
## License

The *INTX Python SDK* sample library is free and open source and released under the [Apache License, Version 2.0](LICENSE).

The application and code are only available for demonstration purposes.

## Installation

```bash
pip install intx-sdk-py
```

Or install from source:

```bash
git clone https://github.com/coinbase-samples/intx-sdk-py.git
cd intx-sdk-py
pip install -e .
```

## Authentication

To use the INTX Python SDK, you will need to create API credentials in the [INTX web console](https://international.coinbase.com/) under Settings -> API.

Credentials can be stored as environment variables or passed directly. The SDK supports two initialization patterns:

### Using .env.example (Recommended)

Copy the example file to `.env` and then fill in your credentials:

```bash
cp .env.example .env
# then edit .env and set your values
```

Initialize the client:

```python
from intx_sdk import IntxServicesClient

client = IntxServicesClient.from_env()
```

### Using Credentials Object

```python
from intx_sdk import IntxServicesClient
from intx_sdk.credentials import Credentials

credentials = Credentials(
    access_key="your-access-key",
    passphrase="your-passphrase",
    signing_key="your-signing-key"
)

client = IntxServicesClient(credentials)
```

## Environment Configuration

By default, the SDK uses the production environment. To use a different environment, set the `INTX_BASE_URL` environment variable:

```bash
# Use sandbox environment
export INTX_BASE_URL=https://api-n5e1.coinbase.com/api/v1

# Or use production (default)
export INTX_BASE_URL=https://api.international.coinbase.com/api/v1
```

Alternatively, you can use the exported constants:

```python
from intx_sdk import IntxServicesClient, SANDBOX_BASE_URL, PRODUCTION_BASE_URL

# Use sandbox
client = IntxServicesClient.from_env(base_url=SANDBOX_BASE_URL)

# Use production (or omit base_url parameter for default)
client = IntxServicesClient.from_env(base_url=PRODUCTION_BASE_URL)

# Use custom URL
client = IntxServicesClient.from_env(base_url="https://custom.api.com/v1")
```

## Usage

```python
from intx_sdk import IntxServicesClient
from intx_sdk.services.portfolios import ListPortfoliosRequest

client = IntxServicesClient.from_env()

# List portfolios
request = ListPortfoliosRequest()
response = client.portfolios.list_portfolios(request)
print(response)
```

For more examples, see the [examples](examples/) directory.