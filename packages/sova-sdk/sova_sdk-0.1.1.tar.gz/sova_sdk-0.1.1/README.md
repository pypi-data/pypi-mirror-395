# Sova SDK for Python

[![PyPI version](https://badge.fury.io/py/sova-sdk.svg)](https://badge.fury.io/py/sova-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/sova-sdk.svg)](https://pypi.org/project/sova-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for [Sova Network](https://github.com/serhiibeznisko/sova-sdk-python) - a MEV (Maximal Extractable Value) infrastructure built for the TON blockchain. This SDK provides a comprehensive interface for interacting with Sova's gRPC services, enabling searchers and validators to participate in the MEV ecosystem.

## Table of Contents

- [What is Sova Network?](#what-is-sova-network)
- [Installation](#installation)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Subscribe to Mempool by Address](#subscribe-to-mempool-by-address)
  - [Subscribe to Mempool by Workchain](#subscribe-to-mempool-by-workchain)
  - [Send a Bundle](#send-a-bundle)
  - [Subscribe to Bundle Results](#subscribe-to-bundle-results)
  - [Get Tip Addresses](#get-tip-addresses)
  - [Block Engine (Validator Integration)](#block-engine-validator-integration)
  - [Custom Client Configuration](#custom-client-configuration)
- [API Reference](#api-reference)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)

## What is Sova Network?

Sova Network provides MEV infrastructure on TON, allowing:
- **Searchers** to monitor the mempool and submit bundles of transactions
- **Validators** to receive and execute profitable bundles
- **Secure authentication** using Ed25519 cryptography
- **Real-time mempool streaming** with flexible filtering options

## Installation

Install the package from PyPI:

```bash
pip install sova-sdk
```

## Requirements

- Python >= 3.8
- Dependencies are automatically installed: `grpcio`, `grpcio-tools`, `protobuf`, `pynacl`

## Features

- **Authentication**: Ed25519-based authentication with Sova services
- **Mempool Subscriptions**: Subscribe to mempool updates by address, workchain, shard, or opcode
- **Bundle Management**: Send bundles and subscribe to bundle results
- **Block Engine**: Validator integration for streaming mempool and receiving bundles
- **TLS Support**: Secure connections with custom CA certificates for testnet and mainnet

## Quick Start

### Basic Usage

```python
from sova_sdk import SovaClient

# Create a testnet client
client = SovaClient.new_testnet_client()

# Or create a mainnet client
# client = SovaClient.new_mainnet_client()

# Authenticate with your private key (32 bytes)
private_key = bytes.fromhex("your_private_key_hex")
token = client.authenticate(private_key)

# Get a searcher client
searcher = client.searcher()
```

### Subscribe to Mempool by Address

```python
import asyncio
from sova_sdk import SovaClient

async def main():
    client = SovaClient.new_testnet_client()
    private_key = bytes.fromhex("your_private_key_hex")
    client.authenticate(private_key)

    searcher = client.searcher()

    def on_packet(packet):
        print(f"Received mempool packet: {packet}")

    # Subscribe to specific addresses
    addresses = ["EQD...", "EQA..."]  # TON addresses
    await searcher.subscribe_by_address(addresses, on_packet)

asyncio.run(main())
```

### Subscribe to Mempool by Workchain

```python
import asyncio
from sova_sdk import SovaClient

async def main():
    client = SovaClient.new_testnet_client()
    private_key = bytes.fromhex("your_private_key_hex")
    client.authenticate(private_key)

    searcher = client.searcher()

    def on_packet(packet):
        print(f"Received packet from workchain: {packet}")

    # Subscribe to workchain 0 (masterchain is -1)
    await searcher.subscribe_by_workchain(0, on_packet)

asyncio.run(main())
```

### Send a Bundle

```python
from sova_sdk import SovaClient, dto_pb2
from google.protobuf.timestamp_pb2 import Timestamp
import time

client = SovaClient.new_testnet_client()
private_key = bytes.fromhex("your_private_key_hex")
client.authenticate(private_key)

searcher = client.searcher()

# Create a bundle
expiration = Timestamp()
expiration.FromDatetime(datetime.now() + timedelta(minutes=5))

bundle = dto_pb2.Bundle(
    message=[
        dto_pb2.ExternalMessage(data=b"your_message_data"),
    ],
    expiration_ns=expiration,
    verification_rules=[]
)

# Send the bundle
response = searcher.send_bundle(bundle)
print(f"Bundle sent with ID: {response.id}")
```

### Subscribe to Bundle Results

```python
import asyncio
from sova_sdk import SovaClient

async def main():
    client = SovaClient.new_testnet_client()
    private_key = bytes.fromhex("your_private_key_hex")
    client.authenticate(private_key)

    searcher = client.searcher()

    def on_result(result):
        if result.HasField('win'):
            print(f"Bundle {result.id} won auction {result.win.auction_id}")
            print(f"Estimated tip: {result.win.estimated_nanoton_tip}")
        elif result.HasField('loose'):
            print(f"Bundle {result.id} lost auction {result.loose.auction_id}")

    await searcher.subscribe_bundle_result(on_result)

asyncio.run(main())
```

### Get Tip Addresses

```python
from sova_sdk import SovaClient

client = SovaClient.new_testnet_client()
private_key = bytes.fromhex("your_private_key_hex")
client.authenticate(private_key)

searcher = client.searcher()

# Get tip addresses for bundle inclusion
response = searcher.get_tip_addresses()
print(f"Tip addresses: {response.address}")
```

### Block Engine (Validator Integration)

```python
import asyncio
from sova_sdk import BlockEngineClient, dto_pb2

async def main():
    # Create block engine client
    engine = BlockEngineClient(
        block_engine_url="your-engine-url:port",
        access_token=your_access_token
    )

    # Subscribe to bundles
    def on_bundle(bundle):
        print(f"Received bundle {bundle.id} with {len(bundle.message)} messages")
        for msg in bundle.message:
            print(f"  Message data: {msg.data.hex()}")

    await engine.subscribe_bundles(on_bundle)

asyncio.run(main())
```

### Custom Client Configuration

```python
from sova_sdk import SovaClient

# Create a custom client
client = SovaClient.new_custom_client(
    url="custom-url:port",
    ca_pem="-----BEGIN CERTIFICATE-----\n...",
    domain_name="custom.domain.com"
)

private_key = bytes.fromhex("your_private_key_hex")
client.authenticate(private_key)
```

## API Reference

### SovaClient

Main client for interacting with Sova Network.

**Methods:**
- `new_testnet_client()` - Create a client for testnet
- `new_mainnet_client()` - Create a client for mainnet
- `new_custom_client(url, ca_pem, domain_name, auth_token)` - Create a custom client
- `authenticate(private_key: bytes)` - Authenticate with Ed25519 private key
- `searcher()` - Get a SovaSearcher instance

### SovaSearcher

Client for MEV searchers to interact with the mempool and bundles.

**Methods:**
- `subscribe_by_address(addresses, on_data)` - Subscribe to mempool by addresses
- `subscribe_by_workchain(workchain_id, on_data)` - Subscribe to mempool by workchain
- `subscribe_by_workchain_shard(workchain_id, shard, on_data)` - Subscribe by workchain and shard
- `subscribe_by_external_out_msg_body_opcode(workchain_id, shard, opcode, on_data)` - Subscribe by external message opcode
- `subscribe_by_internal_msg_body_opcode(workchain_id, shard, opcode, on_data)` - Subscribe by internal message opcode
- `send_bundle(bundle)` - Send a bundle of messages
- `get_tip_addresses()` - Get tip addresses for bundle inclusion
- `subscribe_bundle_result(on_data)` - Subscribe to bundle results

### BlockEngineClient

Client for validators to stream mempool and receive bundles.

**Methods:**
- `stream_mempool(packet_stream)` - Stream mempool packets to the engine
- `subscribe_bundles(on_data)` - Subscribe to profitable bundles

### AuthClient

Authentication client for Sova services.

**Methods:**
- `authenticate()` - Perform authentication flow
- `refresh_access_token()` - Refresh the access token
- `get_access_token()` - Get the current access token
- `get_refresh_token()` - Get the refresh token

## Resources

- **GitHub Repository**: [sova-network/sova-sdk-python](https://github.com/serhiibeznisko/sova-sdk-python)
- **Issue Tracker**: [GitHub Issues](https://github.com/serhiibeznisko/sova-sdk-python/issues)
- **PyPI Package**: [pypi.org/project/sova-sdk](https://pypi.org/project/sova-sdk/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For development setup:

```bash
# Clone the repository
git clone https://github.com/serhiibeznisko/sova-sdk-python.git
cd sova-sdk-python

# Install in development mode
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests, please visit our [GitHub Issues](https://github.com/serhiibeznisko/sova-sdk-python/issues) page.
