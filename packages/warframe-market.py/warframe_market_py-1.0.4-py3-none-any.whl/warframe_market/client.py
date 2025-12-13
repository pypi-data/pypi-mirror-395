import aiohttp
from typing import TypeVar, Type, Optional

from .common import *
from .api import *
                

T = TypeVar("T", bound=BaseRequest)


class WarframeMarketClient:
    """Client for interacting with Warframe Market API.
    Args:
        base_url (str): Base URL for the API. Default is "https://api.warframe.market/v2".
        language (Language): Language for the API responses. Default is Language.ENGLISH.
        platform (Platform): Platform for the API requests. Default is Platform.PC.
        crossplay (bool): Whether to enable crossplay. Default is True.
    """

    def __init__(self,
                 base_url: str = BASE_URL,
                language: Language = Language.ENGLISH,
                platform: Platform = Platform.PC,
                crossplay: bool = True):
        self.base_url = base_url
        self.response = None
        self.language = language
        self.platform = platform
        self.crossplay = crossplay
    
    @property
    def headers(self) -> dict:
        """Headers for the API requests."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Language": self.language.value,
            "Platform": self.platform.value,
            "Crossplay": str(self.crossplay).lower()
        }

    async def get(self, request_class: Type[T], slug="", **kwargs) -> T:
        """Perform a GET request using the specified request class.

        Args:
            request_class: The request class that defines the endpoint and response type
            slug: Optional slug to append to the endpoint URL
            **kwargs: Additional query parameters to include in the request

        Returns:
            The parsed API response
        """
        endpoint = request_class._get_endpoint(slug=slug, **kwargs)
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                #TODO: Handle exceptions and errors in a pythonic way
                if response.status != 200:
                    raise Exception(f"Error {response.status}: {await response.text()}")
                data = await response.text()
                return request_class._decode(data)
    

    # Ready for use API calls

    ####################
    ## ITEM APIs
    ####################
    async def get_all_items(self) -> Items:
        """Get list of all items."""
        return await self.get(Items)
    
    async def get_item(self, slug: str) -> Item:
        """Get details of a specific item by slug.
        Args:
            slug: The slug of the item to retrieve (e.g., 'mesa_prime_blueprint')
        """
        return await self.get(Item, slug=slug)
    
    async def get_item_set(self, slug: str) -> ItemSet:
        """Get details of an item set by slug.
        
        Args:
            slug: The slug of a specific item in the set you want to retrieve (e.g. mesa_prime_blueprint')
        """
        return await self.get(ItemSet, slug=slug)
    
    ####################
    ## ORDER APIs
    ####################
    async def get_orders_for_item(self, slug: str) -> OrdersItem:
        """Get a list of all orders for an item from users who were online within the last 7 days.
        
        Args:
            slug: The slug of the item to retrieve orders for (e.g., 'mesa_prime_blueprint')
        """
        return await self.get(OrdersItem, slug=slug)

    async def get_top_orders_for_item(
            self,
            slug: str,
            rank: Optional[int] = None,
            rankLt: Optional[int] = None,
            charges: Optional[int] = None,
            chargesLt: Optional[int] = None,
            amberStars: Optional[int] = None,
            amberStarsLt: Optional[int] = None,
            cyanStars: Optional[int] = None,
            cyanStarsLt: Optional[int] = None,
            subtype: Optional[Subtype] = None
            ) -> OrdersItemTop:
        """Get top 5 sell and buy orders for a specific item from current online users.
        Args:
            slug: The slug of the item to retrieve orders for (e.g., 'mesa_prime_blueprint')
            rank: Only when applicable, filter by specific rank (e.g., 0, 1, 2, etc.)
            rankLt: Only when applicable, filter by rank less than specified value
            charges: Only when applicable, filter by charges (e.g., 0, 1, 2, etc.)
            chargesLt: Only when applicable, filter by charges less than specified value
            amberStars: Only when applicable, filter by amber stars (e.g., 0, 1, 2, etc.)
            amberStarsLt: Only when applicable, filter by amber stars less than specified value
            cyanStars: Only when applicable, filter by cyan stars (e.g., 0, 1, 2, etc.)
            cyanStarsLt: Only when applicable, filter by cyan stars less than specified value
            subtype: Only when applicable, filter by Item subtype (e.g. "blueprint", "crafted)
        """
        return await self.get(
            OrdersItemTop,
            slug=slug,
            rank=rank,
            rankLt=rankLt,
            charges=charges,
            chargesLt=chargesLt,
            amberStars=amberStars,
            amberStarsLt=amberStarsLt,
            cyanStars=cyanStars,
            cyanStarsLt=cyanStarsLt,
            subtype=subtype.value if subtype else None
        )

    async def get_orders_from_user(
            self,
            username: str,
            platform: Platform = Platform.PC
            ) -> OrdersUser:
        """Get all orders from a specific user.
        
        Args:
            username: The username of the user to retrieve orders from.
            platform: The platform of the user (default is PC)
        """
        return await self.get(OrdersUser, slug=username, platform=platform.value)


    async def __aenter__(self):
        """Enter async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Exit async context manager."""
        pass
