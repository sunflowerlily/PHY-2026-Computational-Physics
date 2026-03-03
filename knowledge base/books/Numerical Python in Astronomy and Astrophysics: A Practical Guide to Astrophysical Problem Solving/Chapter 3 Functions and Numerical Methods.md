# Chapter 3 Functions and Numerical Methods
Abstract: Topics such as black body radiation and Balmer lines set the stage for defining your own Python functions. You will learn about different ways of passing data to functions and returning results. Understanding how to implement numerical methods is an important goal of this chapter. For example, we introduce different algorithms for root finding and discuss common pitfalls encountered in numerics. Moreover, basic techniques of numerical integration and differentiation are covered. Generally, it is a good idea to collect functions in modules. As an example, a module for the computation of planetary ephemerides is presented.

## 3.1 Blackbody Radiation and Stellar Properties
Paradoxical as it may sound, the light emitted by a star is approximately described by the radiation of a black body¹. This is to say that stars emit thermal radiation produced in their outer layers, which have temperatures between a few thousand and tens of thousands of K, depending on the mass and evolutionary stage of the star. The total energy emitted by a black body per unit time is related to its surface area and temperature. This relation is called the Stefan–Boltzmann law. The spectral distribution of the emitted radiation is given by Planck function. See Sect.3.4 in [4] for a more detailed discussion of the physics of black bodies. In this section, Python functions are introduced to perform calculations based on the Stefan–Boltzmann law and the Planck spectrum and to discuss basic properties of stars.

> ¹The term black body refers to its property of perfectly absorbing incident radiation at all wavelengths. At the same time, a black body is an ideal emitter of thermal radiation.

### 3.1.1 Stefan–Boltzmann Law
A star is characterised by its effective temperature \(T_{eff}\) and luminosity \(L\) (i.e. the total energy emitted as radiation per unit time). The effective temperature corresponds to the temperature of a black body radiating the same energy per unit surface area and unit time over all wavelengths as the star. This is expressed by the Stefan–Boltzmann law:
\[F=\sigma T_{eff }^{4}, \quad(3.1)\]
where \(\sigma=5.670 ×10^{-8} ~W ~m^{-2} ~K^{-4}\) is the Stefan–Boltzmann constant. The radiative flux \(F\) is the net energy radiated away per unit surface area and unit time. Integrating the radiative flux over the whole surface of a star of radius \(R\), we obtain the luminosity:
\[L=4\pi R^{2}\sigma T_{eff}^{4} . (3.2)\]

Suppose you want to compute the luminosity of a star of given size and effective temperature. You could do that by writing a few lines of Python code, just like the computation of the orbital velocity in Chap.1. However, it is very common to write a piece of code in such a way that is re-usable and can perform a particular action or algorithm for different input data. This can be achieved by defining a Python function. We have already introduced many library functions, so you should be familiar with using functions by now. A new function can be defined with the keyword `def` followed by a name that identifies the function and a list of arguments in parentheses. Similar to loops, the function header ends with a colon and the indented block of code below the header comprises the body of the function. In the function body, the arguments are processed and usually, but not always, a result is returned at the end. As an example, consider the following definition of the function `luminosity()`:

```python
from math import pi
from scipy.constants import sigma  # Stefan-Boltzmann constant

def luminosity(R, Teff):
    """
    computes luminosity of a star using the Stefan-Boltzmann law
    args:
        R - radius in m
        Teff - effective temperature in K
    returns:
        luminosity in W
    """
    A = 4 * pi * R**2  # local variable for surface area
    return A * sigma * Teff**4
```

The function is explained by a comment enclosed in triple quotes, which is more convenient for longer comments and is used as input for `help()` to display information about functions, particularly if they are defined inside modules. The idea is that somebody who wants to apply the function, can type `help(luminosity)` to get instructions². The variables \(R\) and \(T_{eff}\) are called formal arguments because their values are not specified yet. The definition of the function applies to any values for which the arithmetic expressions in the function body can be evaluated.

A function is executed for particular data in a function call. As you know from previous examples, a function call can be placed on the right side of an assignment statement. For example, the function defined above is used in the following code to compute the luminosity of the Sun:

```python
from astropy.constants import R_sun, L_sun
Teff_sun = 5778  # effective temperature of the Sun in K

print("Solar luminosity:")
# compute luminosity of the Sun
L_sun_sb = luminosity(R_sun.value, 5778)
print("\t{:.3e} W (Stefan-Boltzmann law)".format(L_sun_sb))
# solar luminosity from astropy
print("\t{:.3e} ({:s})".format(L_sun, L_sun.reference))
```

Here, the actual arguments `R_sun.value` (the value of the solar radius defined in `astropy.constants`) and `Teff_sun` (the effective temperature of the Sun defined in line 18) are passed to the function `luminosity()` and the code in the function body (lines 14 to 15) is executed with actual arguments in place of the formal arguments. After the expression following the keyword `return` in line 15 has been evaluated, the resulting value is returned by the function and assigned to `L_sun_sb` in line 23. For comparison, the observed luminosity from the astropy library is printed together with the luminosity resulting from the Stefan–Boltzmann law:

```
Solar luminosity:
    3.844e+26 W (Stefan-Boltzmann law)
    3.828e+26 W (IAU 2015 Resolution B 3)
```

The values agree within 1%. The reference for the observed value is printed in the above example with the help of the attribute `reference` of `L_sun`.

The variable `A` defined in the body of the function `luminosity()` is a local variable, which is not part of Python’s global namespace. It belongs to the local namespace of a function, which exists only while a function call is executed. If you try to print its value after a function call, you will encounter an error because its scope is limited to the function body:

```python
print(A)
```
```
NameError: name ’A’ is not defined
```

In contrast, variable names such as `L_sun_sb` or `sigma` in the above example are defined in the global namespace and can be used anywhere, including the body of a function. However, referencing global variables within a function should generally be avoided. It obscures the interface between data and function, makes the code difficult to read and is prone to programming errors. Data should be passed to a function through its arguments. A common exception are constant parameters from modules. For example, we import `sigma` from `scipy.constants` into the global namespace and then use it inside of the function `luminosity()` in line 13. To sum up³:

> Python functions have a local namespace. Normally, a function receives data from the global namespace through arguments and returns the results it produces explicitly.

Perhaps you noticed that the unit of the solar luminosity is printed for both variables, although the character W (for Watt) is missing in the output string in line 27. This can be understood by recalling that `L_sun` is an Astropy object which has a physical unit incorporated (see Sect. 2.1.2). Although the format specifier refers only to the numeric value, some magic (i.e. clever programming) built into `format()` and `print()` automatically detects and concatenates the unit to the formatted numerical value.

In the example above, we defined `L_sun_sb` as a simple float variable. By means of the units module we can assign dimensional quantities to variables in the likeness of Astropy constants. To obtain the same output as above without explicitly printing the unit W, we just need to make a few modifications:

```python
from astropy.constants import R_sun, L_sun, sigma_sb
import astropy.units as unit

def luminosity(R, Teff):
    """
    function computes luminosity of star
    using the Stefan-Boltzmann law with units
    args:
        dimensional variables based on astropy.units
        R - radius
        Teff - effective temperature
    returns:
        luminosity
    """
    A = 4 * pi * R**2  # local variable for surface area
    return sigma_sb * A * Teff**4

Teff_sun = 5778 * unit.K

# compute luminosity from dimensional variables
L_sun_sb = luminosity(R_sun, Teff_sun)
print("\t{:.3e} (Stefan-Boltzmann law)".format(L_sun_sb))
```

First, `sigma_sb` from `astropy.constants` defines the Stefan–Boltzmann constant with units (simply print `sigma_sb`). Second, a physical unit is attached to the variable `Teff_sun` by multiplying the numerical value 5778 with `unit.K` in line 17. Then `luminosity()` is called with the full object `R_sun` rather than `R_sun.value` as actual argument. Arithmetic operators also work with dimensional quantities in place of pure floating point numbers. However, the flexibility has a downside: there is no safeguard against combining dimensional and dimensionless variables and you might end up with surprising results if you are not careful.

As introduced in Sect. 2.1.2, the method `to()` allows us to convert between units. For example, we can print the luminosity in units of erg/s without bothering about the conversion factor:

```python
# convert from W to erg/s
print("\t{:.3e} (Stefan-Boltzmann law)".format(L_sun_sb.to(unit.erg/unit.s)))
```

This statement prints:
```
3.844e+33 erg / s (Stefan-Boltzmann law)
```

It is even possible to combine different unit systems. Suppose the radius of the Sun is given in units of km rather than m:

```python
# compute luminosity with solar radius in km
L_sun_sb = luminosity(6.957e5 * unit.km, Teff_sun)
print("\t{:.3e} (Stefan-Boltzmann law)".format(L_sun_sb.to(unit.W)))
```

It suffices to convert the result into units of W without modifying the function `luminosity()` at all (also check what you get by printing `L_sun` directly):
```
3.844e+26 W (Stefan-Boltzmann law)
```

Nevertheless, complications introduced by Astropy units might sometimes outweigh their utility. As in many examples throughout this book, you might find it easier to standardize all input data and parameters of a program to a fixed unit system such as SI units. In this case, dimensional quantities are implied, but all variables in the code are of simple floating point type. Depending on your application, you need to choose what suits you best.

Having defined the function `luminosity()`, we can calculate the luminosity of any star with given radius and effective temperature⁴. We will perform this calculation for a sample of well known stars, namely Bernard’s Star, Sirius A and B, Arcturus, and Betelgeuse. The straightforward way would be to define variables for radii and temperatures and then call `luminosity()` with these variables as arguments. In the following, this is accomplished by a more sophisticated implementation that combines several Python concepts:

```python
def stellar_parameters(*args):
    '''
    auxiliary function to create a dictionary
    of stellar parameters in SI units
    args: (radius, effective temperature)
    '''
    return {
        "R": args[0].to(unit.m),
        "Teff": args[1].to(unit.K)
    }

# dictionary of some stars
stars = {
    'Bernard\'s Star': stellar_parameters(0.196 * R_sun, 3.13e3 * unit.K),
    'Sirius A': stellar_parameters(1.711 * R_sun, 9.94e3 * unit.K),
    'Sirius B': stellar_parameters(5.8e3 * unit.km, 2.48e4 * unit.K),
    'Arcturus': stellar_parameters(25.4 * R_sun, 4.29e3 * unit.K),
    'Betelgeuse': stellar_parameters(6.4e8 * unit.km, 3.59e3 * unit.K)
}

print("Luminosities of stars (relative to solar luminosity):")
for name in stars:
    stars[name]['L'] = luminosity(stars[name]['R'], stars[name]['Teff'])
    print("\t{:15s} {:.1e} ({:.1e}) ".format(
        name, stars[name]['L'], stars[name]['L'] / L_sun))
```

First turn your attention to the dictionary defined in lines 41–52 (dictionaries are introduced in Sect. 2.1.2). The keywords are the names of the stars. The items belonging to these keys are returned by the function `stellar_parameters()` defined at the beginning of the program. As you can see in lines 37–38, the function returns a dictionary, i.e. each item of the dictionary `stars` is in turn a dictionary. Such a data structure is called a nested dictionary. As with any dictionary, new items can be added to the subdictionaries. This is done when the luminosity is calculated for each star by iterating over the items of `stars` and adding the result as a new subitem with the key ’L’ (lines 56–57). Items and subitems in nested dictionaries are referenced by keys in concatenated brackets (this syntax differs from multidimensional NumPy arrays). For example, `stars['Sirius B']['R']` is the radius of Sirius B and `stars['Sirius B']['L']` its luminosity (print some items to see for yourself). The whole dictionary of stellar parameters for Sirius B is obtained with `stars['Sirius B']`.

Before we look at the results, let us take a closer look at the function `stellar_parameters()`. In contrast to the function `luminosity()`, which has an explicit list of named arguments, `stellar_parameters()` can receive an arbitrary number of actual arguments. The expression `*args` just serves as a dummy. Such arguments are known as variadic arguments and will be discussed in more detail in Sect. 4.1.2. The function `stellar_parameters()` merely collects values in a dictionary provided that the number of arguments in the function call matches the number of keys (no error checking is made here because it serves only as an auxiliary for constructing the `stars` dictionary). Individual variadic arguments are referenced by an index. The first argument (`args[0]`) defines the radius and the second one (`args[1]`) the effective temperature of the star. Both values are converted into SI units. This implies that the function expects dimensional values as arguments, which is indeed the case in subsequent calls of `stellar_parameters()`. Generally, using an explicit argument list is preferable for readability, but in some cases a flexible argument list can be convenient. In particular, we avoid duplicating names in keys and arguments and new parameters and can be added easily.

The results are listed in the following table (name is printed with the format specifier `15s`, meaning a string with 15 characters, to align the names of the stars):

