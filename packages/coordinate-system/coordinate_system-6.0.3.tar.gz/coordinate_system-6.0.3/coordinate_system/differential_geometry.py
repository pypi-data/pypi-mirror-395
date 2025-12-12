"""
Differential Geometry Module
============================

Comprehensive discrete differential geometry computations on surfaces,
combining classical methods and intrinsic gradient operator framework.

Key Features:
- Surface parametrization (Sphere, Torus, custom surfaces)
- Metric tensor computation
- Intrinsic gradient operator for curvature calculation
- Classical curvature methods with high-order finite differences
- Gaussian, mean, principal, and Riemann curvatures

Author: Coordinate System Package
Date: 2025-12-03
"""

import math
import numpy as np
from typing import Tuple, Optional, Callable, Union, Dict, List
from .coordinate_system import coord3, vec3


# ============================================================
# High-Order Finite Difference Operators
# ============================================================

def derivative_5pt(f: Callable[[float], np.ndarray], x: float, h: float) -> np.ndarray:
    """
    5-point finite difference formula for first derivative.

    Accuracy: O(h^4)

    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Step size

    Returns:
        First derivative approximation
    """
    return (-f(x + 2*h) + 8*f(x + h) - 8*f(x - h) + f(x - 2*h)) / (12*h)


def derivative_2nd_5pt(f: Callable[[float], np.ndarray], x: float, h: float) -> np.ndarray:
    """
    5-point finite difference formula for second derivative.

    Accuracy: O(h^4)

    Args:
        f: Function to differentiate
        x: Point at which to compute derivative
        h: Step size

    Returns:
        Second derivative approximation
    """
    return (-f(x + 2*h) + 16*f(x + h) - 30*f(x) + 16*f(x - h) - f(x - 2*h)) / (12*h*h)


def richardson_extrapolation(f_h: float, f_2h: float, order: int = 4) -> float:
    """
    Richardson extrapolation for accelerating convergence.

    Args:
        f_h: Value computed with step size h
        f_2h: Value computed with step size 2h
        order: Order of the method

    Returns:
        Extrapolated value with improved accuracy
    """
    return (2**order * f_h - f_2h) / (2**order - 1)


# ============================================================
# Surface Base Class and Common Surfaces
# ============================================================

