"""
Block Engine client for Sova SDK.
"""
import logging
from typing import Optional, Callable, AsyncIterator

import grpc

from .generated import auth_pb2, block_engine_pb2, block_engine_pb2_grpc, dto_pb2

logger = logging.getLogger(__name__)


class BlockEngineClient:
    """Block Engine client for validators to stream mempool and subscribe to bundles."""

    def __init__(
        self,
        block_engine_url: str,
        access_token: Optional[auth_pb2.Token] = None
    ):
        """
        Create a new BlockEngineClient instance.

        Args:
            block_engine_url: The URL of the block engine service
            access_token: Optional access token for authentication
        """
        self.access_token = access_token

        # Create insecure channel with keepalive parameters
        options = [
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 60000),
            ('grpc.keepalive_permit_without_stream', 1),
        ]
        channel = grpc.insecure_channel(block_engine_url, options=options)

        self.client = block_engine_pb2_grpc.BlockEngineValidatorStub(channel)

    def _add_authorization_metadata(self):
        """Add authorization metadata for gRPC calls."""
        if not self.access_token:
            return []
        return [('authorization', f'Bearer {self.access_token.value}')]

    async def stream_mempool(
        self,
        packet_stream: AsyncIterator[dto_pb2.MempoolPacket]
    ) -> block_engine_pb2.StreamMempoolResponse:
        """
        Stream mempool packets to the block engine.

        Args:
            packet_stream: An async iterator of mempool packets to stream

        Returns:
            The stream response

        Raises:
            grpc.RpcError: If streaming fails
        """
        metadata = self._add_authorization_metadata()

        try:
            response = self.client.StreamMempool(packet_stream, metadata=metadata)
            return response
        except grpc.RpcError as e:
            logger.error(f"Failed to stream mempool: {e}")
            raise

    async def subscribe_bundles(
        self,
        on_data: Callable[[dto_pb2.ValidatorBundle], None]
    ) -> None:
        """
        Subscribe to profitable bundles from the block engine.

        Args:
            on_data: Callback function to handle incoming bundles

        Raises:
            grpc.RpcError: If subscription fails
        """
        metadata = self._add_authorization_metadata()
        request = block_engine_pb2.SubscribeBundlesRequest()

        try:
            stream = self.client.SubscribeBundles(request, metadata=metadata)
            for bundle in stream:
                on_data(bundle)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.CANCELLED:
                logger.error(f"Stream error: {e}")
            raise
