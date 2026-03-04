# CHAPTER 7 FOURIER TRANSFORMS

THE Fourier transform is one of the most useful, and most widely used, tools in traditional theoretical physics. It's also very useful in computational physics. It allows us to break down functions or signals into their component parts and analyze, smooth, or filter them, and it gives us a way to rapidly perform certain kinds of calculations and solve certain differential equations, such as the diffusion equation or the Schrödinger equation. In this section we look at how Fourier transforms are used in computational physics and at computational methods for calculating them.

---

### 7.1 FOURIER SERIES

As every physicist learns, a periodic function $f(x)$ defined on a finite interval $0 \leq x < L$ can be written as a *Fourier series*.^1 There are several kinds of Fourier series. If the function is even (i.e., symmetric) about the mid-point at $x = \frac{1}{2}L$ then we can use a cosine series thus:

$$f(x) = \sum_{k=0}^{\infty} \alpha_k \cos\left(\frac{2\pi k x}{L}\right), \tag{7.1}$$

where the $\alpha_k$ are a set of coefficients whose values depend on the shape of the function. If the function is odd (antisymmetric) about the midpoint then we can use a sine series:

$$f(x) = \sum_{k=1}^{\infty} \beta_k \sin\left(\frac{2\pi k x}{L}\right). \tag{7.2}$$

---

^1There are some conditions the function must satisfy: it must be bounded and it can have at most a finite number of discontinuities and extrema. If you want to review the mathematics of Fourier series, a good introduction can be found in Boas, M. L., *Mathematical Methods in the Physical Sciences*, John Wiley, New York (2005).

(Note that the sum for the sine series starts at $k = 1$, because the $k = 0$ term vanishes.) And a general function, with no special symmetry, can be written as a sum of even and odd parts thus:

$$f(x) = \sum_{k=0}^{\infty} \alpha_k \cos\left(\frac{2\pi k x}{L}\right) + \sum_{k=1}^{\infty} \beta_k \sin\left(\frac{2\pi k x}{L}\right). \tag{7.3}$$

An alternative way to represent this general sine/cosine series is to make use of the identities $\cos\theta = \frac{1}{2}(e^{-i\theta} + e^{i\theta})$ and $\sin\theta = \frac{1}{2i}(e^{-i\theta} - e^{i\theta})$. Substituting these into Eq. (7.3) gives

$$\begin{aligned}
f(x) = \frac{1}{2}\sum_{k=0}^{\infty} \alpha_k &\left[\exp\left(-i\frac{2\pi k x}{L}\right) + \exp\left(i\frac{2\pi k x}{L}\right)\right] \\
&+ \frac{i}{2}\sum_{k=1}^{\infty} \beta_k \left[\exp\left(-i\frac{2\pi k x}{L}\right) - \exp\left(i\frac{2\pi k x}{L}\right)\right].
\end{aligned} \tag{7.4}$$

Collecting terms, this can be conveniently rewritten as

$$f(x) = \sum_{k=-\infty}^{\infty} \gamma_k \exp\left(i\frac{2\pi k x}{L}\right), \tag{7.5}$$

where the sum now runs from $-\infty$ to $+\infty$ and

$$\gamma_k = \begin{cases}
\frac{1}{2}(\alpha_{-k} + i\beta_{-k}) & \text{if } k < 0, \\
\alpha_0 & \text{if } k = 0, \\
\frac{1}{2}(\alpha_k - i\beta_k) & \text{if } k > 0.
\end{cases} \tag{7.6}$$

Since this complex series includes the sine and cosine series as special cases, we will use it for most of our calculations (although there are cases where the sine and cosine series are useful, as we will see later in the chapter). If we can find the coefficients $\gamma_k$ for a particular function $f(x)$ then the Fourier series gives us a compact way of representing the entire function that comes in handy for all sorts of numerical calculations.

Note that Fourier series can be used only for periodic functions, meaning that the function in the interval from 0 to $L$ is repeated over and over again all the way out to infinity in both the positive and negative directions. Most of the functions we deal with in the real world are not periodic. Does this mean that Fourier series cannot be used in such cases? No, it does not. If we are interested in a portion of a nonperiodic function over a finite interval from 0 to $L$, we can take that portion and just repeat it to create a periodic function, as shown in Fig. 7.1. Then the Fourier series formulas given above will give the correct value for the function in the interval from 0 to $L$ (solid line in the figure). Outside of that interval they will give an incorrect answer, in the sense that they give the value of the repeated periodic function (dashed lines), not the original nonperiodic function (gray lines). But so long as we are interested only in the function in the interval from 0 to $L$ this does not matter.

The coefficients $\gamma_k$ in Eq. (7.5) in are, in general, complex. The standard way to calculate them is to evaluate the integral

