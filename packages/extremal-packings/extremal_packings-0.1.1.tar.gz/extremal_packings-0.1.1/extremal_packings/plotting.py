"""
Módulo de visualización con Matplotlib.

Provee funciones para visualización estática de configuraciones de discos,
grafos de contacto y espectros del Hessiano intrínseco.
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from .configurations import Configuration
from .perimeter import compute_disk_hull_geometry


COLORS = {
    'disk_edge': '#2E3A59',
    'disk_fill': '#E8EAF6',
    'center': '#1A1A1A',
    'contact_tangent': '#9C27B0',
    'hull': '#2E3A59',
    'label': '#1A1A1A',
    'spectrum_bar': '#64B5F6',
}

EDGE_COLORS = [
    '#77B6EA', '#FFB577', '#88D8B0', '#FF9AA2', '#C38EC7',
    '#D4A5A5', '#FF9EC5', '#B0B0B0', '#FFD97D',
]


def _create_arc_points(center: np.ndarray, radius: float, 
                       angle_start: float, angle_end: float, 
                       num_points: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """
    Genera puntos para dibujar un arco circular.
    
    Args:
        center: Centro del círculo (x, y)
        radius: Radio del círculo
        angle_start: Ángulo inicial en grados
        angle_end: Ángulo final en grados
        num_points: Número de puntos del arco
    
    Returns:
        Tupla (x_points, y_points) con coordenadas del arco
    """
    if isinstance(center, (list, tuple)):
        center = np.array(center)
    
    angle_start_rad = np.radians(angle_start)
    angle_end_rad = np.radians(angle_end)
    
    angle_diff = angle_end_rad - angle_start_rad
    if angle_diff < 0:
        angle_diff += 2 * np.pi
    
    if angle_diff > np.pi:
        final_start_rad = angle_end_rad
        final_diff = 2 * np.pi - angle_diff
    else:
        final_start_rad = angle_start_rad
        final_diff = angle_diff
    
    angles = np.linspace(final_start_rad, final_start_rad + final_diff, num_points)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    
    return x, y


def plot_disks(config: Configuration, ax=None, radius: float = 1.0,
               show_labels: bool = True, show_centers: bool = True,
               show_hull: bool = True, show_contacts: bool = True,
               show_tangents: bool = False) -> None:
    """
    Visualiza configuración de discos con opciones de visualización.
    
    Args:
        config: Configuración de discos
        ax: Axes de matplotlib (crea nueva figura si None)
        radius: Radio de los discos
        show_labels: Mostrar etiquetas de índices
        show_centers: Mostrar centros marcados
        show_hull: Mostrar envolvente convexa de discos
        show_contacts: Mostrar aristas de contacto
        show_tangents: Mostrar tangentes de contacto
    """
    coords = config.coords
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
        standalone = True
    else:
        standalone = False
    
    if standalone:
        fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    for i, (xi, yi) in enumerate(coords):
        circle = Circle((xi, yi), radius,
                       fill=True,
                       facecolor=COLORS['disk_fill'],
                       edgecolor=COLORS['disk_edge'],
                       linewidth=2,
                       alpha=0.7,
                       zorder=2)
        ax.add_patch(circle)
    
    if show_contacts:
        for idx, (i, j) in enumerate(config.edges):
            edge_color = EDGE_COLORS[idx % len(EDGE_COLORS)]
            xs = [coords[i, 0], coords[j, 0]]
            ys = [coords[i, 1], coords[j, 1]]
            ax.plot(xs, ys, color=edge_color,
                   linewidth=2.5, zorder=3, alpha=0.9)
    
    if show_tangents:
        for idx, (i, j) in enumerate(config.edges):
            ci, cj = coords[i], coords[j]
            diff = cj - ci
            dist = np.linalg.norm(diff)
            if dist > 1e-10:
                contact_point = ci + (diff / dist) * radius
                tangent = np.array([-diff[1], diff[0]]) / dist
                t_len = 0.5
                p1 = contact_point - tangent * t_len
                p2 = contact_point + tangent * t_len
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                       color=COLORS['contact_tangent'],
                       linewidth=2, zorder=4, alpha=0.9)
    
    if show_centers:
        ax.scatter(coords[:, 0], coords[:, 1],
                  color=COLORS['center'], s=50, zorder=5,
                  edgecolors='white', linewidths=1)
    
    if show_labels:
        for i, (xi, yi) in enumerate(coords):
            centroid = coords.mean(axis=0)
            direction = np.array([xi, yi]) - centroid
            direction_norm = np.linalg.norm(direction)
            
            if direction_norm > 1e-10:
                offset_dir = direction / direction_norm * 0.2
                text_x = xi + offset_dir[0]
                text_y = yi + offset_dir[1]
            else:
                text_x = xi
                text_y = yi + 0.2
            
            ax.text(text_x, text_y, str(i), ha="center", va="center",
                   fontsize=11, fontweight='bold',
                   color=COLORS['label'], zorder=6,
                   bbox=dict(boxstyle='round,pad=0.3',
                           facecolor='white',
                           edgecolor='none',
                           alpha=0.8))
    
    if show_hull:
        hull_geom = compute_disk_hull_geometry(config, radius)
        
        if hull_geom:
            if 'tangent_segments' in hull_geom:
                for segment in hull_geom['tangent_segments']:
                    start = segment['start']
                    end = segment['end']
                    ax.plot([start[0], end[0]], [start[1], end[1]],
                           color=COLORS['hull'], linewidth=4,
                           linestyle='-', zorder=10, alpha=1.0)
            
            if 'arcs' in hull_geom:
                for arc in hull_geom['arcs']:
                    arc_x, arc_y = _create_arc_points(
                        arc['center'],
                        arc['radius'],
                        arc['angle_start'],
                        arc['angle_end']
                    )
                    ax.plot(arc_x, arc_y,
                           color=COLORS['hull'], linewidth=4,
                           linestyle='-', zorder=10, alpha=1.0)
    
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_title(f"{config.name} (Discos)", fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    if standalone:
        plt.tight_layout()
        plt.show()


def plot_contact_graph(config: Configuration, ax=None, show_normals: bool = False) -> None:
    """
    Visualiza el grafo de contacto.
    
    Args:
        config: Configuración de discos
        ax: Axes de matplotlib (crea nueva figura si None)
        show_normals: Mostrar vectores normales de contacto
    """
    coords = config.coords
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
        standalone = True
    else:
        standalone = False
    
    if standalone:
        fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    for idx, (i, j) in enumerate(config.edges):
        edge_color = EDGE_COLORS[idx % len(EDGE_COLORS)]
        xs = [coords[i, 0], coords[j, 0]]
        ys = [coords[i, 1], coords[j, 1]]
        ax.plot(xs, ys, color=edge_color,
               linewidth=3, zorder=2, alpha=0.9)
        
        if show_normals:
            diff = coords[j] - coords[i]
            dist = np.linalg.norm(diff)
            if dist > 0:
                u = diff / dist
                mid = (coords[i] + coords[j]) / 2
                ax.arrow(mid[0], mid[1], u[0] * 0.4, u[1] * 0.4,
                        head_width=0.15, head_length=0.15,
                        fc=COLORS['contact_tangent'],
                        ec=COLORS['contact_tangent'],
                        linewidth=2, zorder=3)
    
    ax.scatter(coords[:, 0], coords[:, 1],
              s=400, c=COLORS['center'], zorder=4,
              edgecolors='white', linewidths=2)
    
    for k, (xi, yi) in enumerate(coords):
        ax.text(xi, yi, str(k), ha="center", va="center",
               fontsize=13, fontweight='bold', color='white', zorder=5)
    
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_title(f"{config.name} (Centros)",
                fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    if standalone:
        plt.tight_layout()
        plt.show()


def plot_spectrum(eigenvalues: np.ndarray, ax=None, config_name: str = "") -> None:
    """
    Visualiza el espectro del Hessiano intrínseco.
    
    Args:
        eigenvalues: Autovalores ordenados
        ax: Axes de matplotlib (crea nueva figura si None)
        config_name: Nombre para el título
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 7))
        standalone = True
    else:
        standalone = False
    
    if standalone:
        fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    x = np.arange(len(eigenvalues))
    colors = [COLORS['spectrum_bar'] if val >= 0 else COLORS['contact_tangent']
              for val in eigenvalues]
    
    bars = ax.bar(x, eigenvalues, color=colors, edgecolor=COLORS['disk_edge'],
                  linewidth=1.5, alpha=0.8)
    
    ax.axhline(y=0, color=COLORS['disk_edge'], linestyle='--',
              linewidth=2, alpha=0.7)
    
    ax.set_xlabel("Índice del autovalor", fontsize=12, fontweight='bold')
    ax.set_ylabel("Autovalor", fontsize=12, fontweight='bold')
    ax.set_title(f"Espectro del Hessiano Intrínseco - {config_name}",
                fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.2, axis='y', linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for i, (val, bar) in enumerate(zip(eigenvalues, bars)):
        if abs(val) > 1e-10:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.2e}',
                   ha='center', va='bottom' if val > 0 else 'top',
                   fontsize=9, fontweight='bold')
    
    if standalone:
        plt.tight_layout()
        plt.show()


def plot_complete_analysis(config: Configuration, result=None, figsize=(16, 12)):
    """
    Visualización completa con 4 subplots.
    
    Args:
        config: Configuración a visualizar
        result: Resultado del análisis (se calcula si None)
        figsize: Tamaño de la figura
    """
    from .analysis import analyze_configuration
    
    if result is None:
        result = analyze_configuration(config)
    
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor('white')
    
    ax1 = plt.subplot(2, 2, 1)
    plot_disks(config, ax=ax1, show_hull=True, show_tangents=False)
    
    ax2 = plt.subplot(2, 2, 2)
    plot_contact_graph(config, ax=ax2, show_normals=True)
    
    ax3 = plt.subplot(2, 2, 3)
    plot_disks(config, ax=ax3, show_hull=False, show_tangents=True)
    
    ax4 = plt.subplot(2, 2, 4)
    plot_spectrum(result.eigenvalues, ax=ax4, config_name=config.name)
    
    plt.suptitle(f"Análisis Completo: {config.name}",
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.show()