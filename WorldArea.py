from typing import List

import numpy as np

from entities.BaseEntity import BaseEntity

# import ray

# @ray.remote
def update_batch_of_world_areas(
    animals, entity_list, showing_animals, step_no, batch_distances_of_entities, batch_rank_order_of_closest_entities
):
    world_areas = []
    for i, animal in enumerate(animals):
        distances_of_entities = batch_distances_of_entities[i]

        rank_order_of_closest_entities = batch_rank_order_of_closest_entities[i]
        # rank_order_of_closest_entities = np.argsort(distances_of_entities)
        # rank_order_of_closest_entities = np.arange(len(distances_of_entities))

        world_area = animal.world_area.update(
            entity_list,
            showing_animals,
            step_no,
            distances_of_entities,
            rank_order_of_closest_entities,
        )
        world_areas.append(world_area)
    return world_areas


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

    def add_entity(self, entity: BaseEntity):
        self.entities_in_radius.append(entity)

    def set_entities_in_radius(self, entities: List[BaseEntity]) -> List[BaseEntity]:
        entities_in_radius: List[BaseEntity] = []
        for entity in entities:
            if self.is_entity_in_radius(entity):
                entities_in_radius.append(entity)
        entities_in_radius = sorted(
            entities_in_radius, key=lambda x: x.distance_from_point(self.position)
        )
        return entities_in_radius

    def set_entities_in_radius_vec(
        self,
        entities: List[BaseEntity],
        distances: np.ndarray,
        rank_order_of_closest_entities: np.ndarray,
    ) -> List[BaseEntity]:
        entities_by_distance = [
            (distances[i], entities[i]) for i in rank_order_of_closest_entities
        ]
        cut_off_index = 0
        for index, dist_ent in enumerate(entities_by_distance[1:]):
            if dist_ent[0] > self.area_radius:
                cut_off_index = index
                break
        entities_in_radius = [
            dist_ent[1] for dist_ent in entities_by_distance[1:cut_off_index]
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

    def is_entity_in_radius(self, entity: BaseEntity):
        return entity.distance_from_point(self.position) <= self.area_radius

    def update(
        self,
        entities: List[BaseEntity],
        showing_entities: List[BaseEntity],
        step_no: int,
        distances: np.ndarray,
        rank_order_of_closest_entities: np.ndarray,
    ):
        if step_no % 1 == 0:
            self.entities_in_radius = self.set_entities_in_radius_vec(
                entities, distances, rank_order_of_closest_entities
            )
            # self.entities_in_radius = self.set_entities_in_radius(entities)
        else:
            self.entities_in_radius = self.update_entities_in_radius(showing_entities)
        return self
