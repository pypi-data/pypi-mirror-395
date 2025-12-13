"""
U(3) 复标架与规范场统一框架
================================================================================

基于《复标架与规范场统一纲领》的完整实现

核心理论：
- 复标架 U(x) ∈ U(3) 作为时空与规范场的统一结构
- 对称性破缺链：SU(4) → SU(3) × SU(2) × U(1)
- 虚时间嵌入：ℝ³ × iℝ → 内部旋转自由度
- 规范场作为复标架联络：A_μ ∈ 𝔲(3)
- 三个相位角对应颜色自由度（红、绿、蓝）

Author: Enhanced by AI following theoretical framework
Date: 2025-12-04
Version: 7.0.0-alpha
"""

__version__ = '7.0.0-alpha'

import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass
import warnings

# 尝试导入基础坐标系统
try:
    from .coordinate_system import coord3, vec3, quat
except ImportError:
    try:
        from coordinate_system import coord3, vec3, quat
    except ImportError:
        coord3 = None
        vec3 = None
        quat = None

# 物理常数
HBAR = 1.0  # 约化普朗克常数（自然单位制）
C_SPEED = 1.0  # 光速（自然单位制）


# ============================================================
# U(3) 复标架类
# ============================================================

class U3Frame:
    """
    U(3) 复标架 - 完整的三维酉矩阵标架

    数学形式：
        U(x) = [e₁(x), e₂(x), e₃(x)] ∈ U(3)

    其中每个基向量 eₖ = aₖ + ibₖ ∈ ℂ³ 满足：
        ⟨eⱼ, eₖ⟩ = δⱼₖ  (复内积)
        det(U) = e^{iφ}  (相位自由度)

    对称性分解：
        U(3) ⊃ SU(3) × U(1)
        SU(3) ⊃ SU(2) × U(1)

    物理诠释：
        - 实部 Re(eₖ)：空间方向矢量
        - 虚部 Im(eₖ)：虚时间演化方向
        - 三个相位角 (θ₁, θ₂, θ₃)：颜色自由度（红、绿、蓝）
    """

    def __init__(self,
                 e1: Optional[np.ndarray] = None,
                 e2: Optional[np.ndarray] = None,
                 e3: Optional[np.ndarray] = None,
                 ensure_unitary: bool = True):
        """
        初始化 U(3) 复标架

        Args:
            e1, e2, e3: 三个复基向量，每个形状为 (3,) 的复数组
            ensure_unitary: 是否确保酉性
        """
        if e1 is None:
            # 默认：单位标架
            self.e1 = np.array([1.0+0j, 0.0+0j, 0.0+0j], dtype=complex)
            self.e2 = np.array([0.0+0j, 1.0+0j, 0.0+0j], dtype=complex)
            self.e3 = np.array([0.0+0j, 0.0+0j, 1.0+0j], dtype=complex)
        else:
            self.e1 = np.array(e1, dtype=complex)
            self.e2 = np.array(e2, dtype=complex)
            self.e3 = np.array(e3, dtype=complex)

        if ensure_unitary:
            self._gram_schmidt_orthonormalize()

    # -------------------- 基础属性 --------------------

    @property
    def matrix(self) -> np.ndarray:
        """
        U(3) 矩阵表示

        Returns:
            3×3 复矩阵 [e₁ | e₂ | e₃]
        """
        return np.column_stack([self.e1, self.e2, self.e3])

    @property
    def determinant(self) -> complex:
        """
        行列式 det(U) = e^{iφ}

        对于 U(3)：|det(U)| = 1
        """
        return np.linalg.det(self.matrix)

    @property
    def global_phase(self) -> float:
        """
        全局相位 φ = arg(det(U))

        对应 U(1) 整体规范变换
        """
        return np.angle(self.determinant)

    @property
    def real_part(self) -> np.ndarray:
        """实部：空间标架"""
        return np.column_stack([self.e1.real, self.e2.real, self.e3.real])

    @property
    def imag_part(self) -> np.ndarray:
        """虚部：虚时间方向"""
        return np.column_stack([self.e1.imag, self.e2.imag, self.e3.imag])

    # -------------------- 对称性分解 --------------------

    def to_su3_u1(self) -> Tuple['SU3Component', complex]:
        """
        分解为 SU(3) × U(1)

        U(3) = SU(3) × U(1)
        U = (det U)^{1/3} · V

        其中 V ∈ SU(3), det(V) = 1

        Returns:
            (su3_component, u1_phase)
        """
        det_u = self.determinant
        u1_phase = det_u ** (1/3)  # ∛det(U)

        # 归一化到 SU(3)
        V_matrix = self.matrix / u1_phase

        return SU3Component(V_matrix), u1_phase

    def color_phases(self) -> Tuple[float, float, float]:
        """
        提取颜色相位角 (θ₁, θ₂, θ₃)

        对于对角化的复标架：
            U = diag(e^{iθ₁}, e^{iθ₂}, e^{iθ₃})

        约束：θ₁ + θ₂ + θ₃ = φ (全局相位)

        Returns:
            (θ_red, θ_green, θ_blue)
        """
        # 提取对角元素的相位
        diag = np.diag(self.matrix)
        phases = np.angle(diag)

        return tuple(phases)

    def to_quaternion_representation(self) -> Tuple[complex, complex, complex, complex]:
        """
        转换为四元数表示（仅 SU(2) 子群）

        SU(2) ⊂ SU(3) 对应四元数 q = a + bi + cj + dk

        Returns:
            (q0, q1, q2, q3) 四元数分量
        """
        # 提取左上 2×2 子矩阵（对应 SU(2)）
        su2_block = self.matrix[:2, :2]

        # SU(2) → 四元数
        # U = [[a+ib, -c+id], [c+id, a-ib]]
        a = su2_block[0, 0].real
        b = su2_block[0, 0].imag
        c = su2_block[1, 0].real
        d = su2_block[1, 0].imag

        # 归一化
        norm = np.sqrt(a**2 + b**2 + c**2 + d**2)
        if norm > 1e-10:
            return (a/norm, b/norm, c/norm, d/norm)
        else:
            return (1.0, 0.0, 0.0, 0.0)

    # -------------------- 规范变换 --------------------

    def gauge_transform_u1(self, phi: float) -> 'U3Frame':
        """
        U(1) 整体规范变换

        U → e^{iφ} U

        Args:
            phi: 规范相位

        Returns:
            变换后的标架
        """
        factor = np.exp(1j * phi)
        return U3Frame(
            e1=self.e1 * factor,
            e2=self.e2 * factor,
            e3=self.e3 * factor,
            ensure_unitary=False
        )

    def gauge_transform_su2(self, pauli_vector: Tuple[float, float, float]) -> 'U3Frame':
        """
        SU(2) 规范变换（作用在前两个基向量）

        对应弱相互作用规范群

        Args:
            pauli_vector: (θ_x, θ_y, θ_z) 泡利矢量参数

        Returns:
            变换后的标架
        """
        θ_x, θ_y, θ_z = pauli_vector
        θ = np.sqrt(θ_x**2 + θ_y**2 + θ_z**2)

        if θ < 1e-10:
            return self

        # SU(2) 矩阵：exp(i θ·σ/2)
        n = np.array([θ_x, θ_y, θ_z]) / θ
        cos_half = np.cos(θ/2)
        sin_half = np.sin(θ/2)

        # 构造 SU(2) 矩阵
        su2_matrix = np.array([
            [cos_half + 1j*n[2]*sin_half, (1j*n[0] + n[1])*sin_half],
            [(1j*n[0] - n[1])*sin_half, cos_half - 1j*n[2]*sin_half]
        ], dtype=complex)

        # 应用到前两个基向量
        e12_block = np.column_stack([self.e1[:2], self.e2[:2]])
        e12_transformed = e12_block @ su2_matrix

        new_e1 = np.concatenate([e12_transformed[:, 0], [self.e1[2]]])
        new_e2 = np.concatenate([e12_transformed[:, 1], [self.e2[2]]])

        return U3Frame(e1=new_e1, e2=new_e2, e3=self.e3, ensure_unitary=False)

    def gauge_transform_su3(self, gell_mann_params: np.ndarray) -> 'U3Frame':
        """
        SU(3) 规范变换（胶子变换）

        对应强相互作用规范群（QCD）

        Args:
            gell_mann_params: 8个Gell-Mann矩阵参数 (θ₁, ..., θ₈)

        Returns:
            变换后的标架
        """
        if len(gell_mann_params) != 8:
            raise ValueError("SU(3) 需要 8 个参数（Gell-Mann 矩阵）")

        # 构造 SU(3) 矩阵：exp(i Σₐ θₐ λₐ/2)
        su3_matrix = self._build_su3_matrix(gell_mann_params)

        # 应用变换
        new_matrix = self.matrix @ su3_matrix

        return U3Frame(
            e1=new_matrix[:, 0],
            e2=new_matrix[:, 1],
            e3=new_matrix[:, 2],
            ensure_unitary=False
        )

    # -------------------- 虚时间演化 --------------------

    def imaginary_time_evolution(self, tau: float, hamiltonian: Optional[np.ndarray] = None) -> 'U3Frame':
        """
        虚时间演化算子：exp(-τĤ)

        对应威克旋转：t → -iτ

        数学形式：
            U(τ) = exp(-τĤ) U(0)

        物理意义：
            - τ > 0: 虚时间参数（热力学β = 1/kT）
            - Ĥ: 哈密顿算符（能量算符）
            - 与路径积分的联系：Z = Tr[exp(-βĤ)]

        Args:
            tau: 虚时间参数
            hamiltonian: 3×3 厄米矩阵（默认使用标准拉普拉斯）

        Returns:
            演化后的标架
        """
        if hamiltonian is None:
            # 默认：使用简单的对角哈密顿量
            hamiltonian = np.diag([1.0, 1.0, 1.0])

        # 演化算符：exp(-τĤ)
        evolution_op = scipy_expm(-tau * hamiltonian)

        # 应用到标架
        new_matrix = evolution_op @ self.matrix

        return U3Frame(
            e1=new_matrix[:, 0],
            e2=new_matrix[:, 1],
            e3=new_matrix[:, 2],
            ensure_unitary=False
        )

    def wick_rotation(self, real_time: float) -> 'U3Frame':
        """
        威克旋转：t → -iτ

        将实时间演化转为虚时间演化

        Args:
            real_time: 实时间 t

        Returns:
            威克旋转后的标架（虚时间 τ = it）
        """
        tau = -1j * real_time
        return self.imaginary_time_evolution(tau.imag)

    # -------------------- 内部方法 --------------------

    def _gram_schmidt_orthonormalize(self):
        """Gram-Schmidt 正交归一化"""
        # e1 归一化
        norm1 = np.sqrt(np.vdot(self.e1, self.e1).real)
        if norm1 > 1e-10:
            self.e1 = self.e1 / norm1

        # e2 正交化并归一化
        self.e2 = self.e2 - np.vdot(self.e1, self.e2) * self.e1
        norm2 = np.sqrt(np.vdot(self.e2, self.e2).real)
        if norm2 > 1e-10:
            self.e2 = self.e2 / norm2

        # e3 正交化并归一化
        self.e3 = self.e3 - np.vdot(self.e1, self.e3) * self.e1 - np.vdot(self.e2, self.e3) * self.e2
        norm3 = np.sqrt(np.vdot(self.e3, self.e3).real)
        if norm3 > 1e-10:
            self.e3 = self.e3 / norm3

    def _build_su3_matrix(self, params: np.ndarray) -> np.ndarray:
        """构造 SU(3) 矩阵"""
        # Gell-Mann 矩阵（λ₁ 到 λ₈）
        lambda_matrices = self._gell_mann_matrices()

        # 线性组合
        generator = sum(params[i] * lambda_matrices[i] for i in range(8))

        # 指数映射
        return scipy_expm(1j * generator)

    @staticmethod
    def _gell_mann_matrices() -> List[np.ndarray]:
        """Gell-Mann 矩阵（SU(3) 生成元）"""
        λ = [
            # λ₁
            np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
            # λ₂
            np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
            # λ₃
            np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
            # λ₄
            np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
            # λ₅
            np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
            # λ₆
            np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
            # λ₇
            np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
            # λ₈
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
        ]
        return λ

    # -------------------- 运算符重载 --------------------

    def __mul__(self, other):
        """标架乘法或标量乘法"""
        if isinstance(other, (int, float, complex)):
            # 标量乘法
            return U3Frame(
                e1=self.e1 * other,
                e2=self.e2 * other,
                e3=self.e3 * other,
                ensure_unitary=False
            )
        elif isinstance(other, U3Frame):
            # 矩阵乘法
            new_matrix = self.matrix @ other.matrix
            return U3Frame(
                e1=new_matrix[:, 0],
                e2=new_matrix[:, 1],
                e3=new_matrix[:, 2],
                ensure_unitary=False
            )
        return NotImplemented

    def __repr__(self):
        phases = self.color_phases()
        return f"U3Frame(phases=(R:{phases[0]:.3f}, G:{phases[1]:.3f}, B:{phases[2]:.3f}), φ={self.global_phase:.3f})"


