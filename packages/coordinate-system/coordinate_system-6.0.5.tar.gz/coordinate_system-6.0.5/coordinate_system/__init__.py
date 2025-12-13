# coordinate_system/__init__.py
"""
Coordinate System Library
=========================

High-performance 3D coordinate system and differential geometry library.

Core Components (C++ Layer):
- vec3, vec2: Vector types
- quat: Quaternion for rotations (SU(2))
- coord3: 3D coordinate frame (Sim(3) group)

Python Modules:
- differential_geometry: Surface curvature via intrinsic gradient / Lie bracket
- spectral_geometry: FourierFrame (GL(1,C)), spectral analysis, heat kernel
- u3_frame: U3Frame (U(3)), gauge field theory, symmetry breaking
- visualization: Coordinate system visualization
- curve_interpolation: C2-continuous curve and frame interpolation

Group Correspondence:
- coord3 ∈ Sim(3) = R³ ⋊ (SO(3) × R⁺)
- FourierFrame ∈ GL(1,C) = U(1) × R⁺
- U3Frame ∈ U(3) = SU(3) × U(1)

Version: 6.0.4
"""

__version__ = '6.0.4'

from .coordinate_system import vec3, vec2
from .coordinate_system import quat
from .coordinate_system import coord3

# Differential geometry module (merged from differential_geometry.py and curvature.py)
from .differential_geometry import (
    # Surface classes
    Surface,
    Sphere,
    Torus,

    # Core classes
    MetricTensor,
    GradientResult,
    IntrinsicGradientOperator,
    IntrinsicGradientCurvatureCalculator,
    CurvatureCalculator,

    # Intrinsic gradient method functions (default)
    compute_gaussian_curvature,
    compute_mean_curvature,
    compute_riemann_curvature,
    compute_all_curvatures,
    compute_intrinsic_gradient,

    # Classical method functions
    gaussian_curvature_classical,
    mean_curvature_classical,
    principal_curvatures_classical,
    all_curvatures_classical,

    # Backward compatibility aliases
    gaussian_curvature,
    mean_curvature,
    principal_curvatures,
    all_curvatures,

    # Method comparison
    compare_methods,

    # Utility functions
    derivative_5pt,
    derivative_2nd_5pt,
    richardson_extrapolation,
)

# Spectral geometry module (FourierFrame, GL(1,C) group)
from .spectral_geometry import (
    # Core classes
    FourierFrame,
    FourierFrameSpectrum,

    # Spectral geometry core
    IntrinsicGradient,
    CurvatureFromFrame,
    BerryPhase,
    ChernNumber,
    SpectralDecomposition,
    HeatKernel,
    FrequencyProjection,
    FrequencyBandState,

    # Convenience functions
    spectral_transform,
    inverse_spectral_transform,

    # Constants
    HBAR,
    GPU_AVAILABLE,
)

# U(3) Frame module (U(3) group, gauge field theory)
from .u3_frame import (
    # Core U(3) classes
    U3Frame,
    SU3Component,

    # Gauge field classes
    GaugeConnection,
    FieldStrength,

    # Symmetry breaking
    SymmetryBreakingPotential,
)

# Visualization module
from .visualization import (
    CoordinateSystemVisualizer,
    CurveVisualizer,
    ParametricCurve,
    visualize_coord_system,
    visualize_curve,
)

# Curve interpolation module
from .curve_interpolation import (
    InterpolatedCurve,
    generate_frenet_frames,
    frame_field_spline,
    frame_field_spline_c2,
    reconstruct_curve_from_polygon,
    compute_curvature_profile,
    catmull_rom,
    squad_interp,
)

__all__ = [
    # Constants
    'ZERO3', 'UNITX', 'UNITY', 'UNITZ', 'ONE3', 'ONE4', 'ONEC',

    # Core types
    'vec3', 'vec2', 'quat', 'coord3', 'lerp',

    # Differential geometry - Surface classes
    'Surface', 'Sphere', 'Torus',

    # Differential geometry - Core classes
    'MetricTensor', 'GradientResult',
    'IntrinsicGradientOperator', 'IntrinsicGradientCurvatureCalculator',
    'CurvatureCalculator',

    # Differential geometry - Intrinsic gradient method (default)
    'compute_gaussian_curvature', 'compute_mean_curvature',
    'compute_riemann_curvature', 'compute_all_curvatures',
    'compute_intrinsic_gradient',

    # Differential geometry - Classical method
    'gaussian_curvature_classical', 'mean_curvature_classical',
    'principal_curvatures_classical', 'all_curvatures_classical',

    # Differential geometry - Backward compatibility
    'gaussian_curvature', 'mean_curvature',
    'principal_curvatures', 'all_curvatures',

    # Differential geometry - Comparison and utilities
    'compare_methods',
    'derivative_5pt', 'derivative_2nd_5pt', 'richardson_extrapolation',

    # Spectral geometry module (FourierFrame, GL(1,C))
    'FourierFrame', 'FourierFrameSpectrum',
    'IntrinsicGradient', 'CurvatureFromFrame', 'BerryPhase', 'ChernNumber',
    'SpectralDecomposition', 'HeatKernel', 'FrequencyProjection', 'FrequencyBandState',
    'spectral_transform', 'inverse_spectral_transform',
    'HBAR', 'GPU_AVAILABLE',

    # U(3) Frame module (Gauge theory)
    'U3Frame', 'SU3Component',
    'GaugeConnection', 'FieldStrength',
    'SymmetryBreakingPotential',

    # Visualization
    'CoordinateSystemVisualizer', 'CurveVisualizer', 'ParametricCurve',
    'visualize_coord_system', 'visualize_curve',

    # Curve interpolation
    'InterpolatedCurve', 'generate_frenet_frames', 'frame_field_spline',
    'frame_field_spline_c2', 'reconstruct_curve_from_polygon', 'compute_curvature_profile',
    'catmull_rom', 'squad_interp',
]

