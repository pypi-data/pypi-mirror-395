from typing import Optional, Sequence, Tuple, Union

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ray_cli.cli import Limits, cli
from ray_cli.modes import Mode

Number = Union[int, float]


def parse(argv, protocol: str = "sacn"):
    return cli.parse_args([protocol, *map(str, argv)])


def in_range_int(
    bounds: Tuple[Optional[Number], Optional[Number]],
) -> st.SearchStrategy[str]:
    lo, hi = bounds
    kw = {}
    if lo is not None:
        kw["min_value"] = int(lo)
    if hi is not None:
        kw["max_value"] = int(hi)
    return st.integers(**kw).map(str)


def out_of_range_int(
    bounds: Tuple[Optional[Number], Optional[Number]],
) -> st.SearchStrategy[str]:
    lo, hi = bounds
    parts = []
    if lo is not None:
        parts.append(st.integers(max_value=int(lo) - 1))
    if hi is not None:
        parts.append(st.integers(min_value=int(hi) + 1))
    return st.one_of(*parts).map(str) if parts else st.nothing()


def list_of_in_range_ints(
    bounds: Tuple[Optional[Number], Optional[Number]],
    *,
    min_size: int = 1,
    max_size: int = 5,
) -> st.SearchStrategy[Sequence[str]]:
    return st.lists(in_range_int(bounds), min_size=min_size, max_size=max_size)


def non_numeric_text() -> st.SearchStrategy[str]:
    bads = ["", "x", "nope", "NaN", "--flag", "∞", "ten"]
    return st.sampled_from(bads)


@given(st.sampled_from([m.value for m in Mode]))
def test_mode_valid(value: str):
    ns = parse(["--mode", value])
    assert isinstance(ns.mode, Mode) and ns.mode.value == value


@given(st.text(min_size=1).filter(lambda s: s not in {m.value for m in Mode}))
def test_mode_invalid(value: str):
    with pytest.raises(SystemExit):
        parse(["--mode", value])


OPTION_CASES = [
    ("--channels", "channels", Limits.channels, int),
    ("--intensity", "intensity", Limits.intensity, int),
    ("--workers", "workers", Limits.workers, int),
    ("--priority", "priority", Limits.sacn_priority, int),
]


@pytest.mark.parametrize("opt, attr, bounds, caster", OPTION_CASES)
@given(data=st.data())
def test_option_valid(opt: str, attr: str, bounds, caster, data):
    value = data.draw(in_range_int(bounds))
    ns = parse([opt, value])
    assert getattr(ns, attr) == caster(value)


@pytest.mark.parametrize("opt, attr, bounds, caster", OPTION_CASES)
@given(data=st.data())
def test_option_invalid(opt: str, attr: str, bounds, caster, data):
    bad = data.draw(out_of_range_int(bounds))
    with pytest.raises(SystemExit):
        parse([opt, bad])


def test_channels_edges():
    lo, hi = Limits.channels
    assert parse(["--channels", str(lo)]).channels == lo
    assert parse(["--channels", str(hi)]).channels == hi


@given(non_numeric_text())
def test_channels_non_numeric_exits(value: str):
    with pytest.raises(SystemExit):
        parse(["--channels", value])


@given(list_of_in_range_ints(Limits.sacn_universes))
def test_sacn_universes_valid(values: Sequence[str]):
    ns = parse(["--universes", *values])
    assert ns.universes == [int(v) for v in values]


@given(out_of_range_int(Limits.sacn_universes))
def test_sacn_universes_invalid(value: str):
    with pytest.raises(SystemExit):
        parse(["--universes", value])


def test_packets_duration_mutex():
    with pytest.raises(SystemExit):
        parse(["--packets", "10", "--duration", "1"])


@pytest.mark.parametrize(
    "flag, attr",
    [
        ("--verbose", "verbose"),
        ("--quiet", "quiet"),
        ("--dry", "dry"),
    ],
)
def test_flag_sets_true(flag: str, attr: str):
    ns = parse([flag])
    assert getattr(ns, attr) is True


def test_verbose_and_quiet_are_exclusive():
    with pytest.raises(SystemExit):
        parse(["--verbose", "--quiet"])


def test_help_prints_and_exits(capsys):
    with pytest.raises(SystemExit) as ei:
        parse(["--help"])
    assert ei.value.code == 0
    out = capsys.readouterr().out
    assert "usage" in out.lower()


def test_version_prints_and_exits(capsys):
    with pytest.raises(SystemExit) as ei:
        parse(["--version"])
    assert ei.value.code == 0
    out = capsys.readouterr().out
    assert out.strip()


@given(
    st.permutations(
        [
            ["--channels", "10"],
            ["--intensity", "5"],
            ["--workers", "2"],
        ]
    )
)
def test_option_order_invariance(pairs):
    argv = [tok for pair in pairs for tok in pair]
    ns = parse(argv)
    assert ns.channels == 10
    assert ns.intensity == 5
    assert ns.workers == 2
