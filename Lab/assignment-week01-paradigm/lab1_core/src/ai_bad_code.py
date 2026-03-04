import numpy as np

def bad_derivative_demo():
    """
    一个典型的 AI 生成的'坏'代码演示。
    它试图通过不断减小步长来获得更高精度，
    却掉进了 IEEE 754 浮点数的陷阱。
    """
    x = 1.0
    # AI 的天真逻辑：步长越小越好？
    # 陷阱：直接生成了 h=0 的情况，或者使用了 float32 导致精度过早崩溃
    h_values = [1e-1, 1e-5, 1e-15, 1e-16, 1e-17] 
    
    print(f"Calculating derivative of sin(x) at x={x}")
    print(f"True value (cos(1)): {np.cos(x)}")
    print("-" * 40)
    print(f"{'h':<10} | {'Calculated':<20} | {'Error':<20}")
    
    for h in h_values:
        # 严重的物理/数值隐患：没有处理 catastrophic cancellation
        # 当 h 很小时，sin(x+h) 和 sin(x) 非常接近，相减导致有效数字丢失
        diff = (np.sin(x + h) - np.sin(x)) / h
        
        # TODO (Task A): 
        # 1. 观察 h=1e-16 和 1e-17 时的输出
        # 2. 修改代码，计算绝对误差 error = abs(diff - np.cos(x))
        # 3. 将结果保存到列表，而不是仅仅打印
        
        print(f"{h:.1e}    | {diff:.20f} | ???")

if __name__ == "__main__":
    bad_derivative_demo()
