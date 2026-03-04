# Chapter 2 Computing and Displaying Data
NumPy arrays are the workhorses of numerics in Python, extending it by remarkable numerical capabilities. For example, they can be used just like simple variables to evaluate an arithmetic expression for many different values without programming a loop. In the first section, we combine the power of NumPy and Astropy and compute the positions of objects on the celestial sphere. Moreover, we introduce Matplotlib to produce plots from array data. Further applications are shown in the context of Kepler’s laws and tidal forces, for example, printing formatted tables and plotting vector maps.

## 2.1 Spherical Astronomy
In astronomy, the positions of stars are specified by directions on the sky, i.e. two angular coordinates. The radial distance of the star from Earth would be the third coordinate, but distances are not known for all astronomical objects. As long as distances do not matter, all astronomical objects can be projected in radial directions onto a sphere with Earth at its center (the size of the sphere does not matter, but you can think of it as a distant spherical surface). This is the so-called celestial sphere¹.

For an observer on Earth, the position of astronomical objects depends on geographical latitude and longitude and varies with the time of day. To specify positions independent of the observer, angular coordinates with respect to fixed reference directions are used. In the equatorial coordinate system, one reference direction is given by Earth’s rotation axis (or, equivalently, the orientation of the equatorial plane). The orientation of the rotation axis is fixed because of angular momentum conservation².

The angular distance of a star from the equatorial plane is called declination and denoted by $\delta$. The other reference direction is defined by the intersection between the equatorial plane and the plane of Earth’s orbital motion around the Sun. The fixed orientation of the orbital plane, which is called ecliptic, is also a consequence of angular momentum conservation (in this case the angular momentum of orbital motion). The second coordinate in the equatorial system, which is called right ascension $\alpha$, is the angle measured from one of the two points where the celestial sphere is pierced by the line of intersection of the equatorial an orbital planes. The zero point for the right ascension is known as vernal equinox, the opposite point as autumnal equinox. If all of this sounds rather complicated, it will become clear from the illustration in Fig.2.1. See also [3, Sect. 2.5].

*Fig. 2.1 Celestial sphere with coordinates $\alpha$ (right ascension) and $\delta$ (declination) of a stellar object. Earth’s orbital plane (ecliptic) intersects the sphere along the red circle, which is inclined by the angle $\epsilon_{0}$ (obliquity) with respect to the celestial equator. The celestial equator is the outward projection of Earth’s equator onto the celestial sphere. The intersection points of the ecliptic and the celestial equator are the two equinoxes*
> north | celestial pole | celestial equator | ecliptic | south celestial pole | autumnal equinox | $\delta$ | $\epsilon_0$ | $\alpha$ | vernal equinox

### 2.1.1 Declination of the Sun
While the declination of stars is constant, the position of the Sun changes in the equatorial system over the period of a year. This is a consequence of the inclination of Earth’s rotation axis with respect to the direction perpendicular to the ecliptic, which is equal to $\epsilon_{0}=23.44^{\circ}$. The angle $\epsilon_{0}$ is called obliquity of the ecliptic. The annual variation of the declination of the Sun is approximately given by³:
$$\delta_{\odot}=-arcsin \left[sin \epsilon_{0} cos \left(\frac{360^{\circ}}{365.24}(N+10)\right)\right]$$
where $N$ is the difference in days starting from 1st January. So the first day of the year corresponds to $N=0$, and the last to $N=364$ (unless it is a leap year). The fraction $360^\circ/365.24$ equals the change in the angular position of Earth per day, assuming a circular orbit. This is just the angular velocity $\omega$ of Earth’s orbital motion around the Sun in units of degrees per day⁴.

The Sun has zero declination at the equinoxes (intersection points of celestial equator and ecliptic) and reaches $\pm \epsilon_{0}$ at the solstices, where the rotation axis of the Earth is inclined towards or away from the Sun. The exact dates vary somewhat from year to year. In 2020, for instance, equinoxes were on 20th March and 22nd September and solstices on 20th June and 21st December (we neglect the exact times in the following). In Exercise 2.2 you are asked to determine the corresponding values of $N$. For example, the 20th of June is the 172nd day of the year 2020. Counting from zero, we thus expect the maximum of the declination $\delta_{\odot}=\epsilon_{0}$ (first solstice) for $N=171$. Let us see if this is consistent with the approximation (2.1). The following Python code computes the declination $\delta_\odot$ based on this formula for a given value of $N$:

```python
import math
N = 171 # day of 1st solstice
omega = 2*math.pi/365.24 # angular velocity in rad/day
ecl = math.radians(23.44) # obliquity of the ecliptic
# approximate expression for declination of the Sun
delta = -math.asin(math.sin(ecl)*math.cos(omega*(N+10)))
print("declination = {:.2f} deg".format(math.degrees(delta)))
```

The result:
```
declination = 23.43 deg
```

To calculate the declination for the second solstice and also for the equinoxes, we need to evaluate the code in line 8 for the corresponding values of $N$. If you put the code listed above into a Python script, you can change the value assigned to the variable $N$ and simply re-run the script. While this is certainly doable for a few different values, it would become too tedious for many values (we will get to that soon enough). Ideally, we would like to compute the Sun’s declination for several days at once. This can be done by using data structures know as arrays. An array is an ordered collection of data elements of the same type. Here is as an example:

```python
import numpy as np
N = np.array([79, 171, 265, 355]) # equinoxes and solstices in 2020
```

In contrast to other programming languages, arrays are not native to Python. They are defined in the module numpy (the library name is also written as NumPy, see www.numpy.org), which is imported under the alias np in line 10. The function `np.array()` takes a list of values in brackets and, if possible, creates an array with these values as elements. Like an array, a list is also an ordered collection of data elements. In this book, we will rarely make use of lists (see, for example, Sect. 5.5). They are more flexible than NumPy arrays, but flexibility comes at the cost of efficiency. This is demonstrated in more detail in Appendix B.1. On top of that, NumPy offers a large toolbox of numerical methods which are specifically implemented to work with arrays⁵. The array returned by `np.array()` is assigned to the variable $N$ (mark the difference between single value versus array in lines 3 and 13, respectively). Its main properties can be displayed by the following print statements:

```python
print(N)
print(N.size)
print(N.dtype)
```

which produces the output:
```
[ 79 171 265 355]
4
int64
```

From this we see that $N$ has four elements (the number of elements is obtained with the `.size` attribute), which are the integers 79, 171, 256, and 355. The data type can be displayed with the `.dtype` attribute (by default, 64-bit integers are used for literals without decimal point).

How can we work with the values in an array? For example, $N[0]$ refers to the first element of the array, which is the number 79. Referring to a single element of an array via an integer in brackets, which specifies the position of the element in the array, is called indexing. The first element has index 0, the second element index 1 and so on (remember, this is Python’s way of counting). You can also index elements from the end of the array. The last element has index −1, the element before the last one has index −2, etc. So, for the array defined above:

```python
print(N[-3])
print(N[1])
```

outputs:
```
171
171
```

Do you see why the value 171 is printed in both cases? Vary the indices and see for yourself what you get. Before proceeding, let us summarize the defining properties of an array:
- Every element of an array must have the same data type.
- Each element is identified by its index.

Having defined $N$ as an array, we could calculate the declination of the Sun on day 171 (the first solstice) by copying the code from line 8 and replacing $N$ by $N[1]$ in the expression for delta. Of course, this would not bring us any closer to calculating the declination of the Sun for all four days at once. With NumPy, it can be done as follows:

```python
delta = -np.arcsin(math.sin(ecl) * np.cos(omega*(N+10)))
print(np.degrees(delta))
```

In short, the expression in line 19 is evaluated for each element of the array $N$ and the results are stored in a new array that is assigned to delta. The four elements of delta are the values of the declination for the two equinoxes and solstices:
```
[ -0.9055077 23.43035419 -0.41950731 -23.43978827]
```

Not perfect (the declination at equinoxes should be zero), but reasonably close. We use only an approximate formula after all.

To get a better idea of how the code in line 19 works, we expand it into several steps and use a temporary array called tmp for intermediate results of the calculation:

```python
# add 10 to each element of N
tmp = N+10
print(tmp)
print(tmp.dtype)

# multipy by omega
tmp = omega*tmp
print(tmp)
print(tmp.dtype)

# calculate the cosine of each element in the resulting array
# and multipy with the sine of the obliquity
tmp = math.sin(ecl)*np.cos(tmp)
print(tmp)

# calculate the negative arcsine of each element
delta = -np.arcsin(tmp)
print(np.degrees(delta))
```

