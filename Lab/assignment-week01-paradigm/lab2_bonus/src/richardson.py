import numpy as np

def richardson_extrapolation(f, x, h):
    """
    使用 Richardson 外推法计算高精度导数。
    公式: D(h) = (4 * D_central(h/2) - D_central(h)) / 3
    误差: O(h^4)
    
    参数:
    f: 目标函数
    x: 求导点
    h: 初始步长
    """
    # 1. 计算步长为 h 的中心差分 D(h)
    D_h = (f(x + h) - f(x - h)) / (2 * h)
    
    # 2. 计算步长为 h/2 的中心差分 D(h/2)
    h_half = h / 2
    D_h_half = (f(x + h_half) - f(x - h_half)) / (2 * h_half)
    
    # 3. 组合消除 O(h^2) 项，得到 O(h^4) 精度
    return (4 * D_h_half - D_h) / 3

def compare_methods():
    x = np.pi / 4
    exact = np.cos(x)
    
    # 我们选择一个较大的步长 h=0.1，来展示高阶方法的威力
    h = 0.1
    
    # 普通中心差分 (O(h^2))
    D_central = (np.sin(x + h) - np.sin(x - h)) / (2 * h)
    err_central = abs(D_central - exact)
    
    # Richardson 外推 (O(h^4))
    D_richardson = richardson_extrapolation(np.sin, x, h)
    err_richardson = abs(D_richardson - exact)
    
    print(f"Step size h = {h}")
    print(f"Central Difference Error (O(h^2)): {err_central:.2e}")
    print(f"Richardson Error (O(h^4)):         {err_richardson:.2e}")
    print(f"Improvement Factor: {err_central / err_richardson:.1f}x")
    
    if err_richardson < 1e-10:
        print("\n>>> Success! Richardson method is extremely accurate even with large step size.")
    else:
        print("\n>>> Keep tuning! Something is not right.")

if __name__ == "__main__":
    compare_methods()
