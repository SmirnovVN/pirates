from typing import List

import requests
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.ship import move_ship
from app.entities.map import Map
from app.entities.ship import Ship
from app.enums.direction import Direction
from app.schemas.cannon_shoot import CannonShoot
from app.schemas.command import Command


def distance(x1: float, x2: float, y1: float, y2: float) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


# async def move_to_coordinates(db: AsyncSession, x: float, y: float):
#     ship: Ship = (
#         await db.scalars(
#             select(
#                 Ship
#             ).where(
#                 Ship.name == settings.ship_name
#             )
#         )
#     ).first()
#     while ship.x != x or ship.y != y:
#         d = distance(ship.x, x, ship.y, y)
#         step_x, step_y = (ship.x - x) / d, (ship.y - y) / d
#         await move(db, ship, step_x, step_y)


# async def move(db: AsyncSession, ship: Ship, x: float, y: float):
#     headers = {"Authorization": f"Bearer {settings.token}"}
#     response = requests.get(f"{settings.external_url}/move?x={x}&y={y}", headers=headers)
#
#     if response.status_code == 200:
#         ship = await move_ship(db, ship, x, y)


def decide(ship: Ship, map: Map, enemies: List[Ship]) -> Command:
    for enemy in enemies:
        if distance(ship.x, enemy.x, ship.y, enemy.y) <= ship.cannonRadius:
            print(f"Shoot to {enemy.x} {enemy.y} by {ship.id}")
            return Command(ship.id, cannon_shoot=CannonShoot(enemy.x, enemy.y))
        else:
            direction = calculate_direction(ship, enemy)
            return Command(ship.id, changeSpeed=1, rotate=direction)
    if ship.speed > 0:
        return Command(ship.id, changeSpeed=-1, rotate=0)


def calculate_direction(ship: Ship, enemy: Ship) -> int:
    delta_x = abs(ship.x - enemy.x)
    delta_y = abs(ship.y - enemy.y)
    if delta_x < delta_y:
        if ((ship.x > enemy.x and ship.direction == Direction.NORTH)
                or (ship.x < enemy.x and ship.direction == Direction.SOUTH)):
            return 90
        elif ((ship.x > enemy.x and ship.direction == Direction.EAST)
              or (ship.x < enemy.x and ship.direction == Direction.WEST)):
            return 0
        else:
            return -90
    else:
        if ((ship.y > enemy.y and ship.direction == Direction.EAST)
                or (ship.y < enemy.y and ship.direction == Direction.WEST)):
            return 90
        elif ((ship.y > enemy.y and ship.direction == Direction.SOUTH)
              or (ship.y < enemy.y and ship.direction == Direction.NORTH)):
            return 0
        else:
            return -90
