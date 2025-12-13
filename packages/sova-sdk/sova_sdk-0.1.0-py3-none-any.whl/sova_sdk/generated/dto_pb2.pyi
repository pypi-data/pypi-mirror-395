import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MempoolInternalMessage(_message.Message):
    __slots__ = ("ihr_disabled", "bounce", "bounced", "src", "dest", "value", "ihr_fee", "fwd_fee", "created_lt", "created_at")
    IHR_DISABLED_FIELD_NUMBER: _ClassVar[int]
    BOUNCE_FIELD_NUMBER: _ClassVar[int]
    BOUNCED_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IHR_FEE_FIELD_NUMBER: _ClassVar[int]
    FWD_FEE_FIELD_NUMBER: _ClassVar[int]
    CREATED_LT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ihr_disabled: bool
    bounce: bool
    bounced: bool
    src: bytes
    dest: bytes
    value: bytes
    ihr_fee: bytes
    fwd_fee: bytes
    created_lt: int
    created_at: int
    def __init__(self, ihr_disabled: bool = ..., bounce: bool = ..., bounced: bool = ..., src: _Optional[bytes] = ..., dest: _Optional[bytes] = ..., value: _Optional[bytes] = ..., ihr_fee: _Optional[bytes] = ..., fwd_fee: _Optional[bytes] = ..., created_lt: _Optional[int] = ..., created_at: _Optional[int] = ...) -> None: ...

class MempoolExternalInMessage(_message.Message):
    __slots__ = ("src", "dest", "created_lt", "created_at")
    SRC_FIELD_NUMBER: _ClassVar[int]
    DEST_FIELD_NUMBER: _ClassVar[int]
    CREATED_LT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    src: bytes
    dest: bytes
    created_lt: int
    created_at: int
    def __init__(self, src: _Optional[bytes] = ..., dest: _Optional[bytes] = ..., created_lt: _Optional[int] = ..., created_at: _Optional[int] = ...) -> None: ...

class MempoolProcessedMessage(_message.Message):
    __slots__ = ("hash", "internal_message", "external_in_message", "init", "in_msg", "gas_spent", "out_msgs", "compute_phase_success", "compute_phase_msg_state_used", "compute_phase_account_activated", "compute_phase_out_of_gas", "compute_phase_accepted", "compute_phase_exit_code", "action_phase_success", "action_phase_result_code")
    class Init(_message.Message):
        __slots__ = ("code", "data")
        CODE_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        code: bytes
        data: bytes
        def __init__(self, code: _Optional[bytes] = ..., data: _Optional[bytes] = ...) -> None: ...
    HASH_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_IN_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    IN_MSG_FIELD_NUMBER: _ClassVar[int]
    GAS_SPENT_FIELD_NUMBER: _ClassVar[int]
    OUT_MSGS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_MSG_STATE_USED_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_ACCOUNT_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_OUT_OF_GAS_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_PHASE_EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    ACTION_PHASE_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ACTION_PHASE_RESULT_CODE_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    internal_message: MempoolInternalMessage
    external_in_message: MempoolExternalInMessage
    init: MempoolProcessedMessage.Init
    in_msg: bytes
    gas_spent: int
    out_msgs: _containers.RepeatedScalarFieldContainer[bytes]
    compute_phase_success: bool
    compute_phase_msg_state_used: bool
    compute_phase_account_activated: bool
    compute_phase_out_of_gas: bool
    compute_phase_accepted: bool
    compute_phase_exit_code: int
    action_phase_success: bool
    action_phase_result_code: int
    def __init__(self, hash: _Optional[bytes] = ..., internal_message: _Optional[_Union[MempoolInternalMessage, _Mapping]] = ..., external_in_message: _Optional[_Union[MempoolExternalInMessage, _Mapping]] = ..., init: _Optional[_Union[MempoolProcessedMessage.Init, _Mapping]] = ..., in_msg: _Optional[bytes] = ..., gas_spent: _Optional[int] = ..., out_msgs: _Optional[_Iterable[bytes]] = ..., compute_phase_success: bool = ..., compute_phase_msg_state_used: bool = ..., compute_phase_account_activated: bool = ..., compute_phase_out_of_gas: bool = ..., compute_phase_accepted: bool = ..., compute_phase_exit_code: _Optional[int] = ..., action_phase_success: bool = ..., action_phase_result_code: _Optional[int] = ...) -> None: ...

