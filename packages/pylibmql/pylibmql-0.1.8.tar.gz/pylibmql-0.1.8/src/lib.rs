use libmql::{parse as libmql_parse, ParseResult};
use pyo3::{exceptions::PyValueError, prelude::*};

#[pyclass]
pub struct MQL {
    file: ParseResult,
}

#[pymethods]
impl MQL {
    #[new]
    fn new(value: String) -> PyResult<Self> {
        Ok(Self {
            file: libmql_parse(&value)
                .map_err(|e| PyErr::new::<PyValueError, _>(format!("{e:?}")))?,
        })
    }

    fn version(&self) -> &'static str {
        self.file.parsed_mql_file().version()
    }

    fn json(&self) -> PyResult<String> {
        self.file
            .to_string()
            .map_err(|e| PyErr::new::<PyValueError, _>(format!("{e:?}")))
    }

    fn json_pretty(&self) -> PyResult<String> {
        self.file
            .to_string_pretty()
            .map_err(|e| PyErr::new::<PyValueError, _>(format!("{e:?}")))
    }

    fn __str__(&self) -> String {
        format!("{:?}", self.file)
    }
}

#[pyfunction]
fn parse(mql: String) -> PyResult<MQL> {
    MQL::new(mql)
}

#[pymodule]
fn pylibmql(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    Ok(())
}
