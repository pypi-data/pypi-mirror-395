import msgspec
from datetime import datetime
from typing import List
from ..common.base import BaseRequest
from ..models.location import LocationModel
from ..models.npc import NpcModel
from ..models.mission import MissionModel


class _AppsData(msgspec.Struct):
    ios: str
    android: str
    minIos: str
    minAndroid: str


class _CollectionsData(msgspec.Struct):
    items: str
    rivens: str
    liches: str
    sisters: str
    missions: str
    npcs: str
    locations: str


class _VersionData(msgspec.Struct):
    apps: _AppsData
    collections: _CollectionsData
    updatedAt: datetime


class Versions(BaseRequest):
    """Get current API version"""

    __endpoint__ = "/versions"

    data: _VersionData


class Locations(BaseRequest):
    """Get list of all tradable lich weapons"""

    __endpoint__ = "/locations"

    data: List[LocationModel]


class NPCs(BaseRequest):
    """Get list of all NPCs"""

    __endpoint__ = "/npcs"

    data: List[NpcModel]


class Missions(BaseRequest):
    """Get list of all missions"""

    __endpoint__ = "/missions"

    data: List[MissionModel]
