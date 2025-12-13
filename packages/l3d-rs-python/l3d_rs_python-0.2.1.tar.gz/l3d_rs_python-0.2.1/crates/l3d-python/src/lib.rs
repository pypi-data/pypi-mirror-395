use pyo3::prelude::*;

/// Parse an L3D file from bytes and return JSON representation
#[pyfunction]
fn parse_l3d(data: &[u8]) -> String {
    let l3d = l3d_rs::from_buffer(data);
    serde_json::to_string(&l3d).unwrap_or_else(|_| "{}".to_string())
}

/// Parse an L3D file and return model parts as JSON
#[pyfunction]
fn get_model_parts(data: &[u8]) -> String {
    let l3d = l3d_rs::from_buffer(data);
    serde_json::to_string(&l3d.model.parts).unwrap_or_else(|_| "[]".to_string())
}

/// Parse structure.xml content directly and return JSON
#[pyfunction]
fn parse_structure_xml(xml: &str) -> String {
    match l3d_rs::Luminaire::from_xml(xml) {
        Ok(luminaire) => luminaire.to_json().unwrap_or_else(|_| "{}".to_string()),
        Err(_) => "{}".to_string(),
    }
}

/// Load an L3D file from path and return JSON representation
#[pyfunction]
fn load_l3d(path: &str) -> PyResult<String> {
    let data = std::fs::read(path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    Ok(parse_l3d(&data))
}

/// L3D Python module - parse Luminaire 3D files
#[pymodule]
fn l3d(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_l3d, m)?)?;
    m.add_function(wrap_pyfunction!(get_model_parts, m)?)?;
    m.add_function(wrap_pyfunction!(parse_structure_xml, m)?)?;
    m.add_function(wrap_pyfunction!(load_l3d, m)?)?;
    Ok(())
}
