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
        coords = np.zeros((n_disks, 2), dtype=np.float64)  # Usar float64 explícitamente
        
        for i, (x, y) in enumerate(coords_raw):
            coords[i, 0] = eval_expr(x)
            coords[i, 1] = eval_expr(y)
        
        # Procesar aristas
        edges = [tuple(edge) for edge in graph['contactos']]
        
        # Nombre de la configuración: D{n}-{idx+1}
        # Por ejemplo: D3-1, D4-2, D5-13, D6-47
        config_name = f"D{n_disks}-{idx + 1}"
        
        config = Configuration(
            coords=coords,
            edges=edges,
            name=config_name
        )
        
        configs.append(config)
    
    return configs


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
