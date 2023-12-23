from app.schemas.cannon_shoot import CannonShoot


class Command:
    def __init__(self, id: int, changeSpeed: int = None, rotate: int = None, cannon_shoot: CannonShoot = None):
        self.id = id
        self.changeSpeed = changeSpeed
        self.rotate = rotate
        self.cannon_shoot = cannon_shoot

    def to_dict(self):
        return {
            'id': self.id,
            'changeSpeed': self.changeSpeed,
            'rotate': self.rotate,
            'cannonShoot': self.cannon_shoot.to_dict() if self.cannon_shoot else None
        }
