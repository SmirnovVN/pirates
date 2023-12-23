import asyncio
from typing import List

import httpx

from app.config import settings
from app.entities.map import Map
from app.entities.ship import Ship
from app.schemas.response import Response
from app.schemas.scan import Scan


async def get_map() -> Map:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.external_url}/map", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            map_url = data.get('mapUrl')
            print(data)
            async with httpx.AsyncClient() as client:
                map_response = await client.get(map_url, headers=headers)
            if map_response.status_code == 200:
                map_data = map_response.json()
                print(map_data)
                return Map(**map_data)
            else:
                print(f"Request failed with status code {map_response.status_code}")
    else:
        print(f"Request failed with status code {response.status_code}")


asyncio.run(get_map())


async def register_deathmatch() -> bool:
    pass


async def leave_deathmatch() -> bool:
    pass


async def register_battle_royal() -> bool:
    pass


async def scan() -> Scan:
    pass


async def long_scan() -> Scan:
    pass


async def send_commands(ships: List[Ship]) -> Response:
    pass
