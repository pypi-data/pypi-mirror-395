"""
Pipeline de análisis de configuraciones de discos.

Este módulo implementa el flujo completo de análisis, desde la validación
del grafo hasta el cálculo del espectro del Hessiano intrínseco.

Classes:
    AnalysisResult: Contenedor de todos los resultados del análisis.

Functions:
    analyze_configuration: Pipeline completo de análisis.

Pipeline de Análisis
--------------------
1. **Validación**: Verificar conectividad y grados máximos del grafo.
2. **Matriz de Contacto**: Construir A(c) de dimensión m×2n.
3. **Rolling Space**: Calcular base ortonormal R de ker(A).
4. **Geometría**: Perímetros de envolventes convexas.
5. **Hessiano Global**: Ensamblar K(c) en ℝ²ⁿ.
6. **Hessiano Intrínseco**: Proyectar H = R^T K R.
7. **Espectro**: Calcular autovalores ordenados de H.

Complejidad Computacional
--------------------------
Para n discos y m contactos:
- Validación del grafo: O(n + m)
- Matriz de contacto: O(m·n)
- Rolling space (SVD): O(min(m, 2n)²·max(m, 2n))
- Convex hull: O(n log n)
- Hessiano global: O(m·n)
- Hessiano intrínseco: O(d²·n) donde d = dim(Roll)
- Espectro: O(d³)

Total: Dominado por SVD, típicamente O(n³) para grafos densos.

Examples
--------
>>> from extremal_packings import load_configuration, analyze_configuration
>>> config = load_configuration("D5-7")
>>> result = analyze_configuration(config)
>>> print(result.eigenvalues)
[0.0000e+00 6.1803e-01 1.6180e+00]
"""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.linalg import null_space

from .configurations import Configuration
from .contact_graphs import check_graph_validity
from .constraints import (
    build_contact_matrix,
    rolling_space_basis,
    compute_perimeter_gradient,
    project_gradient_to_kernel
)
from .perimeter import (
    perimeter_centers,
    perimeter_disks,
)
from .hessian import (
    compute_intrinsic_hessian,
    project_to_roll,
    intrinsic_spectrum,
)


@dataclass
class AnalysisResult:
    """
    Contenedor con todos los resultados del análisis.
    
    Attributes:
        config (Configuration): Configuración analizada.
        A (np.ndarray): Matriz de contacto de dimensión (m, 2n).
        R (np.ndarray): Base ortonormal del rolling space (2n, d).
        K (np.ndarray): Hessiano intrínseco en espacio ambiente (2n, 2n).
        H (np.ndarray): Hessiano intrínseco proyectado (d, d).
        eigenvalues (np.ndarray): Autovalores ordenados de H.
        perimeter_centers (float): Perímetro de convex hull de centros.
        perimeter_disks (float): Perímetro del cluster de discos.
        grad_p (np.ndarray): Gradiente del perímetro (2n,).
        proj_grad_p (np.ndarray): Gradiente proyectado al rolling space (2n,).
    
    Properties:
        rolling_dim (int): Dimensión del rolling space.
        is_rigid (bool): True si rolling_dim == 0.
        is_flexible (bool): True si rolling_dim > 0.
        is_critical (bool): True si gradiente proyectado ≈ 0.
        has_negative_eigenvalue (bool): True si min(eigenvalues) < 0.
        n_stable_modes (int): Número de autovalores positivos.
        n_unstable_modes (int): Número de autovalores negativos.
        n_neutral_modes (int): Número de autovalores cero.
    """
    config: Configuration

    # Contact matrix y rolling space
    A: np.ndarray
    R: np.ndarray

    # Proyección al rolling space
    grad_p: np.ndarray
    proj_grad_p: np.ndarray

    # Hessianos
    K: np.ndarray      # Hessiano global no restringido
    H: np.ndarray      # Hessiano proyectado al rolling space

    # Espectro del Hessiano intrínseco
    eigenvalues: np.ndarray

    # Perímetros (centros y discos)
    perimeter_centers: float
    perimeter_disks: float

    @property
    def rolling_dim(self) -> int:
        """
        Dimensión del rolling space.
        
        Returns:
            Número de grados de libertad infinitesimales = 2n - rank(A).
        """
        return self.R.shape[1]
    @property
    def is_critical(self) -> bool:
        """
        Verifica si la configuración es crítica a primer orden.
        
        Returns:
            True si el gradiente proyectado sobre Roll(c) es cero.
        
        Notes:
            Una configuración es crítica si no hay deformaciones
            infinitesimales que reduzcan el perímetro.
        """
        return np.allclose(self.proj_grad_p, 0.0)
    @property
    def is_rigid(self) -> bool:
        """
        Verifica si la configuración es infinitesimalmente rígida.
        
        Returns:
            True si no hay deformaciones (excepto movimientos rígidos).
        
        Notes:
            Una configuración es rígida si rolling_dim ≤ 3 (en el plano).
            Los 3 grados corresponden a traslaciones (2) y rotación (1).
        """
        return self.rolling_dim <= 3
    
    @property
    def is_flexible(self) -> bool:
        """
        Verifica si la configuración tiene flexibilidad infinitesimal.
        
        Returns:
            True si rolling_dim > 3.
        """
        return not self.is_rigid
    
    @property
    def has_negative_eigenvalue(self) -> bool:
        """
        Verifica si el Hessiano intrínseco tiene autovalores negativos.
        
        Returns:
            True si existe λ < -10⁻¹⁴ (considerando tolerancia numérica).
        
        Notes:
            Un autovalor negativo indica que la configuración no es
            un mínimo local del perímetro en el rolling space.
        """
        if len(self.eigenvalues) == 0:
            return False
        return self.eigenvalues[0] < -1e-14  # Aumentar de -1e-10 a -1e-14

    @property
    def n_stable_modes(self) -> int:
        """Número de modos estables (autovalores positivos)."""
        return int(np.sum(self.eigenvalues > 1e-14))
    
    @property
    def n_unstable_modes(self) -> int:
        """Número de modos inestables (autovalores negativos)."""
        return int(np.sum(self.eigenvalues < -1e-14))
    
    @property
    def n_neutral_modes(self) -> int:
        """Número de modos neutros (autovalores ≈ 0)."""
        return int(np.sum(np.abs(self.eigenvalues) <= 1e-14))
    
    @property
    def is_local_minimum(self) -> bool:
        """
        Verifica si es un mínimo local estricto.
        
        Returns:
            True si es crítico y todos los autovalores no nulos son positivos.
        """
        return self.is_critical and self.n_unstable_modes == 0 and self.n_stable_modes > 0
    
    @property
    def is_saddle_point(self) -> bool:
        """
        Verifica si es un punto silla.
        
        Returns:
            True si tiene autovalores negativos.
        """
        return self.has_negative_eigenvalue


