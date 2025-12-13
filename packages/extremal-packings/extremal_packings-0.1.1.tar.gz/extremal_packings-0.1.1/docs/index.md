# Extremal Packings - Análisis de Empaquetamientos de Discos Congruentes

**Versión:** 1.0.1 
**Autor:** Fabián Andrés Henry Vilaxa, Jose Ayala Hoffman  
**Licencia:** MIT

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Fundamentos Matemáticos](#fundamentos-matemáticos)
3. [Arquitectura del Paquete](#arquitectura-del-paquete)
4. [Módulos Detallados](#módulos-detallados)
5. [Interfaz de Línea de Comandos](#interfaz-de-línea-de-comandos)
6. [Catálogo de Configuraciones](#catálogo-de-configuraciones)
7. [Ejemplos Avanzados](#ejemplos-avanzados)
8. [Guía de Desarrollo](#guía-de-desarrollo)
9. [Referencias](#referencias)

---

## Introducción

### Motivación

El paquete `extremal_packings` surge de la investigación sobre perímetros extremos en empaquetamientos de discos congruentes. El objetivo es estudiar configuraciones de discos unitarios tangentes que minimizan o maximizan el perímetro de su envolvente convexa.

### Alcance

El paquete proporciona:

- **Análisis geométrico**: Envolventes convexas, perímetros, grafos de contacto
- **Análisis variacional**: Rolling space, Análisis de criticidad, Análisis de estabilidad.
- **Catálogo**: Configuraciones predefinidas de 3 a 6 discos
- **Visualización**: Gráficos estáticos con Matplotlib

### Instalación

```bash
# Desde PyPI
pip install extremal-packings

# Desde el repositorio
git clone https://github.com/fhenr/disk-packing-analysis.git
cd disk-packing-analysis
pip install -e .
```

### Dependencias

- **Python**: ≥3.8
- **NumPy**: ≥1.20.0 (álgebra lineal)
- **SciPy**: ≥1.7.0 (convex hull, SVD)
- **Matplotlib**: ≥3.3.0 (visualización)
- **NetworkX**: ≥2.5 (grafos de contacto)

---

## Fundamentos Matemáticos

### 1. Configuración de Discos

**Definición**: Una configuración $\mathcal{C}$ consiste en:

- $n$ discos unitarios (radio $r = 1$)
- Centros $c_1, \ldots, c_n \in \mathbb{R}^2$
- Grafo de contacto $G = (V, E)$ donde $(i,j) \in E \iff \|c_j - c_i\| = 2$

**Espacio de configuraciones**: $\mathcal{D} = \mathbb{R}^{2n}$ (coordenadas apiladas: $[c_1^x, c_1^y, \ldots, c_n^x, c_n^y]$)

### 2. Matriz de Contacto $A(c)$

Para cada contacto $(i,j) \in E$, definimos el vector unitario:

$$u_{ij} = \frac{c_j - c_i}{\|c_j - c_i\|} = \frac{c_j - c_i}{2}$$

La matriz de contacto $A(c) \in \mathbb{R}^{m \times 2n}$ tiene una fila por contacto:

$$\text{row}_k = [\ldots, 0, -u_{ij}, 0, \ldots, 0, u_{ij}, 0, \ldots]$$

con $-u_{ij}$ en las posiciones $(2i, 2i+1)$ y $u_{ij}$ en $(2j, 2j+1)$.

**Propiedad**: $A(c) \cdot \delta{c} = 0 \iff$ la deformación $\delta{c}$ preserva todos los contactos infinitesimalmente.

### 3. Rolling Space

El **rolling space** es el kernel de $A(c)$:

$$\text{Roll}(c) = \ker(A(c)) = \{\delta{c} \in \mathbb{R}^{2n} : A(c) \cdot \delta{c} = 0\}$$

**Dimensión**:

$$\dim(\text{Roll}(c)) = 2n - \text{rank}(A(c))$$

**Interpretación física**:
- Deformaciones infinitesimales que mantienen las distancias de contacto constantes.
- Incluye movimientos rígidos: 2 traslaciones + 1 rotación = 3 grados.
- Si $\dim(\text{Roll}) = 3$, la configuración es infinitesimalmente rígida.
- Si $\dim(\text{Roll}) > 3$, hay flexibilidad (deformaciones no triviales).

### 4. Funcional de Perímetro

El perímetro del cluster de discos es:

$$P(c) = \text{perímetro del casco convexo de } \bigcup_{i=1}^n \{x : \|x - c_i\| \leq 1\}$$

**Simplificación**: Para configuraciones con discos en la frontera bien definida, se puede calcular mediante:

1. Casco convexo de centros: $\text{CH}(c_1, \ldots, c_n)$
2. Agregar arcos circulares en los vértices del casco

### 5. Hessiano del Perímetro

#### 5.1 Hessiano Intrínseco $H$

El Hessiano intrínseco se calcula mediante diferenciación numérica del campo vectorial proyectado:

$$V(c) = P(c) \nabla f(c)$$

donde $P(c) = R(R^T R)^{-1}R^T$ es el proyector ortogonal sobre $\text{Roll}(c)$.

**Proyección al rolling space:**

Una vez calculado $H_{int}$ en el espacio ambiente $\mathbb{R}^{2n}$:

$$H = R^T H_{int} R$$

donde $R \in \mathbb{R}^{2n \times d}$ es una base ortonormal de $\text{Roll}(c)$ con $d = \dim(\text{Roll})$.

**Interpretación**:
- $\lambda_i > 0$: Curvatura positiva en dirección $i$ (mínimo local estable)
- $\lambda_i = 0$: Dirección neutra (degeneración)
- $\lambda_i < 0$: Curvatura negativa (punto de silla o máximo local)

### 6. Condiciones de Optimalidad

Para que $c$ sea un punto crítico del perímetro en su estrato $\mathcal{C}(G)$:

$$\langle \nabla \text{Per}(c), \; \delta{c} \rangle = 0 \quad \forall \; \delta{c} \in \text{Roll(c)}.$$

---

## Arquitectura del Paquete

### Estructura de Directorios

```
disk-packing-analysis/
├── extremal_packings/          # Código fuente principal
│   ├── __init__.py            # API pública
│   ├── analysis.py            # Pipeline de análisis
│   ├── catalog.py             # Catálogo de configuraciones
│   ├── cli.py                 # Interfaz de línea de comandos
│   ├── configurations.py      # Clase Configuration
│   ├── constraints.py         # Matriz A y rolling space
│   ├── contact_graphs.py      # Validación de grafos
│   ├── hessian.py            # Hessiano K y H
│   ├── interface.py          # Funciones de alto nivel
│   ├── json_loader.py        # Carga desde JSON
│   ├── perimeter.py          # Perímetros y convex hull
│   └── plotting.py           # Visualización
├── data/                      # Configuraciones JSON
│   ├── 3disks.json
│   ├── 4disks.json
│   ├── 5disks.json
│   └── 6disks.json
├── tests/                     # Suite de tests
│   ├── test_analysis.py
│   ├── test_catalog.py
│   ├── test_cli.py
│   ├── test_configurations.py
│   ├── test_constraints.py
│   ├── test_contact_graphs.py
│   ├── test_hessian.py
│   └── test_perimeter.py
├── examples/                  # Ejemplos de uso
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                      # Documentación
│   ├── index.md
│   ├── cli.md
│   ├── api.md
│   └── DETAILED_DOCUMENTATION.md
├── pyproject.toml            # Configuración del proyecto
├── setup.py                  # Setup alternativo
├── README.md                 # Readme principal
└── LICENSE                   # Licencia MIT
```

### Flujo de Datos

```
Configuration (coords, edges)
    ↓
[Validación]
    ↓
A(c) ← build_contact_matrix
    ↓
R ← rolling_space_basis(A)
    ↓
H(c) ← compute_intrinsic_hessian
    ↓
λ₁, ..., λ_d ← intrinsic_spectrum(H)
    ↓
AnalysisResult
```

---

## Módulos Detallados

### 1. `configurations.py`

Define la clase base `Configuration`.

#### Clase `Configuration`

```python
@dataclass
class Configuration:
    coords: np.ndarray          # (n, 2) coordenadas de centros
    edges: list[tuple[int, int]] # Lista de contactos
    name: str = ""              # Nombre identificador
    radius: float = 1.0         # Radio (siempre 1.0)
```

**Métodos**:

- `n` (property): Número de discos
- `__post_init__()`: Validación de datos de entrada

**Ejemplo**:

```python
coords = np.array([[0, 0], [2, 0], [1, np.sqrt(3)]])
edges = [(0, 1), (1, 2), (2, 0)]
config = Configuration(coords=coords, edges=edges, name="Triangle")
```

---

### 2. `contact_graphs.py`

Validación de grafos de contacto.

#### Función `check_graph_validity`

```python
def check_graph_validity(n: int, edges: list[tuple[int, int]]) -> None:
    """Valida que el grafo de contacto sea físicamente realizable."""
```

**Validaciones**:

1. **Conectividad**: El grafo debe ser conexo (componente única)
2. **Grados**: Ningún vértice puede tener grado > 6 (*kissing number* en $\mathbb{R}^2$)
3. **Índices**: Todos los índices deben estar en [0, n-1]

**Excepciones**:
- `ValueError` si el grafo no cumple alguna condición

**Ejemplo**:

```python
check_graph_validity(4, [(0,1), (1,2), (2,3), (3,0)])  # OK
check_graph_validity(4, [(0,1), (2,3)])  # ValueError: desconectado
```

---

### 3. `constraints.py`

Construcción de la matriz de contacto y rolling space.

#### Función `build_contact_matrix`

```python
def build_contact_matrix(config: Configuration) -> np.ndarray:
    """Construye matriz A(c) de dimensión (m, 2n)."""
```

**Algoritmo**:

```python
Para cada contacto (i, j):
    1. u_ij = (c_j - c_i) / ||c_j - c_i||
    2. fila_k = [0, ..., -u_ij[0], -u_ij[1], ..., u_ij[0], u_ij[1], ..., 0]
```

**Salida**: Matriz $A \in \mathbb{R}^{m \times 2n}$ con filas ortonormales (si contactos son ortogonales).

#### Función `rolling_space_basis`

```python
def rolling_space_basis(A: np.ndarray) -> np.ndarray:
    """Calcula base ortonormal del ker(A) mediante SVD."""
```

**Algoritmo (SVD)**:

1. Descomposición: $A = U \Sigma V^T$
2. Valores singulares: $\sigma_1 \geq \cdots \geq \sigma_r > 0$ (rank = r)
3. Rolling space: Columnas de $V$ correspondientes a $\sigma_i < \text{tol}$
4. Dimensión: $d = 2n - r$

**Tolerancia**: $\text{tol} = 10^{-10}$ (valores singulares menores se consideran 0)

**Ejemplo**:

```python
A = build_contact_matrix(config)
R = rolling_space_basis(A)  # R: (2n, d)
print(f"Dimension rolling space: {R.shape[1]}")
```

---

### 4. `hessian.py`

Cálculo del Hessiano Intrínseco mediante diferenciación numérica.

#### Función `compute_intrinsic_hessian`

```python
def compute_intrinsic_hessian(
    config: Configuration, 
    R: np.ndarray,
    epsilon: float = None
) -> np.ndarray:
    """
    Calcula el Hessiano intrínseco mediante diferenciación numérica.
    
    Implementa: H_int = D(V) donde V(c) = P(c) @ ∇f(c)
    
    Por defecto usa epsilon = √(machine_eps) * 10 ≈ 1.5e-7
    """
```

**Algoritmo (Diferenciación Numérica)**:

1. Para cada dirección $k = 1, \ldots, 2n$:
   - Perturbar: $c_+ = c + \epsilon e_k$, $c_- = c - \epsilon e_k$
   - Calcular proyectores: $P_+ = P(c_+)$, $P_- = P(c_-)$
   - Calcular gradientes: $g_+ = \nabla f(c_+)$, $g_- = \nabla f(c_-)$
   - Campo vectorial: $V_+ = P_+ g_+$, $V_- = P_- g_-$
   - Derivada: $H_{:,k} = (V_+ - V_-) / (2\epsilon)$

2. Simetrizar: $H = (H + H^T) / 2$

**Salida**: Matriz $H_{int} \in \mathbb{R}^{2n \times 2n}$

#### Función `project_to_roll`

```python
def project_to_roll(H_ambient: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Proyecta el Hessiano del espacio ambiente al rolling space: H = R^T H_ambient R."""
```

**Operación**: Multiplicación matricial $H = R^T H_{ambient} R$

**Dimensiones**:
- Entrada: $H_{ambient} \in \mathbb{R}^{2n \times 2n}$, $R \in \mathbb{R}^{2n \times d}$
- Salida: $H \in \mathbb{R}^{d \times d}$

#### Función `intrinsic_spectrum`

```python
def intrinsic_spectrum(H: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    """Calcula autovalores de H usando np.linalg.eigvalsh (matrices simétricas)."""
```

**Método**: `numpy.linalg.eigvalsh` (optimizado para matrices simétricas)

**Tolerancia**: $\text{tol} = 10^{-12}$ para clasificación de autovalores

**Salida**: Array 1D con autovalores $\lambda_1 \leq \cdots \leq \lambda_d$

---

### 5. `perimeter.py`

Cálculo de perímetros y envolventes convexas.

#### Función `is_collinear_chain`

```python
def is_collinear_chain(config: Configuration, hull: List[int]) -> bool:
    """
    Verifica si el hull forma una cadena colineal.
    
    Una cadena colineal es un conjunto de puntos en línea recta donde
    todos los centros están alineados y el hull solo incluye los extremos.
    """
```

**Criterio**: Producto cruz de los tres primeros puntos del hull < $10^{-6}$

**Uso**: Para decidir si aplicar la fórmula especial de perímetro: $\text{Per} = 2 \times \text{dist}(extremos) + 2\pi r$

#### Función `find_chain_endpoints`

```python
def find_chain_endpoints(config: Configuration, hull: List[int]) -> tuple[int, int]:
    """
    Encuentra los extremos de una cadena colineal.
    
    Para una cadena colineal, los extremos son los dos puntos del hull
    más distantes entre sí.
    """
```

**Algoritmo**: Buscar los dos puntos en el hull con distancia máxima

**Retorno**: Tupla `(índice_inicio, índice_fin)`

#### Función `compute_disk_hull_geometry`

```python
def compute_disk_hull_geometry(config: Configuration, radius: float = 1.0) -> Optional[Dict]:
    """
    Calcula la geometría completa del hull de discos (tangentes externas + arcos).
    
    Returns:
        Diccionario con:
        - 'tangent_segments': Lista de segmentos tangentes {start, end}
        - 'arcs': Lista de arcos {center, radius, angle_start, angle_end}
    """
```

**Algoritmo**:

1. Calcular segmentos tangentes externos entre discos consecutivos del hull
2. Calcular arcos circulares para cada disco del hull
3. Manejar casos especiales (cadenas colineales con semicírculos en extremos)

**Salida**: Diccionario con geometría completa para visualización

---

## Ejemplos Avanzados

### Ejemplo 1: Análisis Comparativo

```python
from extremal_packings import *

configs = ["D5-1", "D5-7", "D5-11"]

print(f"{'Config':<10} {'Roll dim':<10} {'Perímetro':<12} {'Mín λ':<12}")
print("-" * 50)

for name in configs:
    config = load_configuration(name)
    result = analyze_configuration(config)
    
    print(f"{name:<10} {result.rolling_dim:<10} "
          f"{result.perimeter_disks:<12.4f} "
          f"{result.eigenvalues[0]:<12.4e}")
```

### Ejemplo 2: Acceso a Componentes del Pipeline

```python
import numpy as np
from extremal_packings import load_configuration, analyze_configuration
from extremal_packings.constraints import build_contact_matrix, rolling_space_basis
from extremal_packings.hessian import compute_intrinsic_hessian, project_to_roll

# Cargar configuración
config = load_configuration("D5-7")

# Ejecutar pipeline completo
result = analyze_configuration(config)

# O acceder a componentes individuales
A = build_contact_matrix(config)
R = rolling_space_basis(A)
H_ambient = compute_intrinsic_hessian(config, R)
H = project_to_roll(H_ambient, R)

print(f"A: {A.shape}, R: {R.shape}")
print(f"H_ambient: {H_ambient.shape}, H: {H.shape}")
print(f"Autovalores: {result.eigenvalues}")
```

---

## Guía de Desarrollo

### Estructura de Tests

Tests organizados por módulo:

```
tests/
├── test_configurations.py   # Configuration class
├── test_contact_graphs.py   # Validación de grafos
├── test_constraints.py      # A(c) y rolling space
├── test_hessian.py         # K, H, espectro
├── test_perimeter.py       # Perímetros y convex hull
├── test_catalog.py         # Catálogo y carga
└── test_analysis.py        # Pipeline completo
```

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/

# Con cobertura
pytest --cov=extremal_packings tests/

# Test específico
pytest tests/test_analysis.py::TestAnalyzeConfiguration::test_triangle
```

### Agregar Nueva Configuración

1. **Crear entrada JSON en `data/{n}disks.json`**:

```json
{
    "discos": 5,
    "centros": [[0,0], [2,0], ...],
    "contactos": [[0,1], [1,2], ...]
}
```

2. **Validar con test**:

```python
def test_new_config():
    config = load_configuration("D5-14")
    assert config.n == 5
    assert len(config.edges) > 0
```

3. **Analizar**:

```python
result = analyze_configuration(config)
print_analysis_summary(result)
```

---

## Apéndices

### A. Nomenclatura Matemática

| Símbolo | Significado |
|---------|-------------|
| $n$ | Número de discos |
| $m$ | Número de contactos |
| $c_i$ | Centro del disco $i$ |
| $r$ | Radio (siempre 1) |
| $G = (V, E)$ | Grafo de contacto |
| $A(c)$ | Matriz de contacto ($m \times 2n$) |
| $\text{Roll}(c)$ | Rolling space ($\dim = 2n - \text{rank}(A)$) |
| $R$ | Base ortonormal de $\text{Roll}(c)$ |
| $H(c)$ | Hessiano intrínseco |
| $\lambda_i$ | Autovalor $i$ de $H$ |
| $\text{Per}(c)$ | Perímetro de la envolvente de centros |
| $\mathcal{P}(c)$ | Perímetro del cluster |

### B. Glosario de Términos

**Punto Crítico del Perímetro**: $\langle \nabla \text{Per}(c), \; \delta{c} \rangle = 0$ para todo $\delta{c} \in \text{Roll(c)}$

**Configuración rígida**: $\dim(\text{Roll}) \leq 3$ (solo movimientos rígidos).

**Configuración flexible**: $\dim(\text{Roll}) > 3$ (deformaciones no triviales).

**Mínimo local estable**: $H$ semidefinida positiva ($\lambda_i \geq 0 \, \forall i$).

**Punto de silla**: Existe $\lambda_i < 0$.

**Grafo de contacto**: Grafo $G = (V, E)$ donde $V = \{1, \ldots, n\}$ y $(i,j) \in E \iff \|c_j - c_i\| = 2$.

**Convex hull**: Polígono convexo más pequeño que contiene todos los centros.

**Rolling space**: Espacio tangente de configuraciones con contactos preservados.

---

**Fin del documento** | Versión 1.0.0 | Última actualización: 2025
