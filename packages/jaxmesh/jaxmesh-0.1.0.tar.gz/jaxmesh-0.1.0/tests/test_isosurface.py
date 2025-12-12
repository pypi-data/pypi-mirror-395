"""Tests for isosurface extraction."""

import numpy as np
import jax.numpy as jnp
import pytest

from jaxmesh import (
    marching_tetrahedra,
    rectilinear_grid,
    decimate_mesh,
    compute_vertex_normals,
    save_mesh_as_ply,
    save_mesh_as_glb,
)


def _sphere_field(xs, ys, zs, radius):
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    return np.sqrt(X**2 + Y**2 + Z**2) - radius


def test_marching_tetrahedra_sphere_radius():
    xs = np.linspace(-1.5, 1.5, 26)
    ys = np.linspace(-1.5, 1.5, 26)
    zs = np.linspace(-1.5, 1.5, 26)
    coords = rectilinear_grid(xs, ys, zs)
    field = _sphere_field(xs, ys, zs, radius=1.0)

    mesh = marching_tetrahedra(jnp.asarray(field), coords, level=0.0)

    assert mesh.vertices.shape[0] > 0
    radii = np.linalg.norm(mesh.vertices, axis=1)
    assert np.allclose(np.median(radii), 1.0, atol=0.05)


def test_rectilinear_grid_shape():
    x = np.linspace(0, 1, 10)
    y = np.linspace(0, 2, 20)
    z = np.linspace(0, 3, 30)
    coords = rectilinear_grid(x, y, z)
    assert coords.shape == (10, 20, 30, 3)


def test_compute_normals_and_decimate():
    xs = np.linspace(-1.4, 1.4, 24)
    coords = rectilinear_grid(xs, xs, xs)
    field = _sphere_field(xs, xs, xs, radius=1.0)
    mesh = marching_tetrahedra(field, coords, level=0.0)

    normals = compute_vertex_normals(mesh)
    assert normals.shape == mesh.vertices.shape
    norms = np.linalg.norm(normals, axis=1)
    assert np.allclose(norms[norms > 0], 1.0, atol=1e-5)

    decimated = decimate_mesh(mesh, max_faces=max(1, mesh.faces.shape[0] // 10))
    assert decimated.faces.shape[0] <= mesh.faces.shape[0] // 10 + 1
    assert decimated.vertices.shape[0] <= mesh.vertices.shape[0]


def test_save_mesh_as_ply(tmp_path):
    xs = np.linspace(-1.3, 1.3, 18)
    coords = rectilinear_grid(xs, xs, xs)
    field = _sphere_field(xs, xs, xs, radius=0.9)
    mesh = marching_tetrahedra(field, coords, level=0.0)

    ply_path = save_mesh_as_ply(mesh, tmp_path / "mesh.ply")
    text = ply_path.read_text().splitlines()
    assert text[0] == "ply"
    assert any(line.startswith("element vertex") for line in text)
    assert any(line.startswith("element face") for line in text)
    assert any(line.startswith("property float nx") for line in text)


def test_save_mesh_as_glb(tmp_path):
    xs = np.linspace(-1.2, 1.2, 20)
    coords = rectilinear_grid(xs, xs, xs)
    field = _sphere_field(xs, xs, xs, radius=1.0)
    mesh = marching_tetrahedra(field, coords, level=0.0)

    glb_path = save_mesh_as_glb(mesh, tmp_path / "mesh.glb", max_faces=500)
    data = glb_path.read_bytes()
    assert data[:4] == b"glTF"
    assert len(data) > 0


def test_empty_mesh_handling():
    # Field entirely positive - no isosurface
    xs = np.linspace(0, 1, 10)
    coords = rectilinear_grid(xs, xs, xs)
    field = np.ones((10, 10, 10))

    mesh = marching_tetrahedra(field, coords, level=0.0)
    assert mesh.vertices.shape[0] == 0
    assert mesh.faces.shape[0] == 0
