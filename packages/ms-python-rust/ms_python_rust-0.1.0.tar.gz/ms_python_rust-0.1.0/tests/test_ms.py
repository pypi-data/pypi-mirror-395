import math
import pytest
from ms_python_rust import format as ms_format
from ms_python_rust import ms, parse, parse_strict

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("100", 100),
        ("1m", 60_000),
        ("1h", 3_600_000),
        ("2d", 172_800_000),
        ("3w", 1_814_400_000),
        ("1s", 1_000),
        ("100ms", 100),
        ("1y", 31_557_600_000),
        ("4.2h", 15_120_000),
        ("1   s", 1_000),
        ("42 YeArS", 1_325_419_200_000),
        ("42 weeks", 25_401_600_000),
        ("42 HOURS", 151_200_000),
        ("0.42ms", 0.42),
        (".42ms", 0.42),
        ("-100ms", -100),
        ("-4.2h", -15_120_000),
        ("-0.42h", -1_512_000),
        ("-.42ms", -0.42),
    ],
)
def test_parse_variants(value: str, expected: float) -> None:
    """Parse short-unit variants with mixed case, spacing, decimals, and sign."""
    assert parse(value) == expected
    assert parse_strict(value) == expected
    assert ms(value) == expected


def test_parse_long_units() -> None:
    """Parse spelled-out and pluralized unit names."""
    assert parse("42 milliseconds") == 42
    assert parse("42 msecs") == 42
    assert parse("1 sec") == 1_000
    assert parse("1 min") == 60_000
    assert parse("1 hr") == 3_600_000
    assert parse("2 days") == 172_800_000
    assert parse("1 week") == 604_800_000
    assert parse("1 month") == 2_629_800_000
    assert parse("1 year") == 31_557_600_000
    assert parse("-4.2 hours") == -15_120_000
    assert parse("-0.42 hr") == -1_512_000


def test_parse_invalid_patterns_return_nan() -> None:
    """Return NaN for syntactically invalid string patterns."""
    assert math.isnan(parse("☃"))
    assert math.isnan(parse("10-.42"))
    assert math.isnan(parse("foo"))
    assert math.isnan(parse("+1h"))
    assert math.isnan(parse("1h "))
    assert math.isnan(parse("1 h m"))
    assert math.isnan(parse("5qq"))
    assert math.isnan(parse(" 1h"))


def test_parse_strict_invalid_patterns_return_nan() -> None:
    """Ensure parse_strict mirrors parse on invalid patterns."""
    assert math.isnan(parse_strict("foo"))
    assert math.isnan(parse_strict("1 h m"))


@pytest.mark.parametrize(
    "value",
    [
        "",
        "▲" * 101,
        None,
        [],
        {},
        float("nan"),
        float("inf"),
        -float("inf"),
        True,
        False,
    ],
)
def test_parse_invalid_inputs_raise(value: object) -> None:
    """Raise ValueError for non-string inputs or disallowed lengths."""
    with pytest.raises(ValueError):
        parse(value)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        parse_strict(value)  # type: ignore[arg-type]


def test_parse_max_length_allowed() -> None:
    """Allow maximum-length numeric strings."""
    long_number = "1" * 100
    assert parse(long_number) == float(long_number)
    assert parse_strict(long_number) == float(long_number)


