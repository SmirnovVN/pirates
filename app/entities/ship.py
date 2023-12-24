from app.enums.direction import Direction


class Ship:

    def __init__(self, id: int = None, x: int = None, y: int = None, size: int = None,
                 hp: int = None, maxHp: int = None, direction: str = None, speed: int = None, maxSpeed: int = None,
                 minSpeed: int = None, maxChangeSpeed: int = None, cannonCooldown: int = None,
                 cannonCooldownLeft: int = None, cannonRadius: int = None, scanRadius: int = None,
                 cannonShootSuccessCount: int = 0):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.hp = hp
        self.maxHp = maxHp
        self.direction = Direction(direction)
        self.speed = speed
        self.maxSpeed = 14
        self.minSpeed = minSpeed
        self.maxChangeSpeed = maxChangeSpeed
        self.cannonCooldown = cannonCooldown
        self.cannonCooldownLeft = cannonCooldownLeft
        self.cannonRadius = cannonRadius
        self.scanRadius = scanRadius
        self.cannonShootSuccessCount = cannonShootSuccessCount

    def __repr__(self):
        if self.maxChangeSpeed:
            ours = f'\nMs: {self.maxSpeed}, ms: {self.minSpeed}, acc: {self.maxChangeSpeed}, cd: {self.cannonCooldown}, cd_left: {self.cannonCooldownLeft}, cr: {self.cannonRadius}, sr: {self.scanRadius}'
            for i in range(self.cannonShootSuccessCount):
                ours += ' *'
        else:
            ours = ''
        return '\n'+'[]'*self.size + f'({self.x}, {self.y}, {self.direction.value}, speed: {self.speed}) id {self.id}, hp: {self.hp}' + ours
