
'Client and server classes corresponding to protobuf-defined services.'
import grpc
import warnings
from ..services import progression_group_settings_service_pb2 as services_dot_progression__group__settings__service__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(((((f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in services/progression_group_settings_service_pb2_grpc.py depends on') + f' grpcio>={GRPC_GENERATED_VERSION}.') + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}') + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'))

class ProgressionGroupSettingsServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.GetProgressionGroupSettings = channel.unary_unary('/parrygg.services.ProgressionGroupSettingsService/GetProgressionGroupSettings', request_serializer=services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsRequest.SerializeToString, response_deserializer=services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsResponse.FromString, _registered_method=True)

class ProgressionGroupSettingsServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def GetProgressionGroupSettings(self, request, context):
        'Retrieves progression group settings by ID.\n        '
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_ProgressionGroupSettingsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'GetProgressionGroupSettings': grpc.unary_unary_rpc_method_handler(servicer.GetProgressionGroupSettings, request_deserializer=services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsRequest.FromString, response_serializer=services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('parrygg.services.ProgressionGroupSettingsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('parrygg.services.ProgressionGroupSettingsService', rpc_method_handlers)

class ProgressionGroupSettingsService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def GetProgressionGroupSettings(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/parrygg.services.ProgressionGroupSettingsService/GetProgressionGroupSettings', services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsRequest.SerializeToString, services_dot_progression__group__settings__service__pb2.GetProgressionGroupSettingsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