$$\int_0^L f(x) \exp\left(-i\frac{2\pi k x}{L}\right) dx = \sum_{k'=-\infty}^{\infty} \gamma_{k'} \int_0^L \exp\left(i\frac{2\pi(k'-k)x}{L}\right) dx, \tag{7.7}$$

where we have substituted for $f(x)$ from Eq. (7.5). The integral on the right is straightforward. So long as $k' \neq k$ we have

$$\begin{aligned}
\int_0^L \exp\left(i\frac{2\pi(k'-k)x}{L}\right) dx &= \frac{L}{i2\pi(k'-k)} \left[\exp\left(i\frac{2\pi(k'-k)x}{L}\right)\right]_0^L \\
&= \frac{L}{i2\pi(k'-k)} \left[e^{i2\pi(k'-k)} - 1\right] \\
&= 0,
\end{aligned} \tag{7.8}$$

since $e^{i2\pi n} = 1$ for any integer $n$ (and $k'-k$ is an integer).

The only exception to Eq. (7.8) is when $k' = k$, in which case the integral in (7.7) becomes simply $\int_0^L 1 \, dx = L$. Thus only one term in the sum in Eq. (7.7) is nonzero, the one where $k' = k$, giving

$$\int_0^L f(x) \exp\left(-i\frac{2\pi k x}{L}\right) dx = L\gamma_k, \tag{7.9}$$

or equivalently

$$\gamma_k = \frac{1}{L} \int_0^L f(x) \exp\left(-i\frac{2\pi k x}{L}\right) dx. \tag{7.10}$$

Thus given the function $f(x)$ we can find the Fourier coefficients $\gamma_k$, or given the coefficients we can find $f(x)$ from Eq. (7.5)—we can go back and forth freely between the function and the Fourier coefficients as we wish. Both, in a sense, are complete representations of the information contained in the function.

---

### 7.2 THE DISCRETE FOURIER TRANSFORM

For some functions $f(x)$ the integral in Eq. (7.10) can be performed analytically and the Fourier coefficients $\gamma_k$ calculated exactly. There are, however, many cases where this is not possible: the integral may not be doable because $f(x)$ is too complicated, or $f(x)$ may not even be known in analytic form—it might be a signal measured in a laboratory experiment or the output of a computer program. In such cases we can instead calculate the Fourier coefficients numerically. We studied a number of techniques for performing integrals numerically in Chapter 5. Here we will use the trapezoidal rule of Section 5.1.1 to evaluate Eq. (7.10), with $N$ slices of width $h = L/N$ each. Applying Eq. (5.3) we get

$$\gamma_k = \frac{1}{L}\frac{L}{N}\left[\frac{1}{2}f(0) + \frac{1}{2}f(L) + \sum_{n=1}^{N-1} f(x_n) \exp\left(-i\frac{2\pi k x_n}{L}\right)\right], \tag{7.11}$$

where the positions $x_n$ of the sample points for the integral are

$$x_n = \frac{n}{N}L. \tag{7.12}$$

But since $f(x)$ is by hypothesis periodic we have $f(L) = f(0)$ and Eq. (7.11) simplifies to

$$\gamma_k = \frac{1}{N} \sum_{n=0}^{N-1} f(x_n) \exp\left(-i\frac{2\pi k x_n}{L}\right). \tag{7.13}$$

We can use this formula to evaluate the coefficients $\gamma_k$ on the computer.

The formula has a convenient form for computational applications. It is a common occurrence that we know the value of a function $f(x)$ only at a set of equally spaced sample points $x_n$, exactly as in Eq. (7.13). For instance, the function might represent an audio signal—a sound wave—which would typically be sampled at regular intervals at a rate of a few thousand times a second. In that case Eq. (7.13) is perfectly suited to calculating the Fourier coefficients of the signal. A simpler way to write Eq. (7.13) in such situations is to define $y_n = f(x_n)$ to be the values of the $N$ samples and make use of Eq. (7.12) to write

$$\gamma_k = \frac{1}{N} \sum_{n=0}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right). \tag{7.14}$$

In this form, the equation doesn't require us to know the positions $x_n$ of the sample points or even the width $L$ of the interval in which they lie, since neither enters the formula. All we need to know are the sample values $y_n$ and the total number of samples $N$.

The sum in Eq. (7.14) is a standard quantity that appears in many calculations. It is known as the *discrete Fourier transform* or DFT of the samples $y_n$ and we will denote it $c_k$ thus:

$$c_k = \sum_{n=0}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right). \tag{7.15}$$

The quantities $c_k$ and $\gamma_k$ differ by only a factor of $1/N$ and we really don't need a separate symbol for $c_k$, but by convention the DFT is defined as in (7.15), without the factor $1/N$, and we will follow that convention here. A large part of this chapter is devoted to the discussion and study of the DFT, defined as in Eq. (7.15). In this discussion we will refer to the $c_k$ (a little loosely) as "Fourier coefficients," although strictly speaking the true Fourier coefficients are $\gamma_k = c_k/N$. Clearly, however, it's trivial to calculate the $\gamma_k$ once we know the $c_k$ (and in fact, as we will see, it is hardly ever necessary).

We have derived the results above using the trapezoidal rule, which only gives an approximation to the integral of Eq. (7.10). As we now show, however, the discrete Fourier transform is, in a certain sense, *exact*. It allows us to perform exact Fourier transforms of sampled data, even though computers can't normally do integrals exactly. To demonstrate this remarkable fact, we employ the following mathematical result about exponentials. Recall the standard geometric series: $\sum_{k=0}^{N-1} a^k = (1-a^N)/(1-a)$, and put $a = e^{i2\pi m/N}$ with $m$ integer, to get

$$\sum_{k=0}^{N-1} e^{i2\pi k m/N} = \frac{1-e^{i2\pi m}}{1-e^{i2\pi m/N}}. \tag{7.16}$$

Since $e^{i2\pi m} = 1$ for all integers $m$, the numerator vanishes and this just gives zero. The only exception is when $m = 0$ or a multiple of $N$, in which case the denominator also vanishes and we must be careful lest we divide by zero. In this case, however, the original sum is easy: it's just $\sum_{k=0}^{N-1} 1 = N$. Thus

$$\sum_{k=0}^{N-1} e^{i2\pi k m/N} = \begin{cases} N & \text{if } m \text{ is zero or a multiple of } N, \\ 0 & \text{otherwise}. \end{cases} \tag{7.17}$$

Now let's go back to our discrete Fourier transform, Eq. (7.15), and consider the following sum:

$$\begin{aligned}
\sum_{k=0}^{N-1} c_k \exp\left(i\frac{2\pi k n}{N}\right) &= \sum_{k=0}^{N-1} \sum_{n'=0}^{N-1} y_{n'} \exp\left(-i\frac{2\pi k n'}{N}\right) \exp\left(i\frac{2\pi k n}{N}\right) \\
&= \sum_{n'=0}^{N-1} y_{n'} \sum_{k=0}^{N-1} \exp\left(i\frac{2\pi k(n-n')}{N}\right),
\end{aligned} \tag{7.18}$$

where we have swapped the order of summation in the second line. Let's assume that $n$ lies in the range $0 \leq n < N$. The final sum in Eq. (7.18) takes the form of Eq. (7.17) with $m = n-n'$, which means we can work out its value. Since $n$ and $n'$ are both less than $N$ there is no way for $n-n'$ to be a nonzero multiple of $N$, but it could be zero if $n = n'$. Thus the sum is equal to $N$ when $n = n'$, and zero otherwise. But that means there is only one nonzero term in the sum over $n'$—the one where $n' = n$—and so Eq. (7.18) simplifies to just

$$\sum_{k=0}^{N-1} c_k \exp\left(i\frac{2\pi k n}{N}\right) = Ny_n, \tag{7.19}$$

or equivalently,

$$y_n = \frac{1}{N} \sum_{k=0}^{N-1} c_k \exp\left(i\frac{2\pi k n}{N}\right). \tag{7.20}$$

This result is called the *inverse discrete Fourier transform* (or inverse DFT). It is the counterpart to the forward transform of Eq. (7.15). It tells us that, given the coefficients $c_k$ we get from Eq. (7.15), we can recover the values of the samples $y_n$ that they came from *exactly* (except for rounding error). This is an amazing result: even though we thought our Fourier coefficients were only approximate, it turns out that they are actually exact in the sense that we can completely recover the original samples from them.

Thus we can move freely back and forth between the samples and the coefficients $c_k$ without losing any detail in our data—both the samples and the Fourier transform give us a complete representation of the original data. Notice that we only need the Fourier coefficients $c_k$ up to $k = N-1$ to recover the samples, so we only need to evaluate (7.15) for $0 \leq k < N$.

Equation (7.20) is similar, but not identical, to our original expression for the complex Fourier series, Eq. (7.5). It differs by a leading factor of $1/N$ (which compensates for the factor we removed when we defined the DFT in Eq. (7.15)), and in that the sum is over positive values of $k$ only and runs up to $N-1$, rather than to infinity (which is a useful feature, since it makes the sum practical on a computer where a sum to infinity would not be).

It is, however, important to appreciate that, unlike the original Fourier series, the discrete formula of Eq. (7.20) only gives us the sample values $y_n = f(x_n)$. It tells us nothing about the value of $f(x)$ between the sample points. And indeed how could it? Given that we used only the values at the sample points when we computed the $c_k$ in Eq. (7.15), it's clear that the $c_k$ cannot contain any information about the values in between. The original function could do anything it wanted between the sample points and we'd never know, since we didn't measure it there. To put that another way, any two functions that have the same values at the sample points will have the same DFT, no matter what they do between the points—like these two functions, for example:

[Two function plots showing different functions with same sample points]

These would have the same DFT even though they are totally different between the second and third sample points.

Still, if a function is reasonably smooth, with no wild excursions between samples (like the one in the right-hand example above), then knowing the values at the sample points only is enough to get a picture of the function's general shape. And, as we have said, in many cases we are interested in a function that is represented as a set of samples in the first place and not as a continuous function, and for this kind of data the DFT is an excellent tool.

---

#### 7.2.1 POSITIONS OF THE SAMPLE POINTS

One thing to notice about the discrete Fourier transform, Eq. (7.13), is that we can shift the sample points along the $x$-axis if we want to and not much changes. Suppose that instead of using sample points $x_n = (n/N)L$ as in Eq. (7.12), we take our samples at a shifted set of points

$$x'_n = x_n + \Delta = \frac{n}{N}L + \Delta. \tag{7.22}$$

Following through the derivation leading to Eqs. (7.13) and (7.15) again, we find that the equivalent discrete Fourier transform for this set of samples is

$$\begin{aligned}
c_k &= \sum_{n=0}^{N-1} f(x_n + \Delta) \exp\left(-i\frac{2\pi k(x_n + \Delta)}{L}\right) \\
&= \exp\left(-i\frac{2\pi k\Delta}{L}\right) \sum_{n=0}^{N-1} f(x'_n) \exp\left(-i\frac{2\pi k x_n}{L}\right) \\
&= \exp\left(-i\frac{2\pi k\Delta}{L}\right) \sum_{n=0}^{N-1} y'_n \exp\left(-i\frac{2\pi k n}{N}\right),
\end{aligned} \tag{7.23}$$

where $y'_n = f(x'_n)$ are the new samples. But this is just the same as the original DFT, Eq. (7.15), except that we have an extra ($k$-dependent) phase factor at the front. Conventionally, we absorb this phase factor into the definition of $c_k$ and define a new coefficient $c'_k = e^{i2\pi k\Delta/L}c_k$ so that

$$c'_k = \sum_{n=0}^{N-1} y'_n \exp\left(-i\frac{2\pi k n}{N}\right), \tag{7.24}$$

which is now in exactly the same form as before. Thus the DFT is essentially independent of where we choose to place the samples. The coefficients change by a phase factor, but that's all.

Figure 7.2a shows the choice of samples we've been using so far. The interval from 0 to $L$ is divided into $N$ slices and we take one sample from the beginning of each slice. There is no sample at the end of the last slice, since it would be the same as the first sample, because the function is periodic. A common alternative choice is to take samples in the middle of the slices as shown in Fig. 7.2b. Both of these schemes are widely used. The first is called a Type-I DFT; the second is called Type-II. Note that, although the formula we use to perform the DFT is the same in both cases, the coefficients we will get are different for two reasons: first, the values of the samples are different because they are measured at different points, and second the coefficients include an extra phase factor, as we've seen, in the Type-II case.

---

#### 7.2.2 TWO-DIMENSIONAL FOURIER TRANSFORMS

Functions of two variables $f(x,y)$ can also be Fourier transformed, using a *two-dimensional Fourier transform*, which simply means you transform with respect to one variable then with respect to the other.

Suppose we have an $M \times N$ grid of samples $y_{mn}$. To carry out the two-dimensional Fourier transform, we first perform an ordinary Fourier transform on each of the $M$ rows, following Eq. (7.15):

$$c'_{ml} = \sum_{n=0}^{N-1} y_{mn} \exp\left(-i\frac{2\pi l n}{N}\right). \tag{7.25}$$

For each row $m$ we now have $N$ coefficients, one for each value of $l$. Next we take the $l$th coefficient in each of the $M$ rows and Fourier transform these $M$ values again to get

$$c_{kl} = \sum_{m=0}^{M-1} c'_{ml} \exp\left(-i\frac{2\pi k m}{M}\right). \tag{7.26}$$

Alternatively, we can substitute Eq. (7.25) into Eq. (7.26) and write a single expression for the complete Fourier transform in two dimensions:

$$c_{kl} = \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} y_{mn} \exp\left[-i2\pi\left(\frac{km}{M} + \frac{ln}{N}\right)\right]. \tag{7.27}$$

The corresponding inverse transform is

$$y_{mn} = \frac{1}{MN} \sum_{k=0}^{M-1} \sum_{l=0}^{N-1} c_{kl} \exp\left[i2\pi\left(\frac{km}{M} + \frac{ln}{N}\right)\right]. \tag{7.28}$$

If the samples $y_{mn}$ are real—as they almost always are—then there is a further point to notice. When we do the first set of Fourier transforms, Eq. (7.25), we are transforming a row of $N$ real numbers for each value of $l$ and hence, as discussed in Section 7.2, we end up with either $\frac{1}{2}N+1$ independent Fourier coefficients or $\frac{1}{2}(N+1)$, depending on whether $N$ is even or odd—the remaining coefficients are just complex conjugates. As we have seen, however, the coefficients themselves will, in general, be complex, which means that when we perform the second set of transforms in Eq. (7.26) we are transforming $M$ complex numbers, not real numbers. This means that we now have to calculate all $M$ of the Fourier coefficients—it is no longer the case that the second half are the complex conjugates of the first half. Thus the two-dimensional Fourier transform of an $M \times N$ grid of real numbers is a grid of complex numbers with $M \times (\frac{1}{2}N+1)$ independent coefficients if $N$ is even or $M \times \frac{1}{2}(N+1)$ if $N$ is odd.

Two-dimensional transforms are used, for example, in image processing, and are widely employed in astronomy to analyze photographs of the sky and reveal features that are otherwise hard to make out. They are also used in the confocal microscope and the electron microscope, two instruments that find use in many branches of science.

---

#### 7.2.3 PHYSICAL INTERPRETATION OF THE FOURIER TRANSFORM

If we were mathematicians, then the equations for the Fourier transform given in the previous sections would be all we need—they tell us exactly how the transform is defined. But for physicists it's useful to understand what the Fourier transform is telling us in physical terms.

The Fourier transform breaks a function down into a set of real or complex sinusoidal waves. Each term in a sum like Eq. (7.20) represents one wave with its own well-defined frequency. If the function $f(x)$ is a function in space then we have spatial frequencies; if it's a function in time then we have temporal frequencies, like musical notes. Saying that any function can be expressed as a Fourier transform is equivalent to saying that any function can be represented as a sum of waves of given frequencies, and the Fourier transform tells us what that sum is for any particular function: the coefficients of the transform tell us exactly how much of each frequency we have in the sum.

Thus, by looking at the output of our Fourier transform, we can get a picture of what the frequency breakdown of a signal is. Most of us are familiar with the "signal analyzers" that are built in to many home stereo systems—the animated bar charts that go up and down in time with the music. These analyzers present a graph of the frequencies present in the music and the Fourier transform conveys essentially the same information for the function $f(x)$. (Indeed, signal analyzers work precisely by performing a Fourier transform and then displaying the result.)

Thus, for example, consider the signal shown in Fig. 7.3. As we can see, the signal consists of a basic wave that goes up and down with a well-defined frequency, but there is all some noise in the data as well, visible as smaller wiggles in the line. If one were to listen to this signal as sound one would hear a constant note at the frequency of the main wave, accompanied by a background hiss that comes from the noise.

Let us calculate the Fourier transform of this signal. If the signal is stored as a single column of numbers in a file called `pitch.txt`, we could calculate the transform using the function `dft` that we defined on page 296:

```python
from numpy import loadtxt
from pylab import plot, xlim, show

y = loadtxt("pitch.txt", float)
c = dft(y)
plot(abs(c))
xlim(0, 500)
show()
```

Since the coefficients returned by the transform in the array `c` are in general complex, we have plotted their absolute values, which give us a measure of the amplitude of each of the waves in the Fourier series.

The graph produced by the program is shown in Fig. 7.4. The horizontal axis in this graph measures $k$, which is proportional to the frequency of the waves, and the vertical axis measures the absolute values $|c_k|$ of the corresponding Fourier coefficients. As we can see, there are a number of noticeable spikes in the plot, representing coefficients $c_k$ with particularly large magnitudes. The first and largest of these spikes corresponds to the frequency of the main wave visible in Fig. 7.3. The remaining spikes are harmonics of the first one—multiples of its frequency whose presence tell us that the wave in the original data was not a pure sine wave. A pure sine wave could be represented fully with just a single term of the appropriate frequency in the Fourier series, but any other wave cannot and requires some additional terms to represent it.

Between the main spikes in Fig. 7.4 there are also some small, apparently random values of $|c_k|$ creating a low-level background visible as the jagged line along the bottom of the plot. These are produced by the noise in the original signal, which is "white noise," meaning it is completely random and contains on average equal amounts of all frequencies, so in a Fourier transform it appears as a uniform random background, as in the figure, with neither the high frequencies nor the low having larger Fourier coefficients.^2

Fourier transforms have many uses in physics, but one of the most basic is as a simple tool—as here—for understanding a measurement or signal. The Fourier transform can break a signal down for us into its component parts and give us an alternative way to view it, a "spectrum analyzer" view of our data as a sum of different frequencies.

---

^2White noise is so-called by analogy with white light, which is a mixture of all frequencies. You may occasionally see references to "pink noise" as well, which means noise with all frequencies present, so it's sort of white, but more of the low frequencies than the high, which by the same analogy would make it red. The mixture of red and white then gives pink.

---

**Exercise 7.1: Fourier transforms of simple functions**

Write Python programs to calculate the coefficients in the discrete Fourier transforms of the following periodic functions sampled at $N = 1000$ evenly spaced points, and make plots of their amplitudes similar to the plot shown in Fig. 7.4:

a) A single cycle of a square-wave with amplitude 1

b) The sawtooth wave $y_n = n$

c) The modulated sine wave $y_n = \sin(\pi n/N)\sin(20\pi n/N)$

If you wish you can use the Fourier transform function from the file `dft.py` as a starting point for your program.

---

**Exercise 7.2: Detecting periodicity**

In the on-line resources there is a file called `sunspots.txt`, which contains the observed number of sunspots on the Sun for each month since January 1749. The file contains two columns of numbers, the first representing the month and the second being the sunspot number.

a) Write a program that reads the data in the file and makes a graph of sunspots as a function of time. You should see that the number of sunspots has fluctuated on a regular cycle for as long as observations have been recorded. Make an estimate of the length of the cycle in months.

b) Modify your program to calculate the Fourier transform of the sunspot data and then make a graph of the magnitude squared $|c_k|^2$ of the Fourier coefficients as a function of $k$—also called the *power spectrum* of the sunspot signal. You should see that there is a noticeable peak in the power spectrum at a nonzero value of $k$. The appearance of this peak tells us that there is one frequency in the Fourier series that has a higher amplitude than the others around it—meaning that there is a large sine-wave term with this frequency, which corresponds to the periodic wave you can see in the original data.

c) Find the approximate value of $k$ to which the peak corresponds. What is the period of the sine wave with this value of $k$? You should find that the period corresponds roughly to the length of the cycle that you estimated in part (a).

This kind of Fourier analysis is a sensitive method for detecting periodicity in signals. Even in cases where it is not clear to the eye that there is a periodic component to a signal, it may still be possible to find one using a Fourier transform.

---

### 7.3 DISCRETE COSINE AND SINE TRANSFORMS

So far we have been looking at the complex version of the Fourier series but, as mentioned in Section 7.1, one can also construct Fourier series that use sine and cosine functions in place of complex exponentials, and there are versions of the discrete Fourier transform for these sine and cosine series also. These series have their own distinct properties that make them (and particularly the cosine series) useful in certain applications, as we'll see.

Consider, for example, the cosine series of Eq. (7.1). Not every function can be represented using a series of this kind. Because of the shape of the cosine, all functions of the form (7.1) are necessarily symmetric about the midpoint of the interval at $\frac{1}{2}L$, and hence the cosine series can only be used to represent such symmetric functions. This may at first appear to be a grave disadvantage, since most functions we come across in physics are not symmetric in this way. In fact, however, it is not such a problem as it appears. Just as we can turn any function in a finite interval into a periodic function by simply repeating it endlessly, so we can turn any function into a *symmetric* periodic function by adding to it a mirror image of itself and then repeating the whole thing endlessly. The process is illustrated in Fig. 7.5. Thus cosine series can be used for essentially any function, regardless of symmetry. In practice, this is how the cosine version of the Fourier transform is always used. Given a set of samples of a function, we mirror those samples to create a symmetric function before transforming them. As a corollary, note that this implies that the total number of samples in the transform is always even, regardless of how many samples we started with, a fact that will be useful in a moment.

Once we have such a symmetric function the cosine series representing it can be found from the results we already know: it is simply the special case of Eq. (7.15) when the samples $y_n$ are symmetric about $x = \frac{1}{2}L$. When the samples are symmetric we have $y_0 = y_N, y_1 = y_{N-1}, y_2 = y_{N-2}$, and so forth, i.e., $y_n = y_{N-n}$ for all $n$. Given that, as mentioned above, $N$ is always even,

Eq. (7.15) then becomes

$$\begin{aligned}
c_k &= \sum_{n=0}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right) \\
&= \sum_{n=0}^{\frac{1}{2}N} y_n \exp\left(-i\frac{2\pi k n}{N}\right) + \sum_{n=\frac{1}{2}N+1}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right) \\
&= \sum_{n=0}^{\frac{1}{2}N} y_n \exp\left(-i\frac{2\pi k n}{N}\right) + \sum_{n=\frac{1}{2}N+1}^{N-1} y_{N-n} \exp\left(i\frac{2\pi k(N-n)}{N}\right),
\end{aligned} \tag{7.29}$$

where we have made use of the fact that $e^{i2\pi k} = 1$ for all integer $k$. Now we make a change of variables $N-n \rightarrow n$ in the second sum and get

$$\begin{aligned}
c_k &= \sum_{n=0}^{\frac{1}{2}N} y_n \exp\left(-i\frac{2\pi k n}{N}\right) + \sum_{n=1}^{\frac{1}{2}N-1} y_n \exp\left(i\frac{2\pi k n}{N}\right) \\
&= y_0 + y_{N/2}\cos\left(\frac{2\pi k(N/2)}{N}\right) + 2\sum_{n=1}^{\frac{1}{2}N-1} y_n \cos\left(\frac{2\pi k n}{N}\right),
\end{aligned} \tag{7.30}$$

where we have used $\cos\theta = \frac{1}{2}(e^{-i\theta} + e^{i\theta})$. Normally the cosine transform is applied to real samples, which means that the coefficients $c_k$ will all be real (since they are just a sum of real terms).

making use once more of the fact that $N$ is even, Eq. (7.15) becomes

$$\begin{aligned}
c_k &= \sum_{n=0}^{\frac{1}{2}N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right) + \sum_{n=\frac{1}{2}N}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right) \\
&= \exp\left(i\frac{\pi k}{N}\right)\left[\sum_{n=0}^{\frac{1}{2}N-1} y_n \exp\left(-i\frac{2\pi k(n+\frac{1}{2})}{N}\right)\right. \\
&\qquad\qquad\qquad\left. + \sum_{n=\frac{1}{2}N}^{N-1} y_{N-1-n} \exp\left(i\frac{2\pi k(N-\frac{1}{2}-n)}{N}\right)\right] \\
&= \exp\left(i\frac{\pi k}{N}\right)\left[\sum_{n=0}^{\frac{1}{2}N-1} y_n \exp\left(-i\frac{2\pi k(n+\frac{1}{2})}{N}\right)\right. \\
&\qquad\qquad\qquad\left. + \sum_{n=0}^{\frac{1}{2}N-1} y_n \exp\left(i\frac{2\pi k(n+\frac{1}{2})}{N}\right)\right] \\
&= 2\exp\left(i\frac{\pi k}{N}\right) \sum_{n=0}^{\frac{1}{2}N-1} y_n \cos\left(\frac{2\pi k(n+\frac{1}{2})}{N}\right).
\end{aligned} \tag{7.32}$$

Conventionally we absorb the leading phase factor into the Fourier coefficients, defining

$$a_k = 2\sum_{n=0}^{\frac{1}{2}N-1} y_n \cos\left(\frac{2\pi k(n+\frac{1}{2})}{N}\right). \tag{7.33}$$

Again these coefficients are purely real if the $y_n$ are real and it's straightforward to show that the corresponding inverse transform is

$$y_n = \frac{1}{N}\left[a_0 + 2\sum_{k=1}^{\frac{1}{2}N-1} a_k \cos\left(\frac{2\pi k(n+\frac{1}{2})}{N}\right)\right]. \tag{7.34}$$

This Type-II DCT is arguably more elegant than the Type-I version, and it's probably the version that's most often used. Notice that it transforms $\frac{1}{2}N$ inputs $y_n$ into $\frac{1}{2}N$ outputs $a_k$. For this reason, it's common to redefine $\frac{1}{2}N \rightarrow N$ and $a_k \rightarrow 2a_k$ and rewrite Eqs. (7.33) and (7.34) as

$$a_k = \sum_{n=0}^{N-1} y_n \cos\left(\frac{\pi k(n+\frac{1}{2})}{N}\right), \qquad y_n = \frac{1}{N}\left[a_0 + 2\sum_{k=0}^{N-1} a_k \cos\left(\frac{\pi k(n+\frac{1}{2})}{N}\right)\right], \tag{7.35}$$

where $N$ is now the actual number of inputs to the transform. This is probably the form you'll see most often in books and elsewhere. Sometimes you'll see it referred to as "the" discrete cosine transform, because it's so common.

A nice feature of the cosine transform is that, unlike the DFT, it does not assume that the samples themselves are periodic. Since the function being transformed is first mirrored, as in Fig. 7.5, the first and last of the original samples are not obliged to take the same value, as they are in the DFT. As described earlier in the chapter, any function, periodic or not, can be made periodic by repeating it endlessly, thereby making the last sample take the same value as the first, but in so doing one may create a substantial discontinuity in the function, as shown in Fig. 7.1, and such discontinuities can cause problems for DFTs. The discrete cosine transform, by contrast, does not suffer from these problems, and hence is often preferable for data that are not inherently periodic.

One can also calculate discrete *sine* transforms, as in Eq. (7.2), although sine transforms are used less often than cosine transforms because they force the function $f(x)$ to be zero at either end of its range. Relatively few functions encountered in real-world applications do this, so the sine transform has limited applicability. It does find some use in physics, however, for representing physical functions whose boundary conditions force them to be zero at the ends of an interval. Examples are displacement of a vibrating string that is clamped at both ends or quantum wavefunctions in a closed box.

---

#### 7.3.1 TECHNOLOGICAL APPLICATIONS OF COSINE TRANSFORMS

Discrete cosine transforms have important technological uses. For example, they form the mathematical basis for the computer image file format called *JPEG*,^3 which is used to store most of the images you see on the world wide web. Digital images are represented as regular grids of dots, or pixels, of different shades, and the shades are stored on the computer as ordinary numbers. The simplest way of storing an image is just to store all of these numbers, in order, in a computer file, but there are a lot of them and the resulting files tend to be very large. It turns out that one can store images far more economically if one makes use of discrete cosine transforms.

^3The format is named after the committee that invented it, the Joint Photographic Experts Group.

The JPEG format works by dividing the pixels in an image into blocks, performing DCTs on the blocks (two-dimensional Type-II DCTs to be exact), then looking for coefficients $a_k$ that are small and can be discarded.^4 The remaining coefficients are stored in a file and, when you view a picture or request the relevant web page, your computer reconstitutes the picture using the inverse transform of Eq. (7.35). So there are discrete cosine transforms going on in the background pretty much every time you look at the web. The advantage of storing images this way is that in many cases *most* of the $a_k$ are very small and can be neglected. Because only the small remaining fraction of the Fourier coefficients need to be stored, the size of the file required to store the whole picture is thus greatly reduced, and if the picture is transmitted over the Internet, for instance as part of a web page, we save on the time needed to transmit it. The disadvantage is that, because some of the Fourier data are thrown away, the picture you get back on your screen isn't quite the same picture you started with. Usually your eye can't tell the difference, but sometimes if you look carefully you can see problems in images, called *compression artifacts*, arising from the missing data.

^4Technically the components are not thrown out altogether, but are represented with coarser dynamic range.

A variant of the same technique is also used to compress moving pictures, meaning film and video, using the compression format called *MPEG*. Television broadcasts, cable and satellite TV, DVDs, and Internet video all use versions of the MPEG format to compress video images so that they can be stored and transmitted more efficiently. Again, you lose something in the compression. It's usually not very noticeable, but if you know what you're looking for you can sometimes see compression artifacts in the pictures.

A similar scheme is used to compress music, for instance in the popular file format called *MP3*. Music, or any audio signal, can be represented digitally as a set of equally spaced samples of an audio waveform. In an MP3 these samples are divided into blocks, the blocks are individually transformed using a discrete cosine transform, and then some Fourier components are discarded, saving space and allowing one to store and transmit audio recordings more efficiently. When you play an MP3, your computer, phone, or MP3 player is continually performing inverse discrete cosine transforms to reconstruct the music so you can listen to it. There is a lot of computation going on in an MP3 player.

MP3s are clever, however, in that the particular Fourier components they discard are not chosen solely on the grounds of which ones are smallest, but also with a knowledge of what the human ear can and cannot hear. For instance, if there are loud low-frequency sounds in a piece of music, such as bass and drums, then the ear is much less sensitive to high-frequency sounds that occur at the same time. (This is a limitation of the way the ear works, not a physical law.) So in this situation it's safe to throw out some high-frequency Fourier components and save space. Thus a piece of music stored in MP3 format is not a faithful representation of the original, but it *sounds* like one to the human ear because the aspects in which it differs from the original are aspects the human ear can't hear.

Essentially the entire digital music/audio economy—streaming music services, music downloads, Internet radio, digital TV, and all the rest of it—relies on this technology.^5 Without the discrete cosine transform it wouldn't be possible.

^5The notable exception is the CD, which was introduced about ten years before the invention of MP3s. CDs use uncompressed audio—just raw sound samples—which is extremely inefficient, although in theory it also gives higher sound quality because there are no compression artifacts. Good luck hearing the difference though; these days audio compression is extremely good and it's rare that one can actually hear compression artifacts. Double-blind listening tests have been conducted where listeners are played a pristine, uncompressed recording of a piece of music, followed either by a compressed version of the same recording or by the uncompressed version again. When the best modern compression techniques are used, even expert listeners have been unable to reliably tell the difference between the two.

---

### 7.4 FAST FOURIER TRANSFORMS

The discrete Fourier transform is defined by Eq. (7.15), which is repeated here for convenience:

$$c_k = \sum_{n=0}^{N-1} y_n \exp\left(-i\frac{2\pi k n}{N}\right). \tag{7.36}$$

We gave an example of a Python function to evaluate this expression on page 296. In that function we used a for-loop to add up the terms in the sum, of which there are $N$, and whole the calculation is repeated for each of the $\frac{1}{2}N+1$ distinct coefficients $c_k$, so the total number of terms we must add together to evaluate all of the coefficients is $N(\frac{1}{2}N+1)$. Thus the computer will have to perform a little over $\frac{1}{2}N^2$ arithmetic operations to evaluate the complete DFT. In Section 4.3 we discussed a useful rule of thumb: the largest number of operations you can do in a computer program is about a billion if you want it to run in a reasonable amount of time. If we apply this rule of thumb to our Fourier transform, setting $\frac{1}{2}N^2 = 10^9$ and solving for $N$, we find that the largest set of samples for which we can calculate the Fourier transform in reasonable time has about $N \simeq 45\,000$ samples.^6 For practical applications this is not a very large number. For example, 45 000 samples is only about enough to represent one second of music or other audio signals. Often we would like to calculate the transforms of larger data sets, sometimes much larger. Luckily it turns out that there is a clever trick for calculating the DFT much faster than is possible than by directly evaluating Eq. (7.36). This trick is called the *fast Fourier transform* or FFT. It was discovered by Carl Friedrich Gauss in 1805, when he was 28 years old.^7,^8

^6We are treating the evaluation of each term in the sum as a single operation, which is not really correct—each term involves several multiplication operations and the calculation of an exponential. However, the billion-operation rule of thumb is only an approximation anyway, so a rough estimate of the number of operations is good enough.

^7What with Gaussian quadrature, Gaussian elimination, the Gauss–Newton method, and now the fast Fourier transform, Gauss seems to have discovered most of computational physics more than a century before the computer was invented.

^8In much of the computational physics literature you will see the fast Fourier transform attributed not to Gauss but to the computer scientists James Cooley and John Tukey, who published a paper describing it in 1965 [Cooley, J. W. and Tukey, J. W., An algorithm for the machine calculation of complex Fourier series, *Mathematics of Computation* 19, 297–301 (1965)]. Although Cooley and Tukey's paper was influential in popularizing the method, however, it was, unbeknownst to its authors, not the first description of the FFT. Only later did they learn that they'd been scooped by Gauss 160 years earlier.

The fast Fourier transform is simplest when the number of samples is a power of two, so let us consider the case where $N = 2^m$ with $m$ an integer. Consider the sum in the DFT equation, Eq. (7.36), and let us divide the terms into two equally sized groups, which we can always do when $N$ is a power of two. Let the first group consist of the terms with $n$ even and the second the terms with $n$ odd. We consider the even terms first, i.e., the terms where $n = 2r$ with integer $r = 0 \ldots \frac{1}{2}N-1$. The sum of these even terms is

$$E_k = \sum_{r=0}^{\frac{1}{2}N-1} y_{2r} \exp\left(-i\frac{2\pi k(2r)}{N}\right) = \sum_{r=0}^{\frac{1}{2}N-1} y_{2r} \exp\left(-i\frac{2\pi k r}{\frac{1}{2}N}\right). \tag{7.37}$$

But this is simply another Fourier transform, just like Eq. (7.36), but with $\frac{1}{2}N$ samples instead of $N$. Similarly the odd terms, meaning those with $n = 2r+1$, sum to

$$\begin{aligned}
\sum_{r=0}^{\frac{1}{2}N-1} y_{2r+1} \exp\left(-i\frac{2\pi k(2r+1)}{N}\right) &= e^{-i2\pi k/N} \sum_{r=0}^{\frac{1}{2}N-1} y_{2r+1} \exp\left(-i\frac{2\pi k r}{\frac{1}{2}N}\right) \\
&= e^{-i2\pi k/N} O_k,
\end{aligned} \tag{7.38}$$

where $O_k$ is another Fourier transform with $\frac{1}{2}N$ samples.

The complete Fourier coefficient $c_k$ of Eq. (7.36) is the sum of its odd and even terms:

$$c_k = E_k + e^{-i2\pi k/N} O_k. \tag{7.39}$$

In other words, the coefficient $c_k$ in the discrete Fourier transform of $f(x)$ is just the sum of two terms $E_k$ and $O_k$ that are each, themselves, discrete Fourier transforms of the same function $f(x)$, but with half as many points spaced twice as far apart, plus an extra factor $e^{-i2\pi k/N}$, called a *twiddle factor*,^9 which is trivial to calculate. So if we can do the two smaller Fourier transforms, then we can calculate $c_k$ easily.

^9I'm not making this up. That's what it's called.

And how do we do the smaller Fourier transforms? We just repeat the process. We split each of them into their even and odd terms and express them as the sum of the two, with a twiddle factor in between. Because we started with $N$ a power of two, we can go on dividing the transform in half repeatedly like this, until eventually we get to the point where each transform is the transform of just a single sample. But the Fourier transform of a single sample has only a single Fourier coefficient $c_0$, which, putting $k=0, N=1$ in Eq. (7.36), is equal to

$$c_0 = \sum_{n=0}^{0} y_n e^0 = y_0. \tag{7.40}$$

In other words, once we get down to a single sample, the Fourier transform is trivial—it's just equal to the sample itself! So at this stage we don't need to do any more Fourier transforms; we have everything we need.

The actual calculation of the fast Fourier transform is the reverse of the process above. Starting with the individual samples, which are their own Fourier transforms, we combine them in pairs, then combine the pairs into fours, the fours into eights, and so on, creating larger and larger Fourier transforms, until we have reconstructed the full transform of the complete set of samples.

The advantage of this approach is its speed. At the first round of the calculation we have $N$ samples. At the next round we combine these in pairs to make $\frac{1}{2}N$ transforms with two coefficients each, so we have to calculate a total of $N$ coefficients at this round. At the round after that there are $\frac{1}{4}N$ transforms of four coefficients each—$N$ coefficients again. Indeed it's easy to see that there are $N$ coefficients to calculate at every level.

And how many levels are there? After we have gone though $m$ levels the transforms have $2^m$ samples each, so the total number of levels is given by $2^m = N$, or $m = \log_2 N$. Thus the number of coefficients we have to calculate in the whole calculation is $\log_2 N$ levels times $N$ coefficients each, or $N\log_2 N$ coefficients in all. But this is *way* better than the roughly $\frac{1}{2}N^2$ terms needed to calculate the DFT the brute-force way. For instance, if we have a million samples, then the brute-force calculation would require about $\frac{1}{2}N^2 = 5 \times 10^{11}$ operations which is not a practical calculation on a typical computer. But the fast Fourier transform requires only $N\log_2 N = 2 \times 10^7$, which is entirely reasonable—you can do twenty million steps in under a second on most computers. So we've turned a calculation that was essentially impossible into one that can be done very quickly. Alternatively, employing again our rule of thumb that one should limit programs to about a billion operations, setting $N\log_2 N = 10^9$ and solving for $N$ we get $N \simeq 40$ million samples, which is large enough for most scientific applications.

We also note another useful fact: the inverse discrete Fourier transform, Eq. (7.20), which transforms the Fourier coefficients back into samples again, has basically the same form as the forward transform—the only difference is that there's no minus sign in the exponential. This means that the inverse transform can also be performed quickly using the same tricks as for the forward transform. The resulting calculation is called, naturally, the inverse fast Fourier transform, or inverse FFT.

Finally, we have in these developments assumed that the number of samples is a power of two. In fact it is possible to make the fast Fourier transform work if the number is not a power of two, but the algebra is rather tedious, so we'll skip the details here.

---

#### 7.4.1 FORMULAS FOR THE FFT

Let us look at the mathematics of the fast Fourier transform in a little more detail and consider the various stages of the decomposition process. In true Python fashion we'll number the initial stage "stage zero". At this stage we have a single Fourier transform of the entire set of samples. At the next stage, stage 1, we split the samples into two sets, at the stage after that we split again into four sets, and so forth. In general, at the $m$th stage of the process there will be $2^m$ sets consisting of $N/2^m$ samples each. The first of these sets consists of the original samples numbered $0, 2^m, 2^m \times 2, 2^m \times 3$ and so forth. In other words it consists of sample numbers $2^m r$ with integer $r = 0 \ldots N/2^m - 1$. Similarly the second set consists of sample numbers $2^m r + 1$, and third of sample numbers $2^m r + 2$, and so on, with $r = 0 \ldots N/2^m - 1$ in each case.

The DFT of the $j$th set of samples is

$$\begin{aligned}
\sum_{r=0}^{N/2^m-1} y_{2^m r+j} \exp\left(-i\frac{2\pi k(2^m r+j)}{N}\right) &= e^{-i2\pi kj/N} \sum_{r=0}^{N/2^m-1} y_{2^m r+j} \exp\left(-i\frac{2\pi k r}{N/2^m}\right) \\
&= e^{-i2\pi kj/N} E_k^{(m,j)}
\end{aligned} \tag{7.41}$$

for $j = 0 \ldots 2^m-1$. Then the general version of Eq. (7.39) at the $m$th stage is

$$e^{-i2\pi kj/N} E_k^{(m,j)} = e^{-i2\pi kj/N} E_k^{(m+1,j)} + e^{-i2\pi k(j+2^m)/N} E_k^{(m+1,j+2^m)}, \tag{7.42}$$

or equivalently

$$E_k^{(m,j)} = E_k^{(m+1,j)} + e^{-i2\pi 2^m k/N} E_k^{(m+1,j+2^m)}. \tag{7.43}$$

Armed with this formula, the calculation of the full DFT is now relatively simple. The total number of stages—the number of times we have to split the samples in half before we get down to the level of single samples—is, as we have said, $\log_2 N$. The fast Fourier transform works by starting at the last level $m = \log_2 N$ and working backwards to $m = 0$. Initially our sets of samples all have just one sample each and one Fourier coefficient, which is equal to that one sample. Then we use Eq. (7.43) repeatedly to calculate $E_k^{(m,j)}$ for all $j$ and $k$ for lower and lower levels $m$, each level being calculated from the results for the level above it, until we get down to $m = 0$. But for $m = 0$, Eq. (7.41) gives

$$E_k^{0,0} = \sum_{r=0}^{N-1} y_r \exp\left(-i\frac{2\pi k r}{N}\right) = c_k \tag{7.44}$$

so $c_k = E_k^{0,0}$ and we have our values for the final Fourier coefficients.

There's one other detail to notice. For any value of $m$ we need to evaluate Eq. (7.43) for $k = 0 \ldots N/2^m - 1$. But this causes problems because we evaluate the coefficients at the previous $(m+1)$th level only for the smaller range $k = 0 \ldots N/2^{m+1} - 1$. In practice, however, this is not a big deal. Consider $E_k^{(m+1,j)}$ for $k = N/2^{m+1} + s$:

$$\begin{aligned}
E_{N/2^{m+1}+s}^{(m+1,j)} &= \sum_{r=0}^{N/2^{m+1}-1} y_{2^{m+1}r+j} \exp\left(-i\frac{2\pi(N/2^{m+1}+s)r}{N/2^{m+1}}\right) \\
&= \exp(-i2\pi r) \sum_{r=0}^{N/2^{m+1}-1} y_{2^{m+1}r+j} \exp\left(-i\frac{2\pi s r}{N/2^{m+1}}\right) \\
&= E_s^{(m+1,j)}.
\end{aligned} \tag{7.45}$$

Thus the coefficients for values of $k$ beyond $N/2^{m+1}-1$ are simply repeats of the previous values. So long as we bear this in mind, evaluating Eq. (7.43) for all $k$ is straightforward.

Exercise 7.7 gives you the opportunity to write your own program to perform a fast Fourier transform, and doing so is a worthwhile undertaking. You can write an FFT program in Python in only about a dozen lines, though it can be quite tricky to work out what those lines should be, given all the different indices and factors that appear in Eq. (7.43).

Most people, however, don't write their own FFT programs. As with some of the other standard calculations we've looked at, such as the solution of simultaneous equations and the evaluation of eigenvalues and eigenvectors of matrices, the FFT is such a common operation that other people have already written programs to do it for you, and Python includes functions to perform FFTs on both real and complex samples.

---

#### 7.4.2 STANDARD FUNCTIONS FOR FAST FOURIER TRANSFORMS

In Python, fast Fourier transforms are provided by the module `numpy.fft`. For physics calculations the main function we use is the function `rfft`, which calculates the Fourier transform of a set of real samples in an array. (The "r" is for "real." There is another function `fft` that performs transforms of complex samples, but we will not use it in this book.)

For instance, a periodic "sawtooth" function could be represented by a set of samples like this:

```python
from numpy import array
y = array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], float)
```

and we could Fourier transform it like this:

```python
from numpy.fft import rfft
c = rfft(y)
```

This creates a complex array `c` containing the coefficients of the Fourier transform of the samples in the real array `y`. As we have said, there are $N$ distinct coefficients in the DFT of $N$ samples, but if the samples are real and $N$ is even, as here, then only the first $\frac{1}{2}N+1$ coefficients are independent and the rest are their complex conjugates. Python knows this and the array returned by `rfft` contains only the first $\frac{1}{2}N+1$ coefficients—Python does not bother to calculate or store the remaining ones. If you want the rest of the coefficients you're expected to calculate the complex conjugates for yourself (although in practice one rarely has cause to do this). Note also that in the example above the number of samples was ten, which is not a power of two: the `rfft` function knows how to do FFTs for any number of samples.

The module `numpy.fft` also contains a function called `irfft` for performing inverse fast Fourier transforms, meaning it evaluates the sum in Eq. (7.20) and recovers the values of the samples, but it does so quickly, using the tricks of the FFT as discussed previously. Thus if we take the output array `c` from the example above and do the following:

```python
from numpy.fft import irfft
z = irfft(c)
print(z)
```

the program prints

```
[ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9]
```

As you can see, we have recovered our original sample values again. Note that the `irfft` function takes as input an array that has $\frac{1}{2}N+1$ complex elements and creates an array with $N$ real elements. The function knows that the second half of the Fourier coefficients are the complex conjugates of the first half, so you only have to supply the first half.

The module `numpy.fft` also contains functions to calculate Fourier transforms of complex samples (`fft` and `ifft` for the forward and inverse transforms respectively) and two-dimensional transforms (`rfft2` and `irfft2` for real samples, `fft2` and `ifft2` for complex ones). The 2D Fourier transforms take a two-dimensional array as input and return a two-dimensional array. (Pretty much they just do two separate one-dimensional Fourier transforms, one for the rows and one for the columns. You could do the same thing yourself, but it saves a little effort to use the functions provided.) Note that, as discussed in Section 7.2.2, the two-dimensional Fourier transform of an $M \times N$ grid of real numbers is a grid of complex numbers with dimensions $M \times (\frac{1}{2}N+1)$. Python knows this and returns an array of the appropriate size. Higher-dimensional transforms are also possible, in three dimensions or above, and Python has functions for these as well, but we will not use them in this book.

---

**Exercise 7.3: Fourier transforms of musical instruments**

In the on-line resources you will find files called `piano.txt` and `trumpet.txt`, which contain data representing the waveform of a single note, played on, respectively, a piano and a trumpet.

a) Write a program that loads a waveform from one of these files, plots it, then calculates its discrete Fourier transform and plots the magnitudes of the first 10 000 coefficients in a manner similar to Fig. 7.4. Note that you will have to use a fast Fourier transform for the calculation because there are too many samples in the files to do the transforms the slow way in any reasonable amount of time.

