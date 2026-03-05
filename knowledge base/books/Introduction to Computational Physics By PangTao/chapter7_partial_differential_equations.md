# Chapter 7: Partial Differential Equations

Many physics problems are given in the form of a second-order partial differential equation: elliptic, parabolic, or hyperbolic. The numerical methods for ordinary differential equations discussed in Chapter 4 can be generalized to study differential equations involving more than one independent variable.

## 7.1 Partial Differential Equations in Physics

### Types of PDEs in Physics

**Poisson equation** (elliptic):

$$\nabla^2 \phi(\mathbf{r}) = -\frac{\rho(\mathbf{r})}{\varepsilon_0} \tag{7.1}$$

**Diffusion equation** (parabolic):

$$\frac{\partial n(\mathbf{r},t)}{\partial t} - \nabla \cdot D(\mathbf{r})\nabla n(\mathbf{r},t) = S(\mathbf{r},t) \tag{7.2}$$

**Wave equation** (hyperbolic):

$$\frac{1}{c^2}\frac{\partial^2 u(\mathbf{r},t)}{\partial t^2} - \nabla^2 u(\mathbf{r},t) = R(\mathbf{r},t) \tag{7.3}$$

**Time-dependent Schrödinger equation**:

$$-\frac{\hbar}{i}\frac{\partial \Psi(\mathbf{r},t)}{\partial t} = H\Psi(\mathbf{r},t) \tag{7.4}$$

### Fluid Dynamics Equations

**Navier-Stokes equation:**

$$\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v} + \frac{1}{\rho}\nabla P - \eta \nabla^2 \mathbf{v} = 0 \tag{7.5}$$

**Continuity equation:**

$$\frac{\partial \rho}{\partial t} + \nabla \cdot \rho \mathbf{v} = 0 \tag{7.6}$$

**Equation of state:**

$$f(P, \rho) = 0 \tag{7.7}$$

## 7.2 Separation of Variables

The basic idea is to reduce a partial differential equation to several ordinary differential equations.

### Standing Waves on a String

The wave equation for a uniform string with fixed ends:

$$\frac{\partial^2 u(x,t)}{\partial t^2} - c^2\frac{\partial^2 u(x,t)}{\partial x^2} = 0 \tag{7.8}$$

where $c = \sqrt{T/\rho}$ is the phase speed.

Assume separation of variables: $u(x,t) = X(x)\Theta(t)$

This leads to:

$$\frac{\Theta''(t)}{\Theta(t)} = c^2\frac{X''(x)}{X(x)} = -\omega^2 \tag{7.10}$$

The spatial equation:

$$X''(x) = -k^2 X(x) \tag{7.11}$$

with $k = \omega/c$.

**Eigenvalues:**

$$k_n = \frac{n\pi}{L}, \quad n = 1, 2, ..., \infty \tag{7.13}$$

**General solution:**

$$u(x,t) = \sum_{n=1}^{\infty} (a_n \sin\omega_n t + b_n \cos\omega_n t) \sin k_n x \tag{7.16}$$

where:

$$\omega_n = ck_n = \frac{n\pi c}{L} \tag{7.15}$$

**Coefficients from initial conditions:**

$$b_l = \frac{2}{L}\int_0^L u_0(x) \sin k_l x \, dx \tag{7.19}$$

$$a_l = \frac{2}{\omega_l L}\int_0^L v_0(x) \sin k_l x \, dx \tag{7.20}$$

### Loaded String Problem

For a string with non-uniform mass density:

$$\frac{\partial^2 u(x,t)}{\partial t^2} = \frac{T}{\rho(x)}\frac{\partial^2 u(x,t)}{\partial x^2} - g \tag{7.21}$$

The static equilibrium shape:

$$\frac{d^2 u_p(x)}{dx^2} = \frac{g\rho(x)}{T} \tag{7.23}$$

### Diffusion Equation in 3D

For an isotropic, three-dimensional infinite space:

$$\frac{\partial n(\mathbf{r},t)}{\partial t} - D\nabla^2 n(\mathbf{r},t) = S(\mathbf{r},t) \tag{7.25}$$

Using the impulse method:

$$n(\mathbf{r},t) = \int_0^t \eta(\mathbf{r},t;\tau) d\tau \tag{7.26}$$

The solution for a point source:

$$\eta(\mathbf{r},t) = \frac{1}{\sqrt{4\pi D t}} \int S(\mathbf{r}',\tau) e^{-(\mathbf{r}-\mathbf{r}')^2/4Dt} d\mathbf{r}' \tag{7.38}$$

