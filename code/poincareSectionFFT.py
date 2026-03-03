import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.fft import rfft, rfftfreq

# ==========================================
# 1. 定义物理系统 (Lorenz System)
# ==========================================
def lorenz(t, state, sigma=10, beta=8/3, rho=350):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# ==========================================
# 2. 庞加莱截面 (Poincaré Section) - 现代方法
# ==========================================
# 定义“事件”：当 x 穿过 0 时触发
def poincare_section_event(t, state):
    return state[0]  # 当 x = 0 时，返回值为 0，触发事件

poincare_section_event.direction = 1  # 仅检测 x 从负变正 (direction=1) 的穿过
poincare_section_event.terminal = False # 触发后不停止模拟

# ==========================================
# 3. 求解与数据生成
# ==========================================
t_span = (0, 200)
t_eval = np.linspace(0, 200, 10000) # 高分辨率用于 FFT
initial_state = [1.0, 1.0, 1.0]

# 求解 ODE，传入 events
sol = solve_ivp(
    lorenz, 
    t_span, 
    initial_state, 
    t_eval=t_eval, 
    events=poincare_section_event,
    rtol=1e-9, atol=1e-9 # 高精度对于混沌模拟至关重要
)

# 提取庞加莱截面点 (Events result)
# sol.y_events[0] 包含了所有触发点时的 (x, y, z)
poincare_points = sol.y_events[0] 

# ==========================================
# 4. FFT 功率谱分析 (Spectral Analysis)
# ==========================================
# 只取后半段数据，去除瞬态 (Transient)
N = len(t_eval) // 2
x_data = sol.y[0][N:] 
dt = t_eval[1] - t_eval[0]

yf = rfft(x_data)
xf = rfftfreq(N, dt)
power_spectrum = np.abs(yf)**2

# ==========================================
# 5. 可视化 (Visualization)
# ==========================================
fig = plt.figure(figsize=(15, 10))

# 图 A: 3D 轨迹 (Matplotlib)
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot(sol.y[0], sol.y[1], sol.y[2], lw=0.5, alpha=0.7)
ax1.set_title("Lorenz Attractor (Phase Space)")
ax1.set_xlabel("X"); ax1.set_ylabel("Y"); ax1.set_zlabel("Z")

# 图 B: 庞加莱截面 (Poincaré Section)
# 我们在 x=0 截面截取，绘制 y-z 平面上的点
ax2 = fig.add_subplot(2, 2, 2)
if len(poincare_points) > 0:
    ax2.scatter(poincare_points[:, 1], poincare_points[:, 2], s=5, c='red', alpha=0.6)
ax2.set_title("Poincaré Section (x=0 plane)")
ax2.set_xlabel("Y"); ax2.set_ylabel("Z")
ax2.grid(True, alpha=0.3)

# 图 C: 功率谱 (Power Spectrum)
ax3 = fig.add_subplot(2, 2, 3)
ax3.semilogy(xf, power_spectrum) # 对数坐标看噪声底
ax3.set_xlim(0, 10) # 关注低频区
ax3.set_title("Power Spectrum (Log Scale)")
ax3.set_xlabel("Frequency (Hz)"); ax3.set_ylabel("Power")
ax3.grid(True, which="both", alpha=0.3)

# 图 D: 蝴蝶效应 (敏感性演示)
# 重新模拟一个微小扰动的轨迹
initial_state_2 = [1.0 + 1e-8, 1.0, 1.0]
sol2 = solve_ivp(lorenz, t_span, initial_state_2, t_eval=t_eval)
separation = np.linalg.norm(sol.y - sol2.y, axis=0)

ax4 = fig.add_subplot(2, 2, 4)
ax4.semilogy(t_eval, separation)
ax4.set_title("Sensitivity to Initial Conditions (Lyapunov)")
ax4.set_xlabel("Time"); ax4.set_ylabel("Separation ||δ||")
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()