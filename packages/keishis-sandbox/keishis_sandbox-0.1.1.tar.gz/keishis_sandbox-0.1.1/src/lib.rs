#[cfg(feature = "python")]
use pyo3::pymodule;

fn sum_as_str(a: i64, b: i64) -> String {
    (a + b).to_string()
}

#[cfg(feature = "python")]
#[pymodule]
#[pyo3(name = "_keishis_sandbox")]
mod keishis_sandbox {
    use super::sum_as_str as _sum_as_str;
    use pyo3::prelude::PyResult;
    use pyo3::pyfunction;

    #[pyfunction]
    fn sum_as_str(a: i64, b: i64) -> PyResult<String> {
        Ok(_sum_as_str(a, b))
    }
}
