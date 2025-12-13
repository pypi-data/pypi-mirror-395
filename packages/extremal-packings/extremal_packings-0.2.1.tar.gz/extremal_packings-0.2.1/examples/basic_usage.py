"""
Ejemplos básicos de uso del paquete extremal_packings.

Este script muestra los casos de uso más comunes:
1. Cargar configuraciones del catálogo
2. Crear configuraciones personalizadas
3. Análisis completo
4. Visualización
5. Análisis comparativo
"""

import numpy as np
from extremal_packings import (
    # Configuraciones
    Configuration,
    load_configuration,
    list_configurations,
    get_configurations_by_size,
    # Análisis
    analyze_configuration,
    print_analysis_summary,
    # Visualización
    plot_disks,
    plot_contact_graph,
    plot_spectrum,
)


def example_1_load_from_catalog():
    """Ejemplo 1: Cargar configuración del catálogo."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Cargar del catálogo")
    print("="*60)
    
    # Listar configuraciones disponibles
    all_configs = list_configurations()
    print(f"Total de configuraciones: {len(all_configs)}")
    print(f"Primeras 10: {all_configs[:10]}")
    
    # Cargar configuración específica
    config = load_configuration("D5-7")  # Pentágono regular
    print(f"\nConfiguración: {config.name}")
    print(f"Número de discos: {config.n}")
    print(f"Número de contactos: {len(config.edges)}")


def example_2_custom_configuration():
    """Ejemplo 2: Crear configuración personalizada."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Configuración personalizada")
    print("="*60)
    
    # Triángulo equilátero
    coords = np.array([
        [0.0, 0.0],
        [2.0, 0.0],
        [1.0, np.sqrt(3.0)]
    ])
    edges = [(0, 1), (1, 2), (2, 0)]
    
    config = Configuration(
        coords=coords,
        edges=edges,
        name="Triángulo-Equilátero"
    )
    
    print(f"Configuración: {config.name}")
    print(f"Coordenadas:\n{config.coords}")
    print(f"Aristas: {config.edges}")


def example_3_full_analysis():
    """Ejemplo 3: Análisis completo."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Análisis completo")
    print("="*60)
    
    # Cargar configuración
    config = load_configuration("D5-7")
    
    # Análisis
    result = analyze_configuration(config)
    
    # Mostrar resumen
    print_analysis_summary(result)
    
    # Detalles adicionales
    print("Autovalores del Hessiano intrínseco:")
    for i, lam in enumerate(result.eigenvalues):
        print(f"  λ[{i}] = {lam:12.6e}")
    
    print(f"\nDimensión del rolling space: {result.R.shape[1]}")
    print(f"Perímetro (centros): {result.perimeter_centers:.6f}")
    print(f"Perímetro (discos): {result.perimeter_disks:.6f}")


def example_4_visualization():
    """Ejemplo 4: Visualización."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Visualización")
    print("="*60)
    
    config = load_configuration("D5-7")
    result = analyze_configuration(config)
    
    # Gráfico de discos con hull
    print("Mostrando gráfico de discos...")
    plot_disks(config, show_hull=True)
    
    # Grafo de contacto
    print("Mostrando grafo de contacto...")
    plot_contact_graph(config, show_normals=True)
    
    # Espectro
    print("Mostrando espectro...")
    plot_spectrum(result.eigenvalues, config.name)


def example_5_comparative_analysis():
    """Ejemplo 5: Análisis comparativo."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Análisis comparativo")
    print("="*60)
    
    # Comparar todas las configuraciones de 5 discos
    configs_5 = get_configurations_by_size(5)
    print(f"Configuraciones de 5 discos: {len(configs_5)}")
    
    print(f"\n{'Config':<10} {'Roll dim':<10} {'Perimeter':<12} {'Min λ':<12} {'Max λ':<12}")
    print("-" * 60)
    
    for name in configs_5[:5]:  # Primeras 5 para el ejemplo
        config = load_configuration(name)
        result = analyze_configuration(config)
        
        roll_dim = result.R.shape[1]
        perim = result.perimeter_disks
        min_eig = result.eigenvalues[0] if len(result.eigenvalues) > 0 else 0
        max_eig = result.eigenvalues[-1] if len(result.eigenvalues) > 0 else 0
        
        print(f"{name:<10} {roll_dim:<10} {perim:<12.4f} {min_eig:<12.4e} {max_eig:<12.4e}")


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    example_1_load_from_catalog()
    example_2_custom_configuration()
    example_3_full_analysis()
    # example_4_visualization()  # Descomentarparaver gráficos
    example_5_comparative_analysis()
    
    print("\n" + "="*60)
    print("Ejemplos completados")
    print("="*60)
