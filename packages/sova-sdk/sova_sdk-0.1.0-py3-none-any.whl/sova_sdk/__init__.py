"""
Sova SDK - Python SDK for Sova Network MEV infrastructure on TON blockchain.
"""

from .client import SovaClient
from .auth import AuthClient
from .searcher import SovaSearcher
from .block_engine import BlockEngineClient
from .constants import TESTNET_CA_PEM, MAINNET_CA_PEM

# Import generated types for convenience
from .generated import auth_pb2, searcher_pb2, block_engine_pb2, dto_pb2

__version__ = "0.1.0"

__all__ = [
    "SovaClient",
    "AuthClient",
    "SovaSearcher",
    "BlockEngineClient",
    "TESTNET_CA_PEM",
    "MAINNET_CA_PEM",
    # Generated types
    "auth_pb2",
    "searcher_pb2",
    "block_engine_pb2",
    "dto_pb2",
]
