from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(self, colour: str = "pink", speed: float = 0.5, *args, **kwargs):
        super().__init__(colour=colour, speed=speed, *args, **kwargs)
