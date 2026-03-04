# Chapter 2: Approximation of a Function

This chapter and the next examine the most commonly used methods in computational science. Here we concentrate on some basic aspects associated with numerical approximation of a function, interpolation, least-squares and spline approximations of a curve, and numerical representations of uniform and other distribution functions.

## 2.1 Interpolation

In numerical analysis, the results obtained from computations are always approximations of the desired quantities and in most cases are within some uncertainties. This is similar to experimental observations in physics. Every single physical quantity measured carries some experimental error.

Interpolation is needed when we want to infer some local information from a set of incomplete or discrete data. Overall approximation or fitting is needed when we want to know the general or global behavior of the data.

### Linear Interpolation

Consider a discrete data set given from a discrete function $f_i = f(x_i)$ with $i = 0, 1, ..., n$. The simplest way to obtain the approximation of $f(x)$ for $x \in [x_i, x_{i+1}]$ is to construct a straight line between $x_i$ and $x_{i+1}$. Then $f(x)$ is given by:

$$f(x) = f_i + \frac{(f_{i+1} - f_i)(x - x_i)}{x_{i+1} - x_i} + \delta f(x) \tag{2.1}$$

The error $\delta f(x)$ in the linear interpolation is given by:

$$\delta f(x) = \frac{\gamma}{2}(x - x_i)(x - x_{i+1}) \tag{2.2}$$

with $\gamma$ being a parameter determined by the specific form of $f(x)$. If we draw a quadratic curve passing through $f(x_i)$, $f(a)$, and $f(x_{i+1})$, we can show that:

$$\gamma = f''(a) \tag{2.3}$$

with $a \in [x_i, x_{i+1}]$, as long as $f(x)$ is a smooth function in the region $[x_i, x_{i+1}]$; namely, the $k$th-order derivative $f^{(k)}(x)$ exists for any $k$. The maximum error in the linear interpolation is then bounded by:

$$|\delta f(x)| \leq \frac{\gamma_1}{8}(x_{i+1} - x_i)^2 \tag{2.4}$$

where $\gamma_1 = \max[|f''(x)|]$ with $x \in [x_i, x_{i+1}]$.

**Example:** Let us take $f(x) = \sin x$ as an illustrative example. Assuming that $x_i = \pi/4$ and $x_{i+1} = \pi/2$, we have $f_i = 0.707$ and $f_{i+1} = 1.000$. If we use the linear interpolation scheme to find the approximate value of $f(x)$ at $x = 3\pi/8$, we have the interpolated value $f(3\pi/8) \approx 0.854$ from Eq. (2.1). We know that $f(3\pi/8) = \sin(3\pi/8) = 0.924$. The actual difference is $|\delta f(x)| = 0.070$, which is smaller than the maximum error estimated with Eq. (2.4), 0.077.

### The Lagrange Interpolation

The linear interpolation can be generalized to an $n$th-order curve that passes through all the $n+1$ data points:

$$f(x) = \sum_{j=0}^{n} f_j p_{nj}(x) + \delta f(x) \tag{2.7}$$

where $p_{nj}(x)$ is given by:

$$p_{nj}(x) = \prod_{k \neq j}^{n} \frac{x - x_k}{x_j - x_k} \tag{2.8}$$

In other words, $\delta f(x_j) = 0$ at all the data points. The error in the $n$th-order Lagrange interpolation is given by:

$$\delta f(x) = \frac{\gamma}{(n+1)!}(x - x_0)(x - x_1) \cdots (x - x_n) \tag{2.9}$$

where:

$$\gamma = f^{(n+1)}(a) \tag{2.10}$$

with $a \in [x_0, x_n]$. The maximum error is bounded by:

$$|\delta f(x)| \leq \frac{\gamma_n}{4(n+1)} h^{n+1} \tag{2.11}$$

where $\gamma_n = \max[|f^{(n+1)}(x)|]$ with $x \in [x_0, x_n]$ and $h$ is the largest $h_i = x_{i+1} - x_i$.

### The Aitken Method

