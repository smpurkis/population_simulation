import random

import numpy as np

from entities.BaseEntity import BaseEntity


class BaseAnimal(BaseEntity):
    def __init__(self, speed: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = speed

    def move(self):
        move_distance = random.uniform(0, self.speed)
        random_angle = random.randint(0, 180)
        x_step = move_distance * np.cos(np.deg2rad(random_angle))
        y_step = move_distance * np.sin(np.deg2rad(random_angle))
        self.position[0] += x_step
        self.position[1] += y_step
        return self.position
