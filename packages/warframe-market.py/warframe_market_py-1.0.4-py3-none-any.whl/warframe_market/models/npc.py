import msgspec
from ..common.options import LanguageCode


class NpcI18NModel(msgspec.Struct):
    """Localization data for an NPC."""

    name: str
    icon: str
    thumb: str


class NpcModel(msgspec.Struct):
    """Model for NPCs."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    i18n: dict[LanguageCode, NpcI18NModel] = msgspec.field(default_factory=dict)