```
Luminosities of stars (relative to solar luminosity):
    Bernard's Star   1.3e+24 W (3.3e-03)
    Sirius A         9.9e+27 W (2.6e+01)
    Sirius B         9.1e+24 W (2.4e-02)
    Arcturus         7.5e+28 W (2.0e+02)
    Betelgeuse       4.8e+31 W (1.3e+05)
```

We print both the luminosities in W and the corresponding values of \(L / L_{\odot}\) (identify the corresponding expressions in the code). Bernard’s Star is a dim M-type star in the neighbourhood of the Sun. With a mass of only \(0.14 M_{\odot}\), it is small and cool. In contrast, Sirius A is a main sequence star with about two solar masses and spectral type A0. Thus, it is much hotter than the Sun. Since the luminosity increases with the fourth power of the effective temperature, its luminosity is about 26 times the solar luminosity. The luminosity of the companion star Sirius B is very low, yet its effective temperature \(2.5 ×10^{4} ~K\) is much higher than the temperature of Sirius A. Astronomers were puzzled when this property of Sirius B was discovered by Walter Adams in 1915. A theoretical explanation was at hand about a decade later: Sirius B is highly compact star supported only by its electron degeneracy pressure. The size of such a white dwarf star is comparable to size of the Earth⁵, while its mass is about the mass of the Sun. Owing to its small surface area (see Eq.3.2), Sirius B has only a few percent of the solar luminosity even though it is a very hot star. According to the Stefan–Boltzmann law, luminous stars must be either hot or large. The second case applies to giant stars. Arcturus, for example, is in the phase of hydrogen shell burning and evolves along the red-giant branch. With 25 solar radii, its luminosity is roughly 200 times the solar luminosity. At a distance of only 11.3 pc, it appears as one of the brightest stars on the sky. Betelgeuse is a red supergiant with an enormous diameter of the order of a billion km, but relatively low effective temperature (thus the red color; see the parameters defined in our `stars` dictionary). In the solar system, Betelgeuse would extend far beyond the orbit of Mars, almost to Jupiter. It reaches the luminosity of a hundred thousand Sun-like stars.

### 3.1.2 Planck Spectrum
The energy spectrum of a black body of temperature \(T\) is given by the Planck function:
\[B_{\lambda}(T)=\frac{2 h c^{2}}{\lambda^{5}} \frac{1}{exp (h c / \lambda k T)-1},\]
where \(\lambda\) is the wavelength, \(h\) is Planck’s constant, \(k\) the Boltzmann constant and \(c\) the speed of light. The differential \(B_{\lambda}(T) cos \theta d \Omega d \lambda\) is the energy emitted per unit surface area and unit time under an angle \(\theta\) to the surface normal into the solid angle \(d \Omega=sin \theta d \theta d \phi\) (in spherical coordinates) with wavelengths ranging from \(\lambda\) to \(\lambda+d \lambda\). Integration over all spatial directions and wavelengths yields the Stefan–Boltzmann law for the energy flux⁶:
\[F \equiv \pi \int_{0}^{\infty} B_{\lambda}(T) d \lambda=\sigma T^{4} .\]

We continue our discussion with producing plots of the Planck spectrum for the stars discussed in Sect.3.1.1 and, additionally, the Sun. The first step is, of course, the definition of a Python function `planck_spectrum()` to compute \(B_{\lambda}(T)\). To avoid numbering of code lines over too many pages, we reset the line number to 1 here. However, be aware that the code listed below nevertheless depends on definitions from above, for example, the `stars` dictionary.

```python
import numpy as np
from scipy.constants import h, c, k

def planck_spectrum(wavelength, T):
    """
    function computes Planck spectrum of a black body
    args:
        numpy arrays
        wavelength - wavelength in m
        T - temperature in K
    returns:
        intensity in W/m^2/m/sr
    """
    return 2 * h * c**2 / (wavelength**5 * (np.exp(h * c / (wavelength * k * T)) - 1))
```

The expression in the function body corresponds to formula (3.3). We use the exponential function from the NumPy library, which allows us to call `planck_spectrum()` with arrays as actual arguments. This is helpful for producing a plot of the Planck spectrum from an array of wavelengths. Moreover, physical constants are imported from `scipy.constants`. Consequently, we do not make use of dimensional quantities here.

The next step is to generate an array of temperatures for the different stars and a wavelength grid to plot the corresponding spectra. To that end, we collect the values associated with the key ’Teff’ in our dictionary. A wavelength grid with a given number of points between minimum and maximum values is readily generated with `np.linspace()` introduced in Sect. 2.3.

```python
# initialize array for temperatures
T_sample = np.zeros(len(stars) + 1)

# iterate over stellar temperatures in dictionary
for i, key in enumerate(stars):
    T_sample[i] = stars[key]['Teff'].value
# add effective temperature of Sun as last element
T_sample[-1] = 5778

# sort temperatures
T_sample = np.sort(T_sample)

# uniformly spaced grid of wavenumbers
n = 1000
lambda_max = 2e-6
wavelength = np.linspace(lambda_max / n, lambda_max, n)
```

Remember that the loop variable of a `for` loop through a dictionary runs through the keys of the dictionary (see Sect.2.1.2). Here, `key` runs through the names of the stars. By using `enumerate()`, we also have an index \(i\) for the corresponding elements of the array `T_sample`, which is initialized as an array of zeros in line 17. The array length is given by the length of the dictionary, i.e. the number of stars, plus one element for the Sun. After the loop, the NumPy function `sort()` sorts the temperatures in ascending order. The minimum wavelength is set to `lambda_max/n` corresponding to the subdivision of the interval \([0, \lambda_{max}]\) with \(\lambda_{max}=2 ×10^{-6}\) m into 1000 equidistant steps. Although the Planck function is mathematically well defined even for \(\lambda=0\), the numerical evaluation poses a problem because Python computes the different factors and exponents occurring in our definition of the function `planck_spectrum()` separately (you can check this by calling `planck_spectrum()` for wavelength zero). For this reason, zero is excluded.

The following code plots the Planck spectrum for the different temperatures using a color scheme that mimics the appearance of stars (or any black body of given temperature) to the human eye. To make use of this scheme, you need to import the function `convert_K_to_RGB()` from a little module that is not shipped with common packages such as NumPy, but is shared as GitHub gist on the web⁷. The colors are based on the widely used RGB color model to represent colors in computer graphics. A particular RGB color is defined by three (integer) values ranging from 0 to 255 to specify the relative contributions of red, green, and blue⁸. White corresponds to (255, 255, 255), black to (0, 0, 0), pure red to (255, 0, 0), etc. This model allows for the composition of any color shade.

```python
import matplotlib.pyplot as plt
from rgb_to_kelvin import convert_K_to_RGB
%matplotlib inline

plt.figure(figsize=(6, 4), dpi=100)

for T in T_sample:
    # get RGB color corresponding to temperature
    color = tuple([val / 255 for val in convert_K_to_RGB(T)])
    
    # plot Planck spectrum (wavelength in nm, intensity in kW/m^2/nm/sr)
    plt.semilogy(
        1e9 * wavelength,
        1e-12 * planck_spectrum(wavelength, T),
        color=color,
        label="{:.0f} K".format(T)
    )

plt.xlabel("$\lambda$ [nm]")
plt.xlim(0, 1e9 * lambda_max)
plt.ylabel("$B_\lambda(T) $" + "[$\mathrm{kW\,m^{-2}\,nm^{-1}\, sr^{-1}}$]")
plt.ylim(0.1, 5e4)
plt.legend(loc="upper right", fontsize=8)
plt.savefig("planck_spectrum.pdf")
```

We use `semilogy()` from pyplot for semi-logarithmic scaling because the Planck functions for the different stars vary over several orders of magnitude. While `convert_K_to_RGB()` returns three integers, a tuple of three floats in the range from 0 to 1 is expected as color argument in line 46. As an example of somewhat more fancy Python programming, the conversion is made by an inline loop through the return values (see line 40), and the resulting RGB values are then converted into a tuple via the built-in function `tuple()`. To show formatted mathematical symbols in axes labels, it is possible to render text with LaTeX. We do not cover LaTeX here⁹, but examples can be seen in lines 48 and 50–51. For instance, the greek letter \(\lambda\) in the x-axis label is rendered with the LaTeX code `$\lambda$`, and \(B_{\lambda}(T)\) for the y axis is coded as `$B_\lambda(T)$`.

The resulting spectra are shown in Fig.3.1. The temperatures are indicated in the legend. The color changes from orange at temperatures around 3000 K to bluish above 10000 K. Our Sun with an effective temperature of 5778 K appears nearly white with a slightly reddish tinge, in agreement with our perception¹⁰. You can also see that the curves for different temperatures do not intersect, i.e. \(B_{\lambda}(T_{2})>B_{\lambda}(T_{1})\) for \(T_{2}>T_{1}\). Equation(3.4) implies that the radiative flux \(F\) (the total area under the Planck spectrum) is larger for higher temperatures. In other words, a hotter surface emits more energy. Moreover, Fig.3.1 shows that the peak of the spectrum shifts with increasing temperature to shorter wavelengths. This is, of course, related to the overall color (a larger fraction of short wavelengths corresponds to bluer color). The hottest star in our sample, which is the white dwarf Sirius B, even emits most of its radiation in the UV (below 400 nm).

![Planck spectra for effective temperatures of different stars](planck_spectrum.pdf)
*Fig. 3.1 Planck spectra for effective temperatures of different stars*

The position of the maximum of \(B_{\lambda}(T)\) is described by Wien’s displacement law:
\[\lambda_{max }=\frac{b}{T}, \quad(3.5)\]
where \(b ≈h c /(4.965114 k)=0.002897772 ~m ~K\). To determine the maximum of \(B_{\lambda}(T)\) for a given temperature, we need to find the roots of the first derivative with respect to \(\lambda\):
\[\frac{\partial B_{\lambda}(T)}{\partial \lambda}=0\]
which implies:
\[\frac{h c}{\lambda k T} \frac{exp (h c / \lambda k T)}{exp (h c / \lambda k T)-1}-5=0 .\]

This is a transcendent equation that can be solved only numerically. The equation can be simplified with the substitution \(x=h c / \lambda k T\). After rearranging the terms, the following equation in terms of \(x\) is obtained:
\[f(x):=(x-5) e^{x}+5=0 . \quad(3.6)\]

To match Wien’s displacement law (3.5), the solution should be \(x ≈4.965114\).

We apply an algorithm which is known as bisection method to find the roots of the function \(f(x)\) defined by the left-hand side of Eq.(3.6). The idea is really simple. It is known from calculus that a continuous real function \(f(x)^{11}\) has at least one root \(x \in[a, b]\) if \(f(a) f(b)<0\), i.e. the function has opposite sings at the endpoints of the interval \([a, b]\) and, consequently, crosses zero somewhere within the interval. This property can be used to find approximate solutions of \(f(x)=0\) by splitting the interval \([a, b]\) at its midpoint \(x=(a+b) / 2\) into two subintervals \([a, x]\) and \([x, b]\) (thus the name bisection) and checking which subinterval in turn contains a root. This procedure can be repeated iteratively. Since the interval length \(|a-b|\) decreases by a factor after each iteration, the iteration ends once \(|a-b|\) becomes smaller than a given tolerance \(\epsilon\), corresponding to the desired accuracy of the numerical approximation. This means that the final approximation \(x\) does not deviate by more than \(\epsilon\) from the exact root.

The bisection method is implemented in the following Python function. As you know already from many examples, a Python function is generally not equivalent to a function in the mathematical sense, such as `planck_spectrum()`. It is similar to what is called a subprogram or subroutine in other programming languages, providing a well defined interface to an algorithm with various elements of input (the arguments of the function) and output (data returned by the function):

```python
def root_bisection(f, a, b, eps=1e-3, verbose=False):
    """
    bisection algorithm for finding the root of a function f(x)
    args:
        f - function f(x)
        a - left endpoint of start interval
        b - right endpoint of start interval
        eps - tolerance
        verbose - print additional information if true
    returns:
        estimate of x for which f(x) = 0
    """
    i = 0  # counter of number of iterations
    # iterate while separation of endpoints is greater than tolerance
    while abs(b - a) > eps:
        if verbose:
            print(f"{a:6.3f} {f(a):10.3e}", f"{b:6.3f} {f(b):10.3e}")
        # new midpoint
        x = 0.5 * (a + b)
        # check if function crosses zero in left subinterval and reset endpoint
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        # increment counter
        i += 1
    print("tolerance reached after {:d} iterations".format(i))
    print("deviation: f(x) = {:.3e}".format(f(x)))
    return x
```

Let us first look at the different arguments. The first argument is expected to be a function (more precisely, the name of a function) that can be called inside `root_bisection()`. As we shall see shortly, it is an extremely useful feature of Python that functions can be passed as arguments to other functions¹². The following two arguments, \(a\) and \(b\), are simple variables for the two endpoints of the initial interval. The remaining arguments are optional, which is indicated by assigning default values in the definition of the function. This allows the user to omit actual arguments in place of `eps` and `verbose` when calling `root_bisection()`. Unless an optional argument is explicitly specified, its default value will be assumed, for example, 1e-3 for the tolerance `eps` and `False` for `verbose`.