class MempoolExternalMessage(_message.Message):
    __slots__ = ("hash", "workchain_id", "shard", "data", "std_smc_address", "gas_spent", "out_msgs", "processed_messages")
    HASH_FIELD_NUMBER: _ClassVar[int]
    WORKCHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    STD_SMC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GAS_SPENT_FIELD_NUMBER: _ClassVar[int]
    OUT_MSGS_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    workchain_id: int
    shard: bytes
    data: bytes
    std_smc_address: bytes
    gas_spent: int
    out_msgs: _containers.RepeatedScalarFieldContainer[bytes]
    processed_messages: _containers.RepeatedCompositeFieldContainer[MempoolProcessedMessage]
    def __init__(self, hash: _Optional[bytes] = ..., workchain_id: _Optional[int] = ..., shard: _Optional[bytes] = ..., data: _Optional[bytes] = ..., std_smc_address: _Optional[bytes] = ..., gas_spent: _Optional[int] = ..., out_msgs: _Optional[_Iterable[bytes]] = ..., processed_messages: _Optional[_Iterable[_Union[MempoolProcessedMessage, _Mapping]]] = ...) -> None: ...

class MempoolPacket(_message.Message):
    __slots__ = ("server_ts", "expiration_ns", "external_messages")
    SERVER_TS_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_NS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    server_ts: _timestamp_pb2.Timestamp
    expiration_ns: int
    external_messages: _containers.RepeatedCompositeFieldContainer[MempoolExternalMessage]
    def __init__(self, server_ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., expiration_ns: _Optional[int] = ..., external_messages: _Optional[_Iterable[_Union[MempoolExternalMessage, _Mapping]]] = ...) -> None: ...

class ExternalMessage(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class ExpectGenerateMessage(_message.Message):
    __slots__ = ("is_internal", "std_smc_address", "in_msg_body_opcode")
    IS_INTERNAL_FIELD_NUMBER: _ClassVar[int]
    STD_SMC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IN_MSG_BODY_OPCODE_FIELD_NUMBER: _ClassVar[int]
    is_internal: bool
    std_smc_address: bytes
    in_msg_body_opcode: int
    def __init__(self, is_internal: bool = ..., std_smc_address: _Optional[bytes] = ..., in_msg_body_opcode: _Optional[int] = ...) -> None: ...

class BundleVerificationRule(_message.Message):
    __slots__ = ("expect_message",)
    EXPECT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    expect_message: ExpectGenerateMessage
    def __init__(self, expect_message: _Optional[_Union[ExpectGenerateMessage, _Mapping]] = ...) -> None: ...

class ValidatorBundle(_message.Message):
    __slots__ = ("message", "expiration_ns", "id", "verification_rules")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_NS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_RULES_FIELD_NUMBER: _ClassVar[int]
    message: _containers.RepeatedCompositeFieldContainer[ExternalMessage]
    expiration_ns: _timestamp_pb2.Timestamp
    id: str
    verification_rules: _containers.RepeatedCompositeFieldContainer[BundleVerificationRule]
    def __init__(self, message: _Optional[_Iterable[_Union[ExternalMessage, _Mapping]]] = ..., expiration_ns: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., verification_rules: _Optional[_Iterable[_Union[BundleVerificationRule, _Mapping]]] = ...) -> None: ...

class Bundle(_message.Message):
    __slots__ = ("message", "expiration_ns", "verification_rules")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_NS_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_RULES_FIELD_NUMBER: _ClassVar[int]
    message: _containers.RepeatedCompositeFieldContainer[ExternalMessage]
    expiration_ns: _timestamp_pb2.Timestamp
    verification_rules: _containers.RepeatedCompositeFieldContainer[BundleVerificationRule]
    def __init__(self, message: _Optional[_Iterable[_Union[ExternalMessage, _Mapping]]] = ..., expiration_ns: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., verification_rules: _Optional[_Iterable[_Union[BundleVerificationRule, _Mapping]]] = ...) -> None: ...
