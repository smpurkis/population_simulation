from typing import List

from entities.BaseEntity import BaseEntity


class WorldArea:
    def __init__(self, area_radius: int):
        self.area_radius = area_radius
        self.objects_in_sight: List[BaseEntity] = []
        self.objects_in_earshot: List[BaseEntity] = []
