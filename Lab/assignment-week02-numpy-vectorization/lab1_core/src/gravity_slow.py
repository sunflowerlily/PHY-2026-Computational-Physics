import numpy as np
import time

def compute_potential_slow(X, Y, mass_pos, mass_val, G=1.0):
    """
    计算引力势能场 V(x,y) = sum_k { -G * m_k / |r - r_k| }
    
    【警告】
    这段代码是由不懂 Numpy 的 AI 生成的，它使用了极其低效的 Python 循环。
    在网格较大时，这段代码可能会卡死你的电脑。
    
    参数:
    X, Y: 网格坐标 (H, W)
    mass_pos: 质量点位置 (N, 2)
    mass_val: 质量点质量 (N,)
    G: 引力常数
    """
    H, W = X.shape
    N = len(mass_val)
    V = np.zeros_like(X)
    
    print(f"Starting SLOW computation on {H}x{W} grid with {N} bodies...")
    start_t = time.time()
    
    # ❌ 剧毒的三重循环 (Python Loop Hell)
    # 时间复杂度: O(H * W * N)
    for i in range(H):
        if i % 10 == 0: print(f"Processing row {i}/{H}...", end='\r')
        for j in range(W):
            for k in range(N):
                # 物理错误隐患：没有加软化因子 (softening)，r=0 时会发散
                dx = X[i, j] - mass_pos[k, 0]
                dy = Y[i, j] - mass_pos[k, 1]
                r = np.sqrt(dx**2 + dy**2) 
                
                # 笨拙的防除零检查 (在 Python 循环中做 if 判断极其昂贵)
                if r > 1e-6:
                    V[i, j] += -G * mass_val[k] / r
                else:
                    V[i, j] += -G * mass_val[k] / 1e-6 # 粗糙的截断
                    
    end_t = time.time()
    print(f"\nSlow Loop Time: {end_t - start_t:.4f} s")
    return V
