"""
Interfaz de línea de comandos para extremal_packings.
"""

import click
import json
import sys
import numpy as np
from pathlib import Path
from typing import Optional

from .configurations import Configuration
from .catalog import (
    list_configurations,
    load_configuration,
    get_configurations_by_size,
    get_catalog_stats,
)
from .analysis import analyze_configuration
from .plotting import plot_disks, plot_contact_graph, plot_spectrum
import matplotlib.pyplot as plt


@click.group()
@click.version_option(version="1.0.0", prog_name="epack")
def cli():
    """
    epack - Extremal Packings CLI
    
    Herramienta de línea de comandos para analizar configuraciones de discos
    tangentes, calcular rolling spaces, Hessianos intrínsecos y perímetros.
    
    \b
    Ejemplos:
      epack list              # Listar todas las configuraciones
      epack list -s 5         # Solo configuraciones de 5 discos
      epack analyze D5-7      # Analizar configuración específica
      epack analyze D5-7 -p   # Analizar y mostrar gráficos
      epack compare -s 5      # Comparar todas las de 5 discos
      epack info D5-7         # Información detallada
      epack plot D5-7         # Visualizar configuración
      epack stats             # Estadísticas del catálogo
    
    Para más ayuda: epack COMMAND --help
    """
    pass


@cli.command()
@click.option('--size', '-s', type=int, help='Filtrar por número de discos')
@click.option('--verbose', '-v', is_flag=True, help='Mostrar información detallada')
def list(size: Optional[int], verbose: bool):
    """Lista todas las configuraciones disponibles."""
    
    if size:
        configs = get_configurations_by_size(size)
        click.echo(f"\n📋 Configuraciones de {size} discos: {len(configs)}")
    else:
        configs = list_configurations()
        click.echo(f"\n📋 Total de configuraciones: {len(configs)}")
    
    if verbose:
        for name in configs:
            config = load_configuration(name)
            click.echo(f"  • {name}: {config.n} discos, {len(config.edges)} contactos")
    else:
        # Mostrar en columnas
        for i in range(0, len(configs), 6):
            row = configs[i:i+6]
            click.echo("  " + "  ".join(f"{c:<10}" for c in row))
    
    click.echo()


@cli.command()
@click.argument('name')
@click.option('--output', '-o', type=click.Path(), help='Guardar resultados en JSON')
@click.option('--plot', '-p', is_flag=True, help='Mostrar gráficos')
@click.option('--verbose', '-v', is_flag=True, help='Mostrar detalles completos')
@click.option('--debug', '-d', is_flag=True, help='Modo debugging: muestra todos los pasos intermedios')
def analyze(name: str, output: Optional[str], plot: bool, verbose: bool, debug: bool):
    """
    Analiza una configuración específica.
    
    Calcula matriz de contacto, rolling space, Hessiano intrínseco,
    espectro y perímetros.
    
    Ejemplos:
    
        epack analyze D5-7
        epack analyze D5-7 --output results.json
        epack analyze D5-7 --plot --verbose
        epack analyze D5-7 --debug  # Modo debugging completo
    """
    
    try:
        config = load_configuration(name)
    except KeyError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    
    click.echo(f"\n🔍 Analizando {name}...\n")
    
    # Modo debugging: mostrar TODOS los pasos
    if debug:
        _debug_analysis(config)
        return
    
    result = analyze_configuration(config)
    
    # Detectar si es cadena colineal
    from extremal_packings.perimeter import compute_hull, is_collinear_chain
    hull = compute_hull(config)
    is_chain = is_collinear_chain(config, hull)
    
    # Mostrar resumen
    click.echo(f"{'='*60}")
    click.echo(f"Configuración: {config.name}")
    click.echo(f"{'='*60}")
    click.echo(f"Número de discos (n):     {config.n}")
    click.echo(f"Número de contactos (m):  {len(config.edges)}")
    
    if is_chain:
        click.echo(f"Tipo:                     Cadena colineal")
    else:
        click.echo(f"Tipo:                     Cluster 2D")
    
    click.echo(f"\nRolling Space:")
    click.echo(f"  Dimensión:              {result.rolling_dim}")
    click.echo(f"  Rigidez:                {'Rígida' if result.is_rigid else 'Flexible'}")
    
    click.echo(f"\nPerímetros:")
    click.echo(f"  Centros:                {result.perimeter_centers:.6f}")
    click.echo(f"  Discos (+ 2πr):         {result.perimeter_disks:.6f}")
    
    # Aproximar gradiente a cero si es muy pequeño
    grad_display = result.grad_p.copy()
    grad_display[np.abs(grad_display) < 1e-12] = 0.0
    
    proj_grad_display = result.proj_grad_p.copy()
    proj_grad_display[np.abs(proj_grad_display) < 1e-12] = 0.0
    
    click.echo(f"\nGradiente del perímetro:")
    click.echo(f"  ∇Per(c) = {grad_display.tolist()}")
    click.echo(f"\nProyección del gradiente:")
    click.echo(f"  Proj(∇Per) = {proj_grad_display.tolist()}")
    
    # Aproximar autovalores a cero si son muy pequeños
    eigenvalues_display = result.eigenvalues.copy()
    eigenvalues_display[np.abs(eigenvalues_display) < 1e-12] = 0.0
    
    click.echo(f"\nEspectro del Hessiano Intrínseco:")
    click.echo(f"  Autovalores ({len(eigenvalues_display)}):")
    
    for i, lam in enumerate(eigenvalues_display):
        click.echo(f"    λ_{i}: {lam:12.6e}")
    
    click.echo(f"{'='*60}\n")
    
    # Verbose: mostrar dimensiones de matrices
    if verbose:
        click.echo(f"Dimensiones de matrices:")
        click.echo(f"  A (contacto):           {result.A.shape}")
        click.echo(f"  R (rolling space):      {result.R.shape}")
        click.echo(f"  K (Hessiano global):    {result.K.shape}")
        click.echo(f"  H (Hessiano intrínseco): {result.H.shape}")
        click.echo()
    
    # Guardar resultados
    if output:
        data = {
            'name': config.name,
            'n_disks': config.n,
            'n_edges': len(config.edges),
            'rolling_dim': result.rolling_dim,
            'is_rigid': result.is_rigid,
            'perimeter_centers': float(result.perimeter_centers),
            'perimeter_disks': float(result.perimeter_disks),
            'eigenvalues': eigenvalues_display.tolist(),
            'coords': config.coords.tolist(),
            'edges': config.edges,
        }
        
        output_path = Path(output)
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        click.echo(f"💾 Resultados guardados en: {output_path}\n")
    
    # Visualización
    if plot:
        click.echo("📊 Generando gráficos...\n")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        plot_disks(config, ax=axes[0], show_hull=True)
        plot_contact_graph(config, ax=axes[1], show_normals=False)
        
        plt.tight_layout()
        plt.show()