The bisection algorithm is implemented in the `while` loop starting at line 17. The loop continues as long as `abs(b-a)`, where `abs()` returns the absolute value, is larger than the tolerance `eps`. In lines 28–29, the subinterval \([a, x]\) is selected if the function has opposite signs at the endpoint \(a\) and the midpoint \(x=(a+b) / 2\). In this case, the value of \(x\) defined in line 24 is assigned to the variable \(b\) for the next iteration (recall the difference between an assignment and equality in the mathematical sense). Otherwise variable \(a\) is set equal to \(x\), corresponding to the subinterval \([x, b]\) (lines 30–31). Once the tolerance is reached, the loop terminates and the latest midpoint is returned as final approximation.

Before applying `root_bisection()` to the Planck spectrum, it is a good idea to test it for a simple function with known roots. Let us try the quadratic polynomial:
\[f(x)=x^{2}-x-2\]

In Python, we can define this function as:

```python
def quadratic(x):
    return x**2 - x - 2
```

Using interactive Python, the call:

```python
root_bisection(quadratic, 0, 5, verbose=True)
```

produces the following output (the return value is printed automatically in an output cell):

```
0.000 -2.000e+00 5.000 1.800e+01
0.000 -2.000e+00 2.500 1.750e+00
1.250 -1.688e+00 2.500 1.750e+00
1.875 -3.594e-01 2.188 5.977e-01
1.875 -3.594e-01 2.500 1.750e+00
1.875 -3.594e-01 2.031 9.473e-02
1.953 -1.384e-01 2.031 9.473e-02
1.992 -2.338e-02 2.031 9.473e-02
1.992 -2.338e-02 2.012 3.529e-02
1.992 -2.338e-02 2.002 5.863e-03
1.997 -8.780e-03 2.002 5.863e-03
2.000 -1.465e-03 2.002 5.863e-03
2.000 -1.465e-03 2.001 2.198e-03
tolerance reached after 13 iterations
deviation: f(x) = 3.662e-04
2.0001220703125
```

By calling `root_bisection()` with the identifier `quadratic` as first argument, the bisection method is applied to our test function `quadratic()` defined in lines 40–41 in place of the generic function \(f()\). In the same way, any other function with an arbitrary name can be used. This is why specifying the function for which we want to compute a root as an argument of `root_bisection()` is advantageous. While the optional argument `eps` is skipped in the example above, setting the verbosity flag `verbose=True` allows us to see how the endpoints \(a\) and \(b\) of the interval change with each iteration. The Boolean variable `verbose` controls additional output in lines 20–21, which comes in useful if something unexpected happens and one needs to understand in detail how the code operates. The argument name `verbose` is also called a keyword in this context. As expected, the function always has opposite signs at the endpoints and the root \(x_{2}=2\) is found within a tolerance of \(10^{-3}\) after 13 bisections of the initial interval [0, 5]. So far, everything works fine.

However, try:

```python
root_bisection(quadratic, -2, 0, verbose=True)
```

The output is:

```
-2.000 4.000e+00 0.000 -2.000e+00
-1.000 0.000e+00 0.000 -2.000e+00
-0.500 -1.250e+00 0.000 -2.000e+00
-0.250 -1.688e+00 0.000 -2.000e+00
-0.125 -1.859e+00 0.000 -2.000e+00
-0.062 -1.934e+00 0.000 -2.000e+00
-0.031 -1.968e+00 0.000 -2.000e+00
-0.016 -1.984e+00 0.000 -2.000e+00
-0.008 -1.992e+00 0.000 -2.000e+00
-0.004 -1.996e+00 0.000 -2.000e+00
-0.002 -1.998e+00 0.000 -2.000e+00
tolerance reached after 11 iterations
deviation: f(x) = -1.999e+00
-0.0009765625
```

Obviously, the algorithm does not converge to the solution \(x_{1}=-1\) for the start interval [−2, 0]¹³. The problem can be spotted in the second line of output (i.e. the second iteration). At the left endpoint \(a=-1\), we have \(f(a)=0\). However, `root_bisection()` tests whether \(f(a) f(x)<0\) in line 28. Since the product of function values is zero in this case, the `else` clause is entered and the left endpoint is set to the midpoint \(x=-0.5\), as can be seen in the next line of output. As a result, our current implementation of the algorithm misses the exact solution and ends up in an interval that does not contain any root at all (the signs at both endpoints are negative) and erroneously concludes that the variable \(x\) contains an approximate solution after the interval has shrunk enough.

Fortunately, this can be easily fixed by testing whether \(f(x)\) happens to be zero for some given \(x\). The improved version of `root_bisection()` is listed in the following (the comment explaining the function is omitted):

```python
def root_bisection(f, a, b, eps=1e-3, verbose=False):
    i = 0  # counter of number of iterations
    while abs(b - a) > eps:  # iterate while separation of endpoints is greater than tolerance
        if verbose:
            print(f"{a:6.3f} {f(a):10.3e}", f"{b:6.3f} {f(b):10.3e}")
        # new midpoint
        x = 0.5 * (a + b)
        # check if function crosses zero in left subinterval and reset endpoint unless x is exact solution
        if f(x) == 0:
            print("found exact solution after {:d} iteration(s)".format(i+1))
            return x
        elif f(a) * f(x) < 0:
            b = x
        else:
            a = x
        i += 1  # increment counter
    print("tolerance reached after {:d} iterations".format(i))
    print("deviation: f(x) = {:.3e}".format(f(x)))
    return x
```

The keyword `elif` introduces a third case between the `if` and `else` clauses. The `if` statement in line 17 checks if the value of \(x\) is an exact root. If this is the case, the current value will be returned immediately, accompanied by a message. As you can see, a `return` statement can occur anywhere in a function, not only at the end. Of course, this makes sense only if the statement is conditional, otherwise the remaining part of the function body would never be executed. If the condition \(f(x)==0\) evaluates to `False`, the algorithm checks if the function has opposite signs at the endpoints of the subinterval \([a, x]\) (elif statement in line 21) and if that is not case either (else statement), the right subinterval \([x, b]\) is selected for the next iteration.

To test the modified algorithm, we first convince ourselves that answer for the initial interval [0, 5] is the same as before:

```python
root_bisection(quadratic, 0, 5)
```

prints (verbose set to False by default):

```
tolerance reached after 13 iterations
deviation: f(x) = 3.662e-04
2.0001220703125
```

Now let us see if we obtain the root \(x_{1}\) for the start interval [−2, 0]:

```python
root_bisection(quadratic, -2, 0)
```

Indeed, our modification works:

```
found exact solution after 1 iteration(s)
-1.0
```

To obtain a more accurate approximation for \(x_{2}\), we can prescribe a lower tolerance:

```python
root_bisection(quadratic, 0, 5, 1e-6)
```

In this case, it is not necessary to explicitly write `eps=1e-6` in the function call because the actual argument 1e-6 at position four in the argument list corresponds to the fourth formal argument `eps` in the definition of the function. Arguments that are uniquely identified by their position in the argument list are called positional arguments. If an argument is referred by its name rather than position (like `verbose=True` in the examples above), it is called a keyword argument (the keyword being the name of the corresponding formal argument). In particular, an optional argument must be identified by its keyword if it occurs at a different position in the function call¹⁴. The result is:

```
tolerance reached after 23 iterations
deviation: f(x) = -3.576e-07
1.9999998807907104
```

So far, the initial interval \([a, b]\) was chosen such that it contains only one root and the solution is unambiguous. However, what happens if `root_bisection()` is executed for, say, the interval [−5, 5]? The bisection method as implemented above returns only one root, although both \(x_{1}\) and \(x_{2}\) are in [−5, 5]. It turns out that:

```python
root_bisection(quadratic, -5, 5)
```

converges to \(x_{1}\):

```
tolerance reached after 14 iterations
deviation: f(x) = 1.099e-03
-1.0003662109375
```

We leave it as an exercise to study in detail how this solution comes about by using the verbose option. Basically, the reason for obtaining \(x_{1}\) rather than \(x_{2}\) is that we chose to first check whether \(f(a) f(x)<0\) rather than \(f(b) f(x)<0\). In other words, the answer depends on our specific implementation of the bisection method. This is not quite satisfactory.

Is it possible at all to implement a more robust algorithm that does not depend on any particular choices? The trouble with the bisection method is that there is no unique solution for any given interval \([a, b]\) for which \(f(a) f(b)<0\). If the function happens to have multiple roots, the bisection method will converge to any of those roots, but it is unclear to which one. The only way out would be to make sure that all of them are found. This can indeed be accomplished by means of a recursive algorithm. In Python, recursion means that a function repeatedly calls itself. As with loops, there must be a condition for termination. Otherwise an infinite chain of function calls would result. In the case of the bisection method, this condition is \(f(a) f(b) ≥0\) or \(|b-a|<\epsilon\) (where “or” is understood as the inclusive “or” from logic), i.e. the function stops to call itself once the endpoint values for any given interval have equal signs or at least one of the two values is zero or the tolerance for the interval length is reached.

The following listing shows how to find multiple roots through recursion:

```python
def root_bisection(f, a, b, roots, eps=1e-3):
    """
    recursive bisection algorithm for finding multiple roots of a function f(x)
    args:
        f - function f(x)
        a - left endpoint of start interval
        b - right endpoint of start interval
        roots - numpy array of roots
        eps - tolerance
    returns:
        estimate of x for which f(x) = 0
    """
    # midpoint
    x = 0.5 * (a + b)
    # break recursion if x is an exact solution
    if f(x) == 0:
        roots = np.append(roots, x)
        print("found {:d}. solution (exact)".format(len(roots)))
    # break recursion if tolerance is reached
    elif abs(b - a) <= eps:
        roots = np.append(roots, x)
        print("found {:d}. solution, deviation f(x) = {:6e}".format(len(roots), f(x)))
    # continue recursion if function crosses zero in any subinterval
    else:
        if f(a) * f(x) <= 0:
            roots = root_bisection(f, a, x, roots, eps)
        if f(x) * f(b) <= 0:
            roots = root_bisection(f, x, b, roots, eps)
    return roots
```

To understand the recursive algorithm, consider an arbitrary interval \([a, b]\) with \(f(a) f(b)<0\) and midpoint \(x=(a+b) / 2\). We can distinguish the following four cases:
1. If \(f(x)=0\), then \(x\) is an exact solution.
2. If \(|a-b| ≤\epsilon\), then \(x\) is an approximate solution within the prescribed tolerance.
3. If \(|a-b|>\epsilon\) and \(f(a) f(x)<0\), then there is at least one root in the open interval \(x \in] a, x[\).
4. If \(|a-b|>\epsilon\) and \(f(x) f(b)<0\), then there is at least one root in the open interval \(x \in] x, b[\)¹⁵.

The nested control structure beginning in line 18 implements the corresponding courses of action. First the code checks if \(x\) is an exact solution or if the tolerance is already reached (cases 1. and 2.). In both cases, the value of the local variable \(x\) (i.e. the exact or approximate root) is added to the array `roots` before the algorithm terminates. We utilize the NumPy function `append()` to add a new element to an existing array. The resulting array is then re-assigned to `roots`. Only if \(x\) is neither an exact nor an approximate root of sufficient accuracy, `root_bisection()` will be called recursively for one or both subintervals (lines 30–33). This is different from the iterative algorithms discussed at the beginning of this section, where only a single subinterval is selected in each iteration step. Depending on whether only case 3. or 4. or both cases apply, the recursive algorithm progresses like the iterative algorithm toward a single root or branches to pursue different roots. The algorithm can branch an arbitrary number of times. Each call of `root_bisection()` returns an array (see line 35) containing roots appended at deeper recursion levels (the recursion depth increases with the number of recursive functions calls). Since `np.append()` generates a new object rather than modifying an existing object, the arrays returned by the calls in lines 31 and 33 have to be re-assigned to `roots` in the namespace of the calling instance. It does not matter that the name `roots` is used both for the array received as argument and for the array returned by the function. We use the same name only to highlight the recursive nature of the algorithm.

As a first test:

```python
x0 = root_bisection(quadratic, -2, 0, [])
print(x0)
```

should find the solution \(x_{1}=-1\) as in the example above. This is indeed the case:

```
found 1. solution (exact)
[-1.]
```

The value returned by `root_bisection()` is now printed in brackets, which indicates an array. We started with an empty array `[]` (technically speaking, an empty list that is automatically converted into an array) in the initial function call and obtained an array `x0` with a single element, namely −1. This array can in turn be passed as actual argument to another call of `root_bisection()` for a different start interval:

```python
x0 = root_bisection(quadratic, 0, 5, x0)
print(x0)
```

