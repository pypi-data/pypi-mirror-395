import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateAuthChallengeRequest(_message.Message):
    __slots__ = ("pubkey",)
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    pubkey: bytes
    def __init__(self, pubkey: _Optional[bytes] = ...) -> None: ...

class GenerateAuthChallengeResponse(_message.Message):
    __slots__ = ("challenge",)
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    challenge: bytes
    def __init__(self, challenge: _Optional[bytes] = ...) -> None: ...

class GenerateAuthTokensRequest(_message.Message):
    __slots__ = ("challenge", "signed_challenge")
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    SIGNED_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    challenge: bytes
    signed_challenge: bytes
    def __init__(self, challenge: _Optional[bytes] = ..., signed_challenge: _Optional[bytes] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("value", "expires_at_utc")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_UTC_FIELD_NUMBER: _ClassVar[int]
    value: str
    expires_at_utc: _timestamp_pb2.Timestamp
    def __init__(self, value: _Optional[str] = ..., expires_at_utc: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GenerateAuthTokensResponse(_message.Message):
    __slots__ = ("access_token", "refresh_token")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: Token
    refresh_token: Token
    def __init__(self, access_token: _Optional[_Union[Token, _Mapping]] = ..., refresh_token: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class RefreshAccessTokenRequest(_message.Message):
    __slots__ = ("refresh_token",)
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...

class RefreshAccessTokenResponse(_message.Message):
    __slots__ = ("access_token",)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: Token
    def __init__(self, access_token: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...
