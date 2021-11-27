from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt

from entities import Fox, Grass, Pig

np.set_printoptions(linewidth=1000)


class WorldBoard:
    def __init__(self, size: Tuple[float, float] = (100, 100)):
        self.size = size
        self.objects = {}

    def spawn(self, entity_type: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            entity = None
            if entity_type == "grass":
                entity = Grass(board_size=self.size)
            elif entity_type == "pig":
                entity = Pig(board_size=self.size)
            elif entity_type == "fox":
                entity = Fox(board_size=self.size)
            print(entity, entity.position)
            if self.objects.get(entity_type) is None:
                self.objects[entity_type] = []
            self.objects[entity_type].append(entity)

    def spawn_all_entities(self):
        self.spawn_plants()
        self.spawn_pigs()
        self.spawn_foxes()

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_type="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_type="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_type="fox", number_to_spawn=number_to_spawn)

    def move_animals(self):
        for animal in self.objects["fox"] + self.objects["pig"]:
            animal.move()

    def plot_world(self):
        """
        Plots all the entites by their position on a matplotlib graph
        :return:
        """
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.size[0])
        ax.set_ylim(0, self.size[1])
        for entity in self.objects["grass"] + self.objects["pig"] + self.objects["fox"]:
            print(entity, entity.position)
            ax.scatter(entity.position[0], entity.position[1], c=entity.colour)
        plt.show()




