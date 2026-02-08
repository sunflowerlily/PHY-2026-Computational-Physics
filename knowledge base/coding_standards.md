# Coding Standards & Best Practices

The AI TA will enforce these standards in all code reviews and debugging assistance.

## 1. Vectorization (The Golden Rule)
*   **FORBIDDEN**: Using explicit Python `for` loops to perform arithmetic on arrays.
*   **REQUIRED**: Use NumPy vectorization.
    *   *Bad*: `for i in range(len(x)): y[i] = m*x[i] + c`
    *   *Good*: `y = m*x + c`

## 2. Scientific Libraries
*   **Standard Stack**: `numpy`, `scipy`, `matplotlib.pyplot`.
*   **Fitting**: Use `scipy.optimize.curve_fit` for non-linear fitting. Do NOT write your own Levenberg-Marquardt solver unless explicitly asked.
*   **Interpolation**: Use `scipy.interpolate.interp1d` or `CubicSpline`.
*   **Astronomy**: Use `astropy.units` and `astropy.constants` for physical values.

## 3. Plotting Standards (Publication Quality)
All plots must include:
*   **Labels**: Axis labels with units (e.g., "Wavelength [$\AA$]", "Flux [erg/s/cm$^2$]").
*   **Legend**: Required if multiple lines exist.
*   **Grid**: `plt.grid(True, alpha=0.3)`.
*   **Residuals**: When performing a fit (Week 13), you MUST plot the data, the model, AND the residuals (Data - Model) in a subplot.

## 4. Code Structure
*   **Docstrings**: Every function must have a docstring explaining arguments and return values.
*   **Variable Names**: Use physical names (`radius`, `density`) not generic ones (`r`, `d`).
*   **Reproducibility**: If using random numbers (Week 10-11), always set a seed: `np.random.seed(42)`.