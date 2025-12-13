use crate::from_buffer;
use crate::l3d::Luminaire;

/// Minimal L3D test file included in the repository
const TEST_L3D_PATH: &str = "tests/data/minimal.l3d";

#[test]
fn test_l3d_load_and_json_roundtrip() {
    // Load and deserialize the .l3d file into Luminaire
    let loaded = Luminaire::load_l3d(TEST_L3D_PATH).expect("Failed to load L3D file");

    // Serialize to JSON
    let json_data = loaded.to_json().expect("Failed to serialize to JSON");

    // Deserialize the JSON back into the Rust struct
    let luminaire_from_json: Luminaire =
        Luminaire::from_json(&json_data).expect("Failed to deserialize from JSON");

    // Serialize again to JSON and compare
    let json_data_roundtrip = luminaire_from_json
        .to_json()
        .expect("Failed to serialize to JSON");

    assert_eq!(json_data, json_data_roundtrip, "JSON roundtrip failed");
}

#[test]
fn test_from_buffer_parses_model() {
    // Load the L3D file as bytes
    let l3d_bytes = std::fs::read(TEST_L3D_PATH).expect("Failed to read L3D file");

    // Parse using from_buffer
    let l3d = from_buffer(&l3d_bytes);

    // Verify structure.xml was parsed
    assert!(
        !l3d.file.structure.is_empty(),
        "structure.xml should not be empty"
    );

    // Verify model parts were created
    assert!(
        !l3d.model.parts.is_empty(),
        "Model should have at least one part"
    );

    // Verify first part has a valid path
    let first_part = &l3d.model.parts[0];
    assert!(!first_part.path.is_empty(), "Part should have a path");
    assert!(
        first_part.path.ends_with(".obj"),
        "Part path should end with .obj"
    );

    // Verify assets were loaded
    assert!(!l3d.file.assets.is_empty(), "Should have asset files");
}
