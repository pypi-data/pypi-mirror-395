from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatMessageRequest(_message.Message):
    __slots__ = ("thread_id", "message", "sender_id", "recipient_id", "session_id")
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    thread_id: int
    message: str
    sender_id: str
    recipient_id: str
    session_id: str
    def __init__(self, thread_id: _Optional[int] = ..., message: _Optional[str] = ..., sender_id: _Optional[str] = ..., recipient_id: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...

class ChatMessageResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("id", "thread_id", "message", "sender_id", "recipient_id", "session_id", "timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: int
    thread_id: int
    message: str
    sender_id: str
    recipient_id: str
    session_id: str
    timestamp: str
    def __init__(self, id: _Optional[int] = ..., thread_id: _Optional[int] = ..., message: _Optional[str] = ..., sender_id: _Optional[str] = ..., recipient_id: _Optional[str] = ..., session_id: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class ChatClient(_message.Message):
    __slots__ = ("recipient_id", "session_id")
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    recipient_id: str
    session_id: str
    def __init__(self, recipient_id: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...
