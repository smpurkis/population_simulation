from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "pig",
        colour: str = "pink",
        base_speed: float = 1,
        food_class: str = "grass",
        base_eating_penalty: int = 2,
        base_vision_radius: int = 30,
        base_health: int = 100,
        base_hunger: int = 100,
        base_lifespan: int = 2_000,
        base_reproduce_cycle: int = 100,
        genes=None,
        *args,
        **kwargs,
    ):
        super().__init__(
            entity_class=entity_class,
            colour=colour,
            base_speed=base_speed,
            food_class=food_class,
            base_eating_penalty=base_eating_penalty,
            base_vision_radius=base_vision_radius,
            base_health=base_health,
            base_hunger=base_hunger,
            base_lifespan=base_lifespan,
            base_reproduce_cycle=base_reproduce_cycle,
            genes=genes,
            *args,
            **kwargs,
        )
