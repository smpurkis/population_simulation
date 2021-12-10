import random
import time
from copy import copy
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt
from matplotlib import animation

from WorldArea import WorldArea
from entities import Fox, Grass, Pig
from entities.BaseAnimal import BaseAnimal
from entities.BaseEntity import BaseEntity


class WorldBoard:
    def __init__(self, board_size: Tuple[float, float] = (100.0, 100.0)):
        self.board_size = board_size
        self.entities_dict: Dict[str, List[BaseEntity]] = {}
        self.entity_list: List[BaseEntity] = []
        self.showing_entities: List[BaseEntity] = []
        self.day: int = 0
        self._setup_plot()

    def spawn(self, entity_class: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            entity: BaseEntity = None
            if entity_class == "grass":
                entity = Grass(board_size=self.board_size)
            elif entity_class == "pig":
                entity = Pig(board_size=self.board_size)
            elif entity_class == "fox":
                entity = Fox(board_size=self.board_size)
            (point,) = self.ax.plot(
                [entity.position[0]], [entity.position[1]], "o", color=entity.colour
            )
            entity.point = point

            if self.entities_dict.get(entity_class) is None:
                self.entities_dict[entity_class] = []
            self.entities_dict[entity_class].append(entity)
            self.entity_list.append(entity)
            if isinstance(entity, BaseAnimal):
                self.showing_entities.append(entity)

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
        self.spawn(entity_class="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_class="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_class="fox", number_to_spawn=number_to_spawn)

    def step(self):
        self.day += 1

        self.showing_entities = [entity for entity in self.entity_list if entity.show]

        for animal in self.showing_entities:
            animal.step(self.entity_list)

        if self.day % 1 == 0:
            spawn_plants = random.randrange(100) <= 2
            if spawn_plants:
                number_to_spawn = random.choice(range(1, 4))
                self.spawn_plants(number_to_spawn=number_to_spawn)

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
                print(
                    f"Grass: {len([e for e in self.entities_dict.get('grass', []) if e.alive])}, Pigs: {len([e for e in self.entities_dict.get('pig', []) if e.alive])}, Foxes: {len([e for e in self.entities_dict.get('fox', []) if e.alive])}"
                )

        ani = animation.FuncAnimation(self.fig, update_plot, interval=20)
        plt.show()
