from __future__ import annotations
from typing import Dict, Tuple
import numpy as np
from scipy.linalg import null_space
from .configurations import Configuration


def contact_normals(config: Configuration) -> Dict[Tuple[int, int], np.ndarray]:
    """
    Devuelve un diccionario {(i,j): u_ij} con u_ij normal de contacto.
    Se asume distancia > 0; si no es 2, se normaliza igualmente.
    """
    normals: Dict[Tuple[int, int], np.ndarray] = {}
    coords = config.coords
    for (i, j) in config.edges:
        diff = coords[j] - coords[i]
        dist = np.linalg.norm(diff)
        if dist == 0:
            raise ValueError(f"Centros {i} y {j} coinciden (distancia 0)")
        u = diff / dist
        normals[(i, j)] = u
    return normals


def build_contact_matrix(config: Configuration) -> np.ndarray:
    """
    Construye la matriz de contacto A(c) de tamaño (m x 2n).
    Cada fila (i,j) lleva -u_ij en columnas 2*i,2*i+1 y u_ij en 2*j,2*j+1.
    """
    n = config.n
    m = len(config.edges)
    A = np.zeros((m, 2 * n), dtype=np.float64)  # Usar float64 explícitamente
    normals = contact_normals(config)
    for row_idx, (i, j) in enumerate(config.edges):
        u = normals[(i, j)]
        A[row_idx, 2 * i : 2 * i + 2] = -u
        A[row_idx, 2 * j : 2 * j + 2] = u
    return A


def rolling_space_basis(A: np.ndarray, rtol: float = 1e-12) -> np.ndarray:
    """
    Calcula una base ortonormal de ker(A) usando scipy.linalg.null_space.
    Devuelve R de tamaño (2n x d), cuyas columnas generan Roll(c).
    
    Args:
        A: Matriz de contacto (m, 2n)
        rtol: Tolerancia relativa para determinar el rango (rcond en null_space)
    
    Returns:
        Base ortonormal del kernel de A
    
    Notes:
        Usa scipy.linalg.null_space que internamente usa SVD pero garantiza
        una base ortonormal consistente con el código de referencia.
    """
    if A.size == 0:
        raise ValueError("rolling_space_basis: matriz A vacía")
    
    # Usar null_space de scipy (idéntico al código de referencia)
    R = null_space(A, rcond=rtol)
    
    return R


def compute_perimeter_gradient(config: Configuration) -> np.ndarray:
    """
    Calcula el gradiente del perímetro de la envolvente convexa
    con respecto a las coordenadas de los centros.
    
    Para cadenas colineales: ∇Per = 2 * ∇dist(inicio, fin)
    Para hulls generales: ∇Per = suma de ∇dist(vértices consecutivos)
    
    Returns:
        Array de forma (2n,) con el gradiente.
    """
    from .perimeter import compute_hull, is_collinear_chain, find_chain_endpoints
    
    n = config.n
    coords = config.coords
    hull = config.hull_vertices if config.hull_vertices is not None else compute_hull(config)
    
    gradient = np.zeros(2 * n, dtype=np.float64)  # Usar float64 explícitamente
    
    if len(hull) <= 1:
        return gradient
    
    # Detectar si es una cadena colineal
    if is_collinear_chain(config, hull):
        # Caso especial: cadena colineal
        # Per = 2 * ||c_fin - c_inicio||
        # ∇Per = 2 * [∂/∂c_i (||c_fin - c_inicio||)]
        
        i, j = find_chain_endpoints(config, hull)
        
        diff = coords[j] - coords[i]
        dist = np.linalg.norm(diff)
        
        if dist > np.float64(1e-12):
            # Vector unitario de i hacia j
            u = diff / dist
            
            # Gradiente: ∂dist/∂c_i = -u, ∂dist/∂c_j = +u
            # Multiplicar por 2 porque Per = 2 * dist
            gradient[2*i:2*i+2] = np.float64(-2.0) * u
            gradient[2*j:2*j+2] = np.float64(2.0) * u
        
        return gradient
    
    # Caso general: polígono convexo
    # Para cada arista del hull, contribuir al gradiente
    for k in range(len(hull)):
        i = hull[k]
        j = hull[(k + 1) % len(hull)]
        
        diff = coords[j] - coords[i]
        dist = np.linalg.norm(diff)
        
        if dist > np.float64(1e-12):
            # Tangente unitario en dirección i->j
            t = diff / dist
            
            # Contribuciones al gradiente
            gradient[2*i:2*i+2] -= t
            gradient[2*j:2*j+2] += t
    
    return gradient


