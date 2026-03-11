# 第 2 周：AI 时代的 Python 入门与代码审查

> **本周核心**：Python 不仅仅是脚本语言，它是连接人类物理直觉与机器计算能力的桥梁。在 AI 辅助编程时代，我们不仅要会写代码，更要会**审查 (Review)** 代码。我们需要理解代码背后的逻辑与性能陷阱，以防止 AI 生成“看似正确实则荒谬”的物理代码。

### 一、格式化输入输出

物理实验记录讲究有效数字与单位，编程亦然。清晰的 I/O 是可复现研究的第一步。

#### 1. 输入：`input` 函数
`input(prompt='')` 函数仅有一个可缺省参数，`prompt` 为任意字符串，用于提示输入。
**注意：** `input` 函数返回值为**字符串类型**，在计算物理中，必须通过类型转换（如 `float()` 或 `int()`）转为数值类型才能参与公式计算。

**课堂示例：**
```python
# 接收输入并强制转换为浮点型（物理中常用）
# 审查要求：提示词中需写明物理单位
mass_str = input("请输入天体质量 (单位: kg): ")
mass_kg = float(mass_str) 

# 或者简写为一行：
radius = float(input("请输入轨道半径 (单位: m): "))
```

#### 2. 字符串与格式化输出
在 AI 生成的代码或历史文献中，你可能会看到三种不同的格式化输出版本。`f-string` 为最新版，也是本课程的推荐用法：

**最初版（% 占位符）**
```python
import numpy as np
print("圆周率的值是 %f" % (np.pi)) 
# 输出：圆周率的值是 3.141593
```

**第二版（`format` 方法）**
```python
print("圆周率的值是 {}".format(np.pi)) 
# 输出：圆周率的值是 3.141592653589793
```

**最新版（`f-string`）**
```python
print(f"圆周率的值是 {np.pi}") 
# 输出：圆周率的值是 3.141592653589793
```

#### 3. `f-string` 核心用法（计算物理场景）
以 `f` 或 `F` 修饰符引领的字符串，支持变量嵌入、格式限定、对齐设置。这在输出物理结果时极其重要：

**嵌入变量与科学计数法**
*(天体物理中经常处理极大或极小的数值，必须掌握 `.e` 科学计数法)*
```python
G = 6.6743e-11
print(f"万有引力常数 G 为 {G:.4e} m^3/(kg·s^2)")  
# 输出：万有引力常数 G 为 6.6743e-11 m^3/(kg·s^2)
```

**限定有效小数位数**
```python
period_days = 365.256363004
# 物理结果需控制有效数字，保留两位小数
print(f"地球公转周期为 {period_days:.2f} 天。")  
# 输出：地球公转周期为 365.26 天。
```

**设置对齐（用于输出实验数据表格）**
```python
star_name = "Sirius"
temperature = 9940
# < 左对齐，> 右对齐，数字代表字符宽度
print(f"|{'恒星名称':<10}|{'表面温度(K)':>12}|")
print(f"|{star_name:<10}|{temperature:>12}|")
# 输出：
# |恒星名称       |   表面温度(K)|
# |Sirius    |        9940|
```

### 二、Python 模块导入与矢量化思维

#### 1. 模块导入方式：全部导入
*一次性将模块中所有函数导入内存，调用时需带前缀。*

| 导入方式 | 调用方式 | 说明 |
| :--- | :--- | :--- |
| `import numpy` | `numpy.sqrt(2)` | 标准导入 |
| `import numpy as np` | `np.sqrt(2)` | **【强烈推荐】**导入并取别名，`np` 是科学界公认缩写 |
| `from numpy import *` | `sqrt(2)` | 导入所有函数，**【危险】**极易与其他模块函数重名冲突 |

#### 2. 模块导入方式：部分导入
*按需导入特定函数或类，调用时无需写前缀。注意：如果有多个模块包含同名函数（如 `math.sin` 和 `numpy.sin`），后导入的会覆盖先导入的。*

