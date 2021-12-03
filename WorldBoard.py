import random
import time
from copy import copy
from typing import Tuple, List, Dict, Optional

import matplotlib.pyplot as plt
from matplotlib import animation

from WorldArea import WorldArea
from entities import Fox, Grass, Pig
from entities.BaseEntity import BaseEntity
from entities.BaseAnimal import BaseAnimal


class WorldBoard:
    def __init__(self, board_size: Tuple[float, float] = (100.0, 100.0)):
        self.board_size = board_size
        self.entities_dict: Dict[str, List[BaseEntity]] = {}
        self.alive_animals: List[BaseEntity] = []
        self.entity_list: List[BaseEntity] = []
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

            if self.entities_dict.get(entity_type) is None:
                self.entities_dict[entity_type] = []
            self.entities_dict[entity_type].append(entity)
            self.entity_list.append(entity)

    def spawn_all_entities(self, initial_populations: Dict[str, int]):
        self.spawn_plants(number_to_spawn=initial_populations["grass"])
        self.spawn_pigs(number_to_spawn=initial_populations["pig"])
        self.spawn_foxes(number_to_spawn=initial_populations["fox"])
        self.set_world_areas()

    def set_world_areas(self):
        for entity in self.entity_list:
            other_entities = copy(self.entity_list)
            other_entities.remove(entity)
            world_area = WorldArea(
                area_radius=entity.vision_radius,
                entities=other_entities,
                position=entity.position,
            )
            entity.world_area = world_area

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_type="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_type="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_type="fox", number_to_spawn=number_to_spawn)

    def step(self):
        self.day += 1

        for animal in self.entities_dict["fox"] + self.entities_dict["pig"]:
            animal.step()

        if self.day % 1 == 0:
            spawn_plants = random.randrange(100) <= 2
            if spawn_plants:
                number_to_spawn = random.choice(range(1, 4))
                # number_to_spawn = 1
                self.spawn_plants(number_to_spawn=number_to_spawn)

        self.entity_list = [
            entity for l in list(self.entities_dict.values()) for entity in l
        ]

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
        self.entity_list = [
            entity for l in list(self.entities_dict.values()) for entity in l
        ]

        global stationary_time
        stationary_time = time.time()

        def update_plot(n):
            self.step()
            for entity in self.entity_list:
                point = entity.point
                if entity.show:
                    point.set_data([entity.position[0], entity.position[1]])
                    point._color = entity.colour
                else:
                    point.set_data([-1, -1])
            if self.day % 10 == 0:
                time_taken = time.time() - stationary_time
                avg_time = 1000 * (time_taken / self.day)
                print(f"day: {self.day}, time: {time_taken}, average: {avg_time:.2f}ms")

        ani = animation.FuncAnimation(self.fig, update_plot, interval=40)
        plt.show()