The array returned by the second call of `root_bisection()` is re-assigned to `x0` and now contains both roots:

```
found 2. solution, deviation f(x) = -5.492829e-04
[-1. 1.99981689]
```

Try to figure out how the code determines that this is the second solution (as indicated by “found 2. solution” in the output).

Of course, we would not gain anything compared to the iterative implementation if it were not for the possibility of computing all roots at once. For example:

```python
x0 = root_bisection(quadratic, -5, 5, [])
print(x0)
```

we receive the output:

```
found 1. solution, deviation f(x) = 1.831092e-04
found 2. solution, deviation f(x) = -5.492829e-04
[-1.00006104 1.99981689]
```

In this case, the first root is also approximate because the bisection starts with the left endpoint \(a=-5\) instead of −2 and the resulting midpoints do not hit the exact solution \(x_{1}=-1\). As a small exercise, you may modify the recursive function to print detailed information to see how the intervals change with increasing recursion depth.

After having carried out various tests, we are now prepared to numerically solve Eq.(3.6). First we need to define the function \(f(x)\) corresponding to the left-hand side of the equation:

```python
def f(x):
    return (x - 5) * np.exp(x) + 5
```

Since the solution of \(f(x)=0\) is some number \(x ~ 1\) (for large \(x\), exponential growth would rapidly dominate), let us try the start interval [0, 10]:

```python
x0 = root_bisection(f, 0, 10, [])
print(x0)
```

The recursive bisection method finds two solutions:

```
found 1. solution, deviation f(x) = -1.220843e-03
found 2. solution, deviation f(x) = -2.896551e-02
[3.05175781e-04 4.96490479e+00]
```

The first solution is actually the endpoint \(a=0\) for which \(f(a)=0\). The second solution ≈4.965 is approximately the solution we know from Wien’s law (you might want to plot \(f(x)\) using pyplot to get an impression of the shape of the function). You can improve the accuracy by specifying a smaller tolerance `eps` and check the agreement with the value cited above. If you compare the conditions for zero crossings in the iterative and recursive implementations, you might wonder why the operator `<` is used in the former and `<=` (smaller or equal to) in the latter. Replace `<=` by `<` in the checks of both subintervals in the recursive function and see what happens if you repeat the execution for the start interval [0, 10]. The output will change drastically. Try to figure out why¹⁶.

The workflow withseveral cycles of programming and testing is typical for the implementation of a numerical method. The first implementation never works perfectly. This is why simple test cases for which you know the answer beforehand are so important to validate your code. Frequently, you will notice problems you have not thought of in the beginning and sometimes you come to realize there is an altogether better solution.

### Exercises
3.1 Extend the function `stellar_parameters()` to add stellar masses to the dictionary `stars`. For the stars discussed in Sect.3.1.1, the masses in units of the solar mass are 0.144, 2.06, 1.02, 1.1, and 12 (from Bernard’s Star to Betelgeuse). Moreover, write a Python function that calculates the radius for given luminosity and effective temperature. Use this function to add Aldebaran ( \(L=4.4 ×10^{2} L_{\odot}\) , \(T_{eff}=3.9 ×10^{3} ~K\) , \(M=1.2 M_{\odot}\) ) and Bellatrix ( \(L=9.21 ×10^{2} L_{\odot}\) , \(T_{eff}=2.2 ×10^{4} ~K\) , \(M=8.6 M_{\odot}\) ) to the dictionary and carry out the following tasks.
(a) Print a table of the stellar parameters \(M\), \(R\), \(T_{eff}\), and \(L\) aligned in columns.
(b) Plot the luminosities versus the effective temperatures in a double-logarithmic diagram using different markers for main-sequence stars, white dwarfs, and red giants. In other words, produce a Herztsprung–Russell diagram for the stars in the dictionary.
(c) Produce a plot of luminosity vs mass in double-logarithmic scaling. Which type of relation is suggested by the data points?

3.2 In astronomy, the observed brightness of an object on the sky is specified on a logarithmic scale that is based on flux ratios [3, Chap. 4]¹⁷:
\[m=M-2.5 log _{10}\left(\frac{F}{F_{0}}\right) .\]
The convention is to define \(F_{0}=L / 4 \pi r_{0}^{2}\) as the radiative flux at distance \(r_{0}=10 pc\). While the absolute magnitude \(M\) is a constant parameter for a star of given luminosity \(L\), the star’s apparent magnitude \(m\) depends on its distance \(r\). The relation \(F \propto 1 / r^{2}\) for the radiative flux implies:
\[m-M=5 log _{10}\left(\frac{r}{10 pc}\right) .\]
Hence, the distance of the star can be determined if both the apparent and absolute magnitude are known. However, extinction due to interstellar dust modifies this relation:
\[m-M=5 log _{10}\left(\frac{r}{10 pc}\right)+k r, (3.7)\]
Although the extinction varies significantly within the Galaxy, the mean value \(k=2 ×10^{-3} pc^{-1}\) can be assumed for the extinction per unit distance [3, Sect.16.1].
Compute and plot \(r\) in units of pc for B0 main sequence stars with an absolute magnitude \(M=-4.0\) and apparent magnitudes \(m\) in the range from −4.0 to 6.0 in the visual band¹⁸. How are the distances affected by extinction? To answer this question, you will need to solve Eq.(3.7) numerically for each data point. To be able to plot a graph, it is advisable to create an array of closely spaced magnitudes.

## 3.2 Physics of Stellar Atmospheres
To a first approximation, the radiation of stars is black body radiation. However, observed stellar spectra deviate from the Planck function. The most important effect is the absorption of radiation from deeper and hotter layers of a star by cooler gas in layers further outside. The outermost layers which shape the spectrum of the visible radiation of a star are called stellar atmosphere.

Although hydrogen is the most abundant constituent, other atoms and ions play an important role too, especially in stars of low effective temperature. For a more detailed discussion of the physics, see Chaps. 8 and 9 in [4]. As a consequence, modeling the transfer of radiation in stellar atmospheres is extremely complex and requires numerical computations using databases for a huge number of line transitions for a variety of atoms, ions, and molecules. You will see an application of such model atmospheres in Sect. 5.5.2.

In the following, we will consider some basic aspects of the physical processes in stellar atmospheres. An important source of absorption in stellar atmospheres are transitions from lower to higher energy levels (also known as bound-bound transitions). For hydrogen, the energy difference between levels defined by the principal quantum numbers \(n_{1}\) and \(n_{2}>n_{1}\) is given by:
\[\Delta E=-13.6 eV\left(\frac{1}{n_{2}}-\frac{1}{n_{1}}\right) .\]
A photon can be absorbed if its energy matches the energy difference between the two levels:
\[\Delta E=\frac{h c}{\lambda} \quad(3.9)\]
where \(h\) is Planck’s constant, \(c\) is the speed of light, and \(\lambda\) is the wavelength of the photon. For a hydrogen atom in the ground state, \(n_{1}=1\), the wavelength associated with the transition to the next higher level, \(n_{2}=2\), is \(\lambda=121.6 ~nm\) and even shorter for higher levels. Emission or absorption lines at these wavelengths, which are all ultraviolet, are called the Lyman series. One might expect that the Lyman series can be seen in the light emitted by hot stars. However, the fraction of hydrogen atoms in the ground state rapidly decreases with increasing temperature. It turns out that transitions from the first excited state, \(n_{1}=2\), to levels \(n_{2}>2\) give rise to prominent absorption lines in stellar spectra, which are known as Balmer lines. To understand how this comes about, we need to apply two fundamental equations from statistical physics, namely the Boltzmann and Saha equations, to compute the fraction of atoms in excited states and the fraction that is ionized at a given temperature.

### 3.2.1 Thermal Excitation and Ionization
Collisions between atoms excite some of them into a higher energy state, while others lose energy. The balance between these processes is described by the Boltzmann distribution. If the gas is in thermal equilibrium, the ratio of the occupation numbers \(N_{2}\) and \(N_{1}\) of levels \(n_{2}\) and \(n_{1}\), respectively, is given by:
\[\frac{N_{2}}{N_{1}}=\frac{g_{2}}{g_{1}} e^{-\left(E_{2}-E_{1}\right) / k T} (3.10)\]
where \(g_{1}\) and \(g_{2}\) are the statistical weights of the energy levels (i.e. the number of possible quantum states with the same energy) and \(T\) is the temperature of the gas. For the hydrogen atom, the \(n\)-th energy level is degenerate with weight \(g_{n}=2 n^{2}\) (the energy of a state is independent of the spin and the angular momentum quantum numbers).

As an example, let us compute \(N_{2} / N_{1}\) for the first excited state of hydrogen for the stars defined in the dictionary `stars` in Sect.3.1.1:

```python
import numpy as np
from scipy.constants import k, physical_constants

# ionization energy of hydrogen
chi = physical_constants['Rydberg constant times hc in J'][0]
n1, n2 = 1, 2  # energy levels

print("T [K]    N2/N1")
for T in T_sample:
    print("{:5.0f}    {:.3e}".format(
        T,
        (n2/n1)**2 * np.exp(chi*(1/n2**2 - 1/n1**2)/(k*T))
    ))
```

The occupation numbers of the first excited state (\(n_{2}=2\)) relative to the ground state (\(n_{1}=1\)) are printed for the effective temperatures in the array `T_sample` (see Sect.3.1.2). The Boltzmann equation (3.10) is implemented inline as an expression in terms of the variables \(n1\), \(n2\), and \(Teff\). Line 5 defines the ionization energy \(\chi \equiv E_{\infty}-E_{1}\) in terms of the Rydberg constant \(R\):
\[\chi=h c R=13.6 eV . (3.11)\]
This allows us to express the energy difference \(\Delta E\) between the two states in Boltzmann’s equation as:
\[\Delta E=-\chi \left( \frac{1}{n_{2}}-\frac{1}{n_{1}}\right) . (3.12)\]

The value of \(\chi\) in SI units (J) is available in SciPy’s `physical_constants` dictionary, which is imported in line 2. This dictionary allows us to conveniently reference physical constants via keywords. In the case of \(\chi\), the key expresses formula (3.11) in words. Since each item in `physical_constants` is a tuple containing the numerical value, unit, and precision of a constant, we need to assign the first element of the tuple to the variable `chi`.

The code listed produces the output:
```
T [K]    N2/N1
 3130    1.485e-16
 3590    1.892e-14
 4290    4.115e-12
 5778    5.030e-09
 9940    2.681e-05
24800    3.376e-02
```

While the fraction of hydrogen in the first excited state is very low for cooler stars and the Sun, it increases rapidly toward the hot end. An easy calculation shows that \(N_{2}=N_{1}\) is reached at a temperature of \(8.54 ×10^{4} ~K\). This is higher than the effective temperature of even the hottest stars of class O. Transitions from the first excited state thus should become ever more important as the effective temperature increases. However, this is not what is observed: the strongest Balmer absorption lines are seen in the spectra of stars of spectral class A, with effective temperatures below 10000 K.

The reason for this is the ionization of hydrogen. Once a hydrogen atom is stripped of its electron, there are no transitions between energy levels. The temperature-dependent fraction of ionized hydrogen (HII) can be computed using the Saha equation:
\[\frac{N_{II}}{N_{I}}=\frac{2 k T Z_{II}}{P_{e} Z_{I}}\left(\frac{2 \pi m_{e} k T}{h^{2}}\right)^{3 / 2} e^{-\chi / k T} . (3.13)\]

Similar to the Boltzmann equation (3.10), the ratio \(N_{II}/N_{I}\) is dominated by the exponential factor \(e^{-\chi / k T}\) for low temperature. Here, \(\chi\) is the ionization energy defined by Eq.(3.11). An additional parameter is the pressure of free electrons, \(P_{e}\) (i.e. electrons that are not bound to atoms). The factor \(k T / P_{e}\) equals the inverse number density of free electrons. If there are more free electrons per unit volume, recombinations will become more frequent and the number of ions decreases. Apart from the Boltzmann and Planck constants, the electron mass \(m_{e}\) enters the equation. The partition function \(Z\) is the effective statistical weight of an atom or ion. It is obtained by summing over all possible states with relative weights given by the Boltzmann distribution (3.10):
\[Z=g_{1}\left(1+\sum_{n=2}^{\infty} \frac{g_{n}}{g_{1}} e^{-\left(E_{n}-E_{1}\right) / k T}\right) .\]

Since we consider a regime of temperatures for which the thermal energy \(k T\) is small compared to the energy difference \(E_{n}-E_{1}\) between the ground state and higher energy levels (in other words, most of the hydrogen is in its ground state), the approximation \(Z_{I} \approx g_{1}=2\) can be used. This is consistent with the values of \(N_{2} / N_{1}\) computed above. The partition function \(Z_{II}=1\) because a hydrogen ion has no electron left that could occupy different energy levels.

The Saha equation is put into a Python function to evaluate \(N_{II}/N_{I}\) for given temperature and electron pressure:

