from datetime import datetime as dt


class Grass:
    def __init__(self, colour: str = "green", position: tuple = None):
        self.colour = colour
        self.creation_time = dt.now().time()
        self.position = position

    def __str__(self):
        return f"grass_{str(self.creation_time).replace(' ', '-')}"
