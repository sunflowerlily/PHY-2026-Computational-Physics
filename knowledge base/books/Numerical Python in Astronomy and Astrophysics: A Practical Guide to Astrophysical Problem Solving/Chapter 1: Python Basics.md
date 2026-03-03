我来将这份PDF文档（第1章）的内容转换为Markdown格式：

```markdown
# Chapter 1: Python Basics

**Abstract:** This chapter explains basic programming concepts. After an overview of common Python distributions, we show how to use Python as a simple calculator. As a first step toward programming, variables and expressions are introduced. The arithmetic series and Fibonacci numbers illustrate the concepts of iteration and branching. We conclude this chapter with a program for the computation of a planet's orbital velocity around the Sun, using constants and functions from libraries and giving a small glimpse at objects in Python.

---

## 1.1 Using Python

There is quite a variety of Python installations. Depending on the operating system of your computer, you might have some basic Python preinstalled. Typically, this is the case on Linux computers. However, you might find it rather cumbersome to use, especially if you are not well experienced with writing source code in elementary text editors and executing the code on the command line. What is more, installing additional packages typically requires administrative privileges. If you work, for example, in a computer lab it is likely that you do not have the necessary access rights. Apart from that, Python version 2.x is still in use, while this book is based on version 3.

Especially as a beginner, you will probably find it convenient to work with a GUI (graphical user interface). Two popular choices for Python programming are:

- **Spyder** (www.spyder-ide.org): A classical IDE (integrated development environment) which allows you to edit code, execute it and view the output in different frames.
- **Jupyter** (jupyter.org): Can be operated via an arbitrary web browser. It allows you to run an interactive Python session with input and output cells. Apart from input cells for typing Python source code, there are so-called markdown cells for writing headers and explanatory text. This allows you to use formatting similar to elementary HTML for webpages. A valuable feature is the incorporation of LaTeX to display mathematical expressions.

A powerful all-in-one solution is **Anaconda**, a Python distribution and package manager that can be installed under Windows, macOS or Linux by any user (see docs.anaconda.com for more information). Anaconda provides a largely autonomous environment with all required components and libraries on a per-user basis.

### Hello, Universe!

As a first step, check if you can run the traditional "Hello, World!" example. Being astronomers, we use a slightly modified version:

```python
# 1
print("Hello, Universe!")
```

After executing the print statement, you should see:
```
Hello, Universe!
```

The quotes in the source code signify that the enclosed characters form a **string**. The `print()` function puts the string specified in parentheses on the screen.

**Note:** Enclosing the string in parentheses is obligatory in Python 3. You may find versions of "Hello, World!" without parentheses on the web, which work only with Python 2.

---

## 1.2 Understanding Expressions and Assignments

Apart from printing messages on the screen, Python can be used as a scientific calculator. Let us begin with an example from astronomy: calculating the velocity at which Earth is moving along its orbit around the Sun.

For simplicity, we treat the orbit as circular (in fact, it is elliptical with a small eccentricity of 0.017). From the laws of circular motion:

$$v = \frac{2\pi r}{P}$$

where $r$ is the orbital radius and $P$ is the period (one year for Earth).

### Calculator Example

```python
2*3.14159*1.496e8/3.156e7
```

Output:
```
29.783388086185045
```

This is the orbital velocity in km/s.

**Explanation:**
- `2` is an integer literal
- `3.14159` is a floating-point literal (fixed-point decimal notation)
- `1.496e8` is scientific notation for $1.496 \times 10^8$ (the character `e` followed by an integer indicates the exponent)
- `*` and `/` are multiplication and division operators

### Variables and Assignments

Turning the example into a Python program with **variables**:

```python
# 1
radius = 1.496e8    # orbital radius in km
# 2
period = 3.156e7    # orbital period in s
# 3
# 4
# calculate orbital velocity
# 5
velocity = 2*3.14159*radius/period
```

**Key points:**
- Each **assignment** binds the value of the expression on the right-hand side of the equality sign `=` to a **name** on the left-hand side
- A value with a name is called a **variable** in Python
- Text after `#` is a **comment** (not executed)

