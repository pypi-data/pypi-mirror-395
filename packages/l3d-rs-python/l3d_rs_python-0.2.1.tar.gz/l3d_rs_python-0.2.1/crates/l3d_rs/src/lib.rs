//! # l3d_rs - L3D (Luminaire 3D) File Parser for Rust
//!
//! A Rust library for parsing and working with L3D files, the 3D geometry format
//! used in the lighting industry alongside GLDF (Global Lighting Data Format).
//!
//! ## What is L3D?
//!
//! L3D (Luminaire 3D) is a ZIP-based file format that contains:
//! - `structure.xml` - XML file describing the luminaire geometry hierarchy
//! - OBJ files - 3D geometry files for each part of the luminaire
//! - Optional texture and material files
//!
//! The format supports hierarchical assemblies with joints, allowing for
//! adjustable luminaire components (e.g., rotatable lamp heads).
//!
//! ## Features
//!
//! - **XML Parsing**: Parse `structure.xml` into strongly-typed Rust structs
//! - **JSON Serialization**: Convert between L3D XML and JSON formats
//! - **3D Model Building**: Build transformation matrices for rendering
//! - **No 3D Engine Dependency**: Matrix operations are self-contained
//! - **WASM Compatible**: Designed for use in WebAssembly targets
//!
//! ## Quick Start
//!
//! ### Parse an L3D file from bytes (recommended for WASM)
//!
//! ```no_run
//! use l3d_rs::{from_buffer, L3d};
//!
//! // Load L3D file as bytes (e.g., from file upload or fetch)
//! let l3d_bytes = std::fs::read("luminaire.l3d").unwrap();
//!
//! // Parse the L3D file
//! let l3d: L3d = from_buffer(&l3d_bytes);
//!
//! // Access the parsed model
//! println!("Parts: {}", l3d.model.parts.len());
//! for part in &l3d.model.parts {
//!     println!("  {} with transform matrix", part.path);
//! }
//!
//! // Access raw assets for 3D rendering
//! for asset in &l3d.file.assets {
//!     println!("Asset: {} ({} bytes)", asset.name, asset.size);
//! }
//! ```
//!
//! ### Load from file path (native only)
//!
//! ```no_run
//! use l3d_rs::Luminaire;
//!
//! // Load and parse the luminaire structure
//! let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();
//!
//! // Convert to JSON for web transmission
//! let json = luminaire.to_json().unwrap();
//! ```
//!
//! ## Integration with 3D Renderers
//!
//! The [`Mat4`] type is a `[f32; 16]` array in column-major order, compatible
//! with OpenGL, WebGL, and most 3D libraries. To use with `three-d`:
//!
//! ```ignore
//! use three_d::Mat4 as ThreeDMat4;
//! use l3d_rs::L3dPart;
//!
//! fn convert_matrix(part: &L3dPart) -> ThreeDMat4 {
//!     ThreeDMat4::from_cols_array(&part.mat)
//! }
//! ```
//!
//! ## Module Structure
//!
//! - [`l3d`] - Core types for L3D structure (Luminaire, Geometry, etc.)
//! - [`from_buffer`] - Main entry point for parsing L3D files
//! - Matrix utilities - [`mat4_mul`], [`mat4_translation`], [`mat4_scale`], etc.

pub mod l3d;
#[cfg(test)]
mod tests;

use anyhow::{Context, Result};
use quick_xml::de::from_str as from_xml_str;
use regex::Regex;
use serde_json::{from_str as from_json_str, to_string_pretty as to_json_str};
use std::{
    fs::File as StdFile,
    io::Read,
    path::{Path, PathBuf},
};
use zip::ZipArchive;

// Re-export all public types for easy access
pub use l3d::{
    build_transform,
    get_scale,
    // Matrix utilities
    mat4_mul,
    mat4_rotate_x,
    mat4_rotate_y,
    mat4_rotate_z,
    mat4_scale,
    mat4_translation,
    BufFile,
    Geometries,
    Geometry,
    GeometryDefinitions,
    GeometryFileDefinition,
    Header,
    Joint,
    Joints,
    // L3D model types (for 3D rendering)
    L3d,
    L3dFile,
    L3dModel,
    L3dPart,
    // XML structure types
    Luminaire,
    Mat4,
    Structure,
    Vec3f,
    MAT4_IDENTITY,
};

