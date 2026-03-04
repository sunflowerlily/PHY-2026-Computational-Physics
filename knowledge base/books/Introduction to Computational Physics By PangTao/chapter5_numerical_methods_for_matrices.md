# Chapter 5: Numerical Methods for Matrices

Matrix operations are involved in many numerical and analytical scientific problems. Schemes developed for the matrix problems can be applied to the related problems encountered in ordinary and partial differential equations.

## 5.1 Matrices in Physics

Many problems in physics can be formulated in a matrix form. Here we give a few examples to illustrate the importance of matrix operations in physics and related fields.

### Molecular Vibrations

If we want to study the vibrational spectrum of a molecule with $n$ vibrational degrees of freedom, we expand the potential energy up to the second order:

$$U(q_1, q_2, ..., q_n) \approx \frac{1}{2}\sum_{i,j=1}^{n} A_{ij} q_i q_j \tag{5.1}$$

The kinetic energy:

$$T(\dot{q}_1, \dot{q}_2, ..., \dot{q}_n) \approx \frac{1}{2}\sum_{i,j=1}^{n} M_{ij} \dot{q}_i \dot{q}_j \tag{5.2}$$

From the Lagrange equation, we obtain:

$$\sum_{j=1}^{n} (A_{ij} q_j + M_{ij} \ddot{q}_j) = 0 \tag{5.4}$$

Assuming oscillatory time dependence $q_j = x_j e^{-i\omega t}$:

$$\mathbf{A}\mathbf{x} = \lambda \mathbf{M}\mathbf{x} \tag{5.8}$$

where $\lambda = \omega^2$ is the eigenvalue.

### Wheatstone Bridge

The unbalanced Wheatstone bridge circuit equations:

$$\mathbf{R}\mathbf{i} = \mathbf{v} \tag{5.13}$$

where the resistance matrix:

$$\mathbf{R} = \begin{pmatrix} r_s & r_1 & r_2 \\ -r_x & r_1 + r_x + r_a & -r_a \\ -r_3 & -r_a & r_2 + r_3 + r_a \end{pmatrix} \tag{5.14}$$

### Electronic Structure of H₃⁺

The Hubbard model Hamiltonian:

$$H = -t\sum_{i\sigma} \sum_{j \neq i} a_{i\sigma}^\dagger a_{j\sigma} + U\sum_i n_{i\uparrow} n_{i\downarrow} \tag{5.17}$$

The Schrödinger equation:

$$H|\Psi_k\rangle = E_k |\Psi_k\rangle \tag{5.18}$$

## 5.2 Basic Matrix Operations

An $n \times m$ matrix $\mathbf{A}$ is defined through its elements $A_{ij}$ with row index $i = 1, 2, ..., n$ and column index $j = 1, 2, ..., m$.

A typical set of linear algebraic equations:

$$\sum_{j=1}^{n} A_{ij} x_j = b_i \tag{5.22}$$

or in matrix form:

$$\mathbf{A}\mathbf{x} = \mathbf{b} \tag{5.23}$$

### Key Definitions

**Matrix multiplication:**

$$C_{ij} = \sum_k A_{ik} B_{kj} \tag{5.24}$$

**Inverse matrix:**

$$\mathbf{A}^{-1}\mathbf{A} = \mathbf{A}\mathbf{A}^{-1} = \mathbf{I} \tag{5.25}$$

**Determinant:**

$$|\mathbf{A}| = \sum_{i=1}^{n} (-1)^{i+j} A_{ij} |R_{ij}| \tag{5.26}$$

**Trace:**

$$\text{Tr}\mathbf{A} = \sum_{i=1}^{n} A_{ii} \tag{5.28}$$

**Transpose:**

$$\mathbf{A}^T_{ij} = A_{ji} \tag{5.29}$$

**Hermitian:** $\mathbf{A}^\dagger = \mathbf{A}$ where $\mathbf{A}^\dagger_{ij} = A^*_{ji}$

**Unitary:** $\mathbf{A}^\dagger = \mathbf{A}^{-1}$

**Eigenvalue problem:**

