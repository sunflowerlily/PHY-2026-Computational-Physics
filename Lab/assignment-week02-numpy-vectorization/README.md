# Week 02 Lab: The "No Loops" Challenge
## Numpy Vectorization & Scientific Visualization

**截止时间**: [填写日期] | **总分**: 100 分

### 🌌 物理背景：从粒子到场论
在经典力学中，我们习惯追踪单个粒子 $i$ 的轨迹 $\vec{r}_i(t)$。但在计算物理的前沿（如宇宙学N体模拟、流体力学），我们处理的是弥散在整个空间中的**场 (Field)**。

当我们计算引力势：
$$ V(\vec{r}) = \sum_{i=1}^N \frac{-G m_i}{|\vec{r} - \vec{R}_i|} $$
如果我们将空间离散化为 $1000 \times 1000$ 的网格，且有 $N=100$ 个星体，那么总计算量是 $10^8$ 次相互作用。使用 Python 的 `for` 循环处理这种规模的计算是灾难性的。

本周，你的任务是学会**拒绝循环**，掌握 Numpy 的 **Broadcasting (广播)** 机制，将计算速度提升 50 倍以上。

---

### 🎯 任务清单 (Mission List)

#### Part 1: Core Task - 拯救被循环卡死的飞船 (70分)
> **场景**：你的飞船导航计算机被一段 AI 生成的低效代码卡死了，导致无法实时计算引力场以规避黑洞。你需要重构代码。

1.  **运行毒药代码** (`lab1_core/src/gravity_slow.py`)：
    *   运行它，记录计算一张 $200 \times 200$ 网格的势能图需要多少秒。
    *   阅读代码，找出其中的“性能杀手”（双重甚至三重循环）。
2.  **向量化重构** (`lab1_core/src/gravity_fast.py`)：
    *   使用 Numpy 的 Broadcasting 技巧（`[:, None]` 或 `reshape`）消除所有 Python 循环。
    *   **要求**：代码中不得出现任何 `for` 或 `while`。
3.  **通过自动测试**：
    *   运行 `pytest lab1_core/tests/test_performance.py`。
    *   你的代码必须比慢速版本快 **至少 50 倍**，且物理结果误差 $< 10^{-7}$。
4.  **可视化** (`lab1_core/notebook_core.ipynb`)：
    *   绘制引力势能的等高线图 (Contourf)，并正确设置 `aspect='equal'`。

#### Part 2: Bonus Task - 穿越时空的光谱 (30分)
> **场景**：你接收到了一个遥远星系（红移 $z=0.1$）的光谱信号。为了分析其化学成分，你需要将其波长“拉回”到静止参考系。

1.  **数据读取**：从 `lab2_bonus/data/galaxy_spectrum.txt` 读取波长和流量。
2.  **插值修复** (`lab2_bonus/src/spectrum_fix.py`)：
    *   分别实现 **线性插值 (Linear)** 和 **三次样条插值 (Cubic Spline)**。
    *   将红移后的光谱重采样回静止系的波长网格。
3.  **对比分析** (`lab2_bonus/notebook_bonus.ipynb`)：
    *   绘图对比两种插值方法。
    *   解释为什么线性插值会“削平”发射线峰值，导致物理信息丢失。

---

### 🛠️ 环境设置
```bash
pip install -r requirements.txt
```

### 📤 提交规范
1. 填写 `Report_Template.md`，特别是记录你与 AI 的交互过程（Prompt Engineering）。
2. 确保所有测试通过：
   ```bash
   pytest
   ```
3. 提交代码到 GitHub。
