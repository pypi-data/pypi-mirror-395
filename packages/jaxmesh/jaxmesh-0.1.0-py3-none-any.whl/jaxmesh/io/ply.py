"""PLY mesh export."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import numpy as np

from ..geometry.normals import TriangleMesh, compute_vertex_normals


def save_mesh_as_ply(
    mesh: TriangleMesh,
    path: str | Path,
    *,
    include_normals: bool = True,
    vertex_attributes: Mapping[str, np.ndarray] | None = None,
) -> Path:
    """Write the mesh to a binary-free ASCII PLY file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    verts = np.asarray(mesh.vertices, dtype=float)
    faces = np.asarray(mesh.faces, dtype=np.int64)
    normals = compute_vertex_normals(mesh) if include_normals else None
    attr_names: list[str] = []
    attr_arrays: dict[str, np.ndarray] = {}
    if vertex_attributes:
        for name, values in vertex_attributes.items():
            arr = np.asarray(values, dtype=float)
            if arr.shape != (len(verts),):
                raise ValueError("vertex attribute lengths must match number of vertices")
            attr_names.append(name)
            attr_arrays[name] = arr

    with path.open("w", encoding="utf-8") as fh:
        fh.write("ply\n")
        fh.write("format ascii 1.0\n")
        fh.write(f"element vertex {len(verts)}\n")
        fh.write("property float x\nproperty float y\nproperty float z\n")
        if normals is not None:
            fh.write("property float nx\nproperty float ny\nproperty float nz\n")
        for name in attr_names:
            fh.write(f"property float {name}\n")
        fh.write(f"element face {len(faces)}\n")
        fh.write("property list uchar int vertex_indices\n")
        fh.write("end_header\n")
        for idx, v in enumerate(verts):
            parts = [f"{v[0]:.9f}", f"{v[1]:.9f}", f"{v[2]:.9f}"]
            if normals is not None:
                n = normals[idx]
                parts.extend((f"{n[0]:.9f}", f"{n[1]:.9f}", f"{n[2]:.9f}"))
            for name in attr_names:
                parts.append(f"{attr_arrays[name][idx]:.9f}")
            fh.write(" ".join(parts) + "\n")
        for tri in faces:
            fh.write(f"3 {int(tri[0])} {int(tri[1])} {int(tri[2])}\n")
    return path


__all__ = ["save_mesh_as_ply"]
