from entities.BaseEntity import BaseEntity


class Grass(BaseEntity):
    def __init__(
        self, entity_type: str = "grass", colour: str = "green", *args, **kwargs
    ):
        super().__init__(entity_type, colour, *args, **kwargs)
