"""Tests para cálculo de perímetros."""

import unittest
import numpy as np
from extremal_packings.configurations import Configuration
from extremal_packings.perimeter import (
    perimeter_centers,
    perimeter_disks,
    compute_hull
)


class TestComputeHull(unittest.TestCase):
    """Tests para compute_hull."""

    def test_triangle(self):
        """Test casco convexo de triángulo."""
        coords = np.array([[0, 0], [1, 0], [0.5, 0.5]])
        config = Configuration(coords=coords, edges=[])
        hull = compute_hull(config)
        self.assertEqual(len(hull), 3)

    def test_square(self):
        """Test casco convexo de cuadrado."""
        coords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        config = Configuration(coords=coords, edges=[])
        hull = compute_hull(config)
        self.assertEqual(len(hull), 4)

    def test_collinear_points(self):
        """Test puntos colineales."""
        coords = np.array([[0, 0], [1, 0], [2, 0]])
        config = Configuration(coords=coords, edges=[])
        hull = compute_hull(config)
        self.assertEqual(len(hull), 2)


class TestPerimeterCenters(unittest.TestCase):
    """Tests para perimeter_centers."""

    def test_triangle_perimeter(self):
        """Test perímetro de triángulo equilátero."""
        coords = np.array([
            [0, 0],
            [2, 0],
            [1, np.sqrt(3)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges)
        
        perim = perimeter_centers(config)
        
        # Perímetro = 3 * 2 = 6
        self.assertAlmostEqual(perim, 6.0, places=10)

    def test_collinear_disks(self):
        """Test perímetro de discos en línea."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        perim = perimeter_centers(config)
        
        # Perímetro de segmento = 2 * 4 = 8
        self.assertAlmostEqual(perim, 8.0, places=10)


class TestPerimeterDisks(unittest.TestCase):
    """Tests para perimeter_disks."""

    def test_single_disk(self):
        """Test perímetro de un solo disco."""
        coords = np.array([[0, 0]])
        edges = []
        config = Configuration(coords=coords, edges=edges)
        
        perimeter = perimeter_disks(config)
        expected = 2 * np.pi
        self.assertAlmostEqual(perimeter, expected, places=5)

    def test_two_tangent_disks(self):
        """Test dos discos tangentes."""
        coords = np.array([[0, 0], [2, 0]])
        edges = [(0, 1)]
        config = Configuration(coords=coords, edges=edges)
        
        perimeter = perimeter_disks(config)
        expected = 2 * np.pi + 4
        self.assertAlmostEqual(perimeter, expected, places=5)

    def test_triangle_configuration(self):
        """Test triángulo de discos."""
        coords = np.array([
            [0, 0],
            [2, 0],
            [1, np.sqrt(3)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges)
        
        perimeter = perimeter_disks(config)
        self.assertGreater(perimeter, 0)


if __name__ == '__main__':
    unittest.main()
