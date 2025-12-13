"""
傅里叶标架场与希尔伯特空间谱几何 (Fourier Frame Field & Hilbert Space Spectral Geometry)
================================================================================

基于希尔伯特空间的傅里叶标架与谱分析框架。

核心思想：
- 傅里叶标架 = FourierFrame * e^{iθ} (相位旋转，傅里叶变换)
- 共形变换 = FourierFrame * λ (λ ∈ ℝ⁺, 缩放)
- 内禀梯度算子 G_μ = d/dx^μ log FourierFrame(x)
- 曲率 R_{μν} = [G_μ, G_ν]
- Berry相位 γ = ∮ G_μ dx^μ (几何相位，平行输运)
- 陈数 c₁ = (1/2π) ∬ R_{μν} dS (拓扑不变量)

数学框架：
- 希尔伯特空间：L²(M) 上的傅里叶分析
- 谱理论：拉普拉斯算子的本征值问题
- 纤维丛理论：FourierFrame 作为标架丛的局部截面
- 李群李代数：内禀梯度算子构成李代数
- 热核展开：几何不变量的提取

群论对应：
- FourierFrame ↔ GL(1,ℂ) = ℂ× = U(1) × ℝ⁺
- Phase e^{iθ} ↔ U(1) (单位圆)
- Magnitude |Q| ↔ ℝ⁺ (正实缩放)

Author: Quantum Frame Theory
Date: 2025-12-04
Version: 6.0.3
"""

__version__ = '6.0.3'

import numpy as np
from typing import List, Tuple, Dict, Optional, Union, Any, Callable
from dataclasses import dataclass
import warnings

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
# 傅里叶标架代数 (Fourier Frame Algebra)
# ============================================================

