"""Tests para validación de grafos de contacto."""

import unittest
from extremal_packings.contact_graphs import check_graph_validity


class TestCheckGraphValidity(unittest.TestCase):
    """Tests para check_graph_validity."""

    def test_valid_chain(self):
        """Test cadena válida."""
        edges = [(0, 1), (1, 2), (2, 3)]
        # No debe lanzar excepción
        check_graph_validity(4, edges)

    def test_valid_cycle(self):
        """Test ciclo válido."""
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        check_graph_validity(4, edges)

    def test_disconnected_graph(self):
        """Test grafo desconectado."""
        edges = [(0, 1), (2, 3)]  # Dos componentes
        
        with self.assertRaises(ValueError):
            check_graph_validity(4, edges)

    def test_degree_exceeds_six(self):
        """Test vértice con grado > 6."""
        # Vértice 0 conectado a 7 otros
        edges = [(0, i) for i in range(1, 8)]
        
        with self.assertRaises(ValueError):
            check_graph_validity(8, edges)

    def test_empty_graph(self):
        """Test grafo sin aristas."""
        edges = []
        
        # Grafo vacío es desconectado si n > 1
        with self.assertRaises(ValueError):
            check_graph_validity(3, edges)

    def test_single_vertex(self):
        """Test un solo vértice."""
        edges = []
        # Un vértice solo está conectado
        check_graph_validity(1, edges)

    def test_complete_graph_k4(self):
        """Test grafo completo K4."""
        edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3),
            (2, 3)
        ]
        check_graph_validity(4, edges)

    def test_invalid_vertex_index(self):
        """Test índice de vértice inválido."""
        edges = [(0, 1), (1, 5)]  # 5 > n-1
        
        with self.assertRaises(ValueError):
            check_graph_validity(4, edges)


if __name__ == '__main__':
    unittest.main()