```python
def HII_frac(T, P_e):
    """
    computes fraction of ionized hydrogen
    using the Saha equation
    args:
        T - temperature in K
        P_e - electron pressure in Pa
    returns:
        HII fraction
    """
    E_therm = k*T
    return (E_therm/P_e) * \
           (2*np.pi*m_e*E_therm/h**2)**(3/2) * \
           np.exp(-chi/E_therm)
```

While the local variable `E_therm` is used for the thermal energy \(k T\) of the gas, the constant ionization energy is defined by the variable `chi` in the global namespace (see line 5 above).

To estimate the strength of Balmer lines, we need to compute the number of neutral hydrogen atoms (HI) in the first excited state relative to all hydrogen atoms and ions:
\[\begin{aligned} \frac{N_{2}}{N_{I}+N_{II}} & \simeq \frac{N_{2}}{N_{1}+N_{2}} \frac{N_{I}}{N_{I}+N_{II}} \\ & =\frac{N_{2} / N_{1}}{1+N_{2} / N_{1}} \frac{1}{1+N_{II} / N_{I}}, \end{aligned}\]
where we used the approximation \(N_{I} \approx N_{1}+N_{2}\) (fraction of hydrogen in higher excited states is negligible). The fractions \(N_{2} / N_{1}\) and \(N_{II}/N_{I}\) can be computed using Eqs.(3.10) and (3.13), respectively.

The electron pressure in stellar atmosphere \(P_{e}\) ranges from about 0.1 to 100 Pa, where the lower bound applies to cool stars. The following Python code computes and plots \(N_{2}/(N_{I}+N_{II})\) as function of temperature, assuming \(P_{e} \approx20 ~Pa\) (200 dyne \(cm^{-2}\) in the cgs system) as representative value for the electron pressure.

```python
import matplotlib.pyplot as plt

P_e = 20  # electron pressure in Pa

# temperature in K
T_min, T_max = 5000, 25000
T = np.arange(T_min, T_max, 100.0)

# fraction of HI in first excited state
HI2_frac = 4*np.exp(-0.75*chi/(k*T))

# plot fraction of all hydrogen in first excited state
plt.figure(figsize=(6,4), dpi=100)
plt.plot(T, 1e5*HI2_frac / ((1 + HI2_frac)*(1 + HII_frac(T, P_e))))
plt.xlim(T_min, T_max)
plt.xlabel("$T$ [K]")
plt.ylim(0, 0.9)
plt.ylabel("$10^5\,N_2/N_{\mathrm{I+II}}$")
plt.savefig("hydrogen_frac.pdf")
```

In line 38 the Boltzmann equation is applied to compute the fraction \(N_{2} / N_{1}\) for an array of temperatures ranging from 5000 to \(2.5 ×10^{4} ~K\) (variables `T_min` and `T_max` defined in line 34). Expression (3.15) is then used in the call of the plot function in lines 42–43. The resulting fraction is scaled by a factor of \(10^{5}\) to obtain numbers of order unity.

The graph in Fig.3.2 shows that \(N_{2}/(N_{I}+N_{II})\) peaks at a temperature of about 10000 K in good agreement with the observed strength of Balmer lines in the spectra of stars. This temperature is significantly lower than the temperature \(~10^{5} ~K\) for which most of the hydrogen atoms would be in an excited state. However, at such high temperatures, almost all hydrogen is ionized. As a result, the fraction \(N_{2}/(N_{I}+N_{II})\) does not exceed \(~10^{-5}\) even at the peak. Nevertheless, such a small fraction is sufficient to produce strong Balmer absorption lines in the atmospheres of A stars. The first line in the Balmer series is called Hα line and has a wavelength \(\lambda=656.45 ~nm\), which is in the red part of the spectrum. Transitions to higher levels (\(n_{2}>3\)) are seen as absorption lines \(H\beta\), Hγ, etc. at wavelengths ranging from blue to ultraviolet. Observed spectra of stars of different spectral classes can be found in [3, Sect. 9.2] and [4, Sect. 8.1].

![Fraction of hydrogen in the first excited state](hydrogen_frac.pdf)
*Fig. 3.2 Fraction \(N_{2}/(N_{I}+N_{II})\) of hydrogen in the first excited state for constant electron pressure \(P_{e} ≈20 ~Pa\) as function of temperature*

So far, we have ignored the dependence on electron pressure. Since high electron pressure suppresses ionization, it appears possible that we overestimated the decline of \(N_{2}/(N_{I}+N_{II})\) toward high temperature. To investigate the dependence on both parameters (temperature and electron pressure), it is helpful to produce a three-dimensional surface plot:

```python
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator

fig = plt.figure(figsize=(6,4), dpi=100)
ax = plt.axes(projection='3d')
P_min, P_max = 10, 100

# create meshgrid
# (x-axis: temperature, y-axis: electron pressure)
T, P_e = np.meshgrid(
    np.arange(T_min, T_max, 200.0),
    np.arange(P_min, P_max, 1.0)
)

# fraction of HI in first excited state
HI2_frac = 4*np.exp(-0.75*chi/(k*T))

# create surface plot
surf = ax.plot_surface(
    T, P_e,
    1e5*HI2_frac/((1 + HI2_frac)*(1 + HII_frac(T, P_e))),
    rcount=100, ccount=100,
    cmap='BuPu', antialiased=False
)

# customize axes
ax.set_xlim(T_min, T_max)
ax.set_xlabel("$T$ [K]")
ax.xaxis.set_major_locator(LinearLocator(5))

ax.set_ylim(P_min, P_max)
ax.set_ylabel("$P_{\mathrm{e}}$ [Pa]")

# add color bar for z-axis
cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
cbar.ax.set_ylabel("$10^5 N_2/N_{\mathrm{I+II}}$")

plt.savefig("hydrogen_frac_3d.png")
```

Surface plots can be produced with pyplot using the `mplot3d` toolkit. In line 53, a three-dimensional axes object is created (this is based on `Axes3D` imported in line 49). To define the data points from which the surface is rendered, we need a two-dimensional array of points in the \(xy\)-plane and the corresponding \(z\)-values (in our example, \(N_{2}/(N_{I}+N_{II})\) as function of \(T\) and \(P_{e}\)). The \(x\)- and \(y\)-coordinates are defined by one-dimensional arrays of temperatures and pressures in steps of 200 K and 1 Pa, respectively. The function `np.meshgrid()`, which you know from Sect. 2.3, generates a meshgrid of coordinate pairs in the \(xy\)-plane. The resulting two-dimensional arrays followed by the corresponding values of \(N_{2}/(N_{I}+N_{II})\) defined by Eq.(3.15) are passed as arguments in the call of `ax.plot_surface()` in lines 66–67. As in the two-dimensional plot above, we scale the \(Z\)-axis by a factor of \(10^5\). The optional argument `cmap='BuPu'` in line 69 specifies a colormap¹⁹, and further arguments control how the surface is rendered and displayed. The coloring of the surface corresponds to the height in \(z\)-direction, i.e. the function value, as indicated by the colorbar created in lines 79–80.

After rendering the surface, further methods are called to customize the axes. For example, `ax.set_xlim()` sets the plot range along the \(x\)-axis. The method `xaxis.set_major_locator()` can be used to set the major ticks labeled by numbers along the \(x\)-axis. Tick locating and formatting is defined in `matplotlib.ticker` (see line 50). In line 74, the tick locator is informed to use five evenly spaced ticks along the \(x\)-axis. This prevents the axis from becoming too crowded by numbers (experiment with the settings to see for yourself how the appearance of the plot is affected). All of this might sound rather complicated, but you will easily get accustomed to making such plots by starting from examples without worrying too much about the gory details.

The graphical output is shown in Fig.3.3. It turns out that the maximal fraction of excited hydrogen increases with electron pressure (this is expected because ionization is reduced), but the location of the peak is shifted only slightly from lower to higher temperature. Even for the upper bound of \(P_{e}\) in stellar atmospheres (about 100 Pa), the increase is quite moderate (little more than a factor of two compared to Fig.3.2). Of course, \(P_{e}\) and \(T\) are not really independent variables. Conditions in stellar atmospheres will roughly follow a diagonal cut through the surface shown in Fig.3.3 from low \(P_{e}\) in cool stars toward higher \(P_{e}\) in hot stars. Computing \(P_{e}\) requires a detailed model of the stellar atmosphere. For this purpose, researchers have written elaborate codes.

![3D plot of hydrogen fraction](hydrogen_frac_3d.png)
*Fig. 3.3 The same quantity as in Fig.3.2 shown as function of temperature and electron pressure*

### 3.2.2 The Balmer Jump
Balmer lines result from absorbed photons that lift electrons from the first excited state of hydrogen, \(n_{1}=2\), to higher energy levels, \(n_{2}>2\). If a photon is sufficiently energetic, it can even ionize a hydrogen atom. The condition for ionization from the state \(n_{1}=2\) is:
\[\frac{h c}{\lambda} \geq \chi_{2}=\frac{13.6 eV}{2^{2}}=3.40 eV . (3.16)\]
The corresponding maximal wavelength is 364.7 nm. Like the higher Balmer lines, it is in the ultraviolet part of the spectrum. Since ionizing photons can have any energy above \(\chi_{2}\), ionization will result in a drop in the radiative flux at wavelengths shorter than 364.7 nm rather than a line. This is called the Balmer jump.

To estimate the fraction of photons of sufficient energy to ionize hydrogen for a star of given effective temperature, let us assume that the incoming radiation is black body radiation. From the Planck spectrum (3.3), we can infer the flux below a given wavelength:
\[F_{\lambda \leq \lambda_{0}}=\pi \int_{0}^{\lambda_{0}} \frac{2 h c^{2}}{\lambda^{5}} \frac{1}{exp (h c / \lambda k T)-1} d \lambda . (3.17)\]
Since we know that the total radiative flux integrated over all wavelengths is given by Eq.(3.4), the fraction of photons with wavelength \(\lambda ≤\lambda_{0}\) is given by \(F_{\lambda ≤\lambda_{0}} / F\).

Since the integral in Eq.(3.17) cannot be solved analytically, we apply numerical integration²⁰. The definite integral of a function \(f(x)\) is the area below the graph of the function for a given interval \(x \in[a, b]\). The simplest method of numerical integration is directly based on the notion of the Riemann integral:
\[\int_{a}^{b} f(x) d x=\lim _{N \to \infty} \sum_{n=1}^{N} f\left(x_{n-1 / 2}\right) \Delta x,\]
where \(\Delta x=(b-a) / N\) is the width of the \(n\)-th subinterval and \(x_{n-1 / 2}=a+(n-1 / 2) \Delta x\) is its midpoint. The sum on the right-hand side means that the area is approximated by \(N\) rectangles of height \(f(x_{n})\) and constant width \(\Delta x\). If the function meets the basic requirements of Riemann integration (roughly speaking, if it has no poles and does not oscillate within arbitrarily small intervals), the sum converges to the exact solution in the limit \(N \to \infty\). In principle, approximations of arbitrarily high precision can be obtained by using a sufficient number \(N\) of rectangles. This is called rectangle or midpoint rule.

More efficient methods use shapes that are closer to the segments of the function \(f(x)\) in subintervals. For example, the trapezoidal rule is based on a piecewise linear approximation to the function (i.e. linear interpolation between subinterval endpoints). In this case, the integral is approximated by a composite of \(N\) trapezoids, as illustrated in Fig.3.4. The resulting formula for the integral can be readily deduced from the area \((f(x_{n-1})+f(x_{n})) \Delta x / 2\) of the \(n\)-th trapezoid:
\[\int_{a}^{b} f(x) d x \simeq\left(\frac{1}{2} f(a)+\sum_{n=1}^{N-1} f\left(x_{n}\right)+\frac{1}{2} f(b)\right) \Delta x,\]
where \(x_{n}=a+n \Delta x\) for \(0 ≤n ≤N\) are the subinterval endpoints (in particular, \(x_{0}=a\) and \(x_{N}=b\)).

The error of the approximations can be further reduced by quadratic interpolation of function values. This is the underlying idea of Simpson’s rule, which can be expressed as:
\[\int_{a}^{b} f(x) d x \simeq\left(f(a)+2 \sum_{k=1}^{N / 2-1} f\left(x_{2 k}\right)+4 \sum_{k=1}^{N / 2} f\left(x_{2 k-1}\right)+f(b)\right) \frac{\Delta x}{3} . (3.20)\]
Here, the summation index \(k\) is mapped to even and odd numbers in the first and second sum, respectively. As a result, we have the terms \(f(x_{2}), f(x_{4}), ..., f(x_{N-2})\) in the first sum and \(f(x_{1}), f(x_{3}), ..., f(x_{N-1})\) in the second sum.

We will now put these methods into practice, starting with the trapezoidal rule. Here is a straightforward implementation of Eq.(3.19) using NumPy arrays:

