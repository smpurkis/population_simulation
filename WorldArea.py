from copy import copy
from typing import List, Dict, Union

import numpy as np

from entities.BaseEntity import BaseEntity
from optimised_functions import distance_between_points_vectorized


def calculate_world_areas(
    animals,
    entities,
    all_distances,
):
    world_areas = []
    entity_classes_set = {e.entity_class for e in entities if e.alive}
    for i, animal in enumerate(animals):
        distances = all_distances[i]

        world_area = animal.world_area.set(entities, entity_classes_set, distances)
        world_areas.append(world_area)
    return world_areas


class WorldArea:
    def __init__(
        self,
        area_radius: int,
        entity: BaseEntity,
        position: np.ndarray,
        board_size: np.ndarray,
    ):
        self.area_radius = area_radius
        self.position = position
        self.board_size = board_size
        self.entity = entity

    def set_closest_entities(self, entity_classes_set, entities, distances):
        """
        Calculates the closest entity
        """
        closest_entities_by_class = {}
        if len(distances) == 0:
            positions = np.array([e.position for e in entities if e.alive])
            distances = distance_between_points_vectorized(
                self.entity.position, positions, self.board_size
            )
        for entity_class in entity_classes_set:
            nearest_class_entity = None
            nearest_dist = self.area_radius + 1
            for i, e in enumerate(entities):
                if e.entity_class != entity_class:
                    continue
                if e == self.entity:
                    continue
                else:
                    dist = distances[i]
                    if nearest_dist is None or nearest_class_entity is None:
                        nearest_dist = dist
                        nearest_class_entity = e
                    elif dist < nearest_dist:
                        nearest_dist = dist
                        nearest_class_entity = e
            if nearest_dist <= self.area_radius:
                closest_entities_by_class[entity_class] = {
                    "distance": nearest_dist,
                    "entity": nearest_class_entity,
                }
        return closest_entities_by_class

    def set(self, entities, entity_classes_set, distances):
        self.closest_entities_by_class = self.set_closest_entities(
            entity_classes_set, entities, distances
        )
        return self
