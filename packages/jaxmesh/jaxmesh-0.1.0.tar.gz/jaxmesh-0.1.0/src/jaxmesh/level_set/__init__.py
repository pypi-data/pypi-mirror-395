"""Level-set utilities."""

from __future__ import annotations

from .crossings import (
    TRI_EDGES,
    TET_EDGES,
    EdgeIntersection,
    triangle_edge_intersections,
    tetra_edge_intersections,
    triangle_zero_segment,
    tetra_zero_triangles,
)

__all__ = [
    "TRI_EDGES",
    "TET_EDGES",
    "EdgeIntersection",
    "triangle_edge_intersections",
    "tetra_edge_intersections",
    "triangle_zero_segment",
    "tetra_zero_triangles",
]
