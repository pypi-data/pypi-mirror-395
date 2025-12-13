from pydantic import BeforeValidator
from typing import TypeAlias, Annotated, Literal, Sequence, Any, Union
from typing import cast, get_args
import datetime
import re

# Raw types
RecordingQuality: TypeAlias = Literal['A', 'B', 'C', 'D', 'E']
Sex: TypeAlias = Literal['male', 'female']
LifeStage: TypeAlias = Literal[
  'adult',
  'juvenile',
  'nestling',
  'nymph',
  'subadult',
]
Group: TypeAlias = Literal[
  'grasshoppers',
  'bats',
  'birds',
  'frogs',
  'land mammals'
]
SoundType: TypeAlias = Literal[
  'aberrant',
  'advertisement call',
  'agonistic call',
  'alarm call',
  'begging call',
  'call',
  'calling song',
  'courtship song',
  'dawn song',
  'defensive call',
  'distress call',
  'disturbance song',
  'drumming',
  'duet',
  'echolocation',
  'feeding buzz',
  'female song',
  'flight call',
  'flight song',
  'imitation',
  'mating call',
  'mechanical sound',
  'nocturnal flight call',
  'release call',
  'rivalry song',
  'searching song',
  'social call',
  'song',
  'subsong',
  'territorial call',
]
RecordingMethod: TypeAlias = Literal[
  'emerging from roost',
  'field recording',
  'fluorescent light tag',
  'hand-release',
  'in enclosure',
  'in net',
  'in the hand',
  'roosting',
  'roped',
  'studio recording',
]

def parse_xc_bool(value: Any) -> Literal['yes', 'no']:
  if value is None:
    raise ValueError()
  if isinstance(value, bool):
    return 'yes' if value is True else 'no'
  if isinstance(value, str):
        normalized_value = value.lower()
        if normalized_value in ('yes', 'no'):
            return normalized_value
  raise ValueError(value)

def parse_xc_id(value: Any) -> str:
  if isinstance(value, int):
    if value < 1:
      raise ValueError(value)
    return str(value)
  if isinstance(value, str):
    pattern = re.compile(r'^(?:XC|xc)?(\d+)$')
    res = pattern.match(value)
    if not res:
      raise ValueError(value)
    return res.group(1)
  raise ValueError(value)

XcBoolOutput = Literal['yes', 'no']

XcBoolInput = Union[XcBoolOutput, bool]

XcBool = Annotated[
  Union[XcBoolOutput, XcBoolInput], 
  BeforeValidator(parse_xc_bool)
]

XcId = Annotated[
  Union[str | int],
  BeforeValidator(parse_xc_id),
]

SampleRate = Literal[8000, 22050, 44100, 48000, 88200, 96000, 192000]

class Noneable:
  @staticmethod
  def _safe_parse_bool(value: str) -> bool | None:
    match value.strip().lower():
      case 'yes' | 'true':
        return True
      case 'no' | 'false':
        return False
    return None
  
  @staticmethod
  def _safe_parse_float(value: str) -> float | None:
    try:
      return float(value)
    except:
      return None
  
  @staticmethod
  def _safe_parse_duration(value: str) -> datetime.timedelta | None:
    try:
      parts = value.split(':')
      if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return datetime.timedelta(
          minutes=minutes,
          seconds=seconds
        )
      raise ValueError(f'Invalid duration format: {value}')
    except Exception as exc:
      raise ValueError(f'Failed to parse duration string: {value}') from exc
  
  @staticmethod
  def _safe_parse_time(value: str) -> datetime.time | None:
    try:
      parts = value.split(':')
      if len(parts) == 2:
        hour, minute = map(int, parts)
        return datetime.time(
          hour=hour,
          minute=minute
        )
      raise ValueError(f'Invalid time format: {value}')
    except Exception as exc:
      # TODO Warn?
      return None
  
  @staticmethod
  def _safe_parse_date(value: str) -> datetime.date | None:
    try:
      parts = value.split('-')
      if len(parts) == 3:
        year, month, day = map(int, parts)
        return datetime.date(
          year=year,
          month=month,
          day=day,
        )
      raise ValueError(f'Invalid date format: {value}')
    except Exception as exc:
      # TODO Warn?
      return None
  
  @staticmethod
  def _safe_parse_sound_type(value: str) -> SoundType | None:
    return cast(SoundType, value) \
      if value in get_args(SoundType) \
      else None
  
  @staticmethod
  def _safe_parse_life_stage(value: str) -> LifeStage | None:
    return cast(LifeStage, value) \
      if value in get_args(LifeStage) \
      else None
  
  @staticmethod
  def _safe_parse_group(value: str) -> Group | None:
    return cast(Group, value) \
      if value in get_args(Group) \
      else None

  @staticmethod
  def _safe_parse_sex(value: str) -> Sex | None:
    return cast(Sex, value) \
      if value in get_args(Sex) \
      else None
  
  @staticmethod
  def _safe_parse_recording_method(value: str) -> RecordingMethod | None:
    return cast(RecordingMethod, value) \
      if value in get_args(RecordingMethod) \
      else None

  @staticmethod
  def _safe_parse_nonempty_string(value: str) -> str | None:
    return value if len(value) else None

  @staticmethod
  def _safe_parse_integer(value: str) -> int | None:
    try:
      return int(value)
    except:
      return None
    
  @staticmethod
  def _safe_parse_nonempty_string_array(value: Sequence) -> Sequence[str] | None:
    return tuple(value)\
      if len(value) and all(isinstance(i, str) for i in value)\
      else None

  @staticmethod
  def _safe_parse_quality(value: str) -> RecordingQuality | None:
    return cast(RecordingQuality, value)\
      if value in get_args(RecordingQuality)\
      else None
  
  Float = Annotated[
    float | None,
    BeforeValidator(_safe_parse_float)
  ]
  
  Bool = Annotated[
    bool | None,
    BeforeValidator(_safe_parse_bool)
  ]

  Timedelta = Annotated[
    datetime.timedelta,
    BeforeValidator(_safe_parse_duration)
  ]

  Time = Annotated[
    datetime.time | None,
    BeforeValidator(_safe_parse_time)
  ]

  Date = Annotated[
    datetime.date | None,
    BeforeValidator(_safe_parse_date)
  ]

  SoundType = Annotated[
    SoundType | None,
    BeforeValidator(_safe_parse_sound_type)
  ]

  LifeStage = Annotated[
    LifeStage | None,
    BeforeValidator(_safe_parse_life_stage)
  ]

  Group = Annotated[
    Group | None,
    BeforeValidator(_safe_parse_group)
  ]

  Sex = Annotated[
    Sex | None,
    BeforeValidator(_safe_parse_sex)
  ]

  RecordingMethod = Annotated[
    RecordingMethod | None,
    BeforeValidator(_safe_parse_recording_method)
  ]

  String = Annotated[
    str | None,
    BeforeValidator(_safe_parse_nonempty_string)
  ]

  Int = Annotated[
    int | None,
    BeforeValidator(_safe_parse_integer)
  ]

  StringSequence = Annotated[
    Sequence[str] | None,
    BeforeValidator(_safe_parse_nonempty_string_array)
  ]

  Quality = Annotated[
    RecordingQuality | None,
    BeforeValidator(_safe_parse_quality)
  ]