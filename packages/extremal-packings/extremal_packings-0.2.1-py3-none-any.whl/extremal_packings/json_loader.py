"""
Módulo para cargar configuraciones de discos desde archivos JSON.

Procesa los archivos en la carpeta data/ que contienen múltiples configuraciones
con expresiones matemáticas como "sqrt(3)", "cosd(30)", etc.
"""

from __future__ import annotations
from typing import List, Dict, Any, Union
import json
import numpy as np
from pathlib import Path
from .configurations import Configuration


def eval_expr(expr: Union[str, float, int]) -> float:
    """
    Evalúa una expresión matemática segura.
    
    Soporta:
    - Números directos: 0, 1, 2.5
    - sqrt(n): raíz cuadrada
    - cosd(degrees): coseno en grados
    - sind(degrees): seno en grados
    - Operaciones: +, -, *, /
    
    Args:
        expr: Expresión a evaluar (string o número)
        
    Returns:
        Valor numérico evaluado
        
    Examples:
        >>> eval_expr("sqrt(3)")
        1.732050807568877
        >>> eval_expr("2+sqrt(2)")
        3.414213562373095
    """
    if isinstance(expr, (int, float)):
        return np.float64(expr)
    
    expr = str(expr).strip()
    
    # Reemplazar funciones matemáticas
    expr = expr.replace('sqrt', 'np.sqrt')
    expr = expr.replace('cosd', '_cosd')
    expr = expr.replace('sind', '_sind')
    
    # Funciones auxiliares para grados
    def _cosd(degrees):
        return np.cos(np.radians(np.float64(degrees)))
    
    def _sind(degrees):
        return np.sin(np.radians(np.float64(degrees)))
    
    # Evaluar en un namespace seguro
    namespace = {
        'np': np,
        '_cosd': _cosd,
        '_sind': _sind,
    }
    
    try:
        result = eval(expr, {"__builtins__": {}}, namespace)
        return np.float64(result)
    except Exception as e:
        raise ValueError(f"No se pudo evaluar la expresión '{expr}': {e}")


def load_json_file(filepath: Path) -> List[Configuration]:
    """
    Carga todas las configuraciones de un archivo JSON.
    
    Args:
        filepath: Ruta al archivo JSON
        
    Returns:
        Lista de configuraciones cargadas
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    configs = []
    graphs = data.get('graphs', [])
    
    for idx, graph in enumerate(graphs):
        n_disks = graph['discos']
        
        # Procesar coordenadas (pueden tener expresiones matemáticas)
        coords_raw = graph['centros']
        coords = np.zeros((n_disks, 2), dtype=np.float64)
        
        for i, (x, y) in enumerate(coords_raw):
            coords[i, 0] = eval_expr(x)
            coords[i, 1] = eval_expr(y)
        
        # Procesar aristas
        edges = [tuple(edge) for edge in graph['contactos']]
        
        # Nombre de la configuración
        config_name = f"D{n_disks}-{idx + 1}"
        
        # Crear configuración temporal SIN perimeter_edges
        config = Configuration(
            coords=coords,
            edges=edges,
            name=config_name
        )
        
        # CALCULAR perimeter_edges UNA SOLA VEZ desde el hull
        config.perimeter_edges = _compute_perimeter_edges(config)
        
        configs.append(config)
    
    return configs


def _compute_perimeter_edges(config: Configuration) -> List[Tuple[int, int, float]]:
    """
    Calcula la definición explícita del perímetro desde el convex hull.
    
    Esta función se ejecuta UNA SOLA VEZ al cargar la configuración.
    """
    from .perimeter import compute_hull, is_collinear_chain, find_chain_endpoints
    
    hull = compute_hull(config)
    
    if len(hull) <= 1:
        return []
    
    # Detectar cadena colineal
    if is_collinear_chain(config, hull):
        # Perímetro = 2 * dist(extremo1, extremo2)
        i, j = find_chain_endpoints(config, hull)
        return [(i, j, 2.0)]
    else:
        # Perímetro = suma de aristas del hull
        perim_edges = []
        for k in range(len(hull)):
            i = hull[k]
            j = hull[(k + 1) % len(hull)]
            perim_edges.append((i, j, 1.0))
        return perim_edges


def load_all_configurations(data_dir: str = "data") -> Dict[str, Configuration]:
    """
    Carga todas las configuraciones de todos los archivos JSON en data_dir.
    
    Args:
        data_dir: Directorio que contiene los archivos JSON
        
    Returns:
        Diccionario {nombre_config: Configuration}
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        # Intentar con ruta relativa desde el módulo
        module_dir = Path(__file__).parent.parent
        data_path = module_dir / data_dir
    
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el directorio de datos: {data_dir}")
    
    all_configs = {}
    
    # Buscar todos los archivos JSON
    json_files = sorted(data_path.glob("*.json"))
    
    for json_file in json_files:
        try:
            configs = load_json_file(json_file)
            for config in configs:
                all_configs[config.name] = config
        except Exception as e:
            print(f"Advertencia: Error al cargar {json_file}: {e}")
            continue
    
    return all_configs
