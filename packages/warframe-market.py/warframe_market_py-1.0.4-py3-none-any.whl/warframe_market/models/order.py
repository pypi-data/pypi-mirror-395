import msgspec
from typing import Optional

from .user import UserShortModel


class OrderModel(msgspec.Struct):
    """
    Model for trade orders.

    Attributes:
        id: Unique identifier of the order
        type: Type of order ('buy' or 'sell')
        platinum: Total platinum currency involved
        quantity: Number of items in the order
        per_trade: Optional items quantity per transaction
        rank: Optional rank/level of the item
        charges: Optional number of charges left (for requiem mods)
        subtype: Optional specific subtype/category of the item
        amber_stars: Optional count of amber stars (for sculpture orders)
        cyan_stars: Optional count of cyan stars (for sculpture orders)
        visible: Whether the order is publicly visible
        created_at: Creation timestamp of the order
        updated_at: Last modification timestamp
        item_id: Unique identifier of the involved item
        group: User-defined group for the order
    """

    id: str
    type: str
    platinum: int
    quantity: int
    visible: bool
    created_at: str = msgspec.field(name="createdAt")
    updated_at: str = msgspec.field(name="updatedAt")
    item_id: str = msgspec.field(name="itemId")
    group: Optional[str] = None
    per_trade: Optional[int] = msgspec.field(default=None, name="perTrade")
    rank: Optional[int] = None
    charges: Optional[int] = None
    subtype: Optional[str] = None
    amber_stars: Optional[int] = msgspec.field(default=None, name="amberStars")
    cyan_stars: Optional[int] = msgspec.field(default=None, name="cyanStars")

class OrderWithUserModel(OrderModel, kw_only=True):
    """
    Model for trade orders with associated user information.

    Extends the base Order model to include the user who created the order.

    Additional Attributes:
        user: Basic profile information of the order's creator
    """

    user: UserShortModel