$$\mathbf{A}\mathbf{x} = \lambda\mathbf{x} \tag{5.32}$$

**Similarity transformation:**

$$\mathbf{B} = \mathbf{S}^{-1}\mathbf{A}\mathbf{S} \tag{5.34}$$

## 5.3 Linear Equation Systems

### Gaussian Elimination

The basic idea of Gaussian elimination is to transform the original linear equation set to one that has an upper-triangular or lower-triangular coefficient matrix.

**Partial Pivoting:** Search for the pivoting element with the largest magnitude from the remaining elements of the given column.

**Java Implementation:**

```java
// Method to carry out the partial-pivoting Gaussian elimination.
// Here index[] stores pivoting order.
public static void gaussian(double a[][], int index[]) {
    int n = index.length;
    double c[] = new double[n];
    
    // Initialize the index
    for (int i=0; i<n; ++i) index[i] = i;
    
    // Find the rescaling factors, one from each row
    for (int i=0; i<n; ++i) {
        double c1 = 0;
        for (int j=0; j<n; ++j) {
            double c0 = Math.abs(a[i][j]);
            if (c0 > c1) c1 = c0;
        }
        c[i] = c1;
    }
    
    // Search for the pivoting element from each column
    int k = 0;
    for (int j=0; j<n-1; ++j) {
        double pi1 = 0;
        for (int i=j; i<n; ++i) {
            double pi0 = Math.abs(a[index[i]][j]);
            pi0 /= c[index[i]];
            if (pi0 > pi1) {
                pi1 = pi0;
                k = i;
            }
        }
        // Interchange rows according to the pivoting order
        int itmp = index[j];
        index[j] = index[k];
        index[k] = itmp;
        
        for (int i=j+1; i<n; ++i) {
            double pj = a[index[i]][j]/a[index[j]][j];
            // Record pivoting ratios below the diagonal
            a[index[i]][j] = pj;
            // Modify other elements accordingly
            for (int l=j+1; l<n; ++l)
                a[index[i]][l] -= pj*a[index[j]][l];
        }
    }
}
```

### Determinant

The determinant of the original matrix can be obtained after transforming it into an upper-triangular matrix:

$$|\mathbf{A}| = \prod_{i=1}^{n} U_{ii} \tag{5.47}$$

### Solution of Linear Equation Set

After Gaussian elimination, solve by backward substitution:

$$x_i = \frac{1}{A^{(n-1)}_{ii}}\left[b^{(n-1)}_i - \sum_{j=i+1}^{n} A^{(n-1)}_{ij} x_j\right] \tag{5.40}$$

### LU Decomposition

A scheme related to Gaussian elimination splits a nonsingular matrix into:

$$\mathbf{A} = \mathbf{L}\mathbf{U} \tag{5.44}$$

where $\mathbf{L}$ is lower-triangular and $\mathbf{U}$ is upper-triangular.

**Doolittle factorization:** $L_{ii} = 1$

**Crout factorization:** $U_{ii} = 1$

The elements are obtained from:

$$L_{ij} = \frac{1}{U_{jj}}\left(A_{ij} - \sum_{k=1}^{j-1} L_{ik} U_{kj}\right) \tag{5.45}$$

$$U_{ij} = \frac{1}{L_{ii}}\left(A_{ij} - \sum_{k=1}^{i-1} L_{ik} U_{kj}\right) \tag{5.46}$$

## 5.4 Zeros and Extremes of Multivariable Functions

### Multivariable Newton Method

For a set of multivariable equations $\mathbf{f}(\mathbf{x}) = 0$:

$$\mathbf{f}(\mathbf{x}) \approx \mathbf{f}(\mathbf{x}_r) + \Delta\mathbf{x} \cdot \nabla\mathbf{f}(\mathbf{x}_r) = 0 \tag{5.53}$$

In matrix form:

$$\mathbf{A}\Delta\mathbf{x} = \mathbf{b} \tag{5.54}$$

where:

$$A_{ij} = \frac{\partial f_i}{\partial x_j} \tag{5.55}$$
$$b_i = -f_i$$