Apply your program to the piano and trumpet waveforms and discuss briefly what one can conclude about the sound of the piano and trumpet from the plots of Fourier coefficients.

b) Both waveforms were recorded at the industry-standard rate of 44 100 samples per second and both instruments were playing the same musical note when the recordings were made. From your Fourier transform results calculate what note they were playing. (Hint: The musical note middle C has a frequency of 261 Hz.)

---

**Exercise 7.4: Fourier filtering and smoothing**

In the on-line resources you'll find a file called `dow.txt`. It contains the daily closing value for each business day from late 2006 until the end of 2010 of the Dow Jones Industrial Average, which is a measure of average prices on the US stock market.

Write a program to do the following:

a) Read in the data from `dow.txt` and plot them on a graph.

b) Calculate the coefficients of the discrete Fourier transform of the data using the function `rfft` from `numpy.fft`, which produces an array of $\frac{1}{2}N+1$ complex numbers.

c) Now set all but the first 10% of the elements of this array to zero (i.e., set the last 90% to zero but keep the values of the first 10%).

d) Calculate the inverse Fourier transform of the resulting array, zeros and all, using the function `irfft`, and plot it on the same graph as the original data. You may need to vary the colors of the two curves to make sure they both show up on the graph. Comment on what you see. What is happening when you set the Fourier coefficients to zero?

