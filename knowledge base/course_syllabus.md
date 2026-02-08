# Course Syllabus: Computational Physics with Astronomy Applications

## Course Philosophy
This course bridges the gap between theoretical physics and modern computational research.
**Core Philosophy**:
1.  **Vectorization**: Move from "C-style loops" to "NumPy array operations".
2.  **Data-Driven**: From classical fitting to modern AI discovery.
3.  **Open Science**: All work is managed via Git/GitHub.

## Weekly Schedule & Topics

### Module 1: Foundations & Numerical Calculus (Weeks 1-3)
*   **Week 1: Introduction & Tools**. Python ecosystem (Anaconda), Git/GitHub workflow, Floating point errors.
*   **Week 2: Interpolation & Calculus**.
    *   *Theory*: Lagrange Interpolation, Cubic Splines, Finite Differences.
    *   *Astro Application*: Resampling galaxy spectra (aligning wavelengths).
*   **Week 3: ODE Initial Value Problems I**. Euler method (stability issues), Runge-Kutta 4 (RK4) derivation.

### Module 2: Differential Equations & Dynamics (Weeks 4-9)
*   **Week 4: ODE Initial Value Problems II**. Symplectic Integrators (Verlet/Leapfrog).
    *   *Astro Application*: Long-term stability of planetary orbits (Energy conservation).
*   **Week 5: ODE Boundary Value Problems**. Shooting Method, Finite Difference method.
    *   *Astro Application*: Stellar Structure Equations (solving for density/pressure profiles).
*   **Week 6: Linear Algebra**. Gaussian Elimination, LU Decomposition, Eigenvalues.
    *   *Astro Application*: Coupled oscillators, Quantum eigenstates.
*   **Week 7: PDE - Parabolic**. Diffusion Equation, FTCS, Crank-Nicolson (stability analysis).
    *   *Astro Application*: Heat diffusion in asteroids.
*   **Week 8: PDE - Elliptic**. Poisson & Laplace Equations, Relaxation Method (SOR).
    *   *Astro Application*: Gravitational potential from mass distribution.
*   **Week 9: N-Body Simulations**. Particle-Mesh (PM) methods, Tree algorithms (Barnes-Hut concepts).
    *   *Astro Application*: Galaxy dynamics and dark matter halos.

### Module 3: Stochastic Processes & Signal Processing (Weeks 10-12)
*   **Week 10: Monte Carlo (Basics)**. RNG, Rejection Sampling, High-dimensional integration.
*   **Week 11: Random Walks & MCMC**. Diffusion, Metropolis-Hastings algorithm.
    *   *Astro Application*: Bayesian parameter estimation basics.
*   **Week 12: Fourier Analysis**. DFT, FFT algorithm, Power Spectrum.
    *   *Astro Application*: Pulsar search (Time series analysis), LIGO data processing.

### Module 4: Data Modeling & AI (Weeks 13-18)
*   **Week 13: Optimization & Model Fitting**.
    *   *Theory*: Least Squares, Chi-Squared ($\chi^2$) minimization, Non-linear fitting (Levenberg-Marquardt).
    *   *Astro Application*: Hubble's Law, Light curve fitting (Exoplanet transits).
*   **Week 14: Machine Learning I (Unsupervised)**. Dimensionality Reduction (PCA), Clustering (K-Means).
    *   *Astro Application*: Classifying stellar spectra or galaxy morphologies.
*   **Week 15: Machine Learning II (Symbolic)**. Symbolic Regression, Genetic Algorithms, PySR.
    *   *Astro Application*: Rediscovering Kepler's Laws from raw data.
*   **Week 16: Project Management**. Code structure, proposal writing.
*   **Week 17: Advanced Topics**. Guest lecture (HPC/Pipelines).
*   **Week 18: Final Review**. Course wrap-up.