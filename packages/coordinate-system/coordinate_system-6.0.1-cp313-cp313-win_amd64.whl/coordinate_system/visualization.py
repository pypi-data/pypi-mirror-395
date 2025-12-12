"""
3D Coordinate System and Surface Visualization Module
=====================================================

Comprehensive visualization tools for coordinate systems, curves, and surfaces.

Features:
- Coordinate frame visualization with RGB color scheme (X=Red, Y=Green, Z=Blue)
- Parametric curve visualization with Frenet frames
- Surface rendering with curvature coloring
- Frame field visualization on surfaces
- Multiple view angles and animation support

Author: Coordinate System Package
Date: 2025-12-03
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize, LinearSegmentedColormap
import matplotlib.animation as animation
from typing import List, Optional, Tuple, Callable, Union, Dict

# Import from the C extension module
try:
    from .coordinate_system import vec3, coord3
except ImportError:
    import coordinate_system
    vec3 = coordinate_system.vec3
    coord3 = coordinate_system.coord3

# Import differential geometry for surface visualization
try:
    from .differential_geometry import Surface, Sphere, Torus, compute_gaussian_curvature, compute_mean_curvature
except ImportError:
    Surface = None
    Sphere = None
    Torus = None
    compute_gaussian_curvature = None
    compute_mean_curvature = None


# ============================================================
# Color Schemes
# ============================================================

# Curvature colormap: blue (negative) -> white (zero) -> red (positive)
CURVATURE_COLORS = [
    (0.0, 'blue'),
    (0.5, 'white'),
    (1.0, 'red')
]

def create_curvature_colormap():
    """Create a diverging colormap for curvature visualization."""
    return LinearSegmentedColormap.from_list('curvature',
        [(0.0, 'blue'), (0.5, 'white'), (1.0, 'red')])


# ============================================================
# Coordinate System Visualizer
# ============================================================

class CoordinateSystemVisualizer:
    """
    3D coordinate system visualization tool.

    RGB color scheme:
    - X axis: Red
    - Y axis: Green
    - Z axis: Blue
    """

    def __init__(self, figsize: Tuple[int, int] = (12, 9), dpi: int = 100):
        """
        Initialize visualizer.

        Args:
            figsize: Figure size (width, height) in inches
            dpi: Dots per inch for rendering
        """
        self.fig = plt.figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self._setup_axis()

    def _setup_axis(self):
        """Configure axis style."""
        self.ax.set_xlabel('X', fontsize=12, color='red', fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=12, color='green', fontweight='bold')
        self.ax.set_zlabel('Z', fontsize=12, color='blue', fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

    def draw_coord_system(
        self,
        coord: coord3,
        scale: float = 1.0,
        linewidth: float = 2.0,
        alpha: float = 0.8,
        label_prefix: str = "",
        arrow_style: bool = True
    ):
        """
        Draw a single coordinate frame.

        Args:
            coord: coord3 object
            scale: Axis length scale factor
            linewidth: Line width
            alpha: Transparency
            label_prefix: Label prefix for legend
            arrow_style: Use arrow heads if True
        """
        origin = coord.o

        if arrow_style:
            # Use quiver for arrows
            self.ax.quiver(
                origin.x, origin.y, origin.z,
                coord.ux.x * scale, coord.ux.y * scale, coord.ux.z * scale,
                color='red', linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.15
            )
            self.ax.quiver(
                origin.x, origin.y, origin.z,
                coord.uy.x * scale, coord.uy.y * scale, coord.uy.z * scale,
                color='green', linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.15
            )
            self.ax.quiver(
                origin.x, origin.y, origin.z,
                coord.uz.x * scale, coord.uz.y * scale, coord.uz.z * scale,
                color='blue', linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.15
            )
        else:
            # Use simple lines
            x_end = origin + coord.ux * scale
            y_end = origin + coord.uy * scale
            z_end = origin + coord.uz * scale

            self.ax.plot([origin.x, x_end.x], [origin.y, x_end.y], [origin.z, x_end.z],
                        'r-', linewidth=linewidth, alpha=alpha)
            self.ax.plot([origin.x, y_end.x], [origin.y, y_end.y], [origin.z, y_end.z],
                        'g-', linewidth=linewidth, alpha=alpha)
            self.ax.plot([origin.x, z_end.x], [origin.y, z_end.y], [origin.z, z_end.z],
                        'b-', linewidth=linewidth, alpha=alpha)

    def draw_world_coord(
        self,
        origin: vec3 = None,
        scale: float = 1.0,
        linewidth: float = 3.0
    ):
        """
        Draw world coordinate system.

        Args:
            origin: Origin position, default is (0, 0, 0)
            scale: Axis length
            linewidth: Line width
        """
        if origin is None:
            origin = vec3(0, 0, 0)

        world_coord = coord3()
        world_coord.o = origin

        self.draw_coord_system(
            world_coord,
            scale=scale,
            linewidth=linewidth,
            alpha=1.0,
            label_prefix="World-"
        )

    def draw_point(
        self,
        point: vec3,
        color: str = 'black',
        size: float = 50,
        marker: str = 'o',
        label: str = None
    ):
        """
        Draw a single point.

        Args:
            point: Point position
            color: Point color
            size: Marker size
            marker: Marker style
            label: Label for legend
        """
        self.ax.scatter([point.x], [point.y], [point.z],
                       c=color, s=size, marker=marker, label=label)

    def draw_vector(
        self,
        start: vec3,
        direction: vec3,
        color: str = 'black',
        linewidth: float = 2.0,
        alpha: float = 0.8,
        label: str = None
    ):
        """
        Draw a vector as an arrow.

        Args:
            start: Starting point
            direction: Direction vector
            color: Arrow color
            linewidth: Line width
            alpha: Transparency
            label: Label for legend
        """
        self.ax.quiver(
            start.x, start.y, start.z,
            direction.x, direction.y, direction.z,
            color=color, linewidth=linewidth, alpha=alpha,
            arrow_length_ratio=0.15, label=label
        )

    def set_equal_aspect(self):
        """Set equal aspect ratio for all axes."""
        xlim = self.ax.get_xlim3d()
        ylim = self.ax.get_ylim3d()
        zlim = self.ax.get_zlim3d()

        x_range = abs(xlim[1] - xlim[0])
        y_range = abs(ylim[1] - ylim[0])
        z_range = abs(zlim[1] - zlim[0])

        max_range = max(x_range, y_range, z_range)

        x_middle = np.mean(xlim)
        y_middle = np.mean(ylim)
        z_middle = np.mean(zlim)

        self.ax.set_xlim3d([x_middle - max_range/2, x_middle + max_range/2])
        self.ax.set_ylim3d([y_middle - max_range/2, y_middle + max_range/2])
        self.ax.set_zlim3d([z_middle - max_range/2, z_middle + max_range/2])

    def set_view(self, elev: float = 30, azim: float = 45):
        """
        Set camera view angle.

        Args:
            elev: Elevation angle in degrees
            azim: Azimuth angle in degrees
        """
        self.ax.view_init(elev=elev, azim=azim)

    def set_title(self, title: str, fontsize: int = 14):
        """Set plot title."""
        self.ax.set_title(title, fontsize=fontsize, fontweight='bold')

    def show(self):
        """Display the figure."""
        self.ax.legend(loc='upper left')
        plt.tight_layout()
        plt.show()

    def save(self, filename: str, dpi: int = 300):
        """
        Save figure to file.

        Args:
            filename: Output filename
            dpi: Resolution
        """
        self.ax.legend(loc='upper left')
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Saved: {filename}")


# ============================================================
# Surface Visualizer
# ============================================================

class SurfaceVisualizer(CoordinateSystemVisualizer):
    """
    Surface visualization with curvature coloring.

    Supports:
    - Wireframe and surface rendering
    - Gaussian/Mean curvature coloring
    - Frame field overlay
    - Normal vector visualization
    """

    def __init__(self, figsize: Tuple[int, int] = (14, 10), dpi: int = 100):
        super().__init__(figsize, dpi)
        self.colorbar = None

    def draw_surface(
        self,
        surface: 'Surface',
        u_range: Tuple[float, float] = (0.1, np.pi - 0.1),
        v_range: Tuple[float, float] = (0, 2 * np.pi),
        nu: int = 30,
        nv: int = 40,
        color: str = 'cyan',
        alpha: float = 0.6,
        wireframe: bool = True,
        surface_plot: bool = True
    ):
        """
        Draw a parametric surface.

        Args:
            surface: Surface object
            u_range: Parameter u range
            v_range: Parameter v range
            nu: Number of u samples
            nv: Number of v samples
            color: Surface color
            alpha: Transparency
            wireframe: Show wireframe
            surface_plot: Show filled surface
        """
        u = np.linspace(u_range[0], u_range[1], nu)
        v = np.linspace(v_range[0], v_range[1], nv)
        U, V = np.meshgrid(u, v)

        X = np.zeros_like(U)
        Y = np.zeros_like(U)
        Z = np.zeros_like(U)

        for i in range(nu):
            for j in range(nv):
                pos = surface.position(U[j, i], V[j, i])
                X[j, i] = pos.x
                Y[j, i] = pos.y
                Z[j, i] = pos.z

        if surface_plot:
            self.ax.plot_surface(X, Y, Z, color=color, alpha=alpha,
                                edgecolor='none', shade=True)

        if wireframe:
            self.ax.plot_wireframe(X, Y, Z, color='gray', alpha=0.3,
                                  linewidth=0.5, rstride=2, cstride=2)

    def draw_surface_curvature(
        self,
        surface: 'Surface',
        curvature_type: str = 'gaussian',
        u_range: Tuple[float, float] = (0.1, np.pi - 0.1),
        v_range: Tuple[float, float] = (0, 2 * np.pi),
        nu: int = 30,
        nv: int = 40,
        alpha: float = 0.8,
        show_colorbar: bool = True,
        step_size: float = 1e-3
    ):
        """
        Draw surface with curvature coloring.

        Args:
            surface: Surface object
            curvature_type: 'gaussian' or 'mean'
            u_range: Parameter u range
            v_range: Parameter v range
            nu: Number of u samples
            nv: Number of v samples
            alpha: Transparency
            show_colorbar: Show colorbar
            step_size: Step size for curvature computation
        """
        if compute_gaussian_curvature is None:
            raise ImportError("differential_geometry module not available")

        u = np.linspace(u_range[0], u_range[1], nu)
        v = np.linspace(v_range[0], v_range[1], nv)
        U, V = np.meshgrid(u, v)

        X = np.zeros_like(U)
        Y = np.zeros_like(U)
        Z = np.zeros_like(U)
        K = np.zeros_like(U)

        compute_func = compute_gaussian_curvature if curvature_type == 'gaussian' else compute_mean_curvature

        for i in range(nu):
            for j in range(nv):
                pos = surface.position(U[j, i], V[j, i])
                X[j, i] = pos.x
                Y[j, i] = pos.y
                Z[j, i] = pos.z
                K[j, i] = compute_func(surface, U[j, i], V[j, i], step_size)

        # Normalize curvature for coloring
        K_abs_max = max(abs(K.min()), abs(K.max()))
        if K_abs_max > 1e-10:
            K_normalized = (K / K_abs_max + 1) / 2  # Map to [0, 1]
        else:
            K_normalized = np.ones_like(K) * 0.5

        # Create colormap
        cmap = create_curvature_colormap()
        colors = cmap(K_normalized)

        # Draw surface
        surf = self.ax.plot_surface(X, Y, Z, facecolors=colors, alpha=alpha,
                                   shade=True, linewidth=0, antialiased=True)

        if show_colorbar:
            norm = Normalize(vmin=-K_abs_max, vmax=K_abs_max)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            self.colorbar = self.fig.colorbar(sm, ax=self.ax, shrink=0.6, aspect=20,
                                             label=f'{curvature_type.capitalize()} Curvature')

    def draw_surface_normals(
        self,
        surface: 'Surface',
        u_range: Tuple[float, float] = (0.1, np.pi - 0.1),
        v_range: Tuple[float, float] = (0, 2 * np.pi),
        nu: int = 8,
        nv: int = 12,
        scale: float = 0.3,
        color: str = 'blue',
        alpha: float = 0.8
    ):
        """
        Draw surface normal vectors.

        Args:
            surface: Surface object
            u_range: Parameter u range
            v_range: Parameter v range
            nu: Number of u samples
            nv: Number of v samples
            scale: Normal vector length
            color: Vector color
            alpha: Transparency
        """
        u = np.linspace(u_range[0], u_range[1], nu)
        v = np.linspace(v_range[0], v_range[1], nv)

        for ui in u:
            for vi in v:
                pos = surface.position(ui, vi)
                n = surface.normal(ui, vi)

                self.ax.quiver(
                    pos.x, pos.y, pos.z,
                    n.x * scale, n.y * scale, n.z * scale,
                    color=color, alpha=alpha, arrow_length_ratio=0.2
                )

    def draw_surface_frames(
        self,
        surface: 'Surface',
        u_range: Tuple[float, float] = (0.1, np.pi - 0.1),
        v_range: Tuple[float, float] = (0, 2 * np.pi),
        nu: int = 6,
        nv: int = 8,
        scale: float = 0.25,
        linewidth: float = 1.5,
        alpha: float = 0.8
    ):
        """
        Draw frame field on surface.

        Args:
            surface: Surface object
            u_range: Parameter u range
            v_range: Parameter v range
            nu: Number of u samples
            nv: Number of v samples
            scale: Frame axis length
            linewidth: Line width
            alpha: Transparency
        """
        u = np.linspace(u_range[0], u_range[1], nu)
        v = np.linspace(v_range[0], v_range[1], nv)

        for ui in u:
            for vi in v:
                pos = surface.position(ui, vi)
                r_u = surface.tangent_u(ui, vi)
                r_v = surface.tangent_v(ui, vi)
                n = surface.normal(ui, vi)

                # Normalize
                r_u_norm = (r_u.x**2 + r_u.y**2 + r_u.z**2) ** 0.5
                r_v_norm = (r_v.x**2 + r_v.y**2 + r_v.z**2) ** 0.5

                if r_u_norm > 1e-10:
                    r_u = r_u * (1.0 / r_u_norm)
                if r_v_norm > 1e-10:
                    r_v = r_v * (1.0 / r_v_norm)

                # Draw frame (red=u, green=v, blue=normal)
                self.ax.quiver(pos.x, pos.y, pos.z,
                              r_u.x * scale, r_u.y * scale, r_u.z * scale,
                              color='red', linewidth=linewidth, alpha=alpha,
                              arrow_length_ratio=0.15)
                self.ax.quiver(pos.x, pos.y, pos.z,
                              r_v.x * scale, r_v.y * scale, r_v.z * scale,
                              color='green', linewidth=linewidth, alpha=alpha,
                              arrow_length_ratio=0.15)
                self.ax.quiver(pos.x, pos.y, pos.z,
                              n.x * scale, n.y * scale, n.z * scale,
                              color='blue', linewidth=linewidth, alpha=alpha,
                              arrow_length_ratio=0.15)


# ============================================================
# Curve Visualizer
# ============================================================

class CurveVisualizer(CoordinateSystemVisualizer):
    """
    Curve visualization with Frenet frame support.

    Features:
    - Curve path rendering
    - Tangent, normal, binormal vectors
    - Frenet frame field
    - Animation support
    """

    def __init__(self, figsize: Tuple[int, int] = (12, 9), dpi: int = 100):
        super().__init__(figsize, dpi)

    def draw_curve_vertices(
        self,
        points: List[vec3],
        color: str = 'black',
        linewidth: float = 2.0,
        marker: str = '',
        markersize: float = 4,
        alpha: float = 0.9,
        label: str = "Curve"
    ):
        """
        Draw curve through vertices.

        Args:
            points: Vertex list
            color: Line color
            linewidth: Line width
            marker: Marker style (empty for no markers)
            markersize: Marker size
            alpha: Transparency
            label: Legend label
        """
        if not points:
            return

        x = [p.x for p in points]
        y = [p.y for p in points]
        z = [p.z for p in points]

        self.ax.plot(x, y, z, color=color, linewidth=linewidth,
                    marker=marker, markersize=markersize,
                    alpha=alpha, label=label)

    def draw_tangents(
        self,
        points: List[vec3],
        tangents: List[vec3],
        scale: float = 0.5,
        color: str = 'red',
        linewidth: float = 1.5,
        alpha: float = 0.8
    ):
        """
        Draw tangent vectors.

        Args:
            points: Curve points
            tangents: Tangent vectors
            scale: Vector length scale
            color: Vector color
            linewidth: Line width
            alpha: Transparency
        """
        for point, tangent in zip(points, tangents):
            self.ax.quiver(
                point.x, point.y, point.z,
                tangent.x * scale, tangent.y * scale, tangent.z * scale,
                color=color, linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.2
            )

    def draw_normals(
        self,
        points: List[vec3],
        normals: List[vec3],
        scale: float = 0.5,
        color: str = 'green',
        linewidth: float = 1.5,
        alpha: float = 0.8
    ):
        """
        Draw normal vectors.

        Args:
            points: Curve points
            normals: Normal vectors
            scale: Vector length scale
            color: Vector color
            linewidth: Line width
            alpha: Transparency
        """
        for point, normal in zip(points, normals):
            self.ax.quiver(
                point.x, point.y, point.z,
                normal.x * scale, normal.y * scale, normal.z * scale,
                color=color, linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.2
            )

    def draw_binormals(
        self,
        points: List[vec3],
        binormals: List[vec3],
        scale: float = 0.5,
        color: str = 'blue',
        linewidth: float = 1.5,
        alpha: float = 0.8
    ):
        """
        Draw binormal vectors.

        Args:
            points: Curve points
            binormals: Binormal vectors
            scale: Vector length scale
            color: Vector color
            linewidth: Line width
            alpha: Transparency
        """
        for point, binormal in zip(points, binormals):
            self.ax.quiver(
                point.x, point.y, point.z,
                binormal.x * scale, binormal.y * scale, binormal.z * scale,
                color=color, linewidth=linewidth, alpha=alpha,
                arrow_length_ratio=0.2
            )

    def draw_curve_frames(
        self,
        frames: List[coord3],
        scale: float = 0.3,
        linewidth: float = 1.5,
        alpha: float = 0.7,
        skip: int = 1
    ):
        """
        Draw Frenet frames along curve.

        Args:
            frames: List of coord3 frames
            scale: Axis length
            linewidth: Line width
            alpha: Transparency
            skip: Draw every nth frame
        """
        for i, frame in enumerate(frames):
            if i % skip == 0:
                self.draw_coord_system(frame, scale=scale,
                                      linewidth=linewidth, alpha=alpha)

    def draw_complete_curve(
        self,
        points: List[vec3],
        tangents: Optional[List[vec3]] = None,
        normals: Optional[List[vec3]] = None,
        binormals: Optional[List[vec3]] = None,
        frames: Optional[List[coord3]] = None,
        curve_color: str = 'black',
        tangent_scale: float = 0.5,
        normal_scale: float = 0.5,
        binormal_scale: float = 0.5,
        frame_scale: float = 0.3,
        frame_skip: int = 5,
        show_world_coord: bool = True
    ):
        """
        Draw complete curve with geometric properties.

        Args:
            points: Curve vertices
            tangents: Tangent vectors (optional)
            normals: Normal vectors (optional)
            binormals: Binormal vectors (optional)
            frames: Frenet frames (optional, overrides individual vectors)
            curve_color: Curve color
            tangent_scale: Tangent vector scale
            normal_scale: Normal vector scale
            binormal_scale: Binormal vector scale
            frame_scale: Frame axis length
            frame_skip: Frame drawing interval
            show_world_coord: Show world coordinate system
        """
        if show_world_coord:
            self.draw_world_coord(scale=1.0)

        self.draw_curve_vertices(points, color=curve_color, label="Curve")

        if frames is not None:
            # Use complete Frenet frames (RGB coloring)
            self.draw_curve_frames(frames, scale=frame_scale, skip=frame_skip)
        else:
            # Draw individual vectors
            if tangents is not None:
                self.draw_tangents(points, tangents, scale=tangent_scale)
            if normals is not None:
                self.draw_normals(points, normals, scale=normal_scale)
            if binormals is not None:
                self.draw_binormals(points, binormals, scale=binormal_scale)

        self.set_equal_aspect()


# ============================================================
# Parametric Curve
# ============================================================

class ParametricCurve:
    """
    Parametric curve with Frenet frame computation.

    Provides:
    - Position r(t)
    - Tangent T(t)
    - Normal N(t)
    - Binormal B(t)
    - Frenet frame {T, N, B}
    - Curvature and torsion
    """

    def __init__(
        self,
        position_func: Callable[[float], vec3],
        t_range: Tuple[float, float] = (0, 1),
        num_points: int = 100
    ):
        """
        Initialize parametric curve.

        Args:
            position_func: Position function r(t) -> vec3
            t_range: Parameter range (t_min, t_max)
            num_points: Number of sample points
        """
        self.position_func = position_func
        self.t_range = t_range
        self.num_points = num_points
        self.h = 1e-6  # Numerical differentiation step

    def position(self, t: float) -> vec3:
        """Compute position at parameter t."""
        return self.position_func(t)

    def tangent(self, t: float, normalized: bool = True) -> vec3:
        """
        Compute tangent vector T = dr/dt.

        Args:
            t: Parameter value
            normalized: Normalize to unit vector
        """
        r_plus = self.position_func(t + self.h)
        r_minus = self.position_func(t - self.h)
        tangent = (r_plus - r_minus) * (1.0 / (2.0 * self.h))

        if normalized:
            length = (tangent.x**2 + tangent.y**2 + tangent.z**2) ** 0.5
            if length > 1e-10:
                tangent = tangent * (1.0 / length)

        return tangent

    def second_derivative(self, t: float) -> vec3:
        """Compute second derivative d^2r/dt^2."""
        r_plus = self.position_func(t + self.h)
        r_center = self.position_func(t)
        r_minus = self.position_func(t - self.h)
        return (r_plus + r_minus - r_center * 2.0) * (1.0 / (self.h * self.h))

    def normal(self, t: float, normalized: bool = True) -> vec3:
        """
        Compute principal normal N = dT/ds / |dT/ds|.

        Args:
            t: Parameter value
            normalized: Normalize to unit vector
        """
        T_plus = self.tangent(t + self.h, normalized=True)
        T_minus = self.tangent(t - self.h, normalized=True)
        dT_dt = (T_plus - T_minus) * (1.0 / (2.0 * self.h))

        length = (dT_dt.x**2 + dT_dt.y**2 + dT_dt.z**2) ** 0.5

        if length > 1e-10:
            N = dT_dt * (1.0 / length) if normalized else dT_dt
        else:
            N = vec3(0, 0, 1)

        return N

    def binormal(self, t: float, normalized: bool = True) -> vec3:
        """
        Compute binormal B = T x N.

        Args:
            t: Parameter value
            normalized: Normalize to unit vector
        """
        T = self.tangent(t, normalized=True)
        N = self.normal(t, normalized=True)
        B = T.cross(N)

        if normalized:
            length = (B.x**2 + B.y**2 + B.z**2) ** 0.5
            if length > 1e-10:
                B = B * (1.0 / length)

        return B

    def curvature(self, t: float) -> float:
        """
        Compute curvature kappa = |dT/ds|.

        Args:
            t: Parameter value

        Returns:
            Curvature value
        """
        T_plus = self.tangent(t + self.h, normalized=True)
        T_minus = self.tangent(t - self.h, normalized=True)
        dT_dt = (T_plus - T_minus) * (1.0 / (2.0 * self.h))

        # Get speed |dr/dt|
        dr_dt = (self.position_func(t + self.h) - self.position_func(t - self.h)) * (1.0 / (2.0 * self.h))
        speed = (dr_dt.x**2 + dr_dt.y**2 + dr_dt.z**2) ** 0.5

        if speed > 1e-10:
            kappa = (dT_dt.x**2 + dT_dt.y**2 + dT_dt.z**2) ** 0.5 / speed
        else:
            kappa = 0.0

        return kappa

    def frenet_frame(self, t: float) -> coord3:
        """
        Compute Frenet frame {T, N, B}.

        Returns coord3 with:
        - o: Position
        - ux: Tangent T (red)
        - uy: Normal N (green)
        - uz: Binormal B (blue)
        """
        frame = coord3()
        frame.o = self.position(t)
        frame.ux = self.tangent(t, normalized=True)
        frame.uy = self.normal(t, normalized=True)
        frame.uz = self.binormal(t, normalized=True)
        return frame

    def sample_points(self) -> List[vec3]:
        """Sample curve positions."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.position(t) for t in t_values]

    def sample_tangents(self) -> List[vec3]:
        """Sample tangent vectors."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.tangent(t) for t in t_values]

    def sample_normals(self) -> List[vec3]:
        """Sample normal vectors."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.normal(t) for t in t_values]

    def sample_binormals(self) -> List[vec3]:
        """Sample binormal vectors."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.binormal(t) for t in t_values]

    def sample_frames(self) -> List[coord3]:
        """Sample Frenet frames."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.frenet_frame(t) for t in t_values]

    def sample_curvature(self) -> List[float]:
        """Sample curvature values."""
        t_min, t_max = self.t_range
        t_values = np.linspace(t_min, t_max, self.num_points)
        return [self.curvature(t) for t in t_values]


