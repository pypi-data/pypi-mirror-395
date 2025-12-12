"""Barycentric coordinate utilities."""

from __future__ import annotations

from typing import Sequence

import jax
import jax.numpy as jnp

from .._internal.cpu_fallback import CPU_LA_AVAILABLE, cpu_solve_small


def triangle_barycentric_weights(
    vertices: Sequence[Sequence[float]],
    point: Sequence[float],
) -> jnp.ndarray:
    """Return barycentric weights for ``point`` inside a triangle."""
    verts = jnp.asarray(vertices, dtype=jnp.float64)
    if verts.shape[0] != 3:
        raise ValueError("triangle must have exactly three vertices")
    point_arr = jnp.asarray(point, dtype=jnp.float64)
    v0 = verts[0]
    A = jnp.stack((verts[1] - v0, verts[2] - v0), axis=1)
    rhs = point_arr - v0
    if A.shape[0] == 2:
        use_cpu = CPU_LA_AVAILABLE and (jax.default_backend() == "gpu") and (A.shape[0] <= 4)
        if use_cpu:
            lambdas = cpu_solve_small(A, rhs)
        else:
            lambdas = jnp.linalg.solve(A, rhs)
    else:
        lambdas = jnp.linalg.lstsq(A, rhs, rcond=None)[0]
    lambda1, lambda2 = lambdas
    lambda0 = 1.0 - lambda1 - lambda2
    return jnp.asarray([lambda0, lambda1, lambda2], dtype=jnp.float64)


def tetra_barycentric_weights(
    vertices: Sequence[Sequence[float]],
    point: Sequence[float],
) -> jnp.ndarray:
    """Return barycentric weights for ``point`` inside a tetrahedron."""
    verts = jnp.asarray(vertices, dtype=jnp.float64)
    if verts.shape[0] != 4:
        raise ValueError("tetrahedron must have exactly four vertices")
    point_arr = jnp.asarray(point, dtype=jnp.float64)
    v0 = verts[0]
    matrix = jnp.stack((verts[1] - v0, verts[2] - v0, verts[3] - v0), axis=1)
    rhs = point_arr - v0
    use_cpu = CPU_LA_AVAILABLE and (jax.default_backend() == "gpu") and (matrix.shape[0] <= 4)
    if use_cpu:
        coeffs = cpu_solve_small(matrix, rhs)
    else:
        coeffs = jnp.linalg.solve(matrix, rhs)
    lambda1, lambda2, lambda3 = coeffs
    lambda0 = 1.0 - lambda1 - lambda2 - lambda3
    return jnp.asarray([lambda0, lambda1, lambda2, lambda3], dtype=jnp.float64)


__all__ = [
    "triangle_barycentric_weights",
    "tetra_barycentric_weights",
]
