from entities.BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "fox",
        colour: str = "red",
        base_speed: float = 1,
        food_class: str = "pig",
        base_eating_penalty: int = 10,
        base_vision_radius: int = 60,
        base_health: int = 500,
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
