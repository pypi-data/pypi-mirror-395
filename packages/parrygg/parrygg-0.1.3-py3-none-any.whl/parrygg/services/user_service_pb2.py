
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'services/user_service.proto')
_sym_db = _symbol_database.Default()
from ..models import user_pb2 as models_dot_user__pb2
from ..models import event_pb2 as models_dot_event__pb2
from ..models import image_pb2 as models_dot_image__pb2
from ..models import filter_pb2 as models_dot_filter__pb2
from ..models import pagination_pb2 as models_dot_pagination__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bservices/user_service.proto\x12\x10parrygg.services\x1a\x11models/user.proto\x1a\x12models/event.proto\x1a\x12models/image.proto\x1a\x13models/filter.proto\x1a\x17models/pagination.proto",\n\x0eGetUserRequest\x12\x0c\n\x02id\x18\x01 \x01(\tH\x00B\x0c\n\nidentifier"5\n\x0fGetUserResponse\x12"\n\x04user\x18\x01 \x01(\x0b2\x14.parrygg.models.User">\n\x0fGetUsersRequest\x12+\n\x06filter\x18\x01 \x01(\x0b2\x1b.parrygg.models.UsersFilter"7\n\x10GetUsersResponse\x12#\n\x05users\x18\x01 \x03(\x0b2\x14.parrygg.models.User"J\n\x11UpdateUserRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12)\n\x04user\x18\x02 \x01(\x0b2\x1b.parrygg.models.MutableUser"8\n\x12UpdateUserResponse\x12"\n\x04user\x18\x01 \x01(\x0b2\x14.parrygg.models.User"e\n\x18GetUserPlacementsRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12=\n\x12pagination_request\x18\x02 \x01(\x0b2!.parrygg.models.PaginationRequest"\x8c\x01\n\x19GetUserPlacementsResponse\x12.\n\x07results\x18\x01 \x03(\x0b2\x1d.parrygg.models.EntrantResult\x12?\n\x13pagination_response\x18\x02 \x01(\x0b2".parrygg.models.PaginationResponse2\xff\x02\n\x0bUserService\x12P\n\x07GetUser\x12 .parrygg.services.GetUserRequest\x1a!.parrygg.services.GetUserResponse"\x00\x12S\n\x08GetUsers\x12!.parrygg.services.GetUsersRequest\x1a".parrygg.services.GetUsersResponse"\x00\x12Y\n\nUpdateUser\x12#.parrygg.services.UpdateUserRequest\x1a$.parrygg.services.UpdateUserResponse"\x00\x12n\n\x11GetUserPlacements\x12*.parrygg.services.GetUserPlacementsRequest\x1a+.parrygg.services.GetUserPlacementsResponse"\x00B\x1a\n\x16gg.parry.grpc.servicesP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.user_service_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16gg.parry.grpc.servicesP\x01'
    _globals['_GETUSERREQUEST']._serialized_start = 154
    _globals['_GETUSERREQUEST']._serialized_end = 198
    _globals['_GETUSERRESPONSE']._serialized_start = 200
    _globals['_GETUSERRESPONSE']._serialized_end = 253
    _globals['_GETUSERSREQUEST']._serialized_start = 255
    _globals['_GETUSERSREQUEST']._serialized_end = 317
    _globals['_GETUSERSRESPONSE']._serialized_start = 319
    _globals['_GETUSERSRESPONSE']._serialized_end = 374
    _globals['_UPDATEUSERREQUEST']._serialized_start = 376
    _globals['_UPDATEUSERREQUEST']._serialized_end = 450
    _globals['_UPDATEUSERRESPONSE']._serialized_start = 452
    _globals['_UPDATEUSERRESPONSE']._serialized_end = 508
    _globals['_GETUSERPLACEMENTSREQUEST']._serialized_start = 510
    _globals['_GETUSERPLACEMENTSREQUEST']._serialized_end = 611
    _globals['_GETUSERPLACEMENTSRESPONSE']._serialized_start = 614
    _globals['_GETUSERPLACEMENTSRESPONSE']._serialized_end = 754
    _globals['_USERSERVICE']._serialized_start = 757
    _globals['_USERSERVICE']._serialized_end = 1140
