from typing import List

import numpy as np

from entities.BaseEntity import BaseEntity


class WorldArea:
    def __init__(
        self, area_radius: int, entities: List[BaseEntity], position: np.ndarray
    ):
        self.area_radius = area_radius
        self.position = position
        self.entities_in_radius: List[BaseEntity] = self.set_entities_in_radius(
            entities
        )

    def add_entity(self, entity: BaseEntity):
        self.entities_in_radius.append(entity)

    def set_entities_in_radius(self, entities: List[BaseEntity]):
        entities_in_radius: List[BaseEntity] = []
        for entity in entities:
            if self.is_entity_in_radius(entity):
                entities_in_radius.append(entity)
        entities_in_radius = sorted(
            entities_in_radius, key=lambda x: x.distance_from_point(self.position)
        )
        return entities_in_radius

    def is_entity_in_radius(self, entity: BaseEntity):
        return entity.distance_from_point(self.position) <= self.area_radius

    def update(self, entities: List[BaseEntity], step_no: int):
        if step_no % 1 == 0:
            self.entities_in_radius = self.set_entities_in_radius(entities)
