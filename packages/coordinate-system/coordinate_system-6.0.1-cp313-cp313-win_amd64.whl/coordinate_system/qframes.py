"""
复数量子化标架场 (Complex Quantum Frame Field)
==============================================

统一傅里叶变换与路径积分的几何框架。

核心思想：
- 傅里叶变换 = 复标架场的相位旋转 (QFrame * e^{iθ})
- 共形变换 = 复标架场的缩放 (QFrame * λ, λ∈ℝ⁺)
- 路径积分 = 标架场上的测度积分

数学框架：
- 复标度因子 Q ∈ ℂ 编码几何与谱空间的关系
- 标架乘法实现变换复合
- 行列式给出积分测度

Author: Quantum Frame Theory
Date: 2025-12-03
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Union, Any
from dataclasses import dataclass

# 导入坐标系统
try:
    from .coordinate_system import coord3, vec3, quat
except ImportError:
    try:
        from coordinate_system import coord3, vec3, quat
    except ImportError:
        # 延迟导入，允许独立使用
        coord3 = None
        vec3 = None
        quat = None

# 物理常数
HBAR = 1.0  # 约化普朗克常数（自然单位）

# GPU 可用性检查
try:
    import cupy as cp
    import cupyx.scipy.fft as cufft
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    cp = None
    cufft = None


# ============================================================
# 核心复标架代数
# ============================================================

class QFrame:
    """
    量子标架 - 统一傅里叶变换与路径积分的几何框架

    核心属性：
    - base_coord: 基础坐标系 (coord3 对象)
    - Q: 复标度因子 Q ∈ ℂ，编码相位与缩放

    关键变换：
    - QFrame * e^{iθ} = 傅里叶变换 (θ=π/2 为标准变换)
    - QFrame * λ = 共形变换 (λ∈ℝ⁺)
    - QFrame * QFrame = 标架复合 (对应路径积分中的复合)
    """

    def __init__(self, base_coord=None, q_factor=1.0+0j):
        """
        初始化量子标架

        Args:
            base_coord: 基础坐标系 (coord3 对象)，None 时使用单位标架
            q_factor: 复标度因子 Q ∈ ℂ
        """
        if base_coord is None:
            if coord3 is not None:
                self.base = coord3.identity()
            else:
                self.base = None
        else:
            self.base = base_coord

        self.Q = complex(q_factor)  # 确保是复数
        self.dim = 3

    # -------------------- 复标架属性 --------------------

    @property
    def o(self):
        """复位置向量"""
        if self.base is None:
            return None
        o_base = self.base.o
        # 复扩展：实部为原位置，虚部编码相位信息
        return vec3(
            o_base.x * self.Q.real + 1j * o_base.x * self.Q.imag,
            o_base.y * self.Q.real + 1j * o_base.y * self.Q.imag,
            o_base.z * self.Q.real + 1j * o_base.z * self.Q.imag
        ) if vec3 else None

    @property
    def s(self):
        """复缩放向量: s_Q = s_base · Q"""
        if self.base is None:
            return None
        s_base = self.base.s
        return vec3(
            s_base.x * self.Q.real + 1j * s_base.x * self.Q.imag,
            s_base.y * self.Q.real + 1j * s_base.y * self.Q.imag,
            s_base.z * self.Q.real + 1j * s_base.z * self.Q.imag
        ) if vec3 else None

    @property
    def phase(self):
        """相位 arg(Q)"""
        return np.angle(self.Q)

    @property
    def magnitude(self):
        """模 |Q|"""
        return np.abs(self.Q)

    @property
    def det(self):
        """
        行列式: Det(QFrame)

        用于路径积分测度 ∫ Dφ · Det[QFrame] · exp(iS/ħ)
        """
        if self.base is None:
            return self.Q ** 3  # 3维标架
        s = self.base.s
        det_s = s.x * s.y * s.z
        return det_s * (self.Q ** 3)

    # -------------------- 标架运算 --------------------

    def __mul__(self, other):
        """
        标架乘法 - 核心变换操作

        支持：
        - QFrame * complex: 相位旋转/缩放 (傅里叶变换)
        - QFrame * QFrame: 标架复合 (路径积分复合)
        - QFrame * vec3: 向量变换
        """
        if isinstance(other, (int, float, complex)):
            # 标量乘法实现傅里叶变换
            new_Q = self.Q * other
            return QFrame(self.base, new_Q)

        elif isinstance(other, QFrame):
            # 标架复合
            if self.base is not None and other.base is not None:
                new_base = self.base * other.base
            else:
                new_base = self.base or other.base
            new_Q = self.Q * other.Q
            return QFrame(new_base, new_Q)

        elif vec3 is not None and isinstance(other, vec3):
            # 向量变换
            return vec3(
                other.x * self.Q.real,
                other.y * self.Q.real,
                other.z * self.Q.real
            )

        return NotImplemented

    def __rmul__(self, other):
        """右乘法"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """标架除法 - 逆变换"""
        if isinstance(other, (int, float, complex)):
            return QFrame(self.base, self.Q / other)
        elif isinstance(other, QFrame):
            if self.base is not None and other.base is not None:
                new_base = self.base / other.base
            else:
                new_base = self.base
            return QFrame(new_base, self.Q / other.Q)
        return NotImplemented

    def __pow__(self, n):
        """幂运算: 对应多次变换"""
        if isinstance(n, (int, float, complex)):
            return QFrame(self.base, self.Q ** n)
        return NotImplemented

    def __eq__(self, other):
        """相等比较"""
        if not isinstance(other, QFrame):
            return False
        return np.isclose(self.Q, other.Q)

    def __repr__(self):
        if self.base is not None:
            return f"QFrame(Q={self.Q:.4f}, o={self.base.o})"
        return f"QFrame(Q={self.Q:.4f})"

    # -------------------- 傅里叶变换 --------------------

    def fourier_transform(self, theta: float = np.pi/2) -> 'QFrame':
        """
        傅里叶变换: F_θ[QFrame] = QFrame · e^{iθ}

        Args:
            theta: 旋转角度，π/2 为标准傅里叶变换

        Returns:
            变换后的 QFrame

        性质：
        - F^4 = I (四次变换回到自身)
        - F^2 = P (宇称变换)
        """
        ft_factor = np.exp(1j * theta)
        return self * ft_factor

    def inverse_fourier_transform(self, theta: float = np.pi/2) -> 'QFrame':
        """逆傅里叶变换: F^{-1} = F_{-θ}"""
        return self.fourier_transform(-theta)

    def conformal_transform(self, lambda_factor: float) -> 'QFrame':
        """
        共形变换: C → C · λ, λ ∈ ℝ⁺

        实现缩放变换，保持角度不变
        """
        return self * lambda_factor

    # -------------------- 谱变换 (整合自 fourier_spectral) --------------------

    @staticmethod
    def spectral_transform_2d(field: np.ndarray, hbar: float = HBAR) -> np.ndarray:
        """
        二维谱变换：位置空间 → 动量空间

        数学形式：
        ψ̃(k) = ∫ e^{ikx/ħ} ψ(x) dx / √(2πħ)

        Args:
            field: 输入场，形状 [ny, nx, ...] 或 [ny, nx]
            hbar: 约化普朗克常数

        Returns:
            动量空间谱
        """
        # 确定 FFT 的轴
        if field.ndim >= 2:
            axes = (0, 1)
        else:
            axes = None

        spectrum = np.fft.fft2(field, axes=axes)

        # 量子力学归一化
        normalization = 1.0 / np.sqrt(2 * np.pi * hbar)
        return spectrum * normalization

    @staticmethod
    def inverse_spectral_transform_2d(spectrum: np.ndarray, hbar: float = HBAR) -> np.ndarray:
        """
        二维逆谱变换：动量空间 → 位置空间

        Args:
            spectrum: 动量空间谱
            hbar: 约化普朗克常数

        Returns:
            位置空间场
        """
        if spectrum.ndim >= 2:
            axes = (0, 1)
        else:
            axes = None

        denormalization = np.sqrt(2 * np.pi * hbar)
        return np.fft.ifft2(spectrum * denormalization, axes=axes).real

    @staticmethod
    def spectral_transform_2d_gpu(field: np.ndarray, hbar: float = HBAR) -> np.ndarray:
        """GPU 加速的二维谱变换"""
        if not GPU_AVAILABLE:
            raise RuntimeError("CuPy 不可用，无法使用 GPU 加速")

        field_gpu = cp.asarray(field)
        spectrum_gpu = cufft.fft2(field_gpu, axes=(0, 1))
        normalization = 1.0 / np.sqrt(2 * np.pi * hbar)
        spectrum_gpu *= normalization
        return cp.asnumpy(spectrum_gpu)

    @classmethod
    def from_coord_field(cls, coord_field: List[List], hbar: float = HBAR) -> 'QFrameSpectrum':
        """
        从坐标场创建谱表示

        将坐标场的各分量进行谱变换

        Args:
            coord_field: 二维坐标场列表 [[coord3, ...], ...]
            hbar: 约化普朗克常数

        Returns:
            QFrameSpectrum 对象
        """
        ny = len(coord_field)
        nx = len(coord_field[0]) if ny > 0 else 0

        # 提取场分量
        tensor_field = np.zeros((ny, nx, 12), dtype=np.float64)
        for i in range(ny):
            for j in range(nx):
                coord = coord_field[i][j]
                tensor_field[i, j, 0:3] = [coord.o.x, coord.o.y, coord.o.z]
                tensor_field[i, j, 3:6] = [coord.ux.x, coord.ux.y, coord.ux.z]
                tensor_field[i, j, 6:9] = [coord.uy.x, coord.uy.y, coord.uy.z]
                tensor_field[i, j, 9:12] = [coord.uz.x, coord.uz.y, coord.uz.z]

        # 谱变换各分量
        origin_spectrum = cls.spectral_transform_2d(tensor_field[..., 0:3], hbar)
        ux_spectrum = cls.spectral_transform_2d(tensor_field[..., 3:6], hbar)
        uy_spectrum = cls.spectral_transform_2d(tensor_field[..., 6:9], hbar)
        uz_spectrum = cls.spectral_transform_2d(tensor_field[..., 9:12], hbar)

        # 动量网格
        kx = 2 * np.pi * np.fft.fftfreq(nx) / hbar
        ky = 2 * np.pi * np.fft.fftfreq(ny) / hbar

        return QFrameSpectrum(
            ux_spectrum=ux_spectrum,
            uy_spectrum=uy_spectrum,
            uz_spectrum=uz_spectrum,
            origin_spectrum=origin_spectrum,
            momentum_grid=(kx, ky),
            hbar=hbar
        )

    # -------------------- 路径积分 --------------------

    def path_integral_measure(self, field_values: List) -> complex:
        """
        路径积分测度: Det[QFrame] · exp(iS/ħ)

        Args:
            field_values: 场构型列表

        Returns:
            积分权重
        """
        det_frame = self.det
        action = self._compute_action(field_values)
        return det_frame * np.exp(1j * action)

    def _compute_action(self, field_values: List) -> float:
        """计算作用量 S[φ, QFrame]"""
        if not field_values:
            return 0.0

        # 简化的标量场作用量
        kinetic = 0.0
        mass_term = 0.0

        for i, phi in enumerate(field_values):
            if i < len(field_values) - 1:
                phi_next = field_values[i + 1]
                grad = (phi_next - phi) * self.Q
                kinetic += np.abs(grad) ** 2
            mass_term += np.abs(phi) ** 2

        return 0.5 * (kinetic + mass_term)

    # -------------------- 狄拉克符号导出 --------------------

    def to_dirac_notation(self, basis: str = 'position') -> str:
        """
        转换为狄拉克符号表示（导出用）

        Args:
            basis: 'position' | 'momentum'

        Returns:
            狄拉克符号字符串
        """
        symbol = 'x' if basis == 'position' else 'p'
        return f"⟨{symbol}|Q⟩ = {self.Q:.4f}|{symbol}⟩"


# ============================================================
# 量子态表示
# ============================================================

class QuantumState:
    """
    量子态在 QFrame 下的表示

    |ψ⟩ = amplitude · |basis⟩ ⊗ QFrame
    """

    def __init__(self, amplitude: complex = 1.0+0j,
                 frame: QFrame = None,
                 basis: str = 'position'):
        self.amplitude = complex(amplitude)
        self.frame = frame or QFrame()
        self.basis = basis

    def __mul__(self, other):
        """量子态变换: |ψ⟩ → QFrame · |ψ⟩"""
        if isinstance(other, QFrame):
            new_amplitude = self.amplitude * other.Q
            new_frame = self.frame * other
            return QuantumState(new_amplitude, new_frame, self.basis)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def fourier_transform(self) -> 'QuantumState':
        """傅里叶变换量子态"""
        ft_frame = QFrame(q_factor=1j)  # 乘以 i
        new_basis = 'momentum' if self.basis == 'position' else 'position'
        result = self * ft_frame
        result.basis = new_basis
        return result

    def expectation_value(self) -> float:
        """期望值: ⟨ψ|Q|ψ⟩"""
        return (np.conj(self.amplitude) * self.amplitude * self.frame.det).real

    def norm(self) -> float:
        """范数: ||ψ||"""
        return np.abs(self.amplitude)

    def normalize(self) -> 'QuantumState':
        """归一化"""
        n = self.norm()
        if n > 0:
            return QuantumState(self.amplitude / n, self.frame, self.basis)
        return self

    def __repr__(self):
        basis_symbol = 'x' if self.basis == 'position' else 'p'
        return f"{self.amplitude:.4f}|{basis_symbol}⟩ ⊗ {self.frame}"


# ============================================================
# 路径积分
# ============================================================

class PathIntegral:
    """
    路径积分计算器

    Z = ∫ Dφ · Det[QFrame] · exp(iS/ħ)
    """

    def __init__(self, frame: QFrame = None, hbar: float = HBAR):
        self.frame = frame or QFrame()
        self.hbar = hbar
        self.field_configs = []

    def add_configuration(self, field_value):
        """添加场构型"""
        self.field_configs.append(field_value)

    def add_configurations(self, field_values: List):
        """批量添加场构型"""
        self.field_configs.extend(field_values)

    def clear(self):
        """清除所有构型"""
        self.field_configs.clear()

    def compute(self) -> complex:
        """
        计算路径积分

        Returns:
            配分函数 Z
        """
        if not self.field_configs:
            return 0.0 + 0j

        total = 0.0 + 0j
        for phi in self.field_configs:
            weight = self.frame.path_integral_measure([phi])
            total += weight

        return total / len(self.field_configs)

    def classical_limit(self) -> Tuple[Any, float]:
        """
        经典极限: δS/δφ = 0 的解

        Returns:
            (最优构型, 最小作用量)
        """
        best_config = None
        min_action = float('inf')

        for phi in self.field_configs:
            action = self.frame._compute_action([phi])
            if action < min_action:
                min_action = action
                best_config = phi

        return best_config, min_action

    def __repr__(self):
        return f"PathIntegral(n_configs={len(self.field_configs)}, frame={self.frame})"


# ============================================================
# 谱数据结构
# ============================================================

@dataclass
class QFrameSpectrum:
    """
    QFrame 谱表示 - 坐标场在动量空间的表示

    存储坐标场各分量的傅里叶谱
    """
    ux_spectrum: np.ndarray       # x轴基矢量谱
    uy_spectrum: np.ndarray       # y轴基矢量谱
    uz_spectrum: np.ndarray       # z轴基矢量谱
    origin_spectrum: np.ndarray   # 原点位置谱
    momentum_grid: Tuple[np.ndarray, np.ndarray]  # (kx, ky)
    hbar: float = HBAR

    def __post_init__(self):
        """验证维度一致性"""
        shapes = [
            self.ux_spectrum.shape,
            self.uy_spectrum.shape,
            self.uz_spectrum.shape,
            self.origin_spectrum.shape
        ]
        if not all(s == shapes[0] for s in shapes):
            raise ValueError("所有谱分量必须具有相同维度")

    @property
    def shape(self) -> Tuple[int, int]:
        """谱的空间形状"""
        return self.ux_spectrum.shape[:2]

    def total_energy(self) -> float:
        """总能量 E = ∫ |ψ̃(k)|² dk"""
        return float(
            np.sum(np.abs(self.ux_spectrum)**2) +
            np.sum(np.abs(self.uy_spectrum)**2) +
            np.sum(np.abs(self.uz_spectrum)**2) +
            np.sum(np.abs(self.origin_spectrum)**2)
        )

    def spectral_density(self) -> np.ndarray:
        """谱密度 ρ(k) = Σ_μ |ψ̃_μ(k)|²"""
        density = (
            np.abs(self.ux_spectrum)**2 +
            np.abs(self.uy_spectrum)**2 +
            np.abs(self.uz_spectrum)**2 +
            np.abs(self.origin_spectrum)**2
        )
        return np.mean(density, axis=-1) if density.ndim > 2 else density

    def radial_average(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        径向平均谱 (ShapeDNA)

        Returns:
            (k_bins, radial_spectrum)
        """
        kx, ky = self.momentum_grid
        k_mag = np.sqrt(kx[:, None]**2 + ky[None, :]**2)

        density = self.spectral_density()

        k_max = np.max(k_mag)
        k_bins = np.linspace(0, k_max, 50)
        radial_avg = np.zeros(len(k_bins))

        for i in range(len(k_bins) - 1):
            mask = (k_mag >= k_bins[i]) & (k_mag < k_bins[i + 1])
            if np.any(mask):
                radial_avg[i] = np.mean(density[mask])

        return k_bins, radial_avg

    def to_coord_field(self) -> List[List]:
        """
        逆变换：谱 → 坐标场

        Returns:
            二维坐标场列表
        """
        ny, nx = self.shape

        origin_field = QFrame.inverse_spectral_transform_2d(self.origin_spectrum, self.hbar)
        ux_field = QFrame.inverse_spectral_transform_2d(self.ux_spectrum, self.hbar)
        uy_field = QFrame.inverse_spectral_transform_2d(self.uy_spectrum, self.hbar)
        uz_field = QFrame.inverse_spectral_transform_2d(self.uz_spectrum, self.hbar)

        coord_field = []
        for i in range(ny):
            row = []
            for j in range(nx):
                o = vec3(origin_field[i, j, 0], origin_field[i, j, 1], origin_field[i, j, 2])
                ux = vec3(ux_field[i, j, 0], ux_field[i, j, 1], ux_field[i, j, 2])
                uy = vec3(uy_field[i, j, 0], uy_field[i, j, 1], uy_field[i, j, 2])
                uz = vec3(uz_field[i, j, 0], uz_field[i, j, 1], uz_field[i, j, 2])

                c = coord3(o, quat(1, 0, 0, 0), vec3(1, 1, 1))
                c.ux, c.uy, c.uz = ux, uy, uz
                row.append(c)
            coord_field.append(row)

        return coord_field


