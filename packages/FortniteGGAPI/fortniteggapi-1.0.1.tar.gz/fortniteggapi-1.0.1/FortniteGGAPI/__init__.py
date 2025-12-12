import json
import aiohttp
import re

import cloudscraper


from typing import Literal, TypedDict
from pydantic import BaseModel


class FortniteGGItem(TypedDict):
    id: int
    type: int
    s: int
    t: list[int]
    source: int
    r: int
    rarity: int
    added: int
    name: str
    img: int
    season: int


class APIItem(BaseModel):
    api_item_id: int
    item_id: str | None
    added: int
    name: str
    video_url: str
    image_url: str
    url: str
    season: int


class CosmeticsAPI:
    def __init__(
        self,
        language: Literal[
            "en",
            "ar",
            "de",
            "es",
            "es-419",
            "fr",
            "it",
            "ja",
            "ko",
            "pl",
            "pt-BR",
            "ru",
            "tr",
        ] = "en",
    ) -> None:
        self.language = language
        self.BASE_URL = (
            f"https://fortnite.gg/data/items/all-v2.{language}.js?v=1763782224"
        )
        self.scraper = cloudscraper.create_scraper()  # type: ignore
        self.items: list[APIItem] = []

    def get_id_via_html(self, item_id: int) -> str | None:
        try:
            response = self.scraper.get(f"https://fortnite.gg/cosmetics?id={item_id}")

            if response.status_code == 200:
                text = response.text

                # Same Regex logic
                match = re.search(r"ID:</span>\s*(.*?)(?=<)", text)

                if match:
                    return match.group(1).strip()
                else:
                    return None
            else:
                return None

        except:
            return None

    async def get_item(self, name: str | None) -> APIItem | None:

        if name:
            for item in self.items:
                if item.name.lower() == name.lower():
                    return item
        else:
            return None
        return None

    async def store_items(self):

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                file_content = await response.text()

                start_marker = "Items=["
                start_index = file_content.find(start_marker)

                if start_index != -1:
                    raw_list_string = file_content[start_index + len("Items=") :]

                    end_index = raw_list_string.rfind("]")

                    if end_index != -1:
                        clean_string = raw_list_string[: end_index + 1]

                        clean_string = re.sub(r",(\s*[\]}])", r"\1", clean_string)

                        formatted_json = re.sub(
                            r"(?<=[{,])\s*([a-zA-Z0-9_$]+)\s*:", r'"\1":', clean_string
                        )

                        try:

                            raw_json_items: list[FortniteGGItem] = json.loads(
                                formatted_json
                            )
                            final_items: list[APIItem] = []

                            with open("cache.json", encoding="utf-8") as f:
                                cached_items = json.load(f)

                            cached_ids = [item["api_item_id"] for item in cached_items]

                            for items in raw_json_items:
                                if items["id"] in cached_ids:
                                    cached_item = next(
                                        item
                                        for item in cached_items
                                        if item["api_item_id"] == items["id"]
                                    )
                                    item = APIItem(**cached_item)
                                    final_items.append(item)
                                    print(
                                        f"Loaded from cache: {item.name} [{item.item_id}]"
                                    )
                                else:
                                    item = APIItem(
                                        api_item_id=items["id"],
                                        item_id=self.get_id_via_html(items["id"]),
                                        added=items["added"],
                                        name=items["name"],
                                        video_url=f"https://fnggcdn.com/items/{items['id']}/video.mp4?4",
                                        image_url=f"https://fortnite.gg/img/items/{items['id']}/icon.jpg?4",
                                        url=f"https://fortnite.gg/cosmetics?id={items['id']}",
                                        season=items["season"],
                                    )
                                    final_items.append(item)
                                    print(f"Stored: {item.name} [{item.item_id}]")

                            self.items = final_items
                            with open("cache.json", "w", encoding="utf-8") as f:
                                json.dump(
                                    [item.dict() for item in self.items],
                                    f,
                                    ensure_ascii=False,
                                    indent=4,
                                )

                        except json.JSONDecodeError as e:
                            raise ValueError(
                                f"Error parsing JSON: {e}\nNear end of string: {formatted_json[-50:]}"
                            )
                    else:
                        raise SyntaxError("Could not find the end of the Items list.")
                else:
                    raise SyntaxError("Could not find 'Items=['.")
