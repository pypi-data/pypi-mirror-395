//! # L3D Core Types
//!
//! This module contains the core types for representing L3D file structures.
//!
//! ## XML Structure Types
//!
//! These types map directly to the L3D XML schema:
//! - [`Luminaire`] - Root element containing the complete luminaire definition
//! - [`Header`] - Metadata (name, description, creation info)
//! - [`GeometryDefinitions`] - List of geometry file references
//! - [`Structure`] - Hierarchical geometry with positions and rotations
//!
//! ## 3D Model Types
//!
//! These types are used for 3D rendering:
//! - [`L3d`] - Complete parsed L3D data (file contents + model)
//! - [`L3dModel`] - Collection of geometry parts with transforms
//! - [`L3dPart`] - Single geometry part with transformation matrix
//! - [`Mat4`] - 4x4 transformation matrix (column-major `[f32; 16]`)
//!
//! ## Matrix Utilities
//!
//! Self-contained matrix functions (no external dependencies):
//! - [`mat4_mul`] - Matrix multiplication
//! - [`mat4_translation`], [`mat4_scale`] - Basic transforms
//! - [`mat4_rotate_x`], [`mat4_rotate_y`], [`mat4_rotate_z`] - Rotations
//! - [`build_transform`] - Build transform from position and rotation

pub mod geometry;
pub mod header;
pub mod lightemitting;
pub mod structure;

use serde::{Deserialize, Serialize};

pub use geometry::{Geometries, Geometry, GeometryDefinitions, GeometryFileDefinition};
pub use header::Header;
pub use structure::{Joint, Joints, Structure, Vec3f};

/// Root element representing a complete luminaire definition
///
/// This is the top-level structure parsed from `structure.xml` in an L3D file.
/// It contains:
/// - Header metadata (name, description, creation info)
/// - Geometry file definitions (references to OBJ files)
/// - Hierarchical structure with positions and rotations
///
/// # Example
///
/// ```no_run
/// use l3d_rs::Luminaire;
///
/// // Load from file
/// let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();
///
/// // Convert to JSON for web transmission
/// let json = luminaire.to_json().unwrap();
///
/// // Parse back from JSON
/// let restored = Luminaire::from_json(&json).unwrap();
/// ```
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "PascalCase")]
pub struct Luminaire {
    /// Header containing metadata about the luminaire
    pub header: Header,
    /// Definitions of geometry files (OBJ references)
    pub geometry_definitions: GeometryDefinitions,
    /// Hierarchical structure with geometry positions and rotations
    pub structure: Structure,
    /// Path to the source L3D file (set by `load_l3d`, not serialized)
    #[serde(skip)]
    pub path: String,
}

// ============================================================================
// L3D Model Types (for 3D rendering without three-d dependency)
// ============================================================================

/// 4x4 transformation matrix in column-major order
///
/// This is a standard OpenGL-compatible matrix format stored as `[f32; 16]`.
/// The layout is:
///
/// ```text
/// [ m0  m4  m8  m12 ]   [ Xx  Yx  Zx  Tx ]
/// [ m1  m5  m9  m13 ] = [ Xy  Yy  Zy  Ty ]
/// [ m2  m6  m10 m14 ]   [ Xz  Yz  Zz  Tz ]
/// [ m3  m7  m11 m15 ]   [ 0   0   0   1  ]
/// ```
///
/// # Conversion to three-d
///
/// ```ignore
/// use three_d::Mat4 as ThreeDMat4;
/// use l3d_rs::Mat4;
///
/// fn to_three_d(mat: &Mat4) -> ThreeDMat4 {
///     ThreeDMat4::from_cols_array(mat)
/// }
/// ```
pub type Mat4 = [f32; 16];

/// Identity matrix constant
///
/// Use this as the starting point for transformation chains:
///
/// ```
/// use l3d_rs::{MAT4_IDENTITY, mat4_mul, mat4_translation};
///
/// let transform = mat4_mul(&MAT4_IDENTITY, &mat4_translation(1.0, 2.0, 3.0));
/// ```
pub const MAT4_IDENTITY: Mat4 = [
    1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0,
];

/// A single geometry part with its world transformation
///
/// Each part represents one OBJ file that should be rendered with the
/// given transformation matrix applied.
///
/// # Fields
///
/// - `path` - Path to the OBJ file within the L3D archive (e.g., "geom_1/luminaire.obj")
/// - `mat` - 4x4 transformation matrix including position, rotation, and scale
///
/// # Example
///
/// ```ignore
/// use l3d_rs::L3dPart;
/// use three_d::Mat4 as ThreeDMat4;
///
/// fn render_part(part: &L3dPart, assets: &RawAssets) {
///     let model = assets.deserialize::<CpuModel>(&part.path).unwrap();
///     let transform = ThreeDMat4::from_cols_array(&part.mat);
///     // Apply transform to model...
/// }
/// ```
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct L3dPart {
    /// Path to the geometry file (e.g., "geom_1/luminaire.obj")
    pub path: String,
    /// 4x4 transformation matrix (column-major order)
    pub mat: Mat4,
}