| 导入方式 | 调用方式 |
| :--- | :--- |
| `from numpy import sqrt` | `sqrt(2)` |
| `from numpy import sqrt, sin, pi` | `sin(pi / 2)` |
| `from numpy.random import random as rng` | `rng(2)` (生成2个随机数) |

#### 3. 常用科学计算模块一览
在计算物理与天文学中，我们通常会在代码开头一次性配置好“实验室环境”：

```python
# 推荐的高效导入方式
import numpy as np                 # 核心：矢量化数值计算
import matplotlib.pyplot as plt    # 核心：科学图表绘制
from scipy import constants        # 物理常数库（G, c, h 等）
import astropy.units as u          # 天文学专业物理单位库
```

#### 4. ⚠️ 核心避坑：为什么计算物理抛弃了 `math` 库？
*这是大一基础 C 语言/Python 课与大二《计算物理》的分水岭！*

*   **`math` 库（标量运算）**：专为单个数字设计。无法直接处理列表或数组。
*   **`numpy` 库（矢量运算）**：专为物理网格和多粒子系统设计。

**【课堂代码对比演示】**
假设我们要计算 100 万个数据点的正弦波（如处理干涉仪的电磁波信号）：

```python
import math
import numpy as np

# 生成包含 3 个空间坐标点的列表
x_list = [0.0, 1.57, 3.14]

# ❌ 错误示范 (math)：
# result = math.sin(x_list)  
# 运行将直接报错：TypeError! math.sin 不能处理列表！必须写繁琐且低效的 for 循环。

# ✅ 正确示范 (numpy 矢量化)：
x_array = np.array([0.0, 1.57, 3.14])
result = np.sin(x_array)  
# 瞬间输出: [0.  1.  0.00159] (整个数组被同时计算，极速且代码极其简洁)
```
**结论：** 在《计算物理》中，凡是涉及到数学函数（`sin, cos, exp, log`），**请彻底忘掉 `math`，全部使用 `numpy`！** 当审查 AI 生成的代码时，如果看到 AI 在用 `math` 库处理大规模数据，立刻让它重写为 `numpy` 矢量化代码。





### 三、Python 基础数据类型与物理映射

#### 1. Python 的 4 类基本数据类型总览
在物理模拟中，合理选择数据结构不仅影响代码可读性，更决定了内存占用与运行速度。
*   **Number (数值类)**：`int`, `float`, `complex`, `bool`
*   **序列类**：`String` (字符串), `List` (列表), `Tuple` (元组)
*   **集合类**：`set` (集合)
*   **映射类**：`dictionary` (字典)

#### 2. Number (数值类) 与物理精度
*   **`int`（整型）**：Python 中整数没有最大值限制。（物理场景：用于蒙特卡洛模拟的随机步数 $N$、粒子编号）。
*   **`float`（浮点型）**：默认是 C 语言的**双精度数 (Double)**，约保留 15~17 位有效数字。（物理场景：极其重要！求解微分方程时的连续变量 $x, t, v$ 全是 float）。
*   **`complex`（复数）**：Python 原生支持复数，语法为 `a+1j*b` 或 `1+2j`。（物理场景：天生为**量子力学（薛定谔方程波函数）**和交流电路分析准备）。
*   **`bool`（布尔型）**：
    *   `True`：所有非 False 的情况。
    *   `False`：`False`, `None`, `0`, `0.0`, `0+0j`, `''`, `[]`, `{}`, `()`。（物理场景：用于判断系统是否达到平衡态或能量是否收敛）。

#### 3. 序列类（有顺序元素的集合）
列表和元组的元素可以是任意类型，但在物理代码中，它们有截然不同的使命：
```python
Str = 'Python'                 # 字符串：多用于文件读写和图表标题
Lis = [1, 2, 3, 4, 1.5, 'Py']  # 列表：【可变容器】多用于在 while 循环中不断追加记录演化的历史轨迹 (trajectory.append(x))
Tup = (1, 2, 3, 4, 1.5, 'Py')  # 元组：【不可变容器】多用于绑定三维空间的固定坐标 (x, y, z)
```

