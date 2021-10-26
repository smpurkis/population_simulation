from typing import Tuple

import numpy as np

from BaseEntity import BaseEntity
from Fox import Fox
from Grass import Grass
from Pig import Pig

np.set_printoptions(linewidth=1000)


class WorldBoard:
    def __init__(self, size: Tuple[int, int] = (100, 100)):
        self.size = size
        self.positions = np.empty(shape=size, dtype=object)
        self.objects = []

    def __str__(self):
        pos_str = self.positions.astype(str)
        char_to_show = 2
        for ix, iy in np.ndindex(pos_str.shape):
            if pos_str[ix, iy] == "None":
                pos_str[ix, iy] = ""
            pos_str[ix, iy] = pos_str[ix, iy].ljust(char_to_show)[:char_to_show]
        return str(pos_str)

    def spawn(self, entity_type: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            available_positions = np.argwhere(self.positions == None)
            random_empty_position = rep = available_positions[np.random.choice(available_positions.shape[0])]
            entity = None
            if entity_type == "grass":
                entity = Grass(position=random_empty_position)
            elif entity_type == "pig":
                entity = Pig(position=random_empty_position)
            elif entity_type == "fox":
                entity = Fox(position=random_empty_position)
            self.positions[tuple(rep)] = entity
            self.objects.append(entity)

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_type="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_type="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_type="fox", number_to_spawn=number_to_spawn)

    def get_available_positions(self, entity: BaseEntity):
        i, j = entity.position
        li, hi = max(i-1, 0), min(i+2, self.size[0])
        lj, hj = max(j-1, 0), min(j+2, self.size[1])
        area = self.positions[li:hi, lj:hj]
        # available_positions = list(np.where(area != 0))
        available_positions = list(np.where(area != entity))
        available_positions[0] += li
        available_positions[1] += lj
        available_positions = tuple(zip(available_positions[0], available_positions[1]))
        return available_positions

    def move_foxes(self):
        foxes = [e for e in self.objects if isinstance(e, Fox)]
        fox_positions = [fox.position for fox in foxes]
        world_fox_positions = np.where(np.vectorize(lambda x: isinstance(x, Fox))(self.positions))
        for fox in foxes:
            available_positions = self.get_available_positions(fox)
            current_position = tuple(fox.position)

            chosen_position = fox.move(available_positions)

            self.positions[current_position] = None
            self.positions[chosen_position] = fox
        p = 0
