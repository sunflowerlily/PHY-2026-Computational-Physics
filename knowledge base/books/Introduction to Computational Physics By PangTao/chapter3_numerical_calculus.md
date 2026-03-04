# Chapter 3: Numerical Calculus

Calculus is at the heart of describing physical phenomena. As soon as we talk about motion, we must invoke differentiation and integration. For example, the velocity and the acceleration of a particle are the first-order and second-order time derivatives of the corresponding position vector, and the distance traveled by a particle is the integral of the corresponding speed over the elapsed time.

## 3.1 Numerical Differentiation

One basic tool that we will often use in this book is the Taylor expansion of a function $f(x)$ around a point $x_0$:

$$f(x) = f(x_0) + (x-x_0)f'(x_0) + \frac{(x-x_0)^2}{2!}f''(x_0) + \cdots + \frac{(x-x_0)^n}{n!}f^{(n)}(x_0) + \cdots \tag{3.1}$$

The first-order derivative of a single-variable function $f(x)$ around a point $x_i$ is defined from the limit:

$$f'(x_i) = \lim_{\Delta x \to 0} \frac{f(x_i + \Delta x) - f(x_i)}{\Delta x} \tag{3.3}$$

### Two-Point Formula

If we divide the space into discrete points $x_i$ with evenly spaced intervals $x_{i+1} - x_i = h$:

$$f'_i = \frac{f_{i+1} - f_i}{h} + O(h) \tag{3.4}$$

### Three-Point Formula

Using Taylor expansions of $f_{i+1}$ and $f_{i-1}$ around $x_i$:

$$f'_i = \frac{f_{i+1} - f_{i-1}}{2h} + O(h^2) \tag{3.6}$$

### Five-Point Formula

$$f'_i = \frac{1}{12h}(f_{i-2} - 8f_{i-1} + 8f_{i+1} - f_{i+2}) + O(h^4) \tag{3.9}$$

### Second-Order Derivative

**Three-point formula:**

$$f''_i = \frac{f_{i+1} - 2f_i + f_{i-1}}{h^2} + O(h^2) \tag{3.11}$$

**Five-point formula:**

$$f''_i = \frac{1}{12h^2}(-f_{i-2} + 16f_{i-1} - 30f_i + 16f_{i+1} - f_{i+2}) + O(h^4) \tag{3.12}$$

### Nonuniform Data Points

For nonuniform data points with $h_i = x_{i+1} - x_i$:

$$f'_i = \frac{h_{i-1}^2 f_{i+1} + (h_i^2 - h_{i-1}^2)f_i - h_i^2 f_{i-1}}{h_i h_{i-1}(h_i + h_{i-1})} + O(h^2) \tag{3.14}$$

$$f''_i = \frac{2[h_{i-1}f_{i+1} - (h_{i-1} + h_i)f_i + h_i f_{i-1}]}{h_i h_{i-1}(h_i + h_{i-1})} + O(h) \tag{3.15}$$

### Adaptive Scheme

Define:

$$\Delta_1(h) = \frac{f(x+h) - f(x-h)}{2h} \tag{3.16}$$

Using the combination:

$$\Delta_1(h) - 4\Delta_1(h/2) = -3f'(x) + O(h^4) \tag{3.17}$$

The criterion for desired accuracy $\delta$: if $h^2|d - d_1| < \delta$, return $(4d_1 - d)/3$.

### Richardson Extrapolation

Starting from $A_{k0} = \Delta_1(h/2^k)$:

$$A_{kl} = \frac{4^l A_{kl-1} - A_{k-1,l-1}}{4^l - 1}$$

for $0 \leq l \leq k$.

**Java Implementation:**

```java
// An example of evaluating the derivatives with the 3-point formulas
import java.lang.*;

public class Deriv {
    static final int n = 100, m = 5;
    
    public static void main(String argv[]) {
        double[] x = new double[n+1];
        double[] f = new double[n+1];
        double[] f1 = new double[n+1];
        double[] f2 = new double[n+1];
        
        int k = 2;
        double h = Math.PI/(2*n);
        for (int i=0; i<=n; ++i) {
            x[i] = h*i;
            f[i] = Math.sin(x[i]);
        }
        
        f1 = firstOrderDerivative(h, f, k);
        f2 = secondOrderDerivative(h, f, k);
        
        for (int i=0; i<=n; i+=m) {
            double df1 = f1[i] - Math.cos(x[i]);
            double df2 = f2[i] + Math.sin(x[i]);
            System.out.println("x = " + x[i]);
            System.out.println("f'(x) = " + f1[i]);
            System.out.println("Error in f'(x): " + df1);
            System.out.println("f''(x) = " + f2[i]);
            System.out.println("Error in f''(x): " + df2);
        }
    }
    
    public static double[] firstOrderDerivative(double h, double f[], int k) {
        int n = f.length-1;
        double[] y = new double[n+1];
        for (int i=1; i<n; ++i)
            y[i] = (f[i+1]-f[i-1])/(2*h);
        // Lagrange extrapolation at boundaries
        y[0] = aitken(0, xl, fl);
        y[n] = aitken(0, xl, fr);
        return y;
    }
    
    public static double[] secondOrderDerivative(double h, double f[], int k) {
        int n = f.length-1;
        double[] y = new double[n+1];
        for (int i=1; i<n; ++i)
            y[i] = (f[i+1]-2*f[i]+f[i-1])/(h*h);
        // Lagrange extrapolation at boundaries
        return y;
    }
}
```