One way to achieve the Lagrange interpolation efficiently is by performing a sequence of linear interpolations. This scheme was first developed by Aitken (1932). We can first work out $n$ linear interpolations with each constructed from a neighboring pair of the $n+1$ data points. Then we can use these $n$ interpolated data points to achieve another level of $n-1$ linear interpolations with the next neighboring points of $x_i$. We repeat this process until we obtain the final result after $n$ levels of consecutive linear interpolations:

$$f_{i \cdots j} = \frac{x - x_j}{x_i - x_j} f_{i \cdots j-1} + \frac{x - x_i}{x_j - x_i} f_{i+1 \cdots j} \tag{2.13}$$

with $f_i = f(x_i)$ to start.

**Example:** Consider the evaluation of $f(0.9)$ from the given set $f(0.0) = 1.000000$, $f(0.5) = 0.938470$, $f(1.0) = 0.765198$, $f(1.5) = 0.511828$, and $f(2.0) = 0.223891$. These are the values of the zeroth-order Bessel function of the first kind, $J_0(x)$.

| $x_i$ | $f_i$ | $f_{ij}$ | $f_{ijk}$ | $f_{ijkl}$ | $f_{ijklm}$ |
|-------|-------|----------|-----------|------------|-------------|
| 0.0 | 1.000000 | | | | |
| | | 0.889246 | | | |
| 0.5 | 0.938470 | | 0.808792 | | |
| | | 0.799852 | | 0.807272 | |
| 1.0 | 0.765198 | | 0.806260 | | 0.807473 |
| | | 0.815872 | | 0.807717 | |
| 1.5 | 0.511828 | | 0.811725 | | |
| | | 0.857352 | | | |
| 2.0 | 0.223891 | | | | |

The error estimated from the differences of the last two columns is:

$$\delta f(x) \approx \frac{|0.807473 - 0.807273| + |0.807473 - 0.807717|}{2} \approx 2 \times 10^{-4}$$

The exact result of $f(0.9)$ is 0.807524. The error in the interpolated value is $|0.807473 - 0.807524| \approx 5 \times 10^{-5}$.

**Java Implementation:**

```java
// An example of extracting an approximate function
// value via the Lagrange interpolation scheme.
import java.lang.*;

public class Lagrange {
    public static void main(String argv[]) {
        double xi[] = {0, 0.5, 1, 1.5, 2};
        double fi[] = {1, 0.938470, 0.765198, 0.511828, 0.223891};
        double x = 0.9;
        double f = aitken(x, xi, fi);
        System.out.println("Interpolated value: " + f);
    }
    
    // Method to carry out the Aitken recursions.
    public static double aitken(double x, double xi[], double fi[]) {
        int n = xi.length-1;
        double ft[] = (double[]) fi.clone();
        for (int i=0; i<n; ++i) {
            for (int j=0; j<n-i; ++j) {
                ft[j] = (x-xi[j])/(xi[i+j+1]-xi[j])*ft[j+1]
                      + (x-xi[i+j+1])/(xi[j]-xi[i+j+1])*ft[j];
            }
        }
        return ft[0];
    }
}
```

### The Up-and-Down Method

A better way is to construct an indirect scheme that improves the interpolated value at every step by updating the differences of the interpolated values from the adjacent columns:

$$\Delta^+_{ij} = f_{j \cdots j+i} - f_{j+1 \cdots j+i} \tag{2.17}$$
$$\Delta^-_{ij} = f_{j \cdots j+i} - f_{j \cdots j+i-1} \tag{2.18}$$

where $\Delta^-_{ij}$ is the downward correction and $\Delta^+_{ij}$ is the upward correction. They satisfy the following recursion relations:

$$\Delta^+_{ij} = \frac{x_{i+j} - x}{x_{i+j} - x_j}(\Delta^+_{i-1,j} - \Delta^-_{i-1,j+1}) \tag{2.19}$$
$$\Delta^-_{ij} = \frac{x - x_j}{x_{i+j} - x_j}(\Delta^+_{i-1,j} - \Delta^-_{i-1,j+1}) \tag{2.20}$$

with the starting column $\Delta^\pm_{0j} = f_j$.

## 2.2 Least-Squares Approximation

