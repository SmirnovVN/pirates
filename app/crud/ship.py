from typing import Sequence


from app.models import Ship
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_ship(
    db: AsyncSession,
    name: str,
    x: float,
    y: float
) -> Ship:
    new_ship = Ship(name=name, x=x, y=y)
    db.add(new_ship)
    await db.commit()
    await db.refresh(new_ship)
    return new_ship


async def get_ship(db: AsyncSession, ship_name: str) -> Ship:
    ship: Ship = (
        await db.scalars(
            select(
                Ship
            ).where(
                Ship.name == ship_name
            )
        )
    ).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship


async def get_ships_by_coordinates(
    db: AsyncSession,
    x: float,
    y: float,
    eps: float = 1
) -> Sequence[Ship]:
    return (
        await db.scalars(
            select(
                Ship
            ).where(
                Ship.x.between(x - eps, x + eps) & Ship.y.between(y - eps, y + eps)
            )
        )
    ).all()


async def move_ship(
    db: AsyncSession,
    ship: Ship,
    x: float,
    y: float
) -> Ship:
    ship.x = x
    ship.y = y
    await db.commit()
    await db.refresh(ship)
    return ship
