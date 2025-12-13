"""
Cálculo del Hessiano Intrínseco mediante Diferenciación Numérica.

Este módulo implementa el cálculo del Hessiano intrínseco del perímetro
sobre la variedad de restricciones, capturando tanto la curvatura euclidiana
como la curvatura extrínseca de la variedad.

Método:
-------
H_int = D(P ∇f) ≈ [P(c+εe_k)∇f(c+εe_k) - P(c-εe_k)∇f(c-εe_k)] / (2ε)

donde P(c) es el proyector ortogonal sobre el espacio tangente en c.

Esta implementación replica exactamente la lógica del código de referencia
ManifoldSystem.compute_intrinsic_hessian_operator().

Functions:
    compute_intrinsic_hessian: Calcula H_int en el espacio ambiente.
    project_to_roll: Proyecta al rolling space para análisis espectral.
    intrinsic_spectrum: Autovalores del Hessiano intrínseco.
"""

from __future__ import annotations
import numpy as np
from .configurations import Configuration


def compute_intrinsic_hessian(
    config: Configuration, 
    R: np.ndarray,
    epsilon: float = None
) -> np.ndarray:
    """
    Calcula el Hessiano intrínseco mediante diferenciación numérica.
    
    Implementa: H_int = D(V) donde V(c) = P(c) @ ∇f(c)
    
    Replica exactamente ManifoldSystem.compute_intrinsic_hessian_operator():
    - Usa epsilon = √(machine_eps) * 10 ≈ 1.5e-7
    - Usa float64 explícitamente en todos los cálculos
    - Diferencias centradas: [V(c+ε) - V(c-ε)] / (2ε)
    
    El campo vectorial V captura automáticamente:
    - La proyección del Hessiano euclidiano: P H_eucl P
    - La contribución de curvatura: (D_v P) ∇f
    
    Args:
        config: Configuración de discos.
        R: Base del rolling space (para compatibilidad, no se usa aquí).
        epsilon: Tamaño del paso para diferencias finitas.
                 Por defecto: √eps * 10 ≈ 1.5e-7
    
    Returns:
        Matriz Hessiana intrínseca en el espacio ambiente (2n, 2n).
    
    Notes:
        - Usa diferencias finitas centradas para mayor precisión.
        - El proyector P cambia con c, capturando la curvatura extrínseca.
        - La matriz resultante es simétrica (se simetriza al final).
    """
    from .constraints import get_projector, compute_perimeter_gradient
    
    n = config.n
    dim = 2 * n
    
    # Epsilon idéntico al código de referencia
    if epsilon is None:
        epsilon = np.sqrt(np.finfo(np.float64).eps) * 10  # ~1.5e-7
    
    # Configuración actual (vector de coordenadas aplanado)
    c = config.coords.flatten().astype(np.float64)
    
    # Matriz Hessiana completa (usar float64 explícito)
    H_full = np.zeros((dim, dim), dtype=np.float64)
    
    # Para cada dirección en el espacio ambiente
    for k in range(dim):
        # Perturbación en la dirección k (usar float64 explícito)
        delta = np.zeros(dim, dtype=np.float64)
        delta[k] = epsilon
        
        # Configuraciones perturbadas
        c_plus = c + delta
        c_minus = c - delta
        
        # Crear configuraciones temporales
        coords_plus = c_plus.reshape(n, 2)
        coords_minus = c_minus.reshape(n, 2)
        
        config_plus = Configuration(
            coords=coords_plus,
            edges=config.edges,
            name=config.name
        )
        
        config_minus = Configuration(
            coords=coords_minus,
            edges=config.edges,
            name=config.name
        )
        
        # Campo vectorial proyectado en c+
        P_plus = get_projector(config_plus)
        grad_plus = compute_perimeter_gradient(config_plus)
        v_plus = P_plus @ grad_plus
        
        # Campo vectorial proyectado en c-
        P_minus = get_projector(config_minus)
        grad_minus = compute_perimeter_gradient(config_minus)
        v_minus = P_minus @ grad_minus
        
        # Derivada numérica (diferencias centradas)
        H_full[:, k] = (v_plus - v_minus) / (np.float64(2.0) * epsilon)
    
    # Simetrizar para eliminar ruido numérico
    H_full = (H_full + H_full.T) / np.float64(2.0)
    
    return H_full


def project_to_roll(H_ambient: np.ndarray, R: np.ndarray) -> np.ndarray:
    """
    Proyecta el Hessiano del espacio ambiente al rolling space.
    
    H = R^T @ H_ambient @ R
    
    Replica la proyección del código de referencia:
    H_reduced = Z.T @ H_op @ Z
    
    Args:
        H_ambient: Hessiano en el espacio ambiente (2n, 2n).
        R: Base ortonormal del rolling space (2n, d).
    
    Returns:
        Hessiano proyectado (d, d).
    
    Notes:
        Esta proyección preserva la forma cuadrática sobre
        el subespacio generado por R.
    """
    H = R.T @ H_ambient @ R
    
    # Simetrizar nuevamente por seguridad (igual que referencia)
    H = (H + H.T) / np.float64(2.0)
    
    return H


def intrinsic_spectrum(H: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    """
    Calcula autovalores del Hessiano intrínseco.
    
    Usa np.linalg.eigvalsh (idéntico al código de referencia) y
    tolerancia 1e-12 para clasificación de autovalores.
    
    Args:
        H: Matriz Hessiana intrínseca (simétrica).
        tol: Tolerancia para considerar autovalores como cero.
    
    Returns:
        Array de autovalores ordenados (no-decreciente).
    
    Notes:
        - Autovalores < -tol: Modos inestables (punto silla).
        - Autovalores ≈ 0: Modos neutros (rigidez infinitesimal).
        - Autovalores > tol: Modos estables (mínimo local).
        - Usa eigvalsh (matrices simétricas) para máxima precisión.
    """
    # Usar eigvalsh para matrices simétricas (igual que referencia)
    eigenvalues = np.linalg.eigvalsh(H)
    
    # NO aproximar valores pequeños a cero aquí
    # Dejar que el código de análisis decida con base en tol=1e-12
    
    return eigenvalues

