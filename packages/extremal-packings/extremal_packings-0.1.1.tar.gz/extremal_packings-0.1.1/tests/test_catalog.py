"""Tests para catálogo de configuraciones."""

import unittest
from extremal_packings.catalog import (
    list_configurations,
    load_configuration,
    get_configurations_by_size,
    get_catalog_stats
)


class TestListConfigurations(unittest.TestCase):
    """Tests para list_configurations."""

    def test_returns_list(self):
        """Test que retorne una lista."""
        configs = list_configurations()
        self.assertIsInstance(configs, list)

    def test_non_empty(self):
        """Test que no esté vacío."""
        configs = list_configurations()
        self.assertGreater(len(configs), 0)

    def test_contains_expected_configs(self):
        """Test que contenga configuraciones conocidas."""
        configs = list_configurations()
        # Debe tener configuraciones de 3 a 6 discos
        self.assertTrue(any('D3-' in c for c in configs))
        self.assertTrue(any('D5-' in c for c in configs))


class TestLoadConfiguration(unittest.TestCase):
    """Tests para load_configuration."""

    def test_load_valid_config(self):
        """Test cargar configuración válida."""
        config = load_configuration("D3-2")
        
        self.assertEqual(config.n, 3)
        self.assertIsNotNone(config.coords)
        self.assertIsNotNone(config.edges)

    def test_config_properties(self):
        """Test propiedades de configuración cargada."""
        config = load_configuration("D3-1")  # Triángulo
        
        self.assertEqual(config.n, 3)
        self.assertEqual(len(config.edges), 3)

    def test_invalid_config_name(self):
        """Test carga con nombre inválido."""
        with self.assertRaises(KeyError) as context:
            load_configuration("D99-999")
        
        # Verificar que el mensaje contenga la info del error
        self.assertIn("D99-999", str(context.exception))


class TestGetConfigurationsBySize(unittest.TestCase):
    """Tests para get_configurations_by_size."""

    def test_filter_by_size(self):
        """Test filtrado por tamaño."""
        configs_3 = get_configurations_by_size(3)
        configs_4 = get_configurations_by_size(4)
        configs_5 = get_configurations_by_size(5)
        
        # Deben tener diferentes cantidades
        self.assertGreater(len(configs_3), 0)
        self.assertGreater(len(configs_4), 0)
        self.assertGreater(len(configs_5), 0)

    def test_all_have_correct_size(self):
        """Test que todas tengan el tamaño correcto."""
        configs_5 = get_configurations_by_size(5)
        
        for name in configs_5:
            config = load_configuration(name)
            self.assertEqual(config.n, 5)

    def test_invalid_size(self):
        """Test con tamaño inválido."""
        configs = get_configurations_by_size(99)
        self.assertEqual(len(configs), 0)


class TestGetCatalogStats(unittest.TestCase):
    """Tests para get_catalog_stats."""

    def test_returns_dict(self):
        """Test que retorne diccionario."""
        stats = get_catalog_stats()
        self.assertIsInstance(stats, dict)

    def test_has_expected_keys(self):
        """Test que tenga claves esperadas."""
        stats = get_catalog_stats()
        self.assertIn('total', stats)
        self.assertIn('by_size', stats)

    def test_totals_match(self):
        """Test que totales coincidan."""
        stats = get_catalog_stats()
        
        total = stats['total']
        sum_by_size = sum(stats['by_size'].values())
        
        self.assertEqual(total, sum_by_size)


if __name__ == '__main__':
    unittest.main()