class FourierFrame:
    """
    傅里叶标架 - 希尔伯特空间上的频谱分析核心对象

    数学结构：
    -----------
    FourierFrame 对应 GL(1,ℂ) = ℂ× = U(1) × ℝ⁺ 群

    - Q ∈ ℂ× (非零复数)
    - Q = |Q| · e^{iθ}
      - Phase e^{iθ} ∈ U(1): 傅里叶变换（相位旋转）
      - Magnitude |Q| ∈ ℝ⁺: 共形变换（缩放）

    核心属性：
    ----------
    - base_coord: 基础坐标系 (coord3 对象)
    - Q: 复标度因子 Q ∈ ℂ×，编码相位与缩放

    关键变换：
    ----------
    - FourierFrame * e^{iθ} = 傅里叶变换 (θ=π/2 为标准 90° 旋转)
    - FourierFrame * λ = 共形变换 (λ ∈ ℝ⁺，纯缩放)
    - FourierFrame * FourierFrame = 标架复合

    希尔伯特空间意义：
    -----------------
    - L²(M) 空间上的傅里叶基
    - 内禀梯度算子 G_μ = d/dx^μ log Q(x)
    - 谱分解：Δφ_n = -λ_n φ_n
    - 热核：K(x,y,t) = Σ_n e^{-λ_n t} φ_n(x) φ_n*(y)

    几何意义：
    ----------
    - 作为标架丛 F(M) 的局部截面
    - 内禀梯度算子 G_μ 描述局部旋转
    - 曲率 R_{μν} = [G_μ, G_ν] 描述非交换性
    - Berry 相位 γ = ∮ G_μ dx^μ (平行输运)

    与 U3Frame 的关系：
    ------------------
    - FourierFrame: GL(1,ℂ) 群，1个复数自由度
    - U3Frame: U(3) 群，9个实自由度
    - U(3) ⊃ U(1) as global phase subgroup
    """

    def __init__(self, base_coord=None, q_factor=1.0+0j):
        """
        初始化傅里叶标架

        Args:
            base_coord: 基础坐标系 (coord3 对象)，None 时使用单位标架
            q_factor: 复标度因子 Q ∈ ℂ× = GL(1,ℂ)
                     Q = |Q| · e^{iθ}
                     - 相位 e^{iθ}: 傅里叶变换
                     - 模 |Q|: 共形缩放
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
        行列式: Det(Frame)

        用于路径积分测度 ∫ Dφ · Det[Frame] · exp(iS/ħ)
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
        - Frame * complex: 相位旋转/缩放 (傅里叶/共形变换)
        - Frame * Frame: 标架复合 (路径积分复合)
        - Frame * vec3: 向量变换
        """
        if isinstance(other, (int, float, complex)):
            # 标量乘法实现傅里叶/共形变换
            new_Q = self.Q * other
            return FourierFrame(self.base, new_Q)

        elif isinstance(other, FourierFrame):
            # 标架复合
            if self.base is not None and other.base is not None:
                new_base = self.base * other.base
            else:
                new_base = self.base or other.base
            new_Q = self.Q * other.Q
            return FourierFrame(new_base, new_Q)

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
            return FourierFrame(self.base, self.Q / other)
        elif isinstance(other, FourierFrame):
            if self.base is not None and other.base is not None:
                new_base = self.base / other.base
            else:
                new_base = self.base
            return FourierFrame(new_base, self.Q / other.Q)
        return NotImplemented

    def __pow__(self, n):
        """幂运算: 对应多次变换"""
        if isinstance(n, (int, float, complex)):
            return FourierFrame(self.base, self.Q ** n)
        return NotImplemented

    def __eq__(self, other):
        """相等比较"""
        if not isinstance(other, FourierFrame):
            return False
        return np.isclose(self.Q, other.Q)

    def __repr__(self):
        if self.base is not None:
            return f"FourierFrame(Q={self.Q:.4f}, o={self.base.o})"
        return f"FourierFrame(Q={self.Q:.4f})"

    # -------------------- 傅里叶变换 --------------------

    def fourier_transform(self, theta: float = np.pi/2) -> 'FourierFrame':
        """
        傅里叶变换: F_θ[FourierFrame] = FourierFrame · e^{iθ}

        Args:
            theta: 旋转角度，π/2 为标准傅里叶变换

        Returns:
            变换后的 FourierFrame

        性质：
        - F^4 = I (四次变换回到自身)
        - F^2 = P (宇称变换)
        """
        ft_factor = np.exp(1j * theta)
        return self * ft_factor

    def inverse_fourier_transform(self, theta: float = np.pi/2) -> 'FourierFrame':
        """逆傅里叶变换: F^{-1} = F_{-θ}"""
        return self.fourier_transform(-theta)

    def conformal_transform(self, lambda_factor: float) -> 'FourierFrame':
        """
        共形变换: FourierFrame → FourierFrame · λ, λ ∈ ℝ⁺

        实现缩放变换，保持角度不变
        """
        return self * lambda_factor

    # -------------------- 经典几何演化 --------------------

    def diffusion_evolution(self, t: float, kappa: float = 1.0) -> 'FourierFrame':
        """
        扩散演化算子: e^{tΔ} FourierFrame

        这是经典热方程 ∂u/∂t = κΔu 的解算子，其中：
        - Δ 是拉普拉斯算子（几何扩散算子）
        - t 是时间参数（实时间，非虚时间）
        - κ 是扩散系数

        数学形式：
        FourierFrame(x, t) = e^{tκΔ} FourierFrame(x, 0)
                           = FourierFrame₀ · e^{-tκ|k|²} （动量空间）

        物理意义：
        - 描述几何信息在流形上的扩散过程
        - 热核作为基本解：K(x,y,t) = (4πκt)^{-d/2} e^{-|x-y|²/(4κt)}
        - 谱几何中的核心工具，用于提取流形的几何不变量

        注意：这是**经典几何**的扩散过程，与量子力学的虚时间演化
        在形式上类似，但物理意义完全不同。

        Args:
            t: 扩散时间（必须 > 0）
            kappa: 扩散系数（默认1.0）

        Returns:
            扩散演化后的FourierFrame

        局限性：
        - 简化实现：仅对标度因子Q进行扩散
        - 完整实现需要在标架场上定义拉普拉斯算子
        - 数值实现受网格分辨率限制
        """
        if t < 0:
            raise ValueError("扩散时间t必须非负")

        # 简化模型：对Q因子进行衰减（高频抑制）
        # 完整实现需要在标架场的频谱表示中进行
        decay_factor = np.exp(-kappa * t * np.abs(self.Q)**2)
        evolved_Q = self.Q * decay_factor

        return FourierFrame(self.base, evolved_Q)

    @staticmethod
    def laplacian_from_field(frame_field: List[List['FourierFrame']],
                            i: int, j: int) -> complex:
        """
        从离散标架场计算拉普拉斯算子

        Δ log FourierFrame ≈ (∇² log FourierFrame)
                           = ∂²/∂x² log Q + ∂²/∂y² log Q

        Args:
            frame_field: 离散标架场
            i, j: 网格位置

        Returns:
            拉普拉斯算子作用结果（复数）

        数学细节：
        使用五点差分模板计算二阶导数：
        Δf ≈ [f(i+1,j) + f(i-1,j) + f(i,j+1) + f(i,j-1) - 4f(i,j)] / h²
        """
        ny, nx = len(frame_field), len(frame_field[0])

        if i <= 0 or i >= ny - 1 or j <= 0 or j >= nx - 1:
            return 0.0 + 0j

        # 中心点
        log_Q_center = np.log(frame_field[i][j].Q)

        # 四个邻居
        log_Q_xp = np.log(frame_field[i][j+1].Q)
        log_Q_xm = np.log(frame_field[i][j-1].Q)
        log_Q_yp = np.log(frame_field[i+1][j].Q)
        log_Q_ym = np.log(frame_field[i-1][j].Q)

        # 五点拉普拉斯模板（假设网格间距h=1）
        laplacian = (log_Q_xp + log_Q_xm + log_Q_yp + log_Q_ym - 4*log_Q_center)

        return laplacian

    # -------------------- 谱变换 --------------------

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
    def from_coord_field(cls, coord_field: List[List], hbar: float = HBAR) -> 'FourierFrameSpectrum':
        """
        从坐标场创建谱表示

        将坐标场的各分量进行谱变换

        Args:
            coord_field: 二维坐标场列表 [[coord3, ...], ...]
            hbar: 约化普朗克常数

        Returns:
            FourierFrameSpectrum 对象
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

        return FourierFrameSpectrum(
            ux_spectrum=ux_spectrum,
            uy_spectrum=uy_spectrum,
            uz_spectrum=uz_spectrum,
            origin_spectrum=origin_spectrum,
            momentum_grid=(kx, ky),
            hbar=hbar
        )


# ============================================================
# 内禀梯度算子 (Intrinsic Gradient Operator)
# ============================================================

class IntrinsicGradient:
    """
    内禀梯度算子 G_μ = d/dx^μ log FourierFrame(x)

    几何意义（经典谱几何视角）：
    - 描述标架的局部旋转速率（协变导数的对数形式）
    - 对应黎曼几何中的联络1-形式
    - 非交换性 [G_μ, G_ν] 直接给出曲率张量

    数学性质：
    - δFourierFrame = G_μ FourierFrame δx^μ （无穷小变换）
    - [G_μ, G_ν] = R_{μν} （曲率2-形式）
    - γ = ∮ G_μ dx^μ （几何相位 - parallel transport）
    - Δ = ∇² = ∂_μ ∂^μ （拉普拉斯算子）

    与量子理论的关系：
    - 形式上类似规范场论中的联络，但这里是**纯几何对象**
    - Berry相位在这里是经典几何相位（平行输运），非量子效应
    - 该理论完全在经典微分几何框架内
    """

    def __init__(self, frame_field: Union[Callable, List[List['FourierFrame']]]):
        """
        初始化内禀梯度算子

        Args:
            frame_field: 标架场，可以是函数或离散场
        """
        self.frame_field = frame_field
        self.is_discrete = isinstance(frame_field, list)

    def compute_at(self, position: Union[Tuple, int],
                   direction: int, delta: float = 1e-5) -> complex:
        """
        计算指定位置和方向的内禀梯度

        Args:
            position: 位置坐标 (连续) 或索引 (离散)
            direction: 方向索引 (0=x, 1=y, 2=z)
            delta: 有限差分步长

        Returns:
            G_μ 的复数值
        """
        if self.is_discrete:
            return self._compute_discrete(position, direction)
        else:
            return self._compute_continuous(position, direction, delta)

    def _compute_discrete(self, idx: Tuple[int, int], direction: int) -> complex:
        """离散场的内禀梯度"""
        i, j = idx
        ny, nx = len(self.frame_field), len(self.frame_field[0])

        # 中心差分
        if direction == 0:  # x方向
            if j + 1 < nx and j - 1 >= 0:
                frame_forward = self.frame_field[i][j + 1]
                frame_backward = self.frame_field[i][j - 1]
                frame_center = self.frame_field[i][j]

                # G_x ≈ (log Q_{j+1} - log Q_{j-1}) / 2
                return (np.log(frame_forward.Q) - np.log(frame_backward.Q)) / 2.0

        elif direction == 1:  # y方向
            if i + 1 < ny and i - 1 >= 0:
                frame_forward = self.frame_field[i + 1][j]
                frame_backward = self.frame_field[i - 1][j]

                return (np.log(frame_forward.Q) - np.log(frame_backward.Q)) / 2.0

        return 0.0 + 0j

    def _compute_continuous(self, pos: Tuple, direction: int, delta: float) -> complex:
        """连续场的内禀梯度"""
        pos_list = list(pos)

        # 前向和后向位置
        pos_forward = pos_list.copy()
        pos_backward = pos_list.copy()
        pos_forward[direction] += delta
        pos_backward[direction] -= delta

        frame_forward = self.frame_field(tuple(pos_forward))
        frame_backward = self.frame_field(tuple(pos_backward))

        # G_μ = d/dx^μ log Frame
        return (np.log(frame_forward.Q) - np.log(frame_backward.Q)) / (2 * delta)

    def commutator(self, pos: Union[Tuple, int],
                   dir1: int, dir2: int, delta: float = 1e-5) -> complex:
        """
        计算李括号 [G_μ, G_ν] = 曲率 R_{μν}

        Args:
            pos: 位置
            dir1, dir2: 两个方向索引
            delta: 有限差分步长

        Returns:
            曲率分量 R_{μν}
        """
        G_mu = self.compute_at(pos, dir1, delta)
        G_nu = self.compute_at(pos, dir2, delta)

        # 简化版本：[G_μ, G_ν] ≈ G_μ G_ν - G_ν G_μ
        # 对于阿贝尔情况（标量Q），交换子为0
        # 完整实现需要考虑标架场的非阿贝尔结构
        return G_mu * G_nu - G_nu * G_mu

    def laplacian(self, position: Union[Tuple[int, int], int]) -> complex:
        """
        拉普拉斯算子 Δ = ∇² = ∂²/∂x² + ∂²/∂y²

        作用于 log FourierFrame：
        Δ log FourierFrame = ∂²/∂x² log Q + ∂²/∂y² log Q

        这是谱几何的核心算子，其本征值问题：
        Δφ_n = -λ_n φ_n

        定义了流形的谱（spectrum），从而编码几何信息。

        Args:
            position: 网格位置 (i, j) 或索引

        Returns:
            拉普拉斯算子作用结果

        数学背景：
        - 拉普拉斯算子是黎曼流形上的自然微分算子
        - 其谱{λ_n}包含流形的几何不变量（Weyl律、热核展开）
        - "Can one hear the shape of a drum?" - Kac's问题
        """
        if not self.is_discrete:
            raise NotImplementedError("连续场的拉普拉斯算子需要额外实现")

        if isinstance(position, int):
            # 1D情况（简化）
            return 0.0 + 0j

        # 使用FourierFrame的静态方法
        return FourierFrame.laplacian_from_field(self.frame_field, position[0], position[1])


# ============================================================
# 曲率计算 (Curvature from Frames)
# ============================================================

class CurvatureFromFrame:
    """
    从标架场计算曲率

    核心公式：
    - R_{μν} = [G_μ, G_ν] = ∂_μ G_ν - ∂_ν G_μ - [G_μ, G_ν]
    - 高斯曲率 K = -⟨[G_u, G_v] e_v, e_u⟩ / √det(g)
    - 平均曲率 H = (1/2) Tr(R)
    """

    def __init__(self, frame_field: List[List['FourierFrame']]):
        """
        初始化曲率计算器

        Args:
            frame_field: 离散标架场
        """
        self.frame_field = frame_field
        self.gradient_op = IntrinsicGradient(frame_field)
        self.ny = len(frame_field)
        self.nx = len(frame_field[0]) if self.ny > 0 else 0

    def gaussian_curvature(self, i: int, j: int) -> float:
        """
        计算高斯曲率

        K = -⟨[G_u, G_v] e_v, e_u⟩ / √det(g)

        Args:
            i, j: 网格索引

        Returns:
            高斯曲率值
        """
        # 计算李括号 [G_x, G_y]
        R_xy = self.gradient_op.commutator((i, j), 0, 1)

        # 简化版本：K ≈ -Im(R_xy) (对于复标架)
        # 完整实现需要计算度量张量
        return -R_xy.imag

    def mean_curvature(self, i: int, j: int) -> float:
        """
        计算平均曲率

        H = (1/2) Tr(R)

        Args:
            i, j: 网格索引

        Returns:
            平均曲率值
        """
        # 简化实现
        R_xx = self.gradient_op.commutator((i, j), 0, 0)
        R_yy = self.gradient_op.commutator((i, j), 1, 1)

        return 0.5 * (R_xx.real + R_yy.real)

    def riemann_curvature_tensor(self, i: int, j: int) -> np.ndarray:
        """
        计算黎曼曲率张量

        R_{ijkl} = -√det(g) ⟨[G_i, G_j] e_l, e_k⟩

        Args:
            i, j: 网格索引

        Returns:
            曲率张量 (2x2 矩阵，简化2D情况)
        """
        R = np.zeros((2, 2), dtype=complex)

        R[0, 0] = self.gradient_op.commutator((i, j), 0, 0)
        R[0, 1] = self.gradient_op.commutator((i, j), 0, 1)
        R[1, 0] = self.gradient_op.commutator((i, j), 1, 0)
        R[1, 1] = self.gradient_op.commutator((i, j), 1, 1)

        return R


# ============================================================
# 几何相位 (Geometric Phase)
# ============================================================

class BerryPhase:
    """
    Berry相位计算

    几何相位公式：
    γ = ∮_C G_μ dx^μ = ∮_C (∂_μ Frame · Frame^{-1}) dx^μ

    性质：
    - 与路径参数化无关
    - 仅依赖于路径的几何形状
    - 对应曲率的面积分（Stokes定理）
    """

    def __init__(self, gradient_operator: IntrinsicGradient):
        """
        初始化Berry相位计算器

        Args:
            gradient_operator: 内禀梯度算子
        """
        self.gradient_op = gradient_operator

    def compute_along_path(self, path: List[Tuple], closed: bool = True) -> complex:
        """
        沿路径计算Berry相位

        γ = ∮_C G_μ dx^μ

        Args:
            path: 路径点列表 [(i1, j1), (i2, j2), ...]
            closed: 是否闭合路径

        Returns:
            几何相位（复数）
        """
        if len(path) < 2:
            return 0.0 + 0j

        phase = 0.0 + 0j

        for k in range(len(path) - 1):
            pos_current = path[k]
            pos_next = path[k + 1]

            # 确定方向
            dx = pos_next[0] - pos_current[0]
            dy = pos_next[1] - pos_current[1]

            # 计算梯度分量
            if abs(dx) > abs(dy):
                direction = 0  # x方向
                step = dx
            else:
                direction = 1  # y方向
                step = dy

            # G_μ dx^μ
            G_mu = self.gradient_op.compute_at(pos_current, direction)
            phase += G_mu * step

        # 闭合路径
        if closed and len(path) > 2:
            pos_last = path[-1]
            pos_first = path[0]

            dx = pos_first[0] - pos_last[0]
            dy = pos_first[1] - pos_last[1]

            if abs(dx) > abs(dy):
                direction = 0
                step = dx
            else:
                direction = 1
                step = dy

            G_mu = self.gradient_op.compute_at(pos_last, direction)
            phase += G_mu * step

        return phase


# ============================================================
# 陈数 (Chern Number)
# ============================================================

class ChernNumber:
    """
    第一陈数计算

    拓扑不变量：
    c₁ = (1/2π) ∬_M R_{μν} dS^{μν}
       = (1/2π) ∬_M Tr([G_μ, G_ν]) dS^{μν}

    物理意义：
    - 刻画纤维丛的拓扑性质
    - 量子霍尔效应中的拓扑不变量
    - 与Berry相位的关联（Stokes定理）
    """

    def __init__(self, curvature_calculator: CurvatureFromFrame):
        """
        初始化陈数计算器

        Args:
            curvature_calculator: 曲率计算器
        """
        self.curvature = curvature_calculator

    def compute(self) -> float:
        """
        计算第一陈数

        c₁ = (1/2π) Σ_{ij} R_{xy}(i,j) ΔS

        Returns:
            陈数（实数）
        """
        total = 0.0 + 0j

        ny, nx = self.curvature.ny, self.curvature.nx

        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                # 曲率 R_{xy}
                R_xy = self.curvature.gradient_op.commutator((i, j), 0, 1)
                total += R_xy

        # 归一化
        c1 = total / (2 * np.pi)

        # 陈数应为整数（拓扑不变量）
        return round(c1.real)


# ============================================================
# 谱分解 (Spectral Decomposition)
# ============================================================

class SpectralDecomposition:
    """
    拉普拉斯算子的谱分解（经典几何谱理论）

    数学框架：
    拉普拉斯本征值问题：
        Δφ_n = -λ_n φ_n
        ∫ φ_m φ_n dV = δ_{mn}

    谱分解定理：
        Δ = -Σ_n λ_n |φ_n⟩⟨φ_n|

    **FourierFrame作为本征态基础**：
    在我们的框架中，FourierFrame场可展开为本征态的叠加：

        FourierFrame(x) = Σ_n c_n φ_n(x) FourierFrame_n

    其中：
    - φ_n(x) 是拉普拉斯算子的标量本征函数
    - FourierFrame_n 是对应的标架本征态
    - c_n = ⟨φ_n | FourierFrame⟩ 是展开系数

    谱的几何意义：
    - {λ_n} 编码流形的几何信息（形状DNA）
    - 低频模式（小λ）对应大尺度几何特征
    - 高频模式（大λ）对应局部细节

    Weyl渐近律：
        N(λ) ~ (ω_d / (2π)^d) Vol(M) λ^{d/2}

    其中 N(λ) 是小于λ的本征值个数。

    应用：
    - ShapeDNA：谱签名用于形状识别
    - 谱距离：流形间的几何距离度量
    - 多尺度分析：不同频段的几何特征
    - 热核展开：Tr(e^{tΔ}) = Σ_n e^{-tλ_n}
    """

    def __init__(self, frame_field: Union[List[List['FourierFrame']], 'FourierFrameSpectrum']):
        """
        初始化谱分解

        Args:
            frame_field: FourierFrame场或其频谱表示
        """
        if isinstance(frame_field, list):
            # 离散标架场
            self.frame_field = frame_field
            self.gradient_op = IntrinsicGradient(frame_field)
            self.ny = len(frame_field)
            self.nx = len(frame_field[0]) if self.ny > 0 else 0
            self.spectrum = None
        else:
            # 频谱表示
            self.spectrum = frame_field
            self.frame_field = None
            self.gradient_op = None
            self.ny, self.nx = frame_field.shape

        self._eigenvalues = None
        self._eigenvectors = None

    def compute_eigenspectrum(self) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        计算拉普拉斯算子的本征谱

        Returns:
            (eigenvalues, eigenvectors)
            - eigenvalues: λ_n 数组（降序排列）
            - eigenvectors: 本征函数φ_n（简化实现可能为None）

        数值方法：
        对于频谱表示，本征值对应 k² = |k|²
        对于离散场，需要构造拉普拉斯矩阵并求解
        """
        if self._eigenvalues is not None:
            return self._eigenvalues, self._eigenvectors

        if self.spectrum is not None:
            # 频谱表示：本征值 = k²
            kx, ky = self.spectrum.momentum_grid
            k2 = kx[:, None]**2 + ky[None, :]**2

            # 展平并排序（降序）
            eigenvalues = np.sort(k2.flatten())[::-1]

            self._eigenvalues = eigenvalues
            self._eigenvectors = None

        elif self.frame_field is not None:
            # 离散场：估算本征值
            # 完整实现需要构造拉普拉斯矩阵并数值求解
            eigenvalues_list = []

            for i in range(1, self.ny - 1):
                for j in range(1, self.nx - 1):
                    lap = self.gradient_op.laplacian((i, j))
                    eigenvalues_list.append(abs(lap))

            eigenvalues = np.sort(np.array(eigenvalues_list))[::-1]
            self._eigenvalues = eigenvalues
            self._eigenvectors = None

        return self._eigenvalues, self._eigenvectors

    def expand_frame_in_eigenbasis(self, frame: 'FourierFrame',
                                   n_modes: int = 10) -> np.ndarray:
        """
        将FourierFrame展开到本征态基底

        FourierFrame = Σ_n c_n FourierFrame_n

        Args:
            frame: 要展开的FourierFrame
            n_modes: 使用的模式数量

        Returns:
            展开系数 c_n

        数学细节：
        c_n = ∫ φ_n*(x) FourierFrame(x) dV

        简化实现：使用傅里叶系数作为近似
        """
        eigenvalues, _ = self.compute_eigenspectrum()

        # 简化：使用FourierFrame的Q因子
        coefficients = np.zeros(n_modes, dtype=complex)
        q_value = frame.Q

        for n in range(min(n_modes, len(eigenvalues))):
            # 简化投影：c_n ∝ Q / √λ_n
            if eigenvalues[n] > 0:
                coefficients[n] = q_value / np.sqrt(eigenvalues[n])

        return coefficients

    def reconstruct_from_modes(self, coefficients: np.ndarray,
                               base_frame: 'FourierFrame') -> 'FourierFrame':
        """
        从本征模式重建FourierFrame

        FourierFrame = Σ_n c_n FourierFrame_n

        Args:
            coefficients: 展开系数
            base_frame: 基础标架

        Returns:
            重建的FourierFrame
        """
        eigenvalues, _ = self.compute_eigenspectrum()

        reconstructed_Q = 0.0 + 0j
        for n in range(len(coefficients)):
            if n < len(eigenvalues) and eigenvalues[n] > 0:
                reconstructed_Q += coefficients[n] * np.sqrt(eigenvalues[n])

        return FourierFrame(base_frame.base, reconstructed_Q)

    def weyl_counting(self, lambda_threshold: float) -> int:
        """
        Weyl渐近计数函数

        N(λ) = #{n : λ_n < λ}  （小于λ的本征值个数）

        Weyl律：
        N(λ) ~ (ω_d / (2π)^d) Vol(M) λ^{d/2}  (λ → ∞)

        对于2维流形：N(λ) ~ (1/4π) Area(M) λ

        Args:
            lambda_threshold: 本征值阈值λ

        Returns:
            N(λ) - 本征值个数
        """
        eigenvalues, _ = self.compute_eigenspectrum()
        return int(np.sum(eigenvalues < lambda_threshold))

    def shape_dna(self, n_modes: int = 50) -> np.ndarray:
        """
        形状DNA（ShapeDNA）- 流形的谱签名

        前n个本征值 {λ_1, λ_2, ..., λ_n} 唯一标识流形的几何形状
        （在同谱异构的情况下）

        这是谱几何中的核心概念：
        "Can one hear the shape of a drum?" - Mark Kac (1966)

        对于2维流形，谱通常可以听出形状，但存在反例
        （Gordon-Webb-Wolpert, 1992）

        Args:
            n_modes: 模式数量（默认50）

        Returns:
            前n个本征值构成的谱签名

        应用：
        - 形状识别与检索
        - 几何相似性度量
        - 拓扑不变量提取
        """
        eigenvalues, _ = self.compute_eigenspectrum()
        return eigenvalues[:n_modes]


