
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/pagination.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17models/pagination.proto\x12\x0eparrygg.models\x1a\x1cgoogle/protobuf/struct.proto"O\n\x11PaginationRequest\x12\x11\n\tpage_size\x18\x01 \x01(\r\x12\'\n\x06cursor\x18\x02 \x01(\x0b2\x17.google.protobuf.Struct"T\n\x12PaginationResponse\x12,\n\x0bnext_cursor\x18\x01 \x01(\x0b2\x17.google.protobuf.Struct\x12\x10\n\x08has_more\x18\x02 \x01(\x08B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.pagination_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_PAGINATIONREQUEST']._serialized_start = 73
    _globals['_PAGINATIONREQUEST']._serialized_end = 152
    _globals['_PAGINATIONRESPONSE']._serialized_start = 154
    _globals['_PAGINATIONRESPONSE']._serialized_end = 238
