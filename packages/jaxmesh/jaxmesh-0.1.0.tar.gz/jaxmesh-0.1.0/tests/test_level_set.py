"""Tests for level-set utilities."""

import numpy as np
import jax.numpy as jnp
import pytest

from jaxmesh import (
    EdgeIntersection,
    triangle_edge_intersections,
    tetra_edge_intersections,
    triangle_zero_segment,
    tetra_zero_triangles,
    TRI_EDGES,
    TET_EDGES,
)


class TestEdgeIntersections:
    def test_triangle_crossing(self):
        # Triangle with one vertex below level, two above
        values = [-1.0, 1.0, 1.0]
        intersections = triangle_edge_intersections(values, level=0.0)

        # Should have 2 intersections (edges 0-1 and 2-0)
        assert len(intersections) == 2

    def test_triangle_no_crossing(self):
        # All positive - no crossing
        values = [1.0, 2.0, 3.0]
        intersections = triangle_edge_intersections(values, level=0.0)
        assert len(intersections) == 0

    def test_tetra_crossing(self):
        # One vertex below, three above
        values = [-1.0, 1.0, 1.0, 1.0]
        intersections = tetra_edge_intersections(values, level=0.0)

        # Should have 3 intersections (edges from vertex 0)
        assert len(intersections) == 3

    def test_intersection_parameter(self):
        # Midpoint crossing
        values = [-1.0, 1.0, 1.0]
        intersections = triangle_edge_intersections(values, level=0.0)

        # Find intersection on edge (0, 1)
        for inter in intersections:
            if inter.edge == (0, 1):
                assert np.isclose(inter.t, 0.5)


class TestZeroSegment:
    def test_triangle_zero_segment(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        values = [-1.0, 1.0, 1.0]

        result = triangle_zero_segment(vertices, values, level=0.0)
        assert result is not None
        p1, p2 = result

        # Both points should be on the level set
        # And should lie on the triangle edges

    def test_triangle_no_segment(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        values = [1.0, 2.0, 3.0]  # All positive

        result = triangle_zero_segment(vertices, values, level=0.0)
        assert result is None


class TestZeroTriangles:
    def test_tetra_zero_triangles(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        values = [-1.0, 1.0, 1.0, 1.0]  # One below, three above

        triangles = tetra_zero_triangles(vertices, values, level=0.0)

        # Should produce one triangle
        assert len(triangles) == 1
        assert triangles[0].shape == (3, 3)  # 3 vertices, 3D coords

    def test_tetra_no_triangles(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        values = [1.0, 2.0, 3.0, 4.0]  # All positive

        triangles = tetra_zero_triangles(vertices, values, level=0.0)
        assert len(triangles) == 0

    def test_tetra_quad_case(self):
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        values = [-1.0, -1.0, 1.0, 1.0]  # Two below, two above

        triangles = tetra_zero_triangles(vertices, values, level=0.0)

        # Should produce two triangles (quad split into two)
        assert len(triangles) == 2


class TestConstants:
    def test_tri_edges(self):
        assert len(TRI_EDGES) == 3
        assert all(len(e) == 2 for e in TRI_EDGES)

    def test_tet_edges(self):
        assert len(TET_EDGES) == 6
        assert all(len(e) == 2 for e in TET_EDGES)