```python
def integr_trapez(f, a, b, n):
    """
    numerical integration of a function f(x)
    using the trapezoidal rule
    args:
        f - function f(x)
        a - left endpoint of interval
        b - right endpoint of interval
        n - number of subintervals
    returns:
        approximate integral
    """
    # integration step
    h = (b - a)/n
    # endpoints of subintervals between a+h and b-h
    x = np.linspace(a+h, b-h, n-1)
    return 0.5*h*(f(a) + 2*np.sum(f(x)) + f(b))
```

The subinterval width \(\Delta x\) is commonly denoted by \(h\) and called integration step in the numerical context. Subinterval endpoints \(x_{n}\) (excluding \(x_{0}\) and \(x_{N}\)) are organized in an array that is passed as argument to a generic function \(f()\). We implicitly assume that \(f()\) accepts array-like arguments, such as `root_bisection()` in Sect.3.1.2. The array of function values returned by \(f()\) is in turn passed to the NumPy function `sum()` to sum up all elements. Thus, the expression `np.sum(f(x))` in line 20 corresponds to the sum in Eq.(3.19).

As a simple test case, let us apply the trapezoidal rule to the integral:
\[\int_{0}^{\pi / 2} sin (x) d x=1\]
We can use the sine function from NumPy:

```python
print(" n    integr")
for n in range(10,60,10):
    print("{:2d}    {:.6f}".format(n, integr_trapez(np.sin, 0, np.pi/2, n)))
```

The output demonstrates that our implementation works and \(N=20\) subdivisions of the integration interval are sufficient to reduce the numerical error below \(10^{-3}\):
```
 n    integr
10    0.997943
20    0.999486
30    0.999772
40    0.999871
50    0.999918
```

It is also clear that increasing \(N\) further results only in minor improvements of the accuracy of the result.

Before continuing with Simpson’s rule, imagine for a moment you had chosen zero as start value of `range` in line 22. This would have thrown a `ZeroDivisionError` in the first iteration and the remainder of the loop would not have been executed (try it). The error is caused by the division through \(n\) in line 15 in the body of `integr_trapez()`. A detailed error message will point you to this line and you would probably be able to readily fix the problem. To prevent a program from crashing in the first place, Python offers a mechanism to continue with execution even in the case of an error. This is known as exception handling. In Python, exception handling can be implemented via a `try` clause followed by one or more exception clauses. They work similar to `if` and `else` clauses. Instead of evaluating a Boolean expression, Python checks if any of the exceptions specified in the exception clauses occur when the block in the `try` clause is executed. If so, some measures are taken to handle the error. Otherwise, program execution continues without further ado.

In our function for the trapezoidal rule, we can simply add `ZeroDivisionError` as an exception and print an error message without interrupting execution (explanation of function interface is omitted here):

```python
def integr_trapez(f, a, b, n):
    # integration step with exception handling
    try:
        h = (b - a)/n
    except ZeroDivisionError:
        print("Error: n must be non-zero")
        return None
    # endpoints of subintervals between a+h and b-h
    x = np.linspace(a+h, b-h, n-1)
    return 0.5*h*(f(a) + 2*np.sum(f(x)) + f(b))

print(" n    integr")
for n in range(0,60,10):
    print("{:2d}".format(n), end=" ")
    intgr = integr_trapez(np.sin, 0, np.pi/2, n)
    if intgr != None:
        print("{:.6f}".format(intgr))
```

Now we get the same output as above with an additional line indicating that zero subdivisions is not allowed:
```
 n    integr
0  Error: n must be non-zero
10  0.997943
20  0.999486
30  0.999772
40  0.999871
50  0.999918
```

This is accomplished by calculating the subinterval width in the `try` clause in lines 4–5. If \(n\) is zero, a `ZeroDivisionError` is encountered as exception (lines 6–8). After printing an error message, the function immediately returns `None`, indicating that the function did not arrive at a meaningful result for the actual arguments of the function call. To place the error message in a single line right after the value of \(n\) in the table, we split the print statement. First, the number of integration steps is printed with `end=" "` in line 17. This replaces the default newline character by two whitespaces, which separate the table columns. Then the value of the integral is printed only if the call of `integr_trapez()` in line 19 returns a value that is not `None`. Otherwise, the error message will appear.

We can even get more sophisticated though. In fact, only positive integers are allowed for the number of subintervals. In a language such as C a variable of type unsigned integer could be used and checking for zero values would be all that is needed. Since a function argument in Python does not have a particular data type, we need to convert \(n\) to an integer (assuming that the actual argument is at least a number) and check that the result is positive.

```python
def integr_trapez(f, a, b, n):
    n = int(n)
    # integration step with exception handling
    try:
        if n > 0:
            h = (b - a)/n
        else:
            raise ValueError("n must be positive")
    except ValueError as e:
        print("Invalid argument: {}".format(e))
        return None
    # endpoints of subintervals between a+h and b-h
    x = np.linspace(a+h, b-h, n-1)
    return 0.5*h*(f(a) + 2*np.sum(f(x)) + f(b))
```

After chopping off any non-integer fraction with the help of `int()` in line 2, the integration interval is subdivided in the `try` clause provided that \(n\) is greater than zero (lines 6–7). If not, a `ValueError` is raised as exception. The programmer can raise a specific exception via the keyword `raise`. We leave it as a little exercise for you to test the function and to see what happens for arbitrary values of the argument \(n\). This kind of error checking might appear somewhat excessive for such a simple application, but it can save you a lot of trouble in complex programs performing lengthy computations. Making use of exception handling is considered to be good programming practice and important for code robustness.

For Simpson’s rule (3.20), we need to ensure that the number of subintervals, \(N\), is an even integer ≥2. The following implementation of Simpson’s rule simply converts any numeric value of the argument \(n\) into a number that fulfils the requirements of Simpson’s rule. Since the user of the function might not be aware of the assumptions made about the argument, implicit changes of arguments should be used with care. In contrast, the rejection of invalid arguments via exception handling usually tells the user what the problem is. The downside is that exception handling takes more effort and results in longer code. Here, we just make you aware of different options. You need to decide which method is preferable depending on the purpose and target group of the code you write.

```python
def integr_simpson(f, a, b, n):
    """
    numerical integration of a function f(x)
    using Simpson's rule
    args:
        f - function f(x)
        a - left endpoint of interval
        b - right endpoint of interval
        n - number of subintervals (positive even integer)
    returns:
        approximate integral
    """
    # need even number of subintervals
    n = max(2, 2*int(n/2))
    h = (b - a)/n  # integration step
    # endpoints of subintervals (even and odd multiples of h)
    x_even = np.linspace(a+2*h, b-2*h, int(n/2)-1)
    x_odd = np.linspace(a+h, b-h, int(n/2))
    return (h/3)*(f(a) + 2*np.sum(f(x_even)) + 4*np.sum(f(x_odd)) + f(b))
```

In line 15, any numeric value of \(n\) is converted into an even integer with a floor of two (test different values and figure out step by step how the conversion works). The expressions in lines 24–25 correspond to the terms in Eq.(3.20), with the elements of `x_even` being the endpoints \(x_{2k}\) with even indices (excluding \(x_{0}\) and \(x_{N}\)), and `x_odd` containing those with odd indices, \(x_{2k-1}\).

A test of `integr_simpson()` shows that high accuracy is reached with relatively few integration steps:

```python
print(" n    integr")
for n in range(2,12,2):
    print("{:2d}    {:.8f}".format(n, integr_simpson(np.sin, 0, np.pi/2, n)))
```

```
 n    integr
 2    1.00227988
 4    1.00013458
 6    1.00002631
 8    1.00000830
10    1.00000339
```

The error of Simpson’s rule is of the order \(10^{-5}\) for \(N=8\) compared to \(N=50\) for the trapezoidal rule. Consequently, the slightly more complicated algorithm pays off in terms of accuracy.

We are almost prepared now to solve the integral in Eq.(3.17) numerically. To apply numerical integration, we will use a slightly modified Python function for the Planck spectrum because the factor \(1 / \lambda^{5}\) and the exponent \(h c /(\lambda k T)\) diverge toward the lower limit \(\lambda=0\) of the integral. However, analytically it follows that the combined factors do not diverge (the exponential function wins against the power function):
\[lim _{\lambda \to 0} B_{\lambda}(T)=0 .\]
Nevertheless, if you call `planck_spectrum()` defined in Sect. 3.1.2 for zero wavelength, you will encounter zero division errors. This can be avoided by shifting the lower limit of the integral from zero to a wavelength slightly above zero, for example, \(\lambda=1 ~nm\). Even so, Python will likely report a problem (it is left as an exercise to check this):
```
RuntimeWarning: overflow encountered in exp
```
The reason is that \(h c /(\lambda k T)\) is a few times \(10^{3}\) for \(\lambda=1 ~nm\) and typical stellar temperatures. For such exponents, the exponential is beyond the maximum that can be represented as a floating point number in Python (try, for instance, `np.exp(1e3)`).

We can make use of the `sys` module to obtain information about the largest possible floating point number:

```python
import sys
print(sys.float_info.max)
```

It turns out to be a very large number:
```
1.7976931348623157e+308
```

Since the exponential function increases rapidly with the exponent, we need to ensure that the argument `np.exp()` does not exceed the logarithm of `sys.float_info.max`, which is just a little above 700 (assuming the value printed above). For this reason, we use the following definition of the Planck spectrum, where a cutoff of the exponent at 700 is introduced with the help of `np.minimum()`. This function compares its arguments element-wise and selects for each pair the smaller value:

```python
def planck_spectrum(wavelength, T):
    """
    function computes Planck spectrum of a black body
    uses cutoff of exponent to avoid overflow
    args:
        numpy arrays
        wavelength - wavelength in m
        T - temperature in K
    returns:
        intensity in W/m^2/m/sr
    """
    return 2*h*c**2 / (wavelength**5 * (np.exp(np.minimum(700, h*c/(wavelength*k*T))) - 1))
```

With this modification, the Planck spectrum can be readily integrated in the interval \([\lambda_{min}, \lambda_{0}]\), where \(\lambda_{min}=1 ~nm\) and \(\lambda_{0}=364.7\) nm marks the Balmer jump. There is still a problem with applying our implementation of Simpson’s rule, though. You can easily convince yourself that executing:

```python
integr_simpson(planck_spectrum, 1e-9, 364.7e-9, 100)
```

results in an error. To understand the problem you need to recall that `planck_spectrum()` is called in place of the generic function \(f()\) in the body of `integr_simpson()`. As a result, `planck_spectrum()` will be called with only one argument (the integration variable), but it expects the temperature as second argument. To solve this problem, we need to define a proxy function for `planck_spectrum()` which accepts the wavelength as single argument. This can be easily done by means of a Python lambda, which is also known as anonymous function. In essence, a Python lambda is a shorthand definition of a function, which can be directly used in an expression (so far, defining a function and calling the function in an expression have been distinct):

```python
print("Teff [K]    flux [%]")
for Teff in T_sample:
    frac = np.pi*integr_simpson(
        lambda x: planck_spectrum(x, Teff),
        1e-9, 364.7e-9, 100
    ) / (sigma * Teff**4)
    print("{:5.0f}        {:5.2f}".format(Teff, 100*frac))
```

Instead of a function name, we use the expression beginning with the keyword `lambda` in line 50 as actual argument in the call of `integr_simpson()`. It defines the Planck spectrum for a given, but fixed temperature as an anonymous function, whose formal argument is \(x\). For each temperature in `T_sample` (see end of Sect.3.1.2), the result of the numerical integration is multiplied by the factor \(\pi / \sigma T_{eff }^{4}\) to obtain the fraction \(F_{\lambda ≤\lambda_{0}} / F\):

```
Teff [K]    flux [%]
 3130        0.13
 3590        0.46
 4290        1.71
 5778        8.43
 9940       40.87
24800       89.12
```

The percentages suggest that the Balmer jump should be prominent in the spectra of stars similar to our Sun and somewhat hotter. Although the fraction of ionizing photons increases with temperature, the amount of excited neutral hydrogen diminishes through thermal ionization at temperatures above 10000 K. This conclusion is in agreement with observed stellar spectra.

### Exercises
3.3 Explain why the so-called Ca II H and K lines produced by singly ionized calcium in the ground state are so prominent in solar-type spectra, although the fraction of calcium atoms to hydrogen atoms is only \(2 ×10^{-6}\). The reasoning is similar to the analysis of Balmer lines in Sect.3.2.1 (in fact, you will need results from this section to compare occupation numbers giving rise to K and H lines and Balmer lines). The ionization energy of neutral calcium (CaI) is \(\chi_{1}=6.11 eV\) and the partition functions are \(Z_{I}=1.32\) and \(Z_{II}=2.30\). The energy difference between the ground state and the first excited state of Ca I is \(E_{2}-E_{1}=3.12 eV\) with statistical weights \(g_{1}=2\) and \(g_{2}=4\).

