
BASE_URL = "https://api.warframe.market/v2"
BASE_STATIC_ASSETS_URL = "https://warframe.market/static/assets"

from .enums import (
    Language,
    Platform,
    Subtype,
)

from .base import (
    Base,
    BaseRequest,
)

from .options import (
    LanguageCode,
)