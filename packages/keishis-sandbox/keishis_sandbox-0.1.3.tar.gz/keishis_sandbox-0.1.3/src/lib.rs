#[cfg(feature = "python")]
use pyo3::pymodule;

fn _mysum(a: i64, b: i64) -> i64 {
    a + b
}

#[cfg(feature = "python")]
#[pymodule]
#[pyo3(name = "_keishis_sandbox")]
mod keishis_sandbox {
    use super::_mysum;
    use pyo3::prelude::PyResult;
    use pyo3::pyfunction;

    #[pyfunction]
    fn mysum(a: i64, b: i64) -> PyResult<i64> {
        Ok(_mysum(a, b))
    }
}

#[cfg(feature = "julia")]
#[unsafe(no_mangle)]
pub extern "C" fn mysum(a: i64, b: i64) -> i64 {
    _mysum(a, b)
}
