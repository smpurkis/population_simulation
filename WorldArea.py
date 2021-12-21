from typing import List, Dict, Union

import numpy as np

from entities.BaseEntity import BaseEntity


def distance_between_points_vectorized(
        entity_position: np.ndarray, positions: np.ndarray, board_size: np.ndarray
) -> np.ndarray:
    # pythran export distance_between_points_vectorized(float [], float [], float [])
    abs_diff = np.abs(positions - entity_position)

    x_distance = np.amin(
        np.array([abs_diff[:, 0], board_size[0] - abs_diff[:, 0]]), axis=0
    )
    y_distance = np.amin(
        np.array([abs_diff[:, 1], board_size[1] - abs_diff[:, 1]]), axis=0
    )
    distances = np.sqrt(x_distance ** 2 + y_distance ** 2)
    return distances


class WorldArea:
    def __init__(
            self,
            area_radius: int,
            entities: List[BaseEntity],
            position: np.ndarray,
            board_size: np.ndarray,
    ):
        self.area_radius = area_radius
        self.position = position
        self.board_size = board_size
        self.closest_entities_by_class: Dict[
            str, Dict[str, Union[int, BaseEntity]]] = self.set_closest_entities_by_class(entities)

    def set_closest_entities_by_class(
            self,
            other_entities: List[BaseEntity]
    ) -> Dict[str, Dict[str, Union[int, BaseEntity]]]:
        """
        Calculates the closest entity by class
        """
        closest_entities_by_class = {}
        classes_in_entities = set([e.entity_class for e in other_entities if e.alive])
        for entity_class in classes_in_entities:
            entities_of_class = [e for e in other_entities if e.entity_class == entity_class if e.alive]
            positions = np.array([e.position for e in entities_of_class])
            distances = distance_between_points_vectorized(
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

    def is_entity_in_radius(self, entity: BaseEntity):
        return entity.distance_from_point(self.position) <= self.area_radius

    def update(
            self,
            other_entities: List[BaseEntity],
            showing_entities: List[BaseEntity],
            step_no: int,
    ):
        self.closest_entities_by_class = self.set_closest_entities_by_class(other_entities)