The most common approximation scheme is based on the least squares of the differences between the approximation $p_m(x)$ and the data $f(x)$. If $f(x)$ is the data function to be approximated in the region $[a, b]$ and the approximation is an $m$th-order polynomial:

$$p_m(x) = \sum_{k=0}^{m} a_k x^k \tag{2.21}$$

we can construct a function:

$$\chi^2[a_k] = \int_a^b [p_m(x) - f(x)]^2 dx \tag{2.22}$$

for the continuous data function $f(x)$, and:

$$\chi^2[a_k] = \sum_{i=0}^{n} [p_m(x_i) - f(x_i)]^2 \tag{2.23}$$

for the discrete data function $f(x_i)$ with $i = 0, 1, ..., n$.

The least-squares approximation is obtained with $\chi^2[a_k]$ minimized with respect to all the $m+1$ coefficients through:

$$\frac{\partial \chi^2[a_k]}{\partial a_l} = 0 \tag{2.24}$$

for $l = 0, 1, 2, ..., m$.

### Linear Fit

For the special case with $m = 1$ (linear fit):

$$p_1(x) = a_0 + a_1 x \tag{2.25}$$

with:

$$\chi^2[a_k] = \sum_{i=0}^{n} (a_0 + a_1 x_i - f_i)^2 \tag{2.26}$$

From Eq. (2.24), we obtain:

$$(n+1)a_0 + c_1 a_1 - c_3 = 0 \tag{2.27}$$
$$c_1 a_0 + c_2 a_1 - c_4 = 0 \tag{2.28}$$

where $c_1 = \sum_{i=0}^{n} x_i$, $c_2 = \sum_{i=0}^{n} x_i^2$, $c_3 = \sum_{i=0}^{n} f_i$, and $c_4 = \sum_{i=0}^{n} x_i f_i$. Solving these two equations:

$$a_0 = \frac{c_1 c_4 - c_2 c_3}{c_1^2 - (n+1)c_2} \tag{2.29}$$
$$a_1 = \frac{c_1 c_3 - (n+1)c_4}{c_1^2 - (n+1)c_2} \tag{2.30}$$

### Orthogonal Polynomials

We can express the polynomial $p_m(x)$ in terms of a set of orthogonal polynomials:

$$p_m(x) = \sum_{k=0}^{m} \alpha_k u_k(x) \tag{2.31}$$

where $u_k(x)$ is a set of real orthogonal polynomials that satisfy:

$$\langle u_k | u_l \rangle = \int_a^b u_k(x) w(x) u_l(x) dx = \delta_{kl} N_k \tag{2.32}$$

with $w(x)$ being the weight. The orthogonal polynomials can be generated with the following recursion:

$$u_{k+1}(x) = (x - g_k) u_k(x) - h_k u_{k-1}(x) \tag{2.34}$$

where the coefficients $g_k$ and $h_k$ are given by:

$$g_k = \frac{\langle xu_k | u_k \rangle}{\langle u_k | u_k \rangle} \tag{2.35}$$
$$h_k = \frac{\langle xu_k | u_{k-1} \rangle}{\langle u_{k-1} | u_{k-1} \rangle} \tag{2.36}$$

with the starting $u_0(x) = 1$ and $h_0 = 0$.

The least-squares coefficients are:

$$\alpha_j = \frac{\langle u_j | f \rangle}{\langle u_j | u_j \rangle} \tag{2.39}$$

## 2.3 The Millikan Experiment

The data from Millikan's famous oil drop experiment is used here to illustrate the least-squares approximation. The measured charges $q_k$ (in units of $10^{-19}$ C) and the corresponding integers $k$ are:

| $k$ | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|------|------|------|------|------|------|------|------|
| $q_k$ | 6.558 | 8.206 | 9.880 | 11.50 | 13.14 | 14.82 | 16.40 | 18.04 |

| $k$ | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|-----|------|------|------|------|------|------|------|
| $q_k$ | 19.68 | 21.32 | 22.96 | 24.60 | 26.24 | 27.88 | 29.52 |

