import logging
from typing import List

import httpx

from app.config import settings
from app.entities.island import Island
from app.entities.map import Map
from app.entities.ship import Ship
from app.entities.zone import Zone
from app.schemas.command import Command
from app.schemas.default_response import DefaultResponse
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
                islands = [Island(**d) for d in map_data['islands']]
                return Map(width=map_data['width'],
                           height=map_data['height'],
                           slug=map_data['slug'],
                           islands=islands)
            else:
                logging.error(f"Request failed with status code {map_response.status_code}")
    else:
        logging.error(f"Request failed with status code {response.status_code}")


async def register_deathmatch() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/deathMatch/registration",
                                     headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success') or data['errors'][0]['message'] == 'Вы уже участвуете в битве':
            return True
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return False


async def leave_deathmatch() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/deathMatch/exitBattle",
                                     headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('success')
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return False


async def register_battle_royal() -> bool:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/royalBattle/registration",
                                     headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data.get('success')
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
            return False
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return False


async def scan() -> Scan:
    headers = {"X-API-Key": settings.token}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.external_url}/scan", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            logging.debug(data)
            my_ships = [Ship(**entry) for entry in data['scan']['myShips']]
            enemies = [Ship(**entry) for entry in data['scan']['enemyShips']]
            return Scan(myShips=my_ships,
                        enemyShips=enemies,
                        zone=Zone(**data['scan']['zone']) if data['scan']['zone'] else None,
                        tick=data['scan']['tick'])
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
    else:
        logging.error(f"Request failed with status code {response.status_code}")


async def long_scan(x: int, y: int) -> DefaultResponse:
    headers = {"X-API-Key": settings.token, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/longScan",
                                     headers=headers,
                                     json={"x": x, "y": y})
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return DefaultResponse(**data)
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
    else:
        logging.error(f"Request failed with status code {response.status_code}")


async def send_commands(commands: List[Command]) -> DefaultResponse:
    headers = {"X-API-Key": settings.token, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.external_url}/shipCommand",
                                     headers=headers,
                                     json={'ships': [command.to_dict() for command in commands]})
    if response.status_code == 200:
        data = response.json()
        logging.debug(data)
        if data.get('success'):
            return DefaultResponse(**data)
        else:
            logging.error(f"Request failed with errors  {data.get('errors')}")
    else:
        logging.error(f"Request failed with status code {response.status_code}")