# ============================================================
# 狄拉克符号（可选导出）
# ============================================================

class DiracBra:
    """左矢 ⟨ψ| - 狄拉克符号导出"""

    def __init__(self, state: QuantumState):
        self.state = state

    def __or__(self, other: 'DiracKet') -> complex:
        """内积 ⟨ψ|φ⟩"""
        return np.conj(self.state.amplitude) * other.state.amplitude


class DiracKet:
    """右矢 |φ⟩ - 狄拉克符号导出"""

    def __init__(self, state: QuantumState):
        self.state = state


def bra(state: QuantumState) -> DiracBra:
    """创建左矢"""
    return DiracBra(state)


def ket(state: QuantumState) -> DiracKet:
    """创建右矢"""
    return DiracKet(state)


# ============================================================
# 便利函数
# ============================================================

def spectral_transform(coord_field: List[List],
                       hbar: float = HBAR,
                       use_gpu: bool = False) -> QFrameSpectrum:
    """
    坐标场谱变换

    Args:
        coord_field: 二维坐标场
        hbar: 约化普朗克常数
        use_gpu: 是否使用 GPU 加速

    Returns:
        QFrameSpectrum 对象
    """
    return QFrame.from_coord_field(coord_field, hbar)


def inverse_spectral_transform(spectrum: QFrameSpectrum) -> List[List]:
    """
    逆谱变换

    Args:
        spectrum: QFrameSpectrum 对象

    Returns:
        重建的坐标场
    """
    return spectrum.to_coord_field()


