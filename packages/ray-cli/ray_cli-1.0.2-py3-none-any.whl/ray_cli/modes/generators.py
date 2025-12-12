import itertools
import math
from abc import ABC, abstractmethod
from typing import Iterator, Sequence

DmxData = Sequence[int]


def linspace(start: float, stop: float, num: int) -> Iterator[float]:
    if num < 1:
        raise ValueError("num must be >= 1")
    if num == 1:
        yield float(start)
        return

    step = (stop - start) / (num - 1)
    for i in range(num):
        yield start + step * i


class BaseGenerator(ABC):
    def __init__(
        self,
        channels: int,
        fps: int,
        frequency: float,
        intensity_upper: int,
        intensity_lower: int = 0,
    ):
        super().__init__()
        self.channels = channels
        self.fps = fps
        self.frequency = frequency
        self.intensity_lower = intensity_lower
        self.intensity_upper = intensity_upper

        self.generator = self.create(
            channels=self.channels,
            fps=self.fps,
            frequency=self.frequency,
            intensity_lower=self.intensity_lower,
            intensity_upper=self.intensity_upper,
        )

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    @abstractmethod
    def next(self) -> DmxData: ...

    @classmethod
    @abstractmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator: ...


class StaticModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        intensity = next(self.generator)
        return [intensity for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        return itertools.cycle([intensity_upper])


class RampModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        intensity = next(self.generator)
        return [math.ceil(intensity)] * self.channels

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil((fps / frequency) / 2)
        return itertools.cycle(
            itertools.chain(
                linspace(intensity_lower, intensity_upper, size),
                linspace(intensity_upper, intensity_lower, size),
            ),
        )


class RampUpModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        intensity = next(self.generator)
        return [math.ceil(intensity)] * self.channels

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(
            itertools.chain(
                linspace(intensity_lower, intensity_upper, size),
            ),
        )


class RampDownModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        intensity = next(self.generator)
        return [math.ceil(intensity)] * self.channels

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(
            itertools.chain(
                linspace(intensity_upper, intensity_lower, size),
            ),
        )


class ChaseModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        channel = round(next(self.generator))
        return [
            self.intensity_upper if channel == i else self.intensity_lower
            for i in range(self.channels)
        ]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(linspace(0, channels - 1, size))


class SquareModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        intensity = next(self.generator)
        return [math.ceil(intensity)] * self.channels

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil((fps / frequency) / 2)
        return itertools.cycle(
            itertools.chain(
                linspace(intensity_lower, intensity_lower, size),
                linspace(intensity_upper, intensity_upper, size),
            ),
        )


class SineModeDmxDataGenerator(BaseGenerator):
    def next(self) -> DmxData:
        output_coeff = next(self.generator)
        return [
            math.ceil(
                output_coeff * (self.intensity_upper - self.intensity_lower)
                + self.intensity_lower
            )
            for _ in range(self.channels)
        ]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity_lower: int,
        intensity_upper: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)

        if size <= 2:
            return itertools.cycle([0, 1])

        x_values = linspace(0, math.pi, size)
        return itertools.cycle(itertools.chain(map(math.sin, x_values)))
