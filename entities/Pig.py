from entities.BaseAnimal import BaseAnimal


class Pig(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "pig",
        colour: str = "pink",
        speed: float = 0.5,
        food_class: str = "grass",
        eating_penalty: int = 1,
        max_health: int = 200,
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