3.4 Photons do not move straight through stellar interiors. They move only short distances before getting absorbed by atoms or ions, which subsequently re-emit photons. We can therefore think of a photon being frequently scattered in a stellar atmosphere. This process can be described by a simple model. If we assume that the photon moves in random direction over a constant length between two scattering events, its path can be described by a so-called random walk (see also [4], Sect. 9.3):
\[d=\ell_{1}+\ell_{2}+\cdots+\ell_{N}\]
where each step:
\[\ell_{n} \equiv\left(\Delta x_{n}, \Delta y_{n}\right)=\ell\left(cos \theta_{n}, sin \theta_{n}\right)\]
has length \(\ell\) and a random angle \(\theta_{n} \in[0,2 \pi]\) (here, we consider only the two-dimensional case to simplify the model even further). After \(N\) steps, the expectation value for the net distance over which the photon has moved is \(d=\ell \sqrt{N}\). Physically speaking, this is a diffusion process.

By making use of `np.random.random_sample(size=N)`, you can generate an array of equally distributed random numbers in the interval [0, 1] of size \(N\). By multiplying these numbers with \(2 \pi\), you obtain a sequence of random angles for which you can compute a random walk according to the above formula. Set \(\ell=1 /(\rho \kappa)\), where \(\rho\) is the density and \(\kappa\) the opacity of the gas. This is the mean free path. The density and opacity in the layers beneath the atmosphere of a solar-mass star is roughly \(\rho=10^{-6} ~g ~cm^{-3}\) and \(\kappa=50 ~cm^{2} ~g^{-1}\).

(a) Compute a random walk and use `plt.plot()` with `'o-'` as marker to show all positions \((x_{n}, y_{n})\) as dots connected by lines.
(b) Compute a series of random walks with \(N\) increasing in logarithmic steps and determine the distance \(d=|d|\) between start and end points for each walk. The function `curve_fit(func, xdata, ydata)` from `scipy.optimize` allows you to fit data points given by `xdata` and `ydata`, respectively, to a model that is defined by the Python function `func()`. Arguments of the function are an independent variable, which corresponds to `xdata`, and one or more free parameters. Fitting data to a model means that the parameters with the smallest deviation between data and model are determined, which is an optimization problem (we do not worry here about the exact mathematical meaning of deviation)²¹. To apply `curve_fit()`, you need to collect the data for \(N\) and \(d\) from your random walks in arrays, and define a Python function for the expectation value \(d=\ell \sqrt{N}\) with parameter \(\ell\). How does the resulting value of \(\ell\) compare to the mean-free path calculated above? That is to say if you knew only the random-walk data, would you be able to estimate the mean-free path from the fit? Plot your data as dots and the resulting fit function as curve to compare data and model.
(c) The total travel time of the photon over a random walk with \(N\) steps is \(t=N \ell c\), where \(c\) is the speed of light. How long would it take a photon to reach the photosphere, from which radiation is emitted into space, from a depth of \(10^{4} ~km\) (about 1% of the solar radius)?

## 3.3 Planetary Ephemerides
The trajectory followed by an astronomical object is also called ephemeris, which derives from the Latin word for “diary”. In former times, astronomers observed planetary positions on a daily basis and noted the positions in tables. If you think about the modern numerical computation of an orbit, which will be discussed in some detail in the next chapter, you can imagine positions of a planet or star being chronicled for subsequent instants, just like notes in a diary.

In Sect.2.2, we considered the Keplerian motion of a planet around a star, which neglects the gravity of other planets. The orbits of the planets in the solar system can be treated reasonably well as Kepler ellipses, but there are long-term variations in their shape and orientation induced by the gravitational attraction of the other planets, especially Jupiter. To compute such secular variations over many orbital periods with high accuracy, analytical and numerical calculations using perturbation techniques are applied. An example is the VSOP (Variations Séculaires des Orbites Planétaires) theory [8]. The solution known as VSOP87 represents the time-dependent heliocentric coordinates \(X\), \(Y\), and \(Z\) of the planets in the solar system (including Pluto) by series expansions, which are available as source code in several programming languages. We produced a NumPy-compatible transcription into Python.

The Python functions for the VSOP87 ephemerides are so lengthy that it would be awkward to copy and paste them into a notebook. A much more convenient option is to put the code into a user-defined Python module. In its simplest manifestation, a module is just a file named after the module with the extension `.py` containing a collection of function definitions. The file `vsop87.py` is part of the zip archive accompanying this chapter. You can open it in any source code editor or IDE. After a header, you will find definitions of various functions and, as you scroll down, thousands of lines summing cosine functions of different arguments (since we use the cosine from numpy, we need to import this module in `vsop87.py`). As with other modules, all you need to do to use the functions in a Python script or in a notebook is to import the module:

```python
import vsop87 as vsop
```

However, this will only work if the file `vsop87.py` is located in the same directory as the script or notebook into which it is imported. If this is not the case, you can add the directory containing the file to the module search path. Python searches modules in predefined directories listed in `sys.path`. You can easily check which directories are included by importing the `sys` module and printing `sys.path`. If you want to add a new directory, you need to append it to the environmental variable `PYTHONPATH` before starting your Python session. The syntax depends on your operating system and the shell you are using (search the web for `pythonpath` followed by the name of your operating system and you are likely to find instructions or some tutorial explaining how to proceed). Alternatively, you can always copy `vsop87.py` into the directory you are currently working.

Functions such as `vsop.Earth_X()`, `vsop.Earth_Y()`, `vsop.Earth_Z()` for the coordinates of Earth expect the so-called Julian date as argument. The Julian date is used by astronomers as a measure of time in units of days counted from a zero point that dates back to the fifth millennium B.C. (as a consequence, Julian dates for the current epoch are rather large numbers). The following Python function converts the commonly used date of the Gregorian calendar (days, months, year) and universal time (UT) to the corresponding Julian date:

```python
import math

def Julian_date(D, M, Y, UT):
    """
    converts day, month, year, and universal time into Julian date
    args:
        D - day
        M - month
        Y - year
        UT - universal time
    returns:
        Julian date
    """
    if (M <= 2):
        y = Y-1
        m = M+12
    else:
        y = Y
        m = M
    
    if (Y < 1582):
        B = -2
    elif (Y == 1582):
        if (M < 10):
            B = -2
       


       ### 3.3 Planetary Ephemerides (Continued)
The trajectory followed by an astronomical object is also called ephemeris, which derives from the Latin word for “diary”. In former times, astronomers observed planetary positions on a daily basis and noted the positions in tables. If you think about the modern numerical computation of an orbit, which will be discussed in some detail in the next chapter, you can imagine positions of a planet or star being chronicled for subsequent instants, just like notes in a diary.

In Sect.2.2, we considered the Keplerian motion of a planet around a star, which neglects the gravity of other planets. The orbits of the planets in the solar system can be treated reasonably well as Kepler ellipses, but there are long-term variations in their shape and orientation induced by the gravitational attraction of the other planets, especially Jupiter. To compute such secular variations over many orbital periods with high accuracy, analytical and numerical calculations using perturbation techniques are applied. An example is the VSOP (Variations Séculaires des Orbites Planétaires) theory [8]. The solution known as VSOP87 represents the time-dependent heliocentric coordinates \(X\), \(Y\), and \(Z\) of the planets in the solar system (including Pluto) by series expansions, which are available as source code in several programming languages. We produced a NumPy-compatible transcription into Python.

The Python functions for the VSOP87 ephemerides are so lengthy that it would be awkward to copy and paste them into a notebook. A much more convenient option is to put the code into a user defined Python module. In its simplest manifestation, a module is just a file named after the module with the extension .py containing a collection of function definitions. The file vsop87.py is part of the zip archive accompanying this chapter. You can open it in any source code editor or IDE. After a header, you will find definitions of various functions and, as you scroll down, thousands of lines summing cosine functions of different arguments (since we use the cosine from numpy, we need to import this module in vsop87.py). As with other modules, all you need to do to use the functions in a Python script or in a notebook is to import the module:

```python
import vsop87 as vsop
```

However, this will only work if the file vsop87.py is located in the same directory as the script or notebook into which it is imported. If this is not the case, you can add the directory containing the file to the module search path. Python searches modules in predefined directories listed in sys.path. You can easily check which directories are included by importing the sys module and printing sys.path. If you want to add a new directory, you need to append it to the environmental variable PYTHONPATH before starting your Python session. The syntax depends on your operating system and the shell you are using (search the web for pythonpath followed by the name of your operating system and you are likely to find instructions or some tutorial explaining how to proceed). Alternatively, you can always copy vsop87.py into the directory you are currently working.

Functions such as vsop.Earth_X(), vsop.Earth_Y(), vsop.Earth_Z() for the coordinates of Earth expect the so-called Julian date as argument. The Julian date is used by astronomers as a measure of time in units of days counted from a zero point that dates back to the fifth millennium B.C. (as a consequence, Julian dates for the current epoch are rather large numbers). The following Python function converts the commonly used date of the Gregorian calendar (days, months, year) and universal time (UT) to the corresponding Julian date:

```python
import math

def Julian_date(D, M, Y, UT):
    """
    converts day, month, year, and universal time into
    Julian date
    args:
        D - day
        M - month
        Y - year
        UT - universal time
    returns:
        Julian date
    """
    if (M <= 2):
        y = Y-1
        m = M+12
    else:
        y = Y
        m = M
    
    if (Y < 1582):
        B = -2
    elif (Y == 1582):
        if (M < 10):
            B = -2
        elif (M == 10):
            if (D <= 4):
                B = -2
            else:
                B = math.floor(y/400) - math.floor(y/100)
        else:
            B = math.floor(y/400) - math.floor(y/100)
    else:
        B = math.floor(y/400) - math.floor(y/100)
    
    return math.floor(365.25*y) + math.floor(30.6001*(m+1)) + \
           B + 1720996.5 + D + UT/24
```

The function math.floor() returns the largest integer less than or equal to a given floating point number.²²

For example, let us determine the current Julian date:

```python
from datetime import datetime

# get date and UTC now
now = datetime.utcnow()
JD = Julian_date(now.day, now.month, now.year, now.hour + now.minute/60 + now.second/3600)
print("Julian date: {:.4f}".format(JD))  # convert to Julian date
```

The function datetime.utcnow() returns the coordinated universal time (see Sect. 2.1.3) at the moment the function is called. From the object now defined in line 44, we can get the calendar day via the attribute day, the hour of the day via hour, etc. This is the input we need for converting from UTC to the Julian date. Since the argument UT of Julian_date() must be the time in decimal representation, we need to add the number of minutes divided by 60 and the number of seconds divided by 3600. When this sentence was written, the result was:

```
Julian date: 2458836.0753
```

Alternatively, you can use Astropy (see Exercise 3.6).

²²This is not identical to int(), which chops off the non-integer fraction. Apply both functions to some negative floating point number to see the difference.

For a given Julian date, we can easily compute the distance between two planets by using the VSOP87 coordinate functions of the planets. VSOP87 uses an ecliptic heliocentric coordinate system with the Sun at the center and the ecliptic being coplanar with the \(XY\) plane (i.e. Earth’s orbit is in the \(XY\) plane). For example, the distance between Earth (♁) and Mars (♂) is given by:
\[d=\sqrt{\left(X_{\oplus}-X_{\odot}\right)^{2}+\left(Y_{\oplus}-Y_{\odot}\right)^{2}+\left(Z_{\oplus}-Z_{\odot}\right)^{2}}\]
which translates into the following Python code:

```python
def Earth_Mars_dist(JD):
    delta_x = vsop.Earth_X(JD) - vsop.Mars_X(JD)
    delta_y = vsop.Earth_Y(JD) - vsop.Mars_Y(JD)
    delta_z = vsop.Earth_Z(JD) - vsop.Mars_Z(JD)
    return vsop.np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
```

At first glance, you might find it surprising that NumPy’s square root is called as vsop.np.sqrt() in the last line. But remember that numpy is imported (under the alias np) inside the module vsop, while the function Earth_Mars_dist() is not part of this module.²³ For this reason, NumPy functions such as sqrt() need to be referenced via vsop.np (dotted module names are also used in Python packages consisting of a hierarchy of modules). Of course, we could import numpy directly into the global namespace. In this case, each NumPy function would have a duplicate in vsop.np (check that both variants work).

Now execute Earth_Mars_dist() for your Julian date and print the result:

```python
print("distance between Earth and Mars now: {:.3f} AU".format(Earth_Mars_dist(JD)))
```

The answer for the Julian date 2458836.0753 is:
```
distance between Earth and Mars now: 2.278 AU
```

Since VSOP87 computes the coordinates in AU, no unit conversion is required.

A plot showing \(d\) for the next 1000 days is easily produced:

```python
import matplotlib.pyplot as plt
%matplotlib inline

t = JD + np.arange(1000)