The Newton method:

$$\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta\mathbf{x}_k \tag{5.56}$$

### BFGS Optimization Scheme

For finding minima of multivariable function $g(\mathbf{x})$:

$$\mathbf{A}_k = \mathbf{A}_{k-1} + \frac{\mathbf{y}\mathbf{y}^T}{\mathbf{y}^T\mathbf{w}} - \frac{\mathbf{A}_{k-1}\mathbf{w}\mathbf{w}^T\mathbf{A}_{k-1}}{\mathbf{w}^T\mathbf{A}_{k-1}\mathbf{w}} \tag{5.61}$$

where:

$$\mathbf{w} = \mathbf{x}_k - \mathbf{x}_{k-1} \tag{5.62}$$
$$\mathbf{y} = \mathbf{f}_k - \mathbf{f}_{k-1} \tag{5.63}$$

### Geometric Structures of Multicharge Clusters

The interaction potential between two ions in NaCl crystal:

$$V(r_{ij}) = \frac{\eta_{ij}e^2}{4\pi\varepsilon_0 r_{ij}} + \delta_{ij}V_0 e^{-r_{ij}/r_0} \tag{5.64}$$

where $\eta_{ij} = -1$ and $\delta_{ij} = 1$ for opposite charges; otherwise $\eta_{ij} = 1$ and $\delta_{ij} = 0$.

## 5.5 Eigenvalue Problems

### Hermitian Matrix Eigenvalue Problem

$$\mathbf{A}\mathbf{x} = \lambda\mathbf{x} \tag{5.66}$$

The secular equation:

$$|\mathbf{A} - \lambda\mathbf{I}| = 0 \tag{5.67}$$

**Properties of Hermitian matrices:**
1. All eigenvalues are real
2. Eigenvectors can be made orthonormal
3. Can be transformed into a diagonal matrix under unitary transformation

### Householder Method

Tridiagonalization is achieved with $n-2$ consecutive transformations:

$$\mathbf{A}^{(k)} = \mathbf{O}_k^T \mathbf{A}^{(k-1)} \mathbf{O}_k \tag{5.74}$$

where:

$$\mathbf{O}_k = \mathbf{I} - \frac{1}{\eta_k}\mathbf{w}_k\mathbf{w}_k^T \tag{5.75}$$

$$w_{kl} = \begin{cases} 0 & \text{for } l \leq k \\ A^{(k-1)}_{k,k+1} + \alpha_k & \text{for } l = k+1 \\ A^{(k-1)}_{kl} & \text{for } l \geq k+2 \end{cases} \tag{5.76}$$

$$\alpha_k = \pm\sqrt{\sum_{l=k+1}^{n} [A^{(k-1)}_{kl}]^2} \tag{5.77}$$

$$\eta_k = \alpha_k(\alpha_k + A^{(k-1)}_{k,k+1}) \tag{5.78}$$

### Determinant Polynomial Recursion

For a symmetric tridiagonal matrix:

$$p_i(\lambda) = (a_i - \lambda)p_{i-1}(\lambda) - b_{i-1}^2 p_{i-2}(\lambda) \tag{5.79}$$

**Properties:**
1. All roots lie in $[-||\mathbf{A}||, ||\mathbf{A}||]$
2. Number of roots with $\lambda \geq \lambda_0$ equals the number of sign agreements

### Inverse Iteration Method

For general nondefective matrices:

$$\mathbf{x}^{(k)} = \frac{1}{N_k}(\mathbf{A} - \mu\mathbf{I})^{-1}\mathbf{x}^{(k-1)} \tag{5.85}$$

The eigenvalue is obtained from:

$$\lambda_j = \mu + \lim_{k \to \infty} \frac{1}{N_k} \frac{x_l^{(k-1)}}{x_l^{(k)}} \tag{5.90}$$

### QR Algorithm

Split matrix into:

$$\mathbf{A} = \mathbf{Q}\mathbf{R} \tag{5.101}$$

Then construct similarity transformations:

