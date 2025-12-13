"""
Searcher client for Sova SDK.
"""
import asyncio
import logging
from typing import Optional, Callable, List
import ssl

import grpc
import grpc.aio

from .generated import auth_pb2, searcher_pb2, searcher_pb2_grpc, dto_pb2

logger = logging.getLogger(__name__)


class SovaSearcher:
    """Sova Searcher client for subscribing to mempool and sending bundles."""

    def __init__(
        self,
        url: str,
        ca_pem: Optional[str] = None,
        domain_name: Optional[str] = None,
        access_token: Optional[auth_pb2.Token] = None
    ):
        """
        Create a new SovaSearcher instance.

        Args:
            url: The URL of the searcher service
            ca_pem: Optional CA certificate in PEM format
            domain_name: Optional domain name for TLS verification
            access_token: Optional access token for authentication
        """
        self.access_token = access_token

        # Create gRPC channel with or without TLS
        if ca_pem and domain_name:
            # Create TLS credentials
            credentials = grpc.ssl_channel_credentials(
                root_certificates=ca_pem.encode('utf-8')
            )
            # Create secure channel with TLS
            channel = grpc.aio.secure_channel(
                url,
                credentials,
                options=[('grpc.ssl_target_name_override', domain_name)]
            )
        else:
            # Create insecure channel
            channel = grpc.aio.insecure_channel(url)

        self.client = searcher_pb2_grpc.SearcherServiceStub(channel)

    def set_access_token(self, token: auth_pb2.Token) -> None:
        """Set the access token for authentication."""
        self.access_token = token

    def _add_authorization_metadata(self) -> List[tuple]:
        """Add authorization metadata for gRPC calls."""
        if not self.access_token:
            return []
        return [('authorization', f'Bearer {self.access_token.value}')]

    async def subscribe(
        self,
        subscription: searcher_pb2.MempoolSubscription,
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates.

        Args:
            subscription: The mempool subscription configuration
            on_data: Callback function to handle incoming mempool packets

        Raises:
            grpc.RpcError: If subscription fails
        """
        metadata = self._add_authorization_metadata()

        try:
            stream = self.client.SubscribeMempool(subscription, metadata=metadata)
            async for packet in stream:
                on_data(packet)
        except grpc.RpcError as e:
            logger.error(f"Stream error: {e}")
            raise

    async def subscribe_by_address(
        self,
        addresses: List[str],
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates by addresses.

        Args:
            addresses: List of addresses to monitor
            on_data: Callback function to handle incoming mempool packets
        """
        subscription = searcher_pb2.MempoolSubscription(
            addresses=searcher_pb2.AddressSubscriptionV0(address=addresses)
        )
        await self.subscribe(subscription, on_data)

    async def subscribe_by_workchain(
        self,
        workchain_id: int,
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates by workchain.

        Args:
            workchain_id: The workchain ID to monitor
            on_data: Callback function to handle incoming mempool packets
        """
        subscription = searcher_pb2.MempoolSubscription(
            workchain=searcher_pb2.WorkchainSubscriptionV0(workchain_id=workchain_id)
        )
        await self.subscribe(subscription, on_data)

    async def subscribe_by_workchain_shard(
        self,
        workchain_id: int,
        shard: bytes,
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates by workchain and shard.

        Args:
            workchain_id: The workchain ID to monitor
            shard: The shard to monitor
            on_data: Callback function to handle incoming mempool packets
        """
        subscription = searcher_pb2.MempoolSubscription(
            workchainShard=searcher_pb2.WorkchainShardSubscriptionV0(
                workchain_id=workchain_id,
                shard=shard
            )
        )
        await self.subscribe(subscription, on_data)

    async def subscribe_by_external_out_msg_body_opcode(
        self,
        workchain_id: int,
        shard: Optional[bytes],
        opcode: int,
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates by external outgoing message body opcode.

        Args:
            workchain_id: The workchain ID to monitor
            shard: Optional shard to monitor
            opcode: The opcode to match
            on_data: Callback function to handle incoming mempool packets
        """
        subscription = searcher_pb2.MempoolSubscription(
            externalOutMessageBodyOpcode=searcher_pb2.ExternalOutMessageBodyOpcodeSubscriptionV0(
                workchain_id=workchain_id,
                shard=shard,
                opcode=opcode
            )
        )
        await self.subscribe(subscription, on_data)

    async def subscribe_by_internal_msg_body_opcode(
        self,
        workchain_id: int,
        shard: Optional[bytes],
        opcode: int,
        on_data: Callable[[dto_pb2.MempoolPacket], None]
    ) -> None:
        """
        Subscribe to mempool updates by internal message body opcode.

        Args:
            workchain_id: The workchain ID to monitor
            shard: Optional shard to monitor
            opcode: The opcode to match
            on_data: Callback function to handle incoming mempool packets
        """
        subscription = searcher_pb2.MempoolSubscription(
            internalMessageBodyOpcode=searcher_pb2.InternalMessageBodyOpcodeSubscriptionV0(
                workchain_id=workchain_id,
                shard=shard,
                opcode=opcode
            )
        )
        await self.subscribe(subscription, on_data)

    async def send_bundle(self, bundle: dto_pb2.Bundle) -> searcher_pb2.SendBundleResponse:
        """
        Send a bundle of messages.

        Args:
            bundle: The bundle to send

        Returns:
            The response containing the bundle ID

        Raises:
            grpc.RpcError: If sending the bundle fails
        """
        metadata = self._add_authorization_metadata()
        return await self.client.SendBundle(bundle, metadata=metadata)

    async def get_tip_addresses(self) -> searcher_pb2.GetTipAddressesResponse:
        """
        Get the tip addresses for message inclusion.

        Returns:
            The response containing tip addresses

        Raises:
            grpc.RpcError: If getting tip addresses fails
        """
        metadata = self._add_authorization_metadata()
        request = searcher_pb2.GetTipAddressesRequest()
        return await self.client.GetTipAddresses(request, metadata=metadata)

    async def subscribe_bundle_result(
        self,
        on_data: Callable[[searcher_pb2.BundleResult], None]
    ) -> None:
        """
        Subscribe to bundle results.

        Args:
            on_data: Callback function to handle incoming bundle results

        Raises:
            grpc.RpcError: If subscription fails
        """
        metadata = self._add_authorization_metadata()
        request = searcher_pb2.SubscribeBundleResultsRequest()

        try:
            stream = self.client.SubscribeBundleResults(request, metadata=metadata)
            async for result in stream:
                on_data(result)
        except grpc.RpcError as e:
            logger.error(f"Stream error: {e}")
            raise
