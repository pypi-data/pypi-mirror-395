import msgspec
from ..common.options import LanguageCode


# Lich Weapon
class LichWeaponI18NModel(msgspec.Struct):
    """Localization data for a Lich weapon."""

    name: str = msgspec.field(name="itemName")  # Changed to match Go struct's json tag
    icon: str
    thumb: str
    wiki_link: str | None = msgspec.field(default=None, name="wikiLink")


class LichWeaponModel(msgspec.Struct):
    """Model for Kuva/Sister Lich weapons."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    req_mastery_rank: int = msgspec.field(name="reqMasteryRank")
    i18n: dict[LanguageCode, LichWeaponI18NModel] = msgspec.field(default_factory=dict)


# Lich Ephemera
class LichEphemeraI18NModel(msgspec.Struct):
    """Localization data for a Lich ephemera."""

    name: str = msgspec.field(name="itemName")
    icon: str
    thumb: str


class LichEphemeraModel(msgspec.Struct):
    """Model for Kuva/Sister Lich ephemeras."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    animation: str
    element: str
    i18n: dict[LanguageCode, LichEphemeraI18NModel] = msgspec.field(
        default_factory=dict
    )


# Lich Quirk
class LichQuirkI18NModel(msgspec.Struct):
    """Localization data for a Lich quirk."""

    name: str = msgspec.field(name="itemName")
    description: str | None = None
    icon: str | None = None
    thumb: str | None = None


class LichQuirkModel(msgspec.Struct):
    """Model for Kuva/Sister Lich quirks."""

    id: str
    slug: str
    group: str | None = None
    i18n: dict[LanguageCode, LichQuirkI18NModel] = msgspec.field(default_factory=dict)
