import numpy as np
import matplotlib.pyplot as plt

def central_difference(f, x, h):
    """
    计算函数 f 在 x 处的中心差分导数。
    
    参数:
    f: 目标函数 (e.g., np.sin)
    x: 求导点 (float)
    h: 步长 (float)
    
    返回:
    近似导数值 (float)
    """
    # TODO: 实现中心差分公式 (f(x+h) - f(x-h)) / (2h)
    # 提示: 不要忘记 return
    pass

def analyze_error():
    """
    分析数值微分误差随步长 h 的变化。
    """
    x_target = np.pi / 4
    exact_derivative = np.cos(x_target)
    
    # 生成对数均匀分布的步长 h，从 10^-16 到 10^0
    h_values = np.logspace(-16, 0, 100)
    
    errors = []
    for h in h_values:
        # TODO: 
        # 1. 调用 central_difference 计算近似值
        # 2. 计算相对误差: |approx - exact| / |exact|
        # 3. 将误差存入 errors 列表
        pass
        
    errors = np.array(errors)
    
    # TODO: 找到最小误差对应的步长 (最优步长)
    # min_error_idx = ...
    # optimal_h = ...
    # min_error = ...
    
    # print(f"理论最优步长 (双精度): ~1e-5")
    # print(f"实测最优步长: {optimal_h:.2e}")
    # print(f"最小相对误差: {min_error:.2e}")
    
    # 绘图
    plt.figure(figsize=(10, 6))
    # TODO: 绘制双对数坐标图 (log-log plot)
    # plt.loglog(..., ..., 'b.-', label='Total Error')
    
    # TODO (可选): 添加理论截断误差 (Slope 2) 和舍入误差 (Slope -1) 的辅助线
    
    plt.xlabel('Step Size $h$')
    plt.ylabel('Relative Error')
    plt.title('Numerical Differentiation Error Analysis: Truncation vs. Round-off')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig('error_analysis.png')
    plt.show()

if __name__ == "__main__":
    analyze_error()