To see the result, add a print statement:

```python
# 6
print(velocity)
```

Or better, with descriptive output:

```python
# 7
print("orbital velocity =", velocity, "km/s")
```

Output:
```
orbital velocity = 29.783388086185045 km/s
```

### Formatting Output

To control the number of displayed digits:

```python
# 8
print("orbital velocity = {:5.2f} km/s".format(velocity))
```

Output:
```
orbital velocity = 29.78 km/s
```

**Format specifier `5.2f`:**
- `5`: total number of digits (including decimal point)
- `.2`: 2 digits after the decimal point
- `f`: fixed-point notation

Alternative: exponential notation with `e`:
```python
print("new orbital radius = {:.3e} km".format(radius))
```

### Variable Reassignment

Variables can be changed:

```python
# 9
radius = 10*radius
# 10
print("new orbital radius = {:.3e} km".format(radius))
```

Output:
```
new orbital radius = 1.496e+09 km
```

**Important:** The assignment operator `=` in Python means **"set to"**, not "is equal to". The statement `radius = 10*radius` means:
1. Take the current value of `radius`
2. Multiply by 10
3. Reassign the result to `radius`

### Kepler's Third Law

For a planet at a different distance, the period also changes. From Kepler's third law:

$$P^2 = \frac{4\pi^2}{GM}r^3$$

where $M = 1.989 \times 10^{30}$ kg (mass of Sun) and $G = 6.674 \times 10^{-11}$ N kg⁻² m² (gravitational constant).

Solving for $P$:
$$P = 2\pi(GM)^{-1/2}r^{3/2}$$

Python code:

```python
# 11
# calculate period in s from radius in km (Kepler's third law)
# 12
period = 2*3.14159*(6.674e-11*1.989e30)**(-1/2)*\
# 13
         (1e3*radius)**(3/2)
# 14
# print period in yr
# 15
print("new orbital period = {:.1f} yr".format(period/3.156e7))
# 16
# 17
velocity = 2*3.14159*radius/period
# 18
print("new orbital velocity = {:.2f} km/s".format(velocity))
```

Output:
```
new orbital period = 31.6 yr
new orbital velocity = 9.42 km/s
```

**Important notes on units:**
- The mass of the Sun and gravitational constant are in **SI units**
- The radius is in km, so we convert to meters with `1e3*radius`
- One year = $3.156 \times 10^7$ seconds

The backslash `\` at the end of line 12 continues an expression to the next line.

**Warning:** Wrong unit conversion is a common source of error. A famous example is the loss of NASA's Mars Climate Orbiter due to inconsistent use of metric and imperial units.

---

## 1.3 Control Structures

The computation of orbital velocity involves:
1. **Initialization** of input data
2. **Computational rules** (mathematical formulas)
3. **Output** of results

A common generalization is **iteration**: repeated execution of the same computational rule.

### For Loops: Arithmetic Series

Sum of first 100 natural numbers (arithmetic series):
$$s_n \equiv \sum_{k=1}^{n} k = 1 + 2 + 3 + \ldots + n$$

Python implementation:

```python
# 1
sum = 0              # initialization
# 2
n = 100              # number of iterations
# 3
# 4
for k in range(1, n+1):   # k running from 1 to n
# 5
    sum = sum + k    # iteration of sum