## 3.2 Numerical Integration

We want to obtain the numerical value of an integral:

$$S = \int_a^b f(x) dx \tag{3.21}$$

We can divide the region $[a,b]$ into $n$ slices with evenly spaced interval $h$:

$$\int_a^b f(x) dx = \sum_{i=0}^{n-1} \int_{x_i}^{x_{i+1}} f(x) dx \tag{3.22}$$

### Trapezoid Rule

Approximating $f(x)$ linearly in each slice:

$$S = \frac{h}{2}\sum_{i=0}^{n-1} (f_i + f_{i+1}) + O(h^2) \tag{3.23}$$

### Simpson's Rule

Using Lagrange interpolation over pairs of slices:

$$S = \frac{h}{3}\sum_{j=0}^{n/2-1} (f_{2j} + 4f_{2j+1} + f_{2j+2}) + O(h^4) \tag{3.25}$$

For odd number of slices, the last slice is treated separately:

$$\int_{b-h}^b f(x) dx = \frac{h}{12}(-f_{n-2} + 8f_{n-1} + 5f_n) \tag{3.26}$$

### Nonuniform Data Points

For nonuniform spacing with $h_i = x_{i+1} - x_i$:

$$S_i = \int_{x_{i-1}}^{x_{i+1}} f(x) dx = \alpha f_{i+1} + \beta f_i + \gamma f_{i-1} \tag{3.32}$$

where:

$$\alpha = \frac{2h_i^2 + h_i h_{i-1} - h_{i-1}^2}{6h_i(h_i + h_{i-1})} \tag{3.33}$$
$$\beta = \frac{(h_i + h_{i-1})^3}{6h_i h_{i-1}} \tag{3.34}$$
$$\gamma = \frac{-h_i^2 + h_i h_{i-1} + 2h_{i-1}^2}{6h_i(h_i + h_{i-1})} \tag{3.35}$$

### Adaptive Simpson Rule

Zeroth-level approximation:

$$S_0 = \frac{h}{6}[f(a) + 4f(c) + f(b)] \tag{3.41}$$

First-level approximation:

$$S_1 = \frac{h}{12}[f(a) + 4f(d) + 2f(c) + 4f(e) + f(b)] \tag{3.43}$$

Error estimate:

$$S_1 - S_0 \approx \frac{15}{16}\delta S_0 \approx 15\delta S_1 \tag{3.45}$$

Criterion: $|S_1 - S_0| \leq 15\delta$ for desired accuracy $\delta$.

**Java Implementation:**

```java
// An example of evaluating an integral with the Simpson rule
import java.lang.*;

public class Integral {
    static final int n = 8;
    
    public static void main(String argv[]) {
        double f[] = new double[n+1];
        double h = Math.PI/(2.0*n);
        for (int i=0; i<=n; ++i) {
            double x = h*i;
            f[i] = Math.sin(x);
        }
        double s = simpson(f, h);
        System.out.println("The integral is: " + s);
    }
    
    public static double simpson(double y[], double h) {
        int n = y.length-1;
        double s0 = 0, s1 = 0, s2 = 0;
        for (int i=1; i<n; i+=2) {
            s0 += y[i];
            s1 += y[i-1];
            s2 += y[i+1];
        }
        double s = (s1 + 4*s0 + s2)/3;
        if ((n+1)%2 == 0)
            return h*(s + (5*y[n] + 8*y[n-1] - y[n-2])/12);
        else
            return h*s;
    }
}
```

## 3.3 Roots of an Equation

### Bisection Method

If there is a root $x_r$ in region $[a,b]$ for $f(x) = 0$, we can use the bisection method:

