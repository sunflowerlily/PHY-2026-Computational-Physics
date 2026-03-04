# Assignment Week 01: The Paradigm Shift (当真理遭遇误差)

> **致小组**：欢迎来到计算物理的真实世界。在这里，数学公式是完美的，但计算机是“不诚实”的。你们的任务是联手识破计算机的谎言，并驯服 AI 这个强大的助手。

## 📅 截止日期
*   **Lab 1 Core**: [课堂结束前提交]
*   **Lab 2 Bonus**: [下周上课前提交]

## 🛠️ 环境准备
1.  激活环境：`conda activate phys2026`
2.  安装依赖：`pip install -r requirements.txt`
3.  运行测试：`pytest`

## 👥 小组任务 (Group Roles)
请在 `Report.md` 中认领以下角色，并确保每个人都有 Git Commit 记录：
*   **AI 鉴伪员 (Agent A)**: 负责 Lab 1 Task A (修复 `ai_bad_code.py` 并**证伪 AI 的精度谎言**)。
*   **可视化专家 (Agent B)**: 负责 Lab 1 Task B (在 `notebook_error.ipynb` 中绘制**多方法对比图**)。
*   **算法工程师 (Agent C)**: 负责 Lab 1 Task C (实现 `differentiation.py` 中的**多种差分算法**并通过测试)。

## 🎯 Lab 1: 核心排雷 (70分) - 预计耗时 50-60 分钟
1.  **Task A (AI 鉴伪)**:
    *   运行 `ai_bad_code.py`，修复 IEEE 754 精度崩溃的问题。
    *   **新增挑战**：AI 声称它的算法精度是 $O(h^2)$。请通过数据分析（斜率）证明它是 $O(h)$ 还是 $O(h^2)$，并在代码注释中通过 Commit 驳斥它。
2.  **Task C (算法实现)**:
    *   在 `differentiation.py` 中，不仅要实现 `central_diff`，还要实现 `forward_diff`。
    *   确保所有函数都支持**向量化输入**。
3.  **Task B (可视化对比)**:
    *   在 Notebook 中，**同时**绘制前向差分和中心差分的误差曲线。
    *   画出理论参考线（Slope=1 和 Slope=2），直观展示 $O(h)$ 与 $O(h^2)$ 的区别。
    *   标出两者的“最佳步长”是否相同？

## 🚀 Lab 2: 进阶挑战 (30分) - 预计耗时 30 分钟
*   在 `lab2_bonus` 中实现理查德森外推法 (Richardson Extrapolation)。
*   证明理查德森外推法的精度可以达到 $O(h^4)$ (斜率=4)。
