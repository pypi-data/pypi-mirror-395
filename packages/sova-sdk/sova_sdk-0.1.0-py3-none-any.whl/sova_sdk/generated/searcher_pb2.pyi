import dto_pb2 as _dto_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddressSubscriptionV0(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, address: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkchainSubscriptionV0(_message.Message):
    __slots__ = ("workchain_id",)
    WORKCHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    workchain_id: int
    def __init__(self, workchain_id: _Optional[int] = ...) -> None: ...

class WorkchainShardSubscriptionV0(_message.Message):
    __slots__ = ("workchain_id", "shard")
    WORKCHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_FIELD_NUMBER: _ClassVar[int]
    workchain_id: int
    shard: bytes
    def __init__(self, workchain_id: _Optional[int] = ..., shard: _Optional[bytes] = ...) -> None: ...

class ExternalOutMessageBodyOpcodeSubscriptionV0(_message.Message):
    __slots__ = ("workchain_id", "shard", "opcode")
    WORKCHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    workchain_id: int
    shard: bytes
    opcode: int
    def __init__(self, workchain_id: _Optional[int] = ..., shard: _Optional[bytes] = ..., opcode: _Optional[int] = ...) -> None: ...

class InternalMessageBodyOpcodeSubscriptionV0(_message.Message):
    __slots__ = ("workchain_id", "shard", "opcode")
    WORKCHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_FIELD_NUMBER: _ClassVar[int]
    OPCODE_FIELD_NUMBER: _ClassVar[int]
    workchain_id: int
    shard: bytes
    opcode: int
    def __init__(self, workchain_id: _Optional[int] = ..., shard: _Optional[bytes] = ..., opcode: _Optional[int] = ...) -> None: ...

class MempoolSubscription(_message.Message):
    __slots__ = ("addresses", "workchain", "workchainShard", "externalOutMessageBodyOpcode", "internalMessageBodyOpcode")
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    WORKCHAIN_FIELD_NUMBER: _ClassVar[int]
    WORKCHAINSHARD_FIELD_NUMBER: _ClassVar[int]
    EXTERNALOUTMESSAGEBODYOPCODE_FIELD_NUMBER: _ClassVar[int]
    INTERNALMESSAGEBODYOPCODE_FIELD_NUMBER: _ClassVar[int]
    addresses: AddressSubscriptionV0
    workchain: WorkchainSubscriptionV0
    workchainShard: WorkchainShardSubscriptionV0
    externalOutMessageBodyOpcode: ExternalOutMessageBodyOpcodeSubscriptionV0
    internalMessageBodyOpcode: InternalMessageBodyOpcodeSubscriptionV0
    def __init__(self, addresses: _Optional[_Union[AddressSubscriptionV0, _Mapping]] = ..., workchain: _Optional[_Union[WorkchainSubscriptionV0, _Mapping]] = ..., workchainShard: _Optional[_Union[WorkchainShardSubscriptionV0, _Mapping]] = ..., externalOutMessageBodyOpcode: _Optional[_Union[ExternalOutMessageBodyOpcodeSubscriptionV0, _Mapping]] = ..., internalMessageBodyOpcode: _Optional[_Union[InternalMessageBodyOpcodeSubscriptionV0, _Mapping]] = ...) -> None: ...

class SendBundleResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTipAddressesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTipAddressesResponse(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, address: _Optional[_Iterable[str]] = ...) -> None: ...

class SubscribeBundleResultsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BundleResultAuctionWin(_message.Message):
    __slots__ = ("auction_id", "estimated_nanoton_tip")
    AUCTION_ID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_NANOTON_TIP_FIELD_NUMBER: _ClassVar[int]
    auction_id: str
    estimated_nanoton_tip: int
    def __init__(self, auction_id: _Optional[str] = ..., estimated_nanoton_tip: _Optional[int] = ...) -> None: ...

class BundleResultAuctionLoose(_message.Message):
    __slots__ = ("auction_id",)
    AUCTION_ID_FIELD_NUMBER: _ClassVar[int]
    auction_id: str
    def __init__(self, auction_id: _Optional[str] = ...) -> None: ...

class BundleResult(_message.Message):
    __slots__ = ("id", "win", "loose")
    ID_FIELD_NUMBER: _ClassVar[int]
    WIN_FIELD_NUMBER: _ClassVar[int]
    LOOSE_FIELD_NUMBER: _ClassVar[int]
    id: str
    win: BundleResultAuctionWin
    loose: BundleResultAuctionLoose
    def __init__(self, id: _Optional[str] = ..., win: _Optional[_Union[BundleResultAuctionWin, _Mapping]] = ..., loose: _Optional[_Union[BundleResultAuctionLoose, _Mapping]] = ...) -> None: ...
