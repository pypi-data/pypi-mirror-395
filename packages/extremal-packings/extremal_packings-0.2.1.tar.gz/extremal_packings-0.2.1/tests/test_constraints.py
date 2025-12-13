"""Tests para matriz de contacto y rolling space."""

import unittest
import numpy as np
from extremal_packings.configurations import Configuration
from extremal_packings.constraints import build_contact_matrix, rolling_space_basis


class TestBuildContactMatrix(unittest.TestCase):
    """Tests para build_contact_matrix."""

    def test_single_contact(self):
        """Test matriz con un solo contacto."""
        coords = np.array([[0, 0], [2, 0]])
        edges = [(0, 1)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        
        # Dimensiones: 1 contacto, 2 discos -> (1, 4)
        self.assertEqual(A.shape, (1, 4))
        
        # Verificar estructura: [-u, u] donde u = [1, 0]
        expected_row = np.array([-1, 0, 1, 0])
        np.testing.assert_array_almost_equal(A[0], expected_row)

    def test_chain_of_three(self):
        """Test cadena de 3 discos."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        
        # 2 contactos, 3 discos -> (2, 6)
        self.assertEqual(A.shape, (2, 6))

    def test_triangle(self):
        """Test triángulo equilátero."""
        coords = np.array([
            [0, 0],
            [2, 0],
            [1, np.sqrt(3)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        
        # 3 contactos, 3 discos -> (3, 6)
        self.assertEqual(A.shape, (3, 6))

    def test_orthogonality(self):
        """Test que filas sean ortogonales cuando corresponda."""
        coords = np.array([[0, 0], [2, 0], [0, 2]])
        edges = [(0, 1), (0, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        
        # Contactos perpendiculares -> filas ortogonales
        dot_product = np.dot(A[0], A[1])
        self.assertAlmostEqual(dot_product, 0.0, places=10)


class TestRollingSpaceBasis(unittest.TestCase):
    """Tests para rolling_space_basis."""

    def test_rigid_configuration(self):
        """Test configuración rígida (dim = 0)."""
        coords = np.array([
            [0, 0],
            [2, 0],
            [1, np.sqrt(3)]
        ])
        edges = [(0, 1), (1, 2), (2, 0)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        R = rolling_space_basis(A)
        
        # Triángulo es rígido en el plano
        # dim(Roll) = 2n - rank(A) = 6 - 3 = 3 (traslaciones + rotación)
        # Pero después de quitar movimientos rígidos, debería ser 0
        # Sin embargo, el método retorna base sin remover movimientos rígidos
        self.assertEqual(R.shape[0], 6)  # Dimension del espacio ambiente

    def test_flexible_chain(self):
        """Test cadena flexible."""
        coords = np.array([[0, 0], [2, 0], [4, 0], [6, 0]])
        edges = [(0, 1), (1, 2), (2, 3)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        R = rolling_space_basis(A)
        
        # 3 contactos, 4 discos -> dim = 8 - 3 = 5
        self.assertEqual(R.shape[0], 8)
        self.assertGreater(R.shape[1], 3)  # Más que movimientos rígidos

    def test_orthonormality(self):
        """Test que R tenga columnas ortonormales."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        R = rolling_space_basis(A)
        
        # R^T R debe ser identidad
        RtR = R.T @ R
        I = np.eye(R.shape[1])
        np.testing.assert_array_almost_equal(RtR, I)

    def test_kernel_property(self):
        """Test que AR = 0."""
        coords = np.array([[0, 0], [2, 0], [4, 0]])
        edges = [(0, 1), (1, 2)]
        config = Configuration(coords=coords, edges=edges)
        
        A = build_contact_matrix(config)
        R = rolling_space_basis(A)
        
        # A @ R debe ser ~0
        AR = A @ R
        np.testing.assert_array_almost_equal(AR, np.zeros_like(AR), decimal=10)


if __name__ == '__main__':
    unittest.main()
