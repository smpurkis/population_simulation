import random
from datetime import datetime as dt
from typing import Tuple

import numpy as np


class BaseEntity:
    def __init__(self, colour: str = "black", position: Tuple[int, int] = None, speed: int = 0):
        self.speed = speed
        self.colour = colour
        self.creation_time = dt.now().time()
        self.position = position

    def __str__(self):
        raise NotImplementedError("This is a Base Class, don't call this!")

    def move(self, available_positions=None):
        if available_positions is None:
            x_step = random.choice(range(-1, 1))
            y_step = random.choice(range(-1, 1))
            self.position[0] += x_step
            self.position[1] += y_step
        else:
            chosen_position = random.choice(available_positions)
            self.position = chosen_position
        return self.position