def project_gradient_to_kernel(gradient: np.ndarray, R: np.ndarray) -> np.ndarray:
    """
    Proyecta el gradiente sobre el kernel de la matriz de contacto (rolling space).
    
    Args:
        gradient: Vector gradiente en R^{2n}
        R: Base del rolling space (2n x d)
    
    Returns:
        Proyección del gradiente: R (R^T R)^{-1} R^T gradient
    """
    if R.shape[1] == 0:
        return np.zeros_like(gradient)
    
    # Proyector P = R (R^T R)^{-1} R^T
    # Como R es ortonormal (de SVD), R^T R = I, entonces P = R R^T
    projection = R @ (R.T @ gradient)
    
    # Aproximar valores pequeños a cero
    projection[np.abs(projection) < 1e-12] = 0.0
    
    return projection


def compute_hull_tangents(config: Configuration) -> Dict[Tuple[int, int], np.ndarray]:
    """
    Calcula los vectores tangentes para cada arista del convex hull.
    
    Returns:
        Diccionario {(i,j): tangente} donde tangente apunta de i hacia j.
    """
    from .perimeter import compute_hull
    
    coords = config.coords
    hull = config.hull_vertices if config.hull_vertices is not None else compute_hull(config)
    
    tangents: Dict[Tuple[int, int], np.ndarray] = {}
    
    if len(hull) <= 1:
        return tangents
    
    # Generar TODAS las aristas del hull (consecutivas formando el polígono)
    for k in range(len(hull)):
        i = hull[k]
        j = hull[(k + 1) % len(hull)]
        
        diff = coords[j] - coords[i]
        dist = np.linalg.norm(diff)
        
        if dist > 1e-12:
            # Tangente unitario en dirección i->j
            t = diff / dist
            tangents[(i, j)] = t
    
    return tangents


def compute_contact_tangents(config: Configuration) -> Dict[Tuple[int, int], np.ndarray]:
    """
    Calcula los vectores tangentes (perpendiculares a las normales de contacto).
    
    Returns:
        Diccionario {(i,j): tangente} perpendicular a la normal de contacto.
    """
    normals = contact_normals(config)
    tangents: Dict[Tuple[int, int], np.ndarray] = {}
    
    for (i, j), normal in normals.items():
        # Tangente perpendicular: rotar normal 90° en sentido antihorario
        tangent = np.array([-normal[1], normal[0]])
        tangents[(i, j)] = tangent
    
    return tangents


