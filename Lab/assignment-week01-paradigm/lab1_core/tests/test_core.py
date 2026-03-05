import sys
import os
import pytest
import numpy as np

# 将 src 目录加入路径，以便导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from differentiation import central_difference

def test_central_difference_accuracy():
    """
    测试中心差分函数的精度。
    对于 sin(x) 在 x=pi/4，使用 h=1e-5，误差应小于 1e-9。
    """
    x = np.pi / 4
    h = 1e-5
    exact = np.cos(x)
    approx = central_difference(np.sin, x, h)
    
    error = abs(approx - exact)
    
    # 中心差分误差 O(h^2) -> (1e-5)^2 = 1e-10 量级
    # 考虑到浮点误差，放宽到 1e-9
    assert error < 1e-9, f"误差过大: {error}. 检查是否使用了正确的中心差分公式 (f(x+h)-f(x-h))/2h"

def test_central_difference_convergence():
    """
    测试收敛性：h 减小 10 倍，误差应减小约 100 倍 (O(h^2))。
    (在截断误差主导区 h ~ 1e-3 -> 1e-4)
    """
    x = np.pi / 4
    h1 = 1e-3
    h2 = 1e-4
    
    exact = np.cos(x)
    err1 = abs(central_difference(np.sin, x, h1) - exact)
    err2 = abs(central_difference(np.sin, x, h2) - exact)
    
    ratio = err1 / err2
    
    # 理论比值应该是 100，允许一定波动 (80-120)
    assert 80 < ratio < 120, f"收敛阶数不对. h减小10倍，误差减小了 {ratio:.1f} 倍. 期望 ~100倍 (2阶精度)."

def test_roundoff_error_dominance():
    """
    测试舍入误差：当 h 极小时 (1e-16)，误差应该反弹变大。
    """
    x = np.pi / 4
    h_optimal = 1e-5
    h_tiny = 1e-15
    
    exact = np.cos(x)
    err_optimal = abs(central_difference(np.sin, x, h_optimal) - exact)
    err_tiny = abs(central_difference(np.sin, x, h_tiny) - exact)
    
    assert err_tiny > err_optimal, "在极小步长 h=1e-15 处，误差应该比 h=1e-5 大 (舍入误差主导)."
