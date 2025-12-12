"""Normal computation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TriangleMesh:
    """Triangle mesh produced by marching tetrahedra."""

    vertices: np.ndarray  # (n_vertices, 3)
    faces: np.ndarray  # (n_faces, 3) int indices into vertices


def _compute_face_normals(verts: np.ndarray, faces: np.ndarray) -> np.ndarray:
    v0 = verts[faces[:, 0]]
    v1 = verts[faces[:, 1]]
    v2 = verts[faces[:, 2]]
    return np.cross(v1 - v0, v2 - v0)


def compute_vertex_normals(mesh: TriangleMesh, eps: float = 1e-9) -> np.ndarray:
    """Return per-vertex normals normalised to unit length."""
    verts = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces, dtype=np.int64)
    if verts.size == 0 or faces.size == 0:
        return np.zeros_like(verts)
    face_normals = _compute_face_normals(verts, faces)
    vert_normals = np.zeros_like(verts)
    # Accumulate normals per vertex. Broadcast each face normal to its vertices.
    np.add.at(vert_normals, faces.reshape(-1), np.repeat(face_normals, 3, axis=0))
    norms = np.linalg.norm(vert_normals, axis=1, keepdims=True)
    norms = np.clip(norms, eps, None)
    return vert_normals / norms


__all__ = [
    "TriangleMesh",
    "compute_vertex_normals",
]