/// Collection of geometry parts that make up the 3D model
///
/// This is the result of parsing the L3D structure and computing
/// transformation matrices for each geometry part.
///
/// # Example
///
/// ```no_run
/// use l3d_rs::from_buffer;
///
/// let l3d = from_buffer(&std::fs::read("luminaire.l3d").unwrap());
///
/// println!("Model has {} parts:", l3d.model.parts.len());
/// for part in &l3d.model.parts {
///     println!("  - {}", part.path);
/// }
/// ```
#[derive(Debug, Default, Serialize, Deserialize)]
pub struct L3dModel {
    /// List of geometry parts with their transformations
    pub parts: Vec<L3dPart>,
}

/// A file extracted from the L3D ZIP archive
///
/// This represents any file from the archive except `structure.xml`,
/// typically OBJ geometry files, MTL material files, or textures.
///
/// # Example
///
/// ```ignore
/// use l3d_rs::BufFile;
/// use three_d_asset::io::RawAssets;
///
/// fn load_assets(assets: &[BufFile]) -> RawAssets {
///     let mut raw = RawAssets::new();
///     for asset in assets {
///         raw.insert(&asset.name, asset.content.clone());
///     }
///     raw
/// }
/// ```
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct BufFile {
    /// File name/path within the archive (e.g., "geom_1/luminaire.obj")
    pub name: String,
    /// Raw file contents as bytes
    pub content: Vec<u8>,
    /// File size in bytes
    pub size: u64,
}

/// Raw L3D file contents extracted from the ZIP archive
///
/// Contains both the structure XML and all asset files.
///
/// # Fields
///
/// - `structure` - The raw XML content from `structure.xml`
/// - `assets` - All other files (OBJ, MTL, textures, etc.)
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct L3dFile {
    /// Raw XML content from structure.xml
    pub structure: String,
    /// Asset files (geometry, materials, textures)
    pub assets: Vec<BufFile>,
}

/// Complete L3D data with both raw file contents and parsed 3D model
///
/// This is the main result type from [`crate::from_buffer`]. It contains:
/// - The raw file data for asset loading
/// - The parsed model with pre-computed transformation matrices
///
/// # Example
///
/// ```no_run
/// use l3d_rs::{from_buffer, L3d};
///
/// let bytes = std::fs::read("luminaire.l3d").unwrap();
/// let l3d: L3d = from_buffer(&bytes);
///
/// // Check if parsing succeeded
/// if l3d.model.parts.is_empty() {
///     eprintln!("Failed to parse L3D or no geometry found");
/// }
///
/// // Access raw structure XML
/// println!("Structure: {} bytes", l3d.file.structure.len());
///
/// // List assets
/// for asset in &l3d.file.assets {
///     println!("Asset: {} ({} bytes)", asset.name, asset.size);
/// }
///
/// // Render each part
/// for part in &l3d.model.parts {
///     println!("Render {} with matrix {:?}", part.path, part.mat);
/// }
/// ```
#[derive(Debug, Default, Serialize, Deserialize)]
pub struct L3d {
    /// Raw file contents (structure.xml and assets)
    pub file: L3dFile,
    /// Parsed 3D model with transformation matrices
    pub model: L3dModel,
}

// ============================================================================
// Matrix Operations (no external dependencies)
// ============================================================================

/// Multiply two 4x4 matrices
///
/// Performs standard matrix multiplication: `result = a * b`
///
/// Both matrices must be in column-major order.
///
/// # Example
///
/// ```
/// use l3d_rs::{mat4_mul, mat4_translation, mat4_rotate_z};
///
/// // Combine translation and rotation
/// let translate = mat4_translation(1.0, 0.0, 0.0);
/// let rotate = mat4_rotate_z(45.0);
/// let combined = mat4_mul(&translate, &rotate);
/// ```
pub fn mat4_mul(a: &Mat4, b: &Mat4) -> Mat4 {
    let mut result = [0.0f32; 16];
    for col in 0..4 {
        for row in 0..4 {
            let mut sum = 0.0;
            for k in 0..4 {
                sum += a[k * 4 + row] * b[col * 4 + k];
            }
            result[col * 4 + row] = sum;
        }
    }
    result
}

