import math

class BadParticle:
    """
    【警告】
    这段代码是由一个不懂物理的 AI 生成的。
    它包含至少 3 个严重的物理或编程错误。
    请找出它们！
    """
    def __init__(self, x, y, angle_deg, v):
        self.pos = [x, y]  # 使用列表存储坐标 (陷阱1: 列表不是矢量)
        self.v = v
        self.angle = angle_deg # 陷阱2: 存的是角度，后面直接传给 sin/cos

    def move(self, dt):
        # 陷阱2: math.sin 接收弧度，这里却传了角度
        # 导致运动方向完全混乱
        vx = self.v * math.cos(self.angle)
        vy = self.v * math.sin(self.angle)
        
        # 陷阱3: 极其不规范的列表索引更新
        # 如果 self.pos 是 tuple，这里会报错；如果是 list，虽然能跑但不推荐
        self.pos[0] += vx * dt
        self.pos[1] += vy * dt

def simulate_two_particles():
    print("--- Simulation Start ---")
    p1 = BadParticle(0, 0, 45, 10)
    
    # 陷阱4 (最致命): 浅拷贝灾难！
    # 意图是创建一个新粒子 p2，初始状态和 p1 一样
    # 但实际上 p2 只是 p1 的别名 (引用)
    p2 = p1 
    
    print(f"Initial p1: {p1.pos}")
    
    # 移动 p2
    print("Moving p2...")
    p2.move(1.0)
    
    # 打印 p1 的位置 -> 惊恐地发现 p1 也动了！
    print(f"p1 position: {p1.pos} (Why did I move?)") 
    print(f"p2 position: {p2.pos}")
    
    if p1.pos == p2.pos:
        print("!!! GHOST ENTANGLEMENT DETECTED !!!")

if __name__ == "__main__":
    simulate_two_particles()
