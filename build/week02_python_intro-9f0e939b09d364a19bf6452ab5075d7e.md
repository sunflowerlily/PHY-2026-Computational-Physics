# 第 2 周：AI 时代的 Python 入门与代码审查

> **本周核心**：Python 不仅仅是脚本语言，它是连接人类物理直觉与机器计算能力的桥梁。在 AI 辅助编程时代，我们不仅要会写代码，更要会**审查 (Review)** 代码。我们需要理解代码背后的逻辑与性能陷阱，以防止 AI 生成“看似正确实则荒谬”的物理代码。

## 1. 格式化输入输出 (I/O)：与宇宙对话的接口

物理实验记录讲究有效数字与单位，编程亦然。清晰的 I/O 是可复现研究的第一步。

### 1.1 `print` 的物理素养：f-string
在 Python 3.6+ 中，`f-string` (Formatted String Literals) 是打印物理量的最佳实践。它比旧式的 `%` 格式化或 `.format()` 更快、更易读。

**物理学家需要掌握的格式化技巧：**
*   **科学计数法** (`e`): 处理天体尺度 ($10^{30}$) 或原子尺度 ($10^{-34}$)。
*   **有效数字** (`.Nf`): 匹配实验仪器的精度。
*   **对齐与填充** (`>10`): 生成整齐的数据表格。

```python
import numpy as np

mass = 1.9891e30  # kg (Solar Mass)
radius = 6.9634e8 # m (Solar Radius)
G = 6.67430e-11   # m^3 kg^-1 s^-2

# ❌ 糟糕的输出：难以阅读，没有对齐
print("Mass:", mass, "Radius:", radius)
# Output: Mass: 1.9891e+30 Radius: 696340000.0

# ✅ 物理学家的输出：控制精度与对齐
print(f"{'Parameter':<15} | {'Value':<15} | {'Unit':<5}")
print("-" * 40)
print(f"{'Solar Mass':<15} | {mass:>15.4e} | kg")
print(f"{'Solar Radius':<15} | {radius:>15.4e} | m")
print(f"{'Surface G':<15} | {G * mass / radius**2:>15.2f} | m/s^2")
```

> **AI 审查点**：AI 有时会生成旧式的 `%g` 或 `%f`，导致非常大或非常小的数字显示为 `0.000000` 或 `inf`。强制要求使用科学计数法。

### 1.2 `input`：交互式实验
虽然在高性能计算 (HPC) 中我们通常通过配置文件或命令行参数传参，但在教学演示脚本中，`input` 可以提供交互感。

```python
# ⚠️ 注意：input() 永远返回字符串 (str)
user_input = input("请输入模拟时间步长 dt [fs]: ")

try:
    dt = float(user_input)
    if dt <= 0:
        raise ValueError("时间步长必须为正数！")
except ValueError as e:
    print(f"❌ 输入错误: {e}")
    dt = 0.1 # 设置默认回退值
    print(f"⚠️ 已自动使用默认值: dt = {dt} fs")
```

---

## 2. 模块导入 (Modules)：巨人的肩膀

Python 的强大在于其生态。导入模块就像在实验室借用精密仪器。

### 2.1 导入的最佳实践
*   `import numpy as np`：标准缩写，全球通用。
*   `import matplotlib.pyplot as plt`：绘图标准。
*   `import scipy.constants as const`：物理常数库。

```python
import scipy.constants as const

# 直接使用精确的物理常数，避免手动输入引入误差
E_photon = const.h * const.c / 500e-9  # 500nm 光子的能量
print(f"Energy: {E_photon / const.e:.3f} eV")
```

### 2.2 命名空间污染 (Namespace Pollution)
这是新手和 AI 最容易犯的错误。

**❌ 危险写法：**
```python
from numpy import *
from math import *

# 灾难发生：
# numpy.sqrt 支持数组，math.sqrt 只支持标量。
# 后导入的 math.sqrt 覆盖了 numpy.sqrt。
x = array([1, 4, 9])
y = sqrt(x)  # 报错！TypeError: only size-1 arrays can be converted to Python scalars
```

**✅ 安全写法：**
```python
import numpy as np
import math

# 明确指明调用来源
y_arr = np.sqrt(np.array([1, 4, 9]))
y_val = math.sqrt(4)
```

---

## 3. 数据结构：构建物理模型的基础

选择正确的数据结构，往往决定了算法的复杂度。

### 3.1 基础类型
*   **Integer (int)**：量子数 ($n, l, m$)，粒子数。Python 3 的整数精度仅受限于内存。
*   **Float (float)**：物理量。遵循 IEEE 754 双精度标准。
    *   *陷阱*：`0.1 + 0.2 != 0.3`。永远不要用 `==` 比较浮点数，请使用 `abs(a - b) < epsilon` 或 `np.isclose(a, b)`。
*   **String (str)**：标签、路径。

### 3.2 容器类型详解
| 类型 | 特点 | 物理应用场景 | 复杂度 (查找) |
| :--- | :--- | :--- | :--- |
| **List** `[]` | 可变，有序 | 随时间记录的轨迹 `[x_t0, x_t1]` | $O(N)$ |
| **Tuple** `()` | **不可变**，有序 | 时空事件 `(t, x, y, z)`，配置参数 | $O(N)$ |
| **Dict** `{}` | 键值对，无序 | 粒子属性 `{'mass': m, 'charge': q}` | **$O(1)$** |
| **Set** `{}` | 无序，去重 | 统计独立态，费米子占据数 | **$O(1)$** |

