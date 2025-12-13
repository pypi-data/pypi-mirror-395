"""
Extremal Packings - Análisis de Configuraciones de Discos Tangentes
==================================================================

Paquete para análisis geométrico y espectral de configuraciones de discos
unitarios tangentes en el plano.

Módulos Principales
-------------------
configurations
    Definición de la clase Configuration y operaciones básicas.
    
analysis
    Pipeline completo de análisis (matriz de contacto, Hessiano, espectro).
    
constraints
    Construcción de matriz de contacto A(c) y rolling space ker(A).
    
hessian
    Hessiano global K(c) y Hessiano intrínseco H = R^T K R.
    
perimeter
    Cálculo de perímetros y envolventes convexas.
    
catalog
    Catálogo de configuraciones predefinidas y carga desde JSON.
    
plotting
    Visualización con Matplotlib (gráficos estáticos).
    
interface
    Funciones de alto nivel para análisis y presentación.

Flujo de Trabajo Típico
------------------------
>>> from extremal_packings import load_configuration, analyze_configuration
>>> 
>>> # 1. Cargar configuración
>>> config = load_configuration("D5-7")  # Pentágono regular
>>> 
>>> # 2. Análisis completo
>>> result = analyze_configuration(config)
>>> 
>>> # 3. Inspeccionar resultados
>>> print(f"Rolling space dimension: {result.R.shape[1]}")
>>> print(f"Eigenvalues: {result.eigenvalues}")
>>> print(f"Perimeter: {result.perimeter_disks:.4f}")
>>> 
>>> # 4. Visualización
>>> from extremal_packings import plot_disks, print_analysis_summary
>>> print_analysis_summary(result)
>>> plot_disks(config, show_hull=True)

Conceptos Clave
---------------
**Configuración**: 
    n discos unitarios con centros c₁, ..., cₙ ∈ ℝ² y grafo de contacto G.
    
**Matriz de Contacto A(c)**: 
    Matriz m×2n donde cada fila representa un contacto (i,j):
    fila_k = [..., 0, -u_ij, 0, ..., 0, u_ij, 0, ...]
    con u_ij = (c_j - c_i) / ||c_j - c_i||
    
**Rolling Space**: 
    Roll(c) = ker(A(c)) ⊆ ℝ²ⁿ
    Espacio de deformaciones infinitesimales que preservan contactos.
    
**Hessiano Intrínseco**: 
    H = R^T K(c) R
    Proyección del Hessiano del perímetro al rolling space.
    Sus autovalores indican estabilidad de mínimos locales.

Ejemplos
--------
**Crear configuración personalizada:**

>>> import numpy as np
>>> from extremal_packings import Configuration, analyze_configuration
>>> 
>>> coords = np.array([[0, 0], [2, 0], [1, np.sqrt(3)]])
>>> edges = [(0, 1), (1, 2), (2, 0)]
>>> config = Configuration(coords=coords, edges=edges, name="Triangle")
>>> result = analyze_configuration(config)

**Análisis comparativo:**

>>> configs = ["D5-1", "D5-7", "D5-11"]
>>> for name in configs:
...     config = load_configuration(name)
...     result = analyze_configuration(config)
...     print(f"{name}: dim={result.R.shape[1]}, λ={result.eigenvalues}")

Referencias
-----------
- Connelly, R. (1980). The rigidity of polyhedral surfaces.
- Thurston, W. (1998). Shapes of polyhedra and triangulations.

Notas
-----
- Todas las configuraciones usan discos de radio unitario (r = 1).
- Los índices de vértices y aristas comienzan en 0.
- Las distancias entre centros en contacto deben ser ||c_j - c_i|| = 2.

Versión: 1.0
Autor: [Tu nombre]
"""

from .configurations import Configuration
from .analysis import AnalysisResult, analyze_configuration
from .catalog import (
    list_configurations, 
    load_configuration,
    get_configurations_by_size,
    get_catalog_stats,
)
from .perimeter import perimeter_centers, perimeter_disks, compute_hull
from .constraints import build_contact_matrix, rolling_space_basis
from .hessian import (
    compute_intrinsic_hessian,
    project_to_roll,
    intrinsic_spectrum,
)

from .plotting import (
    plot_disks,
    plot_contact_graph,
    plot_spectrum,
)

from .interface import (
    print_analysis_summary,
    show_complete_analysis,
    create_dashboard,
)

__all__ = [
    # Configuraciones
    "Configuration",
    "AnalysisResult",
    "analyze_configuration",
    "list_configurations",
    "load_configuration",
    "get_configurations_by_size",
    "get_catalog_stats",
    
    # Geometría
    "perimeter_centers",
    "perimeter_disks",
    "compute_hull",
    
    # Álgebra lineal
    "build_contact_matrix",
    "rolling_space_basis",
    "compute_intrinsic_hessian",
    "project_to_roll",
    "intrinsic_spectrum",
    
    # Visualización
    "plot_disks",
    "plot_contact_graph",
    "plot_spectrum",
    
    # Interfaz
    "print_analysis_summary",
    "show_complete_analysis",
    "create_dashboard",
]
