# Week 02 Lab: AI Code Review Challenge (Team Project)
## AI 时代的 Python 入门与代码审查

**截止时间**: [填写日期] | **总分**: 100 分 | **形式**: 小组作业 (Max 3人)

### 👥 小组作业领取指南 (Team Setup)

1.  **组队规则**：
    *   本作业为 **小组作业**，每组 **最多 3 人**。
    *   请自行寻找队友，或者在课程群内招募。
    *   **一旦加入小组，不可中途退出或更换小组。**

2.  **创建/加入小组仓库**：
    *   点击 GitHub Classroom 邀请链接（见课程群）。
    *   **组长 (Team Leader)**：
        *   第一个点击链接的人将成为组长。
        *   在 "Create a new team" 中输入小组名称（建议格式：`Team_学号后两位`，例如 `Team_01`）。
        *   创建成功后，将仓库链接发给队友。
    *   **组员 (Team Member)**：
        *   点击链接后，**不要创建新组**！
        *   在列表中找到组长创建的 `Team_XX`，点击 **Join** 加入。

3.  **协作流程**：
    *   使用 Git 进行协作。建议每位成员负责不同的任务（见下文分工建议）。
    *   **严禁直接上传压缩包！** 必须通过 `git push` 提交代码。
    *   在 `Report_Template.md` 中明确记录每个人的分工和贡献。

---

### 🕵️ 实验背景：当 AI 成为猪队友

你是一个科研团队的实习生。你的师兄用 ChatGPT 生成了一段模拟粒子在重力场中运动的代码 `lab1_core/src/bad_particle.py`。
虽然代码能跑通，但模拟结果非常诡异：
*   粒子越跑越快（能量不守恒）。
*   修改一个粒子竟然影响了另一个（幽灵纠缠）。
*   运动轨迹完全不对劲。

你的任务是化身 **Code Reviewer**，找出 AI 代码中的物理与编程陷阱，并重构出正确的代码。

---

### 🎯 任务清单 (Mission List)

#### Part 1: Core Task - 捉鬼特工队 (70分)
> **建议分工**：
> *   成员 A：负责运行 `notebook_review.ipynb`，记录 Bug 现象，并尝试修复“单位混淆”问题。
> *   成员 B：负责修复“浅拷贝灾难”和“列表陷阱”问题。
> *   成员 C：负责重构 `good_particle.py`，实现规范的 `Particle` 类。

1.  **复现 Bug** (`lab1_core/notebook_review.ipynb`)：
    *   运行 notebook，观察并记录 3 个诡异现象。
    *   在报告中截图证明这些 Bug 的存在。
2.  **Code Review** (`lab1_core/src/bad_particle.py`)：
    *   阅读毒药代码，找出以下 3 个陷阱：
        *   **单位混淆**：输入是角度 (degrees)，但 `math.sin` 接收弧度 (radians)。
        *   **浅拷贝灾难**：`p2 = p1` 导致修改 p2 时 p1 也变了。
        *   **列表陷阱**：使用 `math.sin` 处理列表导致报错，或者用低效的 `for` 循环。
3.  **重构代码** (`lab1_core/src/good_particle.py`)：
    *   使用 `numpy` 和正确的 OOP 结构重写 `Particle` 类。
    *   **要求**：使用 `np.array` 存储位置和速度，使用 `np.radians` 转换角度。
4.  **通过自动测试**：
    *   运行 `pytest lab1_core/tests/test_particle.py`。

#### Part 2: Bonus Task - 矢量化狂魔 (30分)
> **建议分工**：全员合作，挑战 Python 性能极限。

1.  **N-Body 模拟** (`lab2_bonus/src/nbody_vectorized.py`)：
    *   生成 100 个随机粒子。
    *   **拒绝循环**：使用 `numpy` 的数组运算（不许用 `for` 循环遍历粒子）计算所有粒子的位置更新。
2.  **性能对决** (`lab2_bonus/tests/test_performance.py`)：
    *   测试你的代码是否比 `math` 循环版本快 **50 倍以上**。

---

### 🛠️ 环境设置
```bash
pip install -r requirements.txt
```

### 📤 提交规范
1.  填写 `Report_Template.md`，务必包含**小组成员分工表**。
2.  确保所有测试通过：
    ```bash
    pytest
    ```
3.  提交代码到 GitHub。
