import random
from datetime import datetime as dt
from typing import Tuple, Optional

import numpy as np
from matplotlib.lines import Line2D

from optimised_functions import distance_between_points


class BaseEntity(object):
    """
    Base class for all entities.
    """

    def __init__(
        self,
        entity_class: str = None,
        colour: str = None,
        board_size: Tuple[float] = (100.0, 100.0),
    ):
        self.id = random.randint(1, 100_000_000_000_000)
        self.entity_class = entity_class
        self.vision_radius = 0
        self.point = None
        self.colour = colour
        self.board_size = np.array(board_size)
        # self.board_size = board_size
        self.creation_time = dt.now().time()
        self.age = 0
        self.death_age = 0
        self.show = True
        self.alive = True
        self.position = self.set_random_position()
        self.point: Optional[Line2D]
        self.world_area = None
        self.health = 50
        self.lifespan = 200

    def set_random_position(self) -> np.ndarray:
        """
        Set random position on the board
        :return:
        """
        position = np.array(
            [
                random.uniform(0, self.board_size[0]),
                random.uniform(0, self.board_size[1]),
            ]
        )
        return position

    def update_death_age(self):
        """
        Updates the death age of the animal
        :return:
        """
        # If the entity is dead, increment its death age
        self.death_age += 1

        # hide the entity after 50 steps
        if self.death_age >= 20:
            self.show = False
        elif self.death_age > 10:
            # if entity is halfway through decaying, change colour to grey
            self.colour = "grey"

    def update_status(self):
        """
        Checks if the animal is healthy
        :return:
        """
        self.age += 1
        if self.alive:
            if self.age >= self.lifespan:
                self.die()
        else:
            self.update_death_age()

    def step(self, entities, entities_dict):
        """
        Takes the next step for this animal
        :param entities:
        :return:
        """
        self.update_status()

    def distance_from_entity(self, entity) -> float:
        """
        Calculate distance between two entities
        :param entity:
        :return:
        """
        return self.distance_from_point(entity.position)

    def distance_from_point(self, position: np.ndarray) -> float:
        """
        Calculate distance between two points
        :param position:
        :return:
        """
        return distance_between_points(self.position, position, self.board_size)

    def die(self):
        """
        Kills the animal
        :return:
        """
        self.alive = False
        self.colour = "black"
        self.speed = 0
        self.death_age = 1

    def find_nearest_entity(self, entity_class=None):
        """
        Find the nearest entity to the current entity
        :param entity_class: find nearest entity of this type
        :return:
        """
        if entity_class is None:
            nearest_entity_with_distance = None
            for entity_with_distance in self.world_area.closest_entities_by_class.items():
                if nearest_entity_with_distance is None:
                    nearest_entity_with_distance = entity_with_distance
                else:
                    if entity_with_distance["distance"] < nearest_entity_with_distance["distance"]:
                        nearest_entity_with_distance = entity_with_distance
            return nearest_entity_with_distance.get("entity", None)
        else:
            return self.world_area.closest_entities_by_class.get(entity_class, {}).get("entity", None)