/// Create a translation matrix
///
/// # Arguments
///
/// * `x`, `y`, `z` - Translation offset in each axis
///
/// # Example
///
/// ```
/// use l3d_rs::mat4_translation;
///
/// let translate = mat4_translation(1.0, 2.0, 3.0);
/// // Position at (1, 2, 3)
/// ```
pub fn mat4_translation(x: f32, y: f32, z: f32) -> Mat4 {
    [
        1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, x, y, z, 1.0,
    ]
}

/// Create a uniform scale matrix
///
/// # Arguments
///
/// * `s` - Scale factor (1.0 = no change, 0.5 = half size, 2.0 = double)
///
/// # Example
///
/// ```
/// use l3d_rs::mat4_scale;
///
/// let half_size = mat4_scale(0.5);
/// let double_size = mat4_scale(2.0);
/// ```
pub fn mat4_scale(s: f32) -> Mat4 {
    [
        s, 0.0, 0.0, 0.0, 0.0, s, 0.0, 0.0, 0.0, 0.0, s, 0.0, 0.0, 0.0, 0.0, 1.0,
    ]
}

/// Create a rotation matrix around the X axis
///
/// # Arguments
///
/// * `deg` - Rotation angle in degrees (positive = counter-clockwise when looking down the axis)
///
/// # Example
///
/// ```
/// use l3d_rs::mat4_rotate_x;
///
/// let rotate_90 = mat4_rotate_x(90.0);
/// ```
pub fn mat4_rotate_x(deg: f32) -> Mat4 {
    let rad = deg * std::f32::consts::PI / 180.0;
    let c = rad.cos();
    let s = rad.sin();
    [
        1.0, 0.0, 0.0, 0.0, 0.0, c, s, 0.0, 0.0, -s, c, 0.0, 0.0, 0.0, 0.0, 1.0,
    ]
}

/// Create a rotation matrix around the Y axis
///
/// # Arguments
///
/// * `deg` - Rotation angle in degrees
///
/// # Example
///
/// ```
/// use l3d_rs::mat4_rotate_y;
///
/// let rotate_45 = mat4_rotate_y(45.0);
/// ```
pub fn mat4_rotate_y(deg: f32) -> Mat4 {
    let rad = deg * std::f32::consts::PI / 180.0;
    let c = rad.cos();
    let s = rad.sin();
    [
        c, 0.0, -s, 0.0, 0.0, 1.0, 0.0, 0.0, s, 0.0, c, 0.0, 0.0, 0.0, 0.0, 1.0,
    ]
}

/// Create a rotation matrix around the Z axis
///
/// # Arguments
///
/// * `deg` - Rotation angle in degrees
///
/// # Example
///
/// ```
/// use l3d_rs::mat4_rotate_z;
///
/// let rotate_180 = mat4_rotate_z(180.0);
/// ```
pub fn mat4_rotate_z(deg: f32) -> Mat4 {
    let rad = deg * std::f32::consts::PI / 180.0;
    let c = rad.cos();
    let s = rad.sin();
    [
        c, s, 0.0, 0.0, -s, c, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0,
    ]
}

/// Convert a unit string to a scale factor
///
/// L3D files can specify geometry in different units. This function
/// returns the scale factor to convert to meters.
///
/// # Supported Units
///
/// - `"mm"` → 0.001 (millimeters to meters)
/// - `"in"` → 0.0254 (inches to meters)
/// - `"m"` or any other → 1.0 (already in meters)
///
/// # Example
///
/// ```
/// use l3d_rs::get_scale;
///
/// assert_eq!(get_scale("mm"), 0.001);
/// assert_eq!(get_scale("in"), 0.0254);
/// assert_eq!(get_scale("m"), 1.0);
/// ```
pub fn get_scale(unit: &str) -> f32 {
    match unit {
        "mm" => 0.001,
        "in" => 2.54 / 100.0,
        _ => 1.0,
    }
}

/// Build a transformation matrix from position and rotation vectors
///
/// Creates a combined transformation by:
/// 1. Translating to position (x, y, z)
/// 2. Rotating around X axis
/// 3. Rotating around Y axis
/// 4. Rotating around Z axis
///
/// This matches the L3D specification for how position and rotation
/// are combined.
///
/// # Arguments
///
/// * `pos` - Position vector (translation)
/// * `rot` - Rotation vector (Euler angles in degrees)
///
/// # Example
///
/// ```
/// use l3d_rs::{build_transform, Vec3f};
///
/// // Note: In real code, Vec3f comes from parsing
/// // This is just for illustration
/// ```
pub fn build_transform(pos: &Vec3f, rot: &Vec3f) -> Mat4 {
    let m1 = mat4_translation(pos.x, pos.y, pos.z);
    let m2 = mat4_rotate_x(rot.x);
    let m3 = mat4_rotate_y(rot.y);
    let m4 = mat4_rotate_z(rot.z);
    mat4_mul(&mat4_mul(&mat4_mul(&m1, &m2), &m3), &m4)
}
