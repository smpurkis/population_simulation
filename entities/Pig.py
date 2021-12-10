from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "pig",
        colour: str = "pink",
        base_speed: float = 0.5,
        food_class: str = "grass",
        base_eating_penalty: int = 1,
        base_vision_radius: int = 100,
        base_health: int = 100,
        base_hunger: int = 100,
        *args,
        **kwargs
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
            *args,
            **kwargs
        )
