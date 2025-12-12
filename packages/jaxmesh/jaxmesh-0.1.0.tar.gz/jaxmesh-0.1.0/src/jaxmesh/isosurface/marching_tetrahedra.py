"""Marching tetrahedra isosurface extraction using JAX."""

from __future__ import annotations

from typing import Sequence

import jax
import jax.numpy as jnp
import numpy as np

from ..geometry.normals import TriangleMesh


# Tetrahedralization using the long diagonal (corner 0 -> 6)
_TETRA_CORNER_IDX = jnp.array(
    [
        (0, 5, 1, 6),
        (0, 5, 6, 4),
        (0, 6, 2, 1),
        (0, 6, 3, 2),
        (0, 6, 7, 3),
        (0, 6, 4, 7),
    ],
    dtype=jnp.int32,
)

# Edge definitions for a tetrahedron listing vertex pairs (by local indices)
_TETRA_EDGE_VERTS = jnp.array(
    [
        (0, 1),
        (1, 2),
        (2, 0),
        (0, 3),
        (1, 3),
        (2, 3),
    ],
    dtype=jnp.int32,
)

# Case lookup: up to two triangles (each defined by three edge indices)
# -1 marks the absence of a triangle/edge in that slot.
_TRIANGLE_EDGE_TABLE = jnp.array(
    [
        (-1, -1, -1, -1, -1, -1),
        (0, 3, 2, -1, -1, -1),
        (0, 1, 4, -1, -1, -1),
        (1, 4, 2, 2, 4, 3),
        (1, 2, 5, -1, -1, -1),
        (0, 3, 5, 0, 5, 1),
        (0, 2, 5, 0, 5, 4),
        (5, 4, 3, -1, -1, -1),
        (3, 4, 5, -1, -1, -1),
        (0, 4, 5, 0, 5, 2),
        (0, 1, 5, 0, 5, 3),
        (1, 5, 2, -1, -1, -1),
        (1, 3, 4, 1, 2, 3),
        (0, 3, 4, -1, -1, -1),
        (0, 2, 3, -1, -1, -1),
        (-1, -1, -1, -1, -1, -1),
    ],
    dtype=jnp.int32,
).reshape(16, 2, 3)

_CASE_BITS = jnp.array([1, 2, 4, 8], dtype=jnp.int32)


def rectilinear_grid(
    x: Sequence[float],
    y: Sequence[float],
    z: Sequence[float],
) -> jnp.ndarray:
    """Return coordinates of a rectilinear grid (indexing='ij')."""
    X, Y, Z = jnp.meshgrid(jnp.asarray(x), jnp.asarray(y), jnp.asarray(z), indexing="ij")
    return jnp.stack([X, Y, Z], axis=-1)


def _prepare_tetrahedra(
    coords: jnp.ndarray,
    field: jnp.ndarray,
) -> tuple[jnp.ndarray, jnp.ndarray]:
    """Convert a structured grid into flattened tetrahedra."""
    if coords.ndim != 4 or coords.shape[-1] != 3:
        raise ValueError("coords must have shape (nx, ny, nz, 3)")
    if field.shape != coords.shape[:-1]:
        raise ValueError("field must have shape (nx, ny, nz)")

    nx, ny, nz, _ = coords.shape
    if min(nx, ny, nz) < 2:
        return jnp.zeros((0, 4, 3), coords.dtype), jnp.zeros((0, 4), field.dtype)

    corners = (
        coords[:-1, :-1, :-1],
        coords[1:, :-1, :-1],
        coords[1:, 1:, :-1],
        coords[:-1, 1:, :-1],
        coords[:-1, :-1, 1:],
        coords[1:, :-1, 1:],
        coords[1:, 1:, 1:],
        coords[:-1, 1:, 1:],
    )
    cube_coords = jnp.stack(corners, axis=-2)  # (..., 8, 3)

    value_corners = (
        field[:-1, :-1, :-1],
        field[1:, :-1, :-1],
        field[1:, 1:, :-1],
        field[:-1, 1:, :-1],
        field[:-1, :-1, 1:],
        field[1:, :-1, 1:],
        field[1:, 1:, 1:],
        field[:-1, 1:, 1:],
    )
    cube_values = jnp.stack(value_corners, axis=-1)  # (..., 8)

    cube_coords_flat = cube_coords.reshape(-1, 8, 3)
    cube_values_flat = cube_values.reshape(-1, 8)

    tet_coords = jnp.take(cube_coords_flat, _TETRA_CORNER_IDX, axis=1)
    tet_values = jnp.take(cube_values_flat, _TETRA_CORNER_IDX, axis=1)

    return tet_coords.reshape(-1, 4, 3), tet_values.reshape(-1, 4)


