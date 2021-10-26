from BaseEntity import BaseEntity


class Fox(BaseEntity):
    def __init__(self, colour: str = "orange", *args, **kwargs):
        super().__init__(colour=colour, *args, **kwargs)

    def __str__(self):
        return f"F-{hash(str(self.creation_time).replace(' ', '-'))}"