As you can see, it is possible to perform arithmetic operations on arrays. For operators such as `+` and `*`, the operands must be (see also Fig.2.2):
- either an array and a single number,
- or two arrays of identical shape (for arrays with only one index this amounts to the same number of elements).

For example, we make use of the first option in line 22, where the number 10 is added to each element of the array $N$. The resulting integers are assigned element-wise to the array tmp:
```
[ 89 181 275 365]
int64
```

The next step is an element-wise multiplication with omega (Earth’s angular velocity defined in line 4). Since the value of omega is a floating point number, the tmp array is automatically converted from data type integer to float:
```
[1.53105764 3.11372396 4.73079608 6.27905661]
float64
```

Now we have the angular positions of Earth on its orbit, from which the vertical distances of the Sun from the celestial equator can be computed. In line 33, the NumPy function `np.cos()` is used to compute the cosine of each value in the tmp array, while `math.sin()` can take only a single-valued argument, which is ecl (the obliquity of the ecliptic). The product is:
```
[ 0.01580343 -0.39763404 0.00732172 0.39778512]
```

and, after computing the arcsine of each element with `np.arcsin`, we finally get the declinations:
```
[ -0.9055077 23.43035419 -0.41950731 -23.43978827]
```

While doing things step by step is helpful for beginners, combining all these steps into the single statement shown in line 19 is extremely useful for the more experienced programmer. Starting with the code for a single day (see line 8), the only modification that has to be made is that the math module has to be replaced by numpy whenever the argument of a function is an array. However, there is small pitfall. By comparing the code examples carefully, you might notice that the identifiers for the arcsine function read `math.asin()` and `np.arcsin()` in lines 8 and 19, respectively.

*Fig. 2.2 Illustration of basic NumPy operations. Adding a number (variable) to an array, means that the same number is added to each element in the array (left). If two arrays of size n are added, the operator + is applied element-wise (right)*

A likely mistake is to replace `math.asin()` by `np.asin()`, which would cause Python to throw the following error message:
```
AttributeError: module ’numpy’ has no attribute ’asin’
```

Since math and numpy are independent modules, you cannot expect that the naming of mathematical functions is always consistent.

Printing an array, results in all elements of the array being displayed in some default format. Now, suppose we want to format the elements nicely as we did at the beginning of this section before introducing arrays. Formatted printing of a particular element of an array is of course possible by indexing the element. For example:

```python
print("declination = {:.2f} deg". format(math.degrees(delta[1])))
```

produces the same output as line 9 (where delta is a simple variable):
```
declination = 23.43 deg
```

To display all elements in a formatted table, we need to loop through the array. Actually, we have already worked with such loops, for example, in line 19. Loops of this type are called implicit. The following example shows an explicit for loop:

```python
for val in delta:
    print("declination = {:6.2f} deg".format(math.degrees(val)))
```

The loop starts with the first element in the array delta, assigns its value to the variable val, which is the loop variable (similar to the loop counter introduced in Sect.1.3), and then executes the loop body. The loop in the example above encompasses only a single print statement. After executing this statement, the loop continues with the next element and so on until the end of the array (the highest index) is reached:
```
declination = -0.91 deg
declination = 23.43 deg
declination = -0.42 deg
declination = -23.44 deg
```

However, the output is not really satisfactory yet. While repeatedly printing declination is redundant, important information for understanding the data is missing. In particular, the days to which these values refer are not specified. A better way of printing related data in arrays is, of course, a table. In order to print the days and the corresponding declinations, we need to simultaneously iterate through the elements of $N$ and delta. One solution is to define a counter with the help of Python’s `enumerate()` function:

```python
print("i day delta [deg]")
for i,val in enumerate(delta):
    print("{1:d} {2:3d} {0:8.2f}".format(math.degrees(val),i,N[i]))
```

Compared to the for loops discussed in Sect.1.3, the range of the counter $i$ is implicitly given by the size of an array: It counts through all elements of delta and, at the same time, enables us to reference the elements of $N$ sequentially in the loop body. Execution of the loop produces the following table:
```
i day delta [deg]
0 79    -0.91
1 171   23.43
2 265   -0.42
3 355   -23.44
```

Here, the arguments of `format()` are explicitly ordered. The placeholder `{1:d}` in line 46 indicates that the second argument (index 1 before the colon) is to be inserted as integer at this position. The next placeholder refers to the third argument (index 2 before the colon) and the last one to the first argument. The format specifiers ensure sufficient space between the columns of numbers (experiment with the settings). The header with labels for the different columns is printed in line 44 (obviously, this has to be done only once before the loop begins).

Surely, instead of enumerating delta, you could just as well enumerate $N$. Is it possible to write a loop that simultaneously iterates both arrays without using an explicit counter? Actually, this is the purpose of the `zip()` function, which aggregates elements with the same index from two or more arrays of equal length. In this case, the loop variable is a tuple containing one element from each array. We will take a closer look at tuples below. All you need to know for the moment is that the tuple row in the following code example contains one element of $N$ and the corresponding element of delta, forming one row of the table we want to print. Tuple elements are indexed like array elements, so row[0] refers to the day and row[1] to the declination for that day.

```python
print("day delta [deg]")
for row in zip(N,delta):
    print("{0:3d} {1:8.2f}". format(row[0],math.degrees(row[1])))
```

Apart from the index column, we obtain the same output as above:
```
day delta [deg]
79    -0.91
171   23.43
265   -0.42
355   -23.44
```

If you replace lines 50–51 by the unformatted print statement `print(row)`, you will get:
```
(79, -0.01580409076383853)
(171, 0.40893682550286947)
(265, -0.007321783769611206)
(355, -0.4091014813515704)
```

While brackets are used for lists and arrays, tuples are enclosed by parentheses. The most important difference is that tuples are immutable, i.e. it is not possible to add, change or remove elements. For example, the tuples shown above are fixed pairs of numbers, similar to coordinates $(x, y)$ for points in a plane. Suppose you want to change day 355 to 364. While it is possible to modify array $N$ by setting $N[3]=364$, you are not allowed to assign a value to an individual element in a tuple, such as row[0]. You can only overwrite the whole tuple by a new one (this is what happens in the loop above).

### 2.1.2 Diurnal Arc
From the viewpoint of an observer on Earth, the apparent motion of an object on the celestial sphere follows an arc above the horizon, which is called diurnal arc (see Fig.2.3). The time-dependent horizontal position of the object is measured by its hour angle $h$. An hour angle of $24^{h}$ corresponds to a full circle of 360° parallel to the celestial equator (an example is the complete red circle in Fig.2.3). For this reason, $h$ is can be equivalently expressed in degrees or radians. However, as we will see below, an hour angle of $1^{h}$ is not equivalent to a time difference of one solar hour. By definition the hour angle is zero when the object reaches the highest altitude above the horizon (see also Exercise 2.4 and Sect.2.1.3). The hour angle corresponding to the setting time, when the object just vanishes beneath the horizon, is given by⁶:
$$cos h_{set }=-tan \delta tan \phi, \quad(2.2)$$
where $\delta$ is the declination of the object (see Sect.2.1) and $\phi$ the latitude of the observer’s position on Earth. As a consequence, the variable $T=2 h_{set }$ measures the so-called sidereal time for which the object is in principle visible on the sky (stars are of course outshined by the Sun during daytime). It is also known as length of the diurnal arc.

*Fig. 2.3 Diurnal arc of a star moving around the celestial sphere (thick red circle) in the horizontal system (see Sect.2.1.3) of an observer at latitude $\phi$ (the horizontal plane is shown in grey). Since the equatorial plane is inclined by the angle $90^{\circ}-\phi$ against the horizontal plane, the upper culmination of the star at the meridian is given by $a_{max }=90^{\circ}-\phi+\delta$, where $\delta$ is the declination. In the corotating system, the star rises at hour angle $h_{rise }$, reaches its highest altitude when it crosses the meridian at $h=0$, and sets at the horizon at $h_{set }=-h_{rise }$*

For example, let us consider the star Betelgeuse in the constellation of Orion. It is a red giant that is among the brightest stars on the sky. Its declination can be readily found with the help of `astropy.coordinates`, which offers a function that searches the name of an object in online databases:

```python
from astropy.coordinates import SkyCoord, EarthLocation
betelgeuse = SkyCoord.from_name(’Betelgeuse’)
print(betelgeuse)
```

When you are confronted with the output for the first time, it might require a little bit of deciphering:
```
<SkyCoord (ICRS): (ra, dec) in deg
(88.79293899, 7.407064)>
```

