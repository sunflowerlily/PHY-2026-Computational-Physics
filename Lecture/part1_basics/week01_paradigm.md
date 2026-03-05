# 第 1 周：计算物理新范式 (The New Paradigm)


# 一 计算物理环境搭建

> **学习目标：** 设置一套完整的"计算物理工作站"——能用 Python 写代码、用 Git 管理版本、用 Trae IDE 与 AI 协同编程。

***

## 1.1 为什么选 Python？

在2026年的科学计算生态中，Python 已成为天文学与物理模拟的**事实标准语言**。以下是我们选择它的核心理由：

| 维度 | Python 的优势 |
|------|-------------|
| **生态** | NumPy、SciPy、Matplotlib、Astropy 构成完整物理计算栈 |
| **AI协同** | 所有主流 AI 编程助手（Trae、Copilot、Cursor）对 Python 支持最好 |
| **社区** | arXiv 上天文/物理方向的开源代码 90% 以上为 Python |
| **可读性** | 代码接近数学伪代码，利于"物理建模思维"的表达 |
| **学习曲线** | 入门快，可快速聚焦在**物理问题**本身，而非语言细节 |

> 💡 **2026年的新范式**：我们不再从零手写底层算法，而是借助 AI 生成代码骨架，再用物理直觉去**审查、纠错和优化**。Python 是与 AI 对话的最佳语言。

***

## 1.2 安装 Python（推荐 Miniforge）

### 1.2.1 为什么用 Miniforge，不直接装 Python？