def test_parse_allows_trailing_space_without_unit() -> None:
    """Permit trailing whitespace when no unit is supplied."""
    assert parse("10 ") == 10
    assert parse_strict("10 ") == 10
    assert ms("10 ") == 10


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (500, "500ms"),
        (1_000, "1s"),
        (10_000, "10s"),
        (60 * 1_000, "1m"),
        (60 * 10_000, "10m"),
        (60 * 60 * 1_000, "1h"),
        (60 * 60 * 10_000, "10h"),
        (24 * 60 * 60 * 1_000, "1d"),
        (24 * 60 * 60 * 6_000, "6d"),
        (7 * 24 * 60 * 60 * 1_000, "1w"),
        (2 * 7 * 24 * 60 * 60 * 1_000, "2w"),
        (30.4375 * 24 * 60 * 60 * 1_000, "1mo"),
        (30.4375 * 24 * 60 * 60 * 10_000, "10mo"),
        (365.25 * 24 * 60 * 60 * 1_000 + 1, "1y"),
        (365.25 * 24 * 60 * 60 * 10_000 + 1, "10y"),
        (234_234_234, "3d"),
        (-500, "-500ms"),
        (-1_000, "-1s"),
        (-10_000, "-10s"),
        (-60 * 1_000, "-1m"),
        (-60 * 10_000, "-10m"),
        (-60 * 60 * 1_000, "-1h"),
        (-60 * 60 * 10_000, "-10h"),
        (-24 * 60 * 60 * 1_000, "-1d"),
        (-24 * 60 * 60 * 6_000, "-6d"),
        (-7 * 24 * 60 * 60 * 1_000, "-1w"),
        (-2 * 7 * 24 * 60 * 60 * 1_000, "-2w"),
        (-30.4375 * 24 * 60 * 60 * 1_000, "-1mo"),
        (-30.4375 * 24 * 60 * 60 * 10_000, "-10mo"),
        (-365.25 * 24 * 60 * 60 * 1_000 - 1, "-1y"),
        (-365.25 * 24 * 60 * 60 * 10_000 - 1, "-10y"),
        (-234_234_234, "-3d"),
        (0, "0ms"),
    ],
)
def test_format_short(value: float, expected: str) -> None:
    """Format milliseconds using compact short-unit notation."""
    assert ms(value) == expected
    assert ms_format(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (500, "500 ms"),
        (1_000, "1 second"),
        (10_000, "10 seconds"),
        (60 * 1_000, "1 minute"),
        (60 * 10_000, "10 minutes"),
        (60 * 60 * 1_000, "1 hour"),
        (60 * 60 * 10_000, "10 hours"),
        (24 * 60 * 60 * 1_000, "1 day"),
        (24 * 60 * 60 * 6_000, "6 days"),
        (7 * 24 * 60 * 60 * 1_000, "1 week"),
        (2 * 7 * 24 * 60 * 60 * 1_000, "2 weeks"),
        (30.4375 * 24 * 60 * 60 * 1_000, "1 month"),
        (30.4375 * 24 * 60 * 60 * 10_000, "10 months"),
        (365.25 * 24 * 60 * 60 * 1_000 + 1, "1 year"),
        (365.25 * 24 * 60 * 60 * 10_000 + 1, "10 years"),
        (234_234_234, "3 days"),
        (-500, "-500 ms"),
        (-1_000, "-1 second"),
        (-10_000, "-10 seconds"),
        (-60 * 1_000, "-1 minute"),
        (-60 * 10_000, "-10 minutes"),
        (-60 * 60 * 1_000, "-1 hour"),
        (-60 * 60 * 10_000, "-10 hours"),
        (-24 * 60 * 60 * 1_000, "-1 day"),
        (-24 * 60 * 60 * 6_000, "-6 days"),
        (-7 * 24 * 60 * 60 * 1_000, "-1 week"),
        (-2 * 7 * 24 * 60 * 60 * 1_000, "-2 weeks"),
        (-30.4375 * 24 * 60 * 60 * 1_000, "-1 month"),
        (-30.4375 * 24 * 60 * 60 * 10_000, "-10 months"),
        (-365.25 * 24 * 60 * 60 * 1_000 - 1, "-1 year"),
        (-365.25 * 24 * 60 * 60 * 10_000 - 1, "-10 years"),
        (-234_234_234, "-3 days"),
        (0, "0 ms"),
    ],
)
def test_format_long(value: float, expected: str) -> None:
    """Format milliseconds using long, plural-aware unit names."""
    assert ms(value, long=True) == expected
    assert ms_format(value, long=True) == expected


@pytest.mark.parametrize(
    ("value", "expected_short", "expected_long"),
    [
        (1_499, "1s", "1 second"),
        (1_500, "2s", "2 seconds"),
        (89_999, "1m", "1 minute"),
        (90_000, "2m", "2 minutes"),
    ],
)
def test_format_rounding_boundaries(
    value: float, expected_short: str, expected_long: str
) -> None:
    """Check rounding around unit boundaries for short and long formats."""
    assert ms_format(value) == expected_short
    assert ms_format(value, long=True) == expected_long


def test_format_sub_second_precision() -> None:
    """Preserve sub-second precision when formatting values below one second."""
    assert ms_format(0.42) == "0.42ms"
    assert ms_format(-0.42) == "-0.42ms"
    assert ms_format(0.42, long=True) == "0.42 ms"


@pytest.mark.parametrize(
    "value",
    [
        "",
        None,
        [],
        {},
        float("nan"),
        float("inf"),
        -float("inf"),
        True,
        False,
    ],
)
def test_format_invalid_inputs_raise(value: object) -> None:
    """Raise ValueError when formatting non-numeric or non-finite inputs."""
    with pytest.raises(ValueError):
        ms_format(value)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        ms(value)  # type: ignore[arg-type]
