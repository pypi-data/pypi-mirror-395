"""
High-Precision Discrete Curvature Computation Module
====================================================

This module provides optimized discrete curvature computation methods
based on traditional differential geometry with high-order finite differences.

Author: PanGuoJun
Date: 2025-10-31
"""

import numpy as np
from typing import Tuple, Optional, Dict, List, Callable, Union
from .differential_geometry import (
    Surface, MetricTensor, IntrinsicGradientOperator, IntrinsicGradientCurvatureCalculator,
    compute_gaussian_curvature, compute_mean_curvature, compute_all_curvatures
)
from .coordinate_system import coord3, vec3


# ========== High-Order Finite Difference Operators ==========

def derivative_5pt(f: Callable[[float], np.ndarray], x: float, h: float) -> np.ndarray:
    """
    5-point finite difference formula for first derivative
    """
    return (-f(x + 2*h) + 8*f(x + h) - 8*f(x - h) + f(x - 2*h)) / (12*h)


def derivative_2nd_5pt(f: Callable[[float], np.ndarray], x: float, h: float) -> np.ndarray:
    """
    5-point finite difference formula for second derivative
    """
    return (-f(x + 2*h) + 16*f(x + h) - 30*f(x) + 16*f(x - h) - f(x - 2*h)) / (12*h*h)


def richardson_extrapolation(f_h: float, f_2h: float, order: int = 4) -> float:
    """
    Richardson extrapolation for accelerating convergence
    """
    return (2**order * f_h - f_2h) / (2**order - 1)


# ========== Curvature Computation Class ==========

