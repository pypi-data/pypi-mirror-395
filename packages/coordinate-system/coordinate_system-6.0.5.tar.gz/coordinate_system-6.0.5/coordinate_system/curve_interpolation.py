"""
Frame Field Curve Interpolation System
=======================================

Frame field spline interpolation based on C++ implementation,
providing geometrically continuous curve reconstruction equivalent to NURBS.

Main Features:
- Generate Frenet frames from discrete points
- Frame field interpolation with multiple parameterization methods
- C2-continuous high-order interpolation
- B-spline and frame field hybrid interpolation
- Curvature distribution analysis

Author: PanGuoJun
Date: 2025-12-01
"""

import math
import numpy as np
from typing import List, Tuple, Optional

try:
    from .coordinate_system import vec3, coord3, quat
except ImportError:
    import coordinate_system
    vec3 = coordinate_system.vec3
    coord3 = coordinate_system.coord3
    quat = coordinate_system.quat


# ========== Utility Functions ==========

def catmull_rom(p0: vec3, p1: vec3, p2: vec3, p3: vec3, t: float) -> vec3:
    """
    Catmull-Rom spline interpolation for smooth position interpolation

    Args:
        p0, p1, p2, p3: Four control points
        t: Parameter [0, 1] between p1 and p2

    Returns:
        Interpolated position
    """
    t2 = t * t
    t3 = t2 * t

    # Catmull-Rom basis functions
    result = (
        p0 * (-0.5 * t3 + 1.0 * t2 - 0.5 * t) +
        p1 * ( 1.5 * t3 - 2.5 * t2 + 1.0) +
        p2 * (-1.5 * t3 + 2.0 * t2 + 0.5 * t) +
        p3 * ( 0.5 * t3 - 0.5 * t2)
    )

    return result


def squad_interp(q0: quat, q1: quat, q2: quat, q3: quat, t: float) -> quat:
    """
    SQUAD (Spherical Quadrangle) quaternion interpolation for C2-continuous rotation

    Args:
        q0, q1, q2, q3: Four quaternions
        t: Parameter [0, 1] between q1 and q2

    Returns:
        Interpolated quaternion
    """
    # Compute intermediate control quaternions for smooth interpolation
    def compute_intermediate(qa: quat, qb: quat, qc: quat) -> quat:
        """Compute intermediate control quaternion"""
        # Ensure shortest path
        if qa.dot(qb) < 0:
            qb = quat(-qb.w, -qb.x, -qb.y, -qb.z)
        if qb.dot(qc) < 0:
            qc = quat(-qc.w, -qc.x, -qc.y, -qc.z)

        # Log map
        inv_qb = qb.inverse()
        log_qa_qb = (inv_qb * qa).ln()
        log_qc_qb = (inv_qb * qc).ln()

        # Intermediate control point
        intermediate = qb * (((log_qa_qb + log_qc_qb) * -0.25).exp())
        return intermediate

    # Compute control quaternions
    try:
        s1 = compute_intermediate(q0, q1, q2)
        s2 = compute_intermediate(q1, q2, q3)
    except:
        # Fallback to simple slerp if SQUAD fails
        return quat.slerp(q1, q2, t)

    # SQUAD interpolation: slerp(slerp(q1, q2, t), slerp(s1, s2, t), 2t(1-t))
    slerp1 = quat.slerp(q1, q2, t)
    slerp2 = quat.slerp(s1, s2, t)
    h = 2.0 * t * (1.0 - t)

    return quat.slerp(slerp1, slerp2, h)


# ========== Core Functions ==========

