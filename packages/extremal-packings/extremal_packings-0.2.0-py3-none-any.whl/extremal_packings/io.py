"""
Módulo de entrada/salida para configuraciones.

Provee funciones para guardar y cargar configuraciones en formato JSON.
"""

from __future__ import annotations
from typing import List, Tuple
import json
import numpy as np
from .configurations import Configuration


def load_from_json(path: str) -> Configuration:
    """
    Carga una configuración desde archivo JSON.
    
    Args:
        path: Ruta al archivo JSON
    
    Returns:
        Configuración cargada
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    coords = np.array(data["coords"], dtype=np.float64)
    edges: List[Tuple[int, int]] = [tuple(e) for e in data["edges"]]
    name = data.get("name")
    hull = data.get("hull_vertices")
    
    return Configuration(coords=coords, edges=edges, name=name, hull_vertices=hull)


def save_to_json(config: Configuration, path: str) -> None:
    """
    Guarda una configuración en archivo JSON.
    
    Args:
        config: Configuración a guardar
        path: Ruta del archivo de salida
    """
    data = {
        "name": config.name,
        "coords": config.coords.tolist(),
        "edges": config.edges,
        "hull_vertices": config.hull_vertices,
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)