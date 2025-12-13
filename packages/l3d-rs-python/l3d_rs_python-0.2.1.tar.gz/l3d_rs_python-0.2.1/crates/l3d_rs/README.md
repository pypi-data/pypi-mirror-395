# l3d_rs

[![Crates.io](https://img.shields.io/crates/v/l3d_rs.svg)](https://crates.io/crates/l3d_rs)
[![Documentation](https://docs.rs/l3d_rs/badge.svg)](https://docs.rs/l3d_rs)
[![Rust](https://github.com/holg/l3d_rs/actions/workflows/rust.yml/badge.svg)](https://github.com/holg/l3d_rs/actions/workflows/rust.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Rust library for parsing L3D (Luminaire 3D) files, the 3D geometry format used in the lighting industry alongside [GLDF](https://gldf.io) (Global Lighting Data Format).

## What is L3D?

L3D is a ZIP-based file format containing:
- `structure.xml` - XML file describing the luminaire geometry hierarchy
- OBJ files - 3D geometry files for each part of the luminaire
- Optional texture and material files

The format supports hierarchical assemblies with joints, allowing for adjustable luminaire components (e.g., rotatable lamp heads).

## Features

- **XML Parsing**: Parse `structure.xml` into strongly-typed Rust structs
- **JSON Serialization**: Convert between L3D XML and JSON formats
- **3D Model Building**: Automatically compute transformation matrices for rendering
- **No 3D Engine Dependency**: Matrix operations are self-contained (`[f32; 16]`)
- **WASM Compatible**: Designed for WebAssembly targets and WebGL rendering

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
l3d_rs = "0.2"
```

## Quick Start

### Parse L3D from bytes (recommended for WASM)

```rust
use l3d_rs::{from_buffer, L3d};

// Load L3D file as bytes (e.g., from file upload or fetch)
let l3d_bytes = std::fs::read("luminaire.l3d").unwrap();

// Parse the L3D file
let l3d: L3d = from_buffer(&l3d_bytes);

// Access the parsed model
println!("Parts: {}", l3d.model.parts.len());
for part in &l3d.model.parts {
    println!("  {} with transform", part.path);
}

// Access raw assets for 3D rendering
for asset in &l3d.file.assets {
    println!("Asset: {} ({} bytes)", asset.name, asset.size);
}
```

### Load from file path (native only)

```rust
use l3d_rs::Luminaire;

// Load and parse the luminaire structure
let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();

// Convert to JSON for web transmission
let json = luminaire.to_json().unwrap();
println!("{}", json);
```

### JSON round-trip

```rust
use l3d_rs::Luminaire;

// Load L3D file
let luminaire = Luminaire::load_l3d("luminaire.l3d").unwrap();

// Convert to JSON
let json = luminaire.to_json().unwrap();

// Parse back from JSON
let restored = Luminaire::from_json(&json).unwrap();
```

## Integration with 3D Renderers

The `Mat4` type is a `[f32; 16]` array in column-major order, compatible with OpenGL, WebGL, and most 3D libraries.

### With three-d

```rust
use three_d::Mat4 as ThreeDMat4;
use l3d_rs::{from_buffer, L3dPart};

let l3d = from_buffer(&bytes);

for part in &l3d.model.parts {
    // Convert l3d_rs matrix to three-d matrix
    let transform = ThreeDMat4::from_cols_array(&part.mat);

    // Load the OBJ file from assets
    let obj_data = l3d.file.assets.iter()
        .find(|a| a.name == part.path)
        .map(|a| &a.content);

    // Apply transform to model...
}
```

### Loading assets into three-d-asset

```rust
use three_d_asset::io::RawAssets;
use l3d_rs::L3d;

fn load_assets(l3d: &L3d) -> RawAssets {
    let mut raw = RawAssets::new();
    for asset in &l3d.file.assets {
        raw.insert(&asset.name, asset.content.clone());
    }
    raw
}
```

## API Overview

### Main Types

| Type | Description |
|------|-------------|
| `L3d` | Complete parsed L3D data (file + model) |
| `L3dFile` | Raw file contents (structure.xml + assets) |
| `L3dModel` | Collection of geometry parts with transforms |
| `L3dPart` | Single geometry part with transformation matrix |
| `Luminaire` | Parsed XML structure (for serialization) |
| `Mat4` | 4x4 transformation matrix (`[f32; 16]`) |
| `BufFile` | Asset file from ZIP archive |

### Key Functions

| Function | Description |
|----------|-------------|
| `from_buffer(&[u8])` | Parse L3D from bytes (main entry point) |
| `Luminaire::load_l3d(path)` | Load L3D from file path |
| `Luminaire::from_json(str)` | Parse from JSON string |
| `Luminaire::to_json()` | Serialize to JSON string |
| `mat4_mul(a, b)` | Multiply two matrices |
| `mat4_translation(x, y, z)` | Create translation matrix |
| `mat4_rotate_x/y/z(deg)` | Create rotation matrix |

## Matrix Layout

The `Mat4` type uses column-major order (OpenGL convention):

```text
[ m0  m4  m8  m12 ]   [ Xx  Yx  Zx  Tx ]
[ m1  m5  m9  m13 ] = [ Xy  Yy  Zy  Ty ]
[ m2  m6  m10 m14 ]   [ Xz  Yz  Zz  Tz ]
[ m3  m7  m11 m15 ]   [ 0   0   0   1  ]
```

## License

This project is licensed under the GPL-3.0-or-later license. See the [LICENSE](LICENSE) file for details.

## Related Projects

- [GLDF](https://gldf.io) - Global Lighting Data Format
- [L3D Specification](https://github.com/globallightingdata/l3d) - Official L3D format specification