# ============================================================
# 演示
# ============================================================

def demonstrate():
    """演示复标架代数"""
    print("=" * 60)
    print("复数量子化标架场 (QFrame) 演示")
    print("=" * 60)

    # 1. 创建基础 QFrame
    if coord3 is not None:
        base_frame = coord3.from_position(vec3(1, 0, 0))
        qf = QFrame(base_frame, q_factor=1.0+0.5j)
    else:
        qf = QFrame(q_factor=1.0+0.5j)

    print(f"\n1. 基础 QFrame: {qf}")
    print(f"   相位: {qf.phase:.4f} rad")
    print(f"   模: {qf.magnitude:.4f}")
    print(f"   行列式: {qf.det:.4f}")

    # 2. 傅里叶变换
    print(f"\n2. 傅里叶变换:")
    ft = qf.fourier_transform()
    print(f"   F[QFrame] = {ft}")
    print(f"   F^4[QFrame] ≈ QFrame: {qf.fourier_transform(2*np.pi)}")

    # 3. 共形变换
    print(f"\n3. 共形变换:")
    conf = qf.conformal_transform(2.0)
    print(f"   λ=2: {conf}")

    # 4. 标架复合
    print(f"\n4. 标架复合:")
    qf2 = QFrame(q_factor=0.5+0.5j)
    composed = qf * qf2
    print(f"   QFrame1 * QFrame2 = {composed}")

    # 5. 量子态
    print(f"\n5. 量子态:")
    psi = QuantumState(amplitude=1.0+0j, frame=qf)
    print(f"   初始: {psi}")
    psi_ft = psi.fourier_transform()
    print(f"   变换: {psi_ft}")
    print(f"   期望值: {psi.expectation_value():.4f}")

    # 6. 路径积分
    print(f"\n6. 路径积分:")
    pi = PathIntegral(frame=qf)
    for x in np.linspace(-1, 1, 5):
        pi.add_configuration(x + 0j)

    Z = pi.compute()
    print(f"   配分函数 Z = {Z:.4f}")

    config, action = pi.classical_limit()
    print(f"   经典解: φ_cl = {config:.4f}, S = {action:.4f}")

    # 7. 狄拉克符号导出
    print(f"\n7. 狄拉克符号导出:")
    print(f"   {qf.to_dirac_notation('position')}")
    print(f"   {qf.to_dirac_notation('momentum')}")

    print("\n" + "=" * 60)
    print("核心特性总结:")
    print("  • QFrame * e^{iθ} = 傅里叶变换")
    print("  • QFrame * λ = 共形变换")
    print("  • QFrame * QFrame = 标架复合")
    print("  • QFrame.det = 路径积分测度")
    print("=" * 60)


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 核心类
    'QFrame',
    'QuantumState',
    'PathIntegral',
    'QFrameSpectrum',

    # 狄拉克符号导出
    'DiracBra',
    'DiracKet',
    'bra',
    'ket',

    # 便利函数
    'spectral_transform',
    'inverse_spectral_transform',

    # 常数
    'HBAR',
    'GPU_AVAILABLE',
]


if __name__ == "__main__":
    demonstrate()
