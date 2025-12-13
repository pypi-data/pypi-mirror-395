"""
Configuraciones de discos tangentes.

Este módulo define la estructura de datos fundamental para representar
configuraciones de discos unitarios tangentes en el plano.

Classes:
    Configuration: Configuración de n discos con su grafo de contacto.

Types:
    Edge: Tupla (i, j) representando una arista del grafo de contacto.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np


Edge = Tuple[int, int]


@dataclass
class Configuration:
    """
    Representa una configuración de n discos unitarios tangentes.
    
    Una configuración consiste en n discos de radio 1 con centros especificados
    y un grafo de contacto que indica qué pares de discos son tangentes.
    
    Attributes:
        coords (np.ndarray): Matriz (n, 2) con coordenadas de los centros.
            Cada fila representa un punto (x, y) ∈ ℝ².
        edges (List[Edge]): Lista de aristas del grafo de contacto.
            Cada arista (i, j) indica que los discos i y j son tangentes.
        name (Optional[str]): Nombre identificador de la configuración.
            Por convención: "D{n}-{índice}" (ej: "D5-7").
        hull_vertices (Optional[List[int]]): Índices de vértices del convex hull.
            Si es None, se calcula bajo demanda.
        perimeter_edges (Optional[List[Tuple[int, int, float]]]): Lista de tuplas (i, j, weight) que definen el perímetro.
            Ejemplo: [(0, 4, 2.0)] para cadena significa Per = 2 * dist(0, 4)
            Si es None, debe ser proporcionado externamente o calculado antes de usar.
        n (int): Número de discos (calculado automáticamente).
    
    Constraints:
        - Los índices en edges deben estar en el rango [0, n-1].
        - No se permiten bucles (i == i).
        - Para discos tangentes: ||c_j - c_i|| = 2 (radio unitario).
        - El grafo de contacto debe ser conexo (excepto n = 1).
    
    Examples:
        >>> import numpy as np
        >>> # Triángulo equilátero
        >>> coords = np.array([[0, 0], [2, 0], [1, np.sqrt(3)]])
        >>> edges = [(0, 1), (1, 2), (2, 0)]
        >>> config = Configuration(coords=coords, edges=edges, name="D3-1")
        >>> print(config.n)
        3
        >>> print(config.degree(0))
        2
    
    Notes:
        - Las aristas se normalizan automáticamente para que i < j.
        - Los duplicados en edges se eliminan automáticamente.
        - La validación completa del grafo se realiza en `analysis.analyze_configuration`.
    """
    coords: np.ndarray
    edges: List[Edge]
    name: Optional[str] = None
    hull_vertices: Optional[List[int]] = None
    perimeter_edges: Optional[List[Tuple[int, int, float]]] = None

    def __post_init__(self) -> None:
        """
        Valida y normaliza la configuración después de la inicialización.
        
        NO calcula perimeter_edges automáticamente para evitar recálculos
        durante perturbaciones numéricas.
        
        Realiza:
        1. Conversión de coords a numpy array (n, 2)
        2. Validación de forma de coords
        3. Normalización de aristas (i < j)
        4. Eliminación de bucles y duplicados
        5. Validación de índices
        
        Raises:
            ValueError: Si coords no tiene forma (n, 2).
            ValueError: Si hay bucles (i == j) en edges.
            ValueError: Si los índices están fuera de rango.
        """
        coords = np.asarray(self.coords, dtype=np.float64)  # Usar float64 explícitamente
        if coords.ndim != 2 or coords.shape[1] != 2:
            raise ValueError("coords debe ser un array de forma (n,2)")
        self.coords = coords
        self.n = coords.shape[0]

        # Normalizar aristas para que (i,j) tenga i<j
        normalized_edges: List[Edge] = []
        for (i, j) in self.edges:
            if i == j:
                raise ValueError("No se permiten bucles (i == j) en edges")
            if i < 0 or j < 0 or i >= self.n or j >= self.n:
                raise ValueError(f"Índice de vértice fuera de rango en arista {(i, j)}")
            if i > j:
                i, j = j, i
            if (i, j) not in normalized_edges:
                normalized_edges.append((i, j))
        self.edges = normalized_edges

    def adjacent(self, i: int) -> List[int]:
        """
        Devuelve lista de vecinos del disco i en el grafo de contacto.
        
        Args:
            i: Índice del disco (0 ≤ i < n).
        
        Returns:
            Lista de índices de discos adyacentes a i.
        
        Examples:
            >>> config = Configuration(
            ...     coords=np.array([[0,0], [2,0], [1,np.sqrt(3)]]),
            ...     edges=[(0,1), (1,2), (2,0)]
            ... )
            >>> config.adjacent(1)
            [0, 2]
        """
        neigh = []
        for (u, v) in self.edges:
            if u == i:
                neigh.append(v)
            elif v == i:
                neigh.append(u)
        return neigh

    def degree(self, i: int) -> int:
        """
        Devuelve el grado del vértice i en el grafo de contacto.
        
        El grado es el número de discos tangentes al disco i.
        
        Args:
            i: Índice del disco.
        
        Returns:
            Grado del vértice i.
        
        Examples:
            >>> config = Configuration(
            ...     coords=np.array([[0,0], [2,0], [4,0]]),
            ...     edges=[(0,1), (1,2)]
            ... )
            >>> config.degree(0)
            1
            >>> config.degree(1)
            2
        
        Notes:
            Para configuraciones físicamente realizables de discos unitarios,
            el grado máximo es típicamente ≤ 6 (empaquetamiento óptimo).
        """
        return len(self.adjacent(i))