1. Divide region into two equal parts with $x_0 = (a+b)/2$
2. If $f(a)f(x_0) < 0$, next trial is $x_1 = (a+x_0)/2$
3. Otherwise, $x_1 = (x_0+b)/2$
4. Repeat until $|f(x_k)| < \delta$

**Java Implementation:**

```java
// An example of searching for a root via the bisection method
import java.lang.*;

public class Bisect {
    public static void main(String argv[]) {
        double x = 0, del = 1e-6, a = 1, b = 2;
        double dx = b-a;
        int k = 0;
        while (Math.abs(dx) > del) {
            x = (a+b)/2;
            if ((f(a)*f(x)) < 0) {
                b = x;
                dx = b-a;
            } else {
                a = x;
                dx = b-a;
            }
            k++;
        }
        System.out.println("Iteration number: " + k);
        System.out.println("Root obtained: " + x);
        System.out.println("Estimated error: " + dx);
    }
    
    public static double f(double x) {
        return Math.exp(x)*Math.log(x) - x*x;
    }
}
```

### Newton Method

Based on linear approximation:

$$f(x_{k+1}) \approx f(x_k) + (x_{k+1} - x_k)f'(x_k) = 0 \tag{3.48}$$

Iterative scheme:

$$x_{k+1} = x_k - \frac{f_k}{f'_k} \tag{3.49}$$

**Java Implementation:**

```java
// An example of searching for a root via the Newton method
import java.lang.*;

public class Newton {
    public static void main(String argv[]) {
        double del = 1e-6, a = 1, b = 2;
        double dx = b-a, x = (a+b)/2;
        int k = 0;
        while (Math.abs(dx) > del) {
            dx = f(x)/d(x);
            x -= dx;
            k++;
        }
        System.out.println("Iteration number: " + k);
        System.out.println("Root obtained: " + x);
        System.out.println("Estimated error: " + dx);
    }
    
    public static double f(double x) {
        return Math.exp(x)*Math.log(x) - x*x;
    }
    
    public static double d(double x) {
        return Math.exp(x)*(Math.log(x) + 1/x) - 2*x;
    }
}
```

### Secant Method

Replace $f'$ with the two-point formula:

$$x_{k+1} = x_k - \frac{(x_k - x_{k-1})f_k}{f_k - f_{k-1}} \tag{3.50}$$

**Java Implementation:**

```java
// An example of searching for a root via the secant method
import java.lang.*;

public class Root {
    public static void main(String argv[]) {
        double del = 1e-6, a = 1, b = 2;
        double dx = (b-a)/10, x = (a+b)/2;
        int n = 6;
        x = secant(n, del, x, dx);
        System.out.println("Root obtained: " + x);
    }
    
    public static double secant(int n, double del, double x, double dx) {
        int k = 0;
        double x1 = x+dx;
        while ((Math.abs(dx)>del) && (k<n)) {
            double d = f(x1)-f(x);
            double x2 = x1 - f(x1)*(x1-x)/d;
            x = x1;
            x1 = x2;
            dx = x1-x;
            k++;
        }
        return x1;
    }
    
    public static double f(double x) {
        return Math.exp(x)*Math.log(x) - x*x;
    }
}
```

## 3.4 Extremes of a Function

An extreme of $g(x)$ occurs at the point with:

$$f(x) = \frac{dg(x)}{dx} = 0 \tag{3.51}$$

This is a minimum (maximum) if $f'(x) = g''(x)$ is greater (less) than zero.

### Example: Bond Length of NaCl

The interaction potential between Na⁺ and Cl⁻:

$$V(r) = -\frac{e^2}{4\pi\varepsilon_0 r} + V_0 e^{-r/r_0} \tag{3.52}$$

The force between the two ions:

$$f(r) = -\frac{dV(r)}{dr} = -\frac{e^2}{4\pi\varepsilon_0 r^2} + \frac{V_0}{r_0}e^{-r/r_0} \tag{3.53}$$

At equilibrium, $f(r) = 0$. Using the secant method with $e^2/4\pi\varepsilon_0 = 14.4$ Å·eV, $V_0 = 1090$ eV, $r_0 = 0.33$ Å, we obtain bond length $r_{eq} = 2.36$ Å.

### Steepest Descent Method

For multivariable case $g = g(x_1, x_2, ..., x_l)$:

$$\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta\mathbf{x}_k = \mathbf{x}_k - a\nabla g(\mathbf{x}_k)/|\nabla g(\mathbf{x}_k)| \tag{3.55}$$

where $\mathbf{x} = (x_1, x_2, ..., x_l)$ and $\nabla g(\mathbf{x}) = (\partial g/\partial x_1, \partial g/\partial x_2, ..., \partial g/\partial x_l)$.

**Java Implementation:**

```java
// An example of searching for a minimum of a multivariable function
import java.lang.*;

public class Minimum {
    public static void main(String argv[]) {
        double del = 1e-6, a = 0.1;
        double x[] = new double[2];
        x[0] = 0.1;
        x[1] = -1;
        steepestDescent(x, a, del);
        System.out.println("The minimum is at x= " + x[0] + ", y= " + x[1]);
    }
    
    public static void steepestDescent(double x[], double a, double del) {
        int n = x.length;
        double h = 1e-6;
        double g0 = g(x);
        double fi[] = new double[n];
        fi = f(x, h);
        double dg = 0;
        for (int i=0; i<n; ++i) dg += fi[i]*fi[i];
        dg = Math.sqrt(dg);
        double b = a/dg;
        while (dg > del) {
            for (int i=0; i<n; ++i) x[i] -= b*fi[i];
            h /= 2;
            fi = f(x, h);
            dg = 0;
            for (int i=0; i<n; ++i) dg += fi[i]*fi[i];
            dg = Math.sqrt(dg);
            b = a/dg;
            double g1 = g(x);
            if (g1 > g0) a /= 2;
            else g0 = g1;
        }
    }
    
    public static double[] f(double x[], double h) {
        int n = x.length;
        double z[] = new double[n];
        double y[] = (double[]) x.clone();
        double g0 = g(x);
        for (int i=0; i<n; ++i) {
            y[i] += h;
            z[i] = (g(y)-g0)/h;
        }
        return z;
    }
    
    public static double g(double x[]) {
        return (x[0]-1)*(x[0]-1)*Math.exp(-x[1]*x[1])
               + x[1]*(x[1]+2)*Math.exp(-2*x[0]*x[0]);
    }
}
```

## 3.5 Classical Scattering

### Two-Particle System

The Lagrangian for a general two-body system:

$$L = \frac{m_1 v_1^2}{2} + \frac{m_2 v_2^2}{2} - V(r_1, r_2) \tag{3.56}$$

Coordinate transformation:

$$\mathbf{r} = \mathbf{r}_2 - \mathbf{r}_1 \tag{3.57}$$
$$\mathbf{r}_c = \frac{m_1 \mathbf{r}_1 + m_2 \mathbf{r}_2}{m_1 + m_2} \tag{3.58}$$

In center-of-mass coordinates with $v_c = d\mathbf{r}_c/dt = 0$:

$$L = \frac{M v_c^2}{2} + \frac{m v^2}{2} - V(r) \tag{3.59}$$

where $M = m_1 + m_2$ is the total mass and $m = m_1 m_2/(m_1 + m_2)$ is the reduced mass.

### Cross Section of Scattering

The total cross section:

$$\sigma = \int \sigma(\theta) d\Omega \tag{3.64}$$

where $\sigma(\theta)$ is the differential cross section:

$$\sigma(\theta) = \frac{b}{\sin\theta}\left|\frac{db}{d\theta}\right| \tag{3.66}$$

### Numerical Evaluation

Conservation laws:

$$l = mbv_0 = mr^2\dot{\phi} \tag{3.67}$$
$$E = \frac{mv_0^2}{2} = \frac{m(\dot{r}^2 + r^2\dot{\phi}^2)}{2} + V(r) \tag{3.68}$$

Relation between $\phi$ and $r$:

$$\frac{d\phi}{dr} = \pm \frac{b}{r^2\sqrt{1 - b^2/r^2 - V(r)/E}} \tag{3.70}$$

Deflection angle:

$$\theta = \pi - 2\Delta\phi \tag{3.71}$$

where:

$$\Delta\phi = b\int_{r_m}^{\infty} \frac{dr}{r^2\sqrt{1 - b^2/r^2 - V(r)/E}} \tag{3.72}$$

The minimum distance $r_m$ is given by:

$$1 - \frac{b^2}{r_m^2} - \frac{V(r_m)}{E} = 0 \tag{3.73}$$

### Yukawa Potential

$$V(r) = \frac{\kappa}{r}e^{-r/a} \tag{3.75}$$

For Coulomb scattering ($a \to \infty$), the Rutherford formula:

$$\sigma(\theta) = \left(\frac{\kappa}{4E}\right)^2 \frac{1}{\sin^4(\theta/2)} \tag{3.76}$$

**Java Implementation:**

```java
// An example of calculating the differential cross section
// of classical scattering on the Yukawa potential.
import java.lang.*;

public class Collide {
    static final int n = 10000, m = 20;
    static final double a = 100, e = 1;
    static double b;
    
    public static void main(String argv[]) {
        int nc = 20, ne = 2;
        double del = 1e-6, db = 0.5, b0 = 0.01, h = 0.01;
        double theta[] = new double[n+1];
        double fi[] = new double[n+1];
        double sig[] = new double[m+1];
        
        for (int i=0; i<=m; ++i) {
            b = b0 + i*db;
            // Calculate the first term of theta
            for (int j=0; j<=n; ++j) {
                double r = b + h*(j+1);
                fi[j] = 1/(r*r*Math.sqrt(fb(r)));
            }
            double g1 = simpson(fi, h);
            // Find r_m from 1-b*b/(r*r)-V/E = 0
            double rm = secant(nc, del, b, h);
            // Calculate the second term of theta
            for (int j=0; j<=n; ++j) {
                double r = rm + h*(j+1);
                fi[j] = 1/(r*r*Math.sqrt(f(r)));
            }
            double g2 = simpson(fi, h);
            theta[i] = 2*b*(g1-g2);
        }
        // Calculate d theta/db
        sig = firstOrderDerivative(db, theta, ne);
        // Output results
        for (int i=m; i>=0; --i) {
            b = b0 + i*db;
            sig[i] = b/(Math.abs(sig[i])*Math.sin(theta[i]));
            double ruth = 1/Math.pow(Math.sin(theta[i]/2), 4)/16;
            double si = Math.log(sig[i]);
            double ru = Math.log(ruth);
            System.out.println("theta = " + theta[i]);
            System.out.println("ln sigma(theta) = " + si);
            System.out.println("ln sigma_r(theta) = " + ru);
        }
    }
    
    public static double f(double x) {
        return 1 - b*b/(x*x) - Math.exp(-x/a)/(x*e);
    }
    
    public static double fb(double x) {
        return 1 - b*b/(x*x);
    }
}
```

## Exercises

3.1 Write a program that obtains the first-order and second-order derivatives from the five-point formulas. Check its accuracy with $f(x) = \cos x \sinh x$.

3.2 Show that derivatives can be obtained by interpolation followed by differentiation of the interpolation polynomial.

3.3 The Richardson extrapolation: Starting from $A_{k0} = \Delta_1(h/2^k)$, show that:
$$A_{kl} = \frac{4^l A_{kl-1} - A_{k-1,l-1}}{4^l - 1}$$

3.4 Repeat Exercise 3.3 with $\Delta_2(h)$ for second-order derivative.

3.5 Construct an adaptive subprogram for second-order derivative using $\Delta_2(h) - 4\Delta_2(h/2) = -3f''(x) + O(h^4)$.

3.6 Derive the Simpson rule with a pair of slices using Taylor expansion.

3.7 Derive the Simpson rule with $f(x) = ax^2 + bx + c$ going through points $x_{i-1}, x_i, x_{i+1}$.

3.8 Develop a program for Simpson rule with nonuniform data points.

3.9 Show that for trapezoid rule: $\delta S_0 = S - S_0 \approx -\frac{h^3}{12}f''(a)$ and develop an adaptive trapezoid evaluation.

3.10 The Romberg algorithm: Show that $\lim_{k \to \infty} S_{kl} = S = \int_a^b f(x)dx$.

3.11 Apply the secant method to solve $e^{x^2}\ln x^2 - x = 0$.

3.12 Develop a Newton method subprogram for multivariable case.

3.13 Write a routine that returns the minimum of a single-variable function $g(x)$ in $[a,b]$.

3.14 Use steepest-descent method to obtain stable geometric structures of ion clusters $(Na^+)_n(Cl^-)_m$.

3.15 Modify the program to evaluate differential cross section for Lennard-Jones potential:
$$V(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

3.16 Show that the period of a pendulum is:
$$T = 4\sqrt{\frac{\ell}{2g}} \int_0^{\theta_0} \frac{d\theta}{\sqrt{\cos\theta - \cos\theta_0}}$$

3.17 Show that the time for a meter stick to fall on a frictionless surface is:
$$t = \sqrt{\frac{\ell}{3g\sin\theta_0}} \int_0^{\theta_0} \sqrt{\frac{1+3\cos^2\phi}{\sin\theta_0 - \sin\phi}} d\phi$$

3.18 For a classical particle in a symmetric potential well $U(x) = U(-x)$, show that:
$$x(U) = \frac{1}{\pi\sqrt{2m}} \int_0^U \frac{T(E)dE}{\sqrt{U-E}}$$