$$\mathbf{A}^{(k+1)} = \mathbf{R}_k\mathbf{Q}_k = \mathbf{Q}_k^\dagger \mathbf{A}^{(k)}\mathbf{Q}_k \tag{5.103}$$

## 5.6 The Faddeev-Leverrier Method

The characteristic polynomial:

$$p_n(\lambda) = |\mathbf{A} - \lambda\mathbf{I}| = \sum_{k=0}^{n} c_k \lambda^k \tag{5.106}$$

Supplementary matrices $\mathbf{S}_k$:

$$p_n(\lambda)(\lambda\mathbf{I} - \mathbf{A})^{-1} = \sum_{k=0}^{n-1} \lambda^{n-k-1}\mathbf{S}_k \tag{5.107}$$

Recursion relations:

$$c_{n-k} = -\frac{1}{k}\text{Tr}(\mathbf{A}\mathbf{S}_{k-1}) \tag{5.109}$$
$$\mathbf{S}_k = \mathbf{A}\mathbf{S}_{k-1} + c_{n-k}\mathbf{I} \tag{5.110}$$

The inverse matrix:

$$\mathbf{A}^{-1} = -\frac{1}{c_0}\mathbf{S}_{n-1} \tag{5.112}$$

## 5.7 Complex Zeros of a Polynomial

For a polynomial:

$$p_n(z) = \sum_{k=0}^{n} c_k z^k \tag{5.115}$$

### Evaluation of Polynomial

$$p_n(z) = u_n(x,y) + iv_n(x,y) \tag{5.118}$$

Recursion:

$$u_k = c_{n-k} + xu_{k-1} - yv_{k-1} \tag{5.119}$$
$$v_k = xv_{k-1} + yu_{k-1} \tag{5.120}$$

### Routh-Hurwitz Test

Construct an $(n+1) \times m$ matrix with:

$$B_{ij} = \frac{B_{i+1,1}B_{i+1,j+1} - B_{i+2,1}B_{i+1,j+1}}{B_{i+1,1}} \tag{5.128}$$

The number of sign agreements between $B_{i1}$ and $B_{i+1,1}$ gives the number of zeros on the right-hand side of the imaginary axis.

## 5.8 Electronic Structures of Atoms

The Schrödinger equation for a multielectron atom:

$$H\Psi_k(\mathbf{R}) = E_k \Psi_k(\mathbf{R}) \tag{5.131}$$

where:

$$H = -\frac{\hbar^2}{2m_e}\sum_{i=1}^{N}\nabla_i^2 - \sum_{i=1}^{N}\frac{Ze^2}{4\pi\varepsilon_0 r_i} + \sum_{i>j}\frac{e^2}{4\pi\varepsilon_0 |\mathbf{r}_i - \mathbf{r}_j|} \tag{5.132}$$

The Hartree-Fock equation:

$$\left[-\frac{1}{2}\nabla^2 - \frac{Z}{r} + V_H(\mathbf{r})\right]\phi_{i\sigma}(\mathbf{r}) - \int V_{x\sigma}(\mathbf{r}', \mathbf{r})\phi_{i\sigma}(\mathbf{r}')d\mathbf{r}' = \varepsilon_i \phi_{i\sigma}(\mathbf{r}) \tag{5.135}$$

where $V_H$ is the Hartree potential and $V_{x\sigma}$ is the exchange interaction.

## 5.9 The Lanczos Algorithm and the Many-Body Problem

Tridiagonalize an $m \times m$ subset of $\mathbf{H}$:

$$\mathbf{O}^T\mathbf{H}\mathbf{O} = \tilde{\mathbf{H}} \tag{5.144}$$

where the $k$th column of $\mathbf{O}$ is:

$$\mathbf{v}_k = \frac{\mathbf{u}_k}{N_k} \tag{5.145}$$

Vectors $\mathbf{u}_k$ are generated recursively:

$$\mathbf{u}_{k+1} = \mathbf{H}\mathbf{v}_k - \alpha_k\mathbf{v}_k - \beta_k\mathbf{v}_{k-1} \tag{5.146}$$

where:

