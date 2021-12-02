from entities.BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(self, colour: str = "orange", speed: float = 1, *args, **kwargs):
        super().__init__(colour, speed, *args, **kwargs)
