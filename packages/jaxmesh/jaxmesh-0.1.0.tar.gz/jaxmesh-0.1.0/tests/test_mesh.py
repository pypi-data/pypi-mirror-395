"""Tests for mesh primitives."""

import numpy as np
import jax.numpy as jnp
import pytest

from jaxmesh import (
    SimplexMesh,
    TriMesh,
    TetMesh,
    QuadMesh,
    HexMesh,
    triangle_barycentric_weights,
    tetra_barycentric_weights,
)


class TestTriMesh:
    def test_basic_triangle(self):
        vertices = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
        simplices = np.array([[0, 1, 2]], dtype=int)
        mesh = TriMesh(vertices=vertices, simplices=simplices)

        assert mesh.num_vertices == 3
        assert mesh.num_simplices == 1
        assert mesh.embedding_dim == 2
        assert mesh.simplex_size == 3

    def test_areas(self):
        vertices = np.array([[0, 0], [2, 0], [0, 2]], dtype=float)
        simplices = np.array([[0, 1, 2]], dtype=int)
        mesh = TriMesh(vertices=vertices, simplices=simplices)

        assert np.isclose(float(mesh.areas[0]), 2.0)

    def test_barycentric_coordinates(self):
        vertices = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
        simplices = np.array([[0, 1, 2]], dtype=int)
        mesh = TriMesh(vertices=vertices, simplices=simplices)

        # Centroid should have equal barycentric coordinates
        centroid = np.array([1/3, 1/3])
        bary = mesh.barycentric_coordinates(0, centroid)
        assert np.allclose(np.asarray(bary), [1/3, 1/3, 1/3], atol=1e-10)

    def test_locate_point(self):
        vertices = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)
        simplices = np.array([[0, 1, 2]], dtype=int)
        mesh = TriMesh(vertices=vertices, simplices=simplices)

        result = mesh.locate_point([0.2, 0.2])
        assert result is not None
        idx, bary = result
        assert idx == 0
        assert np.all(np.asarray(bary) >= -1e-10)


class TestTetMesh:
    def test_basic_tetrahedron(self):
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ], dtype=float)
        simplices = np.array([[0, 1, 2, 3]], dtype=int)
        mesh = TetMesh(vertices=vertices, simplices=simplices)

        assert mesh.num_vertices == 4
        assert mesh.num_simplices == 1
        assert mesh.embedding_dim == 3
        assert mesh.simplex_size == 4

    def test_volumes(self):
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ], dtype=float)
        simplices = np.array([[0, 1, 2, 3]], dtype=int)
        mesh = TetMesh(vertices=vertices, simplices=simplices)

        assert np.isclose(float(mesh.volumes[0]), 1/6, atol=1e-10)

    def test_barycentric_coordinates(self):
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ], dtype=float)
        simplices = np.array([[0, 1, 2, 3]], dtype=int)
        mesh = TetMesh(vertices=vertices, simplices=simplices)

        # Centroid
        centroid = np.array([0.25, 0.25, 0.25])
        bary = mesh.barycentric_coordinates(0, centroid)
        assert np.allclose(np.asarray(bary), [0.25, 0.25, 0.25, 0.25], atol=1e-10)


class TestQuadMesh:
    def test_to_trimesh(self):
        vertices = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1],
        ], dtype=float)
        quads = np.array([[0, 1, 2, 3]], dtype=int)
        mesh = QuadMesh(vertices=vertices, quads=quads)

        tri = mesh.to_trimesh()
        assert tri.num_simplices == 2
        assert tri.num_vertices == 4


class TestHexMesh:
    def test_to_tetmesh(self):
        # Unit cube vertices
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ], dtype=float)
        hexes = np.array([[0, 1, 2, 3, 4, 5, 6, 7]], dtype=int)
        mesh = HexMesh(vertices=vertices, hexes=hexes)

        tet = mesh.to_tetmesh()
        assert tet.num_simplices == 6  # 6 tets per hex


class TestBarycentricHelpers:
    def test_triangle_barycentric_weights(self):
        vertices = [[0, 0], [1, 0], [0, 1]]
        point = [1/3, 1/3]

        weights = triangle_barycentric_weights(vertices, point)
        assert np.allclose(np.asarray(weights), [1/3, 1/3, 1/3], atol=1e-10)

    def test_tetra_barycentric_weights(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        point = [0.25, 0.25, 0.25]

        weights = tetra_barycentric_weights(vertices, point)
        assert np.allclose(np.asarray(weights), [0.25, 0.25, 0.25, 0.25], atol=1e-10)
