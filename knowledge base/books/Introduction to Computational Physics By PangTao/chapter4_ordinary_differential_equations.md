# Chapter 4: Ordinary Differential Equations

Most problems in physics and engineering appear in the form of differential equations. For example, the motion of a classical particle is described by Newton's equation, which is a second-order ordinary differential equation involving at least a second-order derivative in time, and the motion of a quantum particle is described by the Schrödinger equation, which is a partial differential equation involving a first-order partial derivative in time and second-order partial derivatives in coordinates.

In general, we can classify ordinary differential equations into three major categories:

1. **Initial-value problems**: which involve time-dependent equations with given initial conditions
2. **Boundary-value problems**: which involve differential equations with specified boundary conditions
3. **Eigenvalue problems**: which involve solutions for selected parameters (eigenvalues) in the equations

## 4.1 Initial-Value Problems

Typically, initial-value problems involve dynamical systems. The behavior of a dynamical system can be described by a set of first-order differential equations:

$$\frac{d\mathbf{y}}{dt} = \mathbf{g}(\mathbf{y}, t) \tag{4.1}$$

where:

$$\mathbf{y} = (y_1, y_2, ..., y_l) \tag{4.2}$$

is the dynamical variable vector, and:

$$\mathbf{g}(\mathbf{y}, t) = [g_1(\mathbf{y}, t), g_2(\mathbf{y}, t), ..., g_l(\mathbf{y}, t)] \tag{4.3}$$

is the generalized velocity vector.

**Example - Newton's Equation:**

For a particle moving in one dimension under an elastic force:

$$f = ma \tag{4.4}$$

We can rewrite Newton's equation in the form of Eq. (4.1) with $l = 2$:

$$\frac{dy_1}{dt} = y_2 \tag{4.5}$$
$$\frac{dy_2}{dt} = -\frac{k}{m}y_1 \tag{4.6}$$

where $y_1 = x$ (position) and $y_2 = v = dx/dt$ (velocity).

## 4.2 The Euler and Picard Methods

### Euler Method

The simplest algorithm for initial-value problems:

$$y_{i+1} = y_i + \tau g_i + O(\tau^2) \tag{4.8}$$

where $\tau = t_{i+1} - t_i$ is the time step. The accuracy is relatively low, with accumulated error on the order of $O(\tau)$.

### Picard Method

An adaptive scheme using the trapezoid rule:

$$y_{i+1} = y_i + \frac{\tau}{2}(g_i + g_{i+1}) + O(\tau^3) \tag{4.10}$$

The Picard method iterates from right to left:

$$y_{i+1}^{(k+1)} = y_i + \frac{\tau}{2}(g_i + g_{i+1}^{(k)})$$

## 4.3 Predictor-Corrector Methods

One way to avoid tedious iterations is to use the predictor-corrector method:

1. **Predict** the next value using Euler method
2. **Correct** using a better algorithm (e.g., trapezoid rule)

**Java Implementation:**

```java
// A program to study the motion of a particle under an elastic force
// in one dimension through the simplest predictor-corrector scheme.
import java.lang.*;

public class Motion2 {
    static final int n = 100, j = 5;
    
    public static void main(String argv[]) {
        double x[] = new double[n+1];
        double v[] = new double[n+1];
        
        // Assign time step and initial position and velocity
        double dt = 2*Math.PI/n;
        x[0] = 0;
        v[0] = 1;
        
        // Calculate other position and velocity recursively
        for (int i=0; i<n; ++i) {
            // Predict the next position and velocity
            x[i+1] = x[i] + v[i]*dt;
            v[i+1] = v[i] - x[i]*dt;
            
            // Correct the new position and velocity
            x[i+1] = x[i] + (v[i] + v[i+1])*dt/2;
            v[i+1] = v[i] - (x[i] + x[i+1])*dt/2;
        }
    }
}
```

### Higher-Order Algorithm

Taking $j = 2$ in Eq. (4.9) and using linear interpolation:

$$y_{i+2} = y_i + 2\tau g_{i+1} + O(\tau^3) \tag{4.12}$$

