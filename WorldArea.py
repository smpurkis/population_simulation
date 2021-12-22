from copy import copy
from typing import List, Dict, Union

import numpy as np

from entities.BaseEntity import BaseEntity

from optimised_functions import distance_between_points_parallel


class WorldArea:
    def __init__(
            self,
            area_radius: int,
            entity: BaseEntity,
            entities_dict,
            position: np.ndarray,
            board_size: np.ndarray,
    ):
        self.entity = entity
        self.area_radius = area_radius
        self.position = position
        self.board_size = board_size
        self.closest_entities_by_class: Dict[
            str, Dict[str, Union[int, BaseEntity]]] = self.set_closest_entities_by_class(entities_dict)

    def set_closest_entities_by_class(
            self,
            entities_dict: Dict[str, List[BaseEntity]]
    ) -> Dict[str, Dict[str, Union[int, BaseEntity]]]:
        """
        Calculates the closest entity by class
        """
        closest_entities_by_class = {}
        classes_in_entities = set(entities_dict.keys())
        for entity_class in classes_in_entities:
            entities_of_class = [e for e in copy(entities_dict[entity_class]) if e.alive]
            if len(entities_of_class) == 0:
                continue
            if entity_class == self.entity.entity_class:
                try:
                    entities_of_class.remove(self.entity)
                except:
                    pass
            positions = np.array([e.position for e in entities_of_class])
            distances = distance_between_points_parallel(
                self.position, positions, self.board_size
            )
            min_index = distances.argmin()
            dist = distances[min_index]
            if dist <= self.area_radius:
                closest_entities_by_class[entity_class] = {
                    "distance": dist,
                    "entity": entities_of_class[min_index]
                }
        return closest_entities_by_class

    def update(
            self,
            other_entities: List[BaseEntity],
            entities_dict: Dict[str, List[BaseEntity]]
    ):
        self.closest_entities_by_class = self.set_closest_entities_by_class(entities_dict)