/// Normalize XML by removing or collapsing excess whitespace and trimming newlines
pub fn normalize_whitespace(xml: &str) -> String {
    // Remove all excess spaces around self-closing tags
    let re_self_closing = Regex::new(r"(\s+)/>").unwrap();
    let xml = re_self_closing.replace_all(xml, "/>").to_string();

    // Collapse multiple spaces into a single space between tags
    let re_collapse_spaces = Regex::new(r">\s+<").unwrap();
    let xml = re_collapse_spaces.replace_all(&xml, "><").to_string();

    // Trim leading/trailing spaces and newlines from the entire XML
    let xml = xml.trim();

    xml.to_string()
}

/// Trait for synchronous logging (useful for debugging in native environments)
pub trait Logger {
    fn log(&self, message: &str);
}

/// Trait for asynchronous logging (useful for WASM environments)
pub trait AsyncLogger {
    fn log(&self, message: &str) -> impl std::future::Future<Output = ()> + Send;
}

/// Implementation of Luminaire parsing and serialization methods
impl Luminaire {
    /// Detach the luminaire from any parent context (currently a no-op)
    pub fn detach(&mut self) -> Result<()> {
        Ok(())
    }

    /// Remove UTF-8 BOM (Byte Order Mark) from the beginning of a string
    ///
    /// Some XML files include a BOM which can interfere with parsing.
    pub fn remove_bom(s: &str) -> String {
        s.strip_prefix('\u{FEFF}').unwrap_or(s).to_string()
    }

    /// Sanitize an XML string for parsing
    ///
    /// This function:
    /// - Removes the UTF-8 BOM if present
    /// - Normalizes line endings (CRLF to LF)
    /// - Strips namespace declarations from the root element
    ///
    /// This allows parsing L3D files regardless of their XSD version.
    pub fn sanitize_xml_str(xml_str: &str) -> String {
        let cleaned_str = Self::remove_bom(xml_str);
        let cleaned_str = cleaned_str.replace("\r\n", "\n");
        let re = Regex::new(r"<Luminaire .*?>").unwrap();
        re.replace_all(&cleaned_str, "<Luminaire>").to_string()
    }

    /// Deserialize a Luminaire struct from an XML string
    ///
    /// # Example
    ///
    /// ```no_run
    /// use l3d_rs::Luminaire;
    ///
    /// let xml = r#"<Luminaire>...</Luminaire>"#;
    /// let luminaire = Luminaire::from_xml(xml).unwrap();
    /// ```
    pub fn from_xml(xml_str: &str) -> Result<Luminaire> {
        let my_xml_str = Self::sanitize_xml_str(xml_str);
        let loaded: Luminaire = from_xml_str(&my_xml_str)
            .map_err(anyhow::Error::msg)
            .context("Failed to parse XML string")?;
        Ok(loaded)
    }

    /// Serialize a Luminaire struct into an XML string
    ///
    /// # Example
    ///
    /// ```no_run
    /// use l3d_rs::Luminaire;
    ///
    /// let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();
    /// let xml = luminaire.to_xml().unwrap();
    /// ```
    pub fn to_xml(&self) -> Result<String> {
        let xml = quick_xml::se::to_string(self)
            .map_err(anyhow::Error::msg)
            .context("Failed to serialize to XML")?;
        Ok(xml)
    }

    /// Deserialize a Luminaire struct from a JSON string
    ///
    /// Useful for loading luminaires that were previously converted to JSON
    /// for storage or transmission.
    ///
    /// # Example
    ///
    /// ```no_run
    /// use l3d_rs::Luminaire;
    ///
    /// let json = r#"{"Header":...}"#;
    /// let luminaire = Luminaire::from_json(json).unwrap();
    /// ```
    pub fn from_json(json_data: &str) -> Result<Luminaire> {
        let luminaire: Luminaire = from_json_str(json_data)?;
        Ok(luminaire)
    }

    /// Serialize a Luminaire struct into a pretty-printed JSON string
    ///
    /// This is useful for:
    /// - Web transmission (smaller than XML)
    /// - Debugging (human-readable)
    /// - Storage in JSON-based databases
    ///
    /// # Example
    ///
    /// ```no_run
    /// use l3d_rs::Luminaire;
    ///
    /// let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();
    /// let json = luminaire.to_json().unwrap();
    /// println!("{}", json);
    /// ```
    pub fn to_json(&self) -> Result<String> {
        let json = to_json_str(self)?;
        Ok(json)
    }