# ============================================================
# SU(3) 分量类
# ============================================================

@dataclass
class SU3Component:
    """
    SU(3) 分量（强相互作用规范群）

    性质：
        - det(V) = 1
        - V† V = I
        - 8 个生成元（Gell-Mann 矩阵）

    物理意义：
        - 对应量子色动力学（QCD）
        - 8 个胶子场
        - 颜色荷守恒
    """
    matrix: np.ndarray  # 3×3 SU(3) 矩阵

    def __post_init__(self):
        """验证 SU(3) 性质"""
        det = np.linalg.det(self.matrix)
        if not np.isclose(abs(det), 1.0, atol=1e-6):
            warnings.warn(f"SU(3) 矩阵行列式不为 1: |det|={abs(det):.6f}")

    def to_gell_mann_params(self) -> np.ndarray:
        """
        分解为 Gell-Mann 矩阵参数

        V = exp(i Σₐ θₐ λₐ)

        Returns:
            8 个参数 (θ₁, ..., θ₈)
        """
        # 取对数
        log_v = scipy_logm(self.matrix)

        # 提取厄米部分
        log_v_herm = (log_v - log_v.T.conj()) / (2j)

        # 投影到 Gell-Mann 矩阵
        lambda_matrices = U3Frame._gell_mann_matrices()
        params = np.array([
            np.trace(log_v_herm @ lam).real / 2
            for lam in lambda_matrices
        ])

        return params

    def color_charge(self) -> Tuple[float, float]:
        """
        颜色荷（对应 SU(3) 的两个Casimir算符）

        Returns:
            (C₁, C₂) - 一次和二次Casimir不变量
        """
        # 一次 Casimir：C₁ = Tr(T)（对 SU(3) 总为 0）
        C1 = np.trace(self.matrix).real

        # 二次 Casimir：C₂ = Tr(T²)
        C2 = np.trace(self.matrix @ self.matrix).real

        return (C1, C2)


