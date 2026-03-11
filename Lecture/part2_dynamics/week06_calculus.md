# 第三周：数值微积分与线性代数

> **本周名言**："God made the integers, all else is the work of man." —— Leopold Kronecker (但在计算物理中，我们把连续的自然离散化为整数索引)

## 1. 物理翻译：从连续到离散

物理定律通常用**微分方程**（连续语言）书写，但计算机只能处理**离散数组**。
*   **微分 (Differentiation)** $\rightarrow$ **差分 (Finite Difference)**
*   **积分 (Integration)** $\rightarrow$ **求和 (Summation)**

本周的目标是建立这种映射，并理解随之而来的代价——**误差**。

---

## 2. 数值微分：捕捉变化

### 2.1 有限差分法 (Finite Difference)

如何从离散的位置数据 $x[i]$ 计算速度 $v[i]$？

*   **前向差分 (Forward)**：$f'(x) \approx \frac{f(x+h) - f(x)}{h}$ (精度 $O(h)$)
*   **中心差分 (Central)**：$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$ (精度 $O(h^2)$)

**物理直觉**：
中心差分就像是取前后两个时刻的平均斜率，它比只看一侧（前向/后向）更准确，因为它利用了对称性消除了偶数阶误差项。

### 2.2 步长陷阱：截断误差 vs 舍入误差

**不要盲目减小步长 $h$！**
总误差由两部分组成：
1.  **截断误差 (Truncation Error)**：来自于泰勒展开的忽略项，随 $h$ 减小而减小（例如 $O(h^2)$）。
2.  **舍入误差 (Round-off Error)**：来自于浮点数精度限制（$\epsilon \approx 10^{-16}$），随 $h$ 减小而**增大**（$1/h$ 效应）。

$$ \text{Total Error} \approx C_1 h^2 + \frac{C_2 \epsilon}{h} $$

最优步长通常在 $10^{-5}$ 到 $10^{-8}$ 之间。**物理学家必须找到这个甜蜜点 (Sweet Spot)。**

---

## 3. 数值积分：累积效应

### 3.1 黎曼和与梯形公式

最简单的积分就是把函数下的面积切成矩形（黎曼和）或梯形。
*   **梯形公式 (Trapezoidal)**：用直线连接相邻点。精度 $O(h^2)$。

### 3.2 辛普森公式 (Simpson's Rule)

如果你用**抛物线**（二次多项式）来连接每三个点，奇迹发生了：
$$ \int_a^b f(x) dx \approx \frac{h}{3} [f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + ... + f(x_N)] $$
精度跃升至 $O(h^4)$！这在计算物理中性价比极高。

```python
import numpy as np
from scipy.integrate import simps

x = np.linspace(0, np.pi, 101)
y = np.sin(x)
# 计算 sin(x) 在 [0, pi] 的积分，理论值为 2
area = simps(y, x) 
print(f"Area = {area:.6f}") # 极其精确
```

### 3.3 高斯求积 (Gaussian Quadrature) —— 进阶魔法

如果我们不仅可以自由选择 $y$ 值，还可以自由选择**采样点的位置** $x$ 呢？
通过选取特定的节点（勒让德多项式的根），我们可以用极少的点数获得极高的精度。这对计算量巨大的高维积分（如量子多体问题）至关重要。

---

## 4. 线性代数：解方程组

在量子力学（矩阵对角化）、电磁学（边界元法）中，最终往往归结为解 $Ax = b$。

### 4.1 不要算逆矩阵！(Don't compute the inverse)

计算 $A^{-1}$ 再乘 $b$ 的复杂度是 $O(N^3)$，且数值极不稳定。
**永远使用 `np.linalg.solve(A, b)`**，它通常使用 LU 分解，更快更准。

### 4.2 特殊矩阵的加速：三对角矩阵 (Tridiagonal Matrix)

在求解一维薛定谔方程或热传导方程时，我们会遇到**三对角矩阵**（只有主对角线和旁边两条有非零元素）。
针对这种矩阵的 **Thomas Algorithm (TDMA)** 只需要 $O(N)$ 复杂度！

```python
from scipy.linalg import solve_banded

# 求解 Ax = b，其中 A 是三对角矩阵
# SciPy 需要一种紧凑存储格式 (ab)
ab = np.array([[0, -1, -1],   # 上对角线
               [2,  2,  2],   # 主对角线
               [-1, -1, 0]])  # 下对角线
b = np.array([1, 0, 1])

x = solve_banded((1, 1), ab, b)
```

---

## 5. 本周作业 (GitHub Classroom)

### 作业 1：数值微分的精度测试
**任务**：
1.  计算函数 $f(x) = e^{-x} \sin(x)$ 在 $x=1$ 处的导数。
2.  分别使用前向差分和中心差分。
3.  改变步长 $h$（从 $10^{-1}$ 到 $10^{-16}$），绘制 **误差 vs 步长** 的双对数坐标图 (log-log plot)。
4.  **物理分析**：找到最优步长，并解释为什么误差曲线会先降后升（V字形）。

### 作业 2：量子势阱中的粒子 (离散化求解)
**背景**：一维无限深势阱中的定态薛定谔方程 $-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} = E\psi$。
**任务**：
1.  利用 **中心差分** 将二阶导数离散化，把微分方程转化为矩阵方程 $H\psi = E\psi$。
    $$ -\frac{\psi_{i+1} - 2\psi_i + \psi_{i-1}}{h^2} \approx \frac{d^2\psi}{dx^2} $$
2.  构建哈密顿矩阵 $H$（它是一个三对角矩阵）。
3.  使用 `np.linalg.eigh` 求解本征值 $E$ 和本征函数 $\psi$。
4.  **可视化**：画出前 3 个能级对应的波函数概率密度 $|\psi|^2$。

---

## 6. 常见物理陷阱 (Physics Pitfalls)

1.  **边界条件 (Boundary Conditions)**：在做差分或积分时，端点怎么处理？（Dirichlet vs Neumann）。如果是周期性边界条件，矩阵角的元素需要特殊处理。
2.  **矩阵索引**：物理公式通常从 1 开始 ($x_1, ..., x_N$)，但 Python 从 0 开始 ($x[0], ..., x[N-1]$)。写循环时极其容易 off-by-one。
