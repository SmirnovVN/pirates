import requests
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.ship import move_ship
from app.models import Ship


def distance(x1: float, x2: float, y1: float, y2: float) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


async def move_to_coordinates(db: AsyncSession, x: float, y: float):
    ship: Ship = (
        await db.scalars(
            select(
                Ship
            ).where(
                Ship.name == settings.ship_name
            )
        )
    ).first()
    while ship.x != x or ship.y != y:
        d = distance(ship.x, x, ship.y, y)
        step_x, step_y = (ship.x - x) / d, (ship.y - y) / d
        await move(db, ship, step_x, step_y)


async def move(db: AsyncSession, ship: Ship, x: float, y: float):
    headers = {"Authorization": f"Bearer {settings.token}"}
    response = requests.get(f"{settings.external_url}/move?x={x}&y={y}", headers=headers)

    if response.status_code == 200:
        ship = await move_ship(db, ship, x, y)

        return ship
    else:
        raise HTTPException(status_code=response.status_code, detail="Error during move")
