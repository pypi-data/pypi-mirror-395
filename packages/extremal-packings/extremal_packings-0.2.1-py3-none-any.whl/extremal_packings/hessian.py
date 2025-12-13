"""
Cálculo del Hessiano Intrínseco mediante Diferenciación Numérica.

Este módulo implementa el cálculo del Hessiano intrínseco del perímetro
sobre la variedad de restricciones, capturando tanto la curvatura euclidiana
como la curvatura extrínseca de la variedad.

Método:
-------
H_int = D(P ∇f) ≈ [P(c+εe_k)∇f(c+εe_k) - P(c-εe_k)∇f(c-εe_k)] / (2ε)

donde P(c) es el proyector ortogonal sobre el espacio tangente en c.

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
    epsilon: float = None,
    debug: bool = False
) -> np.ndarray:
    """
    Calcula el Hessiano intrínseco mediante diferenciación numérica.
    
    Implementa: H_int = D(V) donde V(c) = P(c) @ ∇f(c)
    
    El campo vectorial V captura automáticamente:
    - La proyección del Hessiano euclidiano: P H_eucl P
    - La contribución de curvatura: (D_v P) ∇f
    
    Args:
        config: Configuración de discos.
        R: Base del rolling space (para compatibilidad).
        epsilon: Tamaño del paso para diferencias finitas.
                 Por defecto: √eps * 10 ≈ 1.5e-7
        debug: Si True, imprime advertencias sobre anomalías numéricas.
    
    Returns:
        Matriz Hessiana intrínseca en el espacio ambiente (2n, 2n).
    """
    from .constraints import get_projector, compute_perimeter_gradient
    
    n = config.n
    dim = 2 * n
    
    if epsilon is None:
        epsilon = np.sqrt(np.finfo(np.float64).eps) * 10
    
    c = config.coords.flatten().astype(np.float64)
    H_full = np.zeros((dim, dim), dtype=np.float64)
    
    for k in range(dim):
        delta = np.zeros(dim, dtype=np.float64)
        delta[k] = epsilon
        
        c_plus = c + delta
        c_minus = c - delta
        
        coords_plus = c_plus.reshape(n, 2)
        coords_minus = c_minus.reshape(n, 2)
        
        config_plus = Configuration(
            coords=coords_plus,
            edges=config.edges,
            name=config.name,
            perimeter_edges=config.perimeter_edges
        )
        
        config_minus = Configuration(
            coords=coords_minus,
            edges=config.edges,
            name=config.name,
            perimeter_edges=config.perimeter_edges
        )
        
        P_plus = get_projector(config_plus)
        grad_plus = compute_perimeter_gradient(config_plus)
        v_plus = P_plus @ grad_plus
        
        P_minus = get_projector(config_minus)
        grad_minus = compute_perimeter_gradient(config_minus)
        v_minus = P_minus @ grad_minus
        
        H_full[:, k] = (v_plus - v_minus) / (np.float64(2.0) * epsilon)
        
        # Debug: detectar asimetrías numéricas significativas
        if debug and k < dim:
            P_orig = get_projector(config)
            grad_orig = compute_perimeter_gradient(config)
            v_orig = P_orig @ grad_orig
            
            diff_forward = (v_plus - v_orig) / epsilon
            diff_backward = (v_orig - v_minus) / epsilon
            asym = np.linalg.norm(diff_forward - diff_backward)
            
            if asym > 1e-6:
                print(f"Advertencia: Asimetría numérica en dirección {k}: {asym:.6e}")
    
    H_full = (H_full + H_full.T) / np.float64(2.0)
    
    return H_full


def project_to_roll(H_ambient: np.ndarray, R: np.ndarray) -> np.ndarray:
    """
    Proyecta el Hessiano del espacio ambiente al rolling space.
    
    H = R^T @ H_ambient @ R
    
    Args:
        H_ambient: Hessiano en el espacio ambiente (2n, 2n).
        R: Base ortonormal del rolling space (2n, d).
    
    Returns:
        Hessiano proyectado (d, d).
    """
    H = R.T @ H_ambient @ R
    H = (H + H.T) / np.float64(2.0)
    
    return H


def intrinsic_spectrum(H: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    """
    Calcula autovalores del Hessiano intrínseco.
    
    Args:
        H: Matriz Hessiana intrínseca (simétrica).
        tol: Tolerancia para considerar autovalores como cero.
    
    Returns:
        Array de autovalores ordenados (no-decreciente).
    """
    eigenvalues = np.linalg.eigvalsh(H)
    
    return eigenvalues

