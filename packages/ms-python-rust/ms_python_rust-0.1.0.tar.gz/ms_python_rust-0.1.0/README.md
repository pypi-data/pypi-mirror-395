# ms-python-rust (Python + Rust)

Tiny millisecond conversion utility for Python. This is a Rust-backed port of Vercel's `ms` package.

The core logic lives in Rust (via PyO3) for speed and is exposed as a small Python API.

[Tests (Python 3.8 to 3.13)](https://github.com/barrar/ms-python-rust/actions/workflows/test.yml):  
![Tests](https://github.com/barrar/ms-python-rust/actions/workflows/test.yml/badge.svg)  

## Quickstart (maturin)

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -U pip maturin
maturin develop  # builds the Rust extension into the virtualenv
```

### Installation options

- Editable dev install: `maturin develop` in an activated venv.
- Build wheels: `maturin build --release` (outputs to `./target/wheels`).
- Source distribution: `maturin sdist`.

```python
from ms_python_rust import ms, parse, parse_strict, format as ms_format

ms("2 days")        # 172800000
ms("1d")            # 86400000
ms("2.5 hrs")       # 9000000
ms("100")           # 100
ms(60000)           # "1m"
ms(60000, long=True)  # "1 minute"
parse("10h")        # 36000000
ms_format(2000)     # "2s"
parse_strict("1h")  # 3600000
```

### CLI-style one-liners (once built/installed)

```bash
python -c "from ms_python_rust import ms; print(ms('4.2h'))"     # 15120000
python -c "from ms_python_rust import format; print(format(60000, long=True))"  # 1 minute
```

## API

- `ms(value, long=False)`: Parse strings into milliseconds or format numeric millisecond values back to strings (short form by default).
- `parse(value: str) -> float`: Convert a string duration to milliseconds. Returns `math.nan` when the string cannot be parsed.
- `parse_strict(value: str) -> float`: Alias for `parse`; exists to mirror the original API.
- `format(ms_value: float, long=False) -> str`: Format milliseconds to a human-readable string. Use `long=True` for verbose units.

### Examples

```python
# Parsing
parse("42 HOURS")          # 151200000
parse("-0.42 hr")          # -1512000
parse("1 week")            # 604800000
parse("100")               # 100 (defaults to ms)
parse("bad input")         # math.nan

# Formatting
ms(234_234_234)            # "3d"
ms(60_000, long=True)      # "1 minute"
ms_format(-10_000)         # "-10s"
ms_format(-10_000, long=True)  # "-10 seconds"
```

## Units

Accepted units (case-insensitive, spaces optional):

- Years: `years`, `year`, `yrs`, `yr`, `y`
- Months: `months`, `month`, `mo`
- Weeks: `weeks`, `week`, `w`
- Days: `days`, `day`, `d`
- Hours: `hours`, `hour`, `hrs`, `hr`, `h`
- Minutes: `minutes`, `minute`, `mins`, `min`, `m`
- Seconds: `seconds`, `second`, `secs`, `sec`, `s`
- Milliseconds: `milliseconds`, `millisecond`, `msecs`, `msec`, `ms`

If no unit is provided (`"2"`), milliseconds are assumed. Fractional inputs like `0.5m`, `-0.5m`, `.5m`, and `-.5m` are supported.

## Error handling

- `parse`/`parse_strict` expect strings between 1 and 100 characters; other inputs raise `ValueError`.
- `format`/`ms` require finite numeric inputs when formatting; invalid types or `nan/inf` raise `ValueError`.
- When parsing, unrecognized patterns yield `math.nan` rather than throwing.

## Development

Prerequisites: Python 3.8+, Rust toolchain, and `maturin` installed in your environment. This project follows the layout recommended in the [maturin docs](https://www.maturin.rs/).

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -U pip maturin pytest
maturin develop       # build extension in-place for the venv
pytest                # run tests

# Build distributable wheels (universal, manylinux/macos/windows via maturin)
maturin build --release
# Or just source distribution
maturin sdist
```
