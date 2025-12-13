
'Client and server classes corresponding to protobuf-defined services.'
import grpc
import warnings
from ..services import match_game_service_pb2 as services_dot_match__game__service__pb2
GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(((((f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in services/match_game_service_pb2_grpc.py depends on') + f' grpcio>={GRPC_GENERATED_VERSION}.') + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}') + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'))

class MatchGameServiceStub(object):
    'MatchGameService provides match game management operations.\n    Handles individual games within matches including stage selection and per-game scoring.\n    '

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.CreateMatchGame = channel.unary_unary('/parrygg.services.MatchGameService/CreateMatchGame', request_serializer=services_dot_match__game__service__pb2.CreateMatchGameRequest.SerializeToString, response_deserializer=services_dot_match__game__service__pb2.CreateMatchGameResponse.FromString, _registered_method=True)
        self.UpdateMatchGame = channel.unary_unary('/parrygg.services.MatchGameService/UpdateMatchGame', request_serializer=services_dot_match__game__service__pb2.UpdateMatchGameRequest.SerializeToString, response_deserializer=services_dot_match__game__service__pb2.UpdateMatchGameResponse.FromString, _registered_method=True)
        self.DeleteMatchGame = channel.unary_unary('/parrygg.services.MatchGameService/DeleteMatchGame', request_serializer=services_dot_match__game__service__pb2.DeleteMatchGameRequest.SerializeToString, response_deserializer=services_dot_match__game__service__pb2.DeleteMatchGameResponse.FromString, _registered_method=True)

class MatchGameServiceServicer(object):
    'MatchGameService provides match game management operations.\n    Handles individual games within matches including stage selection and per-game scoring.\n    '

    def CreateMatchGame(self, request, context):
        'Create a new game within a match.\n        '
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMatchGame(self, request, context):
        "Update an existing match game's data.\n        "
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMatchGame(self, request, context):
        'Delete a match game from its parent match.\n        '
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_MatchGameServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateMatchGame': grpc.unary_unary_rpc_method_handler(servicer.CreateMatchGame, request_deserializer=services_dot_match__game__service__pb2.CreateMatchGameRequest.FromString, response_serializer=services_dot_match__game__service__pb2.CreateMatchGameResponse.SerializeToString), 'UpdateMatchGame': grpc.unary_unary_rpc_method_handler(servicer.UpdateMatchGame, request_deserializer=services_dot_match__game__service__pb2.UpdateMatchGameRequest.FromString, response_serializer=services_dot_match__game__service__pb2.UpdateMatchGameResponse.SerializeToString), 'DeleteMatchGame': grpc.unary_unary_rpc_method_handler(servicer.DeleteMatchGame, request_deserializer=services_dot_match__game__service__pb2.DeleteMatchGameRequest.FromString, response_serializer=services_dot_match__game__service__pb2.DeleteMatchGameResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('parrygg.services.MatchGameService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('parrygg.services.MatchGameService', rpc_method_handlers)

class MatchGameService(object):
    'MatchGameService provides match game management operations.\n    Handles individual games within matches including stage selection and per-game scoring.\n    '

    @staticmethod
    def CreateMatchGame(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/parrygg.services.MatchGameService/CreateMatchGame', services_dot_match__game__service__pb2.CreateMatchGameRequest.SerializeToString, services_dot_match__game__service__pb2.CreateMatchGameResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateMatchGame(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/parrygg.services.MatchGameService/UpdateMatchGame', services_dot_match__game__service__pb2.UpdateMatchGameRequest.SerializeToString, services_dot_match__game__service__pb2.UpdateMatchGameResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteMatchGame(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/parrygg.services.MatchGameService/DeleteMatchGame', services_dot_match__game__service__pb2.DeleteMatchGameRequest.SerializeToString, services_dot_match__game__service__pb2.DeleteMatchGameResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)
