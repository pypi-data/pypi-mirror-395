use pyo3::conversion::IntoPyObjectExt;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{
    PyAny, PyBool, PyFloat, PyInt, PyModule, PyModuleMethods, PyString, PyStringMethods,
};

const S: f64 = 1000.0;
const M: f64 = S * 60.0;
const H: f64 = M * 60.0;
const D: f64 = H * 24.0;
const W: f64 = D * 7.0;
const Y: f64 = D * 365.25;
const MO: f64 = Y / 12.0;

fn py_repr(value: &Bound<'_, PyAny>) -> String {
    value
        .repr()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_else(|_| "<unrepresentable>".to_string())
}

fn parse_input_error(value: &Bound<'_, PyAny>) -> PyErr {
    PyValueError::new_err(format!(
        "Value provided to ms.parse() must be a string with length between 1 and 99. value={}",
        py_repr(value)
    ))
}

fn parse_input_error_from_str(value: &str) -> PyErr {
    PyValueError::new_err(format!(
        "Value provided to ms.parse() must be a string with length between 1 and 99. value={:?}",
        value
    ))
}

fn ensure_string<'py>(value: &'py Bound<'py, PyAny>) -> PyResult<&'py str> {
    let py_str = value.cast::<PyString>().map_err(|_| parse_input_error(value))?;
    let as_str = py_str.to_str()?;
    if as_str.is_empty() || as_str.len() > 100 {
        return Err(parse_input_error_from_str(as_str));
    }
    Ok(as_str)
}

fn parse_str_to_ms(raw: &str) -> f64 {
    let bytes = raw.as_bytes();
    let len = bytes.len();
    let mut idx = 0;

    if idx < len && bytes[idx] == b'-' {
        idx += 1;
    }

    let mut digits_before = 0;
    let mut digits_after = 0;
    let mut dot_seen = false;

    while idx < len {
        let b = bytes[idx];
        if b.is_ascii_digit() {
            if dot_seen {
                digits_after += 1;
            } else {
                digits_before += 1;
            }
            idx += 1;
            continue;
        }
        if b == b'.' {
            if dot_seen {
                return f64::NAN;
            }
            dot_seen = true;
            idx += 1;
            continue;
        }
        break;
    }

    if digits_before + digits_after == 0 {
        return f64::NAN;
    }
    if dot_seen && digits_after == 0 {
        return f64::NAN;
    }

    let number_str = &raw[..idx];
    let number: f64 = match number_str.parse() {
        Ok(val) => val,
        Err(_) => return f64::NAN,
    };

    while idx < len && bytes[idx] == b' ' {
        idx += 1;
    }

    if idx == len {
        return number;
    }

    let unit_str = &raw[idx..];
    if unit_str.as_bytes().iter().any(|b| *b == b' ') {
        return f64::NAN;
    }

    let unit = unit_str.to_ascii_lowercase();

    match unit.as_str() {
        "years" | "year" | "yrs" | "yr" | "y" => number * Y,
        "months" | "month" | "mo" => number * MO,
        "weeks" | "week" | "w" => number * W,
        "days" | "day" | "d" => number * D,
        "hours" | "hour" | "hrs" | "hr" | "h" => number * H,
        "minutes" | "minute" | "mins" | "min" | "m" => number * M,
        "seconds" | "second" | "secs" | "sec" | "s" => number * S,
        "milliseconds" | "millisecond" | "msecs" | "msec" | "ms" => number,
        _ => f64::NAN,
    }
}

fn js_round(value: f64) -> f64 {
    (value + 0.5).floor()
}

fn plural(ms: f64, ms_abs: f64, n: f64, name: &str) -> String {
    let is_plural = ms_abs >= n * 1.5;
    let rounded = js_round(ms / n);
    format!("{rounded} {name}{}", if is_plural { "s" } else { "" })
}

