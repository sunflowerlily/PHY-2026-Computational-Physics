import numpy as np

def compute_potential_vectorized(X, Y, mass_pos, mass_val, G=1.0):
    """
    TODO: 使用 Numpy Broadcasting 实现向量化计算。
    目标：消除所有显式 Python 循环。
    
    参数:
    X, Y: 网格坐标 (H, W)
    mass_pos: 质量点位置 (N, 2)
    mass_val: 质量点质量 (N,)
    """
    # 提示：
    # 1. 将 X, Y 扩展为 (H, W, 1) 的三维张量
    # 2. 将 mass_pos 扩展为 (1, 1, N) 的三维张量
    # 3. 利用广播机制直接计算 dx, dy (H, W, N)
    # 4. 计算距离 r = sqrt(dx^2 + dy^2 + epsilon) (注意加软化因子 epsilon=1e-6 避免除零)
    # 5. 求和：V = sum(-G * m / r)
    
    # [STUDENT_CODE_HERE]
    # 请删除下面的 raise 语句并实现你的代码
    raise NotImplementedError("请在此处实现向量化代码 (删除此行)")
    
    return np.zeros_like(X)
