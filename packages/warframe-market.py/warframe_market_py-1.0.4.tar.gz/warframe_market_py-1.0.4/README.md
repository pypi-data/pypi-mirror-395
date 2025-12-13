# warframe-market.py

An asynchronous Python client for the [Warframe Market API V2](https://api.warframe.market/v2).

> **Warning**: This project is in development and not yet ready for production use.


# Installation
```bash
pip install warframe-market.py
```

## Requirements
- Python 3.9+
- `aiohttp`
- `msgspec`

## Basic Usage
```python
import asyncio
from warframe_market.client import WarframeMarketClient
from warframe_market.api.item import Items, Item

async def main():
    async with WarframeMarketClient() as client:
        # Get all items
        items = await client.get_all_items()
        for item in items.data:
            print(item.i18n["en"].name)
        
        # Get a single item 
        item = await client.get_item("nova_prime_set")
        print(item)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```

## Advanced Usage

### Other languages or platforms
By default, the client uses English language, platform is PC and crossplay enabled. You can change these settings by passing parameters to the client:

```python

from warframe_market.client import WarframeMarketClient
from warframe_market.common import Language, Platform

async with WarframeMarketClient(
    language=Language.ENGLISH,
    platform=Platform.SWITCH,
    crossplay=False
) as client:
    # Your code here
```


### Get top 5 sell/buy orders for an item
```python
from warframe_market.client import WarframeMarketClient


async with WarframeMarketClient() as client:
    item = "nekros_prime_chassis_blueprint"

    item_data = await client.get_top_orders_for_item(item)
    print(f"Top sell orders: \n {item_data.data.sell}")
    print(f"Top buy orders: \n {item_data.data.buy}")
```

### Get top 5 sell/buy orders for an item with custom parameters
Items like mods can have additional parameters like rank You can pass these parameters in 2 ways:

```python
from warframe_market.client import WarframeMarketClient
from warframe_market.api import OrdersItemTop

async with WarframeMarketClient() as client:
    item = "primed_continuity"
    rank = 10  # for maxed rank

    # Using the API model
    item_data = await client.get(OrdersItemTop, slug=item, rank=rank)
    print(f"Top sell orders: \n {item_data.data.sell}")
    print(f"Top buy orders: \n {item_data.data.buy}")

    # Using the convenience method
    item_data = await client.get_top_orders_for_item(item, rank=rank)
    print(f"Top sell orders: \n {item_data.data.sell}")
    print(f"Top buy orders: \n {item_data.data.buy}")
```


### Use API models directly
```python
from warframe_market.client import WarframeMarketClient
from warframe_market.api import OrdersItemTop


async with WarframeMarketClient() as client:
    item = "nekros_prime_chassis_blueprint"

    item_data = await client.get(OrdersItemTop, slug=item)
    print(f"Top sell orders: \n {item_data.data.sell}")
    print(f"Top buy orders: \n {item_data.data.buy}")

```


### Use a custom API model
```python
import msgspec
from typing import Optional
from warframe_market.client import WarframeMarketClient
from warframe_market.common import BaseRequest


class _CustomData(msgspec.Struct):
    """Custom data model"""

    field1: str
    field2: Optional[str] = None 


class CustomAPI(BaseRequest):
    """Custom API request model"""
    endpoint = "/a/new/endpoint/{slug}"
    __slug__ = True # Indicates that 'slug' is a path parameter
    __params__ = ["param1", "param2" ] # Query parameters allowed in the request

    data: _CustomData


async with WarframeMarketClient() as client:
    item = "nekros_prime_chassis_blueprint"
    param1 = "value1"
    param2 = "value2"

    custom_data = await client.get(CustomAPI, slug=item, param1=param1, param2=param2)
    print(custom_data.data.field1)
    print(custom_data.data.field2)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.