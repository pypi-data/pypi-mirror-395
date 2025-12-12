"""jaxmesh - JAX-based mesh primitives and isosurface extraction.

A minimal library providing:
- Simplex mesh types (TriMesh, TetMesh) with barycentric coordinate utilities
- Structured mesh types (QuadMesh, HexMesh) with simplex conversion
- Marching tetrahedra isosurface extraction
- Level-set crossing utilities
- PLY and GLB mesh export
"""

from __future__ import annotations

# Mesh types
from jaxmesh.mesh import (
    SimplexMesh,
    TriMesh,
    TetMesh,
    QuadMesh,
    HexMesh,
)

# Output mesh type from isosurface extraction
from jaxmesh.geometry.normals import TriangleMesh

# Isosurface extraction
from jaxmesh.isosurface import (
    marching_tetrahedra,
    rectilinear_grid,
    decimate_mesh,
)

# Geometry utilities
from jaxmesh.geometry import (
    compute_vertex_normals,
    triangle_barycentric_weights,
    tetra_barycentric_weights,
)

# Level-set utilities
from jaxmesh.level_set import (
    EdgeIntersection,
    TRI_EDGES,
    TET_EDGES,
    triangle_edge_intersections,
    tetra_edge_intersections,
    triangle_zero_segment,
    tetra_zero_triangles,
)

# I/O
from jaxmesh.io import (
    save_mesh_as_ply,
    save_mesh_as_glb,
)

__version__ = "0.1.0"

__all__ = [
    # Mesh types
    "SimplexMesh",
    "TriMesh",
    "TetMesh",
    "QuadMesh",
    "HexMesh",
    "TriangleMesh",
    # Isosurface
    "marching_tetrahedra",
    "rectilinear_grid",
    "decimate_mesh",
    # Geometry
    "compute_vertex_normals",
    "triangle_barycentric_weights",
    "tetra_barycentric_weights",
    # Level-set
    "EdgeIntersection",
    "TRI_EDGES",
    "TET_EDGES",
    "triangle_edge_intersections",
    "tetra_edge_intersections",
    "triangle_zero_segment",
    "tetra_zero_triangles",
    # I/O
    "save_mesh_as_ply",
    "save_mesh_as_glb",
]