**List Slicing (切片) —— 提取子系统：**
```python
data = [10, 20, 30, 40, 50, 60]
print(data[0:3])   # 前三个点 (0, 1, 2)
print(data[-1])    # 最后一个点 (边界条件)
print(data[::2])   # 降采样 (Downsampling)，每隔一个取一个
```

### 3.3 列表解析 (List Comprehension)
Pythonic 的精髓，比 `for` 循环快且简洁。

```python
# 任务：筛选出能量大于 0 的粒子，并计算其动量 p = sqrt(2mE)
mass = 1.0
energies = [-0.5, 1.2, 3.4, -0.1, 5.0]

# 传统写法 (5行)
momenta = []
for E in energies:
    if E > 0:
        momenta.append((2 * mass * E)**0.5)

# 列表解析 (1行)
momenta = [(2 * mass * E)**0.5 for E in energies if E > 0]
```

---

## 4. 控制流：时间的演化

### 4.1 循环的高级用法
物理系学生常写 C 风格的 `range(len(...))` 循环，这在 Python 中不够优雅。

*   **`enumerate`**：同时获取索引和值（例如：需要知道这是第几个粒子）。
*   **`zip`**：同时遍历多个数组（例如：位置和速度）。

```python
positions = [0.1, 0.5, 0.9]
velocities = [1.0, -1.0, 0.5]

# 优雅地同时更新 r 和 v
for i, (r, v) in enumerate(zip(positions, velocities)):
    print(f"Particle {i}: r={r}, v={v}")
```

### 4.2 代码审查：死循环与状态更新遗漏
这是动力学模拟中最常见的 Bug。

**🐛 典型错误代码 (Bad Code)：**
```python
t = 0
dt = 0.01
T_max = 10.0

while t < T_max:
    force = -k * x
    v = v + force * dt
    x = x + v * dt
    # 😱 致命错误：忘记更新时间 t
    # 结果：程序永远运行，CPU 100%，且物理状态不再随时间变化（如果是显式含时势场）
```

**✅ 修复方案：**
1.  显式检查 `t += dt`。
2.  设置最大迭代次数 `max_steps` 作为保险丝。

---

## 5. 函数 (Functions)：物理定律的封装

### 5.1 参数传递与默认值陷阱
Python 的函数参数传递是 "Pass by Assignment"。

**⚠️ 默认参数陷阱 (Mutable Default Argument)：**
```python
# ❌ 错误：不要用可变对象 (list) 作为默认值
def add_particle(p, system=[]):
    system.append(p)
    return system

sys1 = add_particle('electron') # ['electron']
sys2 = add_particle('proton')   # ['electron', 'proton'] -> 惊！sys2 竟然包含了 sys1 的电子！
```
*原因：函数默认值在定义时只被创建一次，所有调用共享同一个列表对象。*

**✅ 正确做法：**
```python
def add_particle(p, system=None):
    if system is None:
        system = []
    system.append(p)
    return system
```

### 5.2 类型提示 (Type Hinting)
在 AI 时代，类型提示能极大帮助 Copilot/Trae 理解你的意图。

```python
def kinetic_energy(mass: float, velocity: float) -> float:
    """计算经典动能"""
    return 0.5 * mass * velocity**2
```

---

## 6. 类与对象 (OOP)：天体物理的抽象

面向对象编程 (OOP) 适合描述具有内部状态和行为的物理实体。

### 6.1 `__init__`, `__str__`, `__repr__`
让你的对象在调试时会“说话”。

```python
class Planet:
    def __init__(self, name, mass, pos):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos)
        
    def __str__(self):
        """面向用户的打印信息"""
        return f"Planet {self.name} at {self.pos}"
    
    def __repr__(self):
        """面向开发者的调试信息 (通常是可以复制执行的代码)"""
        return f"Planet(name='{self.name}', mass={self.mass}, pos={self.pos.tolist()})"

earth = Planet("Earth", 5.97e24, [1, 0, 0])
print(earth)          # Planet Earth at [1 0 0]
print([earth])        # [Planet(name='Earth', mass=5.97e+24, pos=[1, 0, 0])]
```

### 6.2 继承 (Inheritance)
复用代码，建立物理分类学。

```python
class Star(Planet): # 星星也是天体，继承 Planet 的基础属性
    def __init__(self, name, mass, pos, luminosity):
        super().__init__(name, mass, pos) # 调用父类初始化
        self.luminosity = luminosity
    
    def get_flux(self, distance):
        return self.luminosity / (4 * np.pi * distance**2)
```

### 6.3 性能警告：AoS vs SoA
在处理 N 体问题 (N > 1000) 时，OOP 往往是性能瓶颈。

*   **AoS (Array of Structures)**: `[Particle(), Particle(), ...]`
    *   *优点*：直观，符合人类思维。
    *   *缺点*：内存不连续，无法向量化，缓存未命中率高。
*   **SoA (Structure of Arrays)**: `class System: self.x = array([...])`
    *   *优点*：内存连续，支持 SIMD/Numpy 加速。
    *   *缺点*：稍微抽象一点。

> **结论**：在计算物理中，**少用 list of objects，多用 object containing arrays**。

---

## 7. 本周作业预告

1.  **AI 代码鉴伪**：我们会给你一段由 AI 生成的、看似完美但包含 3 个物理/编程陷阱的代码（如单位混淆、深/浅拷贝错误、循环累积误差）。你的任务是找出并修复它们。
2.  **重构练习**：将一段充满 `global` 变量和硬编码数字的脚本，重构为模块化、含类型提示的函数库。
