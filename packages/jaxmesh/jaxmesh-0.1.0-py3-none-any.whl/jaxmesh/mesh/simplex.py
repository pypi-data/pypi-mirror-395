"""Simplex mesh primitives: triangles and tetrahedra."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import jax
import jax.numpy as jnp
import numpy as np
from numpy.typing import ArrayLike

from .types import FloatArray, IntArray
from .._internal.cpu_fallback import CPU_LA_AVAILABLE, cpu_solve_small, cpu_inv_small


def _as_float_array(array: ArrayLike) -> FloatArray:
    arr = jnp.asarray(array, dtype=jnp.float64)
    if arr.ndim == 0:
        raise ValueError("Expected array with ndim >= 1")
    return arr


def _as_index_array(array: ArrayLike) -> IntArray:
    arr = jnp.asarray(array, dtype=jnp.int32)
    if arr.ndim == 0:
        raise ValueError("Expected array with ndim >= 1")
    return arr


def _triangle_area(vertices: FloatArray) -> float:
    if vertices.shape != (3, vertices.shape[1]):
        raise ValueError("Triangle requires three vertices")
    e1 = vertices[1] - vertices[0]
    e2 = vertices[2] - vertices[0]
    if vertices.shape[1] == 2:
        det = e1[0] * e2[1] - e1[1] * e2[0]
        return float(0.5 * jnp.abs(det))
    if vertices.shape[1] == 3:
        return float(0.5 * jnp.linalg.norm(jnp.cross(e1, e2)))
    raise ValueError("Triangle vertices must live in R^2 or R^3")


def _tetra_volume(vertices: FloatArray) -> float:
    if vertices.shape != (4, 3):
        raise ValueError("Tetrahedron requires four vertices in R^3")
    v0 = vertices[0]
    matrix = jnp.stack([vertices[1] - v0, vertices[2] - v0, vertices[3] - v0], axis=0)
    return float(jnp.abs(jnp.linalg.det(matrix)) / 6.0)


def _triangle_solver(vertices: FloatArray) -> FloatArray:
    """Return matrix S mapping delta -> (lambda1, lambda2)."""
    v0 = vertices[0]
    edges = jnp.stack([vertices[1] - v0, vertices[2] - v0], axis=1)  # (dim, 2)
    gram = edges.T @ edges
    determinant = float(jnp.linalg.det(gram))
    if determinant <= 0.0:
        raise ValueError("Degenerate triangle (Gram determinant <= 0)")
    use_cpu = CPU_LA_AVAILABLE and (jax.default_backend() == "gpu") and (gram.shape[0] <= 4)
    if use_cpu:
        return cpu_solve_small(gram, edges.T)
    return jnp.linalg.solve(gram, edges.T)


def _triangle_gradient_from_solver(solver: FloatArray) -> FloatArray:
    """Return gradient matrix (dim, 3) from solver matrix."""
    grad_lambda1 = solver[0]
    grad_lambda2 = solver[1]
    grad_lambda0 = -grad_lambda1 - grad_lambda2
    return jnp.stack([grad_lambda0, grad_lambda1, grad_lambda2], axis=0).T


def _tetra_gradient(inverse_affine: FloatArray) -> FloatArray:
    gradients = inverse_affine[:, :3]
    return gradients.T


@dataclass(frozen=True)
class SimplexMesh:
    """Base mesh type used for simplex elements."""

    vertices: FloatArray
    simplices: IntArray

    def __post_init__(self) -> None:
        verts = _as_float_array(self.vertices)
        simplices = _as_index_array(self.simplices)
        if verts.ndim != 2:
            raise ValueError("vertices must have shape (N, dim)")
        if simplices.ndim != 2:
            raise ValueError("simplices must have shape (M, K)")
        if verts.shape[0] == 0:
            raise ValueError("Mesh requires at least one vertex")
        if simplices.shape[0] == 0:
            raise ValueError("Mesh requires at least one cell")
        if jnp.any(simplices < 0).item() or jnp.any(simplices >= verts.shape[0]).item():
            raise ValueError("Simplex indices out of bounds")
        object.__setattr__(self, "vertices", verts)
        object.__setattr__(self, "simplices", simplices)

    @property
    def embedding_dim(self) -> int:
        return int(self.vertices.shape[1])

    @property
    def simplex_size(self) -> int:
        return int(self.simplices.shape[1])

    @property
    def num_vertices(self) -> int:
        return int(self.vertices.shape[0])

    @property
    def num_simplices(self) -> int:
        return int(self.simplices.shape[0])

    def simplex_vertices(self, simplex_index: int) -> FloatArray:
        return self.vertices[self.simplices[simplex_index]]


@dataclass(frozen=True)
class TriMesh(SimplexMesh):
    """Triangle mesh supporting barycentric queries and gradients."""

    _solver: FloatArray = field(init=False, repr=False)
    _gradients: FloatArray = field(init=False, repr=False)
    _areas: FloatArray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.simplex_size != 3:
            raise ValueError("TriMesh requires simplices with three vertices")
        if self.embedding_dim not in (2, 3):
            raise ValueError("TriMesh vertices must live in R^2 or R^3")
        solver = []
        gradients = []
        areas = []
        for simplex in np.asarray(self.simplices, dtype=np.int32):
            verts = self.vertices[simplex]
            S = _triangle_solver(verts)
            solver.append(S)
            gradients.append(_triangle_gradient_from_solver(S))
            area = _triangle_area(verts)
            if not math.isfinite(area) or area <= 0.0:
                raise ValueError("Triangle area must be positive")
            areas.append(area)
        object.__setattr__(self, "_solver", jnp.stack(solver, axis=0))
        object.__setattr__(self, "_gradients", jnp.stack(gradients, axis=0))
        object.__setattr__(self, "_areas", jnp.asarray(areas, dtype=jnp.float64))

    @property
    def areas(self) -> FloatArray:
        return self._areas

    @property
    def gradient_matrices(self) -> FloatArray:
        return self._gradients

    def barycentric_coordinates(
        self,
        simplex_index: int,
        points: ArrayLike,
    ) -> FloatArray:
        pts = jnp.asarray(points, dtype=jnp.float64)
        if pts.ndim == 1:
            pts = pts[None, :]
        if pts.shape[1] != self.embedding_dim:
            raise ValueError("Point dimensionality mismatch")
        verts = self.simplex_vertices(simplex_index)
        delta = pts - verts[0]
        solver = self._solver[simplex_index]
        coeff = (solver @ delta.T).T
        l1 = coeff[:, 0]
        l2 = coeff[:, 1]
        l0 = 1.0 - l1 - l2
        return jnp.stack([l0, l1, l2], axis=-1)

    def locate_point(
        self,
        point: ArrayLike,
        *,
        atol: float = 1e-10,
    ) -> tuple[int, FloatArray] | None:
        bary_all = [self.barycentric_coordinates(i, point)[0] for i in range(self.num_simplices)]
        for idx, bary in enumerate(bary_all):
            bary_np = np.asarray(bary, dtype=np.float64)
            if np.all(bary_np >= -atol) and abs(float(bary_np.sum()) - 1.0) <= atol:
                return idx, bary
        return None


@dataclass(frozen=True)
class TetMesh(SimplexMesh):
    """Tetrahedral mesh with barycentric utilities."""

    _inverse_affine: FloatArray = field(init=False, repr=False)
    _gradients: FloatArray = field(init=False, repr=False)
    _volumes: FloatArray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.simplex_size != 4:
            raise ValueError("TetMesh requires simplices with four vertices")
        if self.embedding_dim != 3:
            raise ValueError("TetMesh vertices must live in R^3")
        inv_list = []
        gradients = []
        volumes = []
        for simplex in np.asarray(self.simplices, dtype=np.int32):
            verts = self.vertices[simplex]
            ones = jnp.ones((1, 4), dtype=jnp.float64)
            affine = jnp.concatenate((verts.T, ones), axis=0)
            use_cpu = CPU_LA_AVAILABLE and (jax.default_backend() == "gpu") and (affine.shape[0] <= 8)
            if use_cpu:
                inv_affine = cpu_inv_small(affine)
            else:
                inv_affine = jnp.linalg.inv(affine)
            inv_list.append(inv_affine)
            gradients.append(_tetra_gradient(inv_affine))
            vol = _tetra_volume(verts)
            if not math.isfinite(vol) or vol <= 0.0:
                raise ValueError("Tetrahedron volume must be positive")
            volumes.append(vol)
        object.__setattr__(self, "_inverse_affine", jnp.stack(inv_list, axis=0))
        object.__setattr__(self, "_gradients", jnp.stack(gradients, axis=0))
        object.__setattr__(self, "_volumes", jnp.asarray(volumes, dtype=jnp.float64))

    @property
    def volumes(self) -> FloatArray:
        return self._volumes

    @property
    def gradient_matrices(self) -> FloatArray:
        return self._gradients

    def barycentric_coordinates(self, simplex_index: int, points: ArrayLike) -> FloatArray:
        pts = jnp.asarray(points, dtype=jnp.float64)
        if pts.ndim == 1:
            pts = pts[None, :]
        if pts.shape[1] != 3:
            raise ValueError("Point dimensionality mismatch")
        ones = jnp.ones((pts.shape[0], 1), dtype=jnp.float64)
        aug = jnp.concatenate([pts, ones], axis=1)
        inv_affine = self._inverse_affine[simplex_index]
        bary = aug @ inv_affine.T
        return bary

    def locate_point(
        self,
        point: ArrayLike,
        *,
        atol: float = 1e-10,
    ) -> tuple[int, FloatArray] | None:
        bary_all = [self.barycentric_coordinates(i, point)[0] for i in range(self.num_simplices)]
        for idx, bary in enumerate(bary_all):
            bary_np = np.asarray(bary, dtype=np.float64)
            if np.all(bary_np >= -atol) and abs(float(bary_np.sum()) - 1.0) <= atol:
                return idx, bary
        return None


__all__ = [
    "SimplexMesh",
    "TriMesh",
    "TetMesh",
]