def generate_frenet_frames(points: List[vec3]) -> List[coord3]:
    """
    Generate Frenet-like frames from discrete point sequence

    Args:
        points: Discrete point sequence

    Returns:
        Corresponding frame sequence
    """
    frames = []
    n = len(points)

    if n < 3:
        # Use simple frames when not enough points
        for i in range(n):
            if i == 0:
                tangent = (points[1] - points[0]).normalized()
            elif i == n-1:
                tangent = (points[n-1] - points[n-2]).normalized()
            else:
                tangent = (points[i+1] - points[i-1]).normalized()

            # Construct orthogonal frame
            UZ = vec3(0, 0, 1)
            UY = vec3(0, 1, 0)

            if abs(1.0 - abs(tangent.dot(UZ))) > 0.1:
                normal = tangent.cross(UZ).normalized()
            else:
                normal = tangent.cross(UY).normalized()

            binormal = tangent.cross(normal).normalized()

            frame = coord3.from_axes(tangent, normal, binormal)
            frame.o = points[i]
            frames.append(frame)

        return frames

    # Calculate Frenet frame for each point
    for i in range(n):
        if i == 0:
            # Start point: forward difference
            tangent = (points[1] - points[0]).normalized()
            v1 = points[1] - points[0]
            v2 = points[2] - points[1]
            binormal = v1.cross(v2).normalized()

            if binormal.length() < 1e-6:
                UZ = vec3(0, 0, 1)
                UY = vec3(0, 1, 0)
                if abs(1.0 - abs(tangent.dot(UZ))) > 0.1:
                    binormal = tangent.cross(UZ).normalized()
                else:
                    binormal = tangent.cross(UY).normalized()

        elif i == n-1:
            # End point: backward difference
            tangent = (points[n-1] - points[n-2]).normalized()
            v1 = points[n-2] - points[n-3]
            v2 = points[n-1] - points[n-2]
            binormal = v1.cross(v2).normalized()

            if binormal.length() < 1e-6:
                UZ = vec3(0, 0, 1)
                UY = vec3(0, 1, 0)
                if abs(1.0 - abs(tangent.dot(UZ))) > 0.1:
                    binormal = tangent.cross(UZ).normalized()
                else:
                    binormal = tangent.cross(UY).normalized()
        else:
            # Interior point: central difference
            tangent = (points[i+1] - points[i-1]).normalized()
            v1 = points[i] - points[i-1]
            v2 = points[i+1] - points[i]
            binormal = v1.cross(v2).normalized()

            if binormal.length() < 1e-6:
                UZ = vec3(0, 0, 1)
                UY = vec3(0, 1, 0)
                if abs(1.0 - abs(tangent.dot(UZ))) > 0.1:
                    binormal = tangent.cross(UZ).normalized()
                else:
                    binormal = tangent.cross(UY).normalized()

        # Re-orthogonalize
        normal = binormal.cross(tangent).normalized()
        binormal = tangent.cross(normal).normalized()

        frame = coord3.from_axes(tangent, normal, binormal)
        frame.o = points[i]
        frames.append(frame)

    return frames


def frame_field_spline(frames: List[coord3], t: float, curve_type: int = 1) -> coord3:
    """
    Frame field spline interpolation

    Args:
        frames: Frame sequence
        t: Global parameter [0,1]
        curve_type: Curve type (0=uniform, 1=chord-length, 2=centripetal)

    Returns:
        Interpolated frame
    """
    if not frames:
        return coord3()
    if len(frames) == 1:
        return frames[0]

    n = len(frames)

    # Compute node vector
    nodes = [0.0]

    if curve_type == 0:
        # Uniform parameterization
        for i in range(1, n):
            nodes.append(i / (n - 1))
    else:
        # Chord-length or centripetal parameterization
        total_length = 0.0
        segment_lengths = []

        for i in range(n - 1):
            dist = (frames[i+1].o - frames[i].o).length()
            if curve_type == 2:
                dist = math.sqrt(dist)
            segment_lengths.append(dist)
            total_length += dist

        for i in range(1, n):
            nodes.append(nodes[i-1] + segment_lengths[i-1] / total_length)

    # Find the segment containing parameter t
    segment_index = 0
    for i in range(n - 1):
        if nodes[i] <= t <= nodes[i+1]:
            segment_index = i
            break
    if t >= nodes[n-1]:
        segment_index = n - 2

    # Local parameter
    local_t = (t - nodes[segment_index]) / (nodes[segment_index+1] - nodes[segment_index])
    local_t = max(0.0, min(1.0, local_t))

    # SE(3) interpolation using slerp
    return coord3.slerp(frames[segment_index], frames[segment_index+1], local_t)


def frame_field_spline_c2(frames: List[coord3], t: float) -> coord3:
    """
    C2-continuous frame field spline with high-order continuity
    Uses Catmull-Rom for position and SQUAD for rotation

    Args:
        frames: Frame sequence (requires at least 4 frames)
        t: Global parameter [0,1]

    Returns:
        Interpolated frame with C2 continuity
    """
    if len(frames) < 4:
        # Fallback to C1 continuity when not enough frames
        return frame_field_spline(frames, t, 1)

    n = len(frames)

    # Compute node vector using chord-length parameterization
    nodes = [0.0]
    total_length = 0.0
    segment_lengths = []

    for i in range(n - 1):
        dist = (frames[i+1].o - frames[i].o).length()
        segment_lengths.append(dist)
        total_length += dist

    for i in range(1, n):
        nodes.append(nodes[i-1] + segment_lengths[i-1] / total_length)

    # Find the segment containing parameter t
    i = 0
    for i in range(n - 1):
        if t >= nodes[i] and t <= nodes[i+1]:
            break
    if t >= nodes[n-1]:
        i = n - 2

    # Local parameter
    local_t = (t - nodes[i]) / (nodes[i+1] - nodes[i])
    local_t = max(0.0, min(1.0, local_t))

    # Get 4 control frames for interpolation
    i0 = max(0, i - 1)
    i1 = i
    i2 = i + 1
    i3 = min(n - 1, i + 2)

    # Position using Catmull-Rom spline
    pos = catmull_rom(frames[i0].o, frames[i1].o, frames[i2].o, frames[i3].o, local_t)

    # Rotation using SQUAD interpolation
    q0 = frames[i0].Q()
    q1 = frames[i1].Q()
    q2 = frames[i2].Q()
    q3 = frames[i3].Q()

    rot = squad_interp(q0, q1, q2, q3, local_t)

    return coord3(pos, rot)


