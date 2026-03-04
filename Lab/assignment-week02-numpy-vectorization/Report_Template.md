# Week 02 Lab Report: Numpy Vectorization

**Name**: [你的名字]
**Student ID**: [你的学号]

---

## Part 1: Core Task - The Loop vs. Vectorization

### 1. 性能对比
请记录在 $200 \times 200$ 网格（或更大规模）下的运行时间：

| 方法 | 耗时 (秒) | 备注 |
| :--- | :--- | :--- |
| **Python Loops (Slow)** | `0.00` | (在此处填写) |
| **Numpy Vectorized (Fast)** | `0.00` | (在此处填写) |
| **Speedup (加速比)** | `0.0` x | Slow / Fast |

### 2. AI 交互记录 (Mandatory)
> **教学目标**：学会如何向 AI 提问以解决具体的 Broadcasting 维度报错问题。

*   **我遇到的报错/问题**:
    *   *示例：ValueError: operands could not be broadcast together with shapes (200,200) (20,)*
    *   [请填写你实际遇到的问题]

*   **我的 Prompt (提问指令)**:
    *   ```text
        [请粘贴你发给 AI 的原始 Prompt]
        ```

*   **AI 的建议与我的理解**:
    *   [AI 建议了什么？为什么要增加 `np.newaxis`？请用自己的话解释 Broadcasting 的物理意义（张量积）]

---

## Part 2: Bonus Task - Spectrum Interpolation

### 1. 线性插值 vs. 三次样条
请截图 `notebook_bonus.ipynb` 中的对比图，并粘贴在下方：

![Interpolation Comparison](在此处粘贴图片链接或直接拖入图片)

### 2. 物理分析
*   **线性插值 (Linear)** 的主要缺陷是什么？在处理尖锐的发射线（如 H-alpha 线）时会发生什么？
    *   [你的回答]

*   **三次样条 (Cubic Spline)** 为什么能更好地保留物理特征？它遵循什么物理原理（最小化什么能量）？
    *   [你的回答]
