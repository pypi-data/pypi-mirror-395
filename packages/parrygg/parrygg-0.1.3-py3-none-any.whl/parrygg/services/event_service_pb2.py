
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/event_service.proto')
_sym_db = _symbol_database.Default()
from ..models import event_pb2 as models_dot_event__pb2
from ..models import hierarchy_pb2 as models_dot_hierarchy__pb2
from ..models import filter_pb2 as models_dot_filter__pb2
from ..models import entrant_pb2 as models_dot_entrant__pb2
from ..models import phase_pb2 as models_dot_phase__pb2
from ..models import request_pb2 as models_dot_request__pb2
from ..models import event_export_pb2 as models_dot_event__export__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cservices/event_service.proto\x12\x10parrygg.services\x1a\x12models/event.proto\x1a\x16models/hierarchy.proto\x1a\x13models/filter.proto\x1a\x14models/entrant.proto\x1a\x12models/phase.proto\x1a\x14models/request.proto\x1a\x19models/event_export.proto"\x86\x01\n\x0fGetEventRequest\x12\n\n\x02id\x18\x01 \x01(\t\x123\n\nidentifier\x18\x02 \x01(\x0b2\x1f.parrygg.models.EventIdentifier\x122\n\x07options\x18\x03 \x01(\x0b2!.parrygg.services.GetEventOptions"8\n\x10GetEventResponse\x12$\n\x05event\x18\x01 \x01(\x0b2\x15.parrygg.models.Event"B\n\x0fGetEventOptions\x12/\n\nevent_view\x18\x01 \x01(\x0e2\x1b.parrygg.services.EventView"@\n\x10GetEventsRequest\x12,\n\x06filter\x18\x01 \x01(\x0b2\x1c.parrygg.models.EventsFilter":\n\x11GetEventsResponse\x12%\n\x06events\x18\x01 \x03(\x0b2\x15.parrygg.models.Event"\x1f\n\x11ResetEventRequest\x12\n\n\x02id\x18\x01 \x01(\t"\x14\n\x12ResetEventResponse"q\n\x19GetEventPlacementsRequest\x12\x0c\n\x02id\x18\x01 \x01(\tH\x00\x128\n\x0fevent_slug_path\x18\x02 \x01(\x0b2\x1d.parrygg.models.EventSlugPathH\x00B\x0c\n\nidentifier"K\n\x1aGetEventPlacementsResponse\x12-\n\nplacements\x18\x01 \x03(\x0b2\x19.parrygg.models.Placement"\x93\x01\n\x17GetEntrantResultRequest\x129\n\x10event_identifier\x18\x01 \x01(\x0b2\x1f.parrygg.models.EventIdentifier\x12\x14\n\nentrant_id\x18\x02 \x01(\tH\x00\x12\x11\n\x07user_id\x18\x03 \x01(\tH\x00B\x14\n\x12entrant_identifier"o\n\x18GetEntrantResultResponse\x12,\n\tplacement\x18\x01 \x01(\x0b2\x19.parrygg.models.Placement\x12%\n\x06phases\x18\x02 \x03(\x0b2\x15.parrygg.models.Phase"T\n\x17GetEventEntrantsRequest\x129\n\x10event_identifier\x18\x01 \x01(\x0b2\x1f.parrygg.models.EventIdentifier"P\n\x18GetEventEntrantsResponse\x124\n\x0eevent_entrants\x18\x01 \x03(\x0b2\x1c.parrygg.models.EventEntrant*I\n\tEventView\x12\x1c\n\x18EVENT_VIEW_SETTINGS_ONLY\x10\x00\x12\x1e\n\x1aEVENT_VIEW_BRACKET_SUMMARY\x10\x012\xe3\x04\n\x0cEventService\x12S\n\x08GetEvent\x12!.parrygg.services.GetEventRequest\x1a".parrygg.services.GetEventResponse"\x00\x12V\n\tGetEvents\x12".parrygg.services.GetEventsRequest\x1a#.parrygg.services.GetEventsResponse"\x00\x12q\n\x12GetEventPlacements\x12+.parrygg.services.GetEventPlacementsRequest\x1a,.parrygg.services.GetEventPlacementsResponse"\x00\x12k\n\x10GetEventEntrants\x12).parrygg.services.GetEventEntrantsRequest\x1a*.parrygg.services.GetEventEntrantsResponse"\x00\x12Y\n\nResetEvent\x12#.parrygg.services.ResetEventRequest\x1a$.parrygg.services.ResetEventResponse"\x00\x12k\n\x10GetEntrantResult\x12).parrygg.services.GetEntrantResultRequest\x1a*.parrygg.services.GetEntrantResultResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.event_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_EVENTVIEW']._serialized_start = 1273
    _globals['_EVENTVIEW']._serialized_end = 1346
    _globals['_GETEVENTREQUEST']._serialized_start = 207
    _globals['_GETEVENTREQUEST']._serialized_end = 341
    _globals['_GETEVENTRESPONSE']._serialized_start = 343
    _globals['_GETEVENTRESPONSE']._serialized_end = 399
    _globals['_GETEVENTOPTIONS']._serialized_start = 401
    _globals['_GETEVENTOPTIONS']._serialized_end = 467
    _globals['_GETEVENTSREQUEST']._serialized_start = 469
    _globals['_GETEVENTSREQUEST']._serialized_end = 533
    _globals['_GETEVENTSRESPONSE']._serialized_start = 535
    _globals['_GETEVENTSRESPONSE']._serialized_end = 593
    _globals['_RESETEVENTREQUEST']._serialized_start = 595
    _globals['_RESETEVENTREQUEST']._serialized_end = 626
    _globals['_RESETEVENTRESPONSE']._serialized_start = 628
    _globals['_RESETEVENTRESPONSE']._serialized_end = 648
    _globals['_GETEVENTPLACEMENTSREQUEST']._serialized_start = 650
    _globals['_GETEVENTPLACEMENTSREQUEST']._serialized_end = 763
    _globals['_GETEVENTPLACEMENTSRESPONSE']._serialized_start = 765
    _globals['_GETEVENTPLACEMENTSRESPONSE']._serialized_end = 840
    _globals['_GETENTRANTRESULTREQUEST']._serialized_start = 843
    _globals['_GETENTRANTRESULTREQUEST']._serialized_end = 990
    _globals['_GETENTRANTRESULTRESPONSE']._serialized_start = 992
    _globals['_GETENTRANTRESULTRESPONSE']._serialized_end = 1103
    _globals['_GETEVENTENTRANTSREQUEST']._serialized_start = 1105
    _globals['_GETEVENTENTRANTSREQUEST']._serialized_end = 1189
    _globals['_GETEVENTENTRANTSRESPONSE']._serialized_start = 1191
    _globals['_GETEVENTENTRANTSRESPONSE']._serialized_end = 1271
    _globals['_EVENTSERVICE']._serialized_start = 1349
    _globals['_EVENTSERVICE']._serialized_end = 1960
