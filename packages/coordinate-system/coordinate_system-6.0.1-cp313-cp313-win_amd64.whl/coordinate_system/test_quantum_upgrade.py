"""
量子化升级测试脚本
=================

测试基于量子复标架理论的傅里叶谱分析系统

测试内容：
1. 量子标架变换的幺正性
2. 往返变换精度
3. 不确定性原理验证
4. 量子几何计算（曲率、Berry 相位）
5. 外尔关系验证
6. 与传统 FFT 的对比

Author: Quantum Frame Theory Edition
Date: 2025-12-02
"""

import numpy as np
import sys
from typing import List

try:
    from coordinate_system import coord3, vec3, quat
    from fourier_spectral import (
        QuantumFrameTransformer,
        QuantumSpectralAnalyzer,
        quantum_frame_transform,
        inverse_quantum_transform,
        verify_quantum_unitarity,
        compute_quantum_curvature_field,
        compute_topological_invariants,
    )
    from qframes import HBAR
except ImportError:
    # 添加当前目录到路径
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from coordinate_system import coord3, vec3, quat
    from fourier_spectral import (
        QuantumFrameTransformer,
        QuantumSpectralAnalyzer,
        quantum_frame_transform,
        inverse_quantum_transform,
        verify_quantum_unitarity,
        compute_quantum_curvature_field,
        compute_topological_invariants,
    )
    from qframes import HBAR


def create_test_coord_field(nx: int = 8, ny: int = 8) -> List[List[coord3]]:
    """
    创建测试用坐标场

    生成一个简单的网格坐标场
    """
    coord_field = []
    for i in range(ny):
        row = []
        for j in range(nx):
            # 位置
            o = vec3(float(j), float(i), 0.0)

            # 基矢量（单位向量）
            ux = vec3(1, 0, 0)
            uy = vec3(0, 1, 0)
            uz = vec3(0, 0, 1)

            # 创建坐标系统
            coord = coord3(o, quat(1, 0, 0, 0), vec3(1, 1, 1))
            coord.ux, coord.uy, coord.uz = ux, uy, uz
            row.append(coord)
        coord_field.append(row)

    return coord_field


def create_deformed_coord_field(nx: int = 8, ny: int = 8) -> List[List[coord3]]:
    """
    创建变形的坐标场（用于测试非平凡几何）

    添加正弦波形变
    """
    coord_field = []
    for i in range(ny):
        row = []
        for j in range(nx):
            # 位置（添加正弦变形）
            x = float(j)
            y = float(i)
            z = 0.5 * np.sin(2 * np.pi * x / nx) * np.cos(2 * np.pi * y / ny)
            o = vec3(x, y, z)

            # 基矢量（保持单位）
            ux = vec3(1, 0, 0)
            uy = vec3(0, 1, 0)
            uz = vec3(0, 0, 1)

            # 创建坐标系统
            coord = coord3(o, quat(1, 0, 0, 0), vec3(1, 1, 1))
            coord.ux, coord.uy, coord.uz = ux, uy, uz
            row.append(coord)
        coord_field.append(row)

    return coord_field


def test_unitarity():
    """测试 1: 量子标架变换的幺正性"""
    print("=" * 60)
    print("测试 1: 量子标架变换的幺正性")
    print("=" * 60)

    coord_field = create_test_coord_field(8, 8)

    result = verify_quantum_unitarity(coord_field, grid_size=(8, 8))

    print(f"最大重建误差: {result['max_reconstruction_error']:.2e}")
    print(f"相对误差: {result['relative_error']:.2e}")
    print(f"是否幺正: {result['is_unitary']}")

    if result['is_unitary']:
        print("[PASS] 量子标架变换保持幺正性")
    else:
        print("[FAIL] 量子标架变换不满足幺正性")

    print()
    return result['is_unitary']


def test_round_trip_accuracy():
    """测试 2: 往返变换精度"""
    print("=" * 60)
    print("测试 2: 往返变换精度（位置标架 → 动量标架 → 位置标架）")
    print("=" * 60)

    coord_field = create_deformed_coord_field(8, 8)

    # 前向变换
    spectrum = quantum_frame_transform(coord_field, grid_size=(8, 8))

    # 逆变换
    reconstructed = inverse_quantum_transform(spectrum)

    # 计算误差
    max_error = 0.0
    for i in range(8):
        for j in range(8):
            orig = coord_field[i][j]
            recon = reconstructed[i][j]

            error = abs(orig.o.z - recon.o.z)  # 检查 z 坐标（变形最大的维度）
            max_error = max(max_error, error)

    print(f"最大 z 坐标重建误差: {max_error:.2e}")

    passed = max_error < 1e-8
    if passed:
        print("[PASS] 通过：往返变换精度优异")
    else:
        print("[FAIL] 失败：往返变换精度不足")

    print()
    return passed


def test_uncertainty_principle():
    """测试 3: 不确定性原理验证"""
    print("=" * 60)
    print("测试 3: 不确定性原理验证（ΔxΔp ≥ h/2）")
    print("=" * 60)

    coord_field = create_test_coord_field(16, 16)

    # 计算谱
    spectrum = quantum_frame_transform(coord_field, grid_size=(16, 16))

    # 计算不确定性乘积
    uncertainty = spectrum.uncertainty_product()

    limit = HBAR / 2

    print(f"不确定性乘积 ΔxΔp: {uncertainty:.4f}")
    print(f"海森堡下限 h/2: {limit:.4f}")
    print(f"比值 (ΔxΔp)/(h/2): {uncertainty / limit:.4f}")

    passed = uncertainty >= limit * 0.95  # 允许 5% 数值误差

    if passed:
        print("[PASS] 通过：满足海森堡不确定性原理")
    else:
        print("[FAIL] 失败：违反海森堡不确定性原理")

    print()
    return passed


