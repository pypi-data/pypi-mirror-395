//! pmgfal - pydantic model generator for atproto lexicons

mod builtin;
mod codegen;
mod parser;
mod types;

use std::path::Path;

use pyo3::prelude::*;

/// generate pydantic models from lexicon files
#[pyfunction]
#[pyo3(signature = (lexicon_dir, output_dir, namespace_prefix=None))]
fn generate(
    lexicon_dir: &str,
    output_dir: &str,
    namespace_prefix: Option<&str>,
) -> PyResult<Vec<String>> {
    let lexicon_path = Path::new(lexicon_dir);
    let output_path = Path::new(output_dir);

    let docs = parser::parse_lexicons(lexicon_path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;

    let files = codegen::generate_models(&docs, output_path, namespace_prefix)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;

    Ok(files)
}

#[pymodule]
fn _pmgfal(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
