from typing import Tuple

import numpy as np

from entities.BaseEntity import BaseEntity
from entities.Fox import Fox
from entities.Grass import Grass
from entities.Pig import Pig

np.set_printoptions(linewidth=1000)


class WorldBoard:
    def __init__(self, size: Tuple[int, int] = (100, 100)):
        self.size = size
        self.objects = {}

    def spawn(self, entity_type: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            entity = None
            if entity_type == "grass":
                entity = Grass()
            elif entity_type == "pig":
                entity = Pig()
            elif entity_type == "fox":
                entity = Fox()
            self.objects[entity_type].append(entity)

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_type="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_type="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_type="fox", number_to_spawn=number_to_spawn)

    def move_animals(self):
        for animal in self.objects["fox"] + self.objects["pig"]:
            animal.move()

