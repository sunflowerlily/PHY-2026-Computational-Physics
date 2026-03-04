import numpy as np
import pytest
from lab1_core.src.differentiation import central_diff

def test_central_diff_accuracy():
    """测试中心差分的精度"""
    x = 1.0
    h = 1e-5 # Sweet spot for central difference
    true_val = np.cos(x)
    
    calc_val = central_diff(np.sin, x, h)
    
    if calc_val is None:
        pytest.fail("Function central_diff returns None. Did you implement it?")
        
    error = abs(calc_val - true_val)
    
    # 中心差分的误差应该是 O(h^2)，即 10^-10 级别
    assert error < 1e-9, f"Error {error} is too large! Expected < 1e-9"

def test_vectorization():
    """测试是否支持向量化输入 (防循环)"""
    h_arr = np.array([1e-4, 1e-5])
    try:
        res = central_diff(np.sin, 1.0, h_arr)
        assert res.shape == h_arr.shape, "Output shape mismatch. Did you use vectorization?"
    except TypeError:
        pytest.fail("Function does not support numpy array input for h.")