    /// Extract the structure.xml content from an L3D file path
    ///
    /// This is a low-level function. For most use cases, use [`load_l3d`](Self::load_l3d)
    /// or [`from_buffer`] instead.
    pub fn get_xml_str_from_l3d(path: PathBuf) -> anyhow::Result<String> {
        let zipfile = StdFile::open(path)?;
        let mut zip = ZipArchive::new(zipfile)?;
        let mut xmlfile = zip.by_name("structure.xml")?;
        let mut xml_str = String::new();
        xmlfile.read_to_string(&mut xml_str)?;
        Ok(xml_str)
    }

    /// Load and parse a Luminaire from an L3D file path
    ///
    /// This is the recommended way to load L3D files in native (non-WASM) environments.
    /// For WASM or when you have the file as bytes, use [`from_buffer`] instead.
    ///
    /// # Arguments
    ///
    /// * `path` - Path to the .l3d file
    ///
    /// # Example
    ///
    /// ```no_run
    /// use l3d_rs::Luminaire;
    ///
    /// let luminaire = Luminaire::load_l3d("path/to/luminaire.l3d").unwrap();
    /// println!("Loaded luminaire from: {}", luminaire.path);
    /// ```
    pub fn load_l3d(path: &str) -> anyhow::Result<Luminaire> {
        let path_buf = Path::new(path).to_path_buf();
        let xml_str = Luminaire::get_xml_str_from_l3d(path_buf)
            .map_err(anyhow::Error::msg)
            .context("Failed to read L3D file")?;
        let mut loaded: Luminaire = Luminaire::from_xml(&xml_str)?;
        loaded.path = path.to_string();
        Ok(loaded)
    }

    /// Compare two XML strings for equality after normalization
    ///
    /// Useful for testing round-trip serialization.
    pub fn compare_xml(raw_xml: &str, generated_xml: &str) -> Result<(), String> {
        let raw_xml_clean = remove_xml_declaration(raw_xml);
        let generated_xml_clean = remove_xml_declaration(generated_xml);

        let raw_xml_sanitized = Luminaire::sanitize_xml_str(&raw_xml_clean);
        let generated_xml_sanitized = Luminaire::sanitize_xml_str(&generated_xml_clean);

        let _raw_xml_normalized = normalize_whitespace(&raw_xml_sanitized);
        let generated_xml_normalized = normalize_whitespace(&generated_xml_sanitized);
        let raw_xml_normalized = remove_specific_empty_elements(&generated_xml_normalized);

        if raw_xml_normalized == generated_xml_normalized {
            Ok(())
        } else {
            Err(format!(
                "The XML strings do not match!\n\nOriginal:\n{}\n\nGenerated:\n{}",
                raw_xml_normalized, generated_xml_normalized
            ))
        }
    }
}

