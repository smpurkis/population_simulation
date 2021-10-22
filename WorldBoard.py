from typing import Tuple

import numpy as np
from Grass import Grass

np.set_printoptions(linewidth=1000)
class WorldBoard:
    def __init__(self, size: Tuple[int, int] = (100, 100)):
        self.size = size
        self.positions = np.empty(shape=size, dtype=object)
        self.objects = []

    def spawn_plants(self, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            available_positions = np.argwhere(self.positions == None)
            random_empty_position = rep = available_positions[np.random.choice(available_positions.shape[0])]
            grass = Grass(position=random_empty_position)
            self.positions[tuple(rep)] = grass
            self.objects.append(grass)

    def __str__(self):
        pos_str = self.positions.astype(str)
        for ix, iy in np.ndindex(pos_str.shape):
            if pos_str[ix, iy] == "None":
                pos_str[ix, iy] = ""
            pos_str[ix, iy] = pos_str[ix, iy].ljust(8)[:8]
        return str(pos_str)
