"""
Authentication client for Sova SDK.
"""
import ssl
from typing import Optional

import grpc
import nacl.signing

from .generated import auth_pb2, auth_pb2_grpc


class AuthClient:
    """AuthClient wraps the AuthServiceClient and provides convenience methods."""

    def __init__(
        self,
        auth_url: str,
        private_key: bytes,
        ca_pem: Optional[str] = None,
        domain_name: Optional[str] = None
    ):
        """
        Create a new AuthClient instance.

        Args:
            auth_url: The URL of the authentication service
            private_key: 32-byte ed25519 private key seed
            ca_pem: Optional CA certificate in PEM format
            domain_name: Optional domain name for TLS verification
        """
        # Create the signing key from the seed
        self.key = nacl.signing.SigningKey(private_key)
        self.access_token: Optional[auth_pb2.Token] = None
        self.refresh_token: Optional[auth_pb2.Token] = None

        # Create gRPC channel with or without TLS
        if ca_pem and domain_name:
            # Create TLS credentials
            credentials = grpc.ssl_channel_credentials(
                root_certificates=ca_pem.encode('utf-8')
            )
            # Create secure channel with TLS
            channel = grpc.secure_channel(
                auth_url,
                credentials,
                options=[('grpc.ssl_target_name_override', domain_name)]
            )
        else:
            # Create insecure channel
            channel = grpc.insecure_channel(auth_url)

        self.client = auth_pb2_grpc.AuthServiceStub(channel)

    def authenticate(self) -> None:
        """
        Perform authentication flow.

        Raises:
            grpc.RpcError: If authentication fails
        """
        # Get public key
        pubkey = bytes(self.key.verify_key)

        # Request challenge
        challenge_req = auth_pb2.GenerateAuthChallengeRequest(pubkey=pubkey)
        challenge_resp = self.client.GenerateAuthChallenge(challenge_req)
        challenge = challenge_resp.challenge

        # Sign the challenge
        signed_challenge = self.key.sign(challenge).signature

        # Request tokens
        token_req = auth_pb2.GenerateAuthTokensRequest(
            challenge=challenge,
            signed_challenge=signed_challenge
        )
        token_resp = self.client.GenerateAuthTokens(token_req)

        self.access_token = token_resp.access_token
        self.refresh_token = token_resp.refresh_token

    def refresh_access_token(self) -> None:
        """
        Refresh the access token using the refresh token.

        Raises:
            ValueError: If refresh token is not available
            grpc.RpcError: If token refresh fails
        """
        if not self.refresh_token:
            raise ValueError("Refresh token is required")

        refresh_req = auth_pb2.RefreshAccessTokenRequest(
            refresh_token=self.refresh_token.value
        )
        token_resp = self.client.RefreshAccessToken(refresh_req)
        self.access_token = token_resp.access_token

    def get_access_token(self) -> Optional[auth_pb2.Token]:
        """Get the current access token."""
        return self.access_token

    def get_refresh_token(self) -> Optional[auth_pb2.Token]:
        """Get the current refresh token."""
        return self.refresh_token
