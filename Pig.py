from BaseEntity import BaseEntity
import emoji

class Pig(BaseEntity):
    def __init__(self, colour: str = "pink", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)

    def __str__(self):
        return f"{emoji.emojize(':pig:')}"
        # return f"{emoji.emojize(':pig:')}-{hash(str(self.creation_time).replace(' ', '-'))}"
