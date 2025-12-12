from typing import Union

from .generators import (
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
)

DmxDataGenerator = Union[
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    ChaseModeDmxDataGenerator,
]