class Surface:
    """
    Base class for parametric surfaces r(u, v).

    Subclasses must implement the position(u, v) method.
    """

    def __init__(self, h: float = 1e-6):
        """
        Initialize surface.

        Args:
            h: Step size for numerical differentiation
        """
        self.h = h

    def position(self, u: float, v: float) -> vec3:
        """
        Compute position on surface at parameters (u, v).

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement position(u, v)")

    def tangent_u(self, u: float, v: float) -> vec3:
        """Compute tangent vector in u direction using central difference."""
        r_plus = self.position(u + self.h, v)
        r_minus = self.position(u - self.h, v)
        return (r_plus - r_minus) * (1.0 / (2.0 * self.h))

    def tangent_v(self, u: float, v: float) -> vec3:
        """Compute tangent vector in v direction using central difference."""
        r_plus = self.position(u, v + self.h)
        r_minus = self.position(u, v - self.h)
        return (r_plus - r_minus) * (1.0 / (2.0 * self.h))

    def normal(self, u: float, v: float) -> vec3:
        """Compute unit normal vector."""
        r_u = self.tangent_u(u, v)
        r_v = self.tangent_v(u, v)
        n = r_u.cross(r_v)
        length = (n.x**2 + n.y**2 + n.z**2) ** 0.5
        if length > 1e-10:
            return n * (1.0 / length)
        else:
            return vec3(0.0, 0.0, 1.0)


class Sphere(Surface):
    """
    Sphere surface.

    Parametrization: r(theta, phi) = R(sin(theta)cos(phi), sin(theta)sin(phi), cos(theta))
    where theta in [0, pi] is polar angle, phi in [0, 2*pi] is azimuthal angle.

    Theoretical curvatures:
    - Gaussian curvature: K = 1/R^2
    - Mean curvature: H = 1/R
    """

    def __init__(self, radius: float = 1.0, h: float = 1e-6):
        super().__init__(h)
        self.R = radius

    def position(self, theta: float, phi: float) -> vec3:
        """Position on sphere."""
        x = self.R * math.sin(theta) * math.cos(phi)
        y = self.R * math.sin(theta) * math.sin(phi)
        z = self.R * math.cos(theta)
        return vec3(x, y, z)

    @property
    def theoretical_gaussian_curvature(self) -> float:
        """Theoretical Gaussian curvature K = 1/R^2."""
        return 1.0 / (self.R * self.R)

    @property
    def theoretical_mean_curvature(self) -> float:
        """Theoretical mean curvature H = 1/R."""
        return 1.0 / self.R


class Torus(Surface):
    """
    Torus surface.

    Parametrization: r(u, v) = ((R + r*cos(u))*cos(v), (R + r*cos(u))*sin(v), r*sin(u))
    where R is major radius, r is minor radius.

    Theoretical curvatures:
    - Gaussian curvature: K = cos(u) / (r * (R + r*cos(u)))
    - Mean curvature: H = (R + 2*r*cos(u)) / (2*r*(R + r*cos(u)))
    """

    def __init__(self, major_radius: float = 3.0, minor_radius: float = 1.0, h: float = 1e-6):
        super().__init__(h)
        self.R = major_radius
        self.r = minor_radius

    def position(self, u: float, v: float) -> vec3:
        """Position on torus."""
        x = (self.R + self.r * math.cos(u)) * math.cos(v)
        y = (self.R + self.r * math.cos(u)) * math.sin(v)
        z = self.r * math.sin(u)
        return vec3(x, y, z)

    def theoretical_gaussian_curvature(self, u: float) -> float:
        """Theoretical Gaussian curvature at parameter u."""
        return math.cos(u) / (self.r * (self.R + self.r * math.cos(u)))

    def theoretical_mean_curvature(self, u: float) -> float:
        """Theoretical mean curvature at parameter u."""
        return (self.R + 2 * self.r * math.cos(u)) / (2 * self.r * (self.R + self.r * math.cos(u)))


# ============================================================
# Metric Tensor
# ============================================================

class MetricTensor:
    """
    First fundamental form (metric tensor) of a surface.

    g_ij = <dr/du^i, dr/du^j>

    Components:
    - E = g_11 = <r_u, r_u>
    - F = g_12 = <r_u, r_v>
    - G = g_22 = <r_v, r_v>
    """

    def __init__(self, E: float, F: float, G: float):
        """
        Initialize metric tensor.

        Args:
            E: g_11 = <r_u, r_u>
            F: g_12 = <r_u, r_v>
            G: g_22 = <r_v, r_v>
        """
        self.E = E
        self.F = F
        self.G = G
        self.det = E * G - F * F

    @classmethod
    def from_surface(cls, surface: Surface, u: float, v: float) -> 'MetricTensor':
        """Create metric tensor from surface at point (u, v)."""
        r_u = surface.tangent_u(u, v)
        r_v = surface.tangent_v(u, v)
        E = r_u.dot(r_u)
        F = r_u.dot(r_v)
        G = r_v.dot(r_v)
        return cls(E, F, G)

    def determinant(self) -> float:
        """Get determinant of metric tensor."""
        return self.det

    def inverse(self) -> np.ndarray:
        """Get inverse metric tensor as numpy array."""
        if abs(self.det) < 1e-14:
            return np.eye(2)
        return np.array([[self.G, -self.F], [-self.F, self.E]]) / self.det

    def as_matrix(self) -> np.ndarray:
        """Get metric tensor as numpy array."""
        return np.array([[self.E, self.F], [self.F, self.G]])

    def __repr__(self) -> str:
        return f"MetricTensor(E={self.E:.6f}, F={self.F:.6f}, G={self.G:.6f}, det={self.det:.6f})"


# ============================================================
# Gradient Result
# ============================================================

class GradientResult:
    """
    Gradient result containing normal vector derivative.
    """

    def __init__(self, dn: vec3, direction: str):
        """
        Initialize gradient result.

        Args:
            dn: Normal vector derivative
            direction: Parameter direction ('u' or 'v')
        """
        self.dn = dn
        self.direction = direction

    def __repr__(self) -> str:
        return f"GradientResult({self.direction}: [{self.dn.x:.6f}, {self.dn.y:.6f}, {self.dn.z:.6f}])"


# ============================================================
# Intrinsic Gradient Operator
# ============================================================

class IntrinsicGradientOperator:
    """
    Intrinsic gradient operator implementation.

    Key formula:
        G_mu = (c(u+h) - c(u-h)) / (2h) / c(u)
    Then extract normal derivative using .VZ()
    """

    def __init__(self, surface: Surface, step_size: float = 1e-3):
        self.surface = surface
        self.h = step_size

    def calc_intrinsic_frame(self, u: float, v: float) -> coord3:
        """
        Calculate intrinsic frame at point (u, v).

        For Sphere and Torus, uses analytical expressions.
        For other surfaces, uses numerical derivatives.
        """
        if isinstance(self.surface, Sphere):
            R = self.surface.R
            theta, phi = u, v

            pos = self.surface.position(theta, phi)

            # Analytical tangent vectors
            r_theta = vec3(
                R * math.cos(theta) * math.cos(phi),
                R * math.cos(theta) * math.sin(phi),
                -R * math.sin(theta)
            )
            r_phi = vec3(
                -R * math.sin(theta) * math.sin(phi),
                R * math.sin(theta) * math.cos(phi),
                0
            )

            n = r_theta.cross(r_phi).normalized()
            e1 = r_theta.normalized()
            e2 = r_phi.normalized()

        elif isinstance(self.surface, Torus):
            R = self.surface.R
            r = self.surface.r
            u_param, v_param = u, v

            pos = self.surface.position(u_param, v_param)

            # Analytical tangent vectors
            r_u = vec3(
                -r * math.sin(u_param) * math.cos(v_param),
                -r * math.sin(u_param) * math.sin(v_param),
                r * math.cos(u_param)
            )
            r_v = vec3(
                -(R + r * math.cos(u_param)) * math.sin(v_param),
                (R + r * math.cos(u_param)) * math.cos(v_param),
                0
            )

            n = r_u.cross(r_v).normalized()
            e1 = r_u.normalized()
            e2 = r_v.normalized()

        else:
            # Numerical method for general surfaces
            pos = self.surface.position(u, v)
            r_u = self.surface.tangent_u(u, v)
            r_v = self.surface.tangent_v(u, v)

            n = r_u.cross(r_v).normalized()
            e1 = r_u.normalized()
            e2 = r_v.normalized()

        # Create intrinsic frame
        frame = coord3()
        frame.o = pos
        frame.ux = e1
        frame.uy = e2
        frame.uz = n

        return frame

    def compute_both(self, u: float, v: float) -> Tuple[GradientResult, GradientResult, coord3]:
        """
        Compute gradients in both u and v directions using central differences.

        Returns:
            Tuple of (G_u, G_v, center_frame)
        """
        c_center = self.calc_intrinsic_frame(u, v)

        # u direction: central difference
        c_u_plus = self.calc_intrinsic_frame(u + self.h, v)
        c_u_minus = self.calc_intrinsic_frame(u - self.h, v)
        dn_du = ((c_u_plus - c_u_minus) / (2 * self.h)).VZ()

        # v direction: central difference
        c_v_plus = self.calc_intrinsic_frame(u, v + self.h)
        c_v_minus = self.calc_intrinsic_frame(u, v - self.h)
        dn_dv = ((c_v_plus - c_v_minus) / (2 * self.h)).VZ()

        G_u = GradientResult(dn_du, "u")
        G_v = GradientResult(dn_dv, "v")

        return G_u, G_v, c_center

    def compute_u(self, u: float, v: float) -> GradientResult:
        """Compute gradient in u direction only."""
        c_plus = self.calc_intrinsic_frame(u + self.h, v)
        c_minus = self.calc_intrinsic_frame(u - self.h, v)
        dn = ((c_plus - c_minus) / (2 * self.h)).VZ()
        return GradientResult(dn, "u")

    def compute_v(self, u: float, v: float) -> GradientResult:
        """Compute gradient in v direction only."""
        c_plus = self.calc_intrinsic_frame(u, v + self.h)
        c_minus = self.calc_intrinsic_frame(u, v - self.h)
        dn = ((c_plus - c_minus) / (2 * self.h)).VZ()
        return GradientResult(dn, "v")


# ============================================================
# Intrinsic Gradient Curvature Calculator
# ============================================================

class IntrinsicGradientCurvatureCalculator:
    """
    Curvature calculator using intrinsic gradient method.

    Computes curvatures from the shape operator derived
    from the intrinsic gradient of the normal field.
    """

    def __init__(self, surface: Surface, step_size: float = 1e-3):
        self.surface = surface
        self.h = step_size
        self.grad_op = IntrinsicGradientOperator(surface, step_size)

    def _get_tangent_vectors(self, u: float, v: float) -> Tuple[vec3, vec3]:
        """Get tangent vectors (analytical for known surfaces, numerical otherwise)."""
        if isinstance(self.surface, Sphere):
            R = self.surface.R
            theta, phi = u, v
            r_u = vec3(
                R * math.cos(theta) * math.cos(phi),
                R * math.cos(theta) * math.sin(phi),
                -R * math.sin(theta)
            )
            r_v = vec3(
                -R * math.sin(theta) * math.sin(phi),
                R * math.sin(theta) * math.cos(phi),
                0
            )
        elif isinstance(self.surface, Torus):
            R = self.surface.R
            r = self.surface.r
            r_u = vec3(
                -r * math.sin(u) * math.cos(v),
                -r * math.sin(u) * math.sin(v),
                r * math.cos(u)
            )
            r_v = vec3(
                -(R + r * math.cos(u)) * math.sin(v),
                (R + r * math.cos(u)) * math.cos(v),
                0
            )
        else:
            r_u = self.surface.tangent_u(u, v)
            r_v = self.surface.tangent_v(u, v)

        return r_u, r_v

    def compute_gaussian_curvature(self, u: float, v: float) -> float:
        """
        Compute Gaussian curvature K = det(II) / det(I).
        """
        G_u, G_v, _ = self.grad_op.compute_both(u, v)
        r_u, r_v = self._get_tangent_vectors(u, v)

        dn_du = G_u.dn
        dn_dv = G_v.dn

        # First fundamental form
        E = r_u.dot(r_u)
        F = r_u.dot(r_v)
        G = r_v.dot(r_v)
        metric_det = E * G - F * F

        # Second fundamental form
        L = -dn_du.dot(r_u)
        M1 = -dn_du.dot(r_v)
        M2 = -dn_dv.dot(r_u)
        N = -dn_dv.dot(r_v)
        M = (M1 + M2) / 2.0

        # Gaussian curvature
        if abs(metric_det) > 1e-14:
            K = (L * N - M * M) / metric_det
        else:
            K = 0.0

        return K

    def compute_mean_curvature(self, u: float, v: float) -> float:
        """
        Compute mean curvature H = (EN - 2FM + GL) / (2*det(I)).
        """
        G_u, G_v, _ = self.grad_op.compute_both(u, v)
        r_u, r_v = self._get_tangent_vectors(u, v)

        dn_du = G_u.dn
        dn_dv = G_v.dn

        E = r_u.dot(r_u)
        F = r_u.dot(r_v)
        G = r_v.dot(r_v)
        metric_det = E * G - F * F

        L = -dn_du.dot(r_u)
        M1 = -dn_du.dot(r_v)
        M2 = -dn_dv.dot(r_u)
        N = -dn_dv.dot(r_v)
        M = (M1 + M2) / 2.0

        if abs(metric_det) > 1e-14:
            H = (G * L - 2 * F * M + E * N) / (2 * metric_det)
        else:
            H = 0.0

        return H

    def compute_riemann_curvature(self, u: float, v: float) -> float:
        """
        Compute Riemann curvature tensor component R^1_212.

        For 2D surfaces: R^1_212 = K * det(g) = LN - M^2
        """
        G_u, G_v, _ = self.grad_op.compute_both(u, v)
        r_u, r_v = self._get_tangent_vectors(u, v)

        dn_du = G_u.dn
        dn_dv = G_v.dn

        L = -dn_du.dot(r_u)
        M = -dn_du.dot(r_v)
        N = -dn_dv.dot(r_v)

        R_1212 = L * N - M * M
        return R_1212

    def compute_principal_curvatures(self, u: float, v: float) -> Tuple[float, float]:
        """
        Compute principal curvatures k1 and k2.

        Uses: k1,k2 = H +/- sqrt(H^2 - K)
        """
        K = self.compute_gaussian_curvature(u, v)
        H = self.compute_mean_curvature(u, v)

        discriminant = max(0, H * H - K)
        sqrt_disc = discriminant ** 0.5

        k1 = H + sqrt_disc
        k2 = H - sqrt_disc

        return k1, k2

    def compute_all_curvatures(self, u: float, v: float) -> Dict[str, Union[float, Tuple[float, float]]]:
        """
        Compute all curvature quantities at once.
        """
        K = self.compute_gaussian_curvature(u, v)
        H = self.compute_mean_curvature(u, v)

        discriminant = max(0, H * H - K)
        sqrt_disc = discriminant ** 0.5
        k1 = H + sqrt_disc
        k2 = H - sqrt_disc

        return {
            'gaussian_curvature': K,
            'mean_curvature': H,
            'principal_curvatures': (k1, k2)
        }


# ============================================================
# Classical Curvature Calculator
# ============================================================

class CurvatureCalculator:
    """
    High-precision discrete curvature calculator using classical differential geometry.

    Uses high-order finite differences for computing derivatives
    and fundamental forms.
    """

    def __init__(self, surface: Surface, step_size: float = 1e-3):
        self.surface = surface
        self.h = step_size

    def _position_array(self, u: float, v: float) -> np.ndarray:
        """Convert vec3 position to numpy array."""
        pos = self.surface.position(u, v)
        return np.array([pos.x, pos.y, pos.z])

    def _compute_derivatives(self, u: float, v: float) -> Dict[str, np.ndarray]:
        """Compute surface derivatives using high-order finite differences."""
        effective_h = max(self.h, 1e-6)

        r_u = derivative_5pt(lambda uu: self._position_array(uu, v), u, effective_h)
        r_v = derivative_5pt(lambda vv: self._position_array(u, vv), v, effective_h)

        r_uu = derivative_2nd_5pt(lambda uu: self._position_array(uu, v), u, effective_h)
        r_vv = derivative_2nd_5pt(lambda vv: self._position_array(u, vv), v, effective_h)
        r_uv = derivative_5pt(
            lambda vv: derivative_5pt(
                lambda uu: self._position_array(uu, vv), u, effective_h
            ), v, effective_h
        )

        return {
            'r_u': r_u, 'r_v': r_v,
            'r_uu': r_uu, 'r_vv': r_vv, 'r_uv': r_uv
        }

    def compute_fundamental_forms(self, u: float, v: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute first and second fundamental forms.

        Returns:
            (g, h, n): First form, second form, normal vector
        """
        derivs = self._compute_derivatives(u, v)
        r_u = derivs['r_u']
        r_v = derivs['r_v']
        r_uu = derivs['r_uu']
        r_vv = derivs['r_vv']
        r_uv = derivs['r_uv']

        # First fundamental form
        E = np.dot(r_u, r_u)
        F = np.dot(r_u, r_v)
        G = np.dot(r_v, r_v)
        g = np.array([[E, F], [F, G]])

        # Normal vector
        n_vec = np.cross(r_u, r_v)
        n_norm = np.linalg.norm(n_vec)
        if n_norm > 1e-14:
            n = n_vec / n_norm
        else:
            n = np.array([0., 0., 1.])

        # Second fundamental form
        L = np.dot(r_uu, n)
        M = np.dot(r_uv, n)
        N = np.dot(r_vv, n)
        h = np.array([[L, M], [M, N]])

        return g, h, n

    def compute_gaussian_curvature(self, u: float, v: float) -> float:
        """Compute Gaussian curvature K = det(II) / det(I)."""
        g, h, _ = self.compute_fundamental_forms(u, v)

        det_g = np.linalg.det(g)
        det_h = np.linalg.det(h)

        if abs(det_g) < 1e-14:
            return 0.0

        return det_h / det_g

    def compute_mean_curvature(self, u: float, v: float) -> float:
        """Compute mean curvature H."""
        g, h, _ = self.compute_fundamental_forms(u, v)

        det_g = np.linalg.det(g)
        if abs(det_g) < 1e-14:
            return 0.0

        trace_term = g[1, 1] * h[0, 0] - 2 * g[0, 1] * h[0, 1] + g[0, 0] * h[1, 1]
        H = trace_term / (2 * det_g)

        return abs(H)

    def compute_principal_curvatures(self, u: float, v: float) -> Tuple[float, float, np.ndarray, np.ndarray]:
        """
        Compute principal curvatures and principal directions.

        Returns:
            (k1, k2, dir1, dir2): Principal curvatures and directions
        """
        g, h, _ = self.compute_fundamental_forms(u, v)
        derivs = self._compute_derivatives(u, v)
        r_u = derivs['r_u']
        r_v = derivs['r_v']

        det_g = np.linalg.det(g)
        if abs(det_g) < 1e-14:
            return 0.0, 0.0, np.array([1., 0., 0.]), np.array([0., 1., 0.])

        # Shape operator S = g^{-1} h
        g_inv = np.linalg.inv(g)
        S = g_inv @ h

        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eig(S)
        k1, k2 = eigenvalues.real

        # Ensure k1 >= k2 by absolute value
        if abs(k1) < abs(k2):
            k1, k2 = k2, k1
            eigenvectors = eigenvectors[:, [1, 0]]

        # Convert to 3D directions
        dir1_2d = eigenvectors[:, 0]
        dir2_2d = eigenvectors[:, 1]

        dir1_3d = dir1_2d[0] * r_u + dir1_2d[1] * r_v
        dir2_3d = dir2_2d[0] * r_u + dir2_2d[1] * r_v

        dir1_3d = dir1_3d / (np.linalg.norm(dir1_3d) + 1e-14)
        dir2_3d = dir2_3d / (np.linalg.norm(dir2_3d) + 1e-14)

        return k1, k2, dir1_3d, dir2_3d

    def compute_all_curvatures(self, u: float, v: float) -> Dict[str, Union[float, np.ndarray]]:
        """Compute all curvature quantities at once."""
        g, h, n = self.compute_fundamental_forms(u, v)
        K = self.compute_gaussian_curvature(u, v)
        H = self.compute_mean_curvature(u, v)
        k1, k2, dir1, dir2 = self.compute_principal_curvatures(u, v)

        return {
            'K': K,
            'H': H,
            'k1': k1,
            'k2': k2,
            'dir1': dir1,
            'dir2': dir2,
            'g': g,
            'h': h,
            'n': n
        }


