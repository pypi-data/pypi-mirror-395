import msgspec
from typing import List
from ..common.base import BaseRequest
from ..models.user import UserModel


class User(BaseRequest):
    """Getting information about particular user

    Requires user ID (same as slug)
    """

    __endpoint__ = "/userId/{slug}"
    __slug__ = True

    data: UserModel