From the average charges of the oil drops, Millikan concluded that the fundamental charge is $e = 1.65 \times 10^{-19}$ C, which is very close to the currently accepted value $e = 1.60217733(49) \times 10^{-19}$ C.

We take the linear equation:

$$q_k = ke + \delta q_k \tag{2.40}$$

as the approximation of the measured data. The following program applies the least-squares approximation:

```java
// An example of applying the least-squares approximation
// to the Millikan data on a straight line q=k*e+dq.
import java.lang.*;

public class Millikan {
    public static void main(String argv[]) {
        double k[] = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18};
        double q[] = {6.558, 8.206, 9.880, 11.50, 13.14, 14.81, 16.40, 18.04,
                      19.68, 21.32, 22.96, 24.60, 26.24, 27.88, 29.52};
        int n = k.length-1;
        int m = 21;
        double u[][] = orthogonalPolynomialFit(m, k, q);
        
        double sum = 0;
        for (int i=0; i<=n; ++i) sum += k[i];
        double e = u[1][n+1];
        double dq = u[0][n+1] - u[1][n+1]*sum/(n+1);
        
        System.out.println("Fundamental charge: " + e);
        System.out.println("Estimated error: " + dq);
    }
    
    public static double[][] orthogonalPolynomialFit(int m, double x[], double f[]) {...}
}
```

After running the program, we obtain $e \approx 1.64 \times 10^{-19}$ C, and the intercept on the $y$ axis gives us a rough estimate of the error bar $|\delta e| \approx |\delta q| = 0.03 \times 10^{-19}$ C.

## 2.4 Spline Approximation

A spline interpolates the data locally through a polynomial and fits the data overall by connecting each segment of the interpolation polynomial by matching the function and its derivatives at the data points.

Assuming that we are trying to create a spline function that approximates a discrete data set $f_i = f(x_i)$ for $i = 0, 1, ..., n$, we can use an $m$th-order polynomial:

$$p_i(x) = \sum_{k=0}^{m} c_{ik} x^k \tag{2.41}$$

to approximate $f(x)$ for $x \in [x_i, x_{i+1}]$. The coefficients $c_{ik}$ are determined from the smoothness conditions at the non-boundary data points with the $l$th-order derivative there satisfying:

$$p_i^{(l)}(x_{i+1}) = p_{i+1}^{(l)}(x_{i+1}) \tag{2.42}$$

for $l = 0, 1, ..., m-1$.

### Cubic Spline

The most widely adopted spline function is the cubic spline with $m = 3$. The natural spline is given by the choices of $p_0''(x_0) = 0$ and $p_{n-1}''(x_n) = 0$.

To construct the cubic spline, we start with the linear interpolation of the second-order derivative in $[x_i, x_{i+1}]$:

$$p_i''(x) = \frac{1}{x_{i+1} - x_i} [(x - x_i)p_{i+1}'' - (x - x_{i+1})p_i''] \tag{2.43}$$

If we integrate the above equation twice and use $p_i(x_i) = f_i$ and $p_i(x_{i+1}) = f_{i+1}$, we obtain:

$$p_i(x) = \alpha_i(x - x_i)^3 + \beta_i(x - x_{i+1})^3 + \gamma_i(x - x_i) + \eta_i(x - x_{i+1}) \tag{2.44}$$

where:

$$\alpha_i = \frac{p_{i+1}''}{6h_i} \tag{2.45}$$
$$\beta_i = -\frac{p_i''}{6h_i} \tag{2.46}$$
$$\gamma_i = \frac{f_{i+1}}{h_i} - \frac{h_i p_{i+1}''}{6} \tag{2.47}$$
$$\eta_i = \frac{h_i p_i''}{6} - \frac{f_i}{h_i} \tag{2.48}$$

with $h_i = x_{i+1} - x_i$.

Applying the condition $p_{i-1}'(x_i) = p_i'(x_i)$ to the polynomial, we have:

$$h_{i-1} p_{i-1}'' + 2(h_{i-1} + h_i)p_i'' + h_i p_{i+1}'' = 6\left(\frac{g_i}{h_i} - \frac{g_{i-1}}{h_{i-1}}\right) \tag{2.50}$$

