from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ("input_circuit", "compilation_pass", "options")
    INPUT_CIRCUIT_FIELD_NUMBER: _ClassVar[int]
    COMPILATION_PASS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    input_circuit: str
    compilation_pass: str
    options: str
    def __init__(self, input_circuit: _Optional[str] = ..., compilation_pass: _Optional[str] = ..., options: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("output", "error")
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    output: str
    error: int
    def __init__(self, output: _Optional[str] = ..., error: _Optional[int] = ...) -> None: ...
