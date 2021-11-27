import random
from datetime import datetime as dt
from typing import Tuple


class BaseEntity:
    def __init__(
            self,
            colour: str = "black",
            board_size: Tuple[float, float] = (100, 100),
    ):
        self.colour = colour
        self.board_size = board_size
        self.creation_time = dt.now().time()
        self.set_random_position()

    def set_random_position(self):
        """
        Set random position on the board
        :return:
        """
        self.position = [
            random.uniform(0, self.board_size[0]),
            random.uniform(0, self.board_size[1])
        ]
