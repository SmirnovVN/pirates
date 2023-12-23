import logging
from typing import List

from app.entities.map import Map
from app.entities.ship import Ship
from app.enums.direction import Direction
from app.schemas.cannon_shoot import CannonShoot
from app.schemas.command import Command


def distance(x1: float, x2: float, y1: float, y2: float) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def decide(ship: Ship, map: Map, enemies: List[Ship]) -> Command:
    for enemy in enemies:
        if distance(ship.x, enemy.x, ship.y, enemy.y) <= ship.cannonRadius:
            logging.debug(f"Shoot to {enemy.x} {enemy.y} by {ship.id}")
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
            return 0  # todo remove 0 т к ноль не нужно отправлять вообще
        else:
            return -90
    else:
        if ((ship.y > enemy.y and ship.direction == Direction.EAST)
                or (ship.y < enemy.y and ship.direction == Direction.WEST)):
            return 90
        elif ((ship.y > enemy.y and ship.direction == Direction.SOUTH)
              or (ship.y < enemy.y and ship.direction == Direction.NORTH)):
            return 0 # todo remove 0 т к ноль не нужно отправлять вообще
        else:
            return -90
