"""GLB (binary glTF) mesh export."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import numpy as np

from ..geometry.normals import TriangleMesh, compute_vertex_normals
from ..isosurface.marching_tetrahedra import decimate_mesh


def save_mesh_as_glb(
    mesh: TriangleMesh,
    path: str | Path,
    *,
    max_faces: int | None = None,
) -> Path:
    """Write a binary glTF (GLB) file containing the mesh with vertex normals."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    working_mesh = mesh
    if max_faces is not None and max_faces > 0:
        working_mesh = decimate_mesh(mesh, max_faces)

    verts = np.asarray(working_mesh.vertices, dtype=np.float32)
    faces = np.asarray(working_mesh.faces, dtype=np.uint32)

    if verts.size == 0 or faces.size == 0:
        empty = {"asset": {"version": "2.0"}, "scenes": [], "buffers": [{"byteLength": 0}]}
        json_bytes = json.dumps(empty, separators=(",", ":")).encode("utf-8")
        json_pad = (4 - (len(json_bytes) % 4)) % 4
        json_bytes += b" " * json_pad
        total_length = 12 + 8 + len(json_bytes)
        with path.open("wb") as fh:
            fh.write(struct.pack("<4sII", b"glTF", 2, total_length))
            fh.write(struct.pack("<I4s", len(json_bytes), b"JSON"))
            fh.write(json_bytes)
        return path

    normals = compute_vertex_normals(working_mesh).astype(np.float32)
    indices = faces.reshape(-1)

    pos_bytes = verts.tobytes()
    norm_bytes = normals.tobytes()
    idx_bytes = indices.tobytes()

    offset_pos = 0
    offset_norm = offset_pos + len(pos_bytes)
    offset_idx = offset_norm + len(norm_bytes)
    bin_data = pos_bytes + norm_bytes + idx_bytes
    bin_pad = (4 - (len(bin_data) % 4)) % 4
    if bin_pad:
        bin_data += b"\x00" * bin_pad

    accessor_min = verts.min(axis=0).tolist()
    accessor_max = verts.max(axis=0).tolist()

    json_dict = {
        "asset": {"version": "2.0"},
        "buffers": [{"byteLength": len(bin_data)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": offset_pos, "byteLength": len(pos_bytes), "target": 34962},
            {"buffer": 0, "byteOffset": offset_norm, "byteLength": len(norm_bytes), "target": 34962},
            {"buffer": 0, "byteOffset": offset_idx, "byteLength": len(idx_bytes), "target": 34963},
        ],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": int(verts.shape[0]),
                "type": "VEC3",
                "min": accessor_min,
                "max": accessor_max,
            },
            {
                "bufferView": 1,
                "componentType": 5126,
                "count": int(normals.shape[0]),
                "type": "VEC3",
            },
            {
                "bufferView": 2,
                "componentType": 5125,
                "count": int(indices.size),
                "type": "SCALAR",
            },
        ],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "NORMAL": 1},
                        "indices": 2,
                        "mode": 4,
                    }
                ]
            }
        ],
        "nodes": [{"mesh": 0, "name": "mesh"}],
        "scenes": [{"nodes": [0]}],
        "scene": 0,
    }

    json_bytes = json.dumps(json_dict, separators=(",", ":")).encode("utf-8")
    json_pad = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b" " * json_pad

    total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_data)

    with path.open("wb") as fh:
        fh.write(struct.pack("<4sII", b"glTF", 2, total_length))
        fh.write(struct.pack("<I4s", len(json_bytes), b"JSON"))
        fh.write(json_bytes)
        fh.write(struct.pack("<I4s", len(bin_data), b"BIN\x00"))
        fh.write(bin_data)

    return path


__all__ = ["save_mesh_as_glb"]