# 6
# 7
print("Sum =", sum)
```

Output:
```
Sum = 5050
```

**Key points:**
- `for k in range(1, n+1)`: loop counter `k` runs through integers 1, 2, ..., n
- **Important:** Python includes the start value (1) but **excludes** the stop value (n+1)
- The **indented block** following the colon is executed for each value of `k`
- Indentations must be consistent (use one tab per indentation)

![Illustration of for loop computation](figure_1_1.png)

**Figure 1.1:** Illustration of the computation of the sum $s_{100}$ via a for loop

**Note:** The young Carl Friedrich Gauss discovered the closed-form formula:
$$s_n = \frac{n(n+1)}{2}$$

### Fibonacci Sequence

The **Fibonacci sequence** is defined by the recursion:
$$F_{n+1} = F_n + F_{n-1} \quad \text{for} \quad n \geq 1$$

with initial values:
$$F_0 = 0, \quad F_1 = 1$$

Python program:

```python
# 1
# how many numbers are computed
# 2
n_max = 10
# 3
# 4
# initialize variables
# 5
F_prev = 0           # 0. number
# 6
F = 1                # 1. number
# 7
# 8
# compute sequence of Fibonacci numbers
# 9
for n in range(1, n_max+1):
# 10
    print("{:d}. Fibonacci number = {:d}".format(n, F))
# 11
# 12
    # next number is sum of F and the previous number
# 13
    F_next = F + F_prev
# 14
# 15
    # prepare next iteration
# 16
    F_prev = F       # first reset F_prev
# 17
    F = F_next       # then assign next number to F
```

Output:
```
1. Fibonacci number = 1
2. Fibonacci number = 1
3. Fibonacci number = 2
4. Fibonacci number = 3
5. Fibonacci number = 5
6. Fibonacci number = 8
7. Fibonacci number = 13
8. Fibonacci number = 21
9. Fibonacci number = 34
10. Fibonacci number = 55
```

**Alternative: f-strings (Python 3.6+)**
```python
print(f"{n:d}. Fibonacci number = {F:d}")
```

![Illustration of Fibonacci computation](figure_1_2.png)

**Figure 1.2:** Illustration of the recursive computation of the Fibonacci sequence

### While Loops

For situations where the number of iterations is not known in advance:

```python
# 1
# initialize variables
# 2
F_prev = 0           # 0. number
# 3
n, F = 1, 1          # 1. number (multiple assignment)
# 4
# 5
# compute sequence of Fibonacci numbers smaller than 1000
# 6
while F < 1000:
# 7
    print("{:d}. Fibonacci number = {:d}".format(n, F))
# 8
# 9
    # next number is sum of F and the previous number
# 10
    F_next = F + F_prev
# 11
# 12
    # prepare next iteration
# 13
    F_prev = F       # first reset F_prev
# 14
    F = F_next       # then assign next number to F
# 15
    n += 1           # increment counter
```

**Key points:**
- `while F < 1000:` repeats as long as the condition is `True`
- `F < 1000` is a **Boolean expression** (evaluates to `True` or `False`)
- Multiple assignment: `n, F = 1, 1` assigns 1 to both `n` and `F`
- `n += 1` increments `n` by 1 (equivalent to `n = n + 1`)

### Branching: If-Else Statements

Count even and odd Fibonacci numbers:

```python
# 1
# initialize variables
# 2
F_prev = 0
# 3
F = 1
# 4
n_even = 0
# 5
n_odd = 0
# 6
# 7
# compute sequence of Fibonacci numbers smaller than 1000
# 8
while F < 1000:
# 9
    # next number is sum of F and the previous number
# 10
    F_next = F + F_prev
# 11
# 12
    # prepare next iteration
# 13
    F_prev = F
# 14
    F = F_next
# 15
# 16
    # test if F is even (divisible by two) or odd
# 17
    if F % 2 == 0:       # modulo operator % gives remainder
# 18
        n_even += 1
# 19
    else:
# 20
        n_odd += 1
# 21
# 22
print("Found {:d} even and {:d} odd Fibonacci numbers".\
# 23
      format(n_even, n_odd))
