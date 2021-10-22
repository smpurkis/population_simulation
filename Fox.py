from BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(self, colour: str = "orange"):
        super().__init__(colour=colour)

    def __str__(self):
        return f"fox_{str(self.creation_time).replace(' ', '-')}"
