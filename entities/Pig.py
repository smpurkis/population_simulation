from entities import Grass
from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(self, colour: str = "pink", speed: float = 0.5, *args, **kwargs):
        super().__init__(colour, speed, *args, **kwargs)
        self.food_type = Grass

    def move(self):
        entity = self.find_nearest_entity(entity_type=self.food_type)
        if entity is not None:
            if isinstance(entity, Grass):
                self.move_towards(entity)
        else:
            self.random_move()

    def eat(self):
        entity = self.find_nearest_entity(entity_type=self.food_type)
        if entity is not None:
            if isinstance(entity, Grass):
                self.eat_entity(entity)

    def eat_entity(self, entity):
        if self.distance_from_entity(entity) < self.eat_radius:
            self.hunger += entity.health
