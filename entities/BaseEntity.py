import random
from datetime import datetime as dt
from typing import Tuple, Optional

from matplotlib.lines import Line2D


class BaseEntity:
    def __init__(
        self,
        colour,
        board_size: Tuple[float, float] = (100.0, 100.0),
    ):
        self.colour = colour
        self.board_size = board_size
        self.creation_time = dt.now().time()
        self.set_random_position()
        self.age = 0
        self.death_age = 0
        self.show = True
        self.alive = True
        self.position: Tuple[float, float] = (0.0, 0.0)
        self.point: Optional[Line2D]

    def set_random_position(self):
        """
        Set random position on the board
        :return:
        """
        self.position = [
            random.uniform(0, self.board_size[0]),
            random.uniform(0, self.board_size[1]),
        ]
