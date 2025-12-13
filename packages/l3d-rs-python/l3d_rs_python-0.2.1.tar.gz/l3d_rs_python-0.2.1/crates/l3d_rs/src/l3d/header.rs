// src/header.rs

use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(rename_all = "PascalCase")]
pub struct Header {
    name: Option<String>,
    description: Option<String>,
    created_with_application: String,
    creation_time_code: String,
    format_version: Option<FormatVersion>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
struct FormatVersion {
    #[serde(rename = "@major")]
    major: u8,
    #[serde(rename = "@minor")]
    minor: u8,
    #[serde(rename = "@pre-release")]
    pre_release: Option<u8>,
}
