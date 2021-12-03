from entities.BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "fox",
        colour: str = "orange",
        speed: float = 1,
        food_class: str = "pig",
        eating_penalty: int = 10,
        max_health: int = 500,
        *args,
        **kwargs
    ):
        super().__init__(
            entity_class,
            colour,
            speed,
            food_class,
            eating_penalty,
            max_health,
            *args,
            **kwargs
        )
