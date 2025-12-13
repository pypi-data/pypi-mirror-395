import msgspec
from ..common.options import LanguageCode


class AchievementI18NModel(msgspec.Struct):
    """
    Localized information for an achievement.

    Attributes:
        name: Localized name of the achievement
        description: Localized description of the achievement
    """

    name: str
    description: str


class AchievementModel(msgspec.Struct):
    """
    Model for site achievements.

    Attributes:
        id: Unique identifier for the achievement
        icon: URL to the achievement's icon
        thumb: URL to the achievement's thumbnail image
        type: Type or category of the achievement
        i18n: Localized text in various languages
    """

    id: str
    icon: str
    thumb: str
    type: str
    i18n: dict[LanguageCode, AchievementI18NModel]
