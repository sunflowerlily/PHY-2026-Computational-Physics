import numpy as np
import time

def simulate_nbody(N, steps, dt):
    """
    TODO: 实现 N-Body 模拟的矢量化版本
    
    参数:
    N: 粒子数量
    steps: 模拟步数
    dt: 时间步长
    """
    print(f"Initializing {N} particles...")
    
    # 1. 初始化 (使用 numpy 生成随机数组)
    # pos: (N, 2)
    # vel: (N, 2)
    # [YOUR CODE HERE]
    # pos = np.random...
    
    print("Starting simulation loop...")
    start_t = time.time()
    
    for _ in range(steps):
        # 2. 矢量化更新 (不允许使用 for 循环遍历粒子！)
        # 一行代码更新所有粒子的位置
        # [YOUR CODE HERE]
        # pos += ...
        pass
        
    end_t = time.time()
    print(f"Simulation finished in {end_t - start_t:.4f} s")
    
    # 返回最终的位置数组供测试使用
    # return pos
    return np.zeros((N, 2)) # 占位符
