# Interfaz de Línea de Comandos (CLI) - epack

**Comando:** `epack`  
**Versión:** 1.0.1  
**Módulo:** `extremal_packings.cli`

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Comandos Disponibles](#comandos-disponibles)
4. [Guía de Uso](#guía-de-uso)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Flujos de Trabajo Típicos](#flujos-de-trabajo-típicos)
7. [Cheatsheet de Comandos](#cheatsheet-de-comandos)


---

## Introducción

La interfaz de línea de comandos `epack` proporciona acceso completo a las funcionalidades del paquete `extremal_packings` sin necesidad de escribir código Python. Es ideal para:

- **Exploración rápida** del catálogo de configuraciones
- **Análisis** de múltiples configuraciones
- **Generación de reportes**
- **Integración** en pipelines
- **Visualización** desde terminal

---

## Instalación y Configuración

### Instalación del CLI

El CLI se instala automáticamente con el paquete:

```bash
pip install extremal-packings
```

O desde el repositorio:

```bash
git clone https://github.com/fhenr/disk-packing-analysis.git
cd disk-packing-analysis
pip install -e .
```

### Verificar Instalación

```bash
epack --version
# Salida: epack, version 1.0.0

epack --help
# Muestra la ayuda general
```

### Dependencias Adicionales

Para visualización con `--plot`:

```bash
pip install matplotlib
```

---

## Comandos Disponibles

### Resumen de Comandos

| Comando | Descripción | Uso Típico |
|---------|-------------|------------|
| `list` | Listar configuraciones disponibles | `epack list` |
| `analyze` | Analizar una configuración específica | `epack analyze D5-7` |
| `compare` | Comparar configuraciones del mismo tamaño | `epack compare -s 5` |
| `info` | Información detallada de una configuración | `epack info D5-7` |
| `plot` | Visualizar configuración con gráficos | `epack plot D5-7` |
| `stats` | Estadísticas del catálogo completo | `epack stats` |

### Ayuda General

```bash
epack --help
```

**Salida:**
```
Usage: epack [OPTIONS] COMMAND [ARGS]...

  epack - Extremal Packings CLI
  
  Herramienta de línea de comandos para analizar configuraciones de discos
  tangentes, calcular rolling spaces, Hessianos intrínsecos y perímetros.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  analyze  Analiza una configuración específica.
  compare  Compara todas las configuraciones de un tamaño específico.
  info     Muestra información detallada de una configuración.
  list     Lista todas las configuraciones disponibles.
  plot     Visualiza una configuración con gráficos interactivos.
  stats    Muestra estadísticas generales del catálogo.
```

---

## Guía de Uso

### 1. `list` - Listar Configuraciones

**Propósito:** Explorar el catálogo de configuraciones disponibles.

**Sintaxis:**
```bash
epack list [OPTIONS]
```

**Opciones:**

| Opción | Tipo | Descripción |
|--------|------|-------------|
| `-s, --size INTEGER` | Entero | Filtrar por número de discos |
| `-v, --verbose` | Flag | Mostrar información detallada |

**Ejemplos:**

```bash
# Listar todas las configuraciones (formato compacto)
epack list

# Listar solo configuraciones de 5 discos
epack list -s 5

# Listar con detalles (n discos, m contactos)
epack list -v

# Combinar filtro y detalles
epack list -s 6 -v
```

**Salida Ejemplo (no verbose):**
```
📋 Total de configuraciones: 66

  D3-1        D3-2        D4-1        D4-2        D4-3        D4-4      
  D4-5        D5-1        D5-2        D5-3        D5-4        D5-5      
  D5-6        D5-7        D5-8        D5-9        D5-10       D5-11     
  ...
```

**Salida Ejemplo (verbose):**
```
📋 Configuraciones de 5 discos: 13

  • D5-1: 5 discos, 4 contactos
  • D5-2: 5 discos, 4 contactos
  • D5-3: 5 discos, 5 contactos
  • D5-7: 5 discos, 5 contactos
  ...
```

---

### 2. `info` - Información de una Configuración

**Propósito:** Ver detalles geométricos de una configuración sin realizar análisis variacional.

**Sintaxis:**
```bash
epack info CONFIG_NAME
```

**Argumentos:**

- `CONFIG_NAME`: Nombre de la configuración (ej: `D5-7`)

**Ejemplo:**

```bash
epack info D5-7
```

**Salida:**
```
📋 Información de D5-7
============================================================
Nombre:          D5-7
Discos (n):      5
Contactos (m):   5

Coordenadas de centros:
  Disco 0: (  0.0000,   1.7013)
  Disco 1: ( -1.6180,   0.5257)
  Disco 2: ( -1.0000,  -1.3764)
  Disco 3: (  1.0000,  -1.3764)
  Disco 4: (  1.6180,   0.5257)

Grafo de contacto:
  Contacto 0: (0, 1)
  Contacto 1: (0, 4)
  Contacto 2: (1, 2)
  Contacto 3: (2, 3)
  Contacto 4: (3, 4)

Grados de los vértices:
  Disco 0: grado 2
  Disco 1: grado 2
  Disco 2: grado 2
  Disco 3: grado 2
  Disco 4: grado 2
============================================================
```
---

### 3. `analyze` - Análisis Completo

**Propósito:** Realizar análisis variacional completo incluyendo rolling space, Hessiano y espectro.

**Sintaxis:**
```bash
epack analyze CONFIG_NAME [OPTIONS]
```

**Opciones:**

| Opción | Tipo | Descripción |
|--------|------|-------------|
| `-o, --output PATH` | Archivo | Guardar resultados en JSON |
| `-p, --plot` | Flag | Mostrar gráficos interactivos |
| `-v, --verbose` | Flag | Mostrar dimensiones de matrices |

**Ejemplos:**

```bash
# Análisis básico
epack analyze D5-7

# Análisis con gráficos
epack analyze D5-7 --plot

# Análisis con detalles y exportación
epack analyze D5-7 -v -o results_D5-7.json

# Todo junto
epack analyze D5-7 -p -v -o results.json
```

**Salida Ejemplo:**
```
🔍 Analizando D5-7...

============================================================
Configuración: D5-7
============================================================
Número de discos (n):     5
Número de contactos (m):   5
Tipo:                     Cluster 2D

Rolling Space:
  Dimensión:              5
  Rigidez:                Flexible

Perímetros:
  Centros:                10.000000
  Discos (+ 2πr):         16.283185

Gradiente del perímetro:
  ∇Per(c) = [0.0, 1.18, -1.12, 0.36, -0.7, -0.95, 0.69, -0.95, 1.12, 0.36]

Proyección del gradiente:
  Proj(∇Per) = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Espectro del Hessiano Intrínseco:
  Autovalores (5):
    λ_0:  0.000000e+00
    λ_1:  0.000000e+00
    λ_2:  6.909830e-01
    λ_3:  1.000000e+00
    λ_4:  1.000000e+00

============================================================

💾 Resultados guardados en: results_D5-7.json
```

**Con Verbose (-v):**
```
Dimensiones de matrices:
  A (contacto):           (5, 10)
  R (rolling space):      (10, 5)
  K (Hessiano global):    (10, 10)
  H (Hessiano intrínseco): (5, 5)
```

**Formato JSON del Output:**
```json
{
  "name": "D5-7",
  "n_disks": 5,
  "n_edges": 5,
  "rolling_dim": 5,
  "is_rigid": false,
  "perimeter_centers": 10.0,
  "perimeter_disks": 16.283185307179586,
  "gradient_perimeter": [0.0, 1.175570504, -1.118033988, ...],
  "projected_gradient": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
  "is_critical": true,
  "eigenvalues": [0.0, 0.0, 0.6909830056, 0.9999999999, 1.0],
  "coords": [ 
    [0.0, 1.7013016167040798], 
    [-1.6180339887498947, 0.5257311121191335],
    [-1.0, -1.3763819204711736],
    [1.0, -1.3763819204711736],
    [1.6180339887498947, 0.5257311121191335]
  ],
  "edges": [[0,1],[0,4],[1,2],[2,3],[3,4]]
}
```

---

### 4. `compare` - Comparación de Configuraciones

**Propósito:** Analizar todas las configuraciones de un tamaño específico y compararlas en una tabla.

**Sintaxis:**
```bash
epack compare -s SIZE [OPTIONS]
```

**Opciones:**

| Opción | Tipo | Descripción |
|--------|------|-------------|
| `-s, --size INTEGER` | Entero (requerido) | Número de discos |
| `-m, --metric CHOICE` | `perimeter`, `eigenvalue`, `rolling_dim` | Métrica para ordenar |
| `-o, --output PATH` | Archivo CSV | Exportar tabla comparativa |

**Ejemplos:**

```bash
# Comparar todas las de 5 discos (ordenadas por perímetro)
epack compare -s 5

# Ordenar por autovalor mínimo
epack compare -s 5 -m eigenvalue

# Ordenar por dimensión del rolling space
epack compare -s 5 -m rolling_dim

# Exportar a CSV
epack compare -s 5 -o comparison_5disks.csv
```

**Salida Ejemplo:**
```
🔬 Comparando 13 configuraciones de 5 discos...

Analizando [####################################] 100%

Config     Edges   Roll    Perímetro    Crítica    λ_min        λ_max        Rígida  
================================================================================
D5-12      7       3       16.283185    Si         0.0000e+00   1.0294e+00   Sí
D5-8       6       4       17.211389    Si         0.0000e+00   1.3653e+00   No
D5-9       6       4       18.010592    Si         0.0000e+00   1.5625e+00   No
D5-10      6       4       16.283185    Si         0.0000e+00   1.4625e+00   No  
...

================================================================================
Mínimo perímetro: D5-12 = 16.283185
Máximo perímetro: D5-13 = 22.283185
Configuraciones rígidas: 1/13
================================================================================
```

**Nota sobre la columna "Crítica":**

Una configuración es **crítica a primer orden** si el gradiente proyectado sobre el rolling space es el vector nulo: $\text{Proj}(\nabla \text{Per}) = 0$.

Esto significa que no hay deformaciones infinitesimales (dentro del rolling space) que reduzcan el perímetro. Para ser un **mínimo local**, además se requiere que todos los autovalores no nulos del Hessiano intrínseco sean positivos.

**Formato CSV del Output:**
```csv
name,n_edges,rolling_dim,perimeter_centers,perimeter_disks,gradient_perimeter,projected_gradient,is_critical,min_eigenvalue,max_eigenvalue,is_rigid
D5-7,5,5,10.0,16.283185,"[0.0, 1.175, -1.118, ...]","[0.0, 0.0, ...]",Si,0.0,1.0,False
D5-10,6,4,10.0,16.283185,"[-1.0, -1.0, ...]","[0.0, 0.0, ...]",Si,0.0,1.462,False
```

---

### 5. `plot` - Visualización

**Propósito:** Generar gráficos interactivos de una configuración.

**Sintaxis:**
```bash
epack plot CONFIG_NAME [OPTIONS]
```

**Opciones:**

| Opción | Tipo | Descripción |
|--------|------|-------------|
| `--hull/--no-hull` | Flag | Mostrar/ocultar envolvente convexa (default: mostrar) |
| `--normals/--no-normals` | Flag | Mostrar/ocultar vectores normales (default: ocultar) |

**Ejemplos:**

```bash
# Gráficos estándar (discos + grafo)
epack plot D5-7

# Sin envolvente convexa
epack plot D5-7 --no-hull

# Con vectores normales en el grafo
epack plot D5-7 --normals

# Combinar opciones
epack plot D5-7 --no-hull --normals
```

**Elementos Visualizados:**

**Panel Izquierdo (Discos):**
- Círculos blancos con borde negro (discos)
- Puntos rojos (centros)
- Líneas punteadas grises (contactos)
- Polígono azul semitransparente (envolvente convexa, opcional)

**Panel Derecho (Grafo de Contacto):**
- Nodos en posiciones de centros
- Aristas entre contactos
- Vectores normales $u_{ij}$ (opcional)

**Interactividad:**
- Zoom: Scroll del mouse
- Pan: Arrastrar con botón derecho
- Guardar: Botón de guardar en la barra de herramientas

---

### 6. `stats` - Estadísticas del Catálogo

**Propósito:** Ver estadísticas globales del catálogo.

**Sintaxis:**
```bash
epack stats
```

**Salida Ejemplo:**
```
📊 Estadísticas del Catálogo
============================================================
Total de configuraciones: 65
Rango de tamaños: 3 a 6 discos

Distribución por tamaño:
  3 discos:   2 ██
  4 discos:   5 █████
  5 discos:  13 █████████████
  6 discos:  45 ████████████████████████████████████████████
============================================================
``` 
---

## Ejemplos Prácticos

### Ejemplo 1: Exploración Rápida

```bash
# Paso 1: Ver qué hay disponible
epack stats

# Paso 2: Listar configuraciones de 5 discos
epack list -s 5

# Paso 3: Ver detalles de una específica
epack info D5-7

# Paso 4: Visualizar
epack plot D5-7
```

### Ejemplo 2: Análisis Completo con Exportación

```bash
# Analizar y guardar resultados
epack analyze D5-7 -v -o results/D5-7.json

# Generar gráficos
epack plot D5-7

# Ver resultados
cat results/D5-7.json | jq '.perimeter_disks'
```

### Ejemplo 3: Comparación Sistemática

```bash
# Comparar todas las de 5 discos y exportar
epack compare -s 5 -o results/comparison_5disks.csv

# Encontrar la de mínimo perímetro
epack compare -s 5 -m perimeter | head -n 5

# Encontrar configuraciones estables (λ_min ≥ 0)
epack compare -s 5 -m eigenvalue | grep -v "^D.*-[0-9].*-"
```

### Ejemplo 4: Pipeline Automatizado

Script bash para analizar todas las configuraciones:

```bash
#!/bin/bash
# analyze_all.sh

mkdir -p results

# Analizar cada tamaño
for size in 3 4 5 6; do
    echo "Procesando $size discos..."
    epack compare -s $size -o results/comparison_${size}disks.csv
done

# Generar reporte
cat results/comparison_*.csv > results/full_report.csv

echo "✓ Análisis completo en results/"
```

### Ejemplo 5: Búsqueda de Configuraciones Óptimas

```bash
# Encontrar configuraciones rígidas y estables de 5 discos
epack compare -s 5 | awk '$3 == 3 && $6 >= 0 {print $1}'

# Resultado esperado: D5-2, D5-7, D5-11, ...
```

---

## Flujos de Trabajo Típicos

### Workflow 1: Investigación Exploratoria

1. **Explorar catálogo**: `epack stats`, `epack list`
2. **Filtrar por tamaño**: `epack list -s 5`
3. **Ver detalles**: `epack info D5-7`
4. **Visualizar**: `epack plot D5-7`
5. **Analizar**: `epack analyze D5-7 -v`

### Workflow 2: Análisis Comparativo

1. **Comparar grupo**: `epack compare -s 5 -m perimeter`
2. **Identificar extremos**: Mínimo y máximo perímetro
3. **Analizar individualmente**: `epack analyze D5-1 -p`
4. **Exportar resultados**: `-o comparison.csv`
5. **Generar reporte**: Importar CSV en LaTeX/Excel

### Workflow 3: Validación de Hipótesis

**Hipótesis:** "Configuraciones rígidas tienen perímetros mayores"

```bash
# 1. Obtener datos
epack compare -s 5 -o data.csv

# 2. Filtrar rígidas (Roll=3)
awk -F',' '$3 == 3 {print $5}' data.csv > rigid_perimeters.txt

# 3. Filtrar flexibles (Roll>3)
awk -F',' '$3 > 3 {print $5}' data.csv > flexible_perimeters.txt

# 4. Comparar promedios con Python/R
python -c "import numpy as np; print(np.mean(np.loadtxt('rigid_perimeters.txt')))"
```
---

## Cheatsheet de Comandos

```bash
# Exploración
epack stats                          # Estadísticas globales
epack list                           # Todas las configuraciones
epack list -s 5                      # Solo 5 discos
epack info D5-7                      # Detalles de D5-7

# Análisis
epack analyze D5-7                   # Análisis básico
epack analyze D5-7 -p                # Con gráficos
epack analyze D5-7 -v -o out.json    # Detallado + export

# Comparación
epack compare -s 5                   # Comparar 5 discos
epack compare -s 5 -m eigenvalue     # Ordenar por λ_min
epack compare -s 5 -o table.csv      # Exportar tabla

# Visualización
epack plot D5-7                      # Gráficos estándar
epack plot D5-7 --normals            # Con vectores normales
```
---

## Apéndice: Códigos de Salida

| Código | Significado |
|--------|-------------|
| 0 | Éxito |
| 1 | Error general (configuración no encontrada, etc.) |
| 2 | Error de validación (grafo inválido) |

---

**Fin de la documentación CLI** | Versión 1.0.1 | Última actualización: 2025-12-06
