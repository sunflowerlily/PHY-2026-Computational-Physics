
# 第一周讲义：计算物理新范式 (The New Paradigm)

**授课目标**：
1.  **工具链**：不仅会写代码，还要会管理环境（Environment）和版本（Version）。
2.  **AI 协同**：学会“驾驭”AI，而不是“依赖”AI。让 AI 成为你的结对程序员。
3.  **数值直觉**：理解计算机是“不诚实”的——它总是通过近似来撒谎，我们要学会控制这种谎言（误差）。

---

## 1.1 课程概览与环境搭建：现代物理学家的工作台

### 理论视点：为什么不仅是 Python？
在 2026 年，物理学家不再是在真空中写代码。我们需要**复现性 (Reproducibility)** 和 **协作性 (Collaboration)**。
*   **Anaconda**: 你的“武器库”。它管理库的版本，避免“在我的电脑上能跑，在你的电脑上报错”的尴尬（Dependency Hell）。
*   **Jupyter Lab**: 你的“实验记录本”。它允许代码、公式（LaTeX）、图表和文字叙述共存，是现代科研叙事的标准载体。
*   **Git**: 你的“时光机”。当你把代码改崩了，Git 能帮你回退到昨天那个能运行的版本。

### 实验/实战操作：Hello World of Physics
*   **任务**：建立一个名为 `phys2026` 的虚拟环境。
*   **脚手架指令**：
    ```bash
    # 1. 创建环境 (指定 Python 3.12 以保证库兼容性)
    conda create -n phys2026 python=3.12 numpy scipy matplotlib pandas jupyter

    # 2. 激活环境
    conda activate phys2026

    # 3. 启动 Jupyter Lab
    jupyter lab
    ```
*   **Git 初体验**：
    *   在 GitHub/Gitee 上 Fork 课程仓库。
    *   `git clone [url]` 下载到本地。
    *   修改 `README.md` 添加你的名字，然后 `git commit` 和 `git push`。

---

## 1.2 AI 辅助编程：Prompt Engineering 实战

### 理论视点：AI 是望远镜，不是导航员
AI (如 ChatGPT/Claude) 极其擅长生成样板代码（Boilerplate）和解释错误，但它**不懂物理图像**，且经常产生幻觉。
*   **核心原则**：你必须是那个拥有“物理直觉”的审核者 (Reviewer)。
*   **Prompt 黄金公式**：`Role (角色)` + `Context (背景)` + `Task (任务)` + `Constraints (约束)`。

### 实验/实战操作：与 AI 结对编程
我们将通过一个简单的任务——**“计算并绘制阻尼振荡”**，来对比无效 Prompt 和高效 Prompt。

#### ❌ 无效 Prompt (Bad Prompt)
> "帮我写个 Python 代码画一个振动。"
> *后果：AI 可能会给你一个简单的 sin(x)，没有阻尼，没有物理参数，变量名随意（a, b, c），无法用于科研。*

#### ✅ 高效 Prompt (Good Prompt)
> **Role**: 你是一位精通 Python 和 Matplotlib 的计算物理助教。
> **Context**: 我们正在学习经典力学中的受迫阻尼振动。
> **Task**: 请编写一段 Python 代码，数值求解方程 $m\ddot{x} + b\dot{x} + kx = 0$。
> **Constraints**:
> 1. 使用 `scipy.integrate.odeint` 或 `solve_ivp` 求解。
> 2. 参数设为：m=1.0, k=1.0, b=0.5 (欠阻尼)。
> 3. 绘图要求：画出 x-t 图像，使用科研风格（字体清晰、有图例、坐标轴标签含单位）。
> 4. **重要**：为关键步骤添加中文注释，解释物理意义。

#### 课堂练习：AI 调试 (Debug)
*   **故意制造错误**：给学生一段有 Bug 的代码（例如数组维度不匹配 `ValueError: operands could not be broadcast together`）。
*   **任务**：将报错信息和代码片段喂给 AI，要求 AI 解释原因并修复。
*   **目标**：学会阅读 Traceback，并评估 AI 修复方案的正确性。

---

## 1.3 浮点数体系：计算机的“谎言”