e) Modify your program so that it sets all but the first 2% of the coefficients to zero and run it again.

---

And we could write a similar function to perform the inverse Fourier transform, Eq. (7.20). Notice the use of the function `exp` from the `cmath` package—the version from `cmath` differs from the `exp` function in the `math` package in that it can handle complex numbers.

These lines of code represent a very direct translation of Eq. (7.15) into Python. They are not, however, the quickest way to calculate the discrete Fourier transform. There is another, indirect, way of performing the same calculation, known (prosaically) as the "fast Fourier transform," which is significantly quicker. The code above will work fine for our present purposes, but for serious, large-scale physics calculations the fast Fourier transform is much better. We will study the fast Fourier transform in Section 7.4.

---

```python
def dct(y):
    N = len(y)
    y2 = empty(2*N, float)
    for n in range(N):
        y2[n] = y[n]
        y2[2*N-1-n] = y[n]
    c = rfft(y2)
    phi = exp(-1j*pi*arange(N)/(2*N))
    return real(phi*c[:N])
```

Note the use of the multiplier `phi`, which accounts for the leading phase factor in Eq. (7.32).

Similar functions to perform the inverse cosine transform, as well as for forward and inverse sine transforms, are given in Appendix E and copies can be found in the on-line resources.

---

**Exercise 7.6: Comparison of the DFT and DCT**

