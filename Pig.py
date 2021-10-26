from BaseEntity import BaseEntity

class Pig(BaseEntity):
    def __init__(self, colour: str = "pink", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)

    def __str__(self):
        return f"P-{hash(str(self.creation_time).replace(' ', '-'))}"
