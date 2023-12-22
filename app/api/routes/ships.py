from app.api.dependencies import DBSessionDep
from app.crud.ship import get_ship, create_ship
from app.schemas.ship import Ship
from fastapi import APIRouter

router = APIRouter(
    tags=["ships"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new", response_model=Ship, status_code=201)
async def new_ship(name: str, x: float, y: float, db: DBSessionDep):
    """
    Get any ship details
    """
    ship = await create_ship(db, name, x, y)
    return ship


@router.get("/{ship_name}", response_model=Ship)
async def ship_details(ship_name: str, db: DBSessionDep):
    """
    Get any ship details
    """
    ship = await get_ship(db, ship_name)
    return ship
