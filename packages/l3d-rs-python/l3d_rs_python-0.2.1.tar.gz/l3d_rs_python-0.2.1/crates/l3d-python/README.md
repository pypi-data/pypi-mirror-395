# l3d-rs-python

[![PyPI](https://img.shields.io/pypi/v/l3d-rs-python.svg)](https://pypi.org/project/l3d-rs-python/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python bindings for [l3d_rs](https://crates.io/crates/l3d_rs) - a Rust library for parsing L3D (Luminaire 3D) files.

## Installation

```bash
pip install l3d-rs-python
```

## Quick Start

```python
import l3d

# Parse from file
data = l3d.from_file("luminaire.l3d")

# Or from bytes
with open("luminaire.l3d", "rb") as f:
    data = l3d.from_bytes(f.read())

# Access the parsed data
print(f"Parts: {len(data['model']['parts'])}")
print(f"Assets: {len(data['file']['assets'])}")

# Each part has a path and transformation matrix
for part in data['model']['parts']:
    print(f"  {part['path']}: {len(part['mat'])} matrix values")

# Access raw asset data
for asset in data['file']['assets']:
    print(f"  {asset['name']}: {asset['size']} bytes")
```

## API

### `l3d.from_file(path: str) -> dict`

Parse an L3D file from a file path.

### `l3d.from_bytes(data: bytes) -> dict`

Parse an L3D file from bytes.

### Return Value

Both functions return a dictionary with the following structure:

```python
{
    "model": {
        "parts": [
            {
                "path": "geometry/lamp.obj",
                "mat": [1.0, 0.0, 0.0, 0.0, ...]  # 16 floats (4x4 matrix)
            },
            ...
        ]
    },
    "file": {
        "assets": [
            {
                "name": "geometry/lamp.obj",
                "size": 12345,
                "content": b"..."  # Raw bytes
            },
            ...
        ]
    }
}
```

## What is L3D?

L3D is a ZIP-based file format for 3D luminaire geometry, used in the lighting industry alongside [GLDF](https://gldf.io). It contains:

- `structure.xml` - Geometry hierarchy with transformation matrices
- OBJ files - 3D mesh data
- Optional textures and materials

## License

GPL-3.0-or-later

## Related

- [l3d_rs](https://crates.io/crates/l3d_rs) - Core Rust library
- [l3d-egui](https://crates.io/crates/l3d-egui) - 3D Viewer (Desktop & WASM)
- [GLDF](https://gldf.io) - Global Lighting Data Format
