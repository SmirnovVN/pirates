from app.schemas.cannon_shoot import CannonShoot


class Command:
    def __init__(self, id: int, changeSpeed: int, rotate: int, cannon_shoot: CannonShoot):
        self.id = id
        self.changeSpeed = changeSpeed
        self.rotate = rotate
        self.cannon_shoot = cannon_shoot