Using Simpson's rule:

$$y_{i+2} = y_i + \frac{\tau}{3}(g_i + 4g_{i+1} + g_{i+2}) + O(\tau^5) \tag{4.15}$$

### Example: Motorcycle Jump

The motion of a motorcycle with air resistance:

$$\frac{d\mathbf{r}}{dt} = \mathbf{v} \tag{4.16}$$
$$\frac{d\mathbf{v}}{dt} = \mathbf{a} = \frac{\mathbf{f}}{m} \tag{4.17}$$

where:

$$\mathbf{f} = -mg\hat{y} - \kappa v\mathbf{v} \tag{4.18}$$

## 4.4 The Runge-Kutta Method

The fourth-order Runge-Kutta algorithm is given by:

$$y(t+\tau) = y(t) + \frac{1}{6}(c_1 + 2c_2 + 2c_3 + c_4) \tag{4.33}$$

where:

$$c_1 = \tau g(y, t) \tag{4.34}$$
$$c_2 = \tau g\left(y + \frac{c_1}{2}, t + \frac{\tau}{2}\right) \tag{4.35}$$
$$c_3 = \tau g\left(y + \frac{c_2}{2}, t + \frac{\tau}{2}\right) \tag{4.36}$$
$$c_4 = \tau g(y + c_3, t + \tau) \tag{4.37}$$

## 4.5 Chaotic Dynamics of a Driven Pendulum

Consider a pendulum with driving force $f_d$ and resistive force $f_r$:

$$ma_t = f_g + f_d + f_r \tag{4.38}$$

with driving force:

$$f_d(t) = f_0 \cos\omega_0 t \tag{4.39}$$

In dimensionless form:

$$\frac{d^2\theta}{dt^2} + q\frac{d\theta}{dt} + \sin\theta = b\cos\omega_0 t \tag{4.40}$$

Defining $y_1 = \theta$ and $y_2 = \omega = d\theta/dt$:

$$\frac{dy_1}{dt} = y_2 \tag{4.41}$$
$$\frac{dy_2}{dt} = -qy_2 - \sin y_1 + b\cos\omega_0 t \tag{4.42}$$

**Java Implementation:**

```java
// A program to study the driven pendulum under damping
// via the fourth-order Runge-Kutta algorithm.
import java.lang.*;

public class Pendulum {
    static final int n = 100, nt = 10, m = 5;
    
    public static void main(String argv[]) {
        double y1[] = new double[n+1];
        double y2[] = new double[n+1];
        double y[] = new double[2];
        
        // Set up time step and initial values
        double dt = 3*Math.PI/nt;
        y1[0] = y[0] = 0;
        y2[0] = y[1] = 2;
        
        // Perform the 4th-order Runge-Kutta integration
        for (int i=0; i<n; ++i) {
            double t = dt*i;
            y = rungeKutta(y, t, dt);
            y1[i+1] = y[0];
            y2[i+1] = y[1];
            
            // Bring theta back to the region [-pi, pi]
            int np = (int) (y1[i+1]/(2*Math.PI) + 0.5);
            y1[i+1] -= 2*Math.PI*np;
        }
    }
    
    // Method to complete one Runge-Kutta step
    public static double[] rungeKutta(double y[], double t, double dt) {
        int l = y.length;
        double c1[] = new double[l];
        double c2[] = new double[l];
        double c3[] = new double[l];
        double c4[] = new double[l];
        
        c1 = g(y, t);
        for (int i=0; i<l; ++i) c2[i] = y[i] + dt*c1[i]/2;
        c2 = g(c2, t+dt/2);
        for (int i=0; i<l; ++i) c3[i] = y[i] + dt*c2[i]/2;
        c3 = g(c3, t+dt/2);
        for (int i=0; i<l; ++i) c4[i] = y[i] + dt*c3[i];
        c4 = g(c4, t+dt);
        for (int i=0; i<l; ++i)
            c1[i] = y[i] + dt*(c1[i]+2*(c2[i]+c3[i])+c4[i])/6;
        return c1;
    }
    
    // Method to provide the generalized velocity vector
    public static double[] g(double y[], double t) {
        double q = 0.5, b = 0.9, omega0 = 2.0/3;
        double v[] = new double[2];
        v[0] = y[1];
        v[1] = -Math.sin(y[0]) + b*Math.cos(omega0*t);
        v[1] -= q*y[1];
        return v;
    }
}
```

