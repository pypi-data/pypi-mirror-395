import msgspec
from ..common.options import LanguageCode


class ItemI18NModel(msgspec.Struct):
    """Localization data for an item."""

    name: str
    icon: str
    thumb: str
    description: str | None = None
    wiki_link: str | None = msgspec.field(default=None, name="wikiLink")
    sub_icon: str | None = msgspec.field(default=None, name="subIcon")


class ItemShortModel(msgspec.Struct):
    """Short form item data model."""

    id: str
    slug: str
    game_ref: str = msgspec.field(name="gameRef")
    tags: list[str] = msgspec.field(default_factory=list)
    i18n: dict[LanguageCode, ItemI18NModel] = msgspec.field(default_factory=dict)
    max_rank: int | None = msgspec.field(default=None, name="maxRank")
    max_charges: int | None = msgspec.field(default=None, name="maxCharges")
    vaulted: bool | None = None
    ducats: int | None = None
    amber_stars: int | None = msgspec.field(default=None, name="amberStars")
    cyan_stars: int | None = msgspec.field(default=None, name="cyanStars")
    base_endo: int | None = msgspec.field(default=None, name="baseEndo")
    endo_multiplier: float | None = msgspec.field(default=None, name="endoMultiplier")
    subtypes: list[str] = msgspec.field(default_factory=list)


class ItemModel(ItemShortModel):
    """Full item data model that extends ItemShortModel."""

    tradable: bool | None = None
    set_root: bool | None = msgspec.field(default=None, name="setRoot")
    set_parts: list[str] | None = msgspec.field(default=None, name="setParts")
    quantity_in_set: int | None = msgspec.field(default=None, name="quantityInSet")
    rarity: str | None = None
    bulk_tradable: bool | None = msgspec.field(default=None, name="bulkTradable")
    max_amber_stars: int | None = msgspec.field(default=None, name="maxAmberStars")
    max_cyan_stars: int | None = msgspec.field(default=None, name="maxCyanStars")
    req_mastery_rank: int | None = msgspec.field(default=None, name="reqMasteryRank")
    trading_tax: int | None = msgspec.field(default=None, name="tradingTax")
    vosfor: int | None = None
