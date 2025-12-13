
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/group.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12models/group.proto\x12\x0eparrygg.models"\x07\n\x05Group*m\n\nPermission\x12\x1a\n\x16PERMISSION_UNSPECIFIED\x10\x00\x12\x15\n\x11PERMISSION_MEMBER\x10\x01\x12\x16\n\x12PERMISSION_MANAGER\x10\x02\x12\x14\n\x10PERMISSION_OWNER\x10\x03*V\n\nMemberType\x12\x1b\n\x17MEMBER_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10MEMBER_TYPE_USER\x10\x01\x12\x15\n\x11MEMBER_TYPE_GROUP\x10\x02B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.group_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_PERMISSION']._serialized_start = 47
    _globals['_PERMISSION']._serialized_end = 156
    _globals['_MEMBERTYPE']._serialized_start = 158
    _globals['_MEMBERTYPE']._serialized_end = 244
    _globals['_GROUP']._serialized_start = 38
    _globals['_GROUP']._serialized_end = 45
