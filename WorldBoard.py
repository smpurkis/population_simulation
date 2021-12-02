import random
import time
from typing import Tuple, List, Dict, Optional

import matplotlib.pyplot as plt
from matplotlib import animation

from entities import Fox, Grass, Pig
from entities.BaseEntity import BaseEntity


class WorldBoard:
    def __init__(self, board_size: Tuple[float, float] = (100.0, 100.0)):
        self.board_size = board_size
        self.objects: Dict[str, List[BaseEntity]] = {}
        self.alive_animals: List[BaseEntity] = []
        self.object_list: List[BaseEntity] = []
        self.day: int = 0
        self._setup_plot()

    def spawn(self, entity_type: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            entity: BaseEntity
            if entity_type == "grass":
                entity = Grass(board_size=self.board_size)
            elif entity_type == "pig":
                entity = Pig(board_size=self.board_size)
            elif entity_type == "fox":
                entity = Fox(board_size=self.board_size)
            (point,) = self.ax.plot(
                [entity.position[0]], [entity.position[1]], "o", color=entity.colour
            )
            entity.point = point
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

    def step(self):
        self.day += 1

        for animal in self.objects["fox"] + self.objects["pig"]:
            animal.step()

        if self.day % 1 == 0:
            spawn_plants = random.randrange(100) <= 2
            if spawn_plants:
                number_to_spawn = random.choice(range(1, 4))
                # number_to_spawn = 1
                self.spawn_plants(number_to_spawn=number_to_spawn)

        self.object_list = [entity for l in list(self.objects.values()) for entity in l]

    def _setup_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

    def plot_world(self):
        """
        Plots all the entites by their position on a matplotlib graph
        :return:
        """
        self.ax.set_xlim(0, self.board_size[0])
        self.ax.set_ylim(0, self.board_size[1])
        self.object_list = [entity for l in list(self.objects.values()) for entity in l]

        global stationary_time
        stationary_time = time.time()

        def update_plot(n):
            self.step()
            for entity in self.object_list:
                point = entity.point
                if entity.show:
                    point.set_data([entity.position[0], entity.position[1]])
                    point._color = entity.colour
                else:
                    point.set_data([-1, -1])
            if self.day % 10 == 0:
                print(
                    f"day: {self.day}, time: {time.time() - stationary_time}, average: {1000 * ((time.time() - stationary_time) / self.day):.2f}ms"
                )
                exit(0)

        ani = animation.FuncAnimation(self.fig, update_plot, interval=40)
        plt.show()