where $g_i = f_{i+1} - f_i$. This is a linear equation set with $n-1$ unknowns $p_i''$ for $i = 1, 2, ..., n-1$.

We can write the above equations in a matrix form:

$$A p'' = b \tag{2.52}$$

where $d_i = 2(h_{i-1} + h_i)$ and $b_i = 6(g_i/h_i - g_{i-1}/h_{i-1})$. The coefficient matrix $A$ is a real, symmetric, and tridiagonal matrix.

### LU Decomposition

We can decompose an $m \times m$ square matrix $A$ into a product of a lower-triangular matrix $L$ and an upper-triangular matrix $U$:

$$A = LU \tag{2.54}$$

For a tridiagonal matrix $A$:

$$A_{ij} = \begin{cases} d_i & \text{if } i = j \\ e_i & \text{if } i = j-1 \\ c_{i-1} & \text{if } i = j+1 \\ 0 & \text{otherwise} \end{cases} \tag{2.55}$$

the matrices $L$ and $U$ are:

$$L_{ij} = \begin{cases} w_i & \text{if } i = j \\ v_{i-1} & \text{if } i = j+1 \\ 0 & \text{otherwise} \end{cases} \tag{2.56}$$

$$U_{ij} = \begin{cases} 1 & \text{if } i = j \\ t_i & \text{if } i = j-1 \\ 0 & \text{otherwise} \end{cases} \tag{2.57}$$

The elements in $L$ and $U$ can be related to $d_i$, $c_i$, and $e_i$:

$$v_i = c_i \tag{2.58}$$
$$t_i = e_i/w_i \tag{2.59}$$
$$w_i = d_i - v_{i-1} t_{i-1} \tag{2.60}$$

with $w_1 = d_1$. The solution can be obtained by forward and backward substitutions:

$$y_i = (b_i - v_{i-1} y_{i-1})/w_i \tag{2.62}$$
$$z_i = y_i - t_i z_{i+1} \tag{2.63}$$

with $y_1 = b_1/w_1$ and $z_m = y_m$.

## 2.5 Random-Number Generators

In practice, many numerical simulations need random-number generators either for setting up initial configurations or for generating new configurations. There is no such thing as random in a computer program. A random-number generator here really means a pseudo-random-number generator that can generate a long sequence of numbers that can imitate a given distribution.

### Uniform Random-Number Generators

The three most important criteria for a good uniform random-number generator are:

1. **Long period**: Should be close to the range of the integers adopted
2. **Best randomness**: Very small correlation among all the numbers generated
3. **Speed**: Very fast execution

The simplest uniform random-number generator is built using the linear congruent scheme:

$$x_{i+1} = (ax_i + b) \mod c \tag{2.74}$$

One common choice: $a = 7^5 = 16807$, $b = 0$, and $c = 2^{31} - 1 = 2147483647$.

**Java Implementation (32-bit):**

```java
// Method to generate a uniform random number in [0,1]
// following x(i+1)=a*x(i) mod c with a=pow(7,5) and c=pow(2,31)-1.
public static double ranf() {
    final int a = 16807, c = 2147483647, q = 127773, r = 2836;
    final double cd = c;
    int h = seed/q;
    int l = seed%q;
    int t = a*l - r*h;
    if (t > 0) seed = t;
    else seed = c + t;
    return seed/cd;
}
```

**Java Implementation (64-bit):**

```java
// Method to generate a uniform random number in [0,1]
// following x(i+1)=a*x(i) mod c with a=pow(7,5) and c=pow(2,63)-1.
public static double ranl() {
    final long a = 16807L, c = 9223372036854775807L;
    final long q = 548781581296767L, r = 12838L;
    final double cd = c;
    long h = seed/q;
    long l = seed%q;
    long t = a*l - r*h;
    if (t > 0) seed = t;
    else seed = c + t;
    return seed/cd;
}
```

### Initial Seed from Current Time

To start the random-number generator differently every time:

$$i_s = t_6 + 70\{t_5 + 12[t_4 + 31(t_3 + 23(t_2 + 59t_1))]\} \tag{2.75}$$

