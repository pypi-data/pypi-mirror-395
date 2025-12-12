"""CPU fallback kernels for small linear algebra operations.

Tiny SPD systems occasionally trigger cuSolver failures on GPU; these cached
CPU kernels allow fallback without leaving JAX tracing contexts.
"""

from __future__ import annotations

import jax
import jax.numpy as jnp

try:
    _CPU_SOLVE_SMALL = jax.jit(lambda matrix, rhs: jnp.linalg.solve(matrix, rhs), backend="cpu")
    _CPU_INV_SMALL = jax.jit(lambda matrix: jnp.linalg.inv(matrix), backend="cpu")
    # Warm up the kernels
    _CPU_SOLVE_SMALL(jnp.eye(2, dtype=jnp.float32), jnp.ones((2, 1), dtype=jnp.float32))
    _CPU_INV_SMALL(jnp.eye(2, dtype=jnp.float32))
    CPU_LA_AVAILABLE = True
except RuntimeError:
    _CPU_SOLVE_SMALL = None
    _CPU_INV_SMALL = None
    CPU_LA_AVAILABLE = False


def cpu_solve_small(matrix, rhs):
    """Solve a small linear system on CPU."""
    if _CPU_SOLVE_SMALL is None:
        raise RuntimeError("CPU backend unavailable for solve fallback")
    return _CPU_SOLVE_SMALL(matrix, rhs)


def cpu_inv_small(matrix):
    """Invert a small matrix on CPU."""
    if _CPU_INV_SMALL is None:
        raise RuntimeError("CPU backend unavailable for inverse fallback")
    return _CPU_INV_SMALL(matrix)


__all__ = ["CPU_LA_AVAILABLE", "cpu_solve_small", "cpu_inv_small"]
