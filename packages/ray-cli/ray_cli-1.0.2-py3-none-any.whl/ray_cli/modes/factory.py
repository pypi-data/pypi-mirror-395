from typing import Dict, Type

from .generators import (
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
)
from .mode import Mode
from .types import DmxDataGenerator

MODE_TO_GENERATOR: Dict[Mode, Type[DmxDataGenerator]] = {
    Mode.CHASE: ChaseModeDmxDataGenerator,
    Mode.RAMP: RampModeDmxDataGenerator,
    Mode.RAMP_DOWN: RampDownModeDmxDataGenerator,
    Mode.RAMP_UP: RampUpModeDmxDataGenerator,
    Mode.SINE: SineModeDmxDataGenerator,
    Mode.SQUARE: SquareModeDmxDataGenerator,
    Mode.STATIC: StaticModeDmxDataGenerator,
}


def generator_factory(
    mode: Mode,
    channels: int,
    fps: int,
    frequency: int,
    intensity_upper: int,
    intensity_lower: int,
) -> DmxDataGenerator:
    try:
        cls = MODE_TO_GENERATOR[mode]

    except KeyError as exc:
        raise NotImplementedError(f"Generator '{mode}' does not exist.") from exc

    return cls(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity_upper,
        intensity_lower=intensity_lower,
    )
