"""Level-set crossing helpers for simplex meshes."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence, Tuple

import jax.numpy as jnp
import numpy as np


TRI_EDGES: Tuple[Tuple[int, int], ...] = ((0, 1), (1, 2), (2, 0))
TET_EDGES: Tuple[Tuple[int, int], ...] = (
    (0, 1),
    (1, 2),
    (2, 0),
    (0, 3),
    (1, 3),
    (2, 3),
)


@dataclass(frozen=True)
class EdgeIntersection:
    """Simple record describing an edge crossing on a simplex."""

    edge: Tuple[int, int]
    t: float


def triangle_edge_intersections(
    values: Sequence[float],
    *,
    level: float = 0.0,
) -> Tuple[EdgeIntersection, ...]:
    """Return all edge intersections for a triangle's level set."""
    shifted = jnp.asarray(values, dtype=jnp.float64) - float(level)
    if shifted.shape != (3,):
        raise ValueError("triangle values must have shape (3,)")
    intersections: list[EdgeIntersection] = []
    for edge in TRI_EDGES:
        t = _edge_parameter(float(shifted[edge[0]]), float(shifted[edge[1]]))
        if t is None:
            continue
        intersections.append(EdgeIntersection(edge=edge, t=t))
    return tuple(intersections)


def tetra_edge_intersections(
    values: Sequence[float],
    *,
    level: float = 0.0,
) -> Tuple[EdgeIntersection, ...]:
    """Return all edge intersections for a tetrahedron's level set."""
    shifted = jnp.asarray(values, dtype=jnp.float64) - float(level)
    if shifted.shape != (4,):
        raise ValueError("tetrahedron values must have shape (4,)")
    intersections: list[EdgeIntersection] = []
    for edge in TET_EDGES:
        t = _edge_parameter(float(shifted[edge[0]]), float(shifted[edge[1]]))
        if t is None:
            continue
        intersections.append(EdgeIntersection(edge=edge, t=t))
    return tuple(intersections)


def triangle_zero_segment(
    vertices: Sequence[Sequence[float]],
    values: Sequence[float],
    *,
    level: float = 0.0,
) -> tuple[jnp.ndarray, jnp.ndarray] | None:
    """Return the intersection segment of a level set with a triangle, if any."""
    pts = _intersections_to_points(vertices, triangle_edge_intersections(values, level=level))
    if len(pts) < 2:
        return None
    return pts[0], pts[1]


def tetra_zero_triangles(
    vertices: Sequence[Sequence[float]],
    values: Sequence[float],
    *,
    level: float = 0.0,
) -> Tuple[jnp.ndarray, ...]:
    """Return the triangle facets carved by a level set inside a tetrahedron."""
    points = _intersections_to_points(vertices, tetra_edge_intersections(values, level=level))
    if len(points) < 3:
        return ()

    unique_points = _unique_points(points)
    if len(unique_points) < 3:
        return ()
    if len(unique_points) == 3:
        return (jnp.stack(unique_points, axis=0),)

    ordered = _order_convex_polygon(unique_points)
    if len(ordered) == 3:
        return (jnp.stack(ordered, axis=0),)
    if len(ordered) != 4:
        # Fallback: triangulate arbitrary ordering if degeneracy reduced polygon size.
        return (jnp.stack(unique_points[:3], axis=0),)
    tri1 = jnp.stack((ordered[0], ordered[1], ordered[2]), axis=0)
    tri2 = jnp.stack((ordered[0], ordered[2], ordered[3]), axis=0)
    return (tri1, tri2)


def _edge_parameter(va: float, vb: float) -> float | None:
    if va == vb == 0.0:
        return None
    if (va < 0 and vb < 0) or (va > 0 and vb > 0):
        return None
    denominator = va - vb
    if denominator == 0.0:
        return 0.5
    t = va / denominator
    return float(jnp.clip(t, 0.0, 1.0))


def _intersections_to_points(
    vertices: Sequence[Sequence[float]],
    intersections: Iterable[EdgeIntersection],
) -> list[jnp.ndarray]:
    verts = jnp.asarray(vertices, dtype=jnp.float64)
    points: list[jnp.ndarray] = []
    for intersection in intersections:
        i, j = intersection.edge
        vi = verts[i]
        vj = verts[j]
        t = intersection.t
        point = (1.0 - t) * vi + t * vj
        points.append(point)
    return points


def _unique_points(points: Sequence[jnp.ndarray], tol: float = 1e-9) -> list[jnp.ndarray]:
    unique: list[jnp.ndarray] = []
    for point in points:
        if not any(float(jnp.linalg.norm(point - existing)) <= tol for existing in unique):
            unique.append(point)
    return unique


def _order_convex_polygon(points: Sequence[jnp.ndarray]) -> list[jnp.ndarray]:
    centroid = jnp.mean(jnp.stack(points, axis=0), axis=0)
    centered = [point - centroid for point in points]
    normal = _polygon_normal(centered)
    if normal is None:
        return list(points)
    u = None
    for vec in centered:
        candidate = _normalize(vec)
        if candidate is not None:
            u = candidate
            break
    if u is None:
        return list(points)
    v = _normalize(jnp.cross(normal, u))
    if v is None:
        return list(points)
    angles = []
    for point in centered:
        x = float(jnp.dot(point, u))
        y = float(jnp.dot(point, v))
        angles.append(float(jnp.arctan2(y, x)))
    order = np.argsort(angles)
    return [points[int(idx)] for idx in order]


def _polygon_normal(centered: Sequence[jnp.ndarray]) -> jnp.ndarray | None:
    for a, b, c in combinations(centered, 3):
        normal = jnp.cross(b - a, c - a)
        norm = float(jnp.linalg.norm(normal))
        if norm > 1e-12:
            return normal / norm
    return None


def _normalize(vector: jnp.ndarray) -> jnp.ndarray | None:
    norm = float(jnp.linalg.norm(vector))
    if norm <= 1e-12:
        return None
    return vector / norm


__all__ = [
    "TRI_EDGES",
    "TET_EDGES",
    "EdgeIntersection",
    "triangle_edge_intersections",
    "tetra_edge_intersections",
    "triangle_zero_segment",
    "tetra_zero_triangles",
]
