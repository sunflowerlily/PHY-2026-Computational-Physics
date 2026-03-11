import numpy as np

class Particle:
    """
    TODO: 重构 Particle 类
    1. 使用 np.array 存储位置 (self.pos)
    2. 使用 np.array 存储速度 (self.vel)
    3. 初始化时将角度转换为弧度 (np.radians)
    4. move 方法使用矢量加法: self.pos += self.vel * dt
    """
    def __init__(self, x, y, angle_deg, v):
        """
        初始化粒子
        x, y: 初始位置
        angle_deg: 运动方向 (角度制)
        v: 速率
        """
        # [YOUR CODE HERE]
        # self.pos = np.array([x, y], dtype=float)
        # theta = ...
        # self.vel = np.array([...], dtype=float)
        pass

    def move(self, dt):
        """
        更新粒子位置
        """
        # [YOUR CODE HERE]
        pass
