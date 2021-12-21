from typing import List, Dict

import numpy as np

from entities.BaseEntity import BaseEntity
from optimised_functions import (
    distance_between_points_parallel,
)


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
        # self.entities_in_radius: List[BaseEntity] = self.set_entities_in_radius(
        #     entities
        # )
        self.closest_entities_by_class: Dict[str, BaseEntity] = self.set_closest_entities_by_class(entities)

    def set_entities_in_radius(self, entities: List[BaseEntity]) -> List[BaseEntity]:
        entities_in_radius: List[BaseEntity] = []
        for entity in entities:
            if self.is_entity_in_radius(entity):
                entities_in_radius.append(entity)
        entities_in_radius = sorted(
            entities_in_radius, key=lambda x: x.distance_from_point(self.position)
        )
        return entities_in_radius

    def set_entities_in_radius_parallel(
            self, entities: List[BaseEntity]
    ) -> List[BaseEntity]:
        positions = np.array([e.position for e in entities])
        area_radius = self.area_radius
        distances_sorted, last_index_in_radius = distance_between_points_parallel(
            self.position, positions, self.board_size, area_radius
        )
        entities_in_radius = [
            entities[i] for i in distances_sorted if i < last_index_in_radius
        ]
        return entities_in_radius

    def set_entities_in_radius_vec(
            self, entities: List[BaseEntity]
    ) -> List[BaseEntity]:
        positions = np.array([e.position for e in entities])
        distances = distance_between_points_vectorized(
            self.position, positions, self.board_size
        )
        distances_entities = sorted(zip(distances, entities), key=lambda x: x[0])
        cut_off_index = 0
        for index, dist_ent in enumerate(distances_entities):
            if dist_ent[0] > self.area_radius:
                cut_off_index = index
                break
        entities_in_radius = [
            dist_ent[1] for dist_ent in distances_entities[:cut_off_index]
        ]
        return entities_in_radius

    def update_entities_in_radius(
            self, showing_entities: List[BaseEntity]
    ) -> List[BaseEntity]:
        entities_in_radius: List[BaseEntity] = []
        for entity in showing_entities:
            if self.is_entity_in_radius(entity):
                entities_in_radius.append(entity)
        entities_in_radius = sorted(
            entities_in_radius, key=lambda x: x.distance_from_point(self.position)
        )
        return entities_in_radius

    def set_closest_entities_by_class(self, entities: List[BaseEntity]) -> Dict[str, BaseEntity]:
        closest_entities_by_class = {}
        classes_in_entities = set([e.entity_class for e in entities if e.alive])
        for entity_class in classes_in_entities:
            entities_of_class = [e for e in entities if e.entity_class == entity_class if e.alive]
            positions = np.array([e.position for e in entities_of_class])
            distances = distance_between_points_vectorized(
                self.position, positions, self.board_size
            )
            min_index = distances.argmin()
            dist = distances[min_index]
            if dist <= self.area_radius:
                closest_entities_by_class[entity_class] = {
                    "distance": distances[min_index],
                    "entity": entities_of_class[min_index]
                }
        return closest_entities_by_class

    def is_entity_in_radius(self, entity: BaseEntity):
        return entity.distance_from_point(self.position) <= self.area_radius

    def update(
            self,
            entities: List[BaseEntity],
            showing_entities: List[BaseEntity],
            step_no: int,
    ):
        # if step_no % 1 == 0:
        #     self.entities_in_radius = self.set_entities_in_radius(entities)
        # else:
        #     self.entities_in_radius = self.update_entities_in_radius(showing_entities)
        self.closest_entities_by_class = self.set_closest_entities_by_class(entities)
