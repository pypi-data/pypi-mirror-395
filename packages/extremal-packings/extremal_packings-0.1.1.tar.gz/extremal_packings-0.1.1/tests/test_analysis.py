"""Tests de integración para pipeline de análisis."""

import unittest
import numpy as np
from extremal_packings import (
    Configuration,
    analyze_configuration,
    load_configuration
)


class TestAnalyzeConfiguration(unittest.TestCase):
    """Tests para analyze_configuration."""

    def test_simple_chain(self):
        """Test análisis de cadena simple."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        result = analyze_configuration(config)
        
        # Verificar que todos los campos existan
        self.assertIsNotNone(result.A)
        self.assertIsNotNone(result.R)
        self.assertIsNotNone(result.K)
        self.assertIsNotNone(result.H)
        self.assertIsNotNone(result.eigenvalues)
        self.assertIsNotNone(result.perimeter_centers)
        self.assertIsNotNone(result.perimeter_disks)

    def test_triangle(self):
        """Test análisis de triángulo."""
        coords = np.array([
            [0, 0],
            [2, 0],
            [1, np.sqrt(3)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges)
        
        result = analyze_configuration(config)
        
        # Triángulo es rígido -> rolling space pequeño
        self.assertLessEqual(result.R.shape[1], 3)

    def test_no_contacts(self):
        """Test configuración sin contactos."""
        coords = np.array([[0, 0], [10, 0]])
        edges = [(0, 1)]
        config = Configuration(coords=coords, edges=edges)
        
        result = analyze_configuration(config)
        
        # Con un solo contacto -> rolling space grande
        self.assertGreater(result.R.shape[1], 0)

    def test_eigenvalues_ordered(self):
        """Test que autovalores estén ordenados."""
        config = load_configuration("D5-7")
        result = analyze_configuration(config)
        
        eigenvalues = result.eigenvalues
        # Verificar orden no-decreciente
        self.assertTrue(np.all(eigenvalues[:-1] <= eigenvalues[1:]))

    def test_perimeters_positive(self):
        """Test que perímetros sean positivos."""
        config = load_configuration("D4-3")
        result = analyze_configuration(config)
        
        self.assertGreater(result.perimeter_centers, 0)
        self.assertGreater(result.perimeter_disks, 0)

    def test_matrix_dimensions(self):
        """Test dimensiones de matrices."""
        coords = np.array([[0, 0], [2, 0], [4, 0], [6, 0]])
        edges = [(0, 1), (1, 2), (2, 3)]
        config = Configuration(coords=coords, edges=edges)
        
        result = analyze_configuration(config)
        
        n = config.n
        m = len(config.edges)
        d = result.R.shape[1]
        
        # A: (m, 2n)
        self.assertEqual(result.A.shape, (m, 2*n))
        # R: (2n, d)
        self.assertEqual(result.R.shape[0], 2*n)
        # K: (2n, 2n)
        self.assertEqual(result.K.shape, (2*n, 2*n))
        # H: (d, d)
        self.assertEqual(result.H.shape, (d, d))


class TestAnalysisWithCatalog(unittest.TestCase):
    """Tests de análisis con configuraciones del catálogo."""

    def test_all_3disk_configs(self):
        """Test todas las configuraciones de 3 discos."""
        from extremal_packings import get_configurations_by_size
        
        configs_3 = get_configurations_by_size(3)
        
        for name in configs_3:
            config = load_configuration(name)
            result = analyze_configuration(config)
            
            # Verificaciones básicas
            self.assertEqual(result.config.n, 3)
            self.assertGreaterEqual(len(result.eigenvalues), 0)

    def test_pentagon_configuration(self):
        """Test pentágono regular (D5-7)."""
        config = load_configuration("D5-7")
        result = analyze_configuration(config)
        
        # Pentágono tiene 5 discos
        self.assertEqual(config.n, 5)
        # Debe tener algún rolling space
        self.assertGreater(result.R.shape[1], 0)


if __name__ == '__main__':
    unittest.main()
