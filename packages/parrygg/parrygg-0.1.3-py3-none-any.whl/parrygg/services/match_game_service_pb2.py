
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/match_game_service.proto')
_sym_db = _symbol_database.Default()
from ..models import bracket_pb2 as models_dot_bracket__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!services/match_game_service.proto\x12\x10parrygg.services\x1a\x14models/bracket.proto"a\n\x16CreateMatchGameRequest\x12\x10\n\x08match_id\x18\x01 \x01(\t\x125\n\nmatch_game\x18\x02 \x01(\x0b2!.parrygg.models.MatchGameMutation"H\n\x17CreateMatchGameResponse\x12-\n\nmatch_game\x18\x01 \x01(\x0b2\x19.parrygg.models.MatchGame"[\n\x16UpdateMatchGameRequest\x12\n\n\x02id\x18\x01 \x01(\t\x125\n\nmatch_game\x18\x02 \x01(\x0b2!.parrygg.models.MatchGameMutation"H\n\x17UpdateMatchGameResponse\x12-\n\nmatch_game\x18\x01 \x01(\x0b2\x19.parrygg.models.MatchGame"$\n\x16DeleteMatchGameRequest\x12\n\n\x02id\x18\x01 \x01(\t"H\n\x17DeleteMatchGameResponse\x12-\n\nmatch_game\x18\x01 \x01(\x0b2\x19.parrygg.models.MatchGame2\xd0\x02\n\x10MatchGameService\x12h\n\x0fCreateMatchGame\x12(.parrygg.services.CreateMatchGameRequest\x1a).parrygg.services.CreateMatchGameResponse"\x00\x12h\n\x0fUpdateMatchGame\x12(.parrygg.services.UpdateMatchGameRequest\x1a).parrygg.services.UpdateMatchGameResponse"\x00\x12h\n\x0fDeleteMatchGame\x12(.parrygg.services.DeleteMatchGameRequest\x1a).parrygg.services.DeleteMatchGameResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.match_game_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_CREATEMATCHGAMEREQUEST']._serialized_start = 77
    _globals['_CREATEMATCHGAMEREQUEST']._serialized_end = 174
    _globals['_CREATEMATCHGAMERESPONSE']._serialized_start = 176
    _globals['_CREATEMATCHGAMERESPONSE']._serialized_end = 248
    _globals['_UPDATEMATCHGAMEREQUEST']._serialized_start = 250
    _globals['_UPDATEMATCHGAMEREQUEST']._serialized_end = 341
    _globals['_UPDATEMATCHGAMERESPONSE']._serialized_start = 343
    _globals['_UPDATEMATCHGAMERESPONSE']._serialized_end = 415
    _globals['_DELETEMATCHGAMEREQUEST']._serialized_start = 417
    _globals['_DELETEMATCHGAMEREQUEST']._serialized_end = 453
    _globals['_DELETEMATCHGAMERESPONSE']._serialized_start = 455
    _globals['_DELETEMATCHGAMERESPONSE']._serialized_end = 527
    _globals['_MATCHGAMESERVICE']._serialized_start = 530
    _globals['_MATCHGAMESERVICE']._serialized_end = 866
