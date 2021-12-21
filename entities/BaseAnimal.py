import math
import random
import time
from typing import List

import numpy as np

from Genes import Genes, combined_genes
from entities.BaseEntity import BaseEntity
from optimised_functions import deg2rad, rad2deg, angle_between, correct_boundaries


class BaseAnimal(BaseEntity):
    """
    Base class for all animals, inherits from BaseEntity
    """

    def __init__(
        self,
        entity_class,
        colour: str,
        base_speed: float = 0,
        food_class: str = None,
        base_eating_penalty: int = 0,
        base_vision_radius: int = 10,
        base_health: int = 100,
        base_hunger: int = 100,
        base_lifespan: int = 200,
        base_reproduce_cycle: int = 50,
        genes: Genes = None,
        *args,
        **kwargs,
    ):
        super().__init__(entity_class, colour, *args, **kwargs)
        self.food_class = food_class
        self.eat_radius = 0.2
        self.skip_action_counter = 0
        self.reproduce_ready = False
        self.reproduce_counter = 0
        self.days_to_birth = None
        self.with_child = False
        self.child_genes: Genes = None
        self.genes: Genes = genes if genes is not None else Genes()

        self._base_speed = base_speed
        self._max_speed = 1.5 * base_speed

        self._base_vision_radius = base_vision_radius
        self._max_vision_radius = 100

        self._base_eating_penalty = base_eating_penalty
        self._max_eating_penalty = 50

        self._base_hunger = base_hunger
        self._max_hunger = 500
        self._base_hunger_rate = 5
        self.hunger_rate = self._base_hunger_rate

        self._base_health = base_health
        self._max_health = 1_000

        self._base_lifespan = base_lifespan
        self._max_lifespan = 10 * base_lifespan

        self._base_reproduce_cycle = base_reproduce_cycle
        self._max_reproduce_cycle = 5 * base_reproduce_cycle
        self.reproduce_cooldown = base_reproduce_cycle

        self.initial_attributes()

    def initial_attributes(self):
        """
        Set the attributes of the animal, altered by its genes
        :return:
        """
        self.speed = min(self.genes.speed * self._base_speed, self._max_speed)
        self.vision_radius = min(
            self.genes.vision_radius * self._base_vision_radius, self._max_vision_radius
        )
        self.eating_penalty = min(
            self.genes.eating_penalty * self._base_eating_penalty,
            self._max_eating_penalty,
        )
        self.hunger = min(self.genes.hunger * self._base_hunger, self._max_hunger)
        self.health = min(self.genes.health * self._base_health, self._max_health)
        self.lifespan = min(
            self.genes.lifespan * self._base_lifespan, self._max_lifespan
        )
        self.reproduce_cycle = min(
            self.genes.reproduce_cycle * self._base_reproduce_cycle,
            self._max_reproduce_cycle,
        )

    def random_move(self):
        """
        Moves the animal in a random direction
        :return:
        """
        move_distance = random.uniform(0, self.speed)
        random_angle = float(random.randint(0, 360))
        angle_rad = deg2rad(random_angle)
        x_step = move_distance * math.cos(angle_rad)
        y_step = move_distance * math.sin(angle_rad)

        new_position = np.array([self.position[0] + x_step, self.position[1] + y_step])
        # new_position = [self.position[0] + x_step, self.position[1] + y_step]
        self.position = self.correct_boundaries(new_position)

        return self.position

    def move_towards(self, entity: BaseEntity) -> np.ndarray:
        return self.move_towards_position(entity.position)

    def move_towards_position(self, position: np.ndarray) -> np.ndarray:
        """
        Moves the animal towards the position
        :param position:
        :return:
        """
        distance_away = self.distance_from_point(position)
        move_distance = min(self.speed, distance_away)
        angle_rad = deg2rad(self.angle_to(position))
        x_step = move_distance * math.cos(angle_rad)
        y_step = move_distance * math.sin(angle_rad)

        new_position = np.array([self.position[0] + x_step, self.position[1] + y_step])
        # new_position = [self.position[0] + x_step, self.position[1] + y_step]
        self.position = self.correct_boundaries(new_position)

        return self.position

    def update_hunger(self):
        """
        Checks if the animal is hungry
        :return:
        """
        if self.hunger > 0:
            self.hunger -= self.hunger_rate

    def die(self):
        """
        Kills the animal
        :return:
        """
        self.alive = False
        self.colour = "black"
        self.speed = 0
        self.death_age = 1

    def update_status(self):
        """
        Checks if the animal is healthy
        :return:
        """
        self.age += 1

        if self.alive:
            # if the animal's health is less than 0, it dies
            if self.health <= 0:
                self.die()
            elif self.hunger <= 0:
                # if the animals hunger is 0, it starts losing health
                self.health -= 1

            health_penalty_threshold = self._base_hunger * 0.5
            if self.health < health_penalty_threshold:
                # if the animals health is less than 50% max health, it's speed is cut in half
                self.speed = 0.5 * self._base_speed
            elif self.health >= health_penalty_threshold:
                self.speed = self._base_speed
        else:
            # if the animal is dead, increment its death age
            self.update_death_age()
            self.speed = 0

        if self.age > self.lifespan:
            self.die()

        if self.with_child:
            self.speed = 0.5 * self._base_speed
            self.hunger_rate = 2 * self._base_hunger_rate

    def step(
        self,
        entities: List[BaseEntity],
        showing_entities: List[BaseEntity],
        step_no: int,
    ):
        """
        Performs the step of the animal
        :return:
        """
        # s = time.time()
        self.world_area.update(entities, showing_entities, step_no)
        # print(f"Update world area: {time.time() - s:.3f}")
        # s = time.time()
        self.update_status()
        self.update_hunger()
        self.update_reproduction()
        # print(f"Update funcs: {time.time() - s:.3f}")
        if self.skip_action_counter > 0:
            self.skip_action_counter -= 1
        else:
            return self.choose_action()

    def choose_action(self):
        """
        Chooses an action for the animal
        :return:
        """
        s = time.time()
        if self.alive:
            if self.with_child:
                return self.give_birth()
            t = time.time()
            nearest_food_entity = self.find_nearest_entity(entity_class=self.food_class)
            nearest_companion_entity = self.find_nearest_entity(
                entity_class=self.entity_class
            )
            # print(f"Nearest entities time: {time.time() - t:.3f}")
            if (
                nearest_companion_entity is not None
                and self.reproduce_ready
                and self.reproduce_cooldown == 0
            ):
                if (
                    self.distance_from_entity(nearest_companion_entity)
                    < self.eat_radius
                ):
                    self.reproduce_with(nearest_companion_entity)
                else:
                    self.move_towards(nearest_companion_entity)
            elif nearest_food_entity is not None:
                if self.distance_from_entity(nearest_food_entity) < self.eat_radius:
                    self.eat_entity(nearest_food_entity)
                else:
                    self.move_towards(nearest_food_entity)
            else:
                self.random_move()
        # print(f"Choose action time: {time.time() - s}")

    def correct_boundaries(self, new_position):
        return correct_boundaries(new_position, self.board_size)

    def angle_to(self, position):
        """
        Calculates the angle to the position
        :param position:
        :return:
        """
        return angle_between(position, self.position)

    def eat_entity(self, entity: BaseEntity):
        """
        Eats the entity
        gains the health of the entity and sets hunger to base hunger
        :param entity:
        :return:
        """
        self.skip_action_counter = self.eating_penalty
        self.health += entity.health
        self.health = min(self.health, self._max_health)
        self.hunger = self._base_hunger
        entity.die()

    def update_reproduction(self):
        """
        The animal can reproduce if it is older than its reproduce_cycle duration
        :return:
        """
        if self.reproduce_cooldown > 0:
            self.reproduce_cooldown -= 1
        if self.with_child:
            self.days_to_birth -= 1
        else:
            if self.age // self.reproduce_cycle > self.reproduce_counter:
                self.reproduce_ready = True

    def reproduce_with(self, nearest_companion_entity):
        """
        The animal reproduces with the nearest companion animal of the same species
        Their genes are combined and the mating animal becomes pregnant for a duration
        :param nearest_companion_entity:
        :return:
        """
        # TODO: work out logic of how to add to the world board from this class
        self.reproduce_ready = False
        nearest_companion_entity.reproduce_ready = False
        child_genes = combined_genes(self.genes, nearest_companion_entity.genes)
        self.child_genes = child_genes
        self.with_child = True
        self.days_to_birth = self.reproduce_cycle // 5
        self.reproduce_cooldown = self._base_reproduce_cycle
        health_cost = self._base_health // 2
        self.health -= health_cost

    def give_birth(self) -> Genes:
        """
        Gives birth to the child
        :return:
        """
        self.with_child = False
        child_genes = self.child_genes
        self.child_genes = None
        self.days_to_birth = None
        return child_genes