## 4.6 Boundary-Value and Eigenvalue Problems

A typical boundary-value problem is given as a second-order differential equation:

$$u'' = f(u, u'; x) \tag{4.48}$$

where $u$ is a function of $x$, and either $u$ or $u'$ is given at each boundary point.

Four possible types of boundary conditions:

1. $u(0) = u_0$ and $u(1) = u_1$
2. $u(0) = u_0$ and $u'(1) = v_1$
3. $u'(0) = v_0$ and $u(1) = u_1$
4. $u'(0) = v_0$ and $u'(1) = v_1$

**Example - Longitudinal Vibrations:**

$$u''(x) = -k^2 u(x) \tag{4.51}$$

with dispersion relation:

$$\omega = ck \tag{4.52}$$

If both ends are fixed: $u(0) = u(1) = 0$, the eigenfunctions are:

$$u_l(x) = \sqrt{2}\sin k_l x \tag{4.53}$$

with eigenvalues:

$$k_l^2 = (l\pi)^2 \tag{4.54}$$

## 4.7 The Shooting Method

The shooting method converts the boundary-value problem into an initial-value problem by introducing an adjustable parameter.

**Example:** Solve the differential equation:

$$u'' = -\frac{\pi^2}{4}(u + 1) \tag{4.58}$$

with boundary conditions $u(0) = 0$ and $u(1) = 1$.

Define new variables $y_1 = u$ and $y_2 = u'$:

$$\frac{dy_1}{dx} = y_2 \tag{4.59}$$
$$\frac{dy_2}{dx} = -\frac{\pi^2}{4}(y_1 + 1) \tag{4.60}$$

The analytical solution is:

$$u(x) = \cos\frac{\pi x}{2} + 2\sin\frac{\pi x}{2} - 1 \tag{4.61}$$

## 4.8 Linear Equations and the Sturm-Liouville Problem

Many eigenvalue or boundary-value problems are in the form of linear equations:

$$u'' + d(x)u' + q(x)u = s(x) \tag{4.62}$$

Using superposition, the correct solution is:

$$u(x) = a u_{\alpha_0}(x) + b u_{\alpha_1}(x) \tag{4.63}$$

where:

$$a = \frac{u_{\alpha_1}(1) - u_1}{u_{\alpha_1}(1) - u_{\alpha_0}(1)} \tag{4.66}$$
$$b = \frac{u_1 - u_{\alpha_0}(1)}{u_{\alpha_1}(1) - u_{\alpha_0}(1)} \tag{4.67}$$

### Sturm-Liouville Problem

$$[p(x)u'(x)]' + q(x)u(x) = s(x) \tag{4.68}$$

The simplest numerical algorithm (accurate to $O(h^4)$):

$$(2p_i + hp'_i)u_{i+1} + (2p_i - hp'_i)u_{i-1} = 4p_i u_i + 2h^2(s_i - q_i u_i) \tag{4.72}$$

### Legendre Equation

$$\frac{d}{dx}\left[(1-x^2)\frac{du}{dx}\right] + l(l+1)u = 0 \tag{4.73}$$

### Numerov Algorithm

For equations without first-order derivative term:

$$c_{i+1}u_{i+1} + c_{i-1}u_{i-1} = c_i u_i + d_i \tag{4.76}$$

where:

$$c_{i+1} = 1 + \frac{h^2}{12}q_{i+1} \tag{4.87}$$
$$c_{i-1} = 1 + \frac{h^2}{12}q_{i-1} \tag{4.88}$$
$$c_i = 2 - \frac{5h^2}{6}q_i \tag{4.89}$$
$$d_i = \frac{h^2}{12}(s_{i+1} + 10s_i + s_{i-1}) \tag{4.90}$$

## 4.9 The One-Dimensional Schrödinger Equation

$$-\frac{\hbar^2}{2m}\frac{d^2\phi(x)}{dx^2} + V(x)\phi(x) = \varepsilon\phi(x) \tag{4.91}$$

Rewritten as:

$$\phi''(x) + \frac{2m}{\hbar^2}[\varepsilon - V(x)]\phi(x) = 0 \tag{4.92}$$

### Eigenvalue Problem

Matching conditions at the turning point $x_r$:

$$\phi_l(x_r) = \phi_r(x_r) \tag{4.93}$$
$$\phi'_l(x_r) = \phi'_r(x_r) \tag{4.94}$$

Combined condition:

$$\frac{\phi'_l(x_r)}{\phi_l(x_r)} = \frac{\phi'_r(x_r)}{\phi_r(x_r)} \tag{4.95}$$

**Example Potential:**

$$V(x) = \frac{\hbar^2}{2m}\alpha^2\lambda(\lambda-1)\left(\frac{1}{2} - \frac{1}{\cosh^2(\alpha x)}\right) \tag{4.97}$$

Exact eigenvalues:

$$\varepsilon_n = \frac{\hbar^2\alpha^2}{2m}\left[\frac{\lambda(\lambda-1)}{2} - (\lambda - 1 - n)^2\right] \tag{4.98}$$

### Quantum Scattering

General solution outside potential region:

$$\phi(x) = \begin{cases} \phi_1(x) = e^{ikx} + Ae^{-ikx} & \text{for } x < 0 \\ \phi_3(x) = Be^{ik(x-a)} & \text{for } x > a \end{cases} \tag{4.99}$$

where:

$$\varepsilon = \frac{\hbar^2 k^2}{2m} \tag{4.100}$$

Reflectivity $R = |A|^2$ and transmissivity $T = |B|^2$, with $T + R = 1$.

**Double-Barrier Potential:**

$$V(x) = \begin{cases} V_0 & \text{if } 0 \leq x \leq x_1 \text{ or } x_2 \leq x \leq a \\ 0 & \text{elsewhere} \end{cases} \tag{4.113}$$

## Exercises

4.1 Consider two charged particles of masses $m_1$ and $m_2$, and charges $q_1$ and $q_2$, moving in the $xy$ plane under constant electric and magnetic fields. Implement the two-point predictor-corrector method.

4.2 Derive the fourth-order Runge-Kutta algorithm and discuss the options in parameter selection.

4.3 Construct a subprogram that solves differential equations with the fourth-order Runge-Kutta method with different parameters.

4.4 Study the driven pendulum under damping numerically and plot the bifurcation diagram.

4.5 Modify the example program for the driven pendulum with different driving forces (square wave, triangular wave).

4.6 The Duffing model: $\frac{d^2x}{dt^2} + g\frac{dx}{dt} + x^3 = b\cos t$. Write a program and discuss the behavior.

4.7 The Hénon-Heiles model for stellar orbits. Derive and solve the equations numerically.

4.8 The Lorenz model for climate change. Solve numerically and find chaotic parameter regions.

4.9 Consider three objects in the solar system: Sun, Earth, and Mars. Find the modification of Earth's period due to Mars.

4.10 Study the dynamics of two electrons in a classical helium atom.

4.11 Apply the Numerov algorithm to solve $u''(x) = -4\pi^2 u(x)$ and discuss accuracy.

4.12 Apply the shooting method to solve the eigenvalue problem $u''(x) = \lambda u(x)$.

4.13 Develop a program using fourth-order Runge-Kutta and bisection methods for the stationary Schrödinger equation.

4.14 Apply the fourth-order Runge-Kutta algorithm to solve the quantum scattering problem.

4.15 Find the angle dependence of angular velocity for a falling meterstick with friction.

4.16 Implement the full-accuracy algorithm for the Sturm-Liouville problem and test with spherical Bessel equation.

4.17 Study the dynamics of a compact disk rotating on a horizontal table.

4.18 The tippet-top problem: Establish a model and solve the equations.

4.19 The system of two coupled rotors. Write a program and study chaotic behavior.