# ============================================================
# 热核 (Heat Kernel)
# ============================================================

class HeatKernel:
    """
    热核 - 热方程的基本解（经典几何谱分析）

    数学定义：
    ∂u/∂t = Δu  （热方程）
    K(x, y, t) = 基本解满足: ∂K/∂t = Δ_x K, K(x,y,0) = δ(x-y)

    热核的谱展开：
    K(x, y, t) = Σ_n e^{-λ_n t} φ_n(x) φ_n(y)

    其中 {λ_n, φ_n} 是拉普拉斯算子 Δφ_n = -λ_n φ_n 的本征系统。

    热核迹的渐近展开（Minakshisundaram-Pleijel）：
    Tr(e^{tΔ}) ~ (4πt)^{-d/2} Σ_k a_k t^k

    热核系数 {a_k} 编码流形的几何不变量：
    - a₀ = Vol(M)  （体积）
    - a₁ ∝ ∫ R dV  （曲率积分）
    - a₂ ∝ ∫ (R² + 其他曲率不变量) dV

    **FourierFrame作为数学基础**：
    在我们的框架中，热核作为FourierFrame在扩散过程中的演化算子：

    FourierFrame(x, t) = ∫ K(x, y, t) FourierFrame(y, 0) dy
                       = e^{tΔ} FourierFrame(x, 0)

    这将FourierFrame场视为"温度分布"，热核描述其扩散传播。

    **与量子理论的关系及局限性**：
    - 热核在形式上等价于量子力学的虚时间传播子（Wick旋转）
    - 但这里是**纯几何**的扩散过程，非量子演化
    - 不涉及态矢量、算符期望值等量子概念
    - 适用于经典计算机的数值计算

    应用：
    - 形状识别（ShapeDNA）
    - 几何不变量提取
    - 多尺度几何分析
    - 流形谱距离
    """

    def __init__(self, frame_field: Union[List[List['FourierFrame']], 'FourierFrameSpectrum']):
        """
        初始化热核

        Args:
            frame_field: FourierFrame场（离散）或其频谱表示
        """
        if isinstance(frame_field, list):
            # 离散标架场
            self.frame_field = frame_field
            self.gradient_op = IntrinsicGradient(frame_field)
            self.ny = len(frame_field)
            self.nx = len(frame_field[0]) if self.ny > 0 else 0
            self.spectrum = None
        else:
            # 频谱表示
            self.spectrum = frame_field
            self.frame_field = None
            self.gradient_op = None
            self.ny, self.nx = frame_field.shape

    def evolution_operator(self, t: float, kappa: float = 1.0) -> Union[np.ndarray, List[List['FourierFrame']]]:
        """
        热核演化算子: e^{tκΔ} FourierFrame

        计算标架场在时间t后的扩散状态。

        Args:
            t: 扩散时间（>0）
            kappa: 扩散系数（默认1.0）

        Returns:
            演化后的标架场

        数学细节：
        在频域中，热核演化简单地是：
        FourierFrame(k, t) = e^{-κt|k|²} FourierFrame(k, 0)

        这是高频抑制（低通滤波），对应空间的平滑化。
        """
        if t < 0:
            raise ValueError("扩散时间必须非负")

        if self.frame_field is not None:
            # 离散场：逐点演化
            evolved_field = []
            for i in range(self.ny):
                row = []
                for j in range(self.nx):
                    evolved_frame = self.frame_field[i][j].diffusion_evolution(t, kappa)
                    row.append(evolved_frame)
                evolved_field.append(row)
            return evolved_field

        elif self.spectrum is not None:
            # 频谱表示：频域衰减
            kx, ky = self.spectrum.momentum_grid
            k2 = kx[:, None]**2 + ky[None, :]**2

            # e^{-κt k²} 衰减因子
            decay = np.exp(-kappa * t * k2)

            # 应用到各分量
            evolved_spectrum = FourierFrameSpectrum(
                ux_spectrum=self.spectrum.ux_spectrum * decay[..., None],
                uy_spectrum=self.spectrum.uy_spectrum * decay[..., None],
                uz_spectrum=self.spectrum.uz_spectrum * decay[..., None],
                origin_spectrum=self.spectrum.origin_spectrum * decay[..., None],
                momentum_grid=self.spectrum.momentum_grid,
                hbar=self.spectrum.hbar
            )
            return evolved_spectrum

        else:
            raise ValueError("需要提供标架场或频谱")

    def trace(self, t: float, kappa: float = 1.0) -> float:
        """
        热核迹：Tr(e^{tκΔ}) = Σ_n e^{-κt λ_n}

        这是几何信息的凝聚，包含流形谱的全部信息。

        Args:
            t: 扩散时间
            kappa: 扩散系数

        Returns:
            热核迹值
        """
        if self.spectrum is not None:
            # 使用频谱表示
            density = self.spectrum.spectral_density()
            kx, ky = self.spectrum.momentum_grid
            k2 = kx[:, None]**2 + ky[None, :]**2

            # Tr(e^{-κt Δ}) = Σ e^{-κt k²}
            trace_val = np.sum(np.exp(-kappa * t * k2))
            return float(trace_val)

        elif self.frame_field is not None:
            # 简化估计：使用标架场的"能量"
            total = 0.0
            for i in range(self.ny):
                for j in range(self.nx):
                    laplacian = self.gradient_op.laplacian((i, j))
                    # e^{-t λ} ≈ 1 - tλ （小t近似）
                    total += np.exp(-kappa * t * abs(laplacian))
            return total

        return 0.0

    def asymptotic_expansion(self, t: float, kappa: float = 1.0, order: int = 2) -> float:
        """
        热核迹的渐近展开（Minakshisundaram-Pleijel公式）

        Tr(e^{tκΔ}) ~ (4πκt)^{-d/2} [a₀ + a₁(κt) + a₂(κt)² + ...]

        Args:
            t: 扩散时间（小t渐近）
            kappa: 扩散系数
            order: 展开阶数（默认2）

        Returns:
            渐近估计值

        几何意义：
        - a₀ = Vol(M) - 流形体积
        - a₁ ∝ ∫ R dV - 标量曲率积分
        - a₂ ∝ ∫ (R² - |Ric|² + ...) dV - 更高阶曲率不变量
        """
        d = 2  # 2维流形
        prefactor = (4 * np.pi * kappa * t) ** (-d / 2)

        # 估算热核系数
        a0 = float(self.ny * self.nx)  # 体积（网格点数）

        # a₁ 需要曲率信息
        if self.gradient_op is not None:
            curvature_sum = 0.0
            for i in range(1, self.ny - 1):
                for j in range(1, self.nx - 1):
                    R_xy = self.gradient_op.commutator((i, j), 0, 1)
                    curvature_sum += abs(R_xy)
            a1 = curvature_sum / 6.0
        else:
            a1 = 0.0

        a2 = 0.0  # 简化

        # 渐近级数
        expansion = a0
        if order >= 1:
            expansion += a1 * (kappa * t)
        if order >= 2:
            expansion += a2 * (kappa * t)**2

        return prefactor * expansion


