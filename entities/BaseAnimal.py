import random
from typing import List

import numpy as np

from entities.BaseEntity import BaseEntity


class BaseAnimal(BaseEntity):
    def __init__(
        self,
        entity_class,
        colour: str,
        speed: float = 0,
        food_class: str = None,
        *args,
        **kwargs
    ):
        super().__init__(entity_class, colour, *args, **kwargs)
        self.food_class = food_class
        self.speed = speed
        self._max_speed = speed
        self.hunger = 100
        self.vision_radius = 100
        self.eat_radius = 1

    def random_move(self):
        """
        Moves the animal in a random direction
        :return:
        """
        move_distance = random.uniform(0, self.speed)
        random_angle = random.randint(0, 360)
        x_step = move_distance * np.cos(np.deg2rad(random_angle))
        y_step = move_distance * np.sin(np.deg2rad(random_angle))

        new_position = [self.position[0] + x_step, self.position[1] + y_step]
        self.position = self.correct_boundaries(new_position)

        return self.position

    def move_towards(self, entity: BaseEntity):
        return self.move_towards_position(entity.position)

    def move_towards_position(self, position: List[float]):
        """
        Moves the animal towards the position
        :param position:
        :return:
        """
        distance_away = self.distance_from_point(position)
        move_distance = min(self.speed, distance_away)
        x_step = move_distance * np.cos(np.deg2rad(self.angle_to(position)))
        y_step = move_distance * np.sin(np.deg2rad(self.angle_to(position)))

        new_position = [self.position[0] + x_step, self.position[1] + y_step]
        self.position = self.correct_boundaries(new_position)

        return self.position

    def update_hunger(self):
        """
        Checks if the animal is hungry
        :return:
        """
        if self.hunger > 0:
            self.hunger -= 1

    def die(self):
        """
        Kills the animal
        :return:
        """
        self.alive = False
        self.colour = "black"
        self.speed = 0
        self.death_age = 1

    def update_health(self):
        """
        Checks if the animal is healthy
        :return:
        """
        # If the animal is dead, increment it's death age
        if not self.alive:
            self.death_age += 1

            # hide the entity after 50 steps
            if self.death_age >= 50:
                self.show = False
            elif self.death_age > 25:
                self.colour = "grey"

        # If the animal's health is less than 0, it dies
        if self.health == 0 and self.alive:
            self.die()
        elif self.hunger <= 0 and self.alive:
            # if the animals hunger is zero, it starts losting health
            self.health -= 1
        elif self.hunger < 50:
            # if the animals hunger is less than 50, it's speed is cut in half
            self.speed = 0.5 * self._max_speed

    def step(self, entities: List[BaseEntity]):
        """
        Performs the step of the animal
        :return:
        """
        self.world_area.update(entities)
        self.update_health()
        self.update_hunger()
        self.choose_action()

    def choose_action(self):
        """
        Chooses an action for the animal
        :return:
        """
        entity = self.find_nearest_entity(entity_class=self.food_class)
        if entity is not None:
            if self.distance_from_point(entity.position) < self.eat_radius:
                self.eat_entity(entity)
            else:
                self.move_towards(entity)
        else:
            self.random_move()

    def correct_boundaries(self, new_position: List[float]) -> List[float]:
        """
        Checks if the new position is valid
        Ensures it wraps the position
        :param new_position:
        :return:
        """
        if new_position[0] < 0:
            new_position[0] = self.board_size[0] - 1
        elif new_position[0] >= self.board_size[0]:
            new_position[0] = 0
        if new_position[1] < 0:
            new_position[1] = self.board_size[1] - 1
        elif new_position[1] >= self.board_size[1]:
            new_position[1] = 0
        return new_position

    def angle_to(self, position):
        """
        Calculates the angle to the position
        :param position:
        :return:
        """
        x_diff = position[0] - self.position[0]
        y_diff = position[1] - self.position[1]
        angle = np.rad2deg(np.arctan2(y_diff, x_diff))
        return angle

    def eat_entity(self, entity: BaseEntity):
        self.hunger += entity.health
        entity.die()
