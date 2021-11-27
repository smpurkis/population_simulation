from entities.BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(self, colour: str = "orange", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)
        self.speed = 1