直接安装 Python 会遇到**包冲突、环境混乱**等经典问题。我们推荐 **Miniforge**——它是轻量级的 conda 环境管理器，社区驱动、免费无商业限制（Anaconda 公司的 Miniconda 在2025年调整了许可证，对大学课堂使用有限制）。 [fabriziomusacchio](https://www.fabriziomusacchio.com/teaching/minimal_python_installation/)

### 1.2.2 安装步骤（三大平台通用）

**第一步：下载 Miniforge**

前往官网：[https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge)

| 操作系统 | 选择安装包 |
|---------|----------|
| Windows 10/11 | `Miniforge3-Windows-x86_64.exe` |
| macOS (Apple Silicon) | `Miniforge3-MacOSX-arm64.sh` |
| macOS (Intel) | `Miniforge3-MacOSX-x86_64.sh` |
| Linux | `Miniforge3-Linux-x86_64.sh` |

**第二步：安装**
- Windows：双击 `.exe`，全程默认，**勾选"Add to PATH"**
- macOS/Linux：终端执行：
```bash
bash Miniforge3-Linux-x86_64.sh
# 按 Enter / yes 确认所有选项
source ~/.bashrc  # 或 source ~/.zshrc
```

**第三步：验证安装**
```bash
conda --version   # 应显示 conda 24.x.x 或更高
python --version  # 应显示 Python 3.11.x 或更高
```

### 2.3 创建计算物理专用虚拟环境

> **为什么要创建虚拟环境？** 不同课程/项目的包版本可能冲突。用虚拟环境把它们隔离开，就像给每个实验配一套专属仪器。

```bash
# 创建名为 compphys 的环境，指定 Python 版本
conda create -n compphys python=3.11

# 激活环境
conda activate compphys

# 安装计算物理核心包
conda install numpy scipy matplotlib jupyter ipython
pip install astropy sympy tqdm

# 验证：启动 Jupyter
jupyter notebook
```

> ✅ **课堂约定**：本课程所有作业均在 `compphys` 环境下运行。提交代码前，务必在此环境中测试通过。

***

## 1.3 Git 与 GitHub——科学计算的时光机

### 1.3.1 Git 是什么？

Git 是**版本控制系统**。对计算物理学生来说，它的意义是：

- 每次模拟修改，都有完整记录，随时可以"后悔"
- 与同学协作，不再靠"最终版\_v3\_真的最终版.py"
- 将代码公开到 GitHub，这是你学术生涯的**第一份科研档案**

### 1.3.2 安装 Git

**Windows：** 下载 [https://git-scm.com/downloads](https://git-scm.com/downloads)，安装时选择 "Git from the command line and also from 3rd-party software" 。 [youtube](https://www.youtube.com/watch?v=CFCh6Y-reiI)

**macOS：** 终端运行：
```bash
xcode-select --install
```

**Linux（Ubuntu/Debian）：**
```bash
sudo apt install git
```

**验证：**
```bash
git --version  # 应显示 git version 2.4x.x
```

### 1.3.3 配置 Git（首次必做）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@yunnan.edu.cn"
git config --global core.editor "code"   # 设置默认编辑器(可选)
```

### 1.3.4 注册 GitHub 并创建第一个仓库

1. 前往 [https://github.com](https://github.com) 注册账号（用学校邮箱可申请 **GitHub Student Developer Pack**，免费获得大量工具）
2. 点击右上角 "+" → "New repository"
3. 仓库名建议：`compphys-2026`，选 **Public**，勾选 "Add README file"
4. 将仓库克隆到本地 ： [product.hubspot](https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners)

```bash
git clone https://github.com/你的用户名/compphys-2026.git
cd compphys-2026
```

### 3.5 Git 核心工作流（四步循环）

```
编写/修改代码  →  git add  →  git commit  →  git push
```

```bash
# 查看当前状态
git status

# 将修改加入暂存区
git add simulation.py

# 提交，附上有意义的说明
git commit -m "feat: 完成双星系统初始条件设置"

# 推送到 GitHub
git push origin main
```

> 💡 **好的 commit message 示例：**
> - ✅ `fix: 修正龙格-库塔步长导致的能量漂移`
> - ❌ `update` / `修改了一些东西`

***

## 1.4 Trae IDE——你的 AI 编程搭档

### 1.4.1 Trae 是什么？

Trae 是字节跳动推出的**AI原生集成开发环境（IDE）**，基于 VS Code 架构，内置 Claude 4 Sonnet、Gemini 2.5 Pro 等顶级大模型 。在 SWE-bench Verified 基准测试中，Trae 的 AI 编程能力于2025年7月登顶排行榜 。 [datacamp](https://www.datacamp.com/tutorial/trae-ai)

对计算物理课程而言，Trae 的价值在于：
- **Builder 模式**：用自然语言描述物理问题，AI 生成代码框架
- **内联解释**：选中任何代码片段，立即获得物理意义解释
- **错误修复**：AI 直接定位数值发散、维度错误等物理计算常见bug
- **MCP 支持**：可连接天文数据库、计算工具等外部资源 [datacamp](https://www.datacamp.com/tutorial/trae-ai)

### 1.4.2 安装 Trae

1. 前往官网 [https://www.trae.ai](https://www.trae.ai) 下载对应平台安装包 [trae](https://www.trae.ai)
2. 运行安装程序（支持 macOS 和 Windows 10/11） [skywork](https://skywork.ai/blog/trae-ai-ide-review-2025-features-pricing-privacy-comparison/)
3. 启动后，可一键导入你的 VS Code 设置、扩展和快捷键

```
安装完成后，在终端添加 trae 命令（可选）：
Command Palette → "Install 'trae' command in PATH"
```

### 1.4.3 在 Trae 中配置 Python 环境

1. 打开你的项目文件夹：`File → Open Folder → compphys-2026`
2. 右下角点击 Python 解释器选择器 → 选择 `compphys` 虚拟环境
3. 打开终端（`Ctrl+~`），确认：
```bash
which python  # 应指向 miniforge3/envs/compphys/bin/python
```

### 1.4.4 Trae 的 AI 协同编程模式（核心概念）

在本课程中，我们用 Trae 的方式**不是让 AI 替你写作业**，而是：

```
你的角色：物理建模者 + 代码审查员 + 结果解释者
AI的角色：代码实现助手 + 语法工具箱
```

**典型工作流示例：**

```
1. [你]  在 Trae Builder 中输入：
   "用四阶 Runge-Kutta 方法求解双星系统运动方程，
    质量 m1=1, m2=0.5（太阳质量单位），
    初始间距 1 AU"

2. [AI]  生成完整 Python 代码

3. [你]  检查：
   - 引力常数 G 的单位是否正确？
   - 总能量是否守恒（误差 < 0.01%）？
   - 轨道是否闭合？

4. [你]  发现问题 → 用 AI 辅助修正 → 物理解释
```

> ⚠️ **课程警告**：直接提交 AI 生成的未经审查代码，等同于提交一份"可能完全错误"的物理实验报告。**物理直觉 + AI工具 = 生产力；AI 工具 - 物理直觉 = 风险。**

### 1.4.5 推荐安装的 Trae 扩展

在 Trae 的扩展市场中搜索并安装：

| 扩展名 | 用途 |
|--------|------|
| **Python** (Microsoft) | Python 语法高亮、调试 |
| **Jupyter** | 在 IDE 中直接运行 `.ipynb` |
| **GitLens** | 可视化 Git 历史，代码追溯 |
| **LaTeX Workshop** | 撰写物理报告时的公式渲染 |

***

## 1.5 环境验证：第一个计算物理小程序

完成以上安装后，在 Trae 中新建文件 `test_env.py`，运行以下代码验证整个环境：

```python
import numpy as np
import scipy
import matplotlib.pyplot as plt
import astropy
print("=" * 40)
print(f"✅ NumPy    版本: {np.__version__}")
print(f"✅ SciPy    版本: {scipy.__version__}")
print(f"✅ Astropy  版本: {astropy.__version__}")
print("=" * 40)

# 小测试：计算开普勒轨道周期
G = 6.674e-11      # SI单位
M_sun = 1.989e30   # kg
AU = 1.496e11      # m

a = 1.0 * AU       # 地球轨道半长轴
T = 2 * np.pi * np.sqrt(a**3 / (G * M_sun))
print(f"🌍 地球公转周期（计算值）: {T/3600/24:.2f} 天")
print(f"🌍 地球公转周期（真实值）: 365.25 天")
```

**预期输出：**
```
========================================
✅ NumPy    版本: 2.x.x
✅ SciPy    版本: 1.x.x
✅ Astropy  版本: 7.x.x
========================================
🌍 地球公转周期（计算值）: 365.25 天
🌍 地球公转周期（真实值）: 365.25 天
```

***

## 1.6 本节小结与下课任务

### ✅ 本讲完成清单

- [ ] Miniforge 安装完毕，`compphys` 虚拟环境创建成功
- [ ] Git 安装并配置姓名与邮箱
- [ ] GitHub 账号注册，`compphys-2026` 仓库创建并克隆到本地
- [ ] Trae IDE 安装完毕，Python 环境联通
- [ ] `test_env.py` 运行成功，周期计算结果正确

### 📝 课后作业（提交到 GitHub）

1. 将 `test_env.py` 的运行截图作为 `README.md` 的图片，`git push` 到你的 `compphys-2026` 仓库
2. **AI探索题**：在 Trae Builder 中输入"用 Python 画出太阳系八大行星的开普勒轨道"，观察 AI 生成的代码，写下你认为**物理上有问题**的地方（如果有的话）

***

# 二、 AI 辅助编程：Prompt Engineering 实战

> **核心理念**：Prompt 不是"搜索关键词"，而是你与 AI 协作的**合同说明书**。写得越精准，AI 交付的代码越接近物理真实。

***

## 2.1 什么是 Prompt Engineering？

**Prompt Engineering（提示词工程）** 是指通过精心设计输入给 AI 的文字指令，来引导模型输出高质量、符合需求的结果 。在计算物理的语境下，它是你与 Trae / ChatGPT / Claude 等 AI 工具沟通的**技术语言**。 [github](https://github.com/dair-ai/Prompt-Engineering-Guide)

一个朴素的事实：

> 同一个物理问题，**模糊的 Prompt** 得到的是能跑但不可信的代码；**精准的 Prompt** 得到的是可以直接审查、修改的物理代码骨架。

| Prompt 质量 | 典型输入 | AI 输出 |
|------------|---------|---------|
| ❌ 差 | "写一个模拟行星运动的代码" | 无单位、无注释、边界条件不明 |
| ⚠️ 中 | "用 Python 模拟地球绕太阳的轨道" | 能跑，但 G 可能用错单位制 |
| ✅ 好 | 见下文"黄金模板" | 有单位、有守恒量验证、有可视化 |

***

## 2.2 计算物理 Prompt 的黄金模板

好的物理 Prompt 必须包含五个要素，可以用缩写 **RUOVC** 记忆 ： [github](https://github.com/zaops/prompt-engineering)

```
R - Role（角色）：告诉 AI 它是谁
U - Units（单位制）：明确物理量的单位
O - Output（输出格式）：指定代码结构或图表类型
V - Validation（验证条件）：告诉 AI 如何检验物理正确性
C - Constraint（约束/限制）：禁止使用的方法、依赖包限制等
```

**黄金模板示例（双星系统）：**

```
【R】你是一位精通天体力学的计算物理专家，擅长用 Python 做数值模拟。

【U】使用 SI 单位制：质量单位 kg，长度单位 m，时间单位 s。
    引力常数 G = 6.674e-11 N·m²/kg²。

【O】请编写 Python 代码，用四阶 Runge-Kutta 方法求解以下问题：
    - 质量 m1 = 1.989e30 kg (太阳质量)，m2 = 5.972e24 kg (地球质量)
    - 初始地球位置 (1.496e11, 0) m，初始速度 (0, 2.978e4) m/s
    - 太阳固定在原点
    - 模拟时长 = 1 个地球年（365.25 * 24 * 3600 s）
    - 代码结构：1) 参数定义区 2) RK4 函数 3) 主循环 4) 可视化

