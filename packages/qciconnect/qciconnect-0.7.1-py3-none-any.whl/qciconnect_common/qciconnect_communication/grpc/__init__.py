from importlib import import_module
import sys

_messages_module = import_module(".communication_pb2", package=__name__)
sys.modules.setdefault("communication_pb2", _messages_module)

from .communication_pb2_grpc import add_CommunicationServicer_to_server, CommunicationStub
from .communication_pb2 import Request, Response

from .grpc_setting import CommunicationSetting
settings = CommunicationSetting()
del CommunicationSetting
