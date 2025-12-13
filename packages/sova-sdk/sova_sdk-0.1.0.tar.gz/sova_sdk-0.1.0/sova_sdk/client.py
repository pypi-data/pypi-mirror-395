"""
Main Sova SDK client.
"""
from typing import Optional

from .auth import AuthClient
from .searcher import SovaSearcher
from .constants import TESTNET_CA_PEM, MAINNET_CA_PEM
from .generated import auth_pb2


class SovaClient:
    """Main Sova SDK client for interacting with Sova Network."""

    def __init__(
        self,
        url: str,
        ca_pem: Optional[str] = None,
        domain_name: Optional[str] = None,
        auth_token: Optional[auth_pb2.Token] = None
    ):
        """
        Create a new SovaClient instance.

        Args:
            url: The URL of the Sova service
            ca_pem: Optional CA certificate in PEM format
            domain_name: Optional domain name for TLS verification
            auth_token: Optional pre-existing auth token
        """
        self.url = url
        self.ca_pem = ca_pem
        self.domain_name = domain_name
        self.auth_token = auth_token

    @staticmethod
    def new_testnet_client() -> "SovaClient":
        """
        Create a new client configured for Sova testnet.

        Returns:
            A SovaClient configured for testnet
        """
        return SovaClient(
            url="testnet-engine.sova.network:30020",
            ca_pem=TESTNET_CA_PEM,
            domain_name="testnet-engine.sova.network",
            auth_token=None
        )

    @staticmethod
    def new_mainnet_client() -> "SovaClient":
        """
        Create a new client configured for Sova mainnet.

        Returns:
            A SovaClient configured for mainnet
        """
        return SovaClient(
            url="engine.sova.network:30020",
            ca_pem=MAINNET_CA_PEM,
            domain_name="engine.sova.network",
            auth_token=None
        )

    @staticmethod
    def new_custom_client(
        url: str,
        ca_pem: Optional[str] = None,
        domain_name: Optional[str] = None,
        auth_token: Optional[auth_pb2.Token] = None
    ) -> "SovaClient":
        """
        Create a new custom client.

        Args:
            url: The URL of the Sova service
            ca_pem: Optional CA certificate in PEM format
            domain_name: Optional domain name for TLS verification
            auth_token: Optional pre-existing auth token

        Returns:
            A SovaClient with custom configuration
        """
        return SovaClient(
            url=url,
            ca_pem=ca_pem,
            domain_name=domain_name,
            auth_token=auth_token
        )

    def authenticate(self, private_key: bytes) -> auth_pb2.Token:
        """
        Perform authentication with the provided private key.

        Args:
            private_key: 32-byte ed25519 private key seed

        Returns:
            The access token

        Raises:
            grpc.RpcError: If authentication fails
        """
        auth = AuthClient(
            auth_url=self.url,
            private_key=private_key,
            ca_pem=self.ca_pem,
            domain_name=self.domain_name
        )
        auth.authenticate()
        token = auth.get_access_token()
        self.auth_token = token
        return token

    def searcher(self) -> SovaSearcher:
        """
        Get a Searcher client instance.

        Returns:
            A SovaSearcher client configured with this client's settings

        Raises:
            ValueError: If authentication token is not set
        """
        if not self.auth_token:
            raise ValueError("Authentication token is required. Call authenticate() first.")

        return SovaSearcher(
            url=self.url,
            ca_pem=self.ca_pem,
            domain_name=self.domain_name,
            access_token=self.auth_token
        )