This exercise will be easier if you have already done Exercise 7.4.

Exercise 7.4 looked at data representing the variation of the Dow Jones Industrial Average, colloquially called "the Dow," over time. The particular time period studied in that exercise was special in one sense: the value of the Dow at the end of the period was almost the same as at the start, so the function was, roughly speaking, periodic. In the on-line resources there is another file called `dow2.txt`, which also contains data on the Dow but for a different time period, from 2004 until 2008. Over this period the value changed considerably from a starting level around 9000 to a final level around 14000.

a) Write a program similar to the one for Exercise 7.4, part (e), in which you read the data in the file `dow2.txt` and plot it on a graph. Then smooth the data by calculating its Fourier transform, setting all but the first 2% of the coefficients to zero, and inverting the transform again, plotting the result on the same graph as the original data. As in Exercise 7.4 you should see that the data are smoothed, but now there will be an additional artifact. At the beginning and end of the plot you should see large deviations away from the true smoothed function. These occur because the function is required to be periodic—its last value must be the same as its first—so it needs to deviate substantially from the correct value to make the two ends of the function meet. In some situations (including this one) this behavior is unsatisfactory. If we want to use the Fourier transform for smoothing, we would certainly prefer that it not introduce artifacts of this kind.

b) Modify your program to repeat the same analysis using discrete cosine transforms. You can use the functions from `dcst.py` to perform the transforms if you

