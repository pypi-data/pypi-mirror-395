
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'models/bracket.proto')
_sym_db = _symbol_database.Default()
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from ..models import entrant_pb2 as models_dot_entrant__pb2
from ..models import progression_pb2 as models_dot_progression__pb2
from ..models import hierarchy_pb2 as models_dot_hierarchy__pb2
from ..models import game_pb2 as models_dot_game__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14models/bracket.proto\x12\x0eparrygg.models\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x14models/entrant.proto\x1a\x18models/progression.proto\x1a\x16models/hierarchy.proto\x1a\x11models/game.proto"\x8a\x03\n\x07Bracket\x12\n\n\x02id\x18\x01 \x01(\t\x12+\n\x05state\x18\x02 \x01(\x0e2\x1c.parrygg.models.BracketState\x12&\n\x07matches\x18\x03 \x03(\x0b2\x15.parrygg.models.Match\x121\n\x0cprogressions\x18\x04 \x03(\x0b2\x1b.parrygg.models.Progression\x12\r\n\x05index\x18\x05 \x01(\x05\x12#\n\x05seeds\x18\x06 \x03(\x0b2\x14.parrygg.models.Seed\x12.\n\nupdated_at\x18\x07 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x0c\n\x04slug\x18\t \x01(\t\x12\x10\n\x08checksum\x18\n \x01(\t\x12)\n\x04type\x18\x0b \x01(\x0e2\x1b.parrygg.models.BracketType\x12.\n\x10progressed_seeds\x18\x0c \x03(\x0b2\x14.parrygg.models.Seed"\xe2\x03\n\x05Match\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nidentifier\x18\x02 \x01(\t\x12\r\n\x05round\x18\x05 \x01(\x05\x12\x14\n\x0cwinners_side\x18\x06 \x01(\x08\x12\x14\n\x0cgrand_finals\x18\x07 \x01(\x08\x12\x1c\n\x0fprev_match_id_1\x18\x08 \x01(\tH\x00\x88\x01\x01\x12\x1c\n\x0fprev_match_id_2\x18\t \x01(\tH\x01\x88\x01\x01\x12\x1d\n\x10winners_match_id\x18\n \x01(\tH\x02\x88\x01\x01\x12\x1c\n\x0flosers_match_id\x18\x0b \x01(\tH\x03\x88\x01\x01\x12)\n\x05state\x18\x0c \x01(\x0e2\x1a.parrygg.models.MatchState\x12#\n\x05slots\x18\r \x03(\x0b2\x14.parrygg.models.Slot\x124\n\x10state_updated_at\x18\x0e \x01(\x0b2\x1a.google.protobuf.Timestamp\x12.\n\x0bmatch_games\x18\x0f \x03(\x0b2\x19.parrygg.models.MatchGameB\x12\n\x10_prev_match_id_1B\x12\n\x10_prev_match_id_2B\x13\n\x11_winners_match_idB\x12\n\x10_losers_match_id"{\n\tMatchGame\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\x05\x12%\n\x06stages\x18\x03 \x03(\x0b2\x15.parrygg.models.Stage\x12,\n\x05slots\x18\x04 \x03(\x0b2\x1d.parrygg.models.MatchGameSlot"\xad\x01\n\rMatchGameSlot\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04slot\x18\x02 \x01(\x05\x12\r\n\x05score\x18\x03 \x01(\x01\x12-\n\x05state\x18\x04 \x01(\x0e2\x19.parrygg.models.SlotStateH\x00\x88\x01\x01\x12:\n\x0cparticipants\x18\x05 \x03(\x0b2$.parrygg.models.MatchGameParticipantB\x08\n\x06_state"b\n\x14MatchGameParticipant\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12-\n\ncharacters\x18\x03 \x03(\x0b2\x19.parrygg.models.Character"E\n\x0bMatchResult\x126\n\x05slots\x18\x01 \x03(\x0b2\'.parrygg.models.MatchResultSlotMutation"~\n\x17MatchResultSlotMutation\x12\x0c\n\x04slot\x18\x01 \x01(\x05\x12\x12\n\x05score\x18\x02 \x01(\x01H\x00\x88\x01\x01\x12-\n\x05state\x18\x03 \x01(\x0e2\x19.parrygg.models.SlotStateH\x01\x88\x01\x01B\x08\n\x06_scoreB\x08\n\x06_state"q\n\x04Slot\x12\x0c\n\x04slot\x18\x01 \x01(\x05\x12\x0f\n\x07seed_id\x18\x02 \x01(\t\x12\x11\n\tplacement\x18\x03 \x01(\x05\x12\r\n\x05score\x18\x04 \x01(\x01\x12(\n\x05state\x18\x05 \x01(\x0e2\x19.parrygg.models.SlotState"\x9e\x01\n\x04Seed\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04seed\x18\x02 \x01(\x05\x123\n\revent_entrant\x18\x03 \x01(\x0b2\x1c.parrygg.models.EventEntrant\x12\x15\n\rbracket_index\x18\x04 \x01(\x05\x120\n\x0bprogression\x18\x05 \x01(\x0b2\x1b.parrygg.models.Progression"V\n\x0cSeedMutation\x12\x11\n\x04seed\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x19\n\x0cbracket_only\x18\x03 \x01(\x08H\x01\x88\x01\x01B\x07\n\x05_seedB\x0f\n\r_bracket_only"\x83\x01\n\x11MatchGameMutation\x12\r\n\x05index\x18\x01 \x01(\x05\x12.\n\x06stages\x18\x02 \x03(\x0b2\x1e.parrygg.models.StageSelection\x12/\n\x05slots\x18\x03 \x03(\x0b2 .parrygg.models.GameSlotMutation"_\n\x0eStageSelection\x12\x12\n\nstage_slug\x18\x01 \x01(\t\x12-\n\x07variant\x18\x02 \x01(\x0b2\x17.google.protobuf.StructH\x00\x88\x01\x01B\n\n\x08_variant"\xb6\x01\n\x10GameSlotMutation\x12\x0c\n\x04slot\x18\x01 \x01(\x05\x12\x12\n\x05score\x18\x02 \x01(\x01H\x00\x88\x01\x01\x12-\n\x05state\x18\x03 \x01(\x0e2\x19.parrygg.models.SlotStateH\x01\x88\x01\x01\x12=\n\x0cparticipants\x18\x04 \x03(\x0b2\'.parrygg.models.GameParticipantMutationB\x08\n\x06_scoreB\x08\n\x06_state"b\n\x17GameParticipantMutation\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x126\n\ncharacters\x18\x02 \x03(\x0b2".parrygg.models.CharacterSelection"g\n\x12CharacterSelection\x12\x16\n\x0echaracter_slug\x18\x01 \x01(\t\x12-\n\x07variant\x18\x02 \x01(\x0b2\x17.google.protobuf.StructH\x00\x88\x01\x01B\n\n\x08_variant"f\n\rBracketSlugId\x12\x17\n\x0ftournament_slug\x18\x01 \x01(\t\x12\x12\n\nevent_slug\x18\x02 \x01(\t\x12\x12\n\nphase_slug\x18\x03 \x01(\t\x12\x14\n\x0cbracket_slug\x18\x04 \x01(\t"\xfb\x01\n\x0cMatchContext\x12$\n\x05match\x18\x01 \x01(\x0b2\x15.parrygg.models.Match\x12,\n\thierarchy\x18\x02 \x01(\x0b2\x19.parrygg.models.Hierarchy\x124\n\x10event_start_date\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x18\n\x10bracket_progress\x18\x04 \x01(\x02\x12#\n\x05seeds\x18\x05 \x03(\x0b2\x14.parrygg.models.Seed\x12"\n\x04game\x18\x06 \x01(\x0b2\x14.parrygg.models.Game*\x93\x01\n\x0bBracketType\x12\x1c\n\x18BRACKET_TYPE_UNSPECIFIED\x10\x00\x12#\n\x1fBRACKET_TYPE_SINGLE_ELIMINATION\x10\x01\x12#\n\x1fBRACKET_TYPE_DOUBLE_ELIMINATION\x10\x02\x12\x1c\n\x18BRACKET_TYPE_ROUND_ROBIN\x10\x03*\x9d\x01\n\x0cBracketState\x12\x1d\n\x19BRACKET_STATE_UNSPECIFIED\x10\x00\x12\x19\n\x15BRACKET_STATE_PENDING\x10\x01\x12\x17\n\x13BRACKET_STATE_READY\x10\x02\x12\x1d\n\x19BRACKET_STATE_IN_PROGRESS\x10\x03\x12\x1b\n\x17BRACKET_STATE_COMPLETED\x10\x04*\x91\x01\n\nMatchState\x12\x1b\n\x17MATCH_STATE_UNSPECIFIED\x10\x00\x12\x17\n\x13MATCH_STATE_PENDING\x10\x01\x12\x15\n\x11MATCH_STATE_READY\x10\x02\x12\x1b\n\x17MATCH_STATE_IN_PROGRESS\x10\x03\x12\x19\n\x15MATCH_STATE_COMPLETED\x10\x04*~\n\tSlotState\x12\x1a\n\x16SLOT_STATE_UNSPECIFIED\x10\x00\x12\x16\n\x12SLOT_STATE_PENDING\x10\x01\x12\x16\n\x12SLOT_STATE_NUMERIC\x10\x02\x12\x11\n\rSLOT_STATE_DQ\x10\x03\x12\x12\n\x0eSLOT_STATE_BYE\x10\x04B\x18\n\x14gg.parry.grpc.modelsP\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'models.bracket_pb2', _globals)
if (not _descriptor._USE_C_DESCRIPTORS):
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x14gg.parry.grpc.modelsP\x01'
    _globals['_BRACKETTYPE']._serialized_start = 3020
    _globals['_BRACKETTYPE']._serialized_end = 3167
    _globals['_BRACKETSTATE']._serialized_start = 3170
    _globals['_BRACKETSTATE']._serialized_end = 3327
    _globals['_MATCHSTATE']._serialized_start = 3330
    _globals['_MATCHSTATE']._serialized_end = 3475
    _globals['_SLOTSTATE']._serialized_start = 3477
    _globals['_SLOTSTATE']._serialized_end = 3603
    _globals['_BRACKET']._serialized_start = 195
    _globals['_BRACKET']._serialized_end = 589
    _globals['_MATCH']._serialized_start = 592
    _globals['_MATCH']._serialized_end = 1074
    _globals['_MATCHGAME']._serialized_start = 1076
    _globals['_MATCHGAME']._serialized_end = 1199
    _globals['_MATCHGAMESLOT']._serialized_start = 1202
    _globals['_MATCHGAMESLOT']._serialized_end = 1375
    _globals['_MATCHGAMEPARTICIPANT']._serialized_start = 1377
    _globals['_MATCHGAMEPARTICIPANT']._serialized_end = 1475
    _globals['_MATCHRESULT']._serialized_start = 1477
    _globals['_MATCHRESULT']._serialized_end = 1546
    _globals['_MATCHRESULTSLOTMUTATION']._serialized_start = 1548
    _globals['_MATCHRESULTSLOTMUTATION']._serialized_end = 1674
    _globals['_SLOT']._serialized_start = 1676
    _globals['_SLOT']._serialized_end = 1789
    _globals['_SEED']._serialized_start = 1792
    _globals['_SEED']._serialized_end = 1950
    _globals['_SEEDMUTATION']._serialized_start = 1952
    _globals['_SEEDMUTATION']._serialized_end = 2038
    _globals['_MATCHGAMEMUTATION']._serialized_start = 2041
    _globals['_MATCHGAMEMUTATION']._serialized_end = 2172
    _globals['_STAGESELECTION']._serialized_start = 2174
    _globals['_STAGESELECTION']._serialized_end = 2269
    _globals['_GAMESLOTMUTATION']._serialized_start = 2272
    _globals['_GAMESLOTMUTATION']._serialized_end = 2454
    _globals['_GAMEPARTICIPANTMUTATION']._serialized_start = 2456
    _globals['_GAMEPARTICIPANTMUTATION']._serialized_end = 2554
    _globals['_CHARACTERSELECTION']._serialized_start = 2556
    _globals['_CHARACTERSELECTION']._serialized_end = 2659
    _globals['_BRACKETSLUGID']._serialized_start = 2661
    _globals['_BRACKETSLUGID']._serialized_end = 2763
    _globals['_MATCHCONTEXT']._serialized_start = 2766
    _globals['_MATCHCONTEXT']._serialized_end = 3017
