import random
from datetime import datetime as dt
from typing import Tuple, Optional, List

from matplotlib.lines import Line2D


class BaseEntity(object):
    def __init__(
        self,
        entity_class: str = None,
        colour: str = None,
        board_size: Tuple[float, float] = (100.0, 100.0),
    ):
        self.entity_class = entity_class
        self.vision_radius = 0
        self.point = None
        self.colour = colour
        self.board_size = board_size
        self.creation_time = dt.now().time()
        self.age = 0
        self.death_age = 0
        self.show = True
        self.alive = True
        self.position: List[float, float] = self.set_random_position()
        self.point: Optional[Line2D]
        self.world_area = None
        self.health = 100

    def set_random_position(self) -> List[float]:
        """
        Set random position on the board
        :return:
        """
        position = [
            random.uniform(0, self.board_size[0]),
            random.uniform(0, self.board_size[1]),
        ]
        return position

    def update_death_age(self):
        """
        Updates the death age of the animal
        :return:
        """
        # If the entity is dead, increment its death age
        self.death_age += 1

        # hide the entity after 50 steps
        if self.death_age >= 50:
            self.show = False
        elif self.death_age > 25:
            # if entity is halfway through decaying, change colour to grey
            self.colour = "grey"

    def update_status(self):
        """
        Checks if the animal is healthy
        :return:
        """
        if not self.alive:
            self.update_death_age()

    def step(self, entities):
        self.update_status()

    def distance_from_entity(self, entity) -> float:
        """
        Calculate distance between two entities
        :param entity:
        :return:
        """
        return self.distance_from_point(entity.position)

    def distance_from_point(self, position: List[float]) -> float:
        """
        Calculate distance between two points
        :param position:
        :return:
        """
        return self.distance_between_points(self.position, position, self.board_size)

    @staticmethod
    def distance_between_points(
        point_1: List[float], point_2: List[float], board_size: Tuple[float]
    ) -> float:
        """
        Calculates the distance between two points on the board.
        Taking into account wrapping around the board
        :param point_1:
        :param point_2:
        :param board_size:
        :return:
        """
        x_distance = min(
            abs(point_1[0] - point_2[0]), board_size[0] - abs(point_1[0] - point_2[0])
        )
        y_distance = min(
            abs(point_1[1] - point_2[1]), board_size[1] - abs(point_1[1] - point_2[1])
        )
        distance = x_distance + y_distance
        return distance

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
        nearest_entity = None
        if entity_class is None:
            if len(self.world_area.entities_in_radius) == 0:
                return None
            return self.world_area.entities_in_radius[0]
        else:
            for entity in [
                e
                for e in self.world_area.entities_in_radius
                if e.entity_class == entity_class and e.alive
            ]:
                if nearest_entity is None:
                    nearest_entity = entity
                elif self.distance_from_entity(entity) < self.distance_from_entity(
                    nearest_entity
                ):
                    nearest_entity = entity
            return nearest_entity