#### 4. 序列类：索引和切片（提取物理数据）
无论字符串、列表还是元组，都共享这套极其强大的索引规则。
**正向与反向索引对比表**：

| 正向索引 | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **内容** | `1` | `2` | `3` | `4` | `1.5` | `'Python'` |
| **反向索引** | `-6` | `-5` | `-4` | `-3` | `-2` | `-1` |

**切片示例（物理数据截取与降采样）：**
```python
Str = 'Python'
print(Str[1:4])   # 结果：'yth' (包头不包尾)

# 【计算物理常用技巧】
trajectory = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
print(trajectory[-1])  # 获取模拟的【最终状态】(0.5)
print(trajectory[::2]) # 步长为2，提取 [0.0, 0.2, 0.4]，用于庞大数据的【降采样】以节省内存
```

#### 5. 集合类 (set) 与 映射类 (dictionary)
*   **`set` (容器：存储一组唯一且无序的元素)**
    *   物理场景：用于找出多粒子碰撞网络中的独立节点，或剔除重复的能量本征态。
    ```python
    set1 = {1, 2, 3, 4}
    set2 = set([3, 4, 5, 6])
    union_set = set1.union(set2)  # 并集，结果 {1,2,3,4,5,6}
    ```

*   **`dictionary` (容器：存储 key: value 对)**
    *   **计算物理核心用法：** 抛弃零散的变量，使用字典将**物理系统的初始参数**打包，方便传递给求解函数！
    ```python
    # 创建天体物理系统参数字典
    star_system = {'name': 'Sirius', 'mass': 2.06, 'radius': 1.71}
    
    # 修改与添加参数
    star_system['mass'] = 2.10          # 修正质量测量值
    star_system['temperature'] = 9940   # 动态添加表面温度
    
    print(star_system['mass'])          # 输出: 2.10
    ```

#### 6. 进阶语法：列表解析式 (List Comprehension)
这是 Python 的“灵魂语法”，能用一行代码替代繁琐的 `for` 循环生成列表。
```python
# 传统写法 (计算前 5 个整数的平方)
squares = []
for i in range(5):
    squares.append(i**2)

# 列表解析式写法 (极其优雅)
# 语法：[表达式 for 变量 in 序列]
squares_lc = [i**2 for i in range(5)]
print(squares_lc)  # 输出: [0, 1, 4, 9, 16]

# 物理场景：计算一组粒子的动能 E_k = 0.5 * m * v^2 (假设 m=1.0)
velocities = [10, 20, 30]
energies = [0.5 * 1.0 * v**2 for v in velocities]
```

**⚠️ AI 代码审查警告：列表解析式 vs `Numpy` 数组**
如果 AI 用列表解析式处理 $10^6$ 个粒子的速度（如 `[math.sin(v) for v in velocities]`），请立即让它重写！
**原则：** 数据量 $< 1000$ 时，列表解析式很优雅；数据量极大时，必须使用 `Numpy` 的数组！



### 四、程序控制：for / while / continue / break

#### 1. for 循环

**适用场景：**  
- 对“序列类”对象（如字符串、列表、`numpy` 数组）逐元素遍历；  
- 已知需要循环的次数。

**示例 1：遍历字符串**

```python
s = 'abcde'
for e in s:
    print(e)
```

**示例 2：遍历数组元素**

```python
import numpy as np

a = np.arange(10)   # a = [0 1 2 3 4 5 6 7 8 9]
for i in range(10):
    print(a[i])
```

