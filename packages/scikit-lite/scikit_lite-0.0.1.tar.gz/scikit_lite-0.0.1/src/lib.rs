use pyo3::prelude::*;

#[pyfunction]
fn rust_health_check() -> PyResult<&'static str> {
    Ok("Rust OK")
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_health_check, m)?)?;
    Ok(())
}