This tells us that the right ascension (ra) and declination (dec) of the object named Betelgeuse were found to be 88.79° and 7.41°, respectively⁷. The variable betelgeuse defined in line 3 represents not only an astronomical object; it is a Python object, more specifically an object belonging to the class `SkyCoord` (see Sect.1.4 for objects in a nutshell). The attribute dec allows us to directly reference the declination:

```python
delta = betelgeuse.dec
print(delta)
```

The declination is conveniently printed in degrees (d), arc minutes (m) and arc seconds (s), which is the preferred format to express angular coordinates in astronomy: i.e. $\delta \approx+07^{\circ} 24' 25^{\prime \prime}$, where $1'=(1 / 60)^{\circ}$ and $1^{\prime \prime}=(1 / 60)'$
```
7d24m25.4304s
```

Suppose we want to determine the length of Betelgeuse’s diurnal arc as seen from Hamburg Observatory ($\phi \approx+53^{\circ} 28' 49^{\prime \prime}$). In addition to the star’s declination, we need the position of the observer. The counterpart of `SkyCoord` for celestial coordinates is `EarthLocation` (also imported in line 1), which allows us to set the geographical latitude and longitude of a location on Earth:

```python
import astropy.units as u
# geographical position of the observer
obs = EarthLocation(lat=53*u.deg+28*u.arcmin+49*u.arcsec,
                    lon=10*u.deg+14*u.arcmin+23*u.arcsec)
phi = obs.lat # get latitude
```

In the expressions above,`u.deg` is equivalent to 1°,`u.arcmin` $1'$, and`u.arcsec` is $1''$. The units module from astropy implements rules to carry out computations in physical and astronomical unit systems. You will learn more about AstroPy units in Sect.3.1.1.

Next we compute $h$ with the help of trigonometric functions from the math module:

```python
import math
h = math.acos(-math.tan(delta.radian) * math.tan(phi.radian))
```

It is necessary to convert the angles $\delta$ and $\phi$ to radians before applying the tangent function `math.tan()`. With Astropy coordinates, all we need to do is to use the radian attribute of an angle⁸. To obtain $T$ in hours, it is important to keep in mind that an angle of 360° (one full rotation of Earth) corresponds to a sidereal day, which is about 4 min shorter than a solar day. As explained in [3, Sect. 2.13], this is a consequence of the orbital motion of Earth. The conversion is made easy by the units module (see also Exercise 2.5 for a poor man’s calculation):

```python
T = (math.degrees(2*h)/360)*u.sday
print("T = {:.2f}".format(T.to(u.h)))
```

First $T$ is defined in sidereal days (`u.sday`), which is equivalent to $24^{h}$ or 360°. Then we convert to solar hours (`u.h`) by applying the method `to()` in line 19. The result is:
$$T=13.31 h$$

If it were not for the Sun, Betelgeuse could be seen 13h at the Observatory. Of course, the star will be visible only during the overlap between this period and the night, which depends on the date. We will return to this question in the following section.

The diurnal arc of the Sun plays a central role in our daily life, as it determines the period of daylight. In Sect.2.1.1, we introduced an approximation for the declination $\delta_{\odot}$ of the Sun. By substituting the expression (2.1) for $\delta_{\odot}$ into Eq.(2.2), we can compute how the day length varies over the year. First we need to compute $\delta_{\odot}$ for $N$ ranging from 0 to 364. Using NumPy, this is very easy. In the following example, the expression `np.arange(365)` fills an array with the sequence of integers starting from 0 up to the largest number smaller than 365, which is 364⁹. Apart from that, the code works analogous to the NumPy-based computation for equinoxes and solstices in Sect.2.1.1. Since a new task begins here, the line numbering is reset to 1, although we make use of previous assignments (an example is the latitude phi). In other words, you would need to add pieces from above to make the following code work as an autonomous program (you might want to try this).

```python
import numpy as np
N = np.arange(365) # array with elements 0,1,2,...,364
omega = 2*math.pi/365.24 # Earth’s angular velocity in rad/day
ecl = math.radians(23.44) # obliquity of the ecliptic

# calculate declination of the Sun for all days of the year
delta = -np.arcsin(math.sin(ecl) * np.cos(omega*(N+10)))
```

Now we can compute the day length $T$ for all values in the array delta using functions from the numpy module (compare to the code example for Betelgeuse and check which changes have been made):

```python
h = np.arccos(-np.tan(delta) * math.tan(phi.radian))
# calculate day length in solar hours
T = (np.degrees(2*h)/360) * u.sday.to(u.h)
```

Here, phi is still the latitude of Hamburg Observatory defined above. Of course, $T$ is now an array with 365 elements. Since we want the day length in solar hours, we multiply right away with `u.sday.to(u.h)`, which is the length of a sidereal day in solar hours.

When dealing with large data sets (i.e. more than a few values), it is most of the time preferable to extract some statistics or to display the data in graphical form. To show the annual variation of the day length, producing a plot of $T$ versus $N$ is the obvious thing to do. The Python library matplotlib (see matplotlib.org) provides a module called pyplot for plotting data in arrays:

```python
import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(N, T)
plt.xlabel("Day")
plt.ylabel("Day length [hr]")
plt.savefig("day_length.pdf")
```

The function `plt.plot()`, where plt is a commonly used alias for `matplotlib.pyplot`, produces a plot showing data points $(x, y)$ given by the arrays $N$ (x axis) and $T$ (y axis). By default, the points are joined by lines to produce a continuous graph. Axes labels are added in lines 16 and 17. The plot is then saved to a file called day_length.pdf in PDF format. The location of the file depends on the directory in which you started your Python session. You can specify full path if you want to store the plot somewhere else). You can also use other graphics formats, such as PNG or JPG, by specifying the corresponding extension in the filename (e.g. day_length.png)¹⁰. In line 13, you can see a so-called magic command (indicated by % at the beginning of the line). It enables inline viewing of plots in IPython and Jupyter notebooks¹¹.

The graph can be seen as solid line in Fig.2.4 (the dot-dashed line will be added below). As expected, the day length is short in January, reaches a maximum at the first solstice ($N=171$) and then decreases until the second solstice is reached at $N=355$. The minimal and maximal day length can be inferred with the help of `min()` and `max()` methods for NumPy arrays¹²:

```python
print("Minimum day length = {:5.2f} h".format(T.min()))
print("Maximum day length = {:5.2f} h".format(T.max()))
```

We get:
```
Minimum day length = 7.20 h
Maximum day length = 16.73 h
```

