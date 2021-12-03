import random
from datetime import datetime as dt
from typing import Tuple, Optional, List

from matplotlib.lines import Line2D


class BaseEntity(object):
    def __init__(
        self,
        colour,
        board_size: Tuple[float, float] = (100.0, 100.0),
    ):
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

    def step(self):
        raise NotImplementedError

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
        x_distance = abs(self.position[0] - position[0])
        y_distance = abs(self.position[1] - position[1])
        distance = (x_distance ** 2 + y_distance ** 2) ** 0.5
        return distance

    def find_nearest_entity(self, entity_type=None):
        """
        Find the nearest entity to the current entity
        :param entity_type: find nearest entity of this type
        :return:
        """
        nearest_entity = None
        if entity_type is None:
            if len(self.world_area.entities_in_radius) == 0:
                return None
            return self.world_area.entities_in_radius[0]
        else:
            for entity in [
                e
                for e in self.world_area.entities_in_radius
                if isinstance(e, entity_type)
            ]:
                if nearest_entity is None:
                    nearest_entity = entity
                elif self.distance_from_entity(entity) < self.distance_from_entity(
                    nearest_entity
                ):
                    nearest_entity = entity
            return nearest_entity
