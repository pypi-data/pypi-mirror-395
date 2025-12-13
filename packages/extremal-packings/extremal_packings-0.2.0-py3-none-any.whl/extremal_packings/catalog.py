"""
Catálogo de configuraciones de discos.

Carga configuraciones desde:
1. Archivos JSON en la carpeta data/
2. Configuraciones hardcodeadas de ejemplo
"""

from __future__ import annotations
from typing import List, Dict
import numpy as np
from .configurations import Configuration
from .json_loader import load_all_configurations


# Configuraciones de ejemplo hardcodeadas (para tests rápidos)
# Usando la convención D{n}-{idx}
_HARDCODED_EXAMPLES = {
    "D3-1": Configuration(
        coords=np.array([
            [np.float64(0.0), np.float64(0.0)],
            [np.float64(2.0), np.float64(0.0)],
            [np.float64(1.0), np.sqrt(np.float64(3.0))],
        ], dtype=np.float64),
        edges=[(0, 1), (1, 2), (2, 0)],
        name="D3-1",
    ),
    "D3-2": Configuration(
        coords=np.array([
            [np.float64(0.0), np.float64(0.0)],
            [np.float64(2.0), np.float64(0.0)],
            [np.float64(4.0), np.float64(0.0)],
        ], dtype=np.float64),
        edges=[(0, 1), (1, 2)],
        name="D3-2",
    ),
}


# Cache del catálogo completo
_CATALOG_CACHE: Dict[str, Configuration] = None


def _load_catalog() -> Dict[str, Configuration]:
    """
    Carga el catálogo completo de configuraciones.
    Se ejecuta una sola vez y se cachea el resultado.
    
    Returns:
        Diccionario {nombre: Configuration}
    """
    global _CATALOG_CACHE
    
    if _CATALOG_CACHE is not None:
        return _CATALOG_CACHE
    
    catalog = {}
    
    # 1. Agregar ejemplos hardcodeados primero
    catalog.update(_HARDCODED_EXAMPLES)
    
    # 2. Cargar configuraciones desde JSON (pueden sobrescribir ejemplos)
    try:
        json_configs = load_all_configurations("data")
        catalog.update(json_configs)
        print(f"✓ Cargadas {len(json_configs)} configuraciones desde data/")
    except Exception as e:
        print(f"⚠ No se pudieron cargar configuraciones desde data/: {e}")
    
    _CATALOG_CACHE = catalog
    return catalog

def _natural_sort_key(name: str) -> tuple:
    """
    Genera una clave de ordenamiento natural para nombres tipo 'Dn-m'.
    
    Ejemplos:
        D3-1 -> (3, 1)
        D5-10 -> (5, 10)
        D5-2 -> (5, 2)
    
    Así D5-2 viene antes que D5-10.
    """
    import re
    # Extraer números del formato "Dn-m"
    match = re.match(r'D(\d+)-(\d+)', name)
    if match:
        n = int(match.group(1))
        m = int(match.group(2))
        return (n, m)
    # Fallback para nombres no estándar
    return (0, 0)

def list_configurations() -> List[str]:
    """
    Lista todos los nombres de configuraciones disponibles.
    
    Returns:
        Lista ordenada de nombres de configuraciones
    """
    catalog = _load_catalog()
    names = list(catalog.keys())
    # Ordenar usando la clave de ordenamiento natural
    names.sort(key=_natural_sort_key)
    return names


def load_configuration(name: str) -> Configuration:
    """
    Carga una configuración por nombre.
    
    Args:
        name: Nombre de la configuración
        
    Returns:
        Objeto Configuration
        
    Raises:
        KeyError: Si la configuración no existe
    """
    catalog = _load_catalog()
    
    if name not in catalog:
        available = ', '.join(list(catalog.keys())[:10])
        raise KeyError(
            f"Configuración '{name}' no encontrada. "
            f"Disponibles: {available}... (total: {len(catalog)})"
        )
    
    return catalog[name]


def get_configurations_by_size(n_disks: int) -> List[str]:
    """
    Obtiene configuraciones con un número específico de discos.
    
    Args:
        n_disks: Número de discos
        
    Returns:
        Lista de nombres de configuraciones ordenada
        
    Examples:
        >>> get_configurations_by_size(3)
        ['D3-1', 'D3-2']
        >>> get_configurations_by_size(4)
        ['D4-1', 'D4-2', 'D4-3', 'D4-4', 'D4-5']
    """
    catalog = _load_catalog()
    configs = [name for name, config in catalog.items() if config.n == n_disks]
    configs.sort(key=_natural_sort_key)
    return configs


def get_catalog_stats() -> Dict[str, int]:
    """
    Obtiene estadísticas del catálogo.
    
    Returns:
        Diccionario con estadísticas
    """
    catalog = _load_catalog()
    
    # Contar por número de discos
    by_size = {}
    for config in catalog.values():
        n = config.n
        by_size[n] = by_size.get(n, 0) + 1
    
    return {
        'total': len(catalog),
        'by_size': by_size,
        'min_disks': min(c.n for c in catalog.values()) if catalog else 0,
        'max_disks': max(c.n for c in catalog.values()) if catalog else 0,
    }