# ============================================================
# Convenience Functions - Intrinsic Gradient Method (Default)
# ============================================================

def compute_gaussian_curvature(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """
    Compute Gaussian curvature using intrinsic gradient method.
    """
    calc = IntrinsicGradientCurvatureCalculator(surface, step_size)
    return calc.compute_gaussian_curvature(u, v)


def compute_mean_curvature(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """
    Compute mean curvature using intrinsic gradient method.
    """
    calc = IntrinsicGradientCurvatureCalculator(surface, step_size)
    return calc.compute_mean_curvature(u, v)


def compute_riemann_curvature(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """
    Compute Riemann curvature tensor component R^1_212.
    """
    calc = IntrinsicGradientCurvatureCalculator(surface, step_size)
    return calc.compute_riemann_curvature(u, v)


def compute_all_curvatures(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Dict[str, Union[float, Tuple[float, float]]]:
    """
    Compute all curvature quantities using intrinsic gradient method.
    """
    calc = IntrinsicGradientCurvatureCalculator(surface, step_size)
    return calc.compute_all_curvatures(u, v)


def compute_intrinsic_gradient(
    surface: Surface,
    u: float,
    v: float,
    direction: str = 'u',
    step_size: float = 1e-3
) -> GradientResult:
    """
    Compute intrinsic gradient in specified direction.

    Args:
        surface: Surface object
        u, v: Parameter values
        direction: 'u' or 'v'
        step_size: Step size

    Returns:
        GradientResult object
    """
    grad_op = IntrinsicGradientOperator(surface, step_size)

    if direction == 'u':
        return grad_op.compute_u(u, v)
    elif direction == 'v':
        return grad_op.compute_v(u, v)
    else:
        raise ValueError(f"direction must be 'u' or 'v', got: {direction}")


# ============================================================
# Convenience Functions - Classical Method
# ============================================================

def gaussian_curvature_classical(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """Compute Gaussian curvature using classical method."""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_gaussian_curvature(u, v)


def mean_curvature_classical(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """Compute mean curvature using classical method."""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_mean_curvature(u, v)


def principal_curvatures_classical(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Tuple[float, float]:
    """Compute principal curvatures using classical method."""
    calc = CurvatureCalculator(surface, step_size)
    k1, k2, _, _ = calc.compute_principal_curvatures(u, v)
    return k1, k2


def all_curvatures_classical(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Dict[str, Union[float, np.ndarray]]:
    """Compute all curvature quantities using classical method."""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_all_curvatures(u, v)


# ============================================================
# Backward Compatibility Aliases
# ============================================================

def gaussian_curvature(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """Compute Gaussian curvature (default: intrinsic gradient method)."""
    return compute_gaussian_curvature(surface, u, v, step_size)


def mean_curvature(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> float:
    """Compute mean curvature (default: intrinsic gradient method)."""
    return compute_mean_curvature(surface, u, v, step_size)


def principal_curvatures(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Tuple[float, float]:
    """Compute principal curvatures (default: intrinsic gradient method)."""
    calc = IntrinsicGradientCurvatureCalculator(surface, step_size)
    return calc.compute_principal_curvatures(u, v)


def all_curvatures(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Dict[str, Union[float, Tuple[float, float]]]:
    """Compute all curvature quantities (default: intrinsic gradient method)."""
    return compute_all_curvatures(surface, u, v, step_size)


# ============================================================
# Method Comparison
# ============================================================

def compare_methods(
    surface: Surface,
    u: float,
    v: float,
    step_size: float = 1e-3
) -> Dict[str, float]:
    """
    Compare classical and intrinsic gradient curvature methods.

    Returns:
        Dictionary with curvature values from both methods and error metrics
    """
    K_classical = gaussian_curvature_classical(surface, u, v, step_size)
    K_intrinsic = compute_gaussian_curvature(surface, u, v, step_size)

    difference = abs(K_classical - K_intrinsic)
    relative_error = difference / abs(K_classical) if abs(K_classical) > 1e-14 else 0.0

    return {
        'K_classical': K_classical,
        'K_intrinsic': K_intrinsic,
        'difference': difference,
        'relative_error': relative_error
    }


# ============================================================
# Export
# ============================================================

__all__ = [
    # Surface classes
    'Surface',
    'Sphere',
    'Torus',

    # Core classes
    'MetricTensor',
    'GradientResult',
    'IntrinsicGradientOperator',
    'IntrinsicGradientCurvatureCalculator',
    'CurvatureCalculator',

    # Intrinsic gradient method functions (default)
    'compute_gaussian_curvature',
    'compute_mean_curvature',
    'compute_riemann_curvature',
    'compute_all_curvatures',
    'compute_intrinsic_gradient',

    # Classical method functions
    'gaussian_curvature_classical',
    'mean_curvature_classical',
    'principal_curvatures_classical',
    'all_curvatures_classical',

    # Backward compatibility aliases
    'gaussian_curvature',
    'mean_curvature',
    'principal_curvatures',
    'all_curvatures',

    # Method comparison
    'compare_methods',

    # Utility functions
    'derivative_5pt',
    'derivative_2nd_5pt',
    'richardson_extrapolation',
]
