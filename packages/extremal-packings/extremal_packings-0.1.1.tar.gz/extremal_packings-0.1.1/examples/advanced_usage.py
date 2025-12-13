"""
Ejemplos avanzados del paquete extremal_packings.

Cubre funcionalidades de bajo nivel y uso avanzado:
1. Operaciones con matrices (A, R, K, H)
2. Análisis paso a paso del pipeline
3. Cálculo manual de perímetros
4. Validación de grafos
5. Interfaz de alto nivel
"""

import numpy as np
from extremal_packings import (
    Configuration,
    load_configuration,
    # Bajo nivel - constraints
    build_contact_matrix,
    rolling_space_basis,
    # Bajo nivel - hessian
    build_unconstrained_hessian,
    project_to_roll,
    intrinsic_spectrum,
    # Bajo nivel - perimeter
    perimeter_centers,
    perimeter_disks,
    compute_hull,
    # Alto nivel
    analyze_configuration,
    print_analysis_summary,
    show_complete_analysis,
)


def example_6_contact_matrix():
    """Ejemplo 6: Construcción manual de matriz de contacto."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Matriz de contacto")
    print("="*60)
    
    # Configuración simple: 3 discos en línea
    coords = np.array([[0, 0], [2, 0], [4, 0]])
    edges = [(0, 1), (1, 2)]
    config = Configuration(coords=coords, edges=edges)
    
    # Construir matriz de contacto
    A = build_contact_matrix(config)
    
    print(f"Configuración: {config.n} discos, {len(edges)} contactos")
    print(f"Dimensiones de A: {A.shape}")
    print(f"\nMatriz de contacto A:")
    print(A)
    
    # Verificar ortogonalidad de filas
    dot_products = A @ A.T
    print(f"\nA @ A^T (productos de filas):")
    print(dot_products)


def example_7_rolling_space():
    """Ejemplo 7: Análisis del rolling space."""
    print("\n" + "="*60)
    print("EJEMPLO 7: Rolling space")
    print("="*60)
    
    # Configuración flexible
    coords = np.array([[0, 0], [2, 0], [4, 0], [6, 0]])
    edges = [(0, 1), (1, 2), (2, 3)]
    config = Configuration(coords=coords, edges=edges)
    
    # Construir A y calcular rolling space
    A = build_contact_matrix(config)
    R = rolling_space_basis(A)
    
    print(f"Dimensiones:")
    print(f"  A: {A.shape} (m={A.shape[0]}, 2n={A.shape[1]})")
    print(f"  R: {R.shape} (2n={R.shape[0]}, d={R.shape[1]})")
    print(f"\nDimensión del rolling space: {R.shape[1]}")
    print(f"Grados de libertad: 2n - m = {2*config.n} - {len(edges)} = {2*config.n - len(edges)}")
    
    # Verificar ortogonalidad
    RtR = R.T @ R
    print(f"\nR^T @ R (debe ser identidad):")
    print(RtR)
    
    # Verificar que R está en el kernel de A
    AR = A @ R
    print(f"\nA @ R (debe ser ~0):")
    print(f"Norma de Frobenius: {np.linalg.norm(AR):.2e}")


def example_8_hessian_analysis():
    """Ejemplo 8: Análisis del Hessiano."""
    print("\n" + "="*60)
    print("EJEMPLO 8: Hessiano intrínseco")
    print("="*60)
    
    # Triángulo equilátero
    coords = np.array([
        [0, 0],
        [2, 0],
        [1, np.sqrt(3)]
    ])
    edges = [(0, 1), (1, 2), (2, 0)]
    config = Configuration(coords=coords, edges=edges, name="Triangle")
    
    # Pipeline paso a paso
    print("1. Construyendo matriz de contacto...")
    A = build_contact_matrix(config)
    
    print("2. Calculando rolling space...")
    R = rolling_space_basis(A)
    
    print("3. Construyendo Hessiano global...")
    K = build_unconstrained_hessian(config)
    
    print("4. Proyectando al rolling space...")
    H = project_to_roll(K, R)
    
    print("5. Calculando espectro...")
    eigenvalues = intrinsic_spectrum(H)
    
    # Resultados
    print(f"\nResultados:")
    print(f"  Dimensión rolling space: {R.shape[1]}")
    print(f"  Dimensión Hessiano intrínseco: {H.shape}")
    print(f"  Autovalores: {eigenvalues}")
    
    # Verificar simetría
    print(f"\nVerificaciones:")
    print(f"  K simétrico: {np.allclose(K, K.T)}")
    print(f"  H simétrico: {np.allclose(H, H.T)}")
    print(f"  Autovalores reales: {np.all(np.isreal(eigenvalues))}")


def example_9_perimeter_calculations():
    """Ejemplo 9: Cálculo de perímetros."""
    print("\n" + "="*60)
    print("EJEMPLO 9: Cálculo de perímetros")
    print("="*60)
    
    # Pentágono regular
    config = load_configuration("D5-7")
    
    print(f"Configuración: {config.name}")
    print(f"Número de discos: {config.n}")
    
    # Calcular envolvente convexa
    hull_indices = compute_hull(config)
    print(f"\nÍndices del casco convexo: {hull_indices}")
    print(f"Número de vértices en el casco: {len(hull_indices)}")
    
    # Perímetro de centros
    p_centers = perimeter_centers(config)
    print(f"\nPerímetro de centros: {p_centers:.6f}")
    
    # Perímetro de discos
    p_disks = perimeter_disks(config)
    print(f"Perímetro de discos: {p_disks:.6f}")
    
    # Comparación
    ratio = p_disks / p_centers
    print(f"Ratio perímetros: {ratio:.6f}")


def example_10_graph_validation():
    """Ejemplo 10: Validación de grafos."""
    print("\n" + "="*60)
    print("EJEMPLO 10: Validación de grafos")
    print("="*60)
    
    from extremal_packings.contact_graphs import check_graph_validity
    
    # Caso 1: Grafo válido
    print("Caso 1: Grafo conexo válido")
    edges_valid = [(0, 1), (1, 2), (2, 3), (3, 0)]
    try:
        check_graph_validity(4, edges_valid)
        print("  ✓ Grafo válido")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    
    # Caso 2: Grafo desconectado
    print("\nCaso 2: Grafo desconectado")
    edges_disconnected = [(0, 1), (2, 3)]
    try:
        check_graph_validity(4, edges_disconnected)
        print("  ✓ Grafo válido")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    
    # Caso 3: Grado excesivo
    print("\nCaso 3: Vértice con grado > 6")
    edges_high_degree = [(0, i) for i in range(1, 8)]
    try:
        check_graph_validity(8, edges_high_degree)
        print("  ✓ Grafo válido")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def example_11_high_level_interface():
    """Ejemplo 11: Interfaz de alto nivel."""
    print("\n" + "="*60)
    print("EJEMPLO 11: Interfaz de alto nivel")
    print("="*60)
    
    # Cargar configuración
    config = load_configuration("D5-7")
    
    # Análisis completo
    result = analyze_configuration(config)
    
    # Usar print_analysis_summary
    print("\n--- Resumen del análisis ---")
    print_analysis_summary(result)
    
    # Nota: show_complete_analysis crea gráficos
    # Descomentar para ver visualización completa:
    # show_complete_analysis(config)


def example_12_custom_analysis():
    """Ejemplo 12: Análisis personalizado."""
    print("\n" + "="*60)
    print("EJEMPLO 12: Análisis personalizado")
    print("="*60)
    
    # Crear varias configuraciones
    configs = {
        "Cadena-3": Configuration(
            coords=np.array([[0, 0], [2, 0], [4, 0]]),
            edges=[(0, 1), (1, 2)]
        ),
        "Triángulo": Configuration(
            coords=np.array([[0, 0], [2, 0], [1, np.sqrt(3)]]),
            edges=[(0, 1), (1, 2), (2, 0)]
        ),
        "Cuadrado": Configuration(
            coords=np.array([[0, 0], [2, 0], [2, 2], [0, 2]]),
            edges=[(0, 1), (1, 2), (2, 3), (3, 0)]
        ),
    }
    
    # Analizar y comparar
    print(f"\n{'Config':<15} {'n':<5} {'m':<5} {'dim(Roll)':<12} {'p_disks':<12} {'λ_min':<12}")
    print("-" * 70)
    
    for name, config in configs.items():
        result = analyze_configuration(config)
        
        n = config.n
        m = len(config.edges)
        dim_roll = result.R.shape[1]
        p_disks = result.perimeter_disks
        lambda_min = result.eigenvalues[0] if len(result.eigenvalues) > 0 else 0
        
        print(f"{name:<15} {n:<5} {m:<5} {dim_roll:<12} {p_disks:<12.4f} {lambda_min:<12.4e}")


if __name__ == "__main__":
    # Ejecutar ejemplos avanzados
    example_6_contact_matrix()
    example_7_rolling_space()
    example_8_hessian_analysis()
    example_9_perimeter_calculations()
    example_10_graph_validation()
    example_11_high_level_interface()
    example_12_custom_analysis()
    
    print("\n" + "="*60)
    print("Ejemplos avanzados completados")
    print("="*60)
