import random
import time
from typing import Tuple, List, Dict

import matplotlib
import matplotlib.pyplot as plt

# import ray
import cupy as cp

# from joblib import Parallel, delayed
from matplotlib import animation

from Genes import Genes
from WorldArea import WorldArea
from entities import Fox, Grass, Pig
from entities.BaseAnimal import BaseAnimal
from entities.BaseEntity import BaseEntity
from optimised_functions import (
    distance_between_points_vectorized,
    calculate_all_distance_between_animals_and_points_vectorized,
    calculate_all_nearest_ids_to_entity_vectorized,
    calculate_all_distance_between_animals_and_points,
)
from tqdm import tqdm

matplotlib.use("TkAgg")
# matplotlib.use('WebAgg')
random.seed(1)
cupy_datatype = cp.float16

# ray.init(num_cpus=2)


class WorldBoard:
    def __init__(
        self,
        board_size: Tuple[float, float] = (100.0, 100.0),
        initial_populations: Dict[str, int] = None,
        show_plot: bool = True,
    ):
        self.board_size = cp.array(board_size, dtype=cupy_datatype)
        self.entities_dict_by_class: Dict[str, List[BaseEntity]] = {}
        self.entities_dict: Dict[str, BaseEntity] = {}
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
        for i in tqdm(list(range(number_to_spawn))):
            entity: BaseEntity = None
            if entity_class == "grass":
                entity = Grass(board_size=self.board_size)
            elif entity_class == "pig":
                entity = Pig(board_size=self.board_size)
            elif entity_class == "fox":
                entity = Fox(board_size=self.board_size)
            if hasattr(self, "ax"):
                (point,) = self.ax.plot(
                    [entity.position.get()[0]],
                    [entity.position.get()[1]],
                    "x" if entity_class == "grass" else "o",
                    color=entity.colour,
                    markersize=80 / (self.board_size.get()[0] ** 0.5),
                )
                entity.point = point

            if self.entities_dict_by_class.get(entity_class) is None:
                self.entities_dict_by_class[entity_class] = []
            self.entities_dict_by_class[entity_class].append(entity)
            self.entities_dict[entity.id] = entity
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

        self.entity_list.append(animal)
        self.entities_dict[animal.id] = animal
        self.entities_dict_by_class[entity_class].append(animal)
        if isinstance(animal, BaseAnimal):
            self.showing_animals.append(animal)
        positions = cp.array([e.position for e in self.entity_list])
        distances = distance_between_points_vectorized(
            animal.position, positions, self.board_size
        )
        world_area = WorldArea(
            entity=animal,
            area_radius=animal.vision_radius,
            position=animal.position,
            board_size=self.board_size,
        )
        world_area.set(
            distances=distances,
            entities=self.entity_list,
            entity_classes_set={e.entity_class for e in self.entity_list},
        )
        animal.world_area = world_area

    def set_world_areas(self):
        s = time.time()
        for i, entity in tqdm(list(enumerate(self.showing_animals))):
            world_area = WorldArea(
                entity=entity,
                area_radius=entity.vision_radius,
                position=entity.position,
                board_size=self.board_size,
            )
            entity.world_area = world_area
        self.calculate_set_world_areas()
        print(f"Set World areas in: {time.time() - s}")

    def spawn_plants(self, number_to_spawn: int = 10):
        self.spawn(entity_class="grass", number_to_spawn=number_to_spawn)

    def spawn_pigs(self, number_to_spawn: int = 5):
        self.spawn(entity_class="pig", number_to_spawn=number_to_spawn)

    def spawn_foxes(self, number_to_spawn: int = 2):
        self.spawn(entity_class="fox", number_to_spawn=number_to_spawn)

    def calculate_set_world_areas(self):
        t = time.time()
        entity_list = [e for e in self.entity_list if e.alive]
        positions = cp.array([e.position for e in entity_list], dtype=cupy_datatype)
        alive_animals = [e for e in self.showing_animals if e.alive]
        animal_positions = cp.array(
            [e.position for e in self.showing_animals if e.alive], dtype=cupy_datatype
        )
        animal_position_indices = cp.array(
            [cp.array([i, entity_list.index(e)]) for i, e in enumerate(alive_animals)]
        )
        board_size = cp.array(self.board_size, dtype=cupy_datatype)

        p = time.time()
        all_distances = calculate_all_distance_between_animals_and_points_vectorized(
            animal_positions, positions, board_size, animal_position_indices
        )
        # print("all_distances_vect", time.time() - p)
        # p = time.time()
        # all_distances = calculate_all_distance_between_animals_and_points(
        #     animal_positions, positions, self.board_size
        # )
        # print("all_distances", time.time() - p)
        all_distances_time = time.time() - t

        t = time.time()
        # calculate the nearest entity per entity class for each animal vectorized
        animal_entity_ids = cp.array([e.id for e in alive_animals])
        entity_ids = cp.array([e.id for e in entity_list])
        entity_classes = cp.array([e.entity_class_id for e in entity_list])
        area_radiuses = cp.array([e.world_area.area_radius for e in alive_animals])
        (
            nearest_ids_per_entity_class_for_each_animal,
            nearest_distances_per_entity_class_for_each_animal,
        ) = calculate_all_nearest_ids_to_entity_vectorized(
            animal_entity_ids, entity_ids, all_distances, entity_classes, area_radiuses
        )
        # print("calculate_all_nearest_ids_to_entity", time.time() - t)

        t = time.time()
        for animal_nearest_ids_details, animal_nearest_distances_details in zip(
            nearest_ids_per_entity_class_for_each_animal[:],
            nearest_distances_per_entity_class_for_each_animal[:],
        ):
            animal_id = animal_nearest_ids_details.get()[0]
            animal = self.entities_dict[animal_id]
            animal.world_area.set_nearest_ids(
                animal_nearest_ids_details.get()[1:],
                animal_nearest_distances_details.get()[1:],
                self.entities_dict,
            )
        # print("set_nearest_ids", time.time() - t)

    def step(self):
        # TODO - Investigate parallel choose_action events
        self.step_no += 1
        s = time.time()

        self.showing_animals = [
            entity
            for entity in self.entity_list
            if entity.show and isinstance(entity, BaseAnimal)
        ]

        self.calculate_set_world_areas()
        entity_list = [e for e in self.entity_list if e.alive]

        # world_areas = calculate_world_areas(
        #     alive_animals,
        #     entity_list,
        #     all_distances,
        # )

        # for animal, world_area in zip(self.showing_animals, world_areas):
        #     animal.world_area = world_area

        animal_update_world_area_time = time.time() - s

        s = time.time()
        for entity in self.entity_list:
            output = entity.step(entity_list, self.showing_animals)
            if output is not None:
                self.spawn_child_animal(entity, entity.entity_class, output)
        animal_action_time = time.time() - s

        s = time.time()
        if self.step_no % 1 == 0:
            # TODO: Make this a function and improve the mechanics of grass spawning
            base_number_to_spawn = max(
                self.initial_populations["grass"] // 100, 1
            ) * int(float(self.board_size[0] * self.board_size[1] / 100 ** 2) ** 0.5)
            base_number_to_spawn = max(base_number_to_spawn, 1)
            spawn_plants = random.randrange(100) <= 5
            spawn_plants = (
                False if len(self.entities_dict_by_class["grass"]) > 2 else spawn_plants
            )
            if spawn_plants:
                number_to_spawn = random.choice(
                    list(range(base_number_to_spawn, 4 * base_number_to_spawn))
                )
                self.spawn_plants(number_to_spawn=number_to_spawn)
        plant_spawn_time = time.time() - s
        # print(
        #     # f"Distance calculation time: {all_distances_time:.3f}, "
        #     f"Animal world area set time: {animal_update_world_area_time:.3f}, "
        #     f"Animals action time: {animal_action_time:.3f}, "
        #     f"Spawn plants time: {plant_spawn_time:.3f}"
        # )
        o = 0

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
                            point.set_data(
                                [entity.position.get()[0], entity.position.get()[1]]
                            )
                        point._color = entity.colour
                    else:
                        point.set_data([-1, -1])
            else:
                for entity in self.showing_animals:
                    point = entity.point
                    if entity.show:
                        point.set_data(
                            [entity.position.get()[0], entity.position.get()[1]]
                        )
                        point._color = entity.colour
                    else:
                        point.set_data([-1, -1])
            plot_time = time.time() - s
            # print(
            #     f"Step time: {step_time:.3f} Plot time: {plot_time:.3f}, Total time: {step_time + plot_time:.3f}"
            # )
            if self.step_no % 10 == 0:
                time_taken = time.time() - stationary_time
                avg_time = 1000 * (time_taken / self.step_no)
                print(
                    f"step_no: {self.step_no}, time: {time_taken}, average: {avg_time:.2f}ms"
                )
                print(
                    f"Grass: {len([e for e in self.entities_dict_by_class.get('grass', []) if e.alive])}, Pigs: {len([e for e in self.entities_dict_by_class.get('pig', []) if e.alive])}, Foxes: {len([e for e in self.entities_dict_by_class.get('fox', []) if e.alive])}"
                )

            # if self.step_no > 10:
            #     exit(0)

        ani = animation.FuncAnimation(self.fig, update_plot, interval=100, blit=False)
        plt.show()