/// Remove the XML declaration
pub fn remove_xml_declaration(xml: &str) -> String {
    xml.replace(r#"<?xml version="1.0" encoding="utf-8"?>"#, "")
}

/// Remove specific empty optional elements like `<Name/>`
fn remove_specific_empty_elements(xml: &str) -> String {
    // Remove empty <Name/> element
    let re_name = Regex::new(r"<Name\s*/>").unwrap(); // Matches <Name/>
    let xml = re_name.replace_all(xml, "").to_string();

    xml
}

// ============================================================================
// L3D File Parsing (ZIP-based format)
// ============================================================================

/// Parse an L3D file from a byte buffer
///
/// This is the **main entry point** for parsing L3D files, especially in WASM
/// environments where file paths are not available.
///
/// The function:
/// 1. Extracts the ZIP archive contents
/// 2. Parses `structure.xml` to understand the geometry hierarchy
/// 3. Builds transformation matrices for each geometry part
/// 4. Returns both the raw file data and the processed 3D model
///
/// # Arguments
///
/// * `l3d_buf` - The L3D file contents as a byte slice
///
/// # Returns
///
/// An [`L3d`] struct containing:
/// - `file.structure` - The raw XML content
/// - `file.assets` - All asset files (OBJ, textures, etc.)
/// - `model.parts` - Geometry parts with transformation matrices
///
/// # Example
///
/// ```no_run
/// use l3d_rs::{from_buffer, L3d};
///
/// // In a web app, you might get bytes from a file upload
/// let l3d_bytes = std::fs::read("luminaire.l3d").unwrap();
/// let l3d = from_buffer(&l3d_bytes);
///
/// // Check if parsing succeeded
/// if l3d.model.parts.is_empty() {
///     eprintln!("Failed to parse L3D file");
/// } else {
///     println!("Loaded {} parts", l3d.model.parts.len());
/// }
///
/// // Use with a 3D renderer
/// for part in &l3d.model.parts {
///     // part.path is like "geom_1/luminaire.obj"
///     // part.mat is the 4x4 transformation matrix
///     println!("Part: {} at {:?}", part.path, part.mat);
/// }
/// ```
///
/// # Integration with three-d
///
/// ```ignore
/// use three_d::Mat4 as ThreeDMat4;
///
/// let l3d = l3d_rs::from_buffer(&bytes);
/// for part in &l3d.model.parts {
///     let transform = ThreeDMat4::from_cols_array(&part.mat);
///     // Apply transform to loaded model...
/// }
/// ```
pub fn from_buffer(l3d_buf: &[u8]) -> L3d {
    match get_l3d_file(l3d_buf) {
        Ok(file) => {
            let mut l3d = parse_structure(&file.structure);
            l3d.file = file;
            l3d
        }
        Err(_e) => {
            // Return default on error - caller can check if model is empty
            L3d::default()
        }
    }
}

/// Extract L3D file contents from a ZIP buffer
///
/// Internal function that reads the ZIP archive and separates:
/// - `structure.xml` → stored in `L3dFile.structure`
/// - All other files → stored in `L3dFile.assets`
fn get_l3d_file(l3d_buf: &[u8]) -> std::io::Result<L3dFile> {
    let zip_buf = std::io::Cursor::new(l3d_buf);
    let mut zip = zip::ZipArchive::new(zip_buf)?;

    let mut l3d_file = L3dFile::default();
    for i in 0..zip.len() {
        let mut file = zip.by_index(i)?;
        if file.is_file() {
            let mut buf: Vec<u8> = Vec::new();
            file.read_to_end(&mut buf)?;
            if file.name() == "structure.xml" {
                l3d_file.structure = String::from_utf8_lossy(&buf).into_owned();
                continue;
            }
            let buf_file = BufFile {
                name: file.name().to_string(),
                content: buf,
                size: file.size(),
            };
            l3d_file.assets.push(buf_file);
        }
    }

    Ok(l3d_file)
}

/// Parse structure.xml and build the 3D model with transformation matrices
///
/// This function parses the XML and recursively processes the geometry tree,
/// computing the final transformation matrix for each part.
fn parse_structure(xml_data: &str) -> L3d {
    let luminaire: Luminaire = match Luminaire::from_xml(xml_data) {
        Ok(l) => l,
        Err(_e) => {
            return L3d::default();
        }
    };

    let files = &luminaire.geometry_definitions.geometry_file_definition;
    let geo = &luminaire.structure.geometry;
    let mut l3d_model = L3dModel { parts: Vec::new() };

    parse_geometry(files, geo, MAT4_IDENTITY, &mut l3d_model);

    L3d {
        file: L3dFile::default(),
        model: l3d_model,
    }
}

/// Recursively parse the geometry tree and build parts with transformations
///
/// L3D files can have hierarchical geometry with joints (for articulated luminaires).
/// This function walks the tree and computes the combined transformation matrix
/// for each geometry part by multiplying parent transforms.
fn parse_geometry(
    files: &[GeometryFileDefinition],
    geo: &Geometry,
    parent_mat: Mat4,
    model: &mut L3dModel,
) {
    // Find the OBJ file for this geometry and get the unit scale
    let (path, scale) = find_obj(files, &geo.geometry_reference.geometry_id);

    // Build the transformation for this geometry
    let mat_geo = build_transform(&geo.position, &geo.rotation);
    let mat_scale = mat4_scale(scale);
    let mat_final = mat4_mul(&parent_mat, &mat_geo);

    // Process child geometries through joints (for articulated luminaires)
    if let Some(j) = &geo.joints {
        for joint in &j.joint {
            let mat_joint = build_transform(&joint.position, &joint.rotation);
            let mat_combined = mat4_mul(&mat_final, &mat_joint);
            for child_geo in &joint.geometries.geometry {
                parse_geometry(files, child_geo, mat_combined, model);
            }
        }
    }

    // Add this geometry part with its final transformation
    model.parts.push(L3dPart {
        path,
        mat: mat4_mul(&mat_final, &mat_scale),
    });
}

/// Find geometry file by ID and return the path with scale factor
///
/// Returns a tuple of:
/// - Path in format "geometry_id/filename.obj"
/// - Scale factor based on the unit (mm → 0.001, in → 0.0254, m → 1.0)
fn find_obj(files: &[GeometryFileDefinition], id: &str) -> (String, f32) {
    for file in files {
        if file.id == id {
            return (
                format!("{}/{}", &file.id, &file.filename),
                get_scale(&file.units),
            );
        }
    }
    ("".to_string(), 1.0)
}
