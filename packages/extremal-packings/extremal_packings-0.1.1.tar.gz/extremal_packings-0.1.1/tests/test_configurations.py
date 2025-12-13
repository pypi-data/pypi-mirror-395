"""Tests para la clase Configuration."""

import unittest
import numpy as np
from extremal_packings.configurations import Configuration


class TestConfiguration(unittest.TestCase):
    """Tests para Configuration."""

    def test_basic_creation(self):
        """Test creación básica de configuración."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        self.assertEqual(config.n, 3)
        self.assertEqual(len(config.edges), 2)

    def test_empty_configuration(self):
        """Test configuración sin contactos."""
        coords = np.array([[0, 0], [5, 0], [10, 0]])
        edges = []
        config = Configuration(coords=coords, edges=edges)
        
        self.assertEqual(config.n, 3)
        self.assertEqual(len(config.edges), 0)

    def test_triangle_configuration(self):
        """Test triángulo equilátero."""
        coords = np.array([
            [0.0, 0.0],
            [2.0, 0.0],
            [1.0, np.sqrt(3.0)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges, name="Triangle")
        
        self.assertEqual(config.n, 3)
        self.assertEqual(len(config.edges), 3)

    def test_coords_validation(self):
        """Test que coords tenga forma correcta."""
        coords = np.array([[0, 0], [2, 0]])
        edges = [(0, 1)]
        config = Configuration(coords=coords, edges=edges)
        
        self.assertEqual(config.coords.shape, (2, 2))


class TestConfigurationProperties(unittest.TestCase):
    """Tests para propiedades de Configuration."""

    def test_n_property(self):
        """Test propiedad n."""
        coords = np.array([[0, 0], [2, 0], [4, 0], [6, 0]])
        edges = []
        config = Configuration(coords=coords, edges=edges)
        
        self.assertEqual(config.n, 4)

    def test_edge_sorting(self):
        """Test que edges se almacenen correctamente."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(1, 2), (0, 1)]  # Orden arbitrario
        config = Configuration(coords=coords, edges=edges)
        
        self.assertEqual(len(config.edges), 2)
        self.assertIn((1, 2), config.edges)
        self.assertIn((0, 1), config.edges)


if __name__ == '__main__':
    unittest.main()
