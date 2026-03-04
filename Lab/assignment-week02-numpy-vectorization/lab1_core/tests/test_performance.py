import numpy as np
import pytest
import time
import sys
import os

# 确保能导入 src 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gravity_slow import compute_potential_slow
from src.gravity_fast import compute_potential_vectorized

def test_speed_and_accuracy():
    """
    Core Test: 
    1. 验证向量化代码的物理结果是否正确 (与循环版一致)
    2. 验证向量化代码的速度是否足够快 (>50x)
    """
    # 1. 构造测试数据
    N = 20 # 质量点数
    grid_size = 50 # 网格大小 (如果设为 200，慢速版会跑很久，测试时缩小规模)
    x = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, x)
    
    np.random.seed(42)
    mass_pos = np.random.rand(N, 2) * 4 - 2
    mass_val = np.ones(N)
    
    print(f"\n--- Running Test on {grid_size}x{grid_size} Grid ---")
    
    # 2. 运行慢速版本 (基准)
    t0 = time.time()
    V_slow = compute_potential_slow(X, Y, mass_pos, mass_val)
    t_slow = time.time() - t0
    
    # 3. 运行学生版本
    t1 = time.time()
    try:
        V_fast = compute_potential_vectorized(X, Y, mass_pos, mass_val)
    except NotImplementedError:
        pytest.fail("❌ 你还没有实现 compute_potential_vectorized 函数！")
    t_fast = time.time() - t1
    
    # 4. 判定精度 (允许 1e-5 的浮点误差)
    # 慢速代码里有个粗糙的截断 if r > 1e-6，这会导致微小差异，所以放宽误差
    # 如果学生正确使用了 epsilon=1e-6 软化因子，差异应该很小
    diff = np.abs(V_slow - V_fast)
    max_diff = np.max(diff)
    
    print(f"Max Difference: {max_diff:.2e}")
    if max_diff > 1e-1: # 允许一定误差，因为慢速版的 if 截断和软化因子不同
         pytest.fail(f"❌ 物理结果偏差过大 (Max Diff: {max_diff:.2e})！请检查你的物理公式。")

    # 5. 判定速度 (必须快 50 倍)
    # 注意：防止除零
    speedup = t_slow / (t_fast + 1e-9)
    print(f"Slow Time: {t_slow:.4f}s")
    print(f"Fast Time: {t_fast:.4f}s")
    print(f"🚀 Speedup: {speedup:.1f}x")
    
    if speedup < 50:
        pytest.fail(f"❌ 速度不够快！目标 50x，实际 {speedup:.1f}x。你是否还在代码里使用了 for 循环？")
    
    print("✅ 恭喜！你的代码既准确又快如闪电。")
