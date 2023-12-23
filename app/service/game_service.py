import asyncio
from typing import List

import httpx

from app.config import settings
from app.entities.map import Map
from app.entities.ship import Ship
from app.schemas.command import Command
from app.schemas.default_response import DefaultResponse
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
            async with httpx.AsyncClient() as client:
                map_response = await client.get(map_url, headers=headers)
            if map_response.status_code == 200:
                map_data = map_response.json()
                return Map(**map_data)
            else:
                print(f"Request failed with status code {map_response.status_code}")
    else:
        print(f"Request failed with status code {response.status_code}")


async def register_deathmatch() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/deathMatch/registration", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success') or data['errors'][0]['message'] == 'Вы уже участвуете в битве':
            return True
        else:
            print(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        print(f"Request failed with status code {response.status_code}")
        return False


async def leave_deathmatch() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/deathMatch/exitBattle", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('success')
        else:
            print(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        print(f"Request failed with status code {response.status_code}")
        return False


async def register_battle_royal() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/royalBattle/registration", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('success')
        else:
            print(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        print(f"Request failed with status code {response.status_code}")
        return False


async def scan() -> Scan:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.external_url}/scan", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(data)
            return Response(**data).scan
        else:
            print(f"Request failed with errors  {data.get('errors')}")
    else:
        print(f"Request failed with status code {response.status_code}")


async def long_scan(x: int, y: int) -> Scan:
    headers = {"X-API-Key": settings.token, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/longScan",
                                     headers=headers,
                                     json={"x": x, "y": y})
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return Response(**data).scan
        else:
            print(f"Request failed with errors  {data.get('errors')}")
    else:
        print(f"Request failed with status code {response.status_code}")


async def send_commands(ships: List[Command]) -> DefaultResponse:
    headers = {"X-API-Key": settings.token, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/longScan",
                                     headers=headers,
                                     json=ships)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return DefaultResponse(**data)
        else:
            print(f"Request failed with errors  {data.get('errors')}")
    else:
        print(f"Request failed with status code {response.status_code}")
