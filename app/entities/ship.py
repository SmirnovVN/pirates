from app.enums.direction import Direction


class Ship:

    def __init__(self, id: int = None, x: int = None, y: int = None, size: int = None,
                 hp: int = None, maxHp: int = None, direction: str = None, speed: int = None, maxSpeed: int = None,
                 minSpeed: int = None, maxChangeSpeed: int = None, cannonCooldown: int = None,
                 cannonCooldownLeft: int = None, cannonRadius: int = None, scanRadius: int = None,
                 cannonShootSuccessCount: int = None):
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