【V】代码中必须包含对总机械能 E = 动能 + 势能 的计算，
    并在最后打印"能量守恒误差 = (E_end - E_start) / |E_start| * 100%"，
    预期误差应小于 0.01%。

【C】不使用 scipy.integrate，仅用 numpy 实现 RK4；
    matplotlib 绘图，图中标注初始位置和轨道方向。
```

> 💡 **为什么要写【V】验证条件？** 因为 AI 生成的代码可能在语法上完全正确，但因为符号错误（如引力写成了斥力）或步长过大，导致轨道发散。**验证条件是你作为物理学家的把关防线。**


## 2.3 从零到运行：样板代码生成实战

### 2.3.1 场景一：生成物理模拟骨架

以下是在 **Trae Builder** 中输入上述黄金模板后，AI 生成的代码骨架（经过审查的版本）：

```python
# ============================================================
# 双星系统（地球-太阳）四阶 Runge-Kutta 模拟
# AI 生成 + 人工物理审查版 v1.0
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 参数定义区 ---
G  = 6.674e-11        # 引力常数 [N·m²/kg²]
M  = 1.989e30         # 太阳质量 [kg]
m  = 5.972e24         # 地球质量 [kg]
AU = 1.496e11         # 天文单位 [m]
yr = 365.25 * 86400   # 1年 [s]

x0  = np.array([AU, 0.0])        # 初始位置 [m]
v0  = np.array([0.0, 2.978e4])   # 初始速度 [m/s]
dt  = 3600.0                     # 步长：1小时
N   = int(yr / dt)               # 总步数

