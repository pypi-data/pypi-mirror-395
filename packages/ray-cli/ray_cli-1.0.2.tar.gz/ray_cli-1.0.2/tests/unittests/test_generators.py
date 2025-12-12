import pytest

from ray_cli.modes import RampModeDmxDataGenerator
from ray_cli.modes.generators import (
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
)


@pytest.mark.parametrize("fps, expected", [
    (4,  [[10]] * 4),
    (6,  [[10]] * 6),
    (10, [[10]] * 10),
])  # fmt: skip
def test_static_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = StaticModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (4,  [[0], [4], [4], [0]]),
    (6,  [[0], [2], [4], [4], [2], [0]]),
    (10, [[0], [1], [2], [3], [4], [4], [3], [2], [1], [0]]),
])  # fmt: skip
def test_ramp_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=4):
    generator = RampModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [4]]),
    (5,  [[0], [1], [2], [3], [4]]),
    (9,  [[0], [1], [1], [2], [2], [3], [3], [4], [4]]),
])  # fmt: skip
def test_ramp_up_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=4):
    generator = RampUpModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[4], [0]]),
    (5,  [[4], [3], [2], [1], [0]]),
    (9,  [[4], [4], [3], [3], [2], [2], [1], [1], [0]]),
])  # fmt: skip
def test_ramp_down_mode_output_shape(
    fps, expected, channels=1, frequency=1, intensity=4
):
    generator = RampDownModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (1,  [[10, 0, 0]]),
    (2,  [[10, 0, 0], [0, 0, 10]]),
    (3,  [[10, 0, 0], [0, 10, 0], [0, 0, 10]]),
    (6,  [[10, 0, 0], [10, 0, 0], [0, 10, 0], [0, 10, 0], [0, 0, 10], [0, 0, 10]]),
])  # fmt: skip
def test_chase_mode_output_shape(fps, expected, channels=3, frequency=1, intensity=10):
    generator = ChaseModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            output = next(generator)
            assert output == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [10]]),
    (4,  [[0], [0], [10], [10]]),
    (8,  [[0], [0], [0], [0], [10], [10], [10], [10]]),
])  # fmt: skip
def test_square_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = SquareModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [10]]),
    (4,  [[0], [9], [9], [1]]),
    (8,  [[0], [5], [8], [10], [10], [8], [5], [1]]),
])  # fmt: skip
def test_sine_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = SineModeDmxDataGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("generator_class", [
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
])  # fmt: skip
@pytest.mark.parametrize("channels", [0, 1, 2, 3, 5, 10, 100, 512, 10000, 100000])
def test_channels_sweep(generator_class, channels, fps=6, frequency=1, intensity=10):
    generator = generator_class(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity,
    )

    actual = next(generator)

    assert len(actual) == channels


@pytest.mark.parametrize("generator_class", [
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
])  # fmt: skip
@pytest.mark.parametrize("intensity_upper", [1, 2, 3, 5, 10, 100, 255])
def test_intensity_upper_sweep(
    generator_class,
    intensity_upper,
    channels=2,
    fps=6,
    frequency=1,
):
    generator = generator_class(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_upper=intensity_upper,
    )

    output = [next(generator) for _ in range(fps)]
    actual = max(
        i for sublist in output for i in sublist
    )  # find max value in the nested list

    assert pytest.approx(actual, abs=actual * 0.05) == intensity_upper


@pytest.mark.parametrize("generator_class", [
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
])  # fmt: skip
@pytest.mark.parametrize("intensity_lower", [1, 2, 3, 5, 10, 100, 255])
def test_intensity_lower_sweep(
    generator_class,
    intensity_lower,
    intensity_upper=255,
    channels=2,
    fps=6,
    frequency=1,
):
    generator = generator_class(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity_lower=intensity_lower,
        intensity_upper=intensity_upper,
    )

    output = [next(generator) for _ in range(fps)]
    print(output)
    actual = min(
        i for sublist in output for i in sublist
    )  # find min value in the nested list

    assert pytest.approx(actual, abs=actual * 0.05) == intensity_lower
