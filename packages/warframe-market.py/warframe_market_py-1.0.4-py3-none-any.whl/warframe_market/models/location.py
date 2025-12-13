import msgspec
from ..common.options import LanguageCode


class LocationI18NModel(msgspec.Struct):
    """Localization data for a location."""

    node_name: str = msgspec.field(name="nodeName")
    icon: str
    thumb: str
    system_name: str | None = msgspec.field(default=None, name="systemName")


class LocationModel(msgspec.Struct):
    """Model for locations."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    faction: str | None = None
    min_level: int | None = msgspec.field(default=None, name="minLevel")
    max_level: int | None = msgspec.field(default=None, name="maxLevel")
    i18n: dict[LanguageCode, LocationI18NModel] = msgspec.field(default_factory=dict)
