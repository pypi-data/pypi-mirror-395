
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/hierarchy_service.proto')
_sym_db = _symbol_database.Default()
from ..models import event_pb2 as models_dot_event__pb2
from ..models import hierarchy_pb2 as models_dot_hierarchy__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n services/hierarchy_service.proto\x12\x10parrygg.services\x1a\x12models/event.proto\x1a\x16models/hierarchy.proto"v\n\x18GetEventHierarchyRequest\x12\x12\n\x08event_id\x18\x01 \x01(\tH\x00\x128\n\x0fevent_slug_path\x18\x02 \x01(\x0b2\x1d.parrygg.models.EventSlugPathH\x00B\x0c\n\nidentifier"I\n\x19GetEventHierarchyResponse\x12,\n\thierarchy\x18\x01 \x01(\x0b2\x19.parrygg.models.Hierarchy"v\n\x18GetPhaseHierarchyRequest\x12\x12\n\x08phase_id\x18\x01 \x01(\tH\x00\x128\n\x0fphase_slug_path\x18\x02 \x01(\x0b2\x1d.parrygg.models.PhaseSlugPathH\x00B\x0c\n\nidentifier"I\n\x19GetPhaseHierarchyResponse\x12,\n\thierarchy\x18\x01 \x01(\x0b2\x19.parrygg.models.Hierarchy"~\n\x1aGetBracketHierarchyRequest\x12\x14\n\nbracket_id\x18\x01 \x01(\tH\x00\x12<\n\x11bracket_slug_path\x18\x02 \x01(\x0b2\x1f.parrygg.models.BracketSlugPathH\x00B\x0c\n\nidentifier"K\n\x1bGetBracketHierarchyResponse\x12,\n\thierarchy\x18\x01 \x01(\x0b2\x19.parrygg.models.Hierarchy"l\n\x1fGetAllBracketHierarchiesRequest\x12;\n\x10event_identifier\x18\x01 \x01(\x0b2\x1f.parrygg.models.EventIdentifierH\x00B\x0c\n\nidentifier"R\n GetAllBracketHierarchiesResponse\x12.\n\x0bhierarchies\x18\x01 \x03(\x0b2\x19.parrygg.models.Hierarchy2\xee\x03\n\x10HierarchyService\x12n\n\x11GetEventHierarchy\x12*.parrygg.services.GetEventHierarchyRequest\x1a+.parrygg.services.GetEventHierarchyResponse"\x00\x12n\n\x11GetPhaseHierarchy\x12*.parrygg.services.GetPhaseHierarchyRequest\x1a+.parrygg.services.GetPhaseHierarchyResponse"\x00\x12t\n\x13GetBracketHierarchy\x12,.parrygg.services.GetBracketHierarchyRequest\x1a-.parrygg.services.GetBracketHierarchyResponse"\x00\x12\x83\x01\n\x18GetAllBracketHierarchies\x121.parrygg.services.GetAllBracketHierarchiesRequest\x1a2.parrygg.services.GetAllBracketHierarchiesResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.hierarchy_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_GETEVENTHIERARCHYREQUEST']._serialized_start = 98
    _globals['_GETEVENTHIERARCHYREQUEST']._serialized_end = 216
    _globals['_GETEVENTHIERARCHYRESPONSE']._serialized_start = 218
    _globals['_GETEVENTHIERARCHYRESPONSE']._serialized_end = 291
    _globals['_GETPHASEHIERARCHYREQUEST']._serialized_start = 293
    _globals['_GETPHASEHIERARCHYREQUEST']._serialized_end = 411
    _globals['_GETPHASEHIERARCHYRESPONSE']._serialized_start = 413
    _globals['_GETPHASEHIERARCHYRESPONSE']._serialized_end = 486
    _globals['_GETBRACKETHIERARCHYREQUEST']._serialized_start = 488
    _globals['_GETBRACKETHIERARCHYREQUEST']._serialized_end = 614
    _globals['_GETBRACKETHIERARCHYRESPONSE']._serialized_start = 616
    _globals['_GETBRACKETHIERARCHYRESPONSE']._serialized_end = 691
    _globals['_GETALLBRACKETHIERARCHIESREQUEST']._serialized_start = 693
    _globals['_GETALLBRACKETHIERARCHIESREQUEST']._serialized_end = 801
    _globals['_GETALLBRACKETHIERARCHIESRESPONSE']._serialized_start = 803
    _globals['_GETALLBRACKETHIERARCHIESRESPONSE']._serialized_end = 885
    _globals['_HIERARCHYSERVICE']._serialized_start = 888
    _globals['_HIERARCHYSERVICE']._serialized_end = 1382