def reconstruct_curve_from_polygon(
    polygon: List[vec3],
    samples: int = 100,
    curve_type: int = 1
) -> List[vec3]:
    """
    Reconstruct curve from polygon vertices using frame field spline

    Args:
        polygon: Input polygon vertices
        samples: Number of sample points
        curve_type: Curve type (0=uniform, 1=chord-length, 2=centripetal, 3=C2-continuous)

    Returns:
        Reconstructed curve point sequence
    """
    if len(polygon) < 2:
        return []

    # Generate frame field from polygon vertices
    frames = generate_frenet_frames(polygon)

    # Interpolate and sample
    curve_points = []
    for i in range(samples):
        t = i / (samples - 1)

        if curve_type == 3:
            # C2-continuous interpolation
            interpolated_frame = frame_field_spline_c2(frames, t)
        else:
            # Standard interpolation
            interpolated_frame = frame_field_spline(frames, t, curve_type)

        curve_points.append(interpolated_frame.o)

    return curve_points


def compute_curvature_profile(curve: List[vec3]) -> List[float]:
    """
    Compute curvature distribution of reconstructed curve

    Args:
        curve: Curve point sequence

    Returns:
        Curvature value sequence
    """
    if len(curve) < 3:
        return []

    curvatures = []

    for i in range(1, len(curve) - 1):
        v1 = curve[i] - curve[i-1]
        v2 = curve[i+1] - curve[i]

        # Calculate angle change
        dot_product = v1.normalized().dot(v2.normalized())
        dot_product = max(-1.0, min(1.0, dot_product))
        delta_angle = math.acos(dot_product)

        avg_length = (v1.length() + v2.length()) * 0.5

        # Curvature = angle change rate / arc length
        curvature = delta_angle / (avg_length + 1e-6)
        curvatures.append(curvature)

    # Use boundary values for endpoints
    if curvatures:
        curvatures.insert(0, curvatures[0])
        curvatures.append(curvatures[-1])

    return curvatures


# ========== Main Class ==========

class InterpolatedCurve:
    """
    Interpolated curve class - Encapsulates frame field interpolation functionality
    """

    def __init__(self, control_points: List[vec3], curve_type: int = 1, c2_continuity: bool = False):
        """
        Initialize interpolated curve

        Args:
            control_points: Control point list
            curve_type: Curve type (0=uniform, 1=chord-length, 2=centripetal)
            c2_continuity: Enable C2-continuous interpolation (requires 4+ points)
        """
        self.control_points = control_points
        self.curve_type = curve_type
        self.c2_continuity = c2_continuity
        self.frames = generate_frenet_frames(control_points)

    def evaluate(self, t: float) -> vec3:
        """
        Evaluate position at parameter t

        Args:
            t: Parameter value [0, 1]

        Returns:
            Point on curve
        """
        frame = self.evaluate_frame(t)
        return frame.o

    def evaluate_frame(self, t: float) -> coord3:
        """
        Evaluate complete frame at parameter t

        Args:
            t: Parameter value [0, 1]

        Returns:
            Frame on curve
        """
        if self.c2_continuity and len(self.frames) >= 4:
            return frame_field_spline_c2(self.frames, t)
        else:
            return frame_field_spline(self.frames, t, self.curve_type)

    def sample(self, num_samples: int = 100) -> List[vec3]:
        """
        Sample curve points

        Args:
            num_samples: Number of sample points

        Returns:
            Sampled point list
        """
        curve_points = []
        for i in range(num_samples):
            t = i / (num_samples - 1)
            curve_points.append(self.evaluate(t))
        return curve_points

    def sample_frames(self, num_samples: int = 100) -> List[coord3]:
        """
        Sample frames

        Args:
            num_samples: Number of sample points

        Returns:
            Frame list
        """
        sampled_frames = []
        for i in range(num_samples):
            t = i / (num_samples - 1)
            sampled_frames.append(self.evaluate_frame(t))
        return sampled_frames

    def get_curvature_profile(self, num_samples: int = 100) -> List[float]:
        """
        Get curvature distribution

        Args:
            num_samples: Number of sample points

        Returns:
            Curvature value list
        """
        curve_points = self.sample(num_samples)
        return compute_curvature_profile(curve_points)


# ========== Export ==========

__all__ = [
    'generate_frenet_frames',
    'frame_field_spline',
    'frame_field_spline_c2',
    'reconstruct_curve_from_polygon',
    'compute_curvature_profile',
    'InterpolatedCurve',
    'catmull_rom',
    'squad_interp',
]