@cli.command()
@click.option('--size', '-s', type=int, required=True, help='Número de discos')
@click.option('--metric', '-m', 
              type=click.Choice(['perimeter', 'eigenvalue', 'rolling_dim']),
              default='perimeter',
              help='Métrica para ordenar resultados')
@click.option('--output', '-o', type=click.Path(), help='Guardar tabla en CSV')
def compare(size: int, metric: str, output: Optional[str]):
    """
    Compara todas las configuraciones de un tamaño específico.
    
    Analiza todas las configuraciones con el número de discos especificado
    y muestra una tabla comparativa ordenada por la métrica elegida.
    
    Ejemplos:
    
        epack compare -s 5
        epack compare -s 5 -m eigenvalue
        epack compare -s 5 -o resultados.csv
    """
    
    configs = get_configurations_by_size(size)
    
    if not configs:
        click.echo(f"❌ No hay configuraciones de {size} discos", err=True)
        sys.exit(1)
    
    click.echo(f"\n🔬 Comparando {len(configs)} configuraciones de {size} discos...\n")
    
    results = []
    
    with click.progressbar(configs, label='Analizando') as bar:
        for name in bar:
            config = load_configuration(name)
            result = analyze_configuration(config)
            
            results.append({
                'name': name,
                'n_edges': len(config.edges),
                'rolling_dim': result.rolling_dim,
                'perimeter_centers': result.perimeter_centers,
                'perimeter_disks': result.perimeter_disks,
                'gradient_perimeter': result.grad_p.tolist(),
                'projected_gradient': result.proj_grad_p.tolist(),
                'is_critical': 'Si' if result.is_critical else 'No',
                'min_eigenvalue': result.eigenvalues[0] if len(result.eigenvalues) > 0 else 0,
                'max_eigenvalue': result.eigenvalues[-1] if len(result.eigenvalues) > 0 else 0,
                'is_rigid': result.is_rigid,
            })
    
    # Ordenar por métrica
    if metric == 'perimeter':
        results.sort(key=lambda x: x['perimeter_disks'])
        metric_col = 'perimeter_disks'
    elif metric == 'eigenvalue':
        results.sort(key=lambda x: x['min_eigenvalue'])
        metric_col = 'min_eigenvalue'
    else:  # rolling_dim
        results.sort(key=lambda x: x['rolling_dim'])
        metric_col = 'rolling_dim'
    
    # Mostrar tabla
    header = f"{'Config':<10} {'Edges':<7} {'Roll':<7} {'Perímetro':<12} {'Crítica':<10} {'λ_min':<12} {'λ_max':<12} {'Rígida':<8}"
    click.echo(header)
    click.echo("=" * len(header))
    
    for r in results:
        rigid_str = "Sí" if r['is_rigid'] else "No"
        click.echo(
            f"{r['name']:<10} "
            f"{r['n_edges']:<7} "
            f"{r['rolling_dim']:<7} "
            f"{r['perimeter_disks']:<12.6f} "
            f"{r['is_critical']:<10} "
            #Si el gradiente proyectado es el vector nulo, entonces Sí es crítico a primer orden
            #f"{'Sí' if all(v == 0 for v in r['projected_gradient']) else 'No':<10} "
            f"{r['min_eigenvalue']:<12.4e} "
            f"{r['max_eigenvalue']:<12.4e} "
            f"{rigid_str:<8}"
        )
    
    # Resumen
    click.echo(f"\n{'='*80}")
    click.echo(f"Mínimo perímetro: {results[0]['name']} = {results[0]['perimeter_disks']:.6f}")
    click.echo(f"Máximo perímetro: {results[-1]['name']} = {results[-1]['perimeter_disks']:.6f}")
    rigid_count = sum(1 for r in results if r['is_rigid'])
    click.echo(f"Configuraciones rígidas: {rigid_count}/{len(results)}")
    click.echo(f"{'='*80}\n")
    
    # Guardar CSV
    if output:
        import csv
        output_path = Path(output)
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        click.echo(f"💾 Tabla guardada en: {output_path}\n")