**Final solution:**

$$n(\mathbf{r},t) = \int_0^t \frac{d\tau}{\sqrt{4\pi D(t-\tau)}} \int S(\mathbf{r}',\tau) e^{-(\mathbf{r}-\mathbf{r}')^2/4D(t-\tau)} d\mathbf{r}' \tag{7.39}$$

## 7.3 Discretization of the Equation

### Finite Difference Formulas

**First-order time derivative (two-point):**

$$\frac{\partial A(\mathbf{r},t)}{\partial t} = \frac{A(\mathbf{r},t_{k+1}) - A(\mathbf{r},t_k)}{\tau} \tag{7.48}$$

**First-order time derivative (three-point):**

$$\frac{\partial A(\mathbf{r},t)}{\partial t} = \frac{A(\mathbf{r},t_{k+1}) - A(\mathbf{r},t_{k-1})}{2\tau} \tag{7.49}$$

**Second-order time derivative:**

$$\frac{\partial^2 A(\mathbf{r},t)}{\partial t^2} = \frac{A(\mathbf{r},t_{k+1}) - 2A(\mathbf{r},t_k) + A(\mathbf{r},t_{k-1})}{\tau^2} \tag{7.50}$$

**Spatial derivatives:**

$$\frac{\partial A(\mathbf{r},t)}{\partial x} = \frac{A(x_{k+1},y,z,t) - A(x_{k-1},y,z,t)}{2h_x} \tag{7.51}$$

$$\frac{\partial^2 A(\mathbf{r},t)}{\partial x^2} = \frac{A(x_{k+1},y,z,t) - 2A(x_k,y,z,t) + A(x_{k-1},y,z,t)}{h_x^2} \tag{7.52}$$

### Variational Discretization

For the one-dimensional Poisson equation:

$$\frac{d}{dx}\left(\varepsilon(x)\frac{d\phi}{dx}\right) = -\rho(x) \tag{7.53}$$

Construct a functional:

$$U = \int_0^L \left[\frac{1}{2}\varepsilon(x)\left(\frac{d\phi}{dx}\right)^2 - \rho(x)\phi(x)\right] dx \tag{7.54}$$

The discrete form leads to:

$$\varepsilon_{k+1/2}\phi_{k+1} - (\varepsilon_{k+1/2} + \varepsilon_{k-1/2})\phi_k + \varepsilon_{k-1/2}\phi_{k-1} = -h^2\rho_k \tag{7.58}$$

## 7.4 The Matrix Method for Difference Equations

A general linear differential equation:

$$Lu(\mathbf{r},t) = f(\mathbf{r},t) \tag{7.60}$$

can be discretized into matrix form:

$$\mathbf{A}\mathbf{u} = \mathbf{b} \tag{7.61}$$

### Example: Person Sitting on a Bench

The curvature equation:

$$YI\frac{d^2u(x)}{dx^2} = f(x) \tag{7.64}$$

Discretized form:

$$u_{i+1} - 2u_i + u_{i-1} = \frac{h^2 f_i}{YI} \tag{7.65}$$

Matrix form with tridiagonal coefficient matrix:

$$\begin{pmatrix} -2 & 1 & \cdots & 0 \\ 1 & -2 & 1 & \cdots \\ \vdots & \ddots & \ddots & \ddots \\ 0 & \cdots & 1 & -2 \end{pmatrix} \begin{pmatrix} u_1 \\ u_2 \\ \vdots \\ u_n \end{pmatrix} = \begin{pmatrix} b_1 \\ b_2 \\ \vdots \\ b_n \end{pmatrix} \tag{7.66}$$

**Java Implementation:**

```java
// A program to solve the problem of a person sitting on a bench
import java.lang.*;

public class Bench {
    final static int n = 99, m = 2;
    
    public static void main(String argv[]) {
        double d[] = new double[n];
        double b[] = new double[n];
        double c[] = new double[n];
        
        double l = 3, l2 = l/2, h = l/(n+1), h2 = h*h;
        double x0 = 0.25, x2 = x0*x0, e0 = 1/Math.E;
        double rho = 3, g = 9.8, f0 = 200;
        double y = 1e9*Math.pow(0.03,3)*0.2/3;
        
        // Evaluate the coefficient matrix elements
        for (int i=0; i<n; ++i) {
            d[i] = -2;
            c[i] = 1;
            b[i] = -rho*g;
            double x = h*(i+1)-l2;
            if (Math.abs(x) < x0)
                b[i] -= f0*(Math.exp(-x*x/x2)-e0);
            b[i] *= h2/y;
        }
        
        // Obtain the solution
        double u[] = tridiagonalLinearEq(d, c, c, b);
    }
}
```

