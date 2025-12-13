import msgspec

from ..common.options import LanguageCode


class SisterWeaponI18NModel(msgspec.Struct):
    """Localization data for a Sister weapon."""

    name: str = msgspec.field(name="itemName")
    icon: str
    thumb: str
    wiki_link: str | None = msgspec.field(default=None, name="wikiLink")


class SisterWeaponModel(msgspec.Struct):
    """Model for Sister weapons."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    req_mastery_rank: int = msgspec.field(name="reqMasteryRank")
    i18n: dict[LanguageCode, SisterWeaponI18NModel] = msgspec.field(
        default_factory=dict
    )


class SisterEphemeraI18NModel(msgspec.Struct):
    """Localization data for a Sister ephemera."""

    name: str = msgspec.field(name="itemName")
    icon: str
    thumb: str


class SisterEphemeraModel(msgspec.Struct):
    """Model for Sister ephemeras."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    animation: str
    element: str
    i18n: dict[LanguageCode, SisterEphemeraI18NModel] = msgspec.field(
        default_factory=dict
    )


class SisterQuirkI18NModel(msgspec.Struct):
    """Localization data for a Sister quirk."""

    name: str = msgspec.field(name="itemName")
    icon: str
    thumb: str
    description: str | None = None


class SisterQuirkModel(msgspec.Struct):
    """Model for Sister quirks."""

    id: str
    slug: str
    group: str | None = None
    i18n: dict[LanguageCode, SisterQuirkI18NModel] = msgspec.field(default_factory=dict)
