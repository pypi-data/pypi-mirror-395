# FortniteGGAPI

I think this is the only wrapper for fortnite.gg cosmetics

[![Downloads](https://pepy.tech/badge/FortniteGGAPI)](https://pepy.tech/project/FortniteGGAPI)
[![Downloads](https://pepy.tech/badge/FortniteGGAPI/week)](https://pepy.tech/project/FortniteGGAPI)
[![Downloads](https://pepy.tech/badge/FortniteGGAPI/month)](https://pepy.tech/project/FortniteGGAPI)
[![Requires: Python 3.x](https://img.shields.io/pypi/pyversions/FortniteGGAPI.svg)](https://pypi.org/project/FortniteGGAPI/)
[![Version: 1.0.0](https://img.shields.io/pypi/v/FortniteGGAPI.svg)](https://pypi.org/project/FortniteGGAPI/)

### Setup:

`pip install FortniteGGAPI`
`py -m pip install FortniteGGAPI`

### Usage

```py
import asyncio

from FortniteGGAPI import CosmeticsAPI


async def test_store_items():
    api = CosmeticsAPI(language="en")
    await api.store_items()  # Store items from the API into cache can take some time on first run

    while True:
        item = await api.get_item(input("Enter item: "))
        if item:
            print(item.api_item_id)
            print(item.name)
            print(item.image_url)
            print(item.video_url)
            print(item.item_id)
            print(item.added)
            print(item.dict())


if __name__ == "__main__":
    asyncio.run(test_store_items())

```
