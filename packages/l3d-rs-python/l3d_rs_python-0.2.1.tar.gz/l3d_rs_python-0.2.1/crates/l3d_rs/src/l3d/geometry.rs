// src/geometry.rs

use super::lightemitting::{LightEmittingObjects, LightEmittingSurfaces};
use super::structure::{Joints, Vec3f};
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct GeometryDefinitions {
    pub geometry_file_definition: Vec<GeometryFileDefinition>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct GeometryFileDefinition {
    #[serde(rename = "@id")]
    pub id: String,
    #[serde(rename = "@filename")]
    pub filename: String,
    #[serde(rename = "@units")]
    pub units: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct Geometry {
    #[serde(rename = "@partName")]
    pub part_name: String,
    pub position: Vec3f,
    pub rotation: Vec3f,
    pub geometry_reference: GeometryReference,
    pub joints: Option<Joints>,
    pub light_emitting_objects: Option<LightEmittingObjects>,
    pub light_emitting_surfaces: Option<LightEmittingSurfaces>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct GeometryReference {
    #[serde(rename = "@geometryId")]
    pub geometry_id: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Geometries {
    #[serde(rename = "Geometry")]
    pub geometry: Vec<Geometry>,
}
