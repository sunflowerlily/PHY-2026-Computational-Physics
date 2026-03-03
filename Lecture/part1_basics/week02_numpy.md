# 第 2 周：Numpy 向量化与科学可视化（从数据到直觉）

> **本周名言**："In Python, loops are slow. Vectorization is the way." —— 每一个被 `for` 循环折磨过的计算物理学家

## 1. 核心目标 (Learning Objectives)
*   **物理认知**：理解“向量化”不仅是代码优化，更是物理场论思维（整体演化 vs 逐点计算）的体现。
*   **数值技巧**：掌握 Numpy 广播机制与插值算法（Cubic Spline），学会用 Matplotlib 绘制科研级图表。
*   **AI 协同**：识破 AI 生成的低效循环代码，学会用 Prompt 引导 AI 进行向量化重构。

## 2. 物理翻译与数值基石 (Physics & Numerical Foundations)

### 2.1 拒绝循环：搬运工 vs 大卡车
在经典的 C/Fortran 时代，我们习惯像“搬运工”一样，一次搬一块砖（处理一个数据点）：
```c
for (int i=0; i<N; i++) { r[i] = x[i] + y[i]; }
```
但在 Python 中，这种写法是**极其低效**的。Python 的解释器开销巨大。
**向量化 (Vectorization)** 就像开了一辆“大卡车”，一次把所有砖（整个数组）装上车，运到 C 语言底层批量处理。
*   **物理类比**：
    *   **循环**：牛顿力学中的质点动力学（一个一个粒子算）。
    *   **向量化**：流体力学或场论（整个流场同时演化）。

### 2.2 数据重构：插值 (Interpolation)
实验数据总是离散的，但物理定律是连续的。我们需要“脑补”中间的过程。
*   **拉格朗日插值**：用一个高阶多项式穿过所有点。
    *   *痛点*：**龙格现象 (Runge's phenomenon)** —— 边缘处会出现剧烈的非物理振荡（能量不守恒的幻觉）。
*   **三次样条 (Cubic Spline)**：分段用三次多项式连接，保证 $f, f', f''$ 连续。
    *   *物理意义*：模拟一根经过所有数据点的弹性金属条，其**弯曲能量** $\int (f'')^2 dx$ 最小。

## 3. AI 协同与 Code Review 靶场 (AI Synergy & Code Review)

### 【AI 的天真解法】
当你问 AI：“帮我计算两个大数组的距离矩阵”，它可能会给你这样的代码：

```python
import numpy as np
import time

# AI 生成的低效代码
def calc_distance_loop(r1, r2):
    n = len(r1)
    m = len(r2)
    dist = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            # 典型的 O(N*M) 循环，Python 层面执行
            dist[i, j] = np.sqrt(np.sum((r1[i] - r2[j])**2))
    return dist
```

### 【物理与性能破绽分析】
1.  **性能崩塌**：对于 $N=1000$ 个粒子，这需要执行 $10^6$ 次 Python 循环，耗时可能达到秒级甚至分钟级。
2.  **物理直觉缺失**：物理学家看空间距离，应该看到的是“场”的相互作用，而不是孤立的点对点。

### 【向量化修正】
利用 Numpy 的**广播机制 (Broadcasting)**，我们可以将维度扩展，让底层 C 代码自动对齐计算。

```python
# 物理学家的向量化解法
def calc_distance_vectorized(r1, r2):
    # r1: (N, 3) -> (N, 1, 3)
    # r2: (M, 3) -> (1, M, 3)
    # 差值: (N, M, 3) (自动广播)
    diff = r1[:, np.newaxis, :] - r2[np.newaxis, :, :]
    
    # 在最后一个维度求模
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    return dist
```
*   **Prompt 技巧**：告诉 AI “请使用 Numpy Broadcasting 消除所有显式循环”。

## 4. 可视化与物理洞察 (Visualization & Insights)

### 4.1 像发表论文一样绘图
不要使用默认的丑陋风格。

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",  # 衬线字体 (Times New Roman 风格)
    "font.size": 12,
    "axes.labelsize": 14,
    "figure.figsize": (8, 6),
    "text.usetex": False     # 如果安装了 LaTeX 可设为 True
})

fig, ax = plt.subplots()
# ... 绘图代码 ...
ax.set_aspect('equal') # 物理陷阱：画场时必须保证纵横比一致！
```

### 4.2 场的可视化：电偶极子
(代码见上周作业，此处强调物理意义)
*   **Contour (等高线)**：标量场（电势）的地形图。
*   **Streamplot (流线)**：矢量场（电场线）的流动方向。

## 5. 课后挑战 (GitHub Classroom Lab)

### 基础任务：星系光谱的红移校正
**物理背景**：宇宙膨胀导致星系光谱红移 $\lambda_{obs} = (1+z)\lambda_{rest}$。
**任务**：
1.  读取 `code/galaxy_spectrum.txt`。
2.  使用 **Cubic Spline** 插值，将不均匀采样的光谱重采样到均匀网格上。
3.  画出光谱图，并标注 H-alpha 发射线。

### AI 探究任务：Lissajous 图形的“混沌”边界
**任务**：
1.  向 AI 索要一段 `FuncAnimation` 代码，绘制 Lissajous 图形。
2.  **Code Review**：检查 AI 是否正确处理了 `frames` 和 `interval`？如果频率比 $\omega_x/\omega_y$ 是无理数（如 $\pi$），AI 画出的轨迹闭合了吗？（物理上应该是不闭合的，但在有限时间内看起来如何？）
3.  **可视化**：修改代码，让轨迹颜色随时间变化（用 `scatter` 替代 `plot`），展示“时间演化”的过程。

## 6. 常见物理陷阱 (Physics Pitfalls)
1.  **整数除法**：在旧代码或某些语言中 `1/2 = 0`。Python 3 虽然修正了，但在计算索引时务必用 `//`。
2.  **混叠效应 (Aliasing)**：画高频波形时，如果采样点太少（违背奈奎斯特采样定理），你会看到虚假的低频波（莫尔条纹）。**物理学家永远要怀疑：你看到的周期性是真的吗？**
3.  **视图与拷贝**：`b = a` 只是起了个别名。修改 `b` 会同时改变 `a`。这在模拟粒子演化时会导致“幽灵作用”。请用 `b = a.copy()`。

## 7. 文件保存与反馈
*   **保存路径**：`MyComputationalPhysics/part1_basics/week02_numpy.md`
*   **反馈**：讲义已生成。本周重点在于从“点对点”思维转向“场”思维（向量化），并利用插值处理真实天文数据。作业中的星系光谱重采样是一个非常好的实战案例。
