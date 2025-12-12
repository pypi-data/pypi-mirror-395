#!/usr/bin/env bash

# This script install the protocol buffer python files

uv run python -m grpc_tools.protoc -I. \
  --python_out=./src/qciconnect_common/qciconnect_communication/grpc \
  --pyi_out=./src/qciconnect_common/qciconnect_communication/grpc \
  --grpc_python_out=./src/qciconnect_common/qciconnect_communication/grpc \
  communication.proto