# ============================================================
# 频率投影 (Frequency Projection)
# ============================================================

class FrequencyProjection:
    """
    几何频率投影算子

    ω_n = √|κ_n| · sign(κ_n)
    P_Ω = Σ_{n: ω_n ∈ Ω} |Frame_n⟩⟨Frame_n|

    应用：
    - 频段滤波
    - 多尺度分析
    - 频域波函数
    """

    def __init__(self, spectral_decomposition: SpectralDecomposition):
        """
        初始化频率投影

        Args:
            spectral_decomposition: 谱分解
        """
        self.spectral = spectral_decomposition

    def compute_frequencies(self) -> np.ndarray:
        """
        计算几何频率：ω_n = √|κ_n| · sign(κ_n)

        Returns:
            频率数组
        """
        eigenvalues, _ = self.spectral.compute_eigenspectrum()
        frequencies = np.sqrt(np.abs(eigenvalues)) * np.sign(eigenvalues)
        return frequencies

    def project_to_band(self, omega_min: float, omega_max: float) -> 'FrequencyBandState':
        """
        投影到频段 [ω_min, ω_max]

        Args:
            omega_min, omega_max: 频段范围

        Returns:
            频段态
        """
        frequencies = self.compute_frequencies()
        mask = (frequencies >= omega_min) & (frequencies <= omega_max)

        selected_indices = np.where(mask)[0]

        return FrequencyBandState(
            frequency_range=(omega_min, omega_max),
            mode_indices=selected_indices,
            projection_operator=self
        )


