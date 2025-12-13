
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/game.proto')
_sym_db = _symbol_database.Default()
from ..models import image_pb2 as models_dot_image__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11models/game.proto\x12\x0eparrygg.models\x1a\x12models/image.proto\x1a\x1cgoogle/protobuf/struct.proto"\xc0\x01\n\x04Game\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12%\n\x06images\x18\x04 \x03(\x0b2\x15.parrygg.models.Image\x12\x0c\n\x04slug\x18\x05 \x01(\t\x12-\n\ncharacters\x18\x06 \x03(\x0b2\x19.parrygg.models.Character\x12%\n\x06stages\x18\x07 \x03(\x0b2\x15.parrygg.models.Stage"\x1c\n\x0cGameMutation\x12\x0c\n\x04name\x18\x01 \x01(\t"y\n\x0eCharacterImage\x12\x0b\n\x03url\x18\x01 \x01(\t\x120\n\x04type\x18\x02 \x01(\x0e2".parrygg.models.CharacterImageType\x12(\n\x07variant\x18\x03 \x01(\x0b2\x17.google.protobuf.Struct"t\n\tCharacter\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07game_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04slug\x18\x04 \x01(\t\x12.\n\x06images\x18\x05 \x03(\x0b2\x1e.parrygg.models.CharacterImage"q\n\nStageImage\x12\x0b\n\x03url\x18\x01 \x01(\t\x12,\n\x04type\x18\x02 \x01(\x0e2\x1e.parrygg.models.StageImageType\x12(\n\x07variant\x18\x03 \x01(\x0b2\x17.google.protobuf.Struct"l\n\x05Stage\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07game_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04slug\x18\x04 \x01(\t\x12*\n\x06images\x18\x05 \x03(\x0b2\x1a.parrygg.models.StageImage*\x82\x01\n\x12CharacterImageType\x12$\n CHARACTER_IMAGE_TYPE_UNSPECIFIED\x10\x00\x12#\n\x1fCHARACTER_IMAGE_TYPE_STOCK_ICON\x10\x01\x12!\n\x1dCHARACTER_IMAGE_TYPE_PORTRAIT\x10\x02*R\n\x0eStageImageType\x12 \n\x1cSTAGE_IMAGE_TYPE_UNSPECIFIED\x10\x00\x12\x1e\n\x1aSTAGE_IMAGE_TYPE_THUMBNAIL\x10\x01B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.game_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_CHARACTERIMAGETYPE']._serialized_start = 779
    _globals['_CHARACTERIMAGETYPE']._serialized_end = 909
    _globals['_STAGEIMAGETYPE']._serialized_start = 911
    _globals['_STAGEIMAGETYPE']._serialized_end = 993
    _globals['_GAME']._serialized_start = 88
    _globals['_GAME']._serialized_end = 280
    _globals['_GAMEMUTATION']._serialized_start = 282
    _globals['_GAMEMUTATION']._serialized_end = 310
    _globals['_CHARACTERIMAGE']._serialized_start = 312
    _globals['_CHARACTERIMAGE']._serialized_end = 433
    _globals['_CHARACTER']._serialized_start = 435
    _globals['_CHARACTER']._serialized_end = 551
    _globals['_STAGEIMAGE']._serialized_start = 553
    _globals['_STAGEIMAGE']._serialized_end = 666
    _globals['_STAGE']._serialized_start = 668
    _globals['_STAGE']._serialized_end = 776