## 7.5 The Relaxation Method

The relaxation method modifies a guessed solution iteratively to satisfy the difference equation.

### One-Dimensional Diffusion Equation

For the stationary diffusion equation:

$$-\frac{d}{dx}\left(D(x)\frac{dn}{dx}\right) = S(x) \tag{7.68}$$

Discrete form:

$$n_i = \frac{1}{D_{i+1/2} + D_{i-1/2}}[D_{i+1/2}n_{i+1} + D_{i-1/2}n_{i-1} + h^2 S_i] \tag{7.69}$$

**Updating scheme:**

$$n_i^{(k+1)} = (1-p)n_i^{(k)} + pn_i \tag{7.70}$$

where $p \in [0, 2]$ is an adjustable parameter.

### Two-Dimensional Poisson Equation

$$\nabla^2 \phi(\mathbf{r}) = -s(\mathbf{r}) \tag{7.74}$$

Discrete form:

$$\phi_{ij} = \frac{1}{2(1+\alpha)}[\phi_{i+1,j} + \phi_{i-1,j} + \alpha(\phi_{i,j+1} + \phi_{i,j-1}) + h_x^2 s_{ij}] \tag{7.76}$$

where $\alpha = (h_x/h_y)^2$.

**Relaxation scheme:**

$$\phi_{ij}^{(k+1)} = (1-p)\phi_{ij}^{(k)} + p\phi_{ij} \tag{7.77}$$

### Neumann Boundary Condition

For $\frac{dn}{dx}|_{x=0} = 0$:

$$n_0 = \frac{1}{3}(4n_1 - n_2) \tag{7.72}$$

## 7.6 Groundwater Dynamics

### Darcy's Law

$$\mathbf{q} = -\boldsymbol{\sigma} \cdot \nabla \phi \tag{7.78}$$

where $\mathbf{q}$ is the specific discharge vector, $\boldsymbol{\sigma}$ is the hydraulic conductivity tensor, and $\phi$ is the head.

### Groundwater Flow Equation

$$\mu\frac{\partial \phi(\mathbf{r},t)}{\partial t} - \nabla \cdot \boldsymbol{\sigma} \cdot \nabla \phi(\mathbf{r},t) = f(\mathbf{r},t) \tag{7.80}$$

For steady, isotropic flow:

$$\nabla^2 \phi(\mathbf{r}) = -f(\mathbf{r})/\sigma \tag{7.81}$$

Without infiltration (Laplace equation):

$$\nabla^2 \phi(\mathbf{r}) = 0 \tag{7.82}$$

**Java Implementation:**

```java
// An example of studying 2D groundwater dynamics through relaxation
import java.lang.*;

public class Groundwater {
    final static int nx = 100, ny = 50, ni = 5;
    
    public static void main(String argv[]) {
        double sigma0 = 1, a = -0.04, phi0 = 200, b = -20;
        double lx = 1000, hx = lx/nx, ly = 500, hy = ly/ny;
        double phi[][] = new double[nx+1][ny+1];
        double sigma[][] = new double[nx+1][ny+1];
        
        // Set up boundary values and trial solution
        for (int i=0; i<=nx; ++i) {
            double x = i*hx;
            for (int j=0; j<=ny; ++j) {
                double y = j*hy;
                sigma[i][j] = sigma0 + a*y;
                phi[i][j] = phi0 + b*Math.cos(Math.PI*x/lx)*y/ly;
            }
        }
        
        for (int step=0; step<ni; ++step) {
            // Ensure boundary conditions
            for (int j=0; j<ny; ++j) {
                phi[0][j] = (4*phi[1][j]-phi[2][j])/3;
                phi[nx][j] = (4*phi[nx-1][j]-phi[nx-2][j])/3;
            }
            relax2d(p, hx, hy, phi, sigma, f);
        }
    }
}
```

## 7.7 Initial-Value Problems

### Wave Equation Reformulation

Define velocity as a new variable:

$$v(\mathbf{r},t) = \frac{\partial u(\mathbf{r},t)}{\partial t} \tag{7.85}$$

This gives two coupled first-order equations:

$$\frac{\partial u(\mathbf{r},t)}{\partial t} = v(\mathbf{r},t) \tag{7.86}$$