# ============================================================
# Convenience Functions
# ============================================================

def visualize_coord_system(
    coord: coord3,
    scale: float = 1.0,
    figsize: Tuple[int, int] = (10, 8),
    show: bool = True,
    save_path: Optional[str] = None,
    title: str = "Coordinate System"
):
    """
    Quick visualization of a single coordinate frame.

    Args:
        coord: Coordinate frame
        scale: Axis length
        figsize: Figure size
        show: Display figure
        save_path: Save path (optional)
        title: Plot title
    """
    vis = CoordinateSystemVisualizer(figsize=figsize)
    vis.draw_world_coord(scale=scale * 0.8)
    vis.draw_coord_system(coord, scale=scale, label_prefix="Frame-")
    vis.set_equal_aspect()
    vis.set_title(title)

    if save_path:
        vis.save(save_path)
    if show:
        vis.show()


def visualize_curve(
    curve: ParametricCurve,
    show_tangents: bool = False,
    show_normals: bool = False,
    show_binormals: bool = False,
    show_frames: bool = True,
    frame_skip: int = 5,
    figsize: Tuple[int, int] = (12, 9),
    show: bool = True,
    save_path: Optional[str] = None,
    title: str = "Parametric Curve"
):
    """
    Quick visualization of a parametric curve.

    Args:
        curve: Parametric curve object
        show_tangents: Show tangent vectors
        show_normals: Show normal vectors
        show_binormals: Show binormal vectors
        show_frames: Show complete Frenet frames
        frame_skip: Frame drawing interval
        figsize: Figure size
        show: Display figure
        save_path: Save path (optional)
        title: Plot title
    """
    vis = CurveVisualizer(figsize=figsize)

    points = curve.sample_points()
    tangents = curve.sample_tangents() if show_tangents and not show_frames else None
    normals = curve.sample_normals() if show_normals and not show_frames else None
    binormals = curve.sample_binormals() if show_binormals and not show_frames else None
    frames = curve.sample_frames() if show_frames else None

    vis.draw_complete_curve(
        points=points,
        tangents=tangents,
        normals=normals,
        binormals=binormals,
        frames=frames,
        frame_skip=frame_skip
    )
    vis.set_title(title)

    if save_path:
        vis.save(save_path)
    if show:
        vis.show()


