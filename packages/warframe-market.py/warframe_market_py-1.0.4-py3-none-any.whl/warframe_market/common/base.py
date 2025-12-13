import msgspec
from datetime import datetime
from typing import TypeVar, ClassVar, Type, Optional, Any, List


def _dec_hook(type: Type, obj: Any) -> Any:

    # Decode UTC dates
    if isinstance(type, datetime) and isinstance(obj, str):
        return datetime.fromisoformat(obj.strip("Z"))

    # Will add more when needed

    return obj


class Base(msgspec.Struct, kw_only=True):
    """Base model"""

    api_version: str = msgspec.field(name="apiVersion")
    error: Optional[Any] = None


T = TypeVar("T", bound=Base)


class BaseRequest(Base):
    """Base model for all Warframe Market API requests.

    Attributes:
        __endpoint__: The API endpoint for the request.
        __params__: List of query parameters that can be used in the request.
        __slug__: Whether the request requires a slug in the endpoint.
    """

    __endpoint__: ClassVar[str]
    __params__: ClassVar[List[str]] = []
    __slug__: ClassVar[bool] = False

    @classmethod
    def _decode(cls: Type[T], response: str) -> T:
        """Decode the response string into a BaseResponse object."""
        return msgspec.json.decode(response, type=cls, dec_hook=_dec_hook)

    @classmethod
    def _get_endpoint(cls, slug: Optional[str] = None, **kwargs) -> str:
        """Build the endpoint URL with optional slug and query parameters."""
        endpoint = cls.__endpoint__
        if cls.__slug__ and slug:
            endpoint = endpoint.format(slug=slug)
        if cls.__params__:
            params = "&".join(
                f"{k}={v}" for k, v in kwargs.items() if k in cls.__params__ and v is not None
            )
            if params:
                endpoint += f"?{params}"
        return endpoint