def analyze_configuration(config: Configuration) -> AnalysisResult:
    """
    Pipeline completo de análisis de una configuración.
    
    Ejecuta todas las etapas del análisis en orden:
    1. Validación del grafo de contacto
    2. Construcción de la matriz de contacto A(c)
    3. Cálculo del rolling space (ker A) usando scipy.linalg.null_space
    4. Cálculo de perímetros
    5. Cálculo del gradiente y proyección
    6. Construcción del Hessiano intrínseco mediante diferenciación numérica
    7. Proyección al rolling space
    8. Análisis espectral de H
    
    Args:
        config: Configuración a analizar.
    
    Returns:
        Objeto AnalysisResult con todos los resultados.
    
    Raises:
        ValueError: Si el grafo no es conexo o tiene vértices con grado > 6.
        ValueError: Si los centros de algún contacto coinciden.
    
    Notes:
        - Usa scipy.linalg.null_space para garantizar consistencia exacta
          con el código de referencia de ManifoldSystem.
        - El Hessiano intrínseco se calcula mediante diferenciación
          numérica del gradiente proyectado, capturando automáticamente
          la curvatura de la variedad de restricciones.
        - Para configuraciones sin contactos (m=0), Roll(c) = ℝ²ⁿ.
        - Autovalores pequeños (|λ| < 10⁻¹²) se consideran cero numérico.
    """

    # -------------------------------
    # 1. Validación del grafo
    # -------------------------------
    check_graph_validity(config.n, config.edges)

    # -------------------------------
    # 2. Matriz de contacto A(c)
    # -------------------------------
    A = build_contact_matrix(config)

    # -------------------------------
    # 3. Rolling space R = ker(A)
    # -------------------------------
    if len(config.edges) == 0:
        # Caso sin contactos: ker(A) = R^{2n}
        R = np.eye(2 * config.n, dtype=np.float64)
    else:
        # Usar scipy.linalg.null_space con tolerancia 1e-12 (igual que referencia)
        R = null_space(A, rcond=1e-12)

    # -------------------------------
    # 4. Perímetros
    # -------------------------------
    p_centers = perimeter_centers(config)
    p_disks = perimeter_disks(config)

    # -------------------------------
    # 5. Criticidad a Primer Orden
    # -------------------------------
    grad_p = compute_perimeter_gradient(config)
    grad_p_proj = project_gradient_to_kernel(grad_p, R)

    # -------------------------------
    # 6. Hessiano Intrínseco (DIFERENCIACIÓN NUMÉRICA)
    # -------------------------------
    # Calcular en espacio ambiente capturando curvatura
    H_ambient = compute_intrinsic_hessian(config, R)
    
    # -------------------------------
    # 7. Proyección al Rolling Space
    # -------------------------------
    H = project_to_roll(H_ambient, R)
    
    # -------------------------------
    # 8. Autovalores
    # -------------------------------
    eigenvalues = intrinsic_spectrum(H)
    
    # -------------------------------
    # Empaquetar resultados
    # -------------------------------
    return AnalysisResult(
        config=config,
        A=A,
        R=R,
        K=H_ambient,
        H=H,
        grad_p=grad_p,
        proj_grad_p=grad_p_proj,
        eigenvalues=eigenvalues,
        perimeter_centers=p_centers,
        perimeter_disks=p_disks,
    )