def _interpolate_point(
    verts: jnp.ndarray,
    values: jnp.ndarray,
    edge_idx: int,
    level: jnp.ndarray,
) -> jnp.ndarray:
    i0, i1 = _TETRA_EDGE_VERTS[edge_idx]
    p0 = verts[i0]
    p1 = verts[i1]
    v0 = values[i0]
    v1 = values[i1]
    denom = v1 - v0
    t = jnp.where(jnp.abs(denom) > 1e-12, (level - v0) / denom, 0.5)
    t = jnp.clip(t, 0.0, 1.0)
    return p0 + t * (p1 - p0)


def _march_single(verts: jnp.ndarray, values: jnp.ndarray, level: float) -> tuple[jnp.ndarray, jnp.ndarray]:
    lvl = jnp.asarray(level, dtype=values.dtype)
    inside = values < lvl
    case = jnp.sum(jnp.where(inside, _CASE_BITS, 0), axis=0).astype(jnp.int32)

    tri_edges = _TRIANGLE_EDGE_TABLE[case]
    valid = jnp.any(tri_edges >= 0, axis=-1)
    safe_edges = jnp.where(tri_edges >= 0, tri_edges, 0)

    interpolate_edge = jax.vmap(lambda e: _interpolate_point(verts, values, e, lvl))
    interpolate_triangle = jax.vmap(interpolate_edge)
    tri_points = interpolate_triangle(safe_edges)
    return tri_points, valid


_march_single_jit = jax.jit(_march_single, static_argnums=(2,))


def _march_all(tet_verts: jnp.ndarray, tet_values: jnp.ndarray, level: float) -> tuple[jnp.ndarray, jnp.ndarray]:
    march_vmapped = jax.vmap(lambda v, s: _march_single_jit(v, s, level))
    tris, mask = march_vmapped(tet_verts, tet_values)
    return tris, mask


def marching_tetrahedra(
    field: jnp.ndarray | np.ndarray,
    coords: jnp.ndarray | np.ndarray,
    *,
    level: float = 0.0,
) -> TriangleMesh:
    """Extract a triangle mesh approximating the `field == level` isosurface."""
    coords_jnp = jnp.asarray(coords)
    field_jnp = jnp.asarray(field, dtype=coords_jnp.dtype)
    tet_verts, tet_values = _prepare_tetrahedra(coords_jnp, field_jnp)
    if tet_verts.shape[0] == 0:
        return TriangleMesh(np.zeros((0, 3), dtype=float), np.zeros((0, 3), dtype=int))

    tris, mask = _march_all(tet_verts, tet_values, level)
    tris_np = np.asarray(tris.reshape(-1, 3, 3))
    mask_np = np.asarray(mask.reshape(-1))
    valid_tris = tris_np[mask_np]
    if valid_tris.size == 0:
        return TriangleMesh(np.zeros((0, 3), dtype=float), np.zeros((0, 3), dtype=int))

    verts = valid_tris.reshape(-1, 3)
    unique_verts, inverse = np.unique(verts, axis=0, return_inverse=True)
    faces = inverse.reshape(-1, 3)
    return TriangleMesh(unique_verts, faces)


def decimate_mesh(mesh: TriangleMesh, max_faces: int) -> TriangleMesh:
    """Return a mesh with at most `max_faces` by uniform face subsampling."""
    if max_faces <= 0:
        raise ValueError("max_faces must be positive")
    faces = mesh.faces
    if faces.shape[0] <= max_faces:
        return mesh
    if max_faces == 1:
        chosen = faces[[0]]
    else:
        idx = np.linspace(0, faces.shape[0] - 1, max_faces, dtype=int)
        chosen = faces[idx]
    unique, inverse = np.unique(chosen.reshape(-1), return_inverse=True)
    new_vertices = mesh.vertices[unique]
    new_faces = inverse.reshape(-1, 3)
    return TriangleMesh(new_vertices, new_faces)


__all__ = [
    "rectilinear_grid",
    "marching_tetrahedra",
    "decimate_mesh",
]
