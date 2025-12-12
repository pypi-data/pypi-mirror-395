"""Geometry utilities."""

from __future__ import annotations

from .barycentric import triangle_barycentric_weights, tetra_barycentric_weights
from .normals import TriangleMesh, compute_vertex_normals

__all__ = [
    "triangle_barycentric_weights",
    "tetra_barycentric_weights",
    "TriangleMesh",
    "compute_vertex_normals",
]
