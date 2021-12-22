from typing import List, Tuple

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
        self.entities_in_radius: List[BaseEntity] = self.set_entities_in_radius(
            entities
        )

    def set_entities_in_radius(self, other_entities: List[BaseEntity]) -> List[BaseEntity]:
        entities_in_radius = []
        for entity in other_entities:
            dist = entity.distance_from_point(self.position)
            if dist < self.area_radius:
                entities_in_radius.append((dist, entity))
        entities_in_radius = sorted(
            entities_in_radius, key=lambda x: x[0]
        )
        entities_in_radius = [e[1] for e in entities_in_radius]
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

    def is_entity_in_radius(self, entity: BaseEntity):
        return entity.distance_from_point(self.position) <= self.area_radius

    def update(
        self,
        entities: List[BaseEntity],
        showing_entities: List[BaseEntity],
        step_no: int,
    ):
        self.entities_in_radius = self.set_entities_in_radius(entities)
