# Extremal Packings - Análisis de Discos Tangentes

Paquete Python para análisis geométrico y espectral de configuraciones de discos unitarios tangentes en el plano.

## Características

- Catálogo de configuraciones predefinidas de 3 a 6 discos
- Calculo de Matriz de contacto, rolling space, gradiente proyectado, Hessiano intrínseco
- Visualización en plots
- API y utilidad CLI

## Instalación

### Desde PyPI
```bash
pip install extremal-packings
```

### Desde el repositorio
```bash
git clone https://github.com/fhenr/disk-packing-analysis.git
cd disk-packing-analysis
pip install -e .
```

## Uso Rápido

### Desde Python

```python
from extremal_packings import load_configuration, analyze_configuration

# Cargar configuración del catálogo
config = load_configuration("D5-7")  # Pentágono regular

# Análisis completo
result = analyze_configuration(config)

# Ver resultados
print(f"Rolling space dimension: {result.R.shape[1]}")
print(f"Eigenvalues: {result.eigenvalues}")
print(f"Perimeter: {result.perimeter_disks:.4f}")
```

### Desde CLI (Línea de Comandos)

```bash
# Listar configuraciones disponibles
epack list

# Analizar una configuración específica
epack analyze D5-7

# Comparar configuraciones de 5 discos
epack compare -s 5

# Ver información detallada
epack info D5-7

# Visualizar con gráficos
epack plot D5-7
```
## Docs

- **[Docs](docs/index.md)** - Guía completa de uso. Incluye fundamentos matemáticos.
- **[CLI](docs/cli.md)** - Guía de la interfaz de línea de comandos.
- **[Ejemplos Básicos](examples/basic_usage.py)**
- **[Ejemplos Avanzados](examples/advanced_usage.py)**

Ver [`examples/basic_usage.py`](examples/basic_usage.py) para casos de uso completos:

## Estructura del Proyecto

```
extremal_packings/        
├── __init__.py            # API pública
├── analysis.py            # Pipeline de análisis
├── catalog.py             # Catálogo de configuraciones
├── cli.py                 # Interfaz de línea de comandos
├── configurations.py      # Clase Configuration
├── constraints.py         # Matriz A y rolling space
├── contact_graphs.py      # Validación de grafos
├── hessian.py             # Hessiano K y H
├── interface.py           # Funciones de alto nivel
├── json_loader.py         # Carga desde JSON
├── perimeter.py           # Perímetros y convex hull
└── plotting.py            # Visualización
```

## Testing

```bash
pytest tests/
```

## Licencia

MIT License. [LICENSE](LICENSE).

## Autores

- **Fabián Andrés Henry Vilaxa**
- **Jose Ayala Hoffman**