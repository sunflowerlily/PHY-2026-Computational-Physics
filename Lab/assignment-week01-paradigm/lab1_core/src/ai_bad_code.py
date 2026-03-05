import numpy as np

def naive_derivative(f, x):
    """
    AI 生成的代码：试图通过极小的步长获得高精度。
    但是忽略了浮点数的舍入误差陷阱。
    """
    # 错误：步长太小，进入了舍入误差主导区
    h = 1e-15  
    
    # 前向差分 (Forward Difference)
    # 理论误差 O(h)，但在此 h 下，f(x+h) - f(x) 几乎为 0 (catastrophic cancellation)
    return (f(x + h) - f(x)) / h

def main():
    x = np.pi / 4
    exact = np.cos(x)
    
    approx = naive_derivative(np.sin, x)
    error = abs(approx - exact)
    
    print(f"Exact value: {exact}")
    print(f"AI approx (h=1e-15): {approx}")
    print(f"Error: {error}")
    
    if error > 1e-2:
        print(">>> 警告：误差巨大！AI 掉进了'舍入误差'的陷阱！")
        print(">>> 提示：试着增大步长 h，或者改用中心差分公式。")
    else:
        print(">>> 居然蒙对了？不可能，h=1e-15 对于 float64 来说太小了。")

if __name__ == "__main__":
    main()
