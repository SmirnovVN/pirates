import logging
from typing import List, Optional
from app.entities.map import Map
from app.entities.ship import Ship
from app.enums.direction import Direction
from app.schemas.cannon_shoot import CannonShoot
from app.schemas.command import Command


def distance(x1: float, x2: float, y1: float, y2: float) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def decide(ship: Ship, map: Map, enemies: List[Ship], dest_x: int, dest_y: int) -> (Command, int, int):
    if enemies:
        cannon_shoot = calculate_shot(ship, enemies)
        rotate, new_dest_x, new_dest_y = calculate_direction_to_closest_enemy(ship, enemies)
        change_speed = calculate_speed_around_enemies(ship, cannon_shoot)
    else:
        change_speed = calculate_speed(ship, map, enemies, dest_x, dest_y)
        rotate, new_dest_x, new_dest_y = calculate_direction_by_desired_direction(ship,
                                                                                  get_desired_direction(ship, dest_x,
                                                                                                        dest_y), dest_x,
                                                                                  dest_y)
        cannon_shoot = None
    return Command(ship.id, changeSpeed=None if change_speed == 0 else change_speed,
                   rotate=None if rotate == 0 else rotate, cannon_shoot=cannon_shoot), new_dest_x, new_dest_y


def calculate_speed_around_enemies(ship: Ship, cannon_shot: CannonShoot) -> Optional[int]:
    if cannon_shot:
        return -ship.maxChangeSpeed if ship.speed >= ship.maxChangeSpeed else -ship.speed
    else:
        return None


def get_desired_direction(ship: Ship, dest_x: int, dest_y: int) -> Direction:
    if dest_x is None or dest_y is None:
        return Direction(ship.direction)
    if ship.x < dest_x:
        return Direction.EAST
    elif ship.x > dest_x:
        return Direction.WEST
    elif ship.y < dest_y:
        return Direction.SOUTH
    elif ship.y > dest_y:
        return Direction.NORTH
    else:
        return Direction(ship.direction)


def calculate_speed(ship: Ship, map: Map, enemies: List[Ship], dest_x: int, dest_y: int) -> int:
    if ship.speed == 0:
        return ship.maxChangeSpeed
    else:
        return 0


def calculate_direction_to_closest_enemy(ship: Ship, enemies: List[Ship]) -> (int, int, int):
    lowest_distance = 100000
    closest_enemy = None
    for enemy in enemies:
        if distance(ship.x, enemy.x, ship.y, enemy.y) < lowest_distance:
            lowest_distance = distance(ship.x, enemy.x, ship.y, enemy.y)
            closest_enemy = enemy
    return (calculate_direction(ship, closest_enemy), closest_enemy.x,
            closest_enemy.y)


def calculate_shot(ship: Ship, enemies: List[Ship]) -> Optional[CannonShoot]:
    for enemy in enemies:
        pred_x, pred_y = get_enemy_predicted_position(enemy)
        if distance(ship.x, pred_x, ship.y, pred_y) <= ship.cannonRadius:
            logging.info(f"Shoot to {enemy.x} {enemy.y} by {ship.id}")
            return CannonShoot(enemy.x, enemy.y)


def get_enemy_predicted_position(enemy: Ship) -> (int, int):
    if enemy.speed > 0:
        if enemy.direction == Direction.NORTH:
            return enemy.x, int(enemy.y - enemy.speed + enemy.size / 2)
        elif enemy.direction == Direction.EAST:
            return int(enemy.x + enemy.speed + enemy.size / 2), enemy.y
        elif enemy.direction == Direction.SOUTH:
            return enemy.x, int(enemy.y + enemy.speed + enemy.size / 2)
        elif enemy.direction == Direction.WEST:
            return int(enemy.x - enemy.speed + enemy.size / 2), enemy.y
    else:
        return enemy.x, enemy.y


def calculate_direction(ship: Ship, enemy: Ship) -> int:
    if enemy is not None:
        delta_x = abs(ship.x - enemy.x)
        delta_y = abs(ship.y - enemy.y)
        if delta_x < delta_y:
            if ((ship.x > enemy.x and ship.direction == Direction.NORTH)
                    or (ship.x < enemy.x and ship.direction == Direction.SOUTH)):
                return -90
            elif ((ship.x > enemy.x and ship.direction == Direction.EAST)
                  or (ship.x < enemy.x and ship.direction == Direction.WEST)):
                return 90
            else:
                return 0
        else:
            if ((ship.y > enemy.y and ship.direction == Direction.EAST)
                    or (ship.y < enemy.y and ship.direction == Direction.WEST)):
                return -90
            elif ((ship.y > enemy.y and ship.direction == Direction.SOUTH)
                  or (ship.y < enemy.y and ship.direction == Direction.NORTH)):
                return 90
            else:
                return 0
    else:
        return 0


def calculate_direction_by_desired_direction(ship: Ship, desired_direction: Direction, dest_x: int, dest_y: int) -> (
int, int, int):
    if ship.direction == desired_direction:
        return 0, dest_x, dest_y
    elif ship.direction == Direction.NORTH:
        if desired_direction == Direction.EAST:
            return 90, dest_x, dest_y
        else:
            return -90, dest_x, dest_y
    elif ship.direction == Direction.EAST:
        if desired_direction == Direction.SOUTH:
            return 90, dest_x, dest_y
        else:
            return -90, dest_x, dest_y
    elif ship.direction == Direction.SOUTH:
        if desired_direction == Direction.WEST:
            return 90, dest_x, dest_y
        else:
            return -90, dest_x, dest_y
    elif ship.direction == Direction.WEST:
        if desired_direction == Direction.NORTH:
            return 90, dest_x, dest_y
        else:
            return -90, dest_x, dest_y
