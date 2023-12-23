from app.enums.directions import Direction
from app.schemas.command import Command


class Ship:
    def __init__(self, id: int, x: int, y: int, size: int, hp: int, maxHp: int,
                 direction: str, speed: int, maxSpeed: int, minSpeed: int,
                 maxChangeSpeed: int, cannonCooldown: int, cannonCooldownLeft: int,
                 cannonRadius: int, scanRadius: int, cannonShootSuccessCount: int):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.hp = hp
        self.maxHp = maxHp
        self.direction = Direction(direction)
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.minSpeed = minSpeed
        self.maxChangeSpeed = maxChangeSpeed
        self.cannonCooldown = cannonCooldown
        self.cannonCooldownLeft = cannonCooldownLeft
        self.cannonRadius = cannonRadius
        self.scanRadius = scanRadius
        self.cannonShootSuccessCount = cannonShootSuccessCount
