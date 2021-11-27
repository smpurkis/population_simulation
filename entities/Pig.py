from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(self, colour: str = "pink", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)
        self.speed = 0.5
