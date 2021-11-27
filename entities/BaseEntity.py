import random
from datetime import datetime as dt


class BaseEntity:
    def __init__(
            self,
            colour: str = "black",
            board_size: float = 10,
            speed: int = 0
    ):
        self.speed = speed
        self.colour = colour
        self.board_size = board_size
        self.creation_time = dt.now().time()
        self.set_random_position()

    def set_random_position(self):
        """
        Set random position on the board
        :return:
        """
        self.position = [random.uniform(0, self.board_size), random.uniform(0, self.board_size)]