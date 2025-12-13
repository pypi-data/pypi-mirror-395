
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/match_service.proto')
_sym_db = _symbol_database.Default()
from ..models import bracket_pb2 as models_dot_bracket__pb2
from ..models import filter_pb2 as models_dot_filter__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cservices/match_service.proto\x12\x10parrygg.services\x1a\x14models/bracket.proto\x1a\x13models/filter.proto"\x1d\n\x0fGetMatchRequest\x12\n\n\x02id\x18\x01 \x01(\t"8\n\x10GetMatchResponse\x12$\n\x05match\x18\x01 \x01(\x0b2\x15.parrygg.models.Match"B\n\x11GetMatchesRequest\x12-\n\x06filter\x18\x01 \x01(\x0b2\x1d.parrygg.models.MatchesFilter"I\n\x12GetMatchesResponse\x12-\n\x07matches\x18\x02 \x03(\x0b2\x1c.parrygg.models.MatchContextJ\x04\x08\x01\x10\x02"P\n\x15SetMatchResultRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12+\n\x06result\x18\x02 \x01(\x0b2\x1b.parrygg.models.MatchResult"\x18\n\x16SetMatchResultResponse"\x1f\n\x11ResetMatchRequest\x12\n\n\x02id\x18\x01 \x01(\t"\x14\n\x12ResetMatchResponse"\x1f\n\x11StartMatchRequest\x12\n\n\x02id\x18\x01 \x01(\t"\x14\n\x12StartMatchResponse2\xdb\x03\n\x0cMatchService\x12S\n\x08GetMatch\x12!.parrygg.services.GetMatchRequest\x1a".parrygg.services.GetMatchResponse"\x00\x12Y\n\nGetMatches\x12#.parrygg.services.GetMatchesRequest\x1a$.parrygg.services.GetMatchesResponse"\x00\x12e\n\x0eSetMatchResult\x12\'.parrygg.services.SetMatchResultRequest\x1a(.parrygg.services.SetMatchResultResponse"\x00\x12Y\n\nStartMatch\x12#.parrygg.services.StartMatchRequest\x1a$.parrygg.services.StartMatchResponse"\x00\x12Y\n\nResetMatch\x12#.parrygg.services.ResetMatchRequest\x1a$.parrygg.services.ResetMatchResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.match_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_GETMATCHREQUEST']._serialized_start = 93
    _globals['_GETMATCHREQUEST']._serialized_end = 122
    _globals['_GETMATCHRESPONSE']._serialized_start = 124
    _globals['_GETMATCHRESPONSE']._serialized_end = 180
    _globals['_GETMATCHESREQUEST']._serialized_start = 182
    _globals['_GETMATCHESREQUEST']._serialized_end = 248
    _globals['_GETMATCHESRESPONSE']._serialized_start = 250
    _globals['_GETMATCHESRESPONSE']._serialized_end = 323
    _globals['_SETMATCHRESULTREQUEST']._serialized_start = 325
    _globals['_SETMATCHRESULTREQUEST']._serialized_end = 405
    _globals['_SETMATCHRESULTRESPONSE']._serialized_start = 407
    _globals['_SETMATCHRESULTRESPONSE']._serialized_end = 431
    _globals['_RESETMATCHREQUEST']._serialized_start = 433
    _globals['_RESETMATCHREQUEST']._serialized_end = 464
    _globals['_RESETMATCHRESPONSE']._serialized_start = 466
    _globals['_RESETMATCHRESPONSE']._serialized_end = 486
    _globals['_STARTMATCHREQUEST']._serialized_start = 488
    _globals['_STARTMATCHREQUEST']._serialized_end = 519
    _globals['_STARTMATCHRESPONSE']._serialized_start = 521
    _globals['_STARTMATCHRESPONSE']._serialized_end = 541
    _globals['_MATCHSERVICE']._serialized_start = 544
    _globals['_MATCHSERVICE']._serialized_end = 1019