@dataclass
class FrequencyBandState:
    """频段波函数"""
    frequency_range: Tuple[float, float]
    mode_indices: np.ndarray
    projection_operator: FrequencyProjection

    def wavefunction(self, amplitudes: np.ndarray, phases: np.ndarray) -> complex:
        """
        Ψ_Ω = Σ_{n ∈ Ω} a_n Frame_n e^{iθ_n}

        Args:
            amplitudes: 振幅数组
            phases: 相位数组

        Returns:
            波函数值
        """
        psi = 0.0 + 0j
        for idx, amp, phase in zip(self.mode_indices, amplitudes, phases):
            psi += amp * np.exp(1j * phase)
        return psi


# ============================================================
# ============================================================
# 谱数据结构
# ============================================================

@dataclass
class FourierFrameSpectrum:
    """
    傅里叶标架谱表示 - 坐标场在动量空间的表示

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

        origin_field = Frame.inverse_spectral_transform_2d(self.origin_spectrum, self.hbar)
        ux_field = Frame.inverse_spectral_transform_2d(self.ux_spectrum, self.hbar)
        uy_field = Frame.inverse_spectral_transform_2d(self.uy_spectrum, self.hbar)
        uz_field = Frame.inverse_spectral_transform_2d(self.uz_spectrum, self.hbar)

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
# 便利函数
# ============================================================

def spectral_transform(coord_field: List[List],
                       hbar: float = HBAR,
                       use_gpu: bool = False) -> FourierFrameSpectrum:
    """
    坐标场谱变换

    Args:
        coord_field: 二维坐标场
        hbar: 约化普朗克常数
        use_gpu: 是否使用 GPU 加速

    Returns:
        FourierFrameSpectrum 对象
    """
    return FourierFrame.from_coord_field(coord_field, hbar)


def inverse_spectral_transform(spectrum: FourierFrameSpectrum) -> List[List]:
    """
    逆谱变换

    Args:
        spectrum: FourierFrameSpectrum 对象

    Returns:
        重建的坐标场
    """
    return spectrum.to_coord_field()


# ============================================================
# 演示
# ============================================================

def demonstrate():
    """演示傅里叶标架代数与谱几何"""
    print("=" * 70)
    print("傅里叶标架场与量子谱几何 (FourierFrame Field & Spectral Geometry)")
    print("=" * 70)

    # 1. 创建基础 FourierFrame
    if coord3 is not None:
        base_frame = coord3.from_position(vec3(1, 0, 0))
        frame = FourierFrame(base_frame, q_factor=1.0+0.5j)
    else:
        frame = FourierFrame(q_factor=1.0+0.5j)

    print(f"\n1. 基础傅里叶标架: {frame}")
    print(f"   相位: {frame.phase:.4f} rad")
    print(f"   模: {frame.magnitude:.4f}")
    print(f"   行列式: {frame.det:.4f}")

    # 2. 傅里叶变换
    print(f"\n2. 傅里叶变换:")
    ft = frame.fourier_transform()
    print(f"   F[FourierFrame] = {ft}")
    print(f"   F^4[FourierFrame] ≈ FourierFrame: {frame.fourier_transform(2*np.pi)}")

    # 3. 共形变换
    print(f"\n3. 共形变换:")
    conf = frame.conformal_transform(2.0)
    print(f"   λ=2: {conf}")

    # 4. 标架复合
    print(f"\n4. 标架复合:")
    frame2 = FourierFrame(q_factor=0.5+0.5j)
    composed = frame * frame2
    print(f"   FourierFrame1 * FourierFrame2 = {composed}")

    # 5. 内禀梯度算子
    print(f"\n5. 内禀梯度算子:")
    # 创建简单标架场
    frame_field = [[FourierFrame(q_factor=1.0 + 0.1j*(i+j)) for j in range(5)] for i in range(5)]
    grad_op = IntrinsicGradient(frame_field)
    G_x = grad_op.compute_at((2, 2), 0)
    G_y = grad_op.compute_at((2, 2), 1)
    print(f"   G_x(2,2) = {G_x:.4f}")
    print(f"   G_y(2,2) = {G_y:.4f}")

    # 6. 曲率计算
    print(f"\n6. 曲率计算:")
    curvature_calc = CurvatureFromFrame(frame_field)
    K = curvature_calc.gaussian_curvature(2, 2)
    H = curvature_calc.mean_curvature(2, 2)
    print(f"   高斯曲率 K = {K:.6f}")
    print(f"   平均曲率 H = {H:.6f}")

    # 7. Berry相位
    print(f"\n7. Berry相位:")
    berry = BerryPhase(grad_op)
    path = [(1, 1), (1, 3), (3, 3), (3, 1), (1, 1)]
    gamma = berry.compute_along_path(path, closed=True)
    print(f"   γ = ∮ G_μ dx^μ = {gamma:.4f}")

    # 8. 陈数
    print(f"\n8. 陈数:")
    chern = ChernNumber(curvature_calc)
    c1 = chern.compute()
    print(f"   第一陈数 c₁ = {c1}")

    print("\n" + "=" * 70)
    print("核心公式总结:")
    print("  • G_μ = d/dx^μ log FourierFrame(x)  [内禀梯度]")
    print("  • R_{μν} = [G_μ, G_ν]  [曲率]")
    print("  • FourierFrame * e^{iθ} = 傅里叶变换")
    print("  • FourierFrame * λ = 共形变换")
    print("  • γ = ∮ G_μ dx^μ  [Berry相位]")
    print("  • c₁ = (1/2π) ∬ R_{μν} dS  [陈数]")
    print("=" * 70)


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 核心类
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

    # 便利函数
    'spectral_transform',
    'inverse_spectral_transform',

    # 常数
    'HBAR',
    'GPU_AVAILABLE',
]


if __name__ == "__main__":
    demonstrate()
