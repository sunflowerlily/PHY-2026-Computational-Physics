# Algorithm Reference Sheet

## 1. Interpolation & Fitting (Weeks 2 & 13)

### Lagrange Interpolation
$$ P(x) = \sum_{j=0}^{k} y_j L_j(x), \quad L_j(x) = \prod_{i \neq j} \frac{x - x_i}{x_j - x_i} $$

### Chi-Squared ($\chi^2$) Statistic
For observed data $O_i$, model $E_i$, and uncertainty $\sigma_i$:
$$ \chi^2 = \sum_{i=1}^{N} \frac{(O_i - E_i(\theta))^2}{\sigma_i^2} $$
*Reduced Chi-Squared*: $\chi^2_\nu = \chi^2 / (N - k)$, where $k$ is the number of free parameters. Ideally $\chi^2_\nu \approx 1$.

## 2. ODE Solvers (Weeks 3-4)

### Runge-Kutta 4 (RK4)
$$ k_1 = h f(t_n, y_n) $$
$$ k_2 = h f(t_n + h/2, y_n + k_1/2) $$
$$ k_3 = h f(t_n + h/2, y_n + k_2/2) $$
$$ k_4 = h f(t_n + h, y_n + k_3) $$
$$ y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4) $$

### Symplectic Euler (Semi-Implicit)
$$ v_{n+1} = v_n - h \frac{\partial V}{\partial q}(q_n) $$
$$ q_{n+1} = q_n + h v_{n+1} $$

## 3. PDE Methods (Weeks 7-8)

### FTCS (Diffusion Equation)
$$ u_j^{n+1} = u_j^n + \frac{D \Delta t}{(\Delta x)^2} (u_{j+1}^n - 2u_j^n + u_{j-1}^n) $$
*Stability*: $\frac{2D \Delta t}{(\Delta x)^2} \le 1$

### Relaxation (Laplace Equation)
$$ u_{i,j}^{new} = \frac{1}{4} (u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1}) $$

## 4. Fourier Transform (Week 12)
### Discrete Fourier Transform (DFT)
$$ X_k = \sum_{n=0}^{N-1} x_n e^{-i 2\pi k n / N} $$