# ============================================================
# 规范场类
# ============================================================

class GaugeConnection:
    """
    规范场联络 A_μ ∈ 𝔲(3)

    数学形式：
        A_μ = A_μ^{SU(3)} + A_μ^{SU(2)} + A_μ^{U(1)}

    协变导数：
        D_μ U = ∂_μ U + A_μ U

    场强张量（曲率）：
        F_μν = ∂_μ A_ν - ∂_ν A_μ + [A_μ, A_ν]

    物理诠释：
        - A_μ^{SU(3)}: 胶子场（8个分量）
        - A_μ^{SU(2)}: W/Z玻色子场（3个分量）
        - A_μ^{U(1)}: 光子场（1个分量）
    """

    def __init__(self,
                 su3_component: Optional[np.ndarray] = None,
                 su2_component: Optional[np.ndarray] = None,
                 u1_component: Optional[complex] = None):
        """
        初始化规范联络

        Args:
            su3_component: 8×1 实数组（Gell-Mann 分量）
            su2_component: 3×1 实数组（Pauli 分量）
            u1_component: 复数（U(1) 分量）
        """
        self.su3 = su3_component if su3_component is not None else np.zeros(8)
        self.su2 = su2_component if su2_component is not None else np.zeros(3)
        self.u1 = u1_component if u1_component is not None else 0.0+0j

    def connection_matrix(self) -> np.ndarray:
        """
        联络的矩阵表示 A_μ ∈ 𝔲(3)

        Returns:
            3×3 反厄米矩阵
        """
        # SU(3) 部分
        lambda_matrices = U3Frame._gell_mann_matrices()
        A_su3 = sum(self.su3[i] * lambda_matrices[i] for i in range(8))

        # SU(2) 部分（嵌入到左上 2×2 块）
        pauli_matrices = self._pauli_matrices()
        A_su2_block = sum(self.su2[i] * pauli_matrices[i] for i in range(3))
        A_su2 = np.zeros((3, 3), dtype=complex)
        A_su2[:2, :2] = A_su2_block

        # U(1) 部分
        A_u1 = self.u1 * np.eye(3)

        return 1j * (A_su3 + A_su2 + A_u1)

    def field_strength(self, other: 'GaugeConnection') -> 'FieldStrength':
        """
        计算场强张量 F_μν = [D_μ, D_ν]

        Args:
            other: 另一个方向的联络 A_ν

        Returns:
            FieldStrength 对象
        """
        A_mu = self.connection_matrix()
        A_nu = other.connection_matrix()

        # F_μν = [A_μ, A_ν] (简化版本，忽略导数项)
        F_matrix = A_mu @ A_nu - A_nu @ A_mu

        return FieldStrength(F_matrix)

    @staticmethod
    def _pauli_matrices() -> List[np.ndarray]:
        """Pauli 矩阵（SU(2) 生成元）"""
        σ = [
            np.array([[0, 1], [1, 0]], dtype=complex),  # σ₁
            np.array([[0, -1j], [1j, 0]], dtype=complex),  # σ₂
            np.array([[1, 0], [0, -1]], dtype=complex),  # σ₃
        ]
        return σ

    def __repr__(self):
        return f"GaugeConnection(SU(3): {np.linalg.norm(self.su3):.3f}, SU(2): {np.linalg.norm(self.su2):.3f}, U(1): {abs(self.u1):.3f})"


