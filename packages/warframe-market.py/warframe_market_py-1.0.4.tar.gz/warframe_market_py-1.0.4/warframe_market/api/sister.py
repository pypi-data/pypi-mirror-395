from typing import List
from ..common.base import BaseRequest
from ..models.sister import SisterWeaponModel, SisterEphemeraModel, SisterQuirkModel


class SisterWeapons(BaseRequest):
    """Get list of all tradable sister weapons"""

    __endpoint__ = "/sister/weapons"

    data: List[SisterWeaponModel]


class SisterWeapon(BaseRequest):
    """Get full info about one, particular sister weapon. Requires slug"""

    __endpoint__ = "/sister/weapon/{slug}"
    __slug__ = True

    data: SisterWeaponModel


class SisterEphemeras(BaseRequest):
    """Get list of all tradable sister ephemeras"""

    __endpoint__ = "/sister/ephemeras"

    data: List[SisterEphemeraModel]


class SisterQuirks(BaseRequest):
    """Get list of all tradable sister quirks"""

    __endpoint__ = "/sister/quirks"

    data: List[SisterQuirkModel]
