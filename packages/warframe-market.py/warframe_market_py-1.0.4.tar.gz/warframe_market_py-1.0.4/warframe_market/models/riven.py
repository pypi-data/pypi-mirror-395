from typing import Literal

import msgspec

from ..common.options import LanguageCode

RivenType = Literal["rifle", "shotgun", "pistol", "melee", "kitgun", "zaw"]


class RivenI18N(msgspec.Struct):
    """Localization data for a Riven mod."""

    name: str
    icon: str
    thumb: str
    wiki_link: str | None = msgspec.field(default=None, name="wikiLink")


class RivenAttributeI18N(msgspec.Struct):
    """Localization data for a Riven attribute."""

    name: str = msgspec.field(name="effect")
    icon: str
    thumb: str


class RivenModel(msgspec.Struct):
    """Model for Riven mods."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    disposition: float
    req_mastery_rank: int = msgspec.field(name="reqMasteryRank")
    group: str | None = None
    riven_type: str | None = msgspec.field(default=None, name="rivenType")
    i18n: dict[LanguageCode, RivenI18N] = msgspec.field(default_factory=dict)


class RivenAttributeModel(msgspec.Struct):
    """Model for Riven mod attributes."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    prefix: str
    suffix: str
    group: str | None = None
    i18n: dict[LanguageCode, RivenAttributeI18N] = msgspec.field(default_factory=dict)
    exclusive_to: list[str] | None = msgspec.field(default=None, name="exclusiveTo")
    positive_is_negative: bool | None = msgspec.field(
        default=None, name="positiveIsNegative"
    )
    unit: str | None = None
    positive_only: bool | None = msgspec.field(default=None, name="positiveOnly")
    negative_only: bool | None = msgspec.field(default=None, name="negativeOnly")
