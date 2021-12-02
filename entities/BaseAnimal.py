import random
from typing import List

import numpy as np

from entities.BaseEntity import BaseEntity


class BaseAnimal(BaseEntity):
    def __init__(self, colour: str, speed: float = 0, *args, **kwargs):
        super().__init__(colour, *args, **kwargs)
        self.speed = speed
        self._max_speed = speed
        self.hunger = 100
        self.health = 100

    def move(self):
        """
        Moves the animal in a random direction
        :return:
        """
        move_distance = random.uniform(0, self.speed)
        random_angle = random.randint(90, 100)
        x_step = move_distance * np.cos(np.deg2rad(random_angle))
        y_step = move_distance * np.sin(np.deg2rad(random_angle))

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

    def update_health(self):
        """
        Checks if the animal is healthy
        :return:
        """
        if self.hunger <= 0:
            self.alive = False
            self.colour = "black"
            self.speed = 0
            if self.death_age < 50:
                self.death_age += 1
        elif self.hunger < 50:
            self.speed = 0.5 * self._max_speed
        if self.death_age >= 50:
            self.show = False
        elif self.death_age > 25:
            self.colour = "grey"

    def step(self):
        """
        Performs the step of the animal
        :return:
        """
        self.move()
        self.update_hunger()
        self.update_health()

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
