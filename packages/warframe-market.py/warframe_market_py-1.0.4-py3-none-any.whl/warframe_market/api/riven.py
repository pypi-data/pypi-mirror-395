import msgspec
from typing import List
from ..common.base import BaseRequest
from ..models.riven import RivenModel, RivenAttributeModel


class Rivens(BaseRequest):
    """Get list of all tradable riven items"""

    __endpoint__ = "/riven/weapons"

    data: List[RivenModel]


class Riven(BaseRequest):
    """Get full info about one, particular riven item. Requires slug"""

    __endpoint__ = "/riven/weapon/{slug}"
    __slug__ = True

    data: RivenModel


class RivenAttributes(BaseRequest):
    """Get list of all attributes for riven weapons"""

    __endpoint__ = "/riven/attributes"

    data: List[RivenAttributeModel]
