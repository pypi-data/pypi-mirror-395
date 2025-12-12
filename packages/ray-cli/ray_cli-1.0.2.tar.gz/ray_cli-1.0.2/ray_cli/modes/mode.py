import enum


class Mode(enum.Enum):
    CHASE = "chase"
    RAMP = "ramp"
    RAMP_DOWN = "ramp-down"
    RAMP_UP = "ramp-up"
    SINE = "sine"
    SQUARE = "square"
    STATIC = "static"

    def __str__(self):
        return self.value