plt.figure(figsize=(6,4), dpi=100)
plt.plot(t, Earth_Mars_dist(t))
plt.xlabel("JD [d]")
plt.ylabel("$d$ [AU]")
plt.savefig("earth_mars_distance.pdf")
```

Since the Julian date counts days, it is sufficient to add days counting from 0 to 999 to the current date JD (see line 61). By applying np.arange(), we obtain an array of dates for which distances can be directly computed and plotted. The resulting graph will look similar to what is shown in Fig.3.5 (it will be shifted depending on the chosen start date). The distance between the two planets varies with their orbital motion and becomes minimal when Earth is located just in between Mars and Sun (Mars and Sun are then said to be in opposition as seen from Earth). To determine the date when this happens, we need to find points where the first derivative with respect to time, \(\dot{d}\), vanishes. This brings us back to root finding.

![Fig. 3.5 Distance between Earth and Mars over 1000 days. Time is expressed as Julian date. The next minimum is indicated by the red dot](earth_mars_distance.pdf)

If you look into vsop87.py, you will realize that it would be impractical to calculate derivatives of the coordinate functions analytically. However, we can approximate the derivatives numerically by finite differences. We concentrate on centered differences, which are obtained by averaging the forward and backward differences of a function \(f(x)\) for discrete points on the x-axis spaced by \(\Delta x\). To second order in \(\Delta x\),²⁴ the derivative is approximated by the centered difference quotient:
\[f'(x) \equiv \frac{df}{dx} \simeq \frac{f(x+\Delta x)-f(x-\Delta x)}{2\Delta x} .\]

The following Python function implements the centered difference method for a single point or an array of points (the backward and forward coordinate difference \(h=\Delta x\) is specified as third argument):

```python
def derv_center2(f, x, h):
    """
    approximates derivative of a function
    by second-order centered differences
    args:
        f - function f(x)
        x - points for which df/dx is computed
        h - backward/forward difference
    returns:
        approximation of df/dx
    """
    return (f(x+h) - f(x-h))/(2*h)
```

As a simple test, we compute the derivative of the sine function. Since the derivative of sin(x) is cos(x), we can compare the numerical approximation to the analytic solution:

```python
h = 0.1
x = np.linspace(0, np.pi, 9)
print("analytic    cd2")
for (exact, approx) in zip(np.cos(x), derv_center2(np.sin, x, h)):
    print("{:9.6f} {:9.6f}".format(exact, approx))
```

By passing the NumPy array x defined in line 14 as argument, np.cos() and derv_center2() return arrays of analytic and approximate values, respectively, which are zipped and printed in a table via a for loop. The label cd2 is an abbreviation for centered differences of second order. In this case, the variable h is not given by the spacing of the points in the array x (in the example above, the spacing is \(\pi/8\)). Its value is used as an adjustable parameter to control the accuracy of the centered difference approximation. For \(h=0.1\), the results are:

| analytic | cd2      |
|----------|----------|
| 1.000000 | 0.998334 |
| 0.923880 | 0.922341 |
| 0.707107 | 0.705929 |
| 0.382683 | 0.382046 |
| 0.000000 | 0.000000 |
| -0.382683| -0.382046|
| -0.707107| -0.705929|
| -0.923880| -0.922341|
| -1.000000| -0.998334|

²⁴This means that the error decreases with \(\Delta x^2\) as \(\Delta x \to 0\), provided that the function is sufficiently smooth to be differentiable.
²⁵In many applications, however, h is equal to the spacing of grid points. This typically occurs when a function cannot be evaluated for arbitrary x-values, but is given by discrete data.

You can gradually decrease the value of h to investigate how the finite difference approximation converges to the derivative (remember that the derivative is defined by the differential quotient in the limit \(h \to 0\)).

In order to determine whether the function \(f(x)\) has a minimum or a maximum, we need to evaluate the second derivative, \(f''(x)\). The second-order centered difference approximation:
\[f''(x) \simeq \frac{f(x+\Delta x)-2f(x)+f(x-\Delta x)}{\Delta x^2},\]
is also readily implemented in Python:

```python
def dderv_center2(f, x, h):
    """
    approximates second derivative of a function
    by second-order centered differences
    args:
        f - function f(x)
        x - points for which df/dx is computed
        h - backward/forward difference
    returns:
        approximation of d^2f/dx^2
    """
    return (f(x+h) - 2*f(x) + f(x-h))/h**2
```

With the help of dderv_center2(), you can elaborate on the example above and determine points for which the sine function has a minimum, a maximum, or an inflection point. This is left as an exercise for you (convince yourself that your numerical results are consistent with the extrema and inflection points following from analytic considerations).

Returning to our problem of finding the next date when Mars is closest to Earth, the numerical computation of the second derivative comes in very handy if we apply yet another method to find the root of a function. This method, which is known as Newton–Raphson method (or Newton’s method), makes use of tangent lines to extrapolate from some given point to the point where the function crosses zero. If \(f(x)\) is a linear function and \(f'(x)\) its constant slope, it is a matter of elementary geometry to show that \(f(x_1)=0\) for:
\[x_1 = x - \frac{f(x)}{f'(x)} . (3.23)\]

Of course, we are interested in functions that are non-linear and for which \(f(x)=0\) cannot be found analytically. Assuming that \(f(x)\) has a root in some neighbourhood of the point \(x_0\) and provided that \(f(x)\) is differentiable in this neighbourhood, the formula for a linear function can be applied iteratively:
\[x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} . (3.24)\]

As the root is approached, \(f(x_n)\) converges to zero and the difference between \(x_n\) and \(x_{n+1}\) vanishes. If a function has multiple roots, the result depends on the choice of the start point \(x_0\).

In Python, the algorithm can be implemented as follows:

```python
def root_newton(f, df, x0, eps=1e-3, imax=100):
    """
    Newton-Raphson algorithm for finding the root of a function f(x)
    args:
        f - function f(x)
        df - derivative df/dx
        x0 - start point of iteration
        eps - tolerance
        imax - maximal number of iterations
        verbose - print additional information if true
    returns:
        estimate of x for which f(x) = 0
    """
    for i in range(imax):
        x = x0 - f(x0)/df(x0)
        if abs(x - x0) < eps:
            print("tolerance reached after {:d} iterations".format(i+1))
            print("deviation: f(x) = {:.3e}".format(f(x)))
            return x
        x0 = x
    print("exceeded {:d} iterations without reaching tolerance".format(i+1))
    return x
```

The function defined above is similar to the first version of root_bisection() in Sect.3.1.2. Instead of the endpoints of the start interval for the bisection method, a single start point x0 has to be specified, and in addition to the function f() we need to pass its derivative df() as argument. The body of root_newton() is quite simple: The iteration formula (3.24) is repeatedly applied in a for loop with a prescribed maximum number of iterations (optional argument imax). Once the difference between the previous estimate x0 and the current estimate x is smaller than the tolerance eps, the execution of the loop stops and x is returned by the function. Otherwise, the function terminates with an error message.

To test the Newton–Raphson method, let us return to the quadratic function which we used as test case for the bisection method. Choosing the start point \(x_0=0\), we get the first root as solution:

```python
def quadratic(x):
    return x**2 - x - 2

root_newton(quadratic, lambda x: 2*x - 1, 0)
```

```
tolerance reached after 5 iterations
deviation: f(x) = 2.095e-09
-1.000000000698492
```

Here, the derivative:
\[f'(x) = 2x - 1\]
is defined in the call of Newton’s method via a Python lambda (see Sect.3.2.1; alternatively, you can define the derivative separately as a named Python function). For \(x_0=10\), on the other hand:

```python
root_newton(quadratic, lambda x: 2*x - 1, 10)
```

we get:
```
tolerance reached after 5 iterations
deviation: f(x) = 1.267e-08
2.0000000042242396
```

Compared to the bisection method, Newton’s method produces highly accurate approximations after only a few iterations. The downside is that one cannot predict which root is obtained for a given start point and a recursive variant for multiple roots as in the case of the bisection method is not possible.

In the example above, the function and its derivative are defined by analytic expressions. For the distance between Earth and Mars, we use centered differences to compute derivatives numerically. By applying the Newton–Raphson method to the first time derivative of the distance, i.e. \(\dot{d}(t)\) in place of \(f(x)\), we get an extremum of \(d(t)\). Instead of \(f'(x)\), the second derivative of the distance \(\ddot{d}(t)\) is required as input. To calculate the derivatives, we apply derv_center2() and dderv_center2():

```python
delta_t = 0.1
JD_extrem = root_newton(
    lambda t: derv_center2(Earth_Mars_dist, t, delta_t),
    lambda t: dderv_center2(Earth_Mars_dist, t, delta_t),
    JD + 300,
    eps=delta_t
)

print("\ndistance = {1:.3f} AU in {0:.0f} days ({:4.0f}-{:02.0f}-{:02.0f})".format(
    JD_extrem - JD,
    Earth_Mars_dist(JD_extrem),
    vsop.JD_year(JD_extrem),
    vsop.JD_month(JD_extrem),
    vsop.JD_day(JD_extrem)
))
```

To understand the call of root_newton(), it is important to keep in mind that functions with only a single argument are assumed in line 48 in the body of root_newton(). However, derv_center2() and dderv_center2() have several arguments (see definitions above). For this reason, we use lambda to define anonymous functions of the variable t returning centered difference approximations for a given function (Earth_Mars_dist) and timestep (delta_t). The Newton–Raphson iteration starts at the current Julian date JD plus 300 days (see line 70). In our example, this results in:

```
tolerance reached after 3 iterations
deviation: f(x) = 6.209e-13

distance = 0.415 AU in 307 days (2020-10-06)
```

It turns out that the initial guess of 300 days was pretty close. To print the corresponding date in standard format, the Julian date is converted with the help of JD_year, JD_month, and JD_day from vsop87 (lines 74–77). The solution is shown as red dot in Fig.3.5 (we leave it to you to complete the code). It turns out that the distance to Mars reaches a minimum in October 2020.

The solution you get will depend on your initial date and start point for the Newton–Raphson method. To verify whether your result is a minimum or a maximum, evaluate:
```python
dderv_center2(Earth_Mars_dist, JD_extrem, delta_t)
```
If the sign of the second derivative is positive, the distance is minimal, otherwise it is maximal. At the time of its closest approach, Mars appears particularly bright on the night sky. If you are enthusiastic about observing the sky, the date following from your calculation might be worthwhile to note.

### Exercises
3.5 Apply centered differences to calculate the fastest change of the day length in minutes per day at your geographical latitude (see Sect.2.1.2).

3.6 Planetary ephemerides are included in astropy.coordinates. For example, to get the barycentric coordinates of Mars at a particular date,²⁶ you can use the code:
```python
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric

solar_system_ephemeris.set('builtin')
get_body_barycentric('mars', Time("2019-12-18"))
```
In this case, the computation is based on Astropy’s built-in ephemeris.²⁷

Rewrite Earth_Mars_dist() using get_body_barycentric() for the computation of the distance from Earth to Mars and produce a plot similar to Fig.3.5. For the time axis, you can define an array of days similar to elapsed in Sect. 2.1.3. When calling Earth_Mars_dist(), you need to add the array to a Time object. You can express time also as Julian date by using the format attribute.²⁸

3.7 Starting from an initial date of your choice, investigate possible Hohmann transfer orbits to Mars (see Exercise 2.10) over a full orbital period (687 days). For each day, use trigonometry and the ephemerides of Earth and Mars to compute the angular separations \(\delta\) between the two planets at launch time and the angular change \(\Delta\varphi = \varphi' - \varphi\) in the position of Mars over the transfer time \(t_H\). Neglecting the inclination of the orbital plane of Mars against the ecliptic, these two angles should add up to 180° (one half of a revolution) for a Hohmann transfer, i.e. \(\delta + \Delta\varphi = 180^\circ\). Which launch dates come closest to satisfying this condition? However, the parameters of the transfer trajectory are based on the assumption that the orbit of Mars is circular. In fact, Mars has the highest eccentricity of all planets in the solar system. Based on radial distances from the Sun, estimate by what distance is the spaceship going to miss Mars when it reaches the aphelion.²⁹

3.8 From all planets in the solar system, what is the largest distance between two planets going to be in the course of the next 165 years (the time needed by Neptune to complete one full revolution around the Sun)?

²⁶The origin of barycentric coordinates is the center of mass of the solar system. This coordinate frame is also known as International Celestial Reference System (ICRS).
²⁷There are options for more precise positions; see docs.astropy.org/en/stable/coordinates/solarsystem.html for further details.
²⁸See docs.astropy.org/en/stable/time.
²⁹Determining a trajectory with sufficient accuracy for a space mission is quite challenging and requires exact orbital elements and solutions of the equations of motion. Moreover, it is a complicated optimization problem to meet constraints such as fuel consumption and travel time. As a result, various modifications are made. For example, other types of Hohmann transfer trajectories intersect the orbit of the target prior to or after reaching the aphelion. Many space missions, such as the famous Voyager missions, utilize the gravity of planets during flybys to alter their trajectories.