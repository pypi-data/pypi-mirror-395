from typing import Optional
import msgspec
from enum import Enum


class ActivityType(str, Enum):
    """Types of activities a user can be engaged in."""

    ON_MISSION = "ON_MISSION"
    DOJO = "DOJO"
    UNKNOWN = "UNKNOWN"
    EMPTY = ""


class ActivityModel(msgspec.Struct):
    """
    Model for user activity information.

    Attributes:
        type: Name of the activity (e.g., 'on mission', 'dojo')
        details: Optional specifics about the activity
        started_at: Timestamp of when the activity started
    """
    type: Optional[ActivityType] = msgspec.field(default=ActivityType.UNKNOWN, name="type")
    details: Optional[str] = None
    started_at: Optional[str] = msgspec.field(default=None, name="startedAt")