@dataclass
class FieldStrength:
    """
    场强张量 F_μν（规范场的曲率）

    物理意义：
        - 电磁场：F_μν 对应电场和磁场
        - 非阿贝尔规范场：胶子/W玻色子的场强
    """
    matrix: np.ndarray  # 3×3 反厄米矩阵

    def yang_mills_action(self) -> float:
        """
        杨-米尔斯作用量：S = -1/(4g²) Tr(F_μν F^μν)

        Returns:
            作用量（实数）
        """
        return -0.25 * np.trace(self.matrix @ self.matrix.T.conj()).real

    def topological_charge(self) -> float:
        """
        拓扑荷：Q = (1/32π²) ∫ Tr(F ∧ F)

        Returns:
            拓扑荷（instanton 数）
        """
        # 简化版本：使用矩阵迹
        return (1.0 / (32 * np.pi**2)) * np.trace(self.matrix @ self.matrix).real


# ============================================================
# 对称性破缺势能
# ============================================================

class SymmetryBreakingPotential:
    """
    对称性破缺势能函数

    数学形式：
        V(U) = -μ² Tr(U†U) + λ [Tr(U†U)]² + γ Tr([U†,U]²)

    极小值点决定对称破缺模式：
        - SU(4) → SU(3) × U(1)
        - SU(3) → SU(2) × U(1)

    物理类比：
        - 类似 Higgs 势能
        - 真空期望值破坏对称性
    """

    def __init__(self, mu_squared: float = -1.0, lambda_coupling: float = 0.5, gamma_coupling: float = 0.1):
        """
        初始化势能参数

        Args:
            mu_squared: 质量平方项（负值触发对称破缺）
            lambda_coupling: 四次耦合常数
            gamma_coupling: 非阿贝尔耦合常数
        """
        self.mu2 = mu_squared
        self.lambda_ = lambda_coupling
        self.gamma = gamma_coupling

    def potential(self, frame: U3Frame) -> float:
        """
        计算势能 V(U)

        Args:
            frame: U(3) 标架

        Returns:
            势能值
        """
        U = frame.matrix
        U_dag = U.T.conj()

        # 第一项：-μ² Tr(U†U)
        term1 = -self.mu2 * np.trace(U_dag @ U).real

        # 第二项：λ [Tr(U†U)]²
        tr_UdagU = np.trace(U_dag @ U)
        term2 = self.lambda_ * (tr_UdagU * tr_UdagU.conj()).real

        # 第三项：γ Tr([U†,U]²)
        commutator = U_dag @ U - U @ U_dag
        term3 = self.gamma * np.trace(commutator @ commutator).real

        return term1 + term2 + term3

    def gradient(self, frame: U3Frame) -> np.ndarray:
        """
        计算势能梯度 ∇V(U)

        用于最小化势能，找到对称破缺真空

        Returns:
            3×3 复矩阵梯度
        """
        U = frame.matrix
        U_dag = U.T.conj()

        # 数值梯度（简化实现）
        epsilon = 1e-6
        grad = np.zeros((3, 3), dtype=complex)

        V0 = self.potential(frame)

        for i in range(3):
            for j in range(3):
                # 实部方向
                U_perturb = U.copy()
                U_perturb[i, j] += epsilon
                frame_perturb = U3Frame(U_perturb[:, 0], U_perturb[:, 1], U_perturb[:, 2], ensure_unitary=False)
                grad[i, j] = (self.potential(frame_perturb) - V0) / epsilon

                # 虚部方向
                U_perturb = U.copy()
                U_perturb[i, j] += 1j * epsilon
                frame_perturb = U3Frame(U_perturb[:, 0], U_perturb[:, 1], U_perturb[:, 2], ensure_unitary=False)
                grad[i, j] += 1j * (self.potential(frame_perturb) - V0) / epsilon

        return grad

    def find_vacuum(self, initial_frame: Optional[U3Frame] = None,
                   max_iterations: int = 100, tolerance: float = 1e-6) -> U3Frame:
        """
        寻找真空态（势能极小值）

        使用梯度下降方法

        Args:
            initial_frame: 初始猜测
            max_iterations: 最大迭代次数
            tolerance: 收敛容差

        Returns:
            真空态标架
        """
        if initial_frame is None:
            initial_frame = U3Frame()  # 从单位标架开始

        current_frame = initial_frame
        learning_rate = 0.01

        for iteration in range(max_iterations):
            grad = self.gradient(current_frame)
            grad_norm = np.linalg.norm(grad)

            if grad_norm < tolerance:
                print(f"收敛于迭代 {iteration}, |∇V| = {grad_norm:.2e}")
                break

            # 梯度下降步骤
            U_new = current_frame.matrix - learning_rate * grad
            current_frame = U3Frame(U_new[:, 0], U_new[:, 1], U_new[:, 2], ensure_unitary=True)

        return current_frame