# Constants for unit vectors and zero point
ZERO3 = vec3(0.0, 0.0, 0.0)         # Zero vector (origin point)
UNITX = vec3(1.0, 0.0, 0.0)         # Unit vector in X direction
UNITY = vec3(0.0, 1.0, 0.0)         # Unit vector in Y direction
UNITZ = vec3(0.0, 0.0, 1.0)         # Unit vector in Z direction
ONE3  = vec3(1.0, 1.0, 1.0)         # Unit scale vector (1,1,1)

# Unit quaternion (no rotation)
ONE4 = quat(1.0, 0.0, 0.0, 0.0)

# World coordinate system (the fundamental unit one in 3D space)
ONEC = coord3(ZERO3, ONE4, ONE3)


def lerp(a: vec3, b: vec3, t: float) -> vec3:
    """
    Linear interpolation between two points in 3D space.

    Args:
        a: Starting point
        b: End point
        t: Interpolation ratio [0, 1]

    Returns:
        Interpolated point: a + (b - a) * t
    """
    return a + (b - a) * t


class CoordTuple(tuple):
    """
    Custom tuple subclass that supports operations with coord3 objects.
    """

    def __mul__(self, other):
        """Multiplication operation supporting coord3 interaction."""
        if isinstance(other, coord3):
            return self._mul_coord3(other)
        return super().__mul__(other)

    def __rmul__(self, other):
        """Right multiplication operation supporting coord3 interaction."""
        if isinstance(other, coord3):
            return self._mul_coord3(other)
        return super().__rmul__(other)

    def __truediv__(self, other):
        """Division operation supporting coord3 interaction."""
        if isinstance(other, coord3):
            return self._div_coord3(other)
        return super().__truediv__(other)

    def _mul_coord3(self, coord: coord3) -> tuple:
        """Tuple multiplication with coordinate system."""
        if len(self) != 3:
            raise ValueError("Tuple must have exactly 3 elements for spatial operations")

        x, y, z = self
        scale_vec = vec3(x, y, z)
        result = scale_vec * coord
        return (result.x, result.y, result.z)

    def _div_coord3(self, coord: coord3) -> tuple:
        """Tuple division with coordinate system."""
        if len(self) != 3:
            raise ValueError("Tuple must have exactly 3 elements for spatial operations")

        x, y, z = self
        if x == 0 or y == 0 or z == 0:
            raise ZeroDivisionError("Division by zero")

        scale_vec = vec3(x, y, z)
        result = scale_vec / coord
        return (result.x, result.y, result.z)


# Store original coord3 operators
_original_coord3_mul = coord3.__mul__
_original_coord3_rmul = coord3.__rmul__
_original_coord3_truediv = getattr(coord3, '__truediv__', None)


def _new_coord3_mul(self, other):
    """Enhanced multiplication operator for coord3."""
    if isinstance(other, tuple):
        other = CoordTuple(other)
        return other * self
    return _original_coord3_mul(self, other)


def _new_coord3_rmul(self, other):
    """Enhanced right multiplication operator for coord3."""
    if isinstance(other, tuple):
        other = CoordTuple(other)
        return other * self
    return _original_coord3_rmul(self, other)


def _new_coord3_truediv(self, other):
    """Enhanced division operator for coord3."""
    if isinstance(other, tuple):
        other = CoordTuple(other)
        return other / self
    if _original_coord3_truediv:
        return _original_coord3_truediv(self, other)
    raise TypeError(f"unsupported operand type(s) for /: 'coord3' and {type(other).__name__}")


# Apply enhancements to coord3 operators
coord3.__mul__ = _new_coord3_mul
coord3.__rmul__ = _new_coord3_rmul
coord3.__truediv__ = _new_coord3_truediv