class CurvatureCalculator:
    """
    High-precision discrete curvature calculator using classical differential geometry
    """

    def __init__(self, surface: Surface, step_size: float = 1e-3):
        self.surface = surface
        self.h = step_size

    def _compute_derivatives(self, u: float, v: float) -> Dict[str, np.ndarray]:
        """使用更稳定的数值导数"""
        # 避免过小的步长
        effective_h = max(self.h, 1e-6)
        
        # 使用中心差分
        r_u = derivative_5pt(lambda uu: self._position_array(uu, v), u, effective_h)
        r_v = derivative_5pt(lambda vv: self._position_array(u, vv), v, effective_h)
        
        # 二阶导数也使用合适的步长
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

    def _position_array(self, u: float, v: float) -> np.ndarray:
        """Convert vec3 position to numpy array"""
        pos = self.surface.position(u, v)
        return np.array([pos.x, pos.y, pos.z])

    def compute_fundamental_forms(self, u: float, v: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute first and second fundamental forms
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
        """
        Compute Gaussian curvature K at a point
        """
        g, h, _ = self.compute_fundamental_forms(u, v)

        det_g = np.linalg.det(g)
        det_h = np.linalg.det(h)

        if abs(det_g) < 1e-14:
            return 0.0

        return det_h / det_g

    def compute_mean_curvature(self, u: float, v: float) -> float:
        """
        Compute mean curvature H at a point
        """
        g, h, _ = self.compute_fundamental_forms(u, v)

        det_g = np.linalg.det(g)
        if abs(det_g) < 1e-14:
            return 0.0

        trace_term = g[1,1]*h[0,0] - 2*g[0,1]*h[0,1] + g[0,0]*h[1,1]
        H = trace_term / (2 * det_g)
        
        # 对于凸曲面，平均曲率应该是正的
        return abs(H)

    def compute_principal_curvatures(self, u: float, v: float) -> Tuple[float, float, np.ndarray, np.ndarray]:
        """
        Compute principal curvatures and principal directions
        """
        g, h, _ = self.compute_fundamental_forms(u, v)
        derivs = self._compute_derivatives(u, v)
        r_u = derivs['r_u']
        r_v = derivs['r_v']

        det_g = np.linalg.det(g)
        if abs(det_g) < 1e-14:
            return 0.0, 0.0, np.array([1., 0., 0.]), np.array([0., 1., 0.])

        # Shape operator S = g⁻¹h
        g_inv = np.linalg.inv(g)
        S = g_inv @ h

        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eig(S)
        k1, k2 = eigenvalues.real

        # Ensure k1 >= k2 (by absolute value)
        if abs(k1) < abs(k2):
            k1, k2 = k2, k1
            eigenvectors = eigenvectors[:, [1, 0]]

        # Convert tangent plane coordinates to 3D directions
        dir1_2d = eigenvectors[:, 0]
        dir2_2d = eigenvectors[:, 1]

        dir1_3d = dir1_2d[0] * r_u + dir1_2d[1] * r_v
        dir2_3d = dir2_2d[0] * r_u + dir2_2d[1] * r_v

        # Normalize
        dir1_3d = dir1_3d / (np.linalg.norm(dir1_3d) + 1e-14)
        dir2_3d = dir2_3d / (np.linalg.norm(dir2_3d) + 1e-14)

        return k1, k2, dir1_3d, dir2_3d

    def compute_all_curvatures(self, u: float, v: float) -> Dict[str, Union[float, np.ndarray]]:
        """
        Compute all curvature quantities at once
        """
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


# ========== Simplified Interface Functions ==========

def gaussian_curvature_classical(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> float:
    """Compute Gaussian curvature using classical method"""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_gaussian_curvature(u, v)

def mean_curvature_classical(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> float:
    """Compute mean curvature using classical method"""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_mean_curvature(u, v)

def principal_curvatures_classical(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> Tuple[float, float]:
    """Compute principal curvatures using classical method"""
    calc = CurvatureCalculator(surface, step_size)
    k1, k2, _, _ = calc.compute_principal_curvatures(u, v)
    return k1, k2

def all_curvatures_classical(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> Dict[str, Union[float, np.ndarray]]:
    """Compute all curvature quantities using classical method"""
    calc = CurvatureCalculator(surface, step_size)
    return calc.compute_all_curvatures(u, v)


# ========== Intrinsic Gradient Method Functions ==========

def intrinsic_gradient_gaussian_curvature(surface, u, v, step_size=1e-3):
    """Compute Gaussian curvature using intrinsic gradient method"""
    return compute_gaussian_curvature(surface, u, v, step_size)

def intrinsic_gradient_mean_curvature(surface, u, v, step_size=1e-3):
    """Compute mean curvature using intrinsic gradient method"""
    return compute_mean_curvature(surface, u, v, step_size)

def intrinsic_gradient_principal_curvatures(surface, u, v, step_size=1e-3):
    """Compute principal curvatures using intrinsic gradient method"""
    result = compute_all_curvatures(surface, u, v, step_size)
    return result['principal_curvatures']

def intrinsic_gradient_all_curvatures(surface, u, v, step_size=1e-3):
    """Compute all curvatures using intrinsic gradient method"""
    return compute_all_curvatures(surface, u, v, step_size)


# ========== Method Comparison ==========

def compare_methods(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> Dict[str, float]:
    """
    Compare classical and intrinsic gradient curvature methods
    """
    # Classical method
    K_classical = gaussian_curvature_classical(surface, u, v, step_size)
    
    # Intrinsic gradient method
    K_intrinsic = intrinsic_gradient_gaussian_curvature(surface, u, v, step_size)
    
    # Comparison
    difference = abs(K_classical - K_intrinsic)
    relative_error = difference / abs(K_classical) if abs(K_classical) > 1e-14 else 0.0

    return {
        'K_classical': K_classical,
        'K_intrinsic': K_intrinsic,
        'difference': difference,
        'relative_error': relative_error
    }


# ========== Backward Compatibility Functions ==========

def gaussian_curvature(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> float:
    """Compute Gaussian curvature (default: intrinsic gradient method)"""
    return intrinsic_gradient_gaussian_curvature(surface, u, v, step_size)

def mean_curvature(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> float:
    """Compute mean curvature (default: intrinsic gradient method)"""
    return intrinsic_gradient_mean_curvature(surface, u, v, step_size)

def principal_curvatures(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> Tuple[float, float]:
    """Compute principal curvatures (default: intrinsic gradient method)"""
    return intrinsic_gradient_principal_curvatures(surface, u, v, step_size)

def all_curvatures(surface: Surface, u: float, v: float, step_size: float = 1e-3) -> Dict[str, Union[float, np.ndarray]]:
    """Compute all curvature quantities (default: intrinsic gradient method)"""
    return intrinsic_gradient_all_curvatures(surface, u, v, step_size)


# ========== Export ==========

__all__ = [
    # Classical method
    'CurvatureCalculator',
    'gaussian_curvature_classical',
    'mean_curvature_classical',
    'principal_curvatures_classical',
    'all_curvatures_classical',

    # Intrinsic Gradient Operator method
    'intrinsic_gradient_gaussian_curvature',
    'intrinsic_gradient_mean_curvature',
    'intrinsic_gradient_principal_curvatures',
    'intrinsic_gradient_all_curvatures',
    'compare_methods',

    # Backward compatibility (default to intrinsic gradient)
    'gaussian_curvature',
    'mean_curvature',
    'principal_curvatures',
    'all_curvatures',

    # Utility functions
    'derivative_5pt',
    'derivative_2nd_5pt',
    'richardson_extrapolation',
]