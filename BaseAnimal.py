from datetime import datetime as dt


class BaseAnimal:
    def __init__(self, colour: str = "black"):
        self.speed = 1
        self.colour = colour
        self.creation_time = dt.now().time()

    def __str__(self):
        raise NotImplementedError("This is a Base Class, don't call this!")