# ============================================================
# 辅助函数
# ============================================================

def scipy_expm(matrix: np.ndarray) -> np.ndarray:
    """矩阵指数函数（依赖 scipy）"""
    try:
        from scipy.linalg import expm
        return expm(matrix)
    except ImportError:
        # 简化实现：泰勒展开
        return _matrix_exp_taylor(matrix, order=10)

def scipy_logm(matrix: np.ndarray) -> np.ndarray:
    """矩阵对数函数（依赖 scipy）"""
    try:
        from scipy.linalg import logm
        return logm(matrix)
    except ImportError:
        raise NotImplementedError("需要 scipy.linalg.logm")

def _matrix_exp_taylor(A: np.ndarray, order: int = 10) -> np.ndarray:
    """泰勒展开计算矩阵指数"""
    result = np.eye(A.shape[0], dtype=A.dtype)
    term = np.eye(A.shape[0], dtype=A.dtype)

    for k in range(1, order + 1):
        term = term @ A / k
        result += term

    return result


# ============================================================
# 导出
# ============================================================

__all__ = [
    'U3Frame',
    'SU3Component',
    'GaugeConnection',
    'FieldStrength',
    'SymmetryBreakingPotential',
    'HBAR',
    'C_SPEED',
]


# ============================================================
# 演示
# ============================================================

