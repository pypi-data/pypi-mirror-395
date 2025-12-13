
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/event_export.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19models/event_export.proto\x12\x0eparrygg.models"\xc5\x01\n\x0bEventExport\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08event_id\x18\x02 \x01(\t\x121\n\x06status\x18\x03 \x01(\x0e2!.parrygg.models.EventExportStatus\x12\x14\n\x0cbraacket_url\x18\x04 \x01(\t\x12\x13\n\x0bretry_count\x18\x05 \x01(\x05\x12\x12\n\nlast_error\x18\x06 \x01(\t\x12\x12\n\ncreated_at\x18\x07 \x01(\t\x12\x12\n\nupdated_at\x18\x08 \x01(\t*\xbf\x01\n\x11EventExportStatus\x12#\n\x1fEVENT_EXPORT_STATUS_UNSPECIFIED\x10\x00\x12\x1f\n\x1bEVENT_EXPORT_STATUS_PENDING\x10\x01\x12#\n\x1fEVENT_EXPORT_STATUS_IN_PROGRESS\x10\x02\x12\x1f\n\x1bEVENT_EXPORT_STATUS_SUCCESS\x10\x03\x12\x1e\n\x1aEVENT_EXPORT_STATUS_FAILED\x10\x04B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.event_export_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_EVENTEXPORTSTATUS']._serialized_start = 246
    _globals['_EVENTEXPORTSTATUS']._serialized_end = 437
    _globals['_EVENTEXPORT']._serialized_start = 46
    _globals['_EVENTEXPORT']._serialized_end = 243