$$\beta_k = \tilde{H}_{k-1,k} = \mathbf{v}_{k-1}^T\mathbf{H}\mathbf{v}_k$$
$$\alpha_k = \tilde{H}_{kk} = \mathbf{v}_k^T\mathbf{H}\mathbf{v}_k$$

### Dagotto-Moreo Iteration Scheme

$$\mathbf{v}_1^{(l+1)} = \frac{1}{\sqrt{1+a^2}}(\mathbf{v}_1^{(l)} + a\mathbf{v}_2^{(l)}) \tag{5.151}$$

where:

$$a = b - \sqrt{1+b^2} \tag{5.152}$$
$$b = \frac{-3d_3 + 2d_1^3}{2(d_2 - d_1^2)^{3/2}} \tag{5.153}$$

with $d_1 = \mathbf{v}_1^T\mathbf{H}\mathbf{v}_1$, $d_2 = \mathbf{v}_1^T\mathbf{H}^2\mathbf{v}_1$, $d_3 = \mathbf{v}_1^T\mathbf{H}^3\mathbf{v}_1$.

## 5.10 Random Matrices

The Gaussian orthogonal ensemble distribution:

$$W_n(\mathbf{H}) = e^{-\text{Tr}\mathbf{H}^2/4\sigma^2} \tag{5.158}$$

where:

$$\text{Tr}\mathbf{H}^2 = \sum_{i=1}^{n} H_{ii}^2 + \sum_{i \neq j} H_{ij}^2 \tag{5.159}$$

**Wigner semicircle distribution:**

$$\rho(\lambda) = \begin{cases} \frac{1}{2\pi}\sqrt{4-\lambda^2} & \text{if } |\lambda| < 2 \\ 0 & \text{elsewhere} \end{cases} \tag{5.160}$$

**Java Implementation:**

```java
// Method to generate a random matrix for the Gaussian
// orthogonal ensemble with sigma being the standard
// deviation of the off-diagonal elements.
import java.util.Random;

public static double[][] rm(int n, double sigma) {
    double a[][] = new double[n][n];
    double sigmad = Math.sqrt(2)*sigma;
    Random r = new Random();
    for (int i=0; i<n; ++i)
        a[i][i] = sigmad*r.nextGaussian();
    for (int i=0; i<n; ++i) {
        for (int j=0; j<i; ++j) {
            a[i][j] = sigma*r.nextGaussian();
            a[j][i] = a[i][j];
        }
    }
    return a;
}
```

## Exercises

5.1 Find the currents in the unbalanced Wheatstone bridge.

5.2 Hultén's study of the one-dimensional spin-1/2 Heisenberg model: Find $\varepsilon_\infty$ by solving the linear equation set numerically.

5.3 Write a subprogram for least-squares approximation with polynomials.

5.4 Develop a subprogram for LU decomposition of banded matrices.

5.5 Apply the secant method to obtain stable geometric structures of ion clusters $(Na^+)_n(Cl^-)_m$.

5.6 Implement the BFGS optimization scheme for $(NaCl)_5$.

5.7 Write a subprogram using the Householder scheme to tridiagonalize a real symmetric matrix.

5.8 Write a subprogram using determinant polynomials and root search for eigenvalues of tridiagonal matrices.

5.9 Solve the one-dimensional Schrödinger equation by the inverse iteration method.

5.10 Find all 15×15 elements of the Hamiltonian for H₃⁺ and solve numerically.

5.11 Find all vibrational modes of Na₂Cl₂.

5.12 Implement the Faddeev-Leverrier method for inverse, eigenvalues, and eigenvectors.

5.13 Derive the Bairstow method for factoring polynomials.

5.14 Combine Routh-Hurwitz test and bisection method to locate all zeros of a polynomial.

5.15 Derive the Hartree-Fock equation for atomic systems.

5.16 Generate and diagonalize ensembles of real symmetric matrices with various distributions.

5.17 Find optimized configurations of N < 20 charges on a unit sphere.

5.18 Find optimized configurations of N < 20 particles interacting through Lennard-Jones potential.
