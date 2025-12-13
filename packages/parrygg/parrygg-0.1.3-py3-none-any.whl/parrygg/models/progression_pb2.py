
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/progression.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18models/progression.proto\x12\x0eparrygg.models"\xe6\x01\n\x0bProgression\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08match_id\x18\x02 \x01(\t\x12\x17\n\x0ftarget_phase_id\x18\x03 \x01(\t\x12\x0f\n\x07seed_id\x18\x04 \x01(\t\x12\x18\n\x10origin_placement\x18\x05 \x01(\x05\x12\x13\n\x0borigin_seed\x18\x06 \x01(\x05\x12\x14\n\x0cmatch_winner\x18\x07 \x01(\x08\x12\x14\n\x0cwinners_side\x18\x08 \x01(\x08\x12\x19\n\x11origin_bracket_id\x18\t \x01(\t\x12\x19\n\x11target_bracket_id\x18\n \x01(\t"\xa6\x01\n\x18ProgressionGroupSettings\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\rmin_placement\x18\x02 \x01(\x05\x12\x17\n\x0fnum_progressing\x18\x03 \x01(\x05\x12\x17\n\x0ftarget_phase_id\x18\x04 \x01(\t\x125\n\x08behavior\x18\x05 \x01(\x0e2#.parrygg.models.ProgressionBehavior"\xfd\x01\n ProgressionGroupSettingsMutation\x12\x1a\n\rmin_placement\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x1c\n\x0fnum_progressing\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x1c\n\x0ftarget_phase_id\x18\x03 \x01(\tH\x02\x88\x01\x01\x12:\n\x08behavior\x18\x04 \x01(\x0e2#.parrygg.models.ProgressionBehaviorH\x03\x88\x01\x01B\x10\n\x0e_min_placementB\x12\n\x10_num_progressingB\x12\n\x10_target_phase_idB\x0b\n\t_behavior*\xac\x01\n\x13ProgressionBehavior\x12$\n PROGRESSION_BEHAVIOR_UNSPECIFIED\x10\x00\x12 \n\x1cPROGRESSION_BEHAVIOR_NATURAL\x10\x01\x12&\n"PROGRESSION_BEHAVIOR_FORCE_WINNERS\x10\x02\x12%\n!PROGRESSION_BEHAVIOR_FORCE_LOSERS\x10\x03B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.progression_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_PROGRESSIONBEHAVIOR']._serialized_start = 703
    _globals['_PROGRESSIONBEHAVIOR']._serialized_end = 875
    _globals['_PROGRESSION']._serialized_start = 45
    _globals['_PROGRESSION']._serialized_end = 275
    _globals['_PROGRESSIONGROUPSETTINGS']._serialized_start = 278
    _globals['_PROGRESSIONGROUPSETTINGS']._serialized_end = 444
    _globals['_PROGRESSIONGROUPSETTINGSMUTATION']._serialized_start = 447
    _globals['_PROGRESSIONGROUPSETTINGSMUTATION']._serialized_end = 700