$$\frac{1}{c^2}\frac{\partial v(\mathbf{r},t)}{\partial t} = \nabla^2 u(\mathbf{r},t) + R(\mathbf{r},t) \tag{7.87}$$

### One-Dimensional Diffusion Equation

$$\frac{\partial n(x,t)}{\partial t} = D\frac{\partial^2 n(x,t)}{\partial x^2} + S(x,t) \tag{7.89}$$

**Euler method (unstable for $\gamma > 1/2$):**

$$n_i(t+\tau) = n_i(t) + \gamma[n_{i+1}(t) + n_{i-1}(t) - 2n_i(t)] + \tau S_i(t) \tag{7.90}$$

where $\gamma = D\tau/h^2$.

### Crank-Nicolson Method

$$(2-\mathbf{H})n_i(t+\tau) = (2+\mathbf{H})n_i(t) + \tau[S_i(t) + S_i(t+\tau)] \tag{7.93}$$

where:

$$\mathbf{H}n_i(t) = \gamma[n_{i+1}(t) + n_{i-1}(t) - 2n_i(t)] \tag{7.92}$$

### Peaceman-Rachford Algorithm

For 2D diffusion equation, decompose $\mathbf{H} = \mathbf{H}_i + \mathbf{H}_j$:

$$(2-\mathbf{H}_j)n_{ij}(t+\tau/2) = (2+\mathbf{H}_j)n_{ij}(t) + \frac{\tau}{2}[S_{ij}(t) + S_{ij}(t+\tau/2)] \tag{7.97}$$

$$(2-\mathbf{H}_i)n_{ij}(t+\tau) = (2+\mathbf{H}_i)n_{ij}(t+\tau/2) + \frac{\tau}{2}[S_{ij}(t+\tau/2) + S_{ij}(t+\tau)] \tag{7.98}$$

## 7.8 Temperature Field of a Nuclear Waste Rod

The heat equation:

$$\frac{1}{\kappa}\frac{\partial T(\mathbf{r},t)}{\partial t} - \nabla^2 T(\mathbf{r},t) = S(\mathbf{r},t) \tag{7.101}$$

where $\kappa = \sigma/c\rho$ is the diffusivity.

For cylindrical symmetry:

$$\frac{1}{\kappa}\frac{\partial T(r,t)}{\partial t} - \frac{1}{r}\frac{\partial}{\partial r}\left(r\frac{\partial T(r,t)}{\partial r}\right) = S(r,t) \tag{7.102}$$

**Source term:**

$$S(r,t) = \begin{cases} T_0 e^{-t/\tau_0}/a^2 & \text{for } r \leq a \\ 0 & \text{elsewhere} \end{cases} \tag{7.103}$$

**Discretized form:**

$$(2-\mathbf{H})T_i(t+\tau) = (2+\mathbf{H})T_i(t) + \tau\kappa[S_i(t) + S_i(t+\tau)] \tag{7.104}$$

where:

$$\mathbf{H}T_i(t) = \frac{\tau\kappa}{r_i h^2}[r_{i+1/2}T_{i+1}(t) + r_{i-1/2}T_{i-1}(t) - 2r_i T_i(t)] \tag{7.105}$$

**Boundary condition at r=0:**

$$\left.\frac{\partial T}{\partial r}\right|_{r=0} = 0 \tag{7.106}$$

## Exercises

7.1 Solve the Poisson equation on a rectangular geometry using the relaxation method.

7.2 Develop a numerical scheme for the Poisson equation in polar coordinates.

7.3 Derive the difference equation for spherically symmetric charge distribution.

7.4 Derive the relaxation scheme for a three-dimensional system.

7.5 Modify the groundwater dynamics program to study the transient state.

7.6 Write a program that solves the wave equation of a finite string with both ends fixed.

7.7 Solve the time-dependent Schrödinger equation using the Crank-Nicolson method.

7.8 Obtain the algorithm for solving the three-dimensional wave equation.

7.9 Consider an elastic rope with two friends sitting on it:
   - (a) Show the motion is described by $\frac{\partial^2 u}{\partial t^2} = \frac{T}{\rho(x)}\frac{\partial^2 u}{\partial x^2} - g$
   - (b) Find the displacement at equilibrium
   - (c) Find the first five angular frequencies

7.10 Solve the nuclear waste rod problem with extrapolation at the cut-off radius.

7.11 Simulate burning a hole in a silver sheet with a propane torch.

7.12 Solve the Gross-Pitaevskii equation for Bose-Einstein condensate.
