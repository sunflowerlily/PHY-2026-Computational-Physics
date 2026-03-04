# 第 1 周：计算物理新范式 (The New Paradigm)

> **本周名言**："Computers are incredibly fast, accurate, and stupid. Human beings are incredibly slow, inaccurate, and brilliant. Together they are powerful beyond imagination." —— Albert Einstein (Apocryphal)

## 1. 核心目标 (Learning Objectives)
*   **物理认知**：理解计算物理作为“第三支柱”的地位，以及浮点数误差（截断 vs 舍入）的物理本质。
*   **数值技巧**：搭建 Anaconda + Git + Trae IDE 的现代化工作流，掌握 Python 环境管理。
*   **AI 协同**：学会使用 Prompt Engineering 让 AI 成为你的“结对程序员”，而不是“代写作业的枪手”。

## 2. 物理翻译与数值基石 (Physics & Numerical Foundations)

### 2.1 第三支柱：从真空球形鸡到真实世界
在过去，物理学只有两条腿：
*   **理论**：推导完美的解析解（如二体问题），但无法处理复杂系统。
*   **实验**：观测真实世界，但成本高昂且受限于设备。

**计算物理**是第三条腿。它让我们能够：
*   模拟**无法实验**的场景（如黑洞合并、宇宙演化）。
*   求解**无法解析**的方程（如三体问题、湍流）。

### 2.2 计算机的谎言：浮点数与误差博弈
计算机是离散的，而物理世界（通常）是连续的。当我们把连续的实数塞进有限的内存时，必须付出代价——**误差**。

*   **IEEE 754 标准**：计算机用科学计数法存储数字。
    $$ x = (-1)^s \times 1.M \times 2^{E-bias} $$
    这意味着计算机存在一个**最小分辨率**，称为机器精度 $\epsilon_{mach} \approx 2.22 \times 10^{-16}$ (对于 float64)。

*   **误差的博弈**：
    当我们计算导数 $f'(x) \approx \frac{f(x+h)-f(x)}{h}$ 时，存在两股对抗的力量：
    1.  **截断误差 (Truncation Error)**：源于数学近似（泰勒展开）。步长 $h$ 越小，误差越小 ($O(h)$)。
    2.  **舍入误差 (Round-off Error)**：源于计算机精度。步长 $h$ 越小，分母越小，分子中两个相近数相减（**灾难性抵消**），误差反而暴涨 ($O(\epsilon/h)$)。

    **物理直觉**：这就像用尺子量东西。刻度太稀（h太大）测不准；刻度太密（h太小）眼睛看花了也测不准。必须找到一个**最佳步长 (Sweet Spot)**。

## 3. AI 协同与 Code Review 靶场 (AI Synergy & Code Review)

### 【AI 的天真解法】
当你问 AI：“帮我写个代码计算 sin(x) 的导数”，它可能会给你这样的代码：

```python
def derivative(f, x, h=1e-10):
    return (f(x+h) - f(x)) / h
```

### 【物理与性能破绽分析】
1.  **步长陷阱**：AI 默认的 `1e-10` 并不一定是最佳的。对于中心差分，最佳步长通常是 $10^{-5}$ 左右；对于前向差分，是 $10^{-8}$。
2.  **精度灾难**：如果用户传入 `h=1e-16`，AI 的代码会因为舍入误差输出完全错误的结果（甚至为 0），而 AI 不会警告你。

### 【Prompt 重构】
你需要像物理学家一样向 AI 提问：
> "请编写一个 Python 函数计算数值导数。**要求**：
> 1. 演示截断误差与舍入误差的权衡。
> 2. 生成从 $10^{-1}$ 到 $10^{-16}$ 的步长列表。
> 3. 绘制双对数坐标图 (Log-Log Plot)，展示总误差的 V 字形曲线。"

## 4. 可视化与物理洞察 (Visualization & Insights)

本周我们将绘制第一张具有物理深度的图表：**误差的 V 字形曲线**。

```python
import numpy as np
import matplotlib.pyplot as plt

# ... 计算代码 ...

plt.loglog(h_values, errors, 'o-', label='Total Error')
plt.xlabel('Step Size $h$')
plt.ylabel('Absolute Error')
plt.title('The Battle: Truncation vs. Round-off')
plt.grid(True, which="both", ls="-")
```

**物理洞察**：
*   曲线右侧斜率代表算法的**收敛阶**（Order of Accuracy）。
*   曲线谷底代表**最佳工作区**。
*   曲线左侧的混乱代表**量子涨落般的数值噪声**。

## 5. 本周作业 (GitHub Classroom)

### 作业 1：环境搭建与 Hello World
*   **任务**：安装 Anaconda，配置 Trae IDE，Fork 课程仓库。
*   **提交**：修改仓库中的 `README.md`，签上你的名字并 Push。

### 作业 2：当真理遭遇误差 (The Paradigm Shift)
*   **场景**：你是一个数值实验员，需要为一个精密仪器寻找最佳采样频率（步长）。
*   **任务**：
    1.  运行 `lab1_core/src/ai_bad_code.py`，目睹精度崩溃的现场。
    2.  修复代码，绘制出完美的 V 字形误差曲线。
    3.  **Bonus**：尝试使用 `float32` 重复实验，观察“谷底”如何移动（亲身体验单精度的脆弱性）。

## 6. 常见物理陷阱 (Physics Pitfalls)
1.  **盲信 AI**：AI 生成的代码能跑，不代表物理上是对的。它经常搞错单位、边界条件或物理常数。
2.  **过度追求精度**：在数值计算中，**不是步长越小越好**。贪婪地减小步长，往往会掉进舍入误差的深渊。
3.  **环境地狱**：不要在系统自带的 Python 里装库。请务必使用 Conda 虚拟环境 (`conda create -n phys2026`)，否则你的电脑很快会变成一团乱麻。
