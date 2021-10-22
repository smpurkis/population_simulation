from BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(self, colour: str = "pink"):
        super().__init__(colour=colour)

    def __str__(self):
        return f"pig_{str(self.creation_time).replace(' ', '-')}"
