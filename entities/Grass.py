from entities.BaseEntity import BaseEntity


class Grass(BaseEntity):
    def __init__(self, colour: str = "green", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)
