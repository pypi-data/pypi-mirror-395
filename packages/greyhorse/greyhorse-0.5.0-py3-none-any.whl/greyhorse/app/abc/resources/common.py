import enum
from dataclasses import dataclass, field
from datetime import datetime

from greyhorse.enum import Enum, Struct, Unit


class ResourceEventKind(enum.IntFlag):
    SETUP = enum.auto()
    TEARDOWN = enum.auto()
    ALL = SETUP | TEARDOWN


@dataclass(slots=True, frozen=True, kw_only=True)
class Condition:
    name: str
    status: bool = False
    message: str | None = None
    permanent: bool = False
    transition_dt: datetime | None = None
    last_probe_dt: datetime = field(default_factory=datetime.now)
    # metadata: Mapping[str, Any] = field(default_factory=dict)


class TransitionStatus(Enum):
    Pending = Unit()
    Partial = Struct(total=int, completed=int)
    Complete = Unit()
    Failure = Struct(reasons=list[str], message=str)


class ResourceStatus(Enum):
    Idle = Unit()
    Initialization = Unit()
    Finalization = Unit()
    Initialized = Unit()
    Finalized = Unit()
    Failed = Struct(message=str)
    Available = Struct(alive=bool, in_use=bool)
    Acquired = Struct(alive=bool)
