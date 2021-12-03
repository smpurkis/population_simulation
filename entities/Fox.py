from entities.BaseAnimal import BaseAnimal


class Fox(BaseAnimal):
    def __init__(
        self,
        entity_class: str = "fox",
        colour: str = "orange",
        speed: float = 1,
        food_class: str = "pig",
        *args,
        **kwargs
    ):
        super().__init__(entity_class, colour, speed, food_class, *args, **kwargs)
