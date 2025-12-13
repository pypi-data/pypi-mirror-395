//! pmgfal - pydantic model generator for atproto lexicons

mod builtin;
mod codegen;
mod parser;
mod types;

use std::fs;
use std::path::Path;

use pyo3::prelude::*;
use sha2::{Digest, Sha256};

/// compute a hash of all lexicon files in a directory
#[pyfunction]
#[pyo3(signature = (lexicon_dir, namespace_prefix=None))]
fn hash_lexicons(lexicon_dir: &str, namespace_prefix: Option<&str>) -> PyResult<String> {
    let lexicon_path = Path::new(lexicon_dir);

    let mut hasher = Sha256::new();

    // include version in hash so cache invalidates on upgrades
    hasher.update(env!("CARGO_PKG_VERSION").as_bytes());

    // include prefix in hash
    if let Some(prefix) = namespace_prefix {
        hasher.update(prefix.as_bytes());
    }

    // collect and sort json files for deterministic hashing
    let mut json_files: Vec<_> = walkdir::WalkDir::new(lexicon_path)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().is_some_and(|ext| ext == "json"))
        .collect();

    json_files.sort_by(|a, b| a.path().cmp(b.path()));

    for entry in json_files {
        let path = entry.path();
        if let Some(name) = path.file_name() {
            hasher.update(name.as_encoded_bytes());
        }
        if let Ok(content) = fs::read(path) {
            hasher.update(&content);
        }
    }

    let result = hasher.finalize();
    Ok(hex::encode(&result[..8])) // 16 hex chars
}

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
    m.add_function(wrap_pyfunction!(hash_lexicons, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
