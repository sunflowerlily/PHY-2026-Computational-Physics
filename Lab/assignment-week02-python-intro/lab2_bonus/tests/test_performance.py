import numpy as np
import pytest
import time
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.nbody_vectorized import simulate_nbody

def simulate_nbody_slow_loop(N, steps, dt):
    """
    基准测试：使用 math 和 for 循环的低效实现
    """
    # 模拟初始化
    pos_x = [np.random.rand() for _ in range(N)]
    pos_y = [np.random.rand() for _ in range(N)]
    vel_x = [np.random.rand() for _ in range(N)]
    vel_y = [np.random.rand() for _ in range(N)]
    
    start_t = time.time()
    for _ in range(steps):
        for i in range(N):
            pos_x[i] += vel_x[i] * dt
            pos_y[i] += vel_y[i] * dt
    return time.time() - start_t

def test_speedup():
    """
    性能测试：比较矢量化代码与循环代码的速度
    """
    N = 1000  # 粒子数
    steps = 100 # 步数
    dt = 0.01
    
    print(f"\n--- Performance Test (N={N}, steps={steps}) ---")
    
    # 1. 运行慢速基准
    t_slow = simulate_nbody_slow_loop(N, steps, dt)
    print(f"Slow Loop Time: {t_slow:.4f} s")
    
    # 2. 运行学生代码
    start_t = time.time()
    pos_fast = simulate_nbody(N, steps, dt)
    t_fast = time.time() - start_t
    
    # 检查是否真的实现了代码 (不能只返回零矩阵)
    assert not np.all(pos_fast == 0), "❌ 你的代码返回了全零矩阵，是不是还没写完？"
    
    print(f"Vectorized Time: {t_fast:.4f} s")
    
    # 3. 计算加速比
    # 注意：由于包括了初始化时间，纯计算部分的加速比可能更高
    # 这里我们放宽标准，只要比纯循环快 50 倍即可
    # (实际上 numpy 应该快 100-200 倍)
    speedup = t_slow / (t_fast + 1e-9)
    print(f"🚀 Speedup: {speedup:.1f}x")
    
    if speedup < 50:
        pytest.fail(f"❌ 速度不够快！目标 50x，实际 {speedup:.1f}x。你是否还在代码里使用了 for 循环？")
    
    print("✅ 恭喜！你的代码快如闪电。")
