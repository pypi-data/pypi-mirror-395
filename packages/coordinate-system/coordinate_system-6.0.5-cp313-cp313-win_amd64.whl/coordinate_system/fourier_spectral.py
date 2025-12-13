"""
Complex Frame Spectral Analysis - 向后兼容模块
==============================================

此模块已合并到 frames.py 中。
保留此文件仅用于向后兼容。

请直接使用 frames 模块：
    from coordinate_system.frames import (
        FourierFrame,
        FourierFrameSpectrum,
        spectral_transform,
        inverse_spectral_transform,
    )

Author: Quantum Frame Theory
Date: 2025-12-04
"""

import warnings

# 发出弃用警告
warnings.warn(
    "fourier_spectral 模块已合并到 frames.py 中。"
    "请直接使用: from coordinate_system.frames import ...",
    DeprecationWarning,
    stacklevel=2
)

# 从 frames 重导出所有内容
from .frames import (
    # 核心类
    FourierFrame,
    FourierFrameSpectrum,

    # 谱几何核心
    IntrinsicGradient,
    CurvatureFromFrame,
    BerryPhase,
    ChernNumber,
    SpectralDecomposition,
    HeatKernel,
    FrequencyProjection,
    FrequencyBandState,

    # 便利函数
    spectral_transform,
    inverse_spectral_transform,

    # 常数
    HBAR,
    GPU_AVAILABLE,
)

# 向后兼容别名（旧名称映射到新名称）
QFrame = FourierFrame
QFrameSpectrum = FourierFrameSpectrum
QuantumFrameSpectrum = FourierFrameSpectrum
QuantumFrameTransformer = FourierFrame  # FourierFrame 现在包含变换方法
Frame = FourierFrame  # 简称别名
FrameSpectrum = FourierFrameSpectrum  # 简称别名


def quantum_frame_transform(coord_field, grid_size=None, use_gpu=False, hbar=HBAR):
    """
    向后兼容函数 - 已整合到 Frame.from_coord_field()
    """
    warnings.warn(
        "quantum_frame_transform() 已弃用，请使用 Frame.from_coord_field()",
        DeprecationWarning,
        stacklevel=2
    )
    return Frame.from_coord_field(coord_field, hbar)


def inverse_quantum_transform(spectrum, use_gpu=False):
    """
    向后兼容函数 - 已整合到 FrameSpectrum.to_coord_field()
    """
    warnings.warn(
        "inverse_quantum_transform() 已弃用，请使用 spectrum.to_coord_field()",
        DeprecationWarning,
        stacklevel=2
    )
    return spectrum.to_coord_field()


def compute_quantum_spectral_density(spectrum):
    """
    向后兼容函数 - 已整合到 FrameSpectrum.spectral_density()
    """
    warnings.warn(
        "compute_quantum_spectral_density() 已弃用，请使用 spectrum.spectral_density()",
        DeprecationWarning,
        stacklevel=2
    )
    return spectrum.spectral_density()


def compute_radial_spectrum(spectrum):
    """
    向后兼容函数 - 已整合到 FrameSpectrum.radial_average()
    """
    warnings.warn(
        "compute_radial_spectrum() 已弃用，请使用 spectrum.radial_average()",
        DeprecationWarning,
        stacklevel=2
    )
    return spectrum.radial_average()


# 导出列表
__all__ = [
    # 核心类（新名称）
    'FourierFrame',
    'FourierFrameSpectrum',

    # 谱几何核心
    'IntrinsicGradient',
    'CurvatureFromFrame',
    'BerryPhase',
    'ChernNumber',
    'SpectralDecomposition',
    'HeatKernel',
    'FrequencyProjection',
    'FrequencyBandState',

    # 向后兼容别名（旧名称）
    'QFrame',
    'QFrameSpectrum',
    'QuantumFrameSpectrum',
    'QuantumFrameTransformer',
    'Frame',
    'FrameSpectrum',

    # 便利函数
    'spectral_transform',
    'inverse_spectral_transform',

    # 向后兼容函数
    'quantum_frame_transform',
    'inverse_quantum_transform',
    'compute_quantum_spectral_density',
    'compute_radial_spectrum',

    # 常数
    'HBAR',
    'GPU_AVAILABLE',
]
