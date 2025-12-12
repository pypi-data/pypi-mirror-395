# jaxmesh

JAX-based mesh primitives and isosurface extraction.

## Installation

```bash
pip install jaxmesh
```

## Quick Start

```python
import jax.numpy as jnp
from jaxmesh import marching_tetrahedra, rectilinear_grid, save_mesh_as_ply

# Create a grid
x = jnp.linspace(-1, 1, 32)
coords = rectilinear_grid(x, x, x)

# Define a scalar field (sphere SDF)
field = jnp.sqrt(coords[..., 0]**2 + coords[..., 1]**2 + coords[..., 2]**2) - 0.5

# Extract isosurface
mesh = marching_tetrahedra(field, coords, level=0.0)

# Save to file
save_mesh_as_ply(mesh, "sphere.ply")
```

## Features

### Mesh Types

- `SimplexMesh` - Base class for simplex meshes
- `TriMesh` - Triangle mesh with barycentric coordinates and gradients
- `TetMesh` - Tetrahedral mesh with barycentric utilities
- `QuadMesh` - Quad mesh convertible to triangles
- `HexMesh` - Hexahedral mesh convertible to tetrahedra

### Isosurface Extraction

- `marching_tetrahedra(field, coords, level)` - Extract triangle mesh from scalar field
- `rectilinear_grid(x, y, z)` - Create structured 3D grid coordinates
- `decimate_mesh(mesh, max_faces)` - Reduce mesh complexity

### Geometry Utilities

- `compute_vertex_normals(mesh)` - Per-vertex normals
- `triangle_barycentric_weights(vertices, point)` - Barycentric coordinates
- `tetra_barycentric_weights(vertices, point)` - Barycentric coordinates

### Level-Set Utilities

- `triangle_edge_intersections(values, level)` - Find edge crossings
- `tetra_edge_intersections(values, level)` - Find edge crossings
- `triangle_zero_segment(vertices, values, level)` - Extract level-set segment
- `tetra_zero_triangles(vertices, values, level)` - Extract level-set facets

### I/O

- `save_mesh_as_ply(mesh, path)` - ASCII PLY export with normals
- `save_mesh_as_glb(mesh, path)` - Binary glTF export

## License

MIT