@cli.command()
@click.argument('name')
def info(name: str):
    """
    Muestra información detallada de una configuración.
    
    Incluye coordenadas de centros, lista de contactos y grados de vértices.
    
    Ejemplo:
    
        epack info D5-7
    """
    
    try:
        config = load_configuration(name)
    except KeyError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    
    click.echo(f"\n📋 Información de {name}")
    click.echo(f"{'='*60}")
    click.echo(f"Nombre:          {config.name}")
    click.echo(f"Discos (n):      {config.n}")
    click.echo(f"Contactos (m):   {len(config.edges)}")
    click.echo(f"\nCoordenadas de centros:")
    
    for i, (x, y) in enumerate(config.coords):
        click.echo(f"  Disco {i}: ({x:8.4f}, {y:8.4f})")
    
    click.echo(f"\nGrafo de contacto:")
    for i, (u, v) in enumerate(config.edges):
        click.echo(f"  Contacto {i}: ({u}, {v})")
    
    # Calcular grados
    degrees = [0] * config.n
    for i, j in config.edges:
        degrees[i] += 1
        degrees[j] += 1
    
    click.echo(f"\nGrados de los vértices:")
    for i, deg in enumerate(degrees):
        click.echo(f"  Disco {i}: grado {deg}")
    
    click.echo(f"{'='*60}\n")


@cli.command()
@click.argument('name')
@click.option('--hull/--no-hull', default=True, help='Mostrar envolvente convexa')
@click.option('--normals/--no-normals', default=False, help='Mostrar vectores normales')
def plot(name: str, hull: bool, normals: bool):
    """
    Visualiza una configuración con gráficos interactivos.
    
    Muestra dos paneles: discos con envolvente convexa y grafo de contacto.
    
    Ejemplos:
    
        epack plot D5-7
        epack plot D5-7 --no-hull
        epack plot D5-7 --normals
    """
    
    try:
        config = load_configuration(name)
    except KeyError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    
        click.echo(f"📊 Visualizando {name}...\n")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # PASAR ax explícitamente
    plot_disks(config, ax=axes[0], show_hull=hull)
    
    # PASAR ax explícitamente
    plot_contact_graph(config, ax=axes[1], show_normals=normals)
    
    plt.tight_layout()
    plt.show()

