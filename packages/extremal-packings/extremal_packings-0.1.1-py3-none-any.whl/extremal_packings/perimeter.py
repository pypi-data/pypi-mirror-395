from __future__ import annotations
from typing import List, Optional, Dict
import numpy as np
from .configurations import Configuration


def _cross(o: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    """Producto cruz 2D (o->a) x (o->b)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def compute_hull(config: Configuration) -> List[int]:
    """
    Envolvente convexa de los centros (monotone chain).
    Devuelve índices de los vértices del hull en orden CCW.
    """
    pts = config.coords
    n = pts.shape[0]
    if n <= 1:
        return list(range(n))
    
    if n == 2:
        return [0, 1]

    # ordenar por (x,y)
    idx_sorted = sorted(range(n), key=lambda i: (pts[i, 0], pts[i, 1]))
    
    lower: List[int] = []
    for i in idx_sorted:
        while len(lower) >= 2 and _cross(
            pts[lower[-2]], pts[lower[-1]], pts[i]
        ) <= 0:
            lower.pop()
        lower.append(i)

    upper: List[int] = []
    for i in reversed(idx_sorted):
        while len(upper) >= 2 and _cross(
            pts[upper[-2]], pts[upper[-1]], pts[i]
        ) <= 0:
            upper.pop()
        upper.append(i)

    # Remover el último punto de cada lista porque se duplica
    hull = lower[:-1] + upper[:-1]
    
    # Quitar duplicados preservando orden
    seen = set()
    unique_hull: List[int] = []
    for i in hull:
        if i not in seen:
            seen.add(i)
            unique_hull.append(i)
    
    return unique_hull


def is_collinear_chain(config: Configuration, hull: List[int]) -> bool:
    """
    Verifica si el hull forma una cadena colineal.
    
    Una cadena colineal es un conjunto de puntos en línea recta donde:
    - Todos los centros están alineados
    - El hull solo incluye los extremos
    
    Args:
        config: Configuración de discos
        hull: Índices de vértices del convex hull
    
    Returns:
        True si es una cadena colineal
    """
    coords = config.coords
    n_hull = len(hull)
    
    # Si hay menos de 3 puntos en el hull, siempre es colineal
    if n_hull < 3:
        return True
    
    # Tomar los tres primeros puntos del hull
    p0 = coords[hull[0]]
    p1 = coords[hull[1]]
    p2 = coords[hull[2]]
    
    # Producto cruz debe ser ~0 si son colineales
    cross = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
    
    return abs(cross) < 1e-6


def find_chain_endpoints(config: Configuration, hull: List[int]) -> tuple[int, int]:
    """
    Encuentra los extremos de una cadena colineal.
    
    Para una cadena colineal, los extremos son los dos puntos del hull
    más distantes entre sí.
    
    Args:
        config: Configuración de discos
        hull: Índices de vértices del convex hull
    
    Returns:
        Tupla (índice_inicio, índice_fin) de los extremos
    """
    coords = config.coords
    
    if len(hull) == 2:
        return hull[0], hull[1]
    
    # Encontrar los dos puntos más distantes en el hull
    max_dist = -1
    endpoint_i, endpoint_j = hull[0], hull[1]
    
    for i in hull:
        for j in hull:
            if i != j:
                dist = np.linalg.norm(coords[j] - coords[i])
                if dist > max_dist:
                    max_dist = dist
                    endpoint_i, endpoint_j = i, j
    
    return endpoint_i, endpoint_j


def compute_disk_hull_geometry(config: Configuration, radius: float = 1.0) -> Optional[Dict]:
    """
    Calcula la geometría completa del hull de discos (tangentes externas + arcos).
    Replica exactamente la lógica del código JavaScript de referencia.
    
    Args:
        config: Configuración de discos
        radius: Radio de los discos
    
    Returns:
        Diccionario con:
        - 'tangent_segments': Lista de segmentos tangentes {start, end}
        - 'arcs': Lista de arcos {center, radius, angle_start, angle_end}
    """
    coords = config.coords
    hull_indices = compute_hull(config)
    
    if len(hull_indices) < 2:
        return None
    
    n_hull = len(hull_indices)
    tangent_segments = []
    tangent_points = []  # Guardar puntos de tangencia para calcular arcos
    
    # PASO 1: Calcular segmentos tangentes entre pares consecutivos
    for k in range(n_hull):
        i = hull_indices[k]
        j = hull_indices[(k + 1) % n_hull]
        
        ci = coords[i]
        cj = coords[j]
        
        # Vector de i a j
        diff = cj - ci
        dist = np.linalg.norm(diff)
        
        if dist < 1e-10:
            tangent_points.append((ci, ci))
            continue
        
        # Vector unitario de i a j
        u = diff / dist
        
        # Vector perpendicular (rotación 90° CW) - apunta a la DERECHA del vector i->j
        # Esto da las tangentes EXTERNAS al cluster
        perp = np.array([u[1], -u[0]])  # Rotación -90° (CW)
        
        # Puntos de tangencia externa (perpendicular hacia afuera)
        ti = ci + perp * radius
        tj = cj + perp * radius
        
        tangent_points.append((ti, tj))
        
        tangent_segments.append({
            'start': ti.tolist(),
            'end': tj.tolist()
        })
    
    # PASO 2: Calcular arcos para cada disco del hull
    arcs = []
    for k in range(n_hull):
        i = hull_indices[k]
        ci = coords[i]
        
        # Punto de tangencia del segmento ANTERIOR (que termina en este disco)
        # Este es el punto 'end' del segmento anterior
        ti_from_prev = tangent_points[(k - 1) % n_hull][1]
        
        # Punto de tangencia del segmento SIGUIENTE (que empieza en este disco)
        # Este es el punto 'start' del segmento actual
        ti_to_next = tangent_points[k][0]
        
        # Calcular ángulos de estos puntos de tangencia respecto al centro
        angle_from_prev = np.degrees(np.arctan2(
            ti_from_prev[1] - ci[1],
            ti_from_prev[0] - ci[0]
        ))
        
        angle_to_next = np.degrees(np.arctan2(
            ti_to_next[1] - ci[1],
            ti_to_next[0] - ci[0]
        ))
        
        # Normalizar a [0, 360)
        angle_from_prev = angle_from_prev % 360
        angle_to_next = angle_to_next % 360
        
        arcs.append({
            'center': ci.tolist(),
            'radius': radius,
            'angle_start': angle_from_prev,
            'angle_end': angle_to_next
        })
    
    return {
        'tangent_segments': tangent_segments,
        'arcs': arcs
    }


def perimeter_centers(config: Configuration) -> float:
    """
    Perímetro de la envolvente convexa de los centros.
    
    Para cadenas colineales: Per = 2 * dist(inicio, fin)
    Para hulls generales: Per = suma de distancias entre vértices consecutivos
    """
    coords = config.coords
    hull = config.hull_vertices if config.hull_vertices is not None else compute_hull(config)
    
    if len(hull) <= 1:
        return np.float64(0.0)
    
    # Detectar si es una cadena colineal
    if is_collinear_chain(config, hull):
        # Caso especial: cadena colineal
        # Per = 2 * distancia entre extremos
        i, j = find_chain_endpoints(config, hull)
        return np.float64(2.0) * float(np.linalg.norm(coords[j] - coords[i]))
    
    # Caso general: polígono convexo
    per = np.float64(0.0)
    for k in range(len(hull)):
        i = hull[k]
        j = hull[(k + 1) % len(hull)]
        per += float(np.linalg.norm(coords[j] - coords[i]))
    return per


def perimeter_disks(config: Configuration, radius: float = 1.0) -> float:
    """
    Perímetro del cluster de discos.
    
    Para cadenas colineales: Per = 2 * dist(inicio, fin) + 2πr
    Para hulls generales: Per = Per(center hull) + 2πr
    
    Por defecto r = 1 (discos unitarios).
    """
    # Usar precisión máxima para π
    return perimeter_centers(config) + np.float64(2.0) * np.pi * np.float64(radius)
