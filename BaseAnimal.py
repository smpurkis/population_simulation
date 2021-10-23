from datetime import datetime as dt
import random
from typing import Tuple


class BaseAnimal:
    def __init__(self, colour: str = "black", position: Tuple[int, int] = None):
        self.speed = 1
        self.colour = colour
        self.creation_time = dt.now().time()
        self.position = position

    def __str__(self):
        raise NotImplementedError("This is a Base Class, don't call this!")

    def move(self, direction: str = None):
        if direction is None:
            x_step = random.choice(range(-1, 1))
            y_step = random.choice(range(-1, 1))
            self.position[0] += x_step
            self.position[1] += y_step
