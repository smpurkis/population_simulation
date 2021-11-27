import random
from datetime import datetime as dt

from entities.BaseEntity import BaseEntity


class BaseAnimal(BaseEntity):
    def __init__(self, colour: str = "black", board_size: float = 10, speed: int = 0):
        super().__init__(colour, board_size, speed)
        self.speed = speed
        self.colour = colour
        self.board_size = board_size
        self.creation_time = dt.now().time()

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
