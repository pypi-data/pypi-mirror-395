from typing import List
from ..common.base import BaseRequest
from ..models.lich import LichWeaponModel, LichEphemeraModel, LichQuirkModel


class LichWeapons(BaseRequest):
    """Get list of all tradable lich weapons"""

    __endpoint__ = "/lich/weapons"

    data: List[LichWeaponModel]


class LichWeapon(BaseRequest):
    """Get full info about one, particular lich weapon. Requires slug"""

    __endpoint__ = "/lich/weapon/{slug}"
    __slug__ = True

    data: LichWeaponModel


class LichEphemeras(BaseRequest):
    """Get list of all tradable lich ephemeras"""

    __endpoint__ = "/lich/ephemeras"

    data: List[LichEphemeraModel]


class LichQuirks(BaseRequest):
    """Get list of all tradable lich quirks"""

    __endpoint__ = "/lich/quirks"

    data: List[LichQuirkModel]