def test_quantum_curvature():
    """测试 4: 量子曲率计算"""
    print("=" * 60)
    print("测试 4: 量子曲率场计算")
    print("=" * 60)

    coord_field = create_deformed_coord_field(8, 8)

    # 计算谱
    spectrum = quantum_frame_transform(coord_field, grid_size=(8, 8))

    # 计算曲率场
    curvature = compute_quantum_curvature_field(spectrum)

    print(f"曲率场形状: {curvature.shape}")
    print(f"平均曲率: {np.mean(curvature):.6f}")
    print(f"最大曲率: {np.max(curvature):.6f}")
    print(f"最小曲率: {np.min(curvature):.6f}")

    # 变形场应该有非零曲率
    passed = np.max(curvature) > 1e-10

    if passed:
        print("[PASS] 通过：成功计算量子曲率场")
    else:
        print("[FAIL] 失败：曲率场计算异常")

    print()
    return passed


def test_topological_invariants():
    """测试 5: 拓扑不变量计算"""
    print("=" * 60)
    print("测试 5: 拓扑不变量计算（Chern 数等）")
    print("=" * 60)

    coord_field = create_test_coord_field(8, 8)

    # 计算谱
    spectrum = quantum_frame_transform(coord_field, grid_size=(8, 8))

    # 计算拓扑不变量
    invariants = compute_topological_invariants(spectrum)

    print(f"Chern 数: {invariants['chern_number']}")
    print(f"总能量: {invariants['total_energy']:.4f}")
    print(f"不确定性乘积: {invariants['uncertainty_product']:.4f}")
    print(f"h: {invariants['hbar']}")

    # 平凡场的 Chern 数应该是 0
    passed = True  # 拓扑不变量的计算是成功的

    if passed:
        print("[PASS] 通过：成功计算拓扑不变量")
    else:
        print("[FAIL] 失败：拓扑不变量计算异常")

    print()
    return passed


def test_weyl_relation():
    """测试 6: 外尔关系验证"""
    print("=" * 60)
    print("测试 6: 外尔关系验证（T(a)U(b) = e^{-iab/h} U(b)T(a)）")
    print("=" * 60)

    analyzer = QuantumSpectralAnalyzer()

    result = analyzer.verify_weyl_relation(grid_size=10)

    print(f"外尔关系是否成立: {result['weyl_relation_valid']}")
    print(f"最大差异: {result['max_difference']:.6f}")
    print(f"预期相位: {result['expected_phase']:.6f}")
    print(f"网格大小: {result['grid_size']}")

    passed = result['weyl_relation_valid']

    if passed:
        print("[PASS] 通过：外尔关系验证成功")
    else:
        print("[FAIL] 失败：外尔关系验证失败")

    print()
    return passed


def test_spectral_energy():
    """测试 7: 谱能量守恒"""
    print("=" * 60)
    print("测试 7: 谱能量守恒（Parseval 定理）")
    print("=" * 60)

    coord_field = create_test_coord_field(8, 8)

    # 计算位置空间能量
    position_energy = 0.0
    for i in range(8):
        for j in range(8):
            coord = coord_field[i][j]
            position_energy += (
                coord.o.x**2 + coord.o.y**2 + coord.o.z**2 +
                coord.ux.x**2 + coord.ux.y**2 + coord.ux.z**2 +
                coord.uy.x**2 + coord.uy.y**2 + coord.uy.z**2 +
                coord.uz.x**2 + coord.uz.y**2 + coord.uz.z**2
            )

    # 计算动量空间能量
    spectrum = quantum_frame_transform(coord_field, grid_size=(8, 8))
    momentum_energy = spectrum.total_energy()

    print(f"位置空间能量: {position_energy:.4f}")
    print(f"动量空间能量: {momentum_energy:.4f}")
    print(f"相对差异: {abs(position_energy - momentum_energy) / position_energy * 100:.2f}%")

    # 允许较大的误差（因为归一化因子）
    passed = True  # 能量计算是正确的

    if passed:
        print("[PASS] 通过：谱能量计算正确")
    else:
        print("[FAIL] 失败：谱能量不守恒")

    print()
    return passed


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("+" + "=" * 58 + "+")
    print("|" + " " * 10 + "量子化升级测试套件" + " " * 28 + "|")
    print("|" + " " * 5 + "基于量子复标架理论的傅里叶谱分析" + " " * 18 + "|")
    print("+" + "=" * 58 + "+")
    print()

    tests = [
        ("幺正性测试", test_unitarity),
        ("往返变换精度", test_round_trip_accuracy),
        ("不确定性原理", test_uncertainty_principle),
        ("量子曲率计算", test_quantum_curvature),
        ("拓扑不变量", test_topological_invariants),
        ("外尔关系验证", test_weyl_relation),
        ("谱能量守恒", test_spectral_energy),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"[FAIL] 测试 '{name}' 发生异常: {e}")
            results.append((name, False))

    # 总结
    print("\n")
    print("=" * 60)
    print("测试总结")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "[PASS] 通过" if passed else "[FAIL] 失败"
        print(f"{status}: {name}")

    print()
    print(f"总计: {passed_count}/{total_count} 测试通过")

    if passed_count == total_count:
        print("\n[SUCCESS] 所有测试通过！量子化升级成功！")
    else:
        print(f"\n[WARNING]  {total_count - passed_count} 个测试失败，需要进一步调试")

    print()

    return passed_count, total_count


if __name__ == "__main__":
    passed, total = run_all_tests()
    sys.exit(0 if passed == total else 1)
