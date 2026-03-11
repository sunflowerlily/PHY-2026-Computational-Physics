import numpy as np
import pytest
import sys
import os

# 确保能导入 src 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.good_particle import Particle

def test_unit_conversion():
    """
    测试角度是否正确转为弧度。
    使用随机生成的角度，防止学生硬编码特定值。
    """
    np.random.seed(42)
    # 随机生成 5 个角度 (0~360)
    angles = np.random.uniform(0, 360, 5)
    v = 10.0
    dt = 1.0
    
    for angle in angles:
        p = Particle(0, 0, angle, v)
        p.move(dt)
        
        # 理论预期值
        theta_rad = np.radians(angle)
        expected_x = v * np.cos(theta_rad) * dt
        expected_y = v * np.sin(theta_rad) * dt
        
        # 允许 1e-5 的浮点误差
        assert np.isclose(p.pos[0], expected_x, atol=1e-5), f"❌ 角度 {angle:.1f} 度计算错误！math.cos 接收的是弧度吗？"
        assert np.isclose(p.pos[1], expected_y, atol=1e-5), f"❌ 角度 {angle:.1f} 度计算错误！"

def test_independence():
    """
    测试是否修复了浅拷贝问题。
    """
    p1 = Particle(0, 0, 0, 0)
    
    # 尝试模拟创建一个新粒子（这里虽然没有显式 copy，但测试 p1 和 p2 是否独立）
    # 学生的类应该支持创建两个独立的实例
    p2 = Particle(0, 0, 0, 0)
    
    # 修改 p2
    p2.move(10)
    p2.pos[0] = 999
    
    # p1 应该保持不动
    assert p1.pos[0] == 0, "❌ 粒子之间存在量子纠缠！修改 p2 导致 p1 也变了？检查你的变量赋值。"

def test_vectorization_type():
    """
    强制检查：pos 属性必须是 numpy 数组，不能是 list。
    这是为了后续的高性能计算做准备。
    """
    p = Particle(0, 0, 45, 10)
    
    # 1. 类型检查
    assert isinstance(p.pos, np.ndarray), "❌ 请使用 numpy.array 存储位置，不要用 list！"
    assert isinstance(p.vel, np.ndarray) or hasattr(p, 'v'), "❌ 建议使用 numpy.array 存储速度向量"
    
    # 2. 形状检查
    assert p.pos.shape == (2,), "❌ 位置数组形状不对，应该是 (2,)"
    
    # 3. 数据类型检查 (必须是 float)
    assert p.pos.dtype.kind == 'f', "❌ 位置数组必须是浮点型 (float)"

def test_energy_conservation():
    """
    物理守恒量检查：匀速直线运动，动能应该守恒。
    """
    v_init = 10.0
    p = Particle(0, 0, 30, v_init)
    
    # 移动 100 步
    for _ in range(100):
        p.move(0.1)
        
    # 计算当前速度模长
    # 如果学生没有显式存 vel，可以从位移推算（这里假设学生实现了 vel 属性）
    if hasattr(p, 'vel'):
        v_curr = np.linalg.norm(p.vel)
        assert np.isclose(v_curr, v_init), "❌ 速度模长发生改变！这是匀速运动，动能应该守恒。"