### 理论视点：连续世界的离散化
物理世界通常被认为是连续的（实数域 $\mathbb{R}$），但计算机内存是离散的（有限的比特）。
*   **IEEE 754 标准**：计算机用科学计数法存储数字：$x = (-1)^s \times 1.M \times 2^{E-bias}$。
*   **机器精度 (Machine Epsilon, $\epsilon_{mach}$)**：
    在双精度浮点数（float64）下，$\epsilon \approx 2.22 \times 10^{-16}$。这意味着 $1.0 + \epsilon$ 是计算机能区分的最小变化。如果比这更小，计算机就会认为它没变。

### 核心概念：两种误差的博弈
这是计算物理的**第一课核心心法**：
1.  **截断误差 (Truncation Error)**：源于数学近似（如泰勒展开只取前两项）。步长 $h$ 越小，误差越小。
2.  **舍入误差 (Round-off Error)**：源于计算机存储位数有限。步长 $h$ 越小，计算次数越多，累积的舍入误差越大！

$$ \text{Total Error} \approx \underbrace{C_1 h^p}_{\text{截断}} + \underbrace{\frac{C_2 \epsilon}{h}}_{\text{舍入}} $$

### 实验/实战操作：寻找“最佳步长”
*   **物理问题**：计算函数 $f(x) = \sin(x)$ 在 $x=1$ 处的导数。
*   **数学模型**：向前差分公式 $f'(x) \approx \frac{f(x+h) - f(x)}{h}$。
*   **代码任务**：
    1. 编写一个循环，让步长 $h$ 从 $10^{-1}$ 减小到 $10^{-16}$。
    2. 计算数值导数与真实值 ($\cos(1)$) 的误差。
    3. 使用 `matplotlib` 绘制 **双对数坐标图 (log-log plot)**：x轴为 $h$，y轴为误差。

*   **脚手架代码 (Scaffold Code)**：
```python type=react
import numpy as np
import matplotlib.pyplot as plt

def forward_difference(f, x, h):
    return (f(x + h) - f(x)) / h

# 真实值
x0 = 1.0
true_val = np.cos(x0)

# 生成步长序列：10^-1, 10^-2, ... 10^-16
h_values = 10.0**np.arange(-1, -17, -1)
errors = []

for h in h_values:
    # TODO: 学生填写此处
    # 1. 计算数值导数
    # 2. 计算绝对误差 |numerical - true|
    # 3. 将误差 append 到 errors 列表
    pass 

# 绘图
plt.figure(figsize=(8, 6))
plt.loglog(h_values, errors, 'o-', label='Total Error')
plt.xlabel('Step Size $h$')
plt.ylabel('Absolute Error')
plt.grid(True, which="both", ls="-")
plt.title('The Battle: Truncation vs. Round-off Error')
plt.legend()
plt.show()
```

### 教学深度的点睛之笔 (The "Aha!" Moment)
当学生运行上述代码时，他们会看到一个漂亮的 **"V" 字形曲线**。
*   **右侧下降段**：随着 $h$ 减小，数学近似越来越准（截断误差主导）。
*   **谷底**：这是**最佳步长**，通常在 $h \approx \sqrt{\epsilon} \approx 10^{-8}$ 附近。
*   **左侧上升段**：随着 $h$ 继续减小，分子 $f(x+h) - f(x)$ 变成了两个极接近数字的相减，有效数字大量丢失（**灾难性抵消 Catastrophic Cancellation**），误差反而暴涨！

**结论**：在计算物理中，**“更精确”并不意味着“步长越小越好”**。我们需要在数学理论和机器限制之间寻找平衡。

---

## 课后作业 (Homework)
1.  **AI 练手**：使用 AI 生成一段代码，计算 $e^x$ 的泰勒展开，并要求 AI 解释为什么当 x 很大且为负数时（如 $e^{-20}$），直接用泰勒展开计算会出现巨大误差？
2.  **思考题**：在 Python 中输入 `0.1 + 0.2 == 0.3`，结果是 `False`。请查阅资料解释原因，并给出在科学计算中比较两个浮点数是否相等的正确写法（提示：`np.isclose`）。