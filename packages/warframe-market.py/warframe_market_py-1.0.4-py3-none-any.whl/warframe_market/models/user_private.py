import msgspec
from enum import Enum
from typing import List, Optional

from .activity import ActivityModel
from .achievement import AchievementModel


class Role(str, Enum):
    """User roles in the system."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class Tier(str, Enum):
    """Subscription tiers."""

    NONE = "none"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    DIAMOND = "diamond"


class LinkedAccounts(msgspec.Struct):
    """Model for linked external accounts."""

    pass


class UserPrivateModel(msgspec.Struct):
    """
    Private user profile with full details and sensitive information.

    Attributes:
        id: Unique identifier of the user
        role: User's role in the system (e.g., user, moderator, admin)
        ingame_name: In-game name of the user
        reputation: Reputation score
        locale: Preferred communication language (e.g., 'en', 'ko', 'es')
        platform: Gaming platform used by the user
        crossplay: Whether the user has crossplay enabled
        status: Current status of the user
        activity: Current activity of the user
        last_seen: Timestamp of the user's last online presence
        mastery_rank: In-game mastery rank
        credits: User's credit balance
        theme: User's selected theme
        verification: Whether the user is verified
        check_code: Verification check code
        tier: Subscription tier of the user
        subscription: Whether the user has an active subscription
        linked_accounts: Linked external accounts information
        has_email: Whether the user has an email address associated with their account
        created_at: Account creation timestamp
        reviews_left: Number of reviews left by the user
        unread_messages: Count of unread messages in the user's inbox
        avatar: Optional avatar image URL
        achievement_showcase: List of achievements showcased by the user
        ignore_list: List of user IDs that this user has ignored
        about: Optional HTML-formatted user description
        about_raw: Optional raw text version of the user's description
        warned: Whether the user has been warned (mod/admin only)
        warn_message: Optional warning message (mod/admin only)
        banned: Whether the user is currently banned (mod/admin only)
        ban_until: Optional timestamp until which the user is banned (mod/admin only)
        ban_message: Optional reason for the ban (mod/admin only)
        delete_in_progress: Whether the user account deletion is in progress (mod/admin only)
        delete_at: Optional timestamp when the account deletion is scheduled (mod/admin only)
    """

    id: str
    role: Role
    ingame_name: str = msgspec.field(name="ingameName")
    reputation: int
    locale: str
    platform: str
    crossplay: bool
    status: str
    activity: ActivityModel
    last_seen: str = msgspec.field(name="lastSeen")
    mastery_rank: int = msgspec.field(name="masteryRank")
    credits: int
    theme: str
    verification: bool
    check_code: str = msgspec.field(name="checkCode")
    tier: Tier
    subscription: bool
    linked_accounts: LinkedAccounts = msgspec.field(name="linkedAccounts")
    has_email: bool = msgspec.field(name="hasEmail")
    created_at: str = msgspec.field(name="createdAt")
    reviews_left: int = msgspec.field(name="reviewsLeft")
    unread_messages: int = msgspec.field(name="unreadMessages")
    # Optional fields
    avatar: str | None = None
    achievement_showcase: List[AchievementModel] = msgspec.field(
        default_factory=list, name="achievementShowcase"
    )
    ignore_list: List[str] = msgspec.field(default_factory=list, name="ignoreList")
    about: Optional[str] = None
    about_raw: Optional[str] = msgspec.field(default=None, name="aboutRaw")
    warned: Optional[bool] = None
    warn_message: Optional[str] = msgspec.field(default=None, name="warnMessage")
    banned: Optional[bool] = None
    ban_until: Optional[str] = msgspec.field(default=None, name="banUntil")
    ban_message: Optional[str] = msgspec.field(default=None, name="banMessage")
    delete_in_progress: Optional[bool] = msgspec.field(
        default=None, name="deleteInProgress"
    )
    delete_at: Optional[str] = msgspec.field(default=None, name="deleteAt")