```

Output:
```
Found 5 even and 11 odd Fibonacci numbers
```

**Important:** Do not confuse `==` (comparison, "is equal to") with `=` (assignment, "set to").

---

## 1.4 Working with Modules and Objects

Python offers a collection of useful tools in the **Python Standard Library** (docs.python.org/3/library). Functions such as `print()` are **built-in functions**. Many more optional **libraries** (also called **packages**) are available.

### Importing Modules

**Example: Physical constants from SciPy**

```python
# 1
import scipy.constants

# View all names in module
dir(scipy.constants)

# Access constant
print(scipy.constants.gravitational_constant)
# Output: 6.67408e-11

# Same value via shorthand
print(scipy.constants.G)
```

**Using an alias:**
```python
import scipy.constants as const
print(const.G)
```

**Importing specific names:**
```python
from scipy.constants import G
print(G)
```

**Caution:** Importing via `from` can cause name conflicts with your own variables.

### Improved Orbital Velocity Program

Using library constants:

```python
# 1
from math import pi, sqrt
# 2
from astropy.constants import M_sun
# 3
from scipy.constants import G, au, year
# 4
# 5
print("1 au =", au, "m")
# 6
print("1 yr =", year, "s")
# 7
# 8
radius = 10 * au
# 9
print("\nradial distance = {:.1f} au".format(radius/au))
# 10
# 11
# Kepler's third law
# 12
period = 2 * pi * sqrt(radius**3 / (G * M_sun.value))
# 13
print("orbital period = {:.4f} yr".format(period/year))
# 14
# 15
velocity = 2 * pi * radius / period    # velocity in m/s
# 16
print("orbital velocity = {:.2f} km/s".format(1e-3*velocity))
```

Output:
```
1 au = 149597870691.0 m
1 yr = 31536000.0 s

radial distance = 10.0 au
orbital period = 31.6450 yr
orbital velocity = 9.42 km/s
```

**Key features:**
- `pi` and `sqrt` from `math` module
- `M_sun` from `astropy.constants` (includes value, uncertainty, unit, reference)
- `G`, `au`, `year` from `scipy.constants`
- `M_sun.value` extracts just the numerical value
- `\n` inserts a newline (blank line)

### Objects in Python

**Basic facts about objects:**
1. Everything in Python is an object
2. An object contains a particular kind of data
3. Objects have **methods** to manipulate the object's data
4. A method can change an object or create a new one

**Example: The `M_sun` object**

Printing `M_sun` shows:
```
Name   = Solar mass
Value  = 1.9884754153381438e+30
Uncertainty = 9.236140093538353e+25
Unit   = kg
Reference = IAU 2015 Resolution B 3 + CODATA 2014
```

- **Attributes**: `value`, `uncertainty`, `unit`, etc.
- Access with dot notation: `M_sun.value`
- Both `M_sun` and `M_earth` belong to class `Quantity` (same attributes, different data)

**Methods vs. Functions:**
- `format()` is a **method** of string objects
- Must be called with an object: `"string".format(variable)`
- Similar syntax to attributes, but with parentheses for arguments

---

## Summary

This chapter covered:

| Topic | Key Concepts |
|-------|-------------|
| Python environments | Spyder, Jupyter, Anaconda |
| Basic syntax | `print()`, strings, comments |
| Variables | Assignment `=`, naming, reassignment |
| Data types | Integers, floats, scientific notation |
| Operators | `+`, `-`, `*`, `/`, `**` (power), `%` (modulo) |
| Formatting | `format()`, f-strings, `f`/`e` notation |
| Control structures | `for` loops, `while` loops, `if-else` branching |
| Modules | `import`, aliases, `from...import` |
| Objects | Attributes, methods, classes |

**Important formulas:**
- Circular orbital velocity: $v = 2\pi r / P$
- Kepler's third law: $P^2 = \frac{4\pi^2}{GM}r^3$
- Arithmetic series: $s_n = \sum_{k=1}^{n} k = \frac{n(n+1)}{2}$
- Fibonacci recurrence: $F_{n+1} = F_n + F_{n-1}$
```