> 提示：`range(n)` 常用于“循环 n 次”的场景，`np.arange` 更适合生成数值网格、配合数值计算使用。 [realpython](https://realpython.com/how-to-use-numpy-arange/)

***

#### 2. `range` 函数

`range(start, stop, step)` 返回一个可迭代对象，用于 `for` 循环计数。

```python
for i in range(1, 6, 2):
    print(i, end='')   # 输出：135
```

说明：  
- `start` 为起始值（包含）；  
- `stop` 为结束值（不包含）；  
- `step` 为步长，可以为负数。

***

#### 3. while 循环

**适用场景：**  
- 知道循环“开始 / 终止条件”，但**不知道具体循环次数**；  
- 常用于“时间推进”“迭代收敛”等数值计算。

基本结构：

```python
i = 0
while i < 10:
    print(i)
    i = i + 1
```

> 注意：`while` 循环中必须有**状态更新**（如 `i = i + 1`），否则容易产生**死循环**。 [pythonmorsels](https://www.pythonmorsels.com/while-loops/)

***
确实需要，把 `if / else` 放在控制流里才完整，而且后面做“状态更新检查、边界判断”时全靠它。

下面是在原有 PPT 风格基础上的补充版，你可以直接插到“while 循环”与“continue/break”之间：

***

#### 4. 条件判断：`if / elif / else`

**作用：**  
根据条件（True / False）决定代码是否执行，是所有控制流的基础。

**基本结构：**

```python
x = 3

if x > 0:
    print("x 是正数")
elif x == 0:
    print("x 等于 0")
else:
    print("x 是负数")
```

说明：  
- `if` 后跟条件表达式，为真则执行缩进块；  
- `elif` 为“否则如果”，可以有多个；  
- `else` 捕获前面条件都不满足的情况，可选。

**与循环配合的简单示例：**

```python
for i in range(-2, 3):
    if i < 0:
        print(i, "是负数")
    elif i == 0:
        print(i, "等于 0")
    else:
        print(i, "是正数")
```

在后续的数值计算中，`if` 常用于：  
- 判断是否越界（例如位置是否超出模拟区域）；  
- 判断是否满足停止条件（如误差是否小于给定阈值）。


#### 4. `continue` 和 `break`

**`continue`：跳过当前这一轮循环，直接进入下一轮。**

```python
for i in range(6):
    if i == 3:
        continue
    print(i, end='')   # 输出：01245
```

**`break`：终止整个循环。**

```python
for i in range(6):
    if i == 3:
        break
    print(i, end='')   # 输出：012
```


### 五、函数定义与调用：参数、返回值与作用域

#### 1. 函数的作用

- 把**一段可重复使用的代码**打包起来，起一个名字，方便多次调用。  
- 以后写数值算法（比如一步时间推进、一次积分）时，会把“单步操作”写成函数。

#### 2. 函数定义与调用的基本语法

**定义函数：**

```python
def 函数名(参数列表):
    函数体
    return 返回值   # 可选
```

**简单示例：**

```python
# 定义一个求平方的函数
def square(x):
    return x * x

# 调用函数
y = square(3)
print(y)   # 输出：9
```

要点：  
- `def` 是关键词；  
- 函数名尽量见名知意；  
- `return` 把结果“交还”给调用者，可以在后面继续运算。

***

#### 3. 参数传递与默认参数

**位置参数：**

```python
def add(a, b):
    return a + b

result = add(2, 5)
print(result)   # 输出：7
```

**默认参数：**

```python
# b 有默认值 1
def power(a, b=1):
    return a ** b

print(power(3))      # 使用默认参数，输出：3
print(power(3, 2))   # 覆盖默认参数，输出：9
```

***

#### 4. 返回值：单个与多个

**单个返回值：**

```python
def average(a, b):
    return (a + b) / 2

print(average(3, 5))   # 输出：4.0
```

**多个返回值（实际上是返回一个元组）：**

```python
def min_max(a, b):
    if a < b:
        return a, b
    else:
        return b, a

m, M = min_max(3, 5)
print(m, M)   # 输出：3 5
```

***

#### 5. 变量作用域（scope）

- **局部变量**：在函数内部定义，只在函数内部可见。  
- **全局变量**：在函数外定义，整个文件内都可访问（不建议在函数内随意修改）。

**示例：**

```python
x = 10   # 全局变量

def test():
    y = 5          # 局部变量，只在 test 内有效
    print(x, y)    # 可以访问全局变量 x

test()             # 输出：10 5
# print(y)         # 这一行会报错，y 未定义
```

常犯错误：  
- 在函数里试图使用还没定义的变量；  
- 误以为在函数内部改了某个变量，就会自动影响外部同名变量。


### 六、类与对象（OOP 基础语法）

#### 1. 为什么需要类

- 函数可以打包“一段操作”，  
- **类（class）可以同时打包“数据 + 操作”**。  
在实际项目中，如果某个“东西”既有属性（数据），又有方法（操作），就适合用类来表示。

***

#### 2. 定义一个最简单的类

**基本语法：**

```python
class 类名:
    def __init__(self, 参数列表):
        # 初始化对象属性
        ...
```

**示例：定义一个表示点的类（二维坐标）**

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x    # 把参数 x 存到对象属性 self.x 中
        self.y = y    # 把参数 y 存到对象属性 self.y 中
```

要点：  
- `class` 关键字定义类；  
- `__init__` 是构造函数，在创建对象时自动调用；  
- `self` 代表“这个对象本身”，用来绑定属性。

***

#### 3. 创建对象与访问属性

**创建对象（实例化）：**

```python
p = Point2D(1.0, 2.0)   # 创建一个点，x=1.0, y=2.0
```

**访问属性：**

```python
print(p.x)   # 输出：1.0
print(p.y)   # 输出：2.0
```

说明：  
- `对象.属性名` 的方式访问或修改属性；  
- 属性可以是任意类型（数值、字符串、列表等）。

***

#### 4. 在类中定义方法（对象的“操作”）

在类内部，除了 `__init__` 以外，还可以定义普通方法，**第一个参数必须是 `self`**：

```python
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 计算到原点的距离
    def distance_to_origin(self):
        return (self.x**2 + self.y**2) ** 0.5

    # 平移点的位置
    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
```

**调用方法：**

```python
p = Point2D(3.0, 4.0)
d = p.distance_to_origin()
print(d)           # 输出：5.0

p.move(1.0, -2.0)
print(p.x, p.y)    # 输出：4.0 2.0
```

***

#### 5. 一个更贴近后续物理的示例：粒子类（不讲物理细节）

这个例子先不讲具体物理含义，只是示范“类里可以有多个属性和方法”，方便你后面在数值模拟章节直接替换为真实物理模型。

```python
class Particle:
    def __init__(self, x, v, m):
        self.x = x    # 位置
        self.v = v    # 速度
        self.m = m    # 质量

    def kinetic_energy(self):
        return 0.5 * self.m * self.v**2

    def move(self, dt):
        # 简单示例：匀速直线运动
        self.x = self.x + self.v * dt
```

**使用示例：**

```python
p = Particle(x=0.0, v=10.0, m=1.0)
print(p.kinetic_energy())   # 输出：50.0
p.move(0.1)
print(p.x)                  # 输出：1.0
```

后面要讲天体物理时，可以把这个 `Particle` 的属性改成 `mass, position, velocity` 三维向量，把 `move` 换成“根据引力更新位置”的方法，结构是一样的。



## 7. 本周作业预告

1.  **AI 代码鉴伪**：我们会给你一段由 AI 生成的、看似完美但包含 3 个物理/编程陷阱的代码（如单位混淆、深/浅拷贝错误、循环累积误差）。你的任务是找出并修复它们。
2.  **重构练习**：将一段充满 `global` 变量和硬编码数字的脚本，重构为模块化、含类型提示的函数库。