The difference between minimal and maximal day length increases with latitude. Beyond the polar circles ($\phi= \pm 66^{\circ} 33'$), the day length varies between 0 and 24h. An example is Longyearbyen located at $\phi=+78^{\circ} 13'$ on the Norwegian island Spitsbergen in the far North. As we only need to know $\phi$ within an arc minute (accuracy is limited by the approximate declination anyway), a full specification of the geographical position using `EarthLocation` would rather overdo it. Instead we simply use $1'=(1 / 60)^{\circ}$ and immediately convert into radians:

```python
phi = math.radians(78+13/60) # latitude of Longyearbyen
h = np.arccos(-np.tan(delta)*math.tan(phi))
T = (np.degrees(2*h)/360) * u.sday.to(u.h)
```

When you execute this code, you will get a:
```
RuntimeWarning: invalid value encountered in arccos
```

It turns out that Python is able to handle this, but we should nevertheless try to understand what is wrong here. Remember that the range of the declination of the Sun is $-\epsilon_{0} ≤\delta_{\odot} ≤\epsilon_{0}$. Considering Eq.(2.2), you can convince yourself that the right-hand side becomes smaller than −1 or greater than 1 if $|\phi| ≥90^{\circ}-\epsilon_{0}$, i.e. if the location is in the polar regions. In this case, Eq.(2.2) has no solution because the arccosine is undefined if the absolute value of its argument is greater than unity. This corresponds to the polar night or polar day during which the Sun never rises or sets. This can be fixed by setting $cos h_{set }$ equal to ±1 whenever the right-hand side of Eq.(2.2) falls outside of the interval [−1, 1]. Using Numpy, this is easily achieved by means of the `np.clip()` function:

```python
tmp = np.clip(-np.tan(delta)*math.tan(phi), -1.0, 1.0)
h = np.arccos(tmp)
T = (np.degrees(2*h)/360) * u.sday.to(u.h)
```

Assigning the clipped right-hand side of Eq.(2.2) to a temporary array is only intended to highlight this step. We leave it as a little exercise for you to combine lines 24 and 25 into a single line of code and to produce and view the resulting graph for the day length. As expected, you will find that people on Longyearbyen have to cope with a polar night (all day dark) during winter, and a polar day lasting 24h in summer.

Having computed the day length for Hamburg and Longyearbyen, it would be instructive to compare the graphs in a single plot. Obviously, we need the data for both locations at the same time, but in the example above the data for Hamburg were overwritten by the computation for Longyearbyen. A straightforward way of resolving this problem would be to use differently named array, but in Python there is a more elegant and convenient alternative. Apart from arrays in which items are referenced by index, data can be collected in a Python dictionary. Similar to a dictionary in the conventional sense, data items in a dictionary are referenced by keywords rather than a numerical index. The data items of the dictionary can be just anything, including arrays. Let us set up a dictionary associating locations with their latitudes:

```python
phi = {
    ’Hamburg’: obs.lat.radian,
    ’Longyearbyen’ : math.radians(78 + 13/60)
}
```

In Python, a dictionary is defined by pairs of keywords and items enclosed in curly braces. Each keyword, which has to be a string (e.g. ’Hamburg’), is separated by a colon from the corresponding item (the expression `obs.lat.radian` in the case of Hamburg) followed by a comma. How are individual items accessed? For example:

```python
print(phi[’Hamburg’])
```

prints the the latitude of Hamburg in radians. The syntax is similar to accessing array elements, except for the key word instead of an index. Adding new items to a dictionary is very easy. For example, the following assignments add New York and Bangkok to our dictionary:

```python
phi[’New York’] = math.radians(40 + 43/60)
phi[’Bangkok’] = math.radians(13 + 45/60)
```

Indeed, the dictionary now has four items, which can be checked by printing `len(phi)`.

The following code prints all items, computes the day length for each location, and combines them in a single plot:

```python
for key in phi:
    print(key + ": {:.2f} deg".format(math.degrees(phi[key])))
    h = np.arccos(np.clip(-np.tan(delta)*math.tan(phi[key]), -1.0, 1.0))
    T = (np.degrees(2*h)/360) * u.sday.to(u.h)
    plt.plot(N, T, label=key)

plt.xlabel("Day")
plt.xlim(0,364)
plt.ylabel("Day length [hr]")
plt.ylim(0,24)
plt.legend(loc=’upper right’)
plt.savefig("daylength.pdf")
```

The graphical output for the places:
```
Hamburg: 53.48 deg
Longyearbyen: 78.22 deg
New York: 40.72 deg
Bangkok: 13.75 deg
```

can be seen in Fig.2.5. As expected, the day length in Longyearbyen varies between 0 and 24 h, while people in Bangkok, which is in the tropics, experience a day length around 12 h over the whole year. The day length in the temperate zones increases by several hours from winter to summer.

*Fig. 2.4 Annual variation of the day length in Hamburg following from an approximate Eq.(2.1) for the declination of the Sun*
*Fig. 2.5 Annual variation of the day length at different places in the world*

To understand how this output is produced, let us go through the code step by step:
1. The code begins with a for loop iterating the dictionary phi. At first glance, this looks exactly like a loop through an array (see Sect.2.1.1). However, there is an important difference. When iterating an array, the loop variable runs through the elements of the array. In contrast, the loop variable key runs through keywords, not the dictionary items themselves. Since the keyword is the analogue of the index, this loop resembles more an enumeration. The items are referenced by `phi[key]` in the loop body.
2. In line 33, the + operator concatenates two strings. The first string is a keyword, i.e. the name of a location, the second string is a formatted latitude.
3. Lines 35 to 37 correspond to lines 24–26 with the noticeable difference that `phi[key]` instead of phi refers to a particular latitude.
4. The last statement in the loop body (line 39) adds the graph for the current array $T$, which changes with each iteration, to the plot. This means that `plt.plot()` called inside a loop does not produce several plots, but accumulates graphs within a single plot. The optional argument `label=key` sets the graph’s label to the keyword. The labels are used in the legend of the plot (see below).
5. Once the loop is finished, the plot is configured by the statements in lines 41–45: Axes are labeled, their range is limited by `plt.xlim()` and `plt.ylim()`, and labels for the different graphs are shown in a legend in the upper right corner of the plot.
6. Finally, the plot is saved to a PDF file. This will overwrite the previously saved file, unless you choose a different file name.

If you are unsure about any of the steps explained above, make changes to the code and see for yourself what happens and whether it meets your expectations.

### 2.1.3 Observation of Celestial Objects
While it is important to be able to specify the positions of celestial objects in a coordinate system that is independent of time and the observer’s location, at the end of the day you want to know where on the sky you can find the object. To that end, the so-called horizontal coordinate system is used, which is based on an imaginary plane that is oriented tangential to the surface of Earth at the location of the observer. The angular position measured in normal direction from the horizon is the altitude $a$, and the angular separation from some reference direction (usually, the North direction) parallel to the horizon is the azimuth of the object¹³. This is why the horizontal system also goes under the name of alt-azimuth system. The module `astropy.coordinates` offers a powerful framework for working with celestial coordinates (for more information, see docs.astropy.org/en/stable/coordinates). Similar to `SkyCoord` for coordinates in the equatorial system, the alt-azimuth system is represented by the class `AltAz`. In this section, we will utilize `AltAz` to infer the time of observability of the star Betelgeuse. In the course of doing so, we will touch upon some advanced aspects of Python. If you find it too complicated at this point, you can skip over this section and return later if you like.

To begin with, we define once more the position of the observer (see also Sect.2.1.2). You are invited to adjust all settings to your own location and time.

```python
import astropy.units as u
from astropy.coordinates import \
    SkyCoord, EarthLocation, AltAz, get_sun

# geographical position of the observer
obs = EarthLocation(lat=53*u.deg+28*u.arcmin+49*u.arcsec,
                    lon=10*u.deg+14*u.arcmin+23*u.arcsec)

# get latitude
phi = obs.lat
```

Astropy also has a module to define time in different formats¹⁴. By default, `Time()` sets the coordinated universal time (UTC)¹⁵. To define, for example, noon in the CEST time zone (two hours ahead of UTC) on July 31st, 2020, we shift the time by an offset of two hours:

```python
from astropy.time import Time
utc_shift = 2*u.hour # CEST time zone (+2h)
noon_cest = Time("2020-07-31 12:00:00") - utc_shift
```

Printing `noon_cest` shows the UTC time corresponding to 12am CEST. The shift to UTC is necessary because `AltAz` expects UTC time.

With time and location, we can define our horizontal coordinate system. We want to follow the star’s position over a full 24h period and determine the time window for observation during night. Since altitude and azimuth are time dependent, we need to create a sequence of frames covering a whole day (frame is synonymous to coordinate system):

```python
import numpy as np
# time array covering next 24 hours in steps of 5 min
elapsed = np.arange(0, 24*60, 5)*u.min
time = noon_cest + elapsed

# sequence of horizontal frames
frame_local_24h = AltAz(obstime=time, location=obs)
```

In lines 19–20, a time sequence is created, starting from noon (CEST) in steps of five minutes covering an interval of 24h. Let us look at this in more detail. First `np.arange()` creates an array of numbers (0, 5, 10, . . .). Calling:
```python
type(np.arange(0, 24*60, 5))
```
informs us that the type of the object returned by `np.arange()` is:
```
numpy.ndarray
```

What is the type of an object? It is just the class to which the object belongs. Do not confuse this with the data type of the array (i.e. the type of its elements; see Sect.2.1.1). As we shall see, the initially created NumPy array undergoes quite a metamorphosis. To define the time elapsed since noon in minutes, the array is multiplied with `u.min`. While multiplication with a number does not affect the type:
```python
type(elapsed)
```
returns:
```
astropy.units.quantity.Quantity
```

As mentioned in Sect.1.4, quantities with units are instances of the `Quantity` class, which is defined in the submodule `astropy.units.quantity`. On the other hand, when printing `elapsed`, you will probably conclude that it pretty much looks like an array. Can we confirm this? The function `isinstance()` tells you if something belongs to a certain class (this is what instance means). While an object is of course an instance of the class defining its type¹⁶, it can also belong to other classes. Indeed:
```python
isinstance(elapsed, np.ndarray)
```
yields True, i.e. `elapsed` is an array of sorts. Astropy supports arrays with units, which are a subclass of NumPy arrays. A subclass can extend attributes and methods of an existing base class, here `numpy.ndarray`. This is known as inheritance.

Now you might guess that `time` is also an array, created by adding a fixed value to the elements of `elapsed` (see line 20). But no:
```python
isinstance(time, np.ndarray)
```
returns False.

Without going into too much detail, time has some array-like features, but it is not derived from NumPy. And it has its own way of treating units (basically, it replaces the notion of units by time formats). In general, it cannot be used in place of an array, such as `elapsed`. The reason we need it is to create frames by means of `AltAz()` (see line 23).

After this little detour to classes and inheritance, we retrieve Betelgeuse’s coordinates as shown in Sect.2.1.2 and then transform it to the observer’s horizontal frame for the times listed in time.

```python
# star we want to observe
betelgeuse = SkyCoord.from_name(’Betelgeuse’)
betelgeuse_local = betelgeuse.transform_to(frame_local_24h)
```

The method `transform_to()` turns the declination and right ascension of the star into altitudes and azimuths for the time sequence of frames defined in line 23 above. Modern telescopes are controlled by software, making it relatively easy for the observer to direct a telescope to a specific celestial object. Basically, the software uses something like Astropy’s `transform_to()` and moves the telescope accordingly. Historical instruments, such as the 1 m reflector shown in Fig.2.6, are a different matter. They are operated manually and the observer needs to know the position of an object on the sky.

To determine the phases of daylight, we need to determine the Sun’s position in the same frames. Since the position of the Sun changes not only in the horizontal, but also in the equatorial coordinate system, Astropy offers a special function for the Sun:

```python
# time-dependent coordinates of the Sun in equatorial system
sun = get_sun(time)
sun_local = sun.transform_to(frame_local_24h)
```

This completes the preparation of the data.

Now let us plot the altitude of Betelgeuse and the Sun for the chosen time interval and location:

```python
import matplotlib.pyplot as plt
%matplotlib inline

betelgeuse_night = betelgeuse_local.alt[np.where(sun_local.alt < 0)]
elapsed_night = elapsed[np.where(sun_local.alt < 0)]

plt.plot(elapsed.to(u.h), sun_local.alt,
         color=’orange’, label=’Sun’)
plt.plot(elapsed.to(u.h), betelgeuse_local.alt,
         color=’red’, linestyle=’:’,
         label=’Betelgeuse (daylight)’)
plt.plot(elapsed_night.to(u.h), betelgeuse_night,
         color=’red’, label=’Betelgeuse (night)’)

plt.xlabel(’Time from noon [h]’)
plt.xlim(0, 24)
plt.xticks(np.arange(13)*2)
plt.ylim(0, 60)
plt.ylabel(’Altitude [deg]’)
plt.legend(loc=’upper center’)
plt.savefig("Betelgeuse_obs_window.pdf")
```

*Fig. 2.6 Hamburg Observatory’s 1 m reflector. When the instrument was commissioned in 1911, it was the fourth largest reflector worldwide. In the first half of the 20th century, the astronomer Walter Baade used the telescope to observe a great number of star clusters, gas nebulae, and galaxies. For further information, see www.physik.uni-hamburg.de/en/hs/outreach/historical/instruments.html*

Let us begin with the plot statement in lines 43–44. We plot the altitude of the Sun (`sun_local.alt`) as a function of the time elapsed since noon in hours. Rather than using default colors, we set the line color to orange (`color=’orange’`). The graph for the altitude of Betelgeuse has two components. We use a dotted line (`linestyle=’:’`) in red to plot the altitude over the full 24 hour interval (lines 45–47). Since the star is only observable during night, the dotted line is overplotted by a solid line for those times where the altitude of the Sun is negative, i.e. below the horizon-that is basically the definition of night. How do we do that? You find the answer in lines 39–41, where the expression:
```python
np.where(sun_local.alt < 0)
```
appears like an index in brackets. The function `np.where()` identifies those elements of `sun_local.alt` which are less than zero and returns their indices (remember that array elements are identified by their indices). These indices in turn can be applied to select the corresponding elements in `elapsed` and `betelgeuse_local.alt`, producing masked arrays. This is equivalent to looping through the arrays, where any element `elapsed[i]` and `betelgeuse_local.alt[i]` for which `sun_local.alt[i]` is not smaller than zero (Sun above the horizon) is removed. In Exercise 2.4, you will learn how `np.where()` can be utilized to choose between elements of two arrays depending on a condition. This can be regarded as the array version of branching.

The result can be seen in Fig.2.7. Since objects with negative altitude are invisible for the observer, only positive values are shown (see line 54). Moreover, the tick labels for time axis are explicitly set with `plt.xticks()` in line 53. Night is roughly between 9 pm and 6 am (18h counted from noon on the previous day)¹⁷. Betelgeuse rises around 4 o’clock in the morning and there only two hours left before sunrise. This is the interval for which the solid red line plotted in lines 48–49 is visible in the plot. Actually, the observation window is even narrower. Dawn is rather long at a latitude of 53°. The period of complete darkness, the so-called astronomical night, is defined by $\delta_{\odot} \leq-18^{\circ}$. Although Betelgeuse is a very bright star, Hamburg is definitely not the optimal place to observe the star in summer (see Exercise 2.7).

*Fig. 2.7 Altitude of the Sun and the star Betelgeuse as seen from Hamburg Observatory on July 31st, 2020*

### Exercises
2.1 Compute the Sun’s declination for the equinoxes and solstices using only trigonometric functions from the math module in an explicit for loop. Print the results and check if they agree with the values computed with NumPy in this section. This exercise will help you understand what is behind an implicit loop.

2.2 The day count $N$ in Eq.(2.1) can be calculated for a given date with the help of the module datetime. For example, the day of the vernal equinox in the year 2020 is given by:
```python
vernal_equinox = datetime.date(2020, 3, 20) - datetime.date(2020, 1, 1)
```
Then `vernal_equinox.days` evaluates to 79. Define the array $N$ (equinoxes and solstices) using datetime.

2.3 A more accurate formula for the declination of the Sun takes the eccentricity $e=0.0167$ of Earth’s orbit into account¹⁸:
$$\delta_{\odot}=-arcsin \left[sin \left(\epsilon_{0}\right) cos \left(\frac{360^{\circ}}{365.24}(N+10)+e \frac{360^{\circ}}{\pi} sin \left[\frac{360^{\circ}}{365.24}(N-2)\right]\right)\right]$$
Compute the declination assuming a circular orbit (Eq.2.1), the declination resulting from the above formula, the difference between these values, and the relative deviation of the circular approximation in % for equinoxes and solstices and list your results in a table. Make sure that an adequate number of digits is displayed to compare the formulas.

2.4 恒星的最高高度（也称为上中天）是从地球观测者的水平面¹⁹测量的，公式如下：
$$a_{max }= \begin{cases}90^{\circ}-\phi+\delta & if \phi \geq \delta, \\ 90^{\circ}+\phi-\delta & if \phi \leq \delta,\end{cases}$$
其中$\phi$是观测者的纬度，$\delta$是恒星的赤纬。计算你当前位置下以下恒星的$a_{max }$：
- 北极星（$\delta=+89^{\circ} 15' 51^{\prime \prime}$）
- 参宿四（$\delta=+07^{\circ} 24' 25^{\prime \prime}$）
- 参宿七（$\delta=-08^{\circ} 12' 15^{\prime \prime}$）
- 天狼星A（$\delta=-16^{\circ} 42' 58^{\prime \prime}$）

为了区分式(2.3)中的两种情况，使用NumPy的`where()`函数。例如，表达式`np.where(phi <= delta, phi-delta, phi+delta)`会逐元素比较$\phi$和$\delta$，并返回一个数组：当条件$\phi <= delta$为真时，元素为$\phi-delta$；为假时，元素为$\phi+delta$。打印结果时需包含适当有效数字，并附上赤纬值。

2.5 恒星日比太阳日（24小时）短约3分56秒。证明这意味着$1^{h} ≈0.9973 ~h$（恒星时与太阳时的换算系数）。如何在不使用Astropy单位的情况下，修改2.1.2节中$T$的定义以利用该系数？

2.6 结合习题2.3中含偏心率修正的公式和`SkyCoord`的`get_sun()`函数，计算并绘制你所在地理位置的日长年度变化。两种方法的偏差有多大？结果与图2.5中其他地区相比如何？

2.7 确定新年前夜参宿四的观测窗口。首先以汉堡天文台的位置（见2.1.3节）为准，计算该恒星在天文夜（太阳高度角至少低于地平线18°）期间的可观测时长。切换到你所在位置，计算北极星、参宿四和天狼星A在即将到来的夜晚的高度角，生成类似图2.4的图表。若天空晴朗，你能观测到哪些恒星？

## 2.2 开普勒行星运动定律
17世纪初，天文学家约翰内斯·开普勒基于经验数据首次提出了行星运动的基本定律。他利用当时最精确的行星位置测量数据，尤其针对火星，发现其天空中的视运动可通过假设行星沿椭圆轨道绕太阳运行来解释。这一观点具有革命性意义——在此之前，行星运动被认为是圆周运动（更准确地说是托勒密体系中的复合圆周运动），地球被视为宇宙中心。尽管差异微小，开普勒通过分析得出结论：行星沿椭圆轨道运行，太阳位于椭圆的一个焦点上（第一定律）；用现代语言表述，太阳到行星的径向矢量扫过的面积与时间成正比（第二定律）。后来，他发现了轨道半长轴（从椭圆中心穿过焦点到边缘的线段）与公转周期的关系，即如今的开普勒第三定律。艾萨克·牛顿通过应用万有引力定律和角动量守恒，为开普勒行星运动定律提供了理论解释（详见[4, 第2章]的详细推导与讨论）。我们将在4.3节中回到第一和第二定律，通过数值积分求解二体问题（太阳和行星）的运动方程。

行星绕恒星沿椭圆轨道运行的周期$P$的一般表达式为：
$$P^{2}=\frac{4 \pi^{2}}{G(M+m)} a^{3},$$
其中$a$是轨道半长轴，$G$是引力常数，$M$是恒星质量，$m$是行星质量。在1.2节中，我们使用了近似表达式(1.2)，该式适用于行星质量可忽略（即$m \ll M$）且轨道为圆形的情况（此时$a$等于轨道半径$r$）。

以下程序计算太阳系八大行星的轨道周期（基于式(2.4)）。实际上，这也是一种近似，因为忽略了行星之间的相互影响——开普勒第三定律假设的是二体系统（太阳和单个行星），但它比检验质量近似（$m=0$）更精确。代码对比了二体公式与检验质量公式的结果：

```python
import math
import numpy as np
from scipy.constants import year, hour, au, G
from astropy.constants import M_sun

M = M_sun.value  # 太阳质量（单位：kg）

# 行星轨道参数（数据来源：https://nssdc.gsfc.nasa.gov/planetary/factsheet/）
# 质量（单位：kg），乘以1e24简化输入
m = 1e24 * np.array([0.33011, 4.8675, 5.9723, 0.64171, 1898.19, 568.34, 86.813, 102.413])

# 半长轴（单位：m），乘以1e9简化输入
a = 1e9 * np.array([57.9, 108.21, 149.60, 227.92, 778.57, 1433.53, 2872.46, 4495.06])

# 用开普勒第三定律计算周期（单位：秒）
T_test_mass = 2 * math.pi * (G * M)**(-1/2) * a**(3/2)  # 检验质量近似（m=0）
T_two_body = 2 * math.pi * (G * (M + m))**(-1/2) * a**(3/2)  # 二体系统（考虑行星质量）

# 打印结果
print("T [yr]    dev [hr]    dev rel.")
for val1, val2 in zip(T_test_mass, T_two_body):
    dev = val1 - val2  # 偏差（检验质量结果 - 二体结果）
    if dev > hour:
        # 偏差大于1小时时，保留1位小数并左对齐
        line = "{0:6.2f}    {1:<7.1f}    {2:.1e}"
    else:
        # 偏差小于等于1小时时，保留4位小数
        line = "{0:6.2f}    {1:7.4f}    {2:.1e}"
    print(line.format(val2/year, dev/hour, dev/val1))  # 周期转换为年，偏差转换为小时
```

我们使用`scipy.constants`获取引力常数$G$，并从`astropy.constants`获取太阳质量定义（见1.4节）。行星质量和轨道半长轴数据来自NASA网站（见注释）。上述程序的计算基于国际单位制（SI），为了用年和天文单位（AU）表示结果，我们使用`scipy.constants`中的单位转换因子（这些因子本质是数值，例如`year`表示1年对应的秒数，`au`表示1天文单位对应的米数）。在3.1节中，你将学习如何使用Astropy的单位模块，通过方法实现单位转换（前一节已给出初步示例）。

式(2.4)和检验质量近似（忽略行星质量）定义的轨道周期分别在第18行和第19行通过数组运算计算。结果在第22-28行的`for`循环中打印（`zip()`函数的解释见2.1节）：
- 第一列：式(2.4)计算的周期（单位：年）
- 第二列：与检验质量近似的偏差（单位：小时）
- 第三列：相对偏差（偏差/检验质量结果）

程序输出如下：
```
T [yr]    dev [hr]    dev rel.
0.24      0.0002      8.3e-08
0.62      0.0066      1.2e-06
1.00      0.0132      1.5e-06
1.88      0.0027      1.6e-07
11.88     49.6        4.8e-04
29.68     37.2        1.4e-04
84.20     16.1        2.2e-05
164.82    37.2        2.6e-05
```

水星每年绕太阳公转4次，而海王星完成一次公转则需要超过一个世纪。为了将国际单位制（秒）的周期转换为年，需将计算值除以转换因子`year`（见第28行）。外行星（木星、土星、天王星、海王星）比内行星（水星、金星、地球、火星）质量大得多，因此其与检验质量近似的偏差更大，但轨道周期的相对误差仍然很小。为了使第二列的数值在小数点后对齐，程序使用`if-else`语句根据绝对偏差是否大于1小时（`hour`为1小时对应的秒数）定义行格式：两种情况下列宽均为7位，但外行星（质量更大）的偏差值仅保留1位小数，并通过在格式说明符中插入`<`字符左对齐（可尝试修改格式以理解其工作原理）。

幂律关系（如$P \propto a^{2 / 3}$）在双对数图中表现为直线，斜率等于指数：
$$log P=\frac{2}{3} log a+ const. \quad(2.5)$$

我们可以通过`pyplot`模块的`loglog()`函数绘制双对数图：

```python
import matplotlib.pyplot as plt
%matplotlib inline

# 双对数图绘制（x轴：半长轴/AU，y轴：周期/年）
plt.loglog(a/au, T_test_mass/year, 'blue', linestyle='--', label='test mass')  # 检验质量（虚线）
plt.loglog(a/au, T_two_body/year, 'ro', label='planets')  # 行星数据（红色圆点）

# 图表配置
plt.legend(loc='lower right')  # 图例位置：右下角
plt.xlabel("semi-major axis [AU]")  # x轴标签
plt.ylabel("orbital period [yr]")    # y轴标签
plt.savefig("kepler_third_law.pdf")  # 保存图表（PDF格式）
```

图形输出如图2.8所示。将周期（秒）转换为小时、半长轴（米）转换为天文单位，只需将数组分别除以`scipy`的单位转换因子`hr`和`au`。检验质量数据严格遵循幂律关系，显示为蓝色虚线；`T_two_body`中的元素显示为红色圆点（`'ro'`是红色圆形标记的简写）²⁰。`color`关键字（见2.1.3节）可省略，此时第三个参数指定图表颜色（此类参数称为位置参数，与`linestyle`等关键字参数相对）。3.1.2节将详细介绍不同类型的参数（当你学习定义Python函数时）。

*图2.8 基于开普勒第三定律计算的太阳系行星轨道周期*
> 注：y轴为轨道周期（单位：年），x轴为半长轴（单位：AU）；蓝色虚线为检验质量近似结果，红色圆点为行星实际周期（二体系统）。

### 习题
2.8 除了太阳系的八大行星，还有许多矮行星。例如：
- 冥王星（$a=39.48 AU$），曾被视为第九大行星²¹
- 谷神星（$a=2.7675 AU$），位于小行星带
- 海外天体厄里斯（$a=67.781 AU$）

计算这些矮行星的轨道周期（矮行星质量可忽略），并将结果与行星轨道数据一起绘制在图表中，使用不同的标记，并在图例中为矮行星添加额外标签。

2.9 自20世纪90年代中期发现第一颗系外行星以来，已识别出更多系外行星。一类重要的系外行星是“热木星”——它们质量大，但与太阳系的气态巨行星不同，距离母星更近。通常，热木星的轨道周期仅为数天（而太阳系的木星轨道周期约为12年）。表2.1列出了通过凌日法发现的部分热木星样本。行星质量通常是下限值，因为其取决于轨道相对于视线的未知倾角。

表2.1 系外行星数据库（exoplanets.org）中的热木星轨道和恒星参数样本
| 系外行星 | 周期P（天） | 母星质量M（$M_{\odot}$） |
|----------|-------------|---------------------------|
| CoRoT-3 b²² | 4.257 | 1.37 |
| Kepler-14 b | 6.790 | 1.51 |
| Kepler-412 b | 1.721 | 1.17 |
| HD 285507 b | 6.088 | 0.73 |
| WASP-10 b | 3.093 | 0.79 |
| WASP-88 b | 4.954 | 1.45 |
| WASP-114 b | 1.549 | 1.29 |

²²质量大于$13 M_{J}$（木星质量），属于褐矮星

(a) 利用行星质量$m$和母星质量$M$作为参数，计算这些系外行星的半长轴$a$（单位：AU），并绘制轨道周期$P$与$a$的关系图。

(b) 可使用NumPy的`polyfit()`函数对对数数据进行线性拟合。调用`polyfit()`时，第一个参数为$P$（天）的对数（x数据），第二个参数为$a$（AU）的对数（y数据），第三个参数为多项式次数（此处为1，对应线性函数$y=c_{1} x+c_{0}$）。`polyfit()`返回拟合参数$c_{0}$和$c_{1}$。将结果与开普勒第三定律的对数形式（式2.5）对比，分析斜率未完全匹配的原因，并在(a)的图表中添加拟合得到的轨道周期直线。

2.10 假设一艘载人宇宙飞船前往火星，沿霍曼转移轨道飞行（见图2.9）。这是最节省能量（即所需推进剂最少）但并非最快的火星抵达方案。转移轨道由椭圆轨道的一半组成，椭圆轨道绕太阳运行，近地点和远地点分别与地球和火星的轨道相切²³。

*图2.9 从地球轨道（蓝色）到火星轨道（红色）的霍曼转移轨道（黑色实线）示意图。顶点处的近地点速度和远地点速度分别为$v_{p}$和$v_{a}$。发射时行星的位置标记为E（地球）和M（火星），最终位置标记为$M'$（火星）。$\delta$为地球和火星的初始角距，$\Delta \varphi$为火星在转移时间$t_{H}$内扫过的角度*

在基础计算中，行星轨道被假设为圆形，半径分别为$r_{\oplus}=1 AU$（地球）和$r_{\sigma}=1.524 AU$（火星）。此时，近地点和远地点的径向距离分别为$r_{p}=r_{\oplus}$和$r_{a}=r_{\sigma}$。发射后，推进器将飞船从地球轨道推入转移轨道。计算椭圆转移轨道的半长轴$a_{H}$，以及速度差$\Delta v=v_{p}-v_{\oplus}$（其中$v_{p}$是进入近地点轨道所需的速度，$v_{\oplus}$是地球的轨道速度）。（应用活力公式（式4.46）计算$v_{p}$；详见[4, 第2章]的重要方程和关系。）

飞船到达火星轨道的转移时间$t_{H}$是多少？为使飞船在远地点与火星会合（假设火星沿圆形轨道运行），发射时地球和火星的角距$\delta$（即位置矢量$r_{\oplus}$和$r_{\sigma}$之间的夹角）需满足什么条件？

²³“轨道”通常指一类特殊的轨迹，即绕引力中心的周期性运动路径。

## 2.3 潮汐力
两个天体的轨道运动由质点间的牛顿万有引力定律支配。然而，引力随距离的依赖性会导致延伸天体（如行星）在另一天体的引力场中产生潮汐力。考虑一个质量为$m$的小检验质量，位于质量为$M$的遥远天体的引力场中，引力场强度为$g=(G M / r^{2}) e_{r}$（其中$e_{r}=r / r$是从该天体中心指向检验质量的径向单位矢量）。检验质量在相邻点$r$和$r+d r$处受到的引力差可通过场梯度表示：
$$d F=m \nabla g \cdot d r=-\frac{2 G M m}{r^{3}} d r .$$

若将检验质量替换为行星的不同部分，则潮汐力定义为相对于质心的力差。

几乎所有人都知道月球引力对地球产生的潮汐现象。考虑地球中心$C$到地球表面某点$P$的距离$R ≤R_{E}$（见图2.10），近似力差为：
$$\begin{aligned} \Delta F \equiv\left(\Delta F_{x}, \Delta F_{y}\right) & =F_{PM}-F_{CM} \\ & \simeq \frac{G M m R}{r^{3}}(2 cos \theta,-sin \theta), \end{aligned}$$
其中$r \gg R$是地球到月球的距离（推导见[4, 19.2节]）。力分量$\Delta F_{x}$沿质心$C$和$M$的连线（图2.10中的点划线），$\Delta F_{y}$垂直于该连线。潮汐力的大小随到地球中心的距离增加而增大，在朝向月球（$\theta=0$）和背向月球（$\theta=\pi$）的方向均达到最大值。潮汐力在最近和最远侧均最强且向外，从而产生高潮，这一点有时被认为违反直觉，但这是潮汐力作为微分力的必然结果。

*图2.10 月球（M）对地球中心（C）和表面某点（P）施加的局部引力示意图。力差即为式(2.7)给出的潮汐力*

以下程序计算单位质量的潮汐力$a_{tidal }=\Delta F / m$，计算范围为$x$轴和$y$轴上等间距分布的网格点，且网格点位于半径$R=R_{E}$（地球半径）的圆内：

```python
import numpy as np
from scipy.constants import g, G
from astropy.constants import R_earth, M_earth
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
%matplotlib inline

# 月球参数（数据来源：nssdc.gsfc.nasa.gov/planetary/factsheet）
M_moon = 0.07346e24  # 月球质量（单位：kg）
r_moon = 3.844e8     # 月球轨道半长轴（单位：m）

# 潮汐加速度相关计算
coeff = G * M_moon / r_moon**3  # 潮汐加速度系数
accel_scale = 2 * coeff * R_earth.value  # 地球表面沿地月连线的潮汐加速度标度
print("tidal acceleration = {:.2e} m/s^2 = {:.2e} g".format(accel_scale, accel_scale/g))

# 潮汐隆起高度计算（忽略地球刚性的近似公式[5]）
# 公式：h = (3 * M_moon * R_earth^4 * ζ) / (4 * M_earth * r_moon^3)，其中ζ ≈ 5/2
zeta = 5/2
h_bulge = (3 * M_moon * R_earth.value**4 * zeta) / (4 * M_earth.value * r_moon**3)
print("size of tidal bulge = {:.2f} m".format(h_bulge))

# 生成x轴和y轴的网格点（无量纲坐标，归一化到地球半径）
# 范围：[-1.1, 1.1]，包含23个点（端点包含在内），间距Δx=Δy=0.1
X = np.linspace(-1.1, 1.1, num=23, endpoint=True)
Y = np.linspace(-1.1, 1.1, num=23, endpoint=True)
print("Grid points (X):", X)

# 生成二维网格（缩放为地球半径的实际长度）
R_x, R_y = np.meshgrid(R_earth.value * X, R_earth.value * Y)
print("Shape of R_x/R_y:", R_x.shape)  # 输出网格形状（23x23）
print("Example point (R_x[11,21], R_y[11,21]):", R_x[11,21], R_y[11,21])  # 示例点坐标（地球表面沿x轴正方向）

# 计算网格点到原点（地球中心）的径向距离
R = np.sqrt(R_x**2 + R_y**2)

# 计算地球半径内的潮汐加速度分量（使用掩码数组排除地球外部点）
accel_x = np.ma.masked_where(R > R_earth.value, 2 * coeff * R_x)  # x分量：2*coeff*R_x
accel_y = np.ma.masked_where(R > R_earth.value, -coeff * R_y)    # y分量：-coeff*R_y

# 可视化潮汐加速度场（箭头图）
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')  # x轴和y轴等比例

# 绘制矢量场（箭头）
arrows = ax.quiver(X, Y, accel_x, accel_y, color='blue')

# 添加箭头标度（显示1.1e-6 m/s²对应的箭头长度）
ax.quiverkey(arrows, X=0.1, Y=0.95, U=accel_scale, 
             label=r'$1.1\times 10^{-6}\;\mathrm{m/s}^2$', labelpos='E')

# 添加地球轮廓（圆形，半径1，透明度0.2，无边框）
circle = Circle((0, 0), 1, alpha=0.2, edgecolor=None)
ax.add_patch(circle)

# 坐标轴标签（无量纲坐标，x/R_E和y/R_E）
ax.set_xlabel(r'$x/R_{\mathrm{E}}$', fontsize=12)
ax.set_ylabel(r'$y/R_{\mathrm{E}}$', fontsize=12)

# 显示并保存图表
plt.show()
plt.savefig("tidal_accel_earth.pdf")
```

对于$R=R_{E}$（地球表面），沿地月连线（$\theta=0$）的潮汐加速度大小定义了潮汐加速度标度$2 G M R_{E} / r^{3}$。第8-9行使用`astropy.constants`中的常数和月球数据计算其数值：
```
tidal acceleration = 1.10e-06 m/s^2 = 1.12e-07 g
```

相对于地球重力$g ≈9.81 ~m / s^{2}$（使用`scipy.constants`中定义的常数$g$），潮汐加速度非常小——否则潮汐力会对地球产生更剧烈的影响。第13行使用忽略地球刚性的近似公式计算月球引起的地球潮汐隆起高度[5]：
$$h=\frac{3 M R_{E}^{4}}{4 M_{E} r^{3}} \zeta, \quad where \ \zeta \simeq 5 / 2. \quad(2.8)$$

结果与海洋中的高潮高度相当²⁴：
```
size of tidal bulge = 0.67 m
```

下一步是通过在坐标轴上引入网格点$x_{n}=n \Delta x$和$y_{n}=n \Delta y$，对$x$和$y$坐标进行离散化。第17-18行使用NumPy的`np.linspace()`生成网格点数组：该函数返回指定区间内的等间距点，第一个参数为区间起点，第二个为终点，`num`为点数，`endpoint=True`表示包含终点。我们使用归一化到地球半径的无量纲坐标，避免处理实际距离。为了覆盖略大于地球的区域（地球在归一化坐标中的直径为2.0），我们将区间$[-1.1, 1.1]$划分为23个点（包含端点），这意味着$\Delta x=\Delta y=2.2 /(23-1)=0.1$，对应物理长度为$0.1 R_{E}$。第19行打印的$X$数组元素如下：
$$\begin{array}{ccccccccccc}-1.1 & -1.0 & -0.9 & -0.8 & -0.7 & -0.6 & -0.5 & -0.4 & -0.3 & -0.2 & -0.1 & 0.0 \\ 0.1 & 0.2 & 0.3 & 0.4 & 0.5 & 0.6 & 0.7 & 0.8 & 0.9 & 1.0 & 1.1 \end{array}$$

为了表示矢量场$a_{tidal }(R)$，需要在$x y$平面上构造位置矢量$R=(R_{x}, R_{y}) \equiv(x, y)$的二维网格。由于地月系统的旋转对称性，可忽略$z$分量。二维网格可通过所有可能的$x_{n}$和$y_{m}$组合（索引$n$和$m$独立）构造，这正是第22行调用NumPy函数`meshgrid()`的目的。为了得到物理距离，归一化坐标需乘以地球半径（从`astropy.constants`导入）。由于$X$和$Y$各有23个元素，`np.meshgrid()`返回两个二维数组$R_x$和$R_y$，定义了$23 ×23=529$个网格点的坐标分量。此处将多个返回值（数组）分配给多个变量（$R_x$和$R_y$）。二维数组可视为矩阵（此处为23行23列），通过第23行打印$R_x$的`shape`属性可验证（输出`(23, 23)`）。

要获取特定元素，需在括号中指定两个索引：第一个为行索引，第二个为列索引。例如，第24行打印的$R_x [11,21]$和$R_y [11,21]$的值为`6378100.0 0.0`，即位置$R=(R_{E}, 0)$（地球表面沿$x$轴正方向）。为了理解其原理，可考虑一个点数更少且无缩放的简单示例：图2.11展示了如何从大小为7的一维数组构造7×7的网格。例如，绿色点的坐标为$(1, -3)$，对应$R_x [0,4]$和$R_y [0,4]$（见图中数组中的绿色方块）。可见，$x$坐标随列索引变化，$y$坐标随行索引变化。你可能会疑惑为何需要二维数组$R_x$和$R_y$——它们似乎是冗余的（$R_x$的所有行相同，$R_y$的所有列相同），但二维数组可直接推断网格上**所有**点的位置矢量（或其他矢量）分量，本质是矢量场的离散表示（每个空间点都附着一个矢量，位置矢量场是特殊情况）。

*图2.11 从一维数组$X$和$Y$（顶部）构造网格的示意图。二维数组$R_x$和$R_y$（中部）表示网格上所有点的坐标（底部）。示例中，红色和绿色点的坐标在数组中高亮显示*

对于给定位置$(R_{x}, R_{y})$，潮汐加速度$a_{tidal }=\Delta F / m$由式(2.7)推导得出（其中$R cos \theta=R_{x}$，$R sin \theta=R_{y}$）：
$$a_{tidal }(R)=\frac{G M}{r^{3}}\left(2 R_{x},-R_{y}\right) . \quad(2.9)$$

第30-31行通过NumPy运算实现该公式。为了将加速度场限制在半径$R_{E}$的圆形区域内，我们定义了掩码数组：掩码为数组的每个元素标记0或1，标记为1的元素值无效，不会参与后续数组运算。掩码元素未从数组中移除（可后续取消掩码），所有标记为0的未掩码元素可通过原始索引访问。大多数情况下，可通过`numpy.ma`模块中的函数实现数组掩码（另一种方法见2.1.3节）。此处使用`masked_where()`：该函数对所有满足逻辑条件的数组元素进行掩码。为了排除地球外部的位置，我们将条件$R > R_earth.value$（$R$为第27行定义的径向距离）应用于`accel_x`和`accel_y`数组。

数据计算完成后，可通过箭头图形化表示加速度场（矢量场可视化）：第32-53行实现该功能。`quiver()`方法（第40行）用于绘制箭头场，该方法调用在坐标轴对象`ax`上（由`plt.subplots()`创建，见第36行）。第37行将$x$轴和$y$轴的纵横比设置为1，以生成正方形图表。`quiver()`的参数包括坐标轴上的网格点$X$和$Y$，以及加速度场的网格值`accel_x`和`accel_y`：$X$和$Y$确定箭头位置（网格隐式构造），`accel_x`和`accel_y`确定箭头的长度和方向。箭头颜色可通过可选参数指定（类似`plt.plot()`中的线颜色）。`quiverkey()`方法（第41行）在指定坐标处显示一个箭头，标签为该箭头长度对应的数值——该箭头不属于待可视化的矢量场，仅用于展示加速度场的标度。地球内部通过`matplotlib.patches`的`Circle()`函数高亮显示：示例中生成一个半径为1（$X$和$Y$为归一化坐标）、中心在$(0,0)$的填充圆，透明度为0.2，无边框。可尝试修改该函数的参数以观察圆的外观变化。要显示圆，需调用`ax.add_patch()`（第47行），该方法将平面几何对象（matplotlib中称为“补丁”）插入图表。最终图表如图2.12所示，呈现出典型的潮汐隆起模式——地月连线两侧的相对侧均有隆起。由于地球近似为刚体，隆起仅在海洋中产生，导致涨潮和落潮。

*图2.12 月球引力引起的地球内部潮汐加速度场*

### 习题
2.11 月球对地球产生潮汐力，反之亦然。比较木星（质量和半径在`astropy.constants`中定义）对其卫星木卫一（$M=8.9319 ×10^{22} ~kg$，$R=1822 ~km$，平均轨道半径$r=4.217 ×10^{5} ~km$）的潮汐效应与地月系统的差异。木卫一和月球的潮汐隆起高度分别是多少？绘制式(2.9)定义的潮汐加速度$a_{tidal }$的大小与表面局部重力$g$的比值随$\theta$的变化图²⁵。

2.12 长度为$l$、质量为$m$的圆柱形杆沿径向指向质量为$M$的引力天体，其受到的拉力可通过积分式(2.7)得到（假设$l \ll r$）。

(a) 估算长度$l=1 ~m$的杆在以下位置受到的拉力：
- 地球表面
- 1个太阳质量的白矮星表面
- 质量$M=10 M_{\odot}$的黑洞视界处（假设牛顿引力公式适用；视界半径由史瓦西半径$R_{S}=2 G M / c^{2}$给出，$c$为光速）

(b) 若杆的直径为5 cm，由密度$\rho=7.8 ~g ~cm^{-3}$、屈服强度$\sigma=5 ×10^{8} ~Pa$的钢制成（即杆能承受的最大拉力为$\sigma$乘以横截面积），则杆在距离黑洞多远时会被潮汐力撕裂？估算人类能接近黑洞的最小距离（此时人体受到的拉力相当于地球上100 kg物体的重量——想象该重量附着在人体上）。

(c) 任何落入黑洞并穿过视界的物体，最终都会受到极端潮汐力的作用：径向拉伸和横向压缩导致“面条化”。然而，固体由于变形能力有限，会被撕裂成越来越小的碎片。生成类似图2.12的图表，展示杆在(b)中确定的临界距离处受到的潮汐加速度场，使用`matplotlib.patches`的`Rectangle()`函数显示杆沿轴线的横截面。

²⁵球形天体的表面重力由$g=G M / R^{2}$给出（$R$为天体半径）。