def visualize_surface(
    surface: 'Surface',
    curvature_type: Optional[str] = None,
    show_normals: bool = False,
    show_frames: bool = False,
    u_range: Tuple[float, float] = (0.1, np.pi - 0.1),
    v_range: Tuple[float, float] = (0, 2 * np.pi),
    figsize: Tuple[int, int] = (14, 10),
    show: bool = True,
    save_path: Optional[str] = None,
    title: str = "Surface"
):
    """
    Quick visualization of a parametric surface.

    Args:
        surface: Surface object
        curvature_type: 'gaussian' or 'mean' for curvature coloring (None for plain)
        show_normals: Show normal vectors
        show_frames: Show frame field
        u_range: Parameter u range
        v_range: Parameter v range
        figsize: Figure size
        show: Display figure
        save_path: Save path (optional)
        title: Plot title
    """
    vis = SurfaceVisualizer(figsize=figsize)

    if curvature_type:
        vis.draw_surface_curvature(surface, curvature_type=curvature_type,
                                  u_range=u_range, v_range=v_range)
    else:
        vis.draw_surface(surface, u_range=u_range, v_range=v_range)

    if show_normals:
        vis.draw_surface_normals(surface, u_range=u_range, v_range=v_range)

    if show_frames:
        vis.draw_surface_frames(surface, u_range=u_range, v_range=v_range)

    vis.draw_world_coord(scale=0.5)
    vis.set_equal_aspect()
    vis.set_title(title)

    if save_path:
        vis.save(save_path)
    if show:
        vis.show()


# ============================================================
# Export
# ============================================================

__all__ = [
    # Visualizer classes
    'CoordinateSystemVisualizer',
    'CurveVisualizer',
    'SurfaceVisualizer',

    # Curve class
    'ParametricCurve',

    # Convenience functions
    'visualize_coord_system',
    'visualize_curve',
    'visualize_surface',

    # Utility
    'create_curvature_colormap',
]