def compute_disk_hull_geometry(config: Configuration, radius: float = 1.0) -> Dict:
    """
    Calcula la geometría completa de la envolvente convexa de discos.
    
    Para cada par consecutivo de discos en el hull, calcula:
    - Puntos de tangencia externa
    - Ángulos para dibujar los arcos
    
    Returns:
        Diccionario con:
        - 'tangent_segments': lista de segmentos tangentes [(x1,y1), (x2,y2)]
        - 'arcs': lista de arcos [(center, r, angle_start, angle_end)]
    """
    from .perimeter import compute_hull
    
    coords = config.coords
    hull = config.hull_vertices if config.hull_vertices is not None else compute_hull(config)
    
    result = {
        'tangent_segments': [],
        'arcs': []
    }
    
    if len(hull) < 2:
        return result
    
    n_hull = len(hull)
    
    # Calcular centroide del hull para determinar orientación
    hull_center = np.mean(coords[hull], axis=0)
    
    # Detectar si es una cadena colineal
    def is_collinear():
        """Verifica si todos los centros del hull están en línea recta."""
        if n_hull < 3:
            return True  # 2 puntos siempre son colineales
        
        # Tomar los tres primeros puntos
        p0 = coords[hull[0]]
        p1 = coords[hull[1]]
        p2 = coords[hull[2]]
        
        # Producto cruz debe ser ~0 si son colineales
        cross = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
        
        return abs(cross) < 1e-6
    
    collinear = is_collinear()
    
    # Función para calcular tangentes externas entre dos discos de igual radio
    def external_tangents(disk1_center, disk2_center, r):
        """Calcula las dos tangentes externas entre dos discos de igual radio."""
        dx = disk2_center[0] - disk1_center[0]
        dy = disk2_center[1] - disk1_center[1]
        distance = np.hypot(dx, dy)
        
        if distance < 1e-10:
            return None
        
        # Ángulo base entre centros
        base_angle = np.arctan2(dy, dx)
        
        # Dos perpendiculares (90° en cada dirección)
        perp_angle1 = base_angle + np.pi/2
        perp_angle2 = base_angle - np.pi/2
        
        return [
            {
                'p1': disk1_center + r * np.array([np.cos(perp_angle1), np.sin(perp_angle1)]),
                'p2': disk2_center + r * np.array([np.cos(perp_angle1), np.sin(perp_angle1)]),
                'side': 'top'  # Perpendicular hacia arriba
            },
            {
                'p1': disk1_center + r * np.array([np.cos(perp_angle2), np.sin(perp_angle2)]),
                'p2': disk2_center + r * np.array([np.cos(perp_angle2), np.sin(perp_angle2)]),
                'side': 'bottom'  # Perpendicular hacia abajo
            }
        ]
    
    # Función para seleccionar la tangente externa
    def select_hull_tangent(tangents, disk1_center, disk2_center):
        """Selecciona la tangente externa correcta."""
        if not tangents or len(tangents) == 0:
            return None
        if len(tangents) == 1:
            return tangents[0]
        
        if collinear:
            # Para cadenas colineales: elegir la tangente que está en el mismo lado
            # Usamos la tangente 'top' (perpendicular hacia arriba respecto al eje x)
            # Esto asegura consistencia en toda la cadena
            for tangent in tangents:
                if tangent['side'] == 'top':
                    return tangent
            return tangents[0]
        else:
            # Para hulls no colineales: elegir la más alejada del centroide
            best_tangent = tangents[0]
            max_distance = -np.inf
            
            for tangent in tangents:
                # Punto medio del segmento tangente
                mid_point = (tangent['p1'] + tangent['p2']) / 2
                distance = np.linalg.norm(mid_point - hull_center)
                
                if distance > max_distance:
                    max_distance = distance
                    best_tangent = tangent
            
            return best_tangent
    
    # Almacenar tangentes seleccionadas para cada arista
    selected_tangents = []
    
    # 1. Calcular segmentos tangentes entre discos consecutivos
    for k in range(n_hull):
        i = hull[k]
        j = hull[(k + 1) % n_hull]
        
        ci = coords[i]
        cj = coords[j]
        
        # Calcular las dos tangentes externas posibles
        tangents = external_tangents(ci, cj, radius)
        
        if tangents:
            # Seleccionar la tangente externa
            selected = select_hull_tangent(tangents, ci, cj)
            
            if selected is not None:
                selected_tangents.append({
                    'disk_i': i,
                    'disk_j': j,
                    'tangent': selected
                })
                
                result['tangent_segments'].append({
                    'start': selected['p1'].tolist(),
                    'end': selected['p2'].tolist(),
                    'disk_i': int(i),
                    'disk_j': int(j)
                })
    
    # 2. Calcular arcos para cada disco del hull
    for k in range(n_hull):
        i = hull[k]
        ci = coords[i]
        
        # Encontrar tangentes que involucran al disco i
        prev_tangent = None
        next_tangent = None
        
        for t in selected_tangents:
            if t['disk_j'] == i:
                prev_tangent = t['tangent']['p2']  # punto en disco i
            if t['disk_i'] == i:
                next_tangent = t['tangent']['p1']  # punto en disco i
        
        # Para cadenas colineales, los discos extremos necesitan semicírculos
        if collinear and (k == 0 or k == n_hull - 1):
            # Disco extremo en cadena colineal
            if k == 0:
                # Primer disco: usar la tangente hacia el siguiente
                if next_tangent is not None:
                    neighbor_idx = hull[1] if n_hull > 1 else None
            else:
                # Último disco: usar la tangente desde el anterior
                if prev_tangent is not None:
                    neighbor_idx = hull[n_hull - 2] if n_hull > 1 else None
            
            if neighbor_idx is not None:
                neighbor_pos = coords[neighbor_idx]
                
                # Vector del disco hacia su vecino
                to_neighbor = neighbor_pos - ci
                angle_to_neighbor = np.arctan2(to_neighbor[1], to_neighbor[0])
                
                # Semicírculo: empezar 90° perpendicular y terminar en el opuesto (-90°)
                # Esto da un arco de exactamente 180° por el lado opuesto al vecino
                angle_start_rad = angle_to_neighbor + np.pi/2
                angle_end_rad = angle_to_neighbor - np.pi/2
                
                # Convertir a grados
                angle_start_deg = np.degrees(angle_start_rad)
                angle_end_deg = np.degrees(angle_end_rad)
                
                result['arcs'].append({
                    'center': ci.tolist(),
                    'radius': radius,
                    'angle_start': angle_start_deg,
                    'angle_end': angle_end_deg,
                    'disk': int(i)
                })
        
        elif prev_tangent is not None and next_tangent is not None:
            # Caso normal: discos intermedios o no colineales
            # Calcular ángulos de los puntos de tangencia respecto al centro del disco
            angle_prev_rad = np.arctan2(prev_tangent[1] - ci[1], prev_tangent[0] - ci[0])
            angle_next_rad = np.arctan2(next_tangent[1] - ci[1], next_tangent[0] - ci[0])
            
            # Calcular la diferencia angular
            angle_diff = angle_next_rad - angle_prev_rad
            while angle_diff < 0:
                angle_diff += 2 * np.pi
            while angle_diff >= 2 * np.pi:
                angle_diff -= 2 * np.pi
            
            # Para el hull exterior, queremos el arco CORTO (< π)
            if angle_diff > np.pi:
                angle_start_rad = angle_next_rad
                angle_end_rad = angle_prev_rad + 2 * np.pi
                actual_arc_rad = 2 * np.pi - angle_diff
            else:
                angle_start_rad = angle_prev_rad
                angle_end_rad = angle_next_rad
                actual_arc_rad = angle_diff
            
            # Convertir a grados
            angle_start_deg = np.degrees(angle_start_rad)
            angle_end_deg = np.degrees(angle_end_rad)
            
            # Solo agregar arcos significativos
            if np.degrees(actual_arc_rad) > 0.1:
                result['arcs'].append({
                    'center': ci.tolist(),
                    'radius': radius,
                    'angle_start': angle_start_deg,
                    'angle_end': angle_end_deg,
                    'disk': int(i)
                })
    
    return result


def get_projector(config: Configuration, tol: float = 1e-12) -> np.ndarray:
    """
    Calcula el proyector ortogonal sobre el espacio tangente (kernel de A).
    
    P = I - A^T (A A^T)^{-1} A
    
    Se usa la pseudo-inversa para estabilidad numérica.
    
    Args:
        config: Configuración de discos.
        tol: Tolerancia para la pseudo-inversa.
    
    Returns:
        Matriz proyector (2n, 2n).
    
    Notes:
        P es idempotente (P^2 = P) y simétrico (P^T = P).
        Proyecta vectores sobre ker(A), el rolling space.
    """
    n = config.n
    dim = 2 * n
    
    # Caso sin contactos: proyector es la identidad
    if len(config.edges) == 0:
        return np.eye(dim, dtype=np.float64)
    
    # Construir matriz de contacto
    A = build_contact_matrix(config)
    
    # Proyector: I - pinv(A) @ A
    # Equivalente a: I - A^T (A A^T)^{-1} A
    P = np.eye(dim, dtype=np.float64) - np.linalg.pinv(A, rcond=tol) @ A
    
    return P