# --- 2. 导数函数（状态向量 = [x, y, vx, vy]）---
def derivatives(state):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    ax = -G * M * x / r**3      # ⚠️ 审查点：符号为负（引力指向原点）
    ay = -G * M * y / r**3
    return np.array([vx, vy, ax, ay])

# --- 3. 四阶 Runge-Kutta 步进 ---
def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# --- 4. 主循环 ---
state = np.array([x0[0], x0 [github](https://github.com/dair-ai/Prompt-Engineering-Guide), v0[0], v0 [github](https://github.com/dair-ai/Prompt-Engineering-Guide)])
positions = [state[:2].copy()]
energies  = []

def total_energy(state):
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    KE = 0.5 * m * (vx**2 + vy**2)
    PE = -G * M * m / r
    return KE + PE

E0 = total_energy(state)

for _ in range(N):
    state = rk4_step(state, dt)
    positions.append(state[:2].copy())
    energies.append(total_energy(state))

# --- 5. 验证守恒量 ---
E_end = energies[-1]
error = abs((E_end - E0) / E0) * 100
print(f"能量守恒误差 = {error:.6f}%")   # 预期 < 0.01%

# --- 6. 可视化 ---
positions = np.array(positions)
plt.figure(figsize=(6, 6))
plt.plot(positions[:, 0]/AU, positions[:, 1]/AU, 'b-', lw=0.8, label='地球轨道')
plt.plot(0, 0, 'yo', ms=12, label='太阳')
plt.plot(positions[0, 0]/AU, positions[0, 1]/AU, 'gs', ms=8, label='起点')
plt.xlabel('x [AU]'); plt.ylabel('y [AU]')
plt.title('地球公转轨道（RK4，步长=1小时）')
plt.legend(); plt.axis('equal'); plt.tight_layout()
plt.savefig('orbit.png', dpi=150)
plt.show()
```

### 2.3.2 📋 代码审查清单（必须人工检查）

拿到 AI 生成的代码后，**不能直接运行提交**，按以下清单逐项检查：

- [ ] **符号检查**：引力加速度 `ax` 是否指向引力中心（符号为负）？
- [ ] **单位一致性**：所有物理量是否在同一单位制下？有无混用 AU 和 m？
- [ ] **初始条件**：地球速度大小是否约为 29.78 km/s？量级是否正确？
- [ ] **守恒量验证**：能量误差是否 < 0.01%？角动量是否守恒？
- [ ] **步长合理性**：步长与轨道周期相比是否足够小？（建议 < 周期的 1/1000）
- [ ] **边界处理**：是否有 `r → 0` 导致奇点的潜在风险？

***

## 2.4 让 AI 解释报错——报错驱动的学习法

计算物理中的报错分为两类：**Python 语法错误**和**物理错误**。AI 擅长解释前者，但**物理错误需要你自己发现**。

### 2.4.1 解释语法报错的 Prompt 模板

遇到报错时，不要只粘贴错误信息，要附上**上下文代码片段**：

```
我在运行以下计算物理代码时遇到了错误：

【报错信息】
ValueError: operands could not be broadcast together with shapes (4,) (2,)

【相关代码片段】
def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)   # ← 错误在这行
    ...

【我的理解】
state 是 4 维向量，k1 应该也是 4 维，但不确定哪里维度不匹配。

请帮我：
1. 解释这个报错的根本原因
2. 指出代码中哪一行引发了维度不匹配
3. 提供修正方案，并解释为什么这样修正
```

> ✅ **优质报错 Prompt 的三要素**：错误信息 + 代码片段 + 你自己的初步判断。附上"我的理解"能让 AI 给出更精准的解释，而不是泛泛而谈 。 [digitalocean](https://www.digitalocean.com/resources/articles/prompt-engineering-best-practices)

### 2.4.2 常见报错类型与 AI 解释策略

| 报错类型 | 典型报错信息 | 最优 Prompt 策略 |
|---------|------------|----------------|
| **维度错误** | `ValueError: shape mismatch` | 粘贴数组定义 + shape 打印结果 |
| **数值发散** | 轨道飞出屏幕，能量误差 > 100% | 描述"物理现象" + 贴出步长和初始值 |
| **模块缺失** | `ModuleNotFoundError` | 直接问，AI 会给 pip/conda 安装命令 |
| **类型错误** | `TypeError: unsupported operand` | 贴出变量类型（`type(x)` 的输出） |
| **索引越界** | `IndexError: index out of range` | 贴出数组形状和循环范围 |

### 2.4.3 场景示例：数值发散报错

假设你的行星轨道模拟跑了几步后坐标变成 `nan` 或 `1e+300`：

```
我的 RK4 轨道模拟在运行约 100 步后数值发散，
轨道坐标变为 nan。

【现象】
- 前 10 步位置正常，第 87 步出现 r ≈ 0
- 打印的能量从 -3.5e33 突然变成 nan

【代码关键部分】
r = np.sqrt(x**2 + y**2)
ax = -G * M * x / r**3   # 当 r→0 时会发散

【问题】
请帮我：
1. 解释数值发散的物理根源（不只是代码原因）
2. 提供防止奇点碰撞的常见数值方法（如软化参数 softening length）
3. 给出加入 softening length 后的修改代码
```

**AI 将给出类似以下的解答要点：**
- 物理根源：两体距离 → 0 时，引力 → ∞，这是**多体模拟的经典奇点问题**
- 数值方法：引入软化长度 $ r_{\text{soft}} = \sqrt{r^2 + \epsilon^2} $，其中 $ \epsilon $ 通常取粒子间典型距离的 1–5%
- 修正代码：`r_soft = np.sqrt(x**2 + y**2 + epsilon**2)`

> 🔑 **学习提示**：软化长度是 N 体模拟（如星系动力学、星团演化）的核心概念。让 AI 解释报错，顺带学到了真实科研中的技巧——这才是 AI 辅助学习的正确打开方式。

***

## 2.5 进阶技巧：让 AI 生成更好代码的五种策略

### 策略 1：角色设定（Role Prompting）

```
"你是一位发表过 N 体模拟论文的计算天体物理学家，
 请用符合 AstroPy 社区规范的风格编写以下代码..."
```

给 AI 设定专业角色，能显著提升代码的专业程度和注释质量 。 [github](https://github.com/zaops/prompt-engineering)

### 策略 2：少样本示例（Few-Shot）

```
"参考以下我已有的代码风格（样例），
 用同样的结构为薛定谔方程生成有限差分求解器..."
```

粘贴你写好的一段代码，让 AI 模仿风格续写 。 [xlearnonline](https://xlearnonline.com/programming/prompt-engineering-for-python/)

### 策略 3：链式思维（Chain-of-Thought）

```
"在写代码之前，先用中文逐步推导以下物理问题的数学公式，
 确认推导正确后，再将公式转化为 Python 代码..."
```

强迫 AI 先推导公式再写代码，能大幅减少物理错误 。 [github](https://github.com/dair-ai/Prompt-Engineering-Guide)

### 策略 4：迭代精化（Iterative Refinement）

不要期望一次 Prompt 就得到完美代码。标准流程是 ： [dev](https://dev.to/fonyuygita/the-complete-guide-to-prompt-engineering-in-2025-master-the-art-of-ai-communication-4n30)

```
第 1 轮：生成骨架 → 审查物理逻辑
第 2 轮："请在上述代码中加入角动量守恒验证，并绘制 L(t) 图"
第 3 轮："能量误差达到了 0.05%，请分析是步长问题还是算法精度问题"
```

### 策略 5：主动要求解释（Explain Mode）

```
"请在每个关键步骤后，用注释解释：
 ① 这行代码对应的物理意义是什么？
 ② 如果这里写错了，会产生什么物理上可观测的错误？"
```

这种 Prompt 生成的代码兼具**可读性**和**物理教育价值** 。 [arxiv](https://arxiv.org/html/2412.07482v1)

***

## 2.6 反面教材：这些 Prompt 会害了你

以下是计算物理课程中**高危反模式**，请务必避免：

```python
# ❌ 危险 Prompt 1：过于模糊
"帮我写一个物理模拟"

# ❌ 危险 Prompt 2：不验证结果
"帮我写完整的双星模拟代码，直接能运行的那种"
# → AI 生成的代码可能能运行但物理完全错误

# ❌ 危险 Prompt 3：跳过理解直接要答案
"这道题怎么做，给我完整代码"
# → 你失去了最宝贵的建模训练机会

# ❌ 危险 Prompt 4：盲目信任 AI 的数字
"G = 6.67e-8？好的我就用这个值"
# → 这是 CGS 单位的 G，SI 单位应为 6.674e-11！
```

> ⚠️ **课程规则**：所有提交的代码报告，必须包含一段"**AI 使用说明**"，写明哪些部分由 AI 生成、哪些经过了人工修改，以及你如何验证了物理正确性。这不是惩罚，而是科学诚信的训练。

***

## 2.7 本小节实验任务

> 在 Trae IDE 中完成以下练习，并将对话截图和最终代码 push 到 GitHub。

**【任务 A】样板代码生成**
使用本节的黄金模板，为以下物理问题生成代码，并完成代码审查清单：
- 简谐振子（弹簧质量系统）的 RK4 模拟，验证总能量守恒

**【任务 B】报错解读**
故意将上述代码中的步长改为 `dt = 86400 * 100`（100天/步），观察轨道发散现象，用本节的报错 Prompt 模板询问 AI，整理 AI 的回答并写出你自己的物理解释。

**【任务 C】Chain-of-Thought 实践**
用策略 3（链式思维 Prompt）要求 AI 先推导**开普勒第三定律** $ T^2 \propto a^3 $ 的数值验证方案，再生成代码，与任务 A 的结果对比周期计算误差。

***

非常好，我已经仔细读取了你2025年的第八讲内容（迭代序列引例、IEEE双精度、误差类型、随机游走累积模型、总误差最优化等）。本次讲义将在此基础上**深化、重构并加入2026年AI辅助视角**，避免重复，聚焦在"为什么"和"物理影响"上。

***

# 三、浮点数体系：计算机如何存储数字，截断误差与舍入误差的权衡

> **核心问题**：你的 Python 代码在数学上是"正确"的，为什么计算结果还会出错？——答案藏在计算机存储数字的方式里。

***

## 3.1 开篇引例：永不消失的误差

先运行这段代码，观察一个令人不安的现象：

```python
import numpy as np

# 引例：理论上恒为 1/3 的迭代序列
x = 1/3
print(f"初始值: {x:.20f}")   # 真的是 1/3 吗？

for n in range(60):
    x = 4 * x - 1
    if n % 10 == 9:
        print(f"第 {n+1:2d} 步: x = {x:.6e}")
```

**预期输出：**
```
初始值: 0.33333333333333331483
第 10 步: x = 3.333333e-01   ← 暂时正常
第 20 步: x = 3.276991e-01   ← 开始偏离
第 30 步: x = 5.587935e+05   ← 完全发散！
第 60 步: x = 6.145784e+17   ← 误差指数爆炸
```

这不是 bug，这是浮点数体系的**物理本质**在作怪。初始舍入误差 $\delta_0 \sim 10^{-16}$，经过 $n$ 步迭代后放大为 $4^n \delta_0$，经过60步后误差高达 $4^{60} \times 10^{-16} \approx 10^{20}$，彻底淹没了真实值 。 

***

## 3.2 IEEE 754：计算机存储数字的"物理结构"

### 3.2.1 浮点数不是实数

数学中的实数是**连续的**；计算机中的浮点数是**离散的、有限的**。这一根本差异是所有数值误差的来源。

双精度浮点数（`float64`，Python 默认）按照 **IEEE 754 标准**，用 64 个比特位存储 ： 

```
 63      62    52   51                           0
 ┌───┬────────────┬──────────────────────────────┐
 │ S │  指数 E   │         尾数 M                │
 │ 1 │  11 bits  │         52 bits               │
 └───┴────────────┴──────────────────────────────┘

数值 = (-1)^S × 2^(E-1023) × (1.M)₂
```

三个部分的物理意义：

| 部分 | 比特数 | 决定的物理量 |
|------|--------|-----------|
| **符号位 S** | 1 bit | 正数 / 负数 |
| **指数 E** | 11 bits | 数值的**量级**（范围）|
| **尾数 M** | 52 bits | 数值的**精度**（有效数字）|

### 3.2.2 用 Python 亲眼看浮点数的离散性

```python
import numpy as np
import struct

def float_to_bits(x):
    """将 float64 转为二进制表示"""
    bits = struct.pack('d', x)
    return format(int.from_bytes(bits, 'little'), '064b')

# 1/3 在计算机中的真实面目
x = 1/3
bits = float_to_bits(x)
print(f"1/3 的二进制: {bits[0]} | {bits[1:12]} | {bits[12:]}")
print(f"1/3 的精确值: {x:.20f}")
print(f"误差:         {abs(x - 1/3):.2e}")  # 这行会输出 0？为什么？

# 演示浮点数的离散性
x = 1.0
eps = np.spacing(x)   # x 附近的最小间隔
print(f"\n1.0 附近的浮点间隔: {eps:.2e}")   # = 2^-52 ≈ 2.22e-16
print(f"1.0 + eps/2 == 1.0? {1.0 + eps/2 == 1.0}")   # True！小于间隔的数被"吞掉"
print(f"1.0 + eps   == 1.0? {1.0 + eps == 1.0}")      # False

# 机器精度随数值大小变化
for val in [1e-10, 1.0, 1e10]:
    print(f"np.spacing({val:.0e}) = {np.spacing(val):.2e}")
```

> 🔑 **关键洞见**：`np.spacing(x)` 随 $x$ 的增大而增大。在 $x = 10^{10}$ 附近，两个相邻浮点数之间的间距约为 $10^{-6}$——你以为在做精确计算，实际上精度已损失10位 ！ 
### 3.2.3 双精度浮点数的物理极限

```python
print(f"最大正数:   {np.finfo(np.float64).max:.2e}")   # ~1.8e308
print(f"最小正数:   {np.finfo(np.float64).tiny:.2e}")  # ~2.2e-308
print(f"机器精度 ε: {np.finfo(np.float64).eps:.2e}")   # ~2.2e-16
print(f"有效数字:   约 {int(-np.log10(np.finfo(np.float64).eps))} 位")
```

***

## 3.3 两类误差的本质：截断误差 vs 舍入误差

计算物理中的误差分为四大类，但数值算法主要关注其中两类 ： 
```
误差全家族
├── 模型误差：把真实天体当质点（建模阶段，不在本节讨论）
├── 观测误差：测量仪器精度限制（数据处理阶段）
├── 截断误差 ←─── 今天重点 1
└── 舍入误差 ←─── 今天重点 2
```

### 3.1 截断误差——算法的固有代价

截断误差来自用**有限步骤近似无穷过程**。最典型的例子是泰勒展开截断：

$$
\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots
$$

保留前 $N$ 项，截断误差 $\approx \frac{x^{2N+1}}{(2N+1)!}$，随 $N$ 增大**迅速减小** 。 

数值微分也存在截断误差。以前向差分为例，对 $f'(x)$ 的近似：

$$
f'(x) \approx \frac{f(x+h) - f(x)}{h}
$$

泰勒展开可以证明，截断误差 $\propto h$（一阶精度）：

$$
\varepsilon_{\text{approx}} = \frac{h}{2} f''(x) + O(h^2)
$$

而中心差分 $\dfrac{f(x+h) - f(x-h)}{2h}$ 的截断误差 $\propto h^2$（二阶精度），精度提升一个量级。

### 3.2 舍入误差——硬件的无奈

舍入误差来自**浮点数的离散性**。每次算术运算都引入约 $\varepsilon_m \sim 10^{-16}$ 的相对误差。经过 $N$ 步随机游走式的误差累积 ： 

$$
\varepsilon_{\text{ro}} \approx \sqrt{N} \cdot \varepsilon_m
$$

这就是为什么步数越多，舍入误差越大——即使每步误差微小，累积效应不可忽视。

### 3.3 让 AI 帮你量化两类误差

在 Trae 中运行以下代码，**亲眼看到两类误差的对立**：

```python
import numpy as np
import matplotlib.pyplot as plt

# 用数值微分近似 sin'(x) = cos(x)，x = π/4
x = np.pi / 4
exact = np.cos(x)

h_values = np.logspace(-16, 0, 300)   # 步长从 1e-16 到 1
errors = []

for h in h_values:
    # 中心差分
    numerical = (np.sin(x + h) - np.sin(x - h)) / (2 * h)
    errors.append(abs(numerical - exact) / abs(exact))

errors = np.array(errors)

# 找最优步长
best_idx = np.argmin(errors)
best_h   = h_values[best_idx]
best_err = errors[best_idx]

plt.figure(figsize=(9, 5))
plt.loglog(h_values, errors, 'b-', lw=1.5, label='总误差')
plt.axvline(best_h, color='red', ls='--', label=f'最优步长 h ≈ {best_h:.1e}')
plt.axhline(best_err, color='green', ls=':', label=f'最小误差 ≈ {best_err:.1e}')

# 标注两个误差区间
plt.annotate('← 截断误差主导\n  (h 越小越好)',
             xy=(1e-4, 1e-10), fontsize=9, color='navy')
plt.annotate('舍入误差主导 →\n  (h 越小越糟)',
             xy=(1e-14, 1e-4), fontsize=9, color='darkred')

plt.xlabel('步长 h'); plt.ylabel('相对误差')
plt.title('数值微分的总误差：截断误差 vs 舍入误差的博弈')
plt.legend(); plt.grid(True, alpha=0.3)
plt.savefig('error_tradeoff.png', dpi=150)
plt.show()
print(f"最优步长: {best_h:.2e}，最小误差: {best_err:.2e}")
```

你将看到经典的"**误差 U 形曲线**"：

```
误差
 │\                        舍入误差
 │ \                      /（∝ εm/h）
 │  \                    /
 │   \                  /
 │    \________________/  ← 最优步长
 │        截断误差（∝ h²）
 └─────────────────────── 步长 h
   小                    大
```

***

## 3.4 总误差最优化——找到最佳步长

### 3.4.1 总误差公式

对于一个截断误差 $\propto N^{-\beta}$ 的算法，总误差为两者之和 ： 

$$
\varepsilon_{\text{tot}} = \underbrace{\frac{\alpha}{N^\beta}}_{\text{截断误差}} + \underbrace{\sqrt{N}\,\varepsilon_m}_{\text{舍入误差}}
$$

对 $N$ 求导令其为零，可以找到最优步数 $N_{\text{opt}}$：

$$
\frac{d\varepsilon_{\text{tot}}}{dN} = -\frac{\alpha\beta}{N^{\beta+1}} + \frac{\varepsilon_m}{2\sqrt{N}} = 0
\implies N_{\text{opt}}^{\beta + 1/2} = \frac{2\alpha\beta}{\varepsilon_m}
$$

### 3.4.2 实际案例对比

| 算法精度 | $\varepsilon_{\text{approx}}$ | 最优 $N$（双精度）| 最小总误差 |
|---------|-------------------------------|-------------------|----------|
| 一阶（前向差分）| $\alpha / N$ | $\sim 10^{11}$ | $\sim 10^{-8}$ |
| 二阶（中心差分）| $\alpha / N^2$ | $\sim 10^5$ | $\sim 10^{-11}$ |
| 四阶（RK4）| $\alpha / N^4$ | $\sim 10^3$ | $\sim 10^{-13}$ |

> 💡 **物理直觉**：高阶算法（如 RK4）用**更少的步数**达到**更低的误差**。这正是为什么天文数值模拟优先用 RK4 而非简单欧拉法——不只是精度，还有**计算效率**。

***

## 3.5 四大数值陷阱与防御策略

你的旧讲义中已提到这四个陷阱 ，这里用物理案例深化理解： 

### 陷阱 1：两个相近的数相减（精度灾难）

```python
# 抛物线方程的两种求解方式
a, b, c = 1, -(1e17 + 1), 1e17

# ❌ 直接公式：b² ≈ √b² → x2 ≈ 0（大数吃掉小数）
discriminant = np.sqrt(b**2 - 4*a*c)
x1_bad = (-b + discriminant) / (2*a)
x2_bad = (-b - discriminant) / (2*a)   # 灾难性抵消！

# ✅ 等价公式：利用韦达定理 x1*x2 = c/a
x2_good = c / (a * x1_bad)

print(f"精确解: x1 = 1e17,  x2 = 1.0")
print(f"直接公式: x1 = {x1_bad:.4e},  x2 = {x2_bad:.4e}")   # x2 ≈ 0！
print(f"优化公式: x1 = {x1_bad:.4e},  x2 = {x2_good:.4e}")  # x2 ≈ 1 ✓
```

### 陷阱 2：浮点数相等判断

```python
# ❌ 永远不要这样写
x = 0.1 + 0.2
if x == 0.3:
    print("相等")   # 永远不会执行！

# ✅ 正确的比较方式
epsilon = 1e-12
if abs(x - 0.3) < epsilon:
    print(f"在精度 {epsilon} 内相等")  # ✓
```

### 陷阱 3：步长过小引起舍入主导

从上面的 U 形曲线可以看到，步长 `h = 1e-15` 比 `h = 1e-7` 的误差反而**更大**。

### 陷阱 4：大数吃掉小数

在 N 体模拟中，若某颗星 $10^{10}$ 倍质量的天体存在，其引力场会在浮点精度上"淹没"小质量天体的动能项。解决方案：对各物理量做无量纲化（归一化）处理。

***

## 3.6 AI 时代的误差分析新范式

### 用 AI 诊断误差来源

当你遇到数值结果可疑时，可以用以下 Prompt 让 AI 帮助诊断：

```
我的 N 体引力模拟在运行 1000 步后，总能量误差达到 0.5%，
超出了预期的 0.01%。

【算法参数】
- 数值方法: Euler 法（一阶）
- 时间步长: dt = 0.01 s
- 粒子数: 100
- 模拟时长: 1000 步

请帮我：
1. 分析误差超标的主要来源：截断误差还是舍入误差？
2. 估算 Euler 法的截断误差量级（用 dt 的幂次表示）
3. 推荐能将误差降到 0.001% 的改进方案（比较 RK2、RK4 的代价）
4. 给出改进后的代码片段
```

> ✅ AI 能快速给出理论分析，但你需要自己验证：**数值实验 > AI 理论推导**。改完代码后，必须重新测量实际误差。

### 用误差分析评估 AI 生成的代码

当 AI 为你生成数值算法代码时，加入以下**标准验收测试**：

```python
def convergence_test(solver, exact_func, h_values):
    """
    收敛性测试：验证数值算法的阶数是否符合理论预期
    solver: AI 生成的数值求解器
    exact_func: 解析解
    h_values: 一组步长值
    """
    errors = []
    for h in h_values:
        numerical = solver(h)
        exact = exact_func()
        errors.append(abs(numerical - exact))

    # 用对数线性回归估计收敛阶数
    log_h = np.log10(h_values)
    log_e = np.log10(errors)
    order = np.polyfit(log_h, log_e, 1)[0]
    print(f"收敛阶数估计: {order:.2f}（理论值: RK4 应为 4.0）")
    return order
```

***

## 3.7 本小节实验任务

### 【任务 A】浮点数探索（基础）

```python
# 完成以下填空，并解释每个结果的物理意义
print(0.1 + 0.2 == 0.3)          # 填写：预期输出？为什么？
print(1e16 + 1.0 == 1e16)        # 填写：这说明了什么物理现象？
print(np.spacing(1e16))           # 填写：这个数的单位和意义？
```

### 【任务 B】误差 U 形曲线（核心）

修改第三节的代码，对 $\cos'(x) = -\sin(x)$ 同时绘制**前向差分**和**中心差分**的误差曲线，在同一张图中比较两者的最优步长和最小误差，写出你的物理解释。

### 【任务 C】AI 诊断实践（进阶）

对第 1.2 节的双星模拟代码，将步长从 `dt=3600s` 改为 `dt=86400s`（1天/步），观察能量误差的变化，用本节的 Prompt 模板让 AI 分析误差来源，并与你自己的理论估算对比。

***

## 八、本节核心概念速查

| 概念 | 数学表达 | Python 工具 |
|------|---------|------------|
| 机器精度 | $\varepsilon_m = 2^{-52} \approx 2.2 \times 10^{-16}$ | `np.finfo(float).eps` |
| 浮点间隔 | `spacing(x)` ∝ $x$ | `np.spacing(x)` |
| 截断误差 | $\varepsilon_{\text{approx}} \sim \alpha / N^\beta$ | 与 $h$ 正相关 |
| 舍入误差累积 | $\varepsilon_{\text{ro}} \sim \sqrt{N} \varepsilon_m$ | 与 $h$ 负相关 |
| 总误差最优 | $d\varepsilon_{\text{tot}}/dN = 0$ | `np.argmin(errors)` |

***
