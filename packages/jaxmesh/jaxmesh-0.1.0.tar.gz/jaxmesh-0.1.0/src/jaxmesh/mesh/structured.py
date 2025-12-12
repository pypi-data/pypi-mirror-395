"""Structured mesh types: quads and hexahedra."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import jax.numpy as jnp
import numpy as np

from .types import FloatArray, IntArray
from .simplex import TriMesh, TetMesh


def _as_float_array(array) -> FloatArray:
    arr = jnp.asarray(array, dtype=jnp.float64)
    if arr.ndim == 0:
        raise ValueError("Expected array with ndim >= 1")
    return arr


def _as_index_array(array) -> IntArray:
    arr = jnp.asarray(array, dtype=jnp.int32)
    if arr.ndim == 0:
        raise ValueError("Expected array with ndim >= 1")
    return arr


_QUAD_SPLIT_MAIN = np.array([(0, 1, 2), (0, 2, 3)], dtype=np.int32)
_QUAD_SPLIT_ALTERNATE = np.array([(0, 1, 3), (1, 2, 3)], dtype=np.int32)


@dataclass(frozen=True)
class QuadMesh:
    """Axis-aligned quad mesh with helpers to convert to triangles."""

    vertices: FloatArray
    quads: IntArray

    def __post_init__(self) -> None:
        verts = _as_float_array(self.vertices)
        quads = _as_index_array(self.quads)
        if verts.ndim != 2 or verts.shape[1] < 2:
            raise ValueError("QuadMesh requires vertices in R^2 or higher")
        if quads.ndim != 2 or quads.shape[1] != 4:
            raise ValueError("Quads must have shape (M, 4)")
        if jnp.any(quads < 0).item() or jnp.any(quads >= verts.shape[0]).item():
            raise ValueError("Quad indices out of range")
        object.__setattr__(self, "vertices", verts)
        object.__setattr__(self, "quads", quads)

    def to_trimesh(self, diagonal: Literal["main", "alternate"] = "main") -> TriMesh:
        pattern = _QUAD_SPLIT_MAIN if diagonal == "main" else _QUAD_SPLIT_ALTERNATE
        flat = jnp.asarray(pattern.reshape(-1), dtype=jnp.int32)
        tris = self.quads[:, flat].reshape(-1, 3)
        return TriMesh(vertices=self.vertices, simplices=tris)


_HEX_SPLIT_LONG_DIAGONAL = np.array(
    [
        (0, 5, 1, 6),
        (0, 5, 6, 4),
        (0, 6, 2, 1),
        (0, 6, 3, 2),
        (0, 6, 7, 3),
        (0, 6, 4, 7),
    ],
    dtype=np.int32,
)


@dataclass(frozen=True)
class HexMesh:
    """Hexahedral mesh convertible to tetrahedra via long-diagonal split."""

    vertices: FloatArray
    hexes: IntArray

    def __post_init__(self) -> None:
        verts = _as_float_array(self.vertices)
        hexes = _as_index_array(self.hexes)
        if verts.ndim != 2 or verts.shape[1] != 3:
            raise ValueError("HexMesh requires vertices in R^3")
        if hexes.ndim != 2 or hexes.shape[1] != 8:
            raise ValueError("Hex cells must have shape (M, 8)")
        if jnp.any(hexes < 0).item() or jnp.any(hexes >= verts.shape[0]).item():
            raise ValueError("Hex indices out of range")
        object.__setattr__(self, "vertices", verts)
        object.__setattr__(self, "hexes", hexes)

    def to_tetmesh(self) -> TetMesh:
        flat = jnp.asarray(_HEX_SPLIT_LONG_DIAGONAL.reshape(-1), dtype=jnp.int32)
        tets = self.hexes[:, flat].reshape(-1, 4)
        return TetMesh(vertices=self.vertices, simplices=tets)


__all__ = [
    "QuadMesh",
    "HexMesh",
]