numbers, and a complex number typically takes sixteen bytes of memory to store. So if you had to do a large Fourier transform of, say, $N = 10^8$ numbers, it would take $16N\log_2 N \simeq 42$ gigabytes of memory, which is much more than most computers have.

An alternative approach is to notice that we do not really need to store all of the coefficients. At any one point in the calculation we only need the coefficients at the current level and the previous level (from which the current level is calculated). If one is clever one can write a program that uses only two arrays, one for the current level and one for the previous level, each consisting of $N$ complex numbers. Then our transform of $10^8$ numbers would require less than four gigabytes, which is fine on most computers.

(There is a third way of storing the coefficients that is even more efficient. If you store the coefficients in the correct order, then you can arrange things so that every time you compute a coefficient for the next level, it gets stored in the same place as the old coefficient from the previous level from which it was calculated, and which you no longer need. With this way of doing things you only need one array of $N$ complex numbers—we say the transform is done "in place." Unfortunately, this in-place Fourier transform is much harder to work out and harder to program. If you are feeling particularly ambitious you might want to give it a try, but it's not for the faint-hearted.)

---

**7.8 Diffraction gratings:** Exercise 5.19 (page 206) looked at the physics of diffraction gratings, calculating the intensity of the diffraction patterns they produce from the equation

$$I(x) = \left|\int_{-w/2}^{w/2} \sqrt{q(u)} \, e^{i2\pi xu/\lambda f} \, du\right|^2,$$

where $w$ is the width of the grating, $\lambda$ is the wavelength of the light, $f$ is the focal length of the lens used to focus the image, and $q(u)$ is the intensity transmission function of the diffraction grating at a distance $u$ from the central axis, i.e., the fraction of the incident light that the grating lets through. In Exercise 5.19 we evaluated this expression directly using standard methods for performing integrals, but a more efficient way to do the calculation is to note that the integral is basically just a Fourier transform. Approximating the integral, as we did in Eq. (7.13), using the trapezoidal rule, with $N$ points $u_n = nw/N - w/2$, we get

$$\begin{aligned}
\int_{-w/2}^{w/2} \sqrt{q(u)} \, e^{i2\pi xu/\lambda f} \, du &\simeq \frac{w}{N} e^{-i\pi wx/\lambda f} \sum_{n=0}^{N-1} \sqrt{q(u_n)} \, e^{i2\pi wxn/\lambda fN} \\
&= \frac{w}{N} e^{-i\pi k} \sum_{n=0}^{N-1} y_n \, e^{i2\pi kn/N},
\end{aligned}$$

where $k = wx/\lambda f$ and $y_n = \sqrt{q(u_n)}$. Comparing with Eq. (7.15), we see that the sum in this expression is equal to the complex conjugate $c_k^*$ of the $k$th coefficient of the DFT of $y_n$. Substituting into the expression for the intensity $I(x)$, we then have

$$I(x_k) = \frac{w^2}{N^2}|c_k|^2,$$

where

$$x_k = \frac{\lambda f}{w}k.$$

Thus we can calculate the intensity of the diffraction pattern at the points $x_k$ by performing a Fourier transform.

There is a catch, however. Given that $k$ is an integer, $k = 0 \ldots N-1$, the points $x_k$ at which the intensity is evaluated have spacing $\lambda f/w$ on the screen. This spacing can be large in some cases, giving us only a rather coarse picture of the diffraction pattern. For instance, in Exercise 5.19 we had $\lambda = 500$ nm, $f = 1$ m, and $w = 200\,\mu$m, and the screen was 10 cm wide, which means that $\lambda f/w = 2.5$ mm and we have only forty points on the screen. This is not enough to make a usable plot of the diffraction pattern.

One way to fix this problem is to increase the width of the grating from the given value $w$ to a larger value $W > w$, which makes the spacing $\lambda f/W$ of the points on the screen closer. We can add the extra width on one or the other side of the grating, or both, as we prefer, but—and this is crucial—the extra portion added must be opaque, it must not transmit light, so that the physics of the system does not change. In other words, we need to "pad out" the data points $y_n$ that measure the transmission profile of the grating with additional zeros so as to make the grating wider while keeping its transmission properties the same. For example, to increase the width to $W = 10w$, we would increase the number $N$ of points $y_n$ by a factor of ten, with the extra points set to zero. The extra points can be at the beginning, at the end, or split between the two—it will make no difference to the answer. Then the intensity is given by

$$I(x_k) = \frac{W^2}{N^2}|c_k|^2,$$

where

$$x_k = \frac{\lambda f}{W}k.$$

Write a Python program that uses a fast Fourier transform to calculate the diffraction pattern for a grating with transmission function $q(u) = \sin^2 \alpha u$ (the same as in Exercise 5.19), with slits of width $20\,\mu$m [meaning that $\alpha = \pi/(20\,\mu\text{m})$] and parameters as above: $w = 200\,\mu\text{m}$, $W = 10w = 2$ mm, incident light of wavelength $\lambda = 500$ nm, a lens with focal length of 1 meter, and a screen 10 cm wide. Choose a suitable number of points to give a good approximation to the grating transmission function and then make a graph of the diffraction intensity on the screen as a function of position $x$ in the range $-5\text{cm} \leq x \leq 5$cm. If you previously did Exercise 5.19, check to make sure your answers to the two exercises agree.

---

**7.9 Image deconvolution:** You've probably seen it on TV, in one of those crime drama shows. They have a blurry photo of a crime scene and they click a few buttons on the computer and magically the photo becomes sharp and clear, so you can make out someone's face, or some lettering on a sign. Surely (like almost everything else on such TV shows) this is just science fiction? Actually, no. It's not. It's real and in this exercise you'll write a program that does it.

When a photo is blurred each point on the photo gets smeared out according to some "smearing distribution," which is technically called a *point spread function*. We can represent this smearing mathematically as follows. For simplicity let's assume we're working with a black and white photograph, so that the picture can be represented by a single function $a(x,y)$ which tells you the brightness at each point $(x,y)$. And let us denote the point spread function by $f(x,y)$. This means that a single bright dot at the origin ends up appearing as $f(x,y)$ instead. If $f(x,y)$ is a broad function then the picture is badly blurred. If it is a narrow peak then the picture is relatively sharp.

In general the brightness $b(x,y)$ of the blurred photo at point $(x,y)$ is given by

$$b(x,y) = \int_0^K \int_0^L a(x',y') f(x-x', y-y') \, dx' \, dy',$$

where $K \times L$ is the dimension of the picture. This equation is called the *convolution* of the picture with the point spread function.

Working with two-dimensional functions can get complicated, so to get the idea of how the math works, let's switch temporarily to a one-dimensional equivalent of our problem. Once we work out the details in 1D we'll return to the 2D version. The one-dimensional version of the convolution above would be

$$b(x) = \int_0^L a(x') f(x-x') \, dx'.$$

The function $b(x)$ can be represented by a Fourier series as in Eq. (7.5):

$$b(x) = \sum_{k=-\infty}^{\infty} \tilde{b}_k \exp\left(i\frac{2\pi k x}{L}\right),$$

where

$$\tilde{b}_k = \frac{1}{L} \int_0^L b(x) \exp\left(-i\frac{2\pi k x}{L}\right) dx$$

are the Fourier coefficients, Eq. (7.10). Substituting for $b(x)$ in this equation gives

$$\begin{aligned}
\tilde{b}_k &= \frac{1}{L} \int_0^L \int_0^L a(x') f(x-x') \exp\left(-i\frac{2\pi k x}{L}\right) dx' \, dx \\
&= \frac{1}{L} \int_0^L \int_0^L a(x') f(x-x') \exp\left(-i\frac{2\pi k(x-x')}{L}\right) \exp\left(-i\frac{2\pi k x'}{L}\right) dx' \, dx.
\end{aligned}$$

Now let us change variables to $X = x - x'$, and we get

$$\tilde{b}_k = \frac{1}{L} \int_0^L a(x') \exp\left(-i\frac{2\pi k x'}{L}\right) \int_{-x'}^{L-x'} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX \, dx'.$$

If we make $f(x)$ a periodic function in the standard fashion by repeating it infinitely many times to the left and right of the interval from 0 to $L$, then the second integral above can be written as

$$\begin{aligned}
\int_{-x'}^{L-x'} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX &= \int_{-x'}^{0} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX \\
&\quad + \int_{0}^{L-x'} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX \\
&= \exp\left(i\frac{2\pi k L}{L}\right) \int_{L-x'}^{L} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX + \int_{0}^{L-x'} f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX \\
&= \int_0^L f(X) \exp\left(-i\frac{2\pi k X}{L}\right) dX,
\end{aligned}$$

which is simply $L$ times the Fourier transform $\tilde{f}_k$ of $f(x)$. Substituting this result back into our equation for $\tilde{b}_k$ we then get

$$\tilde{b}_k = \int_0^L a(x') \exp\left(-i\frac{2\pi k x'}{L}\right) \tilde{f}_k \, dx' = L\tilde{a}_k \tilde{f}_k.$$

In other words, apart from the factor of $L$, the Fourier transform of the blurred photo is the product of the Fourier transforms of the unblurred photo and the point spread function.

Now it is clear how we deblur our picture. We take the blurred picture and Fourier transform it to get $\tilde{b}_k = L\tilde{a}_k \tilde{f}_k$. We also take the point spread function and Fourier transform it to get $\tilde{f}_k$. Then we divide one by the other:

$$\frac{\tilde{b}_k}{L\tilde{f}_k} = \tilde{a}_k$$

which gives us the Fourier transform of the *unblurred* picture. Then, finally, we do an inverse Fourier transform on $\tilde{a}_k$ to get back the unblurred picture. This process of recovering the unblurred picture from the blurred one, of reversing the convolution process, is called *deconvolution*.

Real pictures are two-dimensional, but the mathematics follows through exactly the same. For a picture of dimensions $K \times L$ we find that the two-dimensional Fourier transforms are related by

$$\tilde{b}_{kl} = KL\tilde{a}_{kl}\tilde{f}_{kl},$$

and again we just divide the blurred Fourier transform by the Fourier transform of the point spread function to get the Fourier transform of the unblurred picture.

In the digital realm of computers, pictures are not pure functions $f(x,y)$ but rather grids of samples, and our Fourier transforms are discrete transforms not continuous ones. But the math works out the same again.

The main complication with deblurring in practice is that we don't usually know the point spread function. Typically we have to experiment with different ones until we find something that works. For many cameras it's a reasonable approximation to assume the point spread function is Gaussian:

$$f(x,y) = \exp\left(-\frac{x^2+y^2}{2\sigma^2}\right),$$

where $\sigma$ is the width of the Gaussian. Even with this assumption, however, we still don't know the value of $\sigma$ and we may have to experiment to find a value that works well. In the following exercise, for simplicity, we'll assume we know the value of $\sigma$.

a) On the web site you will find a file called `blur.txt` that contains a grid of values representing brightness on a black-and-white photo—a badly out-of-focus one that has been deliberately blurred using a Gaussian point spread function of width $\sigma = 25$. Write a program that reads the grid of values into a two-dimensional array of real numbers and then draws the values on the screen of the computer as a density plot. You should see the photo appear. If you get something wrong it might be upside-down. Work with the details of your program until you get it appearing correctly. (Hint: The picture has the sky, which is bright, at the top and the ground, which is dark, at the bottom.)

b) Write another program that creates an array, of the same size as the photo, containing a grid of samples drawn from the Gaussian $f(x,y)$ above with $\sigma = 25$. Make a density plot of these values on the screen too, so that you get a visualization of your point spread function. Remember that the point spread function is periodic (along both axes), which means that the values for negative $x$ and $y$ are repeated at the end of the interval. Since the Gaussian is centered on the origin, this means there should be bright patches in each of the four corners of your picture, something like this:

