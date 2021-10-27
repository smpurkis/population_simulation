import emoji

from BaseEntity import BaseEntity


class Grass(BaseEntity):
    def __init__(self, colour: str = "green", position: tuple = None):
        super().__init__(colour=colour, position=position)

    def __str__(self):
        return f"{emoji.emojize(':seedling:')}"
        # return f"{emoji.emojize(':seedling:')}-{hash(str(self.creation_time).replace(' ', '-'))}"
