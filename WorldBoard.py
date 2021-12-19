import random
import time
from copy import copy
from typing import Tuple, List, Dict

import matplotlib
import matplotlib.pyplot as plt

# import ray
import numpy as np

# from joblib import Parallel, delayed
from matplotlib import animation

from Genes import Genes
from WorldArea import WorldArea, update_batch_of_world_areas
from entities import Fox, Grass, Pig
from entities.BaseAnimal import BaseAnimal
from entities.BaseEntity import BaseEntity
from optimised_functions import calculate_all_distance_between_points

matplotlib.use("TkAgg")
# matplotlib.use('WebAgg')
random.seed(1)


# ray.init(num_cpus=2)


class WorldBoard:
    def __init__(
        self,
        board_size: Tuple[float, float] = (100.0, 100.0),
        initial_populations: Dict[str, int] = None,
        show_plot: bool = True,
    ):
        self.board_size = np.array(board_size)
        self.entities_dict: Dict[str, List[BaseEntity]] = {}
        self.entity_list: List[BaseEntity] = []
        self.showing_animals: List[BaseEntity] = []
        self.step_no: int = 0
        self.show_plot = show_plot
        if show_plot:
            self._setup_plot()
        if initial_populations is None:
            initial_populations = dict(grass=2000, pig=100, fox=0)
        self.spawn_all_entities(initial_populations)

    def spawn(self, entity_class: str, number_to_spawn: int = 100):
        for i in range(number_to_spawn):
            entity: BaseEntity = None
            if entity_class == "grass":
                entity = Grass(board_size=self.board_size)
            elif entity_class == "pig":
                entity = Pig(board_size=self.board_size)
            elif entity_class == "fox":
                entity = Fox(board_size=self.board_size)
            if hasattr(self, "ax"):
                (point,) = self.ax.plot(
                    [entity.position[0]],
                    [entity.position[1]],
                    "x" if entity_class == "grass" else "o",
                    color=entity.colour,
                    markersize=80 / (self.board_size[0] ** 0.5),
                )
                entity.point = point

            if self.entities_dict.get(entity_class) is None:
                self.entities_dict[entity_class] = []
            self.entities_dict[entity_class].append(entity)
            self.entity_list.append(entity)
            if isinstance(entity, BaseAnimal):
                self.showing_animals.append(entity)

    def spawn_all_entities(self, initial_populations: Dict[str, int]):
        s = time.time()
        self.initial_populations = initial_populations
        self.spawn_plants(number_to_spawn=initial_populations["grass"])
        self.spawn_pigs(number_to_spawn=initial_populations["pig"])
        self.spawn_foxes(number_to_spawn=initial_populations["fox"])
        print(f"Time to Spawn entities: {time.time() - s}")
        self.set_world_areas()

    def spawn_child_animal(
        self, parent_animal: BaseAnimal, entity_class: str, genes: Genes
    ):
        """
        Spawns an animal with the given genes
        """
        animal: BaseAnimal = None
        if entity_class == "fox":
            animal = Fox(board_size=self.board_size, genes=genes)
        elif entity_class == "pig":
            animal = Pig(board_size=self.board_size, genes=genes)

        # set animal to same location as the parent
        animal.position = parent_animal.position

        # give a chance for the parent to move away from the child
        animal.skip_action_counter = 40
        if hasattr(self, "ax"):
            (point,) = self.ax.plot(
                [animal.position[0]],
                [animal.position[1]],
                "o",
                color=animal.colour,
                markersize=80 / (self.board_size[0] ** 0.5),
            )
            animal.point = point
        other_entities = copy(self.entity_list)
        other_entities.remove(animal)
        world_area = WorldArea(
            area_radius=animal.vision_radius,
            entities=other_entities,
            position=animal.position,
            board_size=self.board_size,
        )
        animal.world_area = world_area
        self.entity_list.append(animal)
        self.entities_dict[entity_class].append(animal)
        if isinstance(animal, BaseAnimal):
            self.showing_animals.append(animal)

    def set_world_areas(self):
        s = time.time()
        for entity in self.showing_animals:
            other_entities = copy(self.entity_list)
            other_entities.remove(entity)
            world_area = WorldArea(
                area_radius=entity.vision_radius,
                entities=other_entities,
                position=entity.position,
                board_size=self.board_size,
            )
            entity.world_area = world_area
        print(f"Set World areas in: {time.time() - s}")

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_class="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_class="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_class="fox", number_to_spawn=number_to_spawn)

    def step(self):
        # TODO - Investigate parallel choose_action events
        self.step_no += 1

        s = time.time()
        self.showing_animals = [
            entity
            for entity in self.entity_list
            if entity.show and isinstance(entity, BaseAnimal)
        ]

        for entity in self.showing_animals:
            del entity.world_area.entities_in_radius

        # calculate all distances between entities
        positions = np.array([entity.position for entity in self.entity_list])
        all_distances = calculate_all_distance_between_points(
            positions, self.board_size
        )
        # all_rank_order_of_closest_entities = np.argsort(all_distances, axis=1)
        number_of_showing_animals = len(self.showing_animals)
        batch_size = 1_000
        batches = [
            self.showing_animals[i : i + batch_size]
            for i in range(0, number_of_showing_animals, batch_size)
        ]

        entity_list = np.array(self.entity_list)
        showing_animals = np.array(self.showing_animals)
        world_areas = []
        tasks = []
        for batch in batches:
            batch_distances = []
            for animal in batch:
                animal_distance_index = np.where(positions == animal.position)[0][0]
                animal_distances = all_distances[animal_distance_index]
                batch_distances.append(animal_distances)
            batch_distances = np.array(batch_distances)
            batch_world_areas = update_batch_of_world_areas(
                batch,
                self.entity_list,
                self.showing_animals,
                self.step_no,
                batch_distances,
            )
            world_areas.extend(batch_world_areas)
        # batches_world_areas = []
        # batches_world_areas.extend(Parallel(n_jobs=5)(
        #     delayed(update_batch_of_world_areas)(batch, self.entity_list, self.showing_animals, self.step_no,
        #                                          [all_distances[np.where(positions == animal.position)[0][0]] for animal
        #                                           in batch]) for batch in batches))
        #     tasks.append(update_batch_of_world_areas.remote(batch, entity_list, showing_animals, self.step_no, batch_distances))
        # batches_world_areas = ray.get(tasks)
        # for batch_world_areas in batches_world_areas:
        #     world_areas.extend(batch_world_areas)

        for animal, world_area in zip(self.showing_animals, world_areas):
            animal.world_area = world_area

        animal_update_world_area_time = time.time() - s

        s = time.time()
        for animal in self.entity_list:
            output = animal.step(self.entity_list, self.showing_animals, self.step_no)
            if output is not None:
                self.spawn_child_animal(animal, animal.entity_class, output)
        animal_action_time = time.time() - s

        s = time.time()
        if self.step_no % 1 == 0:
            # TODO: Make this a function and improve the mechanics of grass spawning
            base_number_to_spawn = max(
                self.initial_populations["grass"] // 100, 1
            ) * int(float(self.board_size[0] * self.board_size[1] / 100 ** 2) ** 0.5)
            spawn_plants = random.randrange(100) <= 5
            if spawn_plants:
                number_to_spawn = random.choice(
                    list(range(base_number_to_spawn, 4 * base_number_to_spawn))
                )
                self.spawn_plants(number_to_spawn=number_to_spawn)
        plant_spawn_time = time.time() - s
        print(
            f"Animal update world area time: {animal_update_world_area_time}, Animals action time: {animal_action_time:.3f}, Spawn plants time: {plant_spawn_time:.3f}"
        )

    def _setup_plot(self):
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot()

    def run(self):
        if self.show_plot:
            self.plot_world()
        else:
            self.plotless_world()

    def plotless_world(self):
        global stationary_time
        stationary_time = time.time()

        while True:
            s = time.time()
            self.step()
            print(f"Step time: {time.time() - s}")
            if self.step_no % 10 == 0:
                time_taken = time.time() - stationary_time
                avg_time = 1000 * (time_taken / self.step_no)
                print(
                    f"day: {self.step_no}, time: {time_taken}, average: {avg_time:.2f}ms"
                )
                print(
                    f"Grass: {len([e for e in self.entities_dict.get('grass', []) if e.alive])}, Pigs: {len([e for e in self.entities_dict.get('pig', []) if e.alive])}, Foxes: {len([e for e in self.entities_dict.get('fox', []) if e.alive])}"
                )
            if self.step_no > 10:
                exit(0)

    def plot_world(self):
        """
        Plots all the entities by their position on a matplotlib graph
        :return:
        """
        self.ax.set_xlim(0, self.board_size[0])
        self.ax.set_ylim(0, self.board_size[1])

        global stationary_time
        stationary_time = time.time()

        def update_plot(n):
            s = time.time()
            self.step()
            step_time = time.time() - s
            s = time.time()
            if self.step_no % 1 == 0:
                for entity in self.entity_list:
                    point = entity.point
                    if entity.show:
                        if isinstance(entity, BaseAnimal):
                            point.set_data([entity.position[0], entity.position[1]])
                        point._color = entity.colour
                    else:
                        point.set_data([-1, -1])
            else:
                for entity in self.showing_animals:
                    point = entity.point
                    if entity.show:
                        point.set_data([entity.position[0], entity.position[1]])
                        point._color = entity.colour
                    else:
                        point.set_data([-1, -1])
            plot_time = time.time() - s
            print(
                f"Step time: {step_time:.3f} Plot time: {plot_time:.3f}, Total time: {step_time + plot_time:.3f}"
            )
            if self.step_no % 10 == 0:
                time_taken = time.time() - stationary_time
                avg_time = 1000 * (time_taken / self.step_no)
                print(
                    f"step_no: {self.step_no}, time: {time_taken}, average: {avg_time:.2f}ms"
                )
                print(
                    f"Grass: {len([e for e in self.entities_dict.get('grass', []) if e.alive])}, Pigs: {len([e for e in self.entities_dict.get('pig', []) if e.alive])}, Foxes: {len([e for e in self.entities_dict.get('fox', []) if e.alive])}"
                )

            if self.step_no > 10:
                exit(0)

        ani = animation.FuncAnimation(self.fig, update_plot, interval=100)
        plt.show()