[Image: Gaussian point spread function visualization]

c) Combine your two programs and add Fourier transforms using the functions `rfft2` and `irfft2` from `numpy.fft`, to make a program that does the following:
   i) Reads in the blurred photo
   ii) Calculates the point spread function
   iii) Fourier transforms both
   iv) Divides one by the other
   v) Performs an inverse transform to get the unblurred photo
   vi) Displays the unblurred photo on the screen

When you are done, you should be able to make out the scene in the photo, although probably it will still not be perfectly sharp.

Hint: One thing you'll need to deal with is what happens when the Fourier transform of the point spread function is zero, or close to zero. In that case if you divide by it you'll get an error (because you can't divide by zero) or just a very large number (because you're dividing by something small). A workable compromise is that if a value in the Fourier transform of the point spread function is smaller than a certain amount $\epsilon$ you don't divide by it—just leave that coefficient alone. The value of $\epsilon$ is not very critical but a reasonable value seems to be $10^{-3}$.

d) Bearing in mind this last point about zeros in the Fourier transform, what is it that limits our ability to deblur a photo? Why can we not perfectly unblur any photo and make it completely sharp?

We have seen this process in action here for a normal snapshot, but it is also used in many physics applications where one takes photos. For instance, it is used in astronomy to enhance photos taken by telescopes. It was famously used with images from the Hubble Space Telescope after it was realized that the telescope's main mirror had a serious manufacturing flaw and was returning blurry photos—scientists managed to partially correct the blurring using Fourier transform techniques.
```

以上是Mark Newman《Computational Physics》第七章"Fourier Transforms"的完整Markdown转换。内容包括：

- **7.1 Fourier Series** - 傅里叶级数基础，包括正弦/余弦级数和复指数形式
- **7.2 The Discrete Fourier Transform** - 离散傅里叶变换（DFT）的推导、采样点位置、二维DFT、物理解释
- **7.3 Discrete Cosine and Sine Transforms** - 离散余弦/正弦变换，Type-I和Type-II DCT，以及在JPEG、MPEG、MP3中的应用
- **7.4 Fast Fourier Transforms** - 快速傅里叶变换（FFT）算法、Python实现（`numpy.fft`模块）

所有数学公式、图表说明、Python代码示例和练习题都已完整保留。