fn fmt_short(ms: f64) -> String {
    let ms_abs = ms.abs();
    if ms_abs >= Y {
        return format!("{}y", js_round(ms / Y));
    }
    if ms_abs >= MO {
        return format!("{}mo", js_round(ms / MO));
    }
    if ms_abs >= W {
        return format!("{}w", js_round(ms / W));
    }
    if ms_abs >= D {
        return format!("{}d", js_round(ms / D));
    }
    if ms_abs >= H {
        return format!("{}h", js_round(ms / H));
    }
    if ms_abs >= M {
        return format!("{}m", js_round(ms / M));
    }
    if ms_abs >= S {
        return format!("{}s", js_round(ms / S));
    }
    format!("{ms}ms")
}

fn fmt_long(ms: f64) -> String {
    let ms_abs = ms.abs();
    if ms_abs >= Y {
        return plural(ms, ms_abs, Y, "year");
    }
    if ms_abs >= MO {
        return plural(ms, ms_abs, MO, "month");
    }
    if ms_abs >= W {
        return plural(ms, ms_abs, W, "week");
    }
    if ms_abs >= D {
        return plural(ms, ms_abs, D, "day");
    }
    if ms_abs >= H {
        return plural(ms, ms_abs, H, "hour");
    }
    if ms_abs >= M {
        return plural(ms, ms_abs, M, "minute");
    }
    if ms_abs >= S {
        return plural(ms, ms_abs, S, "second");
    }
    format!("{ms} ms")
}

fn format_internal(ms: f64, long: bool) -> PyResult<String> {
    if !ms.is_finite() {
        return Err(PyValueError::new_err(
            "Value provided to ms.format() must be of type number.",
        ));
    }
    Ok(if long { fmt_long(ms) } else { fmt_short(ms) })
}

fn extract_number(value: &Bound<'_, PyAny>) -> PyResult<f64> {
    if value.is_instance_of::<PyBool>() {
        return Err(PyValueError::new_err(
            "Value provided to ms.format() must be of type number.",
        ));
    }
    if !(value.is_instance_of::<PyFloat>() || value.is_instance_of::<PyInt>()) {
        return Err(PyValueError::new_err(
            "Value provided to ms.format() must be of type number.",
        ));
    }
    let ms: f64 = value.extract().map_err(|_| {
        PyValueError::new_err("Value provided to ms.format() must be of type number.")
    })?;
    if !ms.is_finite() {
        return Err(PyValueError::new_err(
            "Value provided to ms.format() must be of type number.",
        ));
    }
    Ok(ms)
}

fn ms_type_error(value: &Bound<'_, PyAny>) -> PyErr {
    PyValueError::new_err(format!(
        "Value provided to ms() must be a string or number. value={}",
        py_repr(value)
    ))
}

#[pyfunction(signature = (value, *, long = None))]
fn ms(py: Python<'_>, value: Bound<'_, PyAny>, long: Option<bool>) -> PyResult<Py<PyAny>> {
    if value.is_instance_of::<PyString>() {
        let parsed = parse_str_to_ms(ensure_string(&value)?);
        return Ok(parsed.into_py_any(py)?);
    }

    if value.is_instance_of::<PyBool>() {
        return Err(ms_type_error(&value));
    }

    if value.is_instance_of::<PyFloat>() || value.is_instance_of::<PyInt>() {
        let formatted = format_internal(extract_number(&value)?, long.unwrap_or(false))?;
        return Ok(formatted.into_py_any(py)?);
    }

    Err(ms_type_error(&value))
}

#[pyfunction]
fn parse(value: Bound<'_, PyAny>) -> PyResult<f64> {
    let input = ensure_string(&value)?;
    Ok(parse_str_to_ms(input))
}

#[pyfunction]
fn parse_strict(value: Bound<'_, PyAny>) -> PyResult<f64> {
    let input = ensure_string(&value)?;
    Ok(parse_str_to_ms(input))
}

#[pyfunction(signature = (ms_value, *, long = None))]
fn format(ms_value: Bound<'_, PyAny>, long: Option<bool>) -> PyResult<String> {
    let number = extract_number(&ms_value)?;
    format_internal(number, long.unwrap_or(false))
}

#[pymodule]
fn ms_python_rust(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ms, m)?)?;
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_function(wrap_pyfunction!(parse_strict, m)?)?;
    m.add_function(wrap_pyfunction!(format, m)?)?;
    Ok(())
}
