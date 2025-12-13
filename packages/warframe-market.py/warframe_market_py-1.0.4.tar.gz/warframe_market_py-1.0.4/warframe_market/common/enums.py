from enum import Enum


class Language(Enum):
    """Supported languages"""
    KOREAN = "ko"
    RUSSIAN = "ru"
    GERMAN = "de"
    FRENCH = "fr"
    PORTUGUESE = "pt"
    CHINESE_SIMPLIFIED = "zh-hans"
    CHINESE_TRADITIONAL = "zh-hant"
    SPANISH = "es"
    ITALIAN = "it"
    POLISH = "pl"
    UKRAINIAN = "uk"
    ENGLISH = "en"


class Platform(Enum):
    """Supported platforms"""
    PC = "pc"
    PS4 = "ps4"
    XBOX = "xbox"
    SWITCH = "switch"
    MOBILE = "mobile"


class Subtype(Enum):
    """Item subtypes"""
    BLUEPRINT = "blueprint"
    CRAFTED = "crafted"
