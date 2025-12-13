use super::structure::{Circle, Rectangle, Vec3f};
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct LightEmittingObjects {
    light_emitting_object: Vec<LightEmittingObject>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct LightEmittingObject {
    #[serde(rename = "@partName")]
    part_name: String,
    position: Vec3f,
    rotation: Vec3f,
    rectangle: Option<Rectangle>,
    circle: Option<Circle>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct LightEmittingObjectReference {
    #[serde(rename = "@lightEmittingPartName")]
    light_emitting_part_name: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct LightEmittingSurfaces {
    light_emitting_surface: Vec<LightEmittingSurface>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct LightEmittingSurface {
    #[serde(rename = "@partName")]
    part_name: String,
    light_emitting_object_reference: LightEmittingObjectReference,
    face_assignments: FaceAssignments,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
struct FaceAssignments {
    face_assignment: Option<Vec<FaceAssignment>>,
    face_range_assignment: Option<Vec<FaceRangeAssignment>>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct FaceAssignment {
    #[serde(rename = "@faceIndex")]
    face_index: usize,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct FaceRangeAssignment {
    #[serde(rename = "@faceIndexBegin")]
    face_index_begin: usize,
    #[serde(rename = "@faceIndexEnd")]
    face_index_end: usize,
}