where $t_1$ is the second of the minute, $t_2$ is the minute of the hour, $t_3$ is the hour of the day, $t_4$ is the day of the month, $t_5$ is the month of the year, and $t_6$ is the current year.

### Other Distributions

**Exponential Distribution:**

$$p(x) = e^{-x} \tag{2.76}$$

Relating to uniform distribution:

$$x = -\ln(1 - y) \tag{2.80}$$

```java
// Method to generate an exponential random number from a
// uniform random number in [0,1].
public static double rane() {
    return -Math.log(1-ranf());
}
```

**Gaussian Distribution:**

$$g(x) = \frac{1}{\sqrt{2\pi}\sigma} e^{-x^2/2\sigma^2} \tag{2.81}$$

Using the Box-Muller transform:

$$x = \sqrt{2t} \cos\phi \tag{2.84}$$
$$y = \sqrt{2t} \sin\phi \tag{2.85}$$

```java
// Method to create two Gaussian random numbers from two
// uniform random numbers in [0,1].
public static double[] rang() {
    double x[] = new double[2];
    double r1 = -Math.log(1-ranf());
    double r2 = 2*Math.PI*ranf();
    r1 = Math.sqrt(2*r1);
    x[0] = r1*Math.cos(r2);
    x[1] = r1*Math.sin(r2);
    return x;
}
```

### Percolation in Two Dimensions

The following method creates a 2-dimensional percolation lattice:

```java
// Method to create a 2-dimensional percolation lattice.
import java.util.Random;

public static boolean[][] lattice(double p, int n) {
    Random r = new Random();
    boolean y[][] = new boolean[n][n];
    for (int i=0; i<n; ++i) {
        for (int j=0; j<n; ++j) {
            if (p > r.nextDouble()) y[i][j] = true;
            else y[i][j] = false;
        }
    }
    return y;
}
```

## Exercises

2.1 Show that the error in the $n$th-order Lagrange interpolation scheme is bounded by:
$$|\delta f(x)| \leq \frac{\gamma_n}{4(n+1)} h^{n+1}$$
where $\gamma_n = \max[|f^{(n+1)}(x)|]$, for $x \in [x_0, x_n]$.

2.2 Write a program that implements the Lagrange interpolation scheme directly. Test it by evaluating $f(0.3)$ and $f(0.5)$ from the data taken from the error function with $f(0.0) = 0$, $f(0.4) = 0.428392$, $f(0.8) = 0.742101$, $f(1.2) = 0.910314$, and $f(1.6) = 0.970348$.

2.3 The Newton interpolation is another popular interpolation scheme that adopts the polynomial:
$$p_n(x) = \sum_{j=0}^{n} c_j \prod_{i=0}^{j-1} (x - x_i)$$
where $\prod_{i=0}^{-1}(x - x_i) = 1$. Show that this polynomial is equivalent to that of the Lagrange interpolation.

2.4 Show that the coefficients in the Newton interpolation can be cast into divided differences recursively.

2.5 The Newton interpolation can be used inversely to find approximate roots of an equation $f(x) = 0$.

2.6 Modify the program for the least-squares approximation to fit a data set from the Bessel function $J_0(3x)$.

2.7 Use the program that fits the Millikan data directly to a linear function to analyze the accuracy of the approximation.

2.8 For periodic functions, modify the cubic-spline program to have periodic boundary conditions.

2.9 Modify the cubic-spline program to have the LU decomposition carried out by the Doolittle factorization.

2.10 Use a fifth-order polynomial to create a quintic spline approximation.

2.11 Develop a computer program to implement B-splines of degree 3.

2.12 If we randomly drop a needle of unit length on an infinite plane covered by parallel lines one unit apart, derive the probability analytically.

2.13 Generate 21 pairs of random numbers and fit them to orthogonal polynomials.

2.14 Develop a scheme that can generate any distribution $w(x) > 0$ in a given region $[a, b]$.

2.15 Generate a large set of Gaussian random numbers and perform a least-squares fit.

2.16 Write a program that can generate clusters of occupied sites in a two-dimensional square lattice and determine the percolation threshold.
