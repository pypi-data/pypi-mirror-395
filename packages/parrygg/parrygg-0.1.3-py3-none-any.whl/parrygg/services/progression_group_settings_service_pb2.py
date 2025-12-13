
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/progression_group_settings_service.proto')
_sym_db = _symbol_database.Default()
from ..models import progression_pb2 as models_dot_progression__pb2
from ..models import phase_pb2 as models_dot_phase__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1services/progression_group_settings_service.proto\x12\x10parrygg.services\x1a\x18models/progression.proto\x1a\x12models/phase.proto"0\n"GetProgressionGroupSettingsRequest\x12\n\n\x02id\x18\x01 \x01(\t"s\n#GetProgressionGroupSettingsResponse\x12L\n\x1aprogression_group_settings\x18\x01 \x01(\x0b2(.parrygg.models.ProgressionGroupSettings2\xb0\x01\n\x1fProgressionGroupSettingsService\x12\x8c\x01\n\x1bGetProgressionGroupSettings\x124.parrygg.services.GetProgressionGroupSettingsRequest\x1a5.parrygg.services.GetProgressionGroupSettingsResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.progression_group_settings_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_GETPROGRESSIONGROUPSETTINGSREQUEST']._serialized_start = 117
    _globals['_GETPROGRESSIONGROUPSETTINGSREQUEST']._serialized_end = 165
    _globals['_GETPROGRESSIONGROUPSETTINGSRESPONSE']._serialized_start = 167
    _globals['_GETPROGRESSIONGROUPSETTINGSRESPONSE']._serialized_end = 282
    _globals['_PROGRESSIONGROUPSETTINGSSERVICE']._serialized_start = 285
    _globals['_PROGRESSIONGROUPSETTINGSSERVICE']._serialized_end = 461
