# 第 2 周：AI 时代的 Python 入门与代码审查

> **本周核心**：Python 不仅仅是脚本语言，它是连接人类物理直觉与机器计算能力的桥梁。在 AI 辅助编程时代，我们更需要理解代码背后的逻辑，以防止 AI 生成“看似正确实则荒谬”的物理代码。

## 1. 格式化输入输出 (I/O)：与宇宙对话的接口

物理实验记录讲究有效数字与单位，编程亦然。

### 1.1 `print` 的物理素养：f-string
在 Python 3.6+ 中，`f-string` 是打印物理量的最佳实践。它允许你直接控制**有效数字**和**科学计数法**。

```python
import numpy as np

mass = 1.989e30  # kg (Solar Mass)
radius = 6.9634e8 # m (Solar Radius)

# ❌ 糟糕的输出：难以阅读
print("Mass:", mass, "Radius:", radius)
# Output: Mass: 1.989e+30 Radius: 696340000.0

# ✅ 物理学家的输出：控制精度与对齐
print(f"Solar Mass:   {mass:.3e} kg")  # 科学计数法，保留3位小数
print(f"Solar Radius: {radius:.3e} m")
print(f"Density:      {mass / (4/3 * np.pi * radius**3):.2f} kg/m^3")
```

### 1.2 `input`：交互式实验
虽然在高性能计算中很少交互，但在教学演示中，`input` 可以让程序具有实验仪器的感觉。

```python
T = float(input("请输入系统温度 (K): "))  # 记得转换类型！input 返回的是 str
if T < 0:
    print("⚠️ 警告：检测到负绝对温度（除非你在做激光布居数反转实验）！")
```

---

## 2. 模块导入 (Modules)：巨人的肩膀

Python 的强大在于其生态。导入模块就像在实验室借用精密仪器。

*   `import numpy as np`：借用了一台超级计算机（矩阵运算）。
*   `import matplotlib.pyplot as plt`：借用了一台绘图仪。
*   `import scipy.constants as const`：查阅了物理常数表。

```python
import scipy.constants as const

print(f"光速 c = {const.c:.0f} m/s")
print(f"普朗克常数 h = {const.h:.2e} J·s")
```

> **AI 审查点**：AI 常喜欢 `from numpy import *`。**这是大忌！** 它会污染命名空间（例如 `sum` 会覆盖 Python 内置的求和函数），导致难以排查的 Bug。

---

## 3. 数据结构：构建物理模型的基础

### 3.1 基础类型
*   **Integer (int)**：量子数（如 $n, l, m$），粒子数。Python 的整数精度无限，不会溢出。
*   **Float (float)**：物理量（如坐标、速度）。遵循 IEEE 754 标准，有 15-17 位有效数字。
*   **String (str)**：粒子名称、文件路径。

### 3.2 容器类型
*   **List (list)**：可变序列。
    *   *物理类比*：一个随时间变化的粒子位置记录本 `[x_t0, x_t1, x_t2]`。
    *   `pos = [1.0, 1.1, 1.2]`
*   **Tuple (tuple)**：不可变序列。
    *   *物理类比*：时空坐标事件 `(t, x, y, z)`，一旦发生不可更改。
    *   `event = (0.5, 1.0, 2.0, 3.0)`
*   **Dictionary (dict)**：键值对。
    *   *物理类比*：粒子的属性卡片。
    *   `particle = {'name': 'electron', 'mass': 9.1e-31, 'charge': -1.6e-19}`
*   **Set (set)**：无序不重复集合。
    *   *物理类比*：费米子系统（全同粒子，但在集合论意义上用于去重）。

### 3.3 列表解析 (List Comprehension)
Pythonic 的精髓。
```python
# 生成前 10 个谐振子能级 E_n = n + 0.5
energies = [n + 0.5 for n in range(10)]
```

---

## 4. 控制流：时间的演化

### 4.1 循环 (Loops)
物理模拟的核心往往是时间步进。

*   `for`：已知步数（如演化 1000 年）。
*   `while`：未知步数，直到满足条件（如直到粒子逃逸）。

**⚠️ 代码审查：死循环与状态更新遗漏**
```python
t = 0
dt = 0.1
while t < 10:
    # do physics...
    # ❌ 错误：忘记更新 t，导致死循环 (Time Frozen)
    # t += dt  <-- 必须加上这行
    pass
```

### 4.2 条件判断 (If/Else)
物理中的边界条件或相变判断。
```python
if T > T_critical:
    phase = "Disordered"
else:
    phase = "Ordered"
```

---

## 5. 函数 (Functions)：物理定律的封装

函数是物理公式的代码化。

```python
def gravitational_force(m1, m2, r, G=6.67e-11):
    """
    计算两质点间的万有引力。
    
    参数:
    m1, m2: 质量 (kg)
    r: 距离 (m)
    G: 引力常数 (可选)
    
    返回:
    F: 力 (N)
    """
    if r == 0:
        raise ValueError("距离不能为 0 (Singularity)!")
    return G * m1 * m2 / r**2

f = gravitational_force(5.97e24, 70, 6.371e6)
```

*   **参数传递**：Python 是 "Pass by Object Reference"。对于可变对象（如 list），函数内修改会影响函数外！
*   **作用域 (Scope)**：函数内的变量是局部的。不要依赖全局变量（Global Variables），那是“幽灵超距作用”，是调试的噩梦。

---

## 6. 类与对象 (OOP)：天体物理的抽象

面向对象编程 (OOP) 非常适合描述具有内部状态和行为的物理实体。

### 6.1 抽象：以“行星”为例
一个行星有属性（质量、位置、速度）和行为（移动、受力）。

```python
class Planet:
    def __init__(self, name, mass, pos, vel):
        """构造函数：初始化行星状态"""
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        
    def kinetic_energy(self):
        """计算动能"""
        return 0.5 * self.mass * np.sum(self.vel**2)
    
    def update_position(self, dt):
        """时间演化：一阶欧拉法"""
        self.pos += self.vel * dt

# 实例化对象
earth = Planet("Earth", 5.97e24, [1.5e11, 0], [0, 30000])

print(f"{earth.name} KE: {earth.kinetic_energy():.2e} J")
earth.update_position(3600) # 演化 1 小时
```

> **思考**：为什么在高性能计算（如 N-body）中，我们通常不使用这种“纯 OOP”结构（每个粒子一个对象），而是使用“数组结构”（Structure of Arrays, SoA）？
> *答案：因为 Python 对象开销太大，且无法利用 CPU 缓存和向量化指令。OOP 适合高层逻辑，底层计算还是得靠 Numpy 数组。*

---
