@ECHO OFF
REM This script install the protocol buffer python files

set TARGET=./src/qciconnect_common/qciconnect_communication/grpc

uv run python -m grpc_tools.protoc ^
  -I. --python_out=%TARGET% --pyi_out=%TARGET% --grpc_python_out=%TARGET%  communication.proto