def demonstrate():
    """演示 U(3) 复标架与规范场"""
    print("=" * 70)
    print("U(3) 复标架与规范场统一框架演示")
    print("=" * 70)

    # 1. 创建 U(3) 标架
    print("\n1. 创建 U(3) 复标架")
    frame = U3Frame()
    print(f"   {frame}")
    print(f"   det(U) = {frame.determinant:.6f}")
    print(f"   全局相位 φ = {frame.global_phase:.4f} rad")

    # 2. 颜色相位
    print("\n2. 颜色相位（RGB）")
    phases = frame.color_phases()
    print(f"   θ_R (红) = {phases[0]:.4f} rad")
    print(f"   θ_G (绿) = {phases[1]:.4f} rad")
    print(f"   θ_B (蓝) = {phases[2]:.4f} rad")
    print(f"   约束检查: θ_R + θ_G + θ_B = {sum(phases):.4f} (应等于 φ)")

    # 3. 对称性分解
    print("\n3. U(3) → SU(3) × U(1) 分解")
    su3_comp, u1_phase = frame.to_su3_u1()
    print(f"   SU(3) 分量 det = {np.linalg.det(su3_comp.matrix):.6f} (应为 1)")
    print(f"   U(1) 相位 = {u1_phase:.6f}")

    # 4. 四元数表示
    print("\n4. 四元数表示（SU(2) 子群）")
    q = frame.to_quaternion_representation()
    print(f"   q = ({q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f}, {q[3]:.4f})")
    print(f"   |q| = {np.sqrt(sum(abs(x)**2 for x in q)):.6f}")

    # 5. 规范变换
    print("\n5. 规范变换")
    # U(1) 变换
    frame_u1 = frame.gauge_transform_u1(np.pi/4)
    print(f"   U(1) 变换后: {frame_u1}")

    # SU(2) 变换
    frame_su2 = frame.gauge_transform_su2((0.1, 0.2, 0.3))
    print(f"   SU(2) 变换后: {frame_su2}")

    # 6. 规范场联络
    print("\n6. 规范场联络")
    connection = GaugeConnection(
        su3_component=np.random.randn(8) * 0.1,
        su2_component=np.random.randn(3) * 0.1,
        u1_component=0.05+0.02j
    )
    print(f"   {connection}")
    A_matrix = connection.connection_matrix()
    print(f"   ||A_μ|| = {np.linalg.norm(A_matrix):.4f}")

    # 7. 场强张量
    print("\n7. 场强张量（曲率）")
    connection2 = GaugeConnection(
        su3_component=np.random.randn(8) * 0.1,
        su2_component=np.random.randn(3) * 0.1,
        u1_component=0.03+0.01j
    )
    F = connection.field_strength(connection2)
    print(f"   ||F_μν|| = {np.linalg.norm(F.matrix):.4f}")
    print(f"   杨-米尔斯作用量 S = {F.yang_mills_action():.6f}")
    print(f"   拓扑荷 Q = {F.topological_charge():.6f}")

    # 8. 对称性破缺
    print("\n8. 对称性破缺势能")
    potential = SymmetryBreakingPotential(mu_squared=-1.0, lambda_coupling=0.5)
    V = potential.potential(frame)
    print(f"   V(U) = {V:.6f}")
    print(f"   寻找真空态...")
    vacuum = potential.find_vacuum(max_iterations=50)
    V_vacuum = potential.potential(vacuum)
    print(f"   V(U_vacuum) = {V_vacuum:.6f}")
    print(f"   真空态: {vacuum}")

    print("\n" + "=" * 70)
    print("核心理论总结：")
    print("  • U(3) = [e₁, e₂, e₃] ∈ U(3)  [完整酉标架]")
    print("  • U(3) = SU(3) × U(1)  [对称性分解]")
    print("  • (θ_R, θ_G, θ_B)  [颜色相位]")
    print("  • A_μ = A_μ^{SU(3)} + A_μ^{SU(2)} + A_μ^{U(1)}  [规范联络]")
    print("  • F_μν = [D_μ, D_ν]  [场强张量]")
    print("  • V(U) 极小化 → 对称性破缺模式")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate()
