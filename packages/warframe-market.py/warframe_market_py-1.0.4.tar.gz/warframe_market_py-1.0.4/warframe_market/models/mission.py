import msgspec
from ..common.options import LanguageCode


class MissionI18NModel(msgspec.Struct):
    """Localization data for a mission."""

    name: str
    icon: str | None = None
    thumb: str | None = None


class MissionModel(msgspec.Struct):
    """Model for missions."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    i18n: dict[LanguageCode, MissionI18NModel] = msgspec.field(default_factory=dict)