@cli.command()
def stats():
    """
    Muestra estadísticas generales del catálogo.
    
    Incluye total de configuraciones, distribución por tamaño y rango.
    
    Ejemplo:
    
        epack stats
    """
    
    stats = get_catalog_stats()
    
    click.echo(f"\n📊 Estadísticas del Catálogo")
    click.echo(f"{'='*60}")
    click.echo(f"Total de configuraciones: {stats['total']}")
    click.echo(f"Rango de tamaños: {stats['min_disks']} a {stats['max_disks']} discos")
    click.echo(f"\nDistribución por tamaño:")
    
    for size in sorted(stats['by_size'].keys()):
        count = stats['by_size'][size]
        bar = '█' * min(count // 2, 40)  # Limitar ancho de barras
        click.echo(f"  {size} discos: {count:3d} {bar}")
    
    click.echo(f"{'='*60}\n")


def _debug_analysis(config: Configuration):
    """
    Análisis detallado paso a paso con información de diagnóstico.
    """
    from extremal_packings.perimeter import compute_hull, is_collinear_chain, find_chain_endpoints
    from extremal_packings.constraints import (
        build_contact_matrix, 
        rolling_space_basis,
        compute_perimeter_gradient,
        get_projector
    )
    
    click.echo(f"{'='*80}")
    click.echo(f"DEBUG: {config.name}")
    click.echo(f"{'='*80}\n")
    
    # 1. Configuración básica
    click.echo("1. CONFIGURACIÓN")
    click.echo(f"   n = {config.n}, m = {len(config.edges)}")
    click.echo(f"   Coordenadas:")
    for i, (x, y) in enumerate(config.coords):
        click.echo(f"     c[{i}] = [{x:.6f}, {y:.6f}]")
    click.echo()
    
    # 2. Hull y perímetro
    click.echo("2. CONVEX HULL Y PERÍMETRO")
    hull = compute_hull(config)
    is_chain = is_collinear_chain(config, hull)
    click.echo(f"   Hull: {hull}")
    click.echo(f"   Tipo: {'Cadena colineal' if is_chain else 'Polígono convexo'}")
    
    if is_chain:
        i, j = find_chain_endpoints(config, hull)
        dist = np.linalg.norm(config.coords[j] - config.coords[i])
        click.echo(f"   Extremos: {i}, {j}")
        click.echo(f"   Perímetro centros = 2 × {dist:.6f} = {2*dist:.6f}")
    else:
        perim = sum(np.linalg.norm(config.coords[hull[(k+1)%len(hull)]] - config.coords[hull[k]]) 
                   for k in range(len(hull)))
        click.echo(f"   Perímetro centros = {perim:.6f}")
    
    click.echo(f"   perimeter_edges: {config.perimeter_edges}")
    click.echo()
    
    # 3. Matriz de contacto
    click.echo("3. MATRIZ DE CONTACTO")
    A = build_contact_matrix(config)
    click.echo(f"   Dimensión: {A.shape}")
    click.echo(f"   Rango: {np.linalg.matrix_rank(A)}")
    click.echo()
    
    # 4. Rolling space
    click.echo("4. ROLLING SPACE")
    R = rolling_space_basis(A) if len(config.edges) > 0 else np.eye(2*config.n, dtype=np.float64)
    click.echo(f"   Dimensión: {R.shape[1]}")
    click.echo(f"   Esperada: {2*config.n - len(config.edges)}")
    click.echo(f"   Rígida: {R.shape[1] <= 3}")
    click.echo()
    
    # 5. Gradiente
    click.echo("5. GRADIENTE DEL PERÍMETRO")
    grad = compute_perimeter_gradient(config)
    click.echo(f"   ||∇Per|| = {np.linalg.norm(grad):.6e}")
    
    P = get_projector(config)
    proj_grad = P @ grad
    click.echo(f"   ||P∇Per|| = {np.linalg.norm(proj_grad):.6e}")
    click.echo(f"   Punto crítico: {np.linalg.norm(proj_grad) < 1e-12}")
    click.echo()
    
    # 6. Hessiano intrínseco
    click.echo("6. HESSIANO INTRÍNSECO")
    from extremal_packings.hessian import compute_intrinsic_hessian, project_to_roll
    
    epsilon = np.sqrt(np.finfo(np.float64).eps) * 10
    click.echo(f"   Epsilon: {epsilon:.6e}")
    
    H_ambient = compute_intrinsic_hessian(config, R, epsilon=epsilon, debug=False)
    click.echo(f"   ||H_ambient|| = {np.linalg.norm(H_ambient, 'fro'):.6e}")
    
    H = project_to_roll(H_ambient, R)
    click.echo(f"   Dimensión reducida: {H.shape}")
    click.echo()
    
    # 7. Espectro
    click.echo("7. ESPECTRO")
    from extremal_packings.hessian import intrinsic_spectrum
    
    if H.shape[0] > 0:
        eigenvalues = intrinsic_spectrum(H)
        click.echo(f"   Autovalores:")
        for i, lam in enumerate(eigenvalues):
            tipo = "0" if abs(lam) < 1e-12 else ("+" if lam > 0 else "-")
            click.echo(f"     λ[{i}] = {lam:+.6e}  [{tipo}]")
        
        n_neg = np.sum(eigenvalues < -1e-12)
        n_pos = np.sum(eigenvalues > 1e-12)
        n_zero = len(eigenvalues) - n_neg - n_pos
        
        click.echo(f"\n   Negativos: {n_neg}, Ceros: {n_zero}, Positivos: {n_pos}")
    
    click.echo(f"\n{'='*80}\n")


if __name__ == '__main__':
    cli()