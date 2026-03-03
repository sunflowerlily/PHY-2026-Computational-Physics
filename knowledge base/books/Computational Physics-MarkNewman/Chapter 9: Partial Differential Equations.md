
# Chapter 9: Partial Differential Equations

Some of the most challenging problems in computational physics—and also some of the most interesting—involve the solution of partial differential equations, such as the wave equation, the diffusion equation, the Laplace and Poisson equations, Maxwell's equations, and the Schrödinger equation. Although the basic numerical methods for solving these problems are straightforward, they are also computationally demanding, so a lot of effort has been invested in finding ways to arrive at solutions quickly.

As with the ordinary differential equations of Chapter 8, problems involving partial differential equations can be divided into initial value problems and boundary value problems. By contrast with the situation in Chapter 8, however, boundary value problems for partial differential equations are usually simpler to solve than initial value problems, so we'll study them first. With boundary value problems we have a partial differential equation describing the behavior of a variable in a space and we are given some constraint on the variable around the boundary of the space. The goal is to solve for the values inside the rest of the space. A classic example of a boundary value problem is the problem of solving for the electric potential in electrostatics. Suppose, for instance, we have a box as shown in Fig. 9.1. The box is empty and has one wall at voltage $V$ and the others at voltage zero. Our goal is to determine the value of the electrostatic potential at points within the box. Problems like this arise in electronics and in many physics experiments.

The electrostatic potential $\phi$ is related to the vector electric field $\mathbf{E}$ by $\mathbf{E} = -\nabla\phi$. And Maxwell's equations tell us that $\nabla \cdot \mathbf{E} = 0$ in the absence of any electric charges, so $\nabla \cdot \nabla\phi = 0$ or

$$\nabla^2\phi = 0, \tag{9.1}$$

which is **Laplace's equation**. If we write out the Laplacian operator $\nabla^2$ in full, the equation takes the form

$$\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} + \frac{\partial^2\phi}{\partial z^2} = 0. \tag{9.2}$$

The challenge is to solve this equation inside the box, subject to the boundary conditions that $\phi = V$ on the top wall and $\phi = 0$ on the other walls.

The other broad class of partial differential equation problems are the initial value problems. In an initial value problem, the field or other variable of interest is not only subject to boundary conditions, but is also time varying. Typically we are given the initial state of the field at some time $t = 0$, in a manner similar to the initial conditions we used for ordinary differential equations in Chapter 8, and we want to calculate how the field evolves over time thereafter, subject to that initial condition plus the boundary conditions. An example of an initial value problem would be the wave equation for the vibration of a string, like a string in a musical instrument, for which there are boundary conditions (the string is usually pinned and stationary at its ends) but also an initial condition (the string is plucked or struck at $t = 0$) and the challenge is to solve for the motion of the string.

In the following sections of this chapter we will look at techniques for solving both boundary value problems and initial value problems.

## 9.1 Boundary Value Problems and the Relaxation Method

A fundamental technique for the solution of partial differential equations is the **method of finite differences**. Consider the electrostatics example of Fig. 9.1, whose solution involves solving Laplace's equation, Eq. (9.2), for the electric potential $\phi$, subject to the appropriate boundary conditions. To make the pictures manageable (and the programs easier) let's consider the problem in two-dimensional space, where Laplace's equation takes the simpler form

$$\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = 0. \tag{9.3}$$

Real problems are in three dimensions, of course, but the techniques for two and three dimensions are fundamentally the same; once we can do the two-dimensional version, the three-dimensional one is a straightforward generalization.

The method of finite differences involves dividing space into a grid of discrete points. Many kinds of grids are used, depending on the particular problem in hand, but in the simplest and commonest case we use a regular, square grid as shown in Fig. 9.2. Note that we put points on the boundaries of the space (where we already know the value of $\phi$) as well as in the interior (where we want to calculate the solution).

Suppose the spacing of the grid points is $a$ and consider a point at position $(x,y)$. As we saw in Section 5.10.5, second derivatives can be approximated using a finite difference formula, just as first derivatives can, and, as we saw in Section 5.10.6, so can partial derivatives. Applying the results we learned in those sections (particularly Eq. (5.109) on page 197), we can write the second derivative of $\phi$ in the $x$-direction as

$$\frac{\partial^2\phi}{\partial x^2} = \frac{\phi(x+a,y) + \phi(x-a,y) - 2\phi(x,y)}{a^2}. \tag{9.4}$$

This formula gives us an expression for the second derivative in terms of the values $\phi(x,y)$, $\phi(x-a,y)$, and $\phi(x+a,y)$ at three adjacent points on our grid. Similarly the derivative in the $y$-direction is

$$\frac{\partial^2\phi}{\partial y^2} = \frac{\phi(x,y+a) + \phi(x,y-a) - 2\phi(x,y)}{a^2}, \tag{9.5}$$

and the Laplacian operator in two dimensions is:

$$\frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} = \frac{\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a) - 4\phi(x,y)}{a^2}. \tag{9.6}$$

In other words, we add together the values of $\phi$ at all the grid points immediately adjacent to $(x,y)$ and subtract four times the value at $(x,y)$, then divide by $a^2$. Sometimes this rule is represented visually by a diagram like this:

```
    +1
    |
+1--4--+1
    |
    +1
```

Combining Eqs. (9.3) and (9.6) and canceling the factor of $a^2$, our Laplace equation now takes the form

$$\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a) - 4\phi(x,y) = 0. \tag{9.7}$$

We have one equation like this for every grid point $(x,y)$ and the solution to the entire set of equations gives us the value of $\phi(x,y)$ at every grid point. In other words, we have turned our problem from the solution of a partial differential equation into the solution of a set of linear simultaneous equations.

We studied the solution of simultaneous equations in Chapter 6, where we saw that sets of equations like (9.7) can be solved by a variety of methods, such as Gaussian elimination (Section 6.1.1) or LU decomposition (Section 6.1.4). In the present case, however, because the equations are particularly simple, there is a quicker way to solve them: we can use the relaxation method of Section 6.3.1. We introduced the relaxation method as a method for the solution of nonlinear equations, but there's no reason in principle why it cannot be applied to linear ones as well, and in the present case it's actually a good choice—better than Gaussian elimination, for instance, because it involves less work, both for the programmer and for the computer.

To make use of the relaxation method, we rearrange Eq. (9.7) to read

$$\phi(x,y) = \frac{1}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right], \tag{9.8}$$

which tells us that $\phi(x,y)$ is simply the average of the values on the immediately adjacent points of the grid. Now we fix $\phi(x,y)$ at the boundaries of the system to have the value that we know it must have, which for the current electrostatic problem means $\phi = V$ on the top wall of the box and $\phi = 0$ on the other three walls. Then we guess some initial values for $\phi(x,y)$ at the grid points in the interior of the box. The guesses don't have to be good ones. For instance, we could just guess that the values are all zero, which is obviously wrong, but it doesn't much matter. Now we apply Eq. (9.8) to calculate new values $\phi'$ on all the grid points in the interior space. That is, we calculate

$$\phi'(x,y) = \frac{1}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right], \tag{9.9}$$

Then we take these values and feed them back in on the right-hand side again to calculate another new set of values, and so on until $\phi$ settles down to a fixed value. If it does that means that we have found a solution to Eq. (9.8).

This approach for solving the Laplace equation is called the **Jacobi method**. Like all relaxation methods, it does require that the iteration process actually converge to a solution, rather than diverging; as we saw in Section 6.3.1, this is not always guaranteed for relaxation methods. Situations where the calculation diverges are said to be **numerically unstable**, and there are some relaxation methods for partial differential equations that can be numerically unstable. But it turns out that the Jacobi method is not one of them. It can be proved that the Jacobi method is always stable and so always gives a solution.

As described in Section 6.3.1, there are a couple of different ways to decide when to stop the iteration process for the relaxation method, of which the simplest is just to wait until the values of $\phi$ stop changing, at least within whatever limits of accuracy you have set for yourself. Thus, having calculated $\phi'(x,y)$ from Eq. (9.9), you could calculate the change $\phi'(x,y) - \phi(x,y)$ and when the magnitude of this change is smaller than your target accuracy on every grid point, the calculation ends.

### Example 9.1: Solution of Laplace's Equation

Let us compute a solution to the two-dimensional electrostatics problem of Fig. 9.1 using the Jacobi method, for the case where the box is 1 m along each side, $V = 1$ volt, and the grid spacing $a = 1$ cm, so that there are 100 grid points on a side, or 101 if we count the points at both the beginning and the end. Here's a program to calculate the solution and make a density plot of the result:

```python
from numpy import empty,zeros,max
from pylab import imshow,gray,show

# Constants
M = 100         # Grid squares on a side
V = 1.0         # Voltage at top wall
target = 1e-6   # Target accuracy

# Create arrays to hold potential values
phi = zeros([M+1,M+1],float)
phi[0,:] = V
phiprime = empty([M+1,M+1],float)

# Main loop
delta = 1.0
while delta>target:
    
    # Calculate new values of the potential
    for i in range(M+1):
        for j in range(M+1):
            if i==0 or i==M or j==0 or j==M:
                phiprime[i,j] = phi[i,j]
            else:
                phiprime[i,j] = (phi[i+1,j] + phi[i-1,j] \
                                + phi[i,j+1] + phi[i,j-1])/4
    
    # Calculate maximum difference from old values
    delta = max(abs(phi-phiprime))
    
    # Swap the two arrays around
    phi,phiprime = phiprime,phi

# Make a plot
imshow(phi)
gray()
show()
```

A couple of things are worth noting in this program. First, observe that neither the system size $L$ nor the grid spacing $a$ ever enters into the calculation. We perform the whole calculation in terms of the indices `i` and `j` of the grid points, integers that run from 0 to 100 and which we can conveniently use as the indices of the arrays `phi` and `phiprime` that hold the values of the electric potential. Notice also how when we calculate the new values of $\phi$, which are stored in the array `phiprime`, we run through each point `i,j` and first check whether it is on the boundary of the box. If it is, then the new value $\phi'$ of the electric potential is equal to the old one $\phi$—the electric potential never changes on the boundaries. If, on the other hand, the point is in the interior of the box then we calculate a new value using Eq. (9.9). Finally, notice the line `"phi,phiprime = phiprime,phi"`, which swaps around the two arrays `phi` and `phiprime`, so that the new values of electric potential get used as the old values the next time around the loop.

Figure 9.3 shows the density plot that results from running the program. As we can see, there is a region of high electric potential around the top wall of the box, as we would expect, and low potential around the other three walls.

It's important to appreciate that, since we have approximated our derivatives with finite differences, the Jacobi method is only going to give us an approximate solution to our problem. Even if we make the target accuracy for the iteration very small, the solution will still contain relatively large errors because the finite difference approximation to the second derivative is not very accurate. One can use higher-order derivative approximations, of the kind we studied in Section 5.10.4, to improve the accuracy of the calculation—the generalization of the method is straightforward—or one can just increase the number of grid points, making them closer together, which improves the accuracy of the current approximation. Increasing the number of grid points, however, will also make the program run more slowly.

Another point to notice is that the calculation gives us the value of $\phi$ only at the grid points and not elsewhere. If we need values in between the grid points we could calculate them using an interpolation scheme such as the linear interpolation of Section 5.11, although this introduces a further approximation. This approximation can also be improved by making the grid size smaller, though again the resulting program will run more slowly.

A more technical point to be aware of is that the boundaries around our space may not always be simple and square the way they are in the exercise above. We may have diagonal surfaces or round surfaces or holes cut out of the space. Such things can make it difficult to divide up the space with a square grid because the grid points don't fall exactly on the boundaries. We can always approximate an inconvenient shape by moving the boundaries to the grid points closest to them, applying the boundary conditions at these points rather than exactly on the true boundaries. This, however, introduces more approximations into the calculation. There exist more complicated finite difference methods that get around these issues by using grids whose spacing varies from place to place or that are not square but instead, for instance, triangular. These methods can be useful for difficult geometries, but they are substantially more complex to program.

### Example 9.2: A More Complicated Electrostatics Problem

Two square charges are placed inside a two-dimensional box. The potential is zero on the walls and the charges have charge density $+1$ Cm$^{-2}$ and $-1$ Cm$^{-2}$.

The charges are each 20 cm on a side and 20 cm from the walls of the box and have charge density $\pm 1$ Cm$^{-2}$.

To solve this problem using the relaxation method we make use of Eq. (9.6) to rewrite Eq. (9.10) as

$$\frac{\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a) - 4\phi(x,y)}{a^2} = -\frac{\rho(x,y)}{\epsilon_0}. \tag{9.11}$$

Now we rearrange this expression for $\phi(x,y)$ and get

$$\phi(x,y) = \frac{1}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right] + \frac{a^2}{4\epsilon_0}\rho(x,y). \tag{9.12}$$

This is similar to Eq. (9.8) for the Laplace equation, but with the addition of the term in $\rho(x,y)$. Note that the spacing $a$ of the grid points no longer drops out of the calculation. We can, however, still solve the problem as we did before by choosing initial values for $\phi(x,y)$ on a grid and then iterating to convergence. The program is only slightly modified from the one for the Laplace equation on page 409—Exercise 9.1 below gives you the opportunity to work out the details yourself. Figure 9.5 shows the solution you should get for the electrostatic potential.

**Exercise 9.1:** Write a program, or modify the one from Example 9.1, to solve Poisson's equation for the system described in Example 9.2. Work in units where $\epsilon_0 = 1$ and continue the iteration until your solution for the electric potential changes by less than $10^{-6}$ V per step at every grid point.

## 9.2 Faster Methods for Boundary Value Problems

The Jacobi method gives good answers, but it has a serious shortcoming: it's slow. It takes quite a while to settle down to the final solution. To be fair this is partly just because we're solving a very difficult problem. The program of Example 9.1 is effectively solving 10 000 simultaneous equations for 10 000 unknowns, one for every point on the $100 \times 100$ grid, which is no mean feat. Still, the calculation that produced Fig. 9.3 took about ten minutes, and bigger calculations on larger lattices could take a very long time indeed. If we could find a faster method of solution, it would certainly be a good thing. In fact, it turns out that with two relatively simple modifications we can make the Jacobi method much faster.

### 9.2.1 Overrelaxation

On each iteration of the Jacobi method the values of $\phi$ on all the grid points converge a little closer to their final values. One way to make this convergence faster is on each step to "overshoot" the new value a little. For instance, suppose on a particular grid point the value goes from 0.1 to 0.3 on one iteration, and eventually converges to 0.5 if we wait long enough. Then we could observe those values 0.1 and 0.3 and tell ourselves, "Instead of changing to 0.3 on this step, let's overshoot and go to, say, 0.4." In this case, doing so will get us closer to the final value of 0.5. This method is called **overrelaxation**. In detail it works like this.

Consider again the solution of Laplace's equation, as in Example 9.1, and suppose at some point in the operation of our program we have a set of values $\phi(x,y)$ on our grid points and at the next iteration we have a new set $\phi'(x,y)$ calculated from Eq. (9.9). Then the new set can be written in terms of the old as

$$\phi'(x,y) = \phi(x,y) + \Delta\phi(x,y), \tag{9.13}$$

where $\Delta\phi(x,y)$ is the change in $\phi$ on this step, given by $\Delta\phi(x,y) = \phi'(x,y) - \phi(x,y)$. Now we define a set of overrelaxed values $\phi_\omega(x,y)$ by

$$\phi_\omega(x,y) = \phi(x,y) + (1+\omega)\Delta\phi(x,y), \tag{9.14}$$

where $\omega > 0$. In other words we change each $\phi(x,y)$ by a little more than we normally would, the exact amount being controlled by the parameter $\omega$. Substituting $\Delta\phi(x,y) = \phi'(x,y) - \phi(x,y)$ into Eq. (9.14) gives

$$\begin{aligned}
\phi_\omega(x,y) &= \phi(x,y) + (1+\omega)\left[\phi'(x,y) - \phi(x,y)\right] \\
&= (1+\omega)\phi'(x,y) - \omega\phi(x,y) \\
&= \frac{1+\omega}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right] - \omega\phi(x,y),
\end{aligned} \tag{9.15}$$

where we have used Eq. (9.9) for $\phi'(x,y)$.

The overrelaxation method involves using this equation instead of Eq. (9.9) to calculate new values of $\phi$ on each step, but in other respects is the same as the Jacobi method. In order to use the equation we must choose a value for the parameter $\omega$. We discuss in a moment how this is done.

### 9.2.2 The Gauss-Seidel Method

A second trick for speeding up the Jacobi method is as follows. In our program to solve Laplace's equation in Example 9.1 we calculated the new values $\phi'(x,y)$ of the potential at each grid point one by one, working along the rows of the grid in turn, so that when we come to each new point we have already calculated new values at two of the neighbors of that point, though not at the other two. Assuming the new values are better than the old ones, i.e., closer to the true solution we are searching for, it makes sense to use these better values to calculate $\phi'(x,y)$ rather than using the old values at those grid points. If we do this, we get a variant of the Jacobi method called the **Gauss-Seidel method**. In the Gauss-Seidel method we never use the old values of $\phi(x,y)$ if we have new and better ones for the same grid points. Among other things, this means that we can throw away the old value for any grid square as soon as we calculate the new one. A simple way of doing this in practice is to store the new values in the same array as the old ones, overwriting the old ones in the process. The Gauss-Seidel method can be written (in a notation commonly used in computer science) as

$$\phi(x,y) \leftarrow \frac{1}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right], \tag{9.16}$$

meaning that we calculate the value on the right-hand side and use it to replace the value on the left. This technique has the nice feature that we only need one array to store the values of $\phi(x,y)$, and not two as in the traditional Jacobi method.

We can also combine the Gauss-Seidel method with the overrelaxation method of Section 9.2.1 to get a method that is faster than either, which we would write thus:

$$\phi(x,y) \leftarrow \frac{1+\omega}{4}\left[\phi(x+a,y) + \phi(x-a,y) + \phi(x,y+a) + \phi(x,y-a)\right] - \omega\phi(x,y). \tag{9.17}$$

In fact most of the speed-up in this combined overrelaxation/Gauss-Seidel method comes from the overrelaxation and not from Gauss and Seidel, so you might think we could just forget about Gauss-Seidel. There are, however, two reasons not to do this. First, the Gauss-Seidel method is not just faster, but also uses only one array instead of two, so it uses less memory. Given that it is faster *and* uses less memory, there is no reason to use the Jacobi method in most cases. Second, and more importantly, it turns out that in fact the simple Jacobi overrelaxation method as we described it in Section 9.2.1 *does not work*. It is numerically unstable (at least on square grids), whereas the Gauss-Seidel version is stable. The reasons for the instability are subtle but suffice it to say that the Gauss-Seidel method is better in essentially all respects than the Jacobi method.

Before we can use the method described here, we need to choose a value for the overrelaxation parameter $\omega$. There is no general optimal value that gives the best performance of the method for all problems. The choice of value depends both on the specific equations we are solving and on the shape of the grid we use. However, there are some guidelines that can be helpful. First, larger values of $\omega$ in general give faster calculations, but only up to a point. And if we use too large a value the calculation can become numerically unstable. It has been proved that the method is in general stable for $\omega < 1$ but unstable otherwise, so we should confine ourselves to values less than one. Other than this, the best way to find a good value is usually by experimentation. For the solution of Laplace's equation using a square grid of points the best value, the value that gives the fastest solution, is somewhere in the vicinity of $\omega = 0.9$, or a little larger. A solution of the problem from Example 9.1 using $\omega = 0.9$ took the author's computer just 38 seconds—much better than the 10 minutes taken by the Jacobi method. Exercise 9.2 gives you an opportunity to develop a program of your own to do the calculation.

**Exercise 9.2:** Use the combined overrelaxation/Gauss-Seidel method to solve Laplace's equation for the two-dimensional problem in Example 9.1—a square box 1 m on each side, at voltage $V = 1$ volt along the top wall and zero volts along the other three. Use a grid of spacing $a = 1$ cm, so that there are 100 grid points along each wall, or 101 if you count the points at both ends. Continue the iteration of the method until the value of the electric potential changes by no more than $\delta = 10^{-6}$ V at any grid point on any step, then make a density plot of the final solution, similar to that shown in Fig. 9.3. Experiment with different values of $\omega$ to find which value gives the fastest solution. As mentioned above, you should find that a value around 0.9 does well. In general larger values cause the calculation to run faster, but if you choose too large a value the speed drops off and for values above 1 the calculation becomes unstable.

**Exercise 9.3:** Consider the following simple model of an electronic capacitor, consisting of two flat metal plates enclosed in a square metal box:

For simplicity let us model the system in two dimensions. Using any of the methods we have studied, write a program to calculate the electrostatic potential in the box on a grid of $100 \times 100$ points, where the walls of the box are at voltage zero and the two plates (which are of negligible thickness) are at voltages $\pm 1$ V as shown. Have your program calculate the value of the potential at each grid point to a precision of $10^{-6}$ volts and then make a density plot of the result.

*Hint:* Notice that the capacitor plates are at fixed *voltage*, not fixed charge, so this problem differs from the problem with the two charges in Exercise 9.1. In effect, the capacitor plates are part of the boundary condition in this case: they behave the same way as the walls of the box, with potentials that are fixed at a certain value and cannot change.

## 9.3 Initial Value Problems

In the first part of this chapter we looked at the solution of boundary value problems. The other main class of partial differential equation problems in physics is initial value problems, where we are told the starting conditions for a variable and our goal is to predict future variation as a function of time. A simple example of such a problem is the diffusion equation in one (spatial) dimension:

$$\frac{\partial\phi}{\partial t} = D\frac{\partial^2\phi}{\partial x^2}, \tag{9.18}$$

where $D$ is a diffusion coefficient. The diffusion equation is used to calculate the motion of diffusing gases and liquids, as well as the flow of heat in thermal conductors. (When used to study heat, it is sometimes called the **heat equation**.)

The variable $\phi(x,t)$ in Eq. (9.18) depends on both position $x$ and time $t$. So, like the two-dimensional Laplace equation that we solved in the previous section, this is a partial differential equation with two independent variables. You might imagine, therefore, that one could solve it the same way: create a grid of points—a "space-time grid" in this case, in which the two dimensions of space-time are divided into a discrete set of points—then write the derivatives in finite difference form and get a set of simultaneous equations that can be solved by a relaxation method (or any other suitable method).

Unfortunately, this approach doesn't work for initial value problems because we don't have boundary conditions all the way around the space. Typically we have boundary conditions in the spatial dimension or dimensions (e.g., the $x$ dimension in Eq. (9.18)), but in the time dimension we have instead an *initial* condition, meaning we are told where the value of $\phi$ starts but not where it ends. This means that the relaxation method breaks down because we don't know what value to use for $\phi$ at the time-like end of the grid. Instead of a relaxation method, therefore, we use a different approach for solving initial value problems, a **forward integration method**, as follows.

### 9.3.1 The FTCS Method

Consider the solution of the diffusion equation, Eq. (9.18). As with our earlier solution of Laplace's equation, we start by dividing the *spatial* dimension (or dimensions) into a grid of points. In the case of Eq. (9.18) there is only one spatial dimension, so the "grid" is actually just a line of points along the $x$-axis. We will use evenly spaced points, although unevenly spaced ones are sometimes used in special cases. Let the spacing of the points be $a$. Then the derivative on the right-hand side of (9.18) can be written, as previously, using Eq. (5.109):

$$\frac{\partial^2\phi}{\partial x^2} = \frac{\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)}{a^2}, \tag{9.19}$$

and so our diffusion equation, Eq. (9.18), becomes

$$\frac{\mathrm{d}\phi}{\mathrm{d}t} = \frac{D}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.20}$$

If we think of the value of $\phi$ at the different grid points as separate variables, we now have a set of simultaneous *ordinary* differential equations in those variables, equations of exactly the kind we studied in Chapter 8, which can be solved by the methods we already know about. The catch is that there can be a lot of equations to solve—hundreds, thousands, or even millions, depending on how fine a grid we use and how many spatial dimensions we have. A few thousand equations is quite feasible with modern computers; a few million is pushing the limits, unless you have a supercomputer.

The most common method for solving the differential equations in Eq. (9.20) is Euler's method, which we studied in Section 8.1.1. This may seem like a strange choice: we said in Chapter 8 that one never uses Euler's method because higher-order Runge-Kutta methods are not much harder to program and give better results. That's true here too, but the point to notice is that the approximation to the second derivative on the right-hand side of Eq. (9.20) is not very accurate—it introduces a second-order error as shown in Section 5.10.5. There is not much point expending a lot of effort to get a very accurate solution for the differential equation in $t$ if the inputs to that solution—the right-hand side of the equation—aren't accurate in the first place. Euler's method also has a second-order error and gives errors typically of comparable size to those coming from the second derivative, so there is little harm in using it in this case, and its relative simplicity gives it an advantage over the Runge-Kutta method.

Recall that Euler's method for solving a differential equation of the form

$$\frac{\mathrm{d}\phi}{\mathrm{d}t} = f(\phi,t), \tag{9.21}$$

is to Taylor expand $\phi(t)$ about time $t$ and write

$$\phi(t+h) \simeq \phi(t) + h\frac{\mathrm{d}\phi}{\mathrm{d}t} = \phi(t) + hf(\phi,t). \tag{9.22}$$

Applying the same approach to Eq. (9.20) gives us

$$\phi(x,t+h) = \phi(x,t) + h\frac{D}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.23}$$

If we know the value of $\phi$ at every grid point $x$ at some time $t$, then this equation tells us the value at every grid point at time $t+h$, a short interval later. Hence, by repeatedly using this equation at every grid point, we can derive the solution to our partial differential equation at a succession of time points a distance $h$ apart, in a manner similar the way we solved ordinary differential equations in Chapter 8. This is called the **forward-time centered-space method** for solving partial differential equations, or **FTCS** for short.

### Example 9.3: The Heat Equation

The flat base of a container made of 1 cm thick stainless steel is initially at a uniform temperature of 20° Celsius everywhere. The container is placed in a bath of cold water at 0°C and filled with hot water at 50°C:

Our goal is to calculate the temperature profile of the steel as a function of distance $x$ from the hot side to the cold side, and as a function of time. For simplicity let us treat the base of the container as being arbitrarily wide, so that its temperature profile is the same everywhere, and assume that neither the hot nor the cold water changes temperature appreciably.

Thermal conduction is governed by the diffusion equation (also called the heat equation in this context), so solving this problem is a matter of solving the one-dimensional diffusion equation for the temperature $T$:

$$\frac{\partial T}{\partial t} = D\frac{\partial^2 T}{\partial x^2}. \tag{9.24}$$

Let us divide the $x$-axis into 100 equal grid intervals, meaning that there will be 101 grid points in total, counting the first and last ones. The first and last points have fixed temperatures of 50° and 0°C, respectively, while the intermediate points are initially all at 20°C. We also need the heat diffusion coefficient for stainless steel, also called the **thermal diffusivity**, which is $D = 4.25 \times 10^{-6}$ m$^2$s$^{-1}$.

Here is a program to perform the calculation using the FTCS method and make a plot of the temperature profile at times $t = 0.01$ s, 0.1 s, 0.4 s, 1 s, and 10 s, all on the same graph:

```python
from numpy import empty
from pylab import plot,xlabel,ylabel,show

# Constants
L = 0.01        # Thickness of steel in meters
D = 4.25e-6     # Thermal diffusivity
N = 100         # Number of divisions in grid
a = L/N         # Grid spacing
h = 1e-4        # Time-step
epsilon = h/1000

Tlo = 0.0       # Low temperature in Celsius
Tmid = 20.0     # Intermediate temperature in Celsius
Thi = 50.0      # Hi temperature in Celsius

t1 = 0.01
t2 = 0.1
t3 = 0.4
t4 = 1.0
t5 = 10.0
tend = t5 + epsilon

# Create arrays
T = empty(N+1,float)
T[0] = Thi
T[N] = Tlo
T[1:N] = Tmid
Tp = empty(N+1,float)
Tp[0] = Thi
Tp[N] = Tlo

# Main loop
t = 0.0
c = h*D/(a*a)
while t<tend:
    
    # Calculate the new values of T
    for i in range(1,N):
        Tp[i] = T[i] + c*(T[i+1]+T[i-1]-2*T[i])
    T,Tp = Tp,T
    t += h
    
    # Make plots at the given times
    if abs(t-t1)<epsilon:
        plot(T)
    if abs(t-t2)<epsilon:
        plot(T)
    if abs(t-t3)<epsilon:
        plot(T)
    if abs(t-t4)<epsilon:
        plot(T)
    if abs(t-t5)<epsilon:
        plot(T)

xlabel("x")
ylabel("T")
show()
```

This is a straightforward use of Eq. (9.23). The only slightly subtle point arises in making the plots. We need to make a plot when the time variable `t` is equal to any of the times 0.01, 0.1, 0.4, and so forth, which are called `t1`, `t2`, `t3` in the program. But because the time is a floating-point variable it is subject to numerical rounding error, as discussed in Section 4.2, so we cannot simply write "`if t==t1`". As we said in Section 4.2, one should never compare two floats for equality because numerical error may make them different in practice even when in theory they are really the same. So instead we compute the absolute value of the difference "`abs(t-t1)`" and check if it is smaller than the small number `epsilon`; if it is, then `t` is very close to `t1`, which is all we need.

Here's one further nice trick. In the program above we calculate the new values of the temperature at each time-step with the lines

```python
for i in range(1,N):
    Tp[i] = T[i] + c*(T[i+1]+T[i-1]-2*T[i])
```

but we can if we wish do this more simply—and more quickly—by recalling that Python can do arithmetic with entire arrays in a single step. Using the "slicing" methods that we introduced in Section 2.4.5 we can calculate the new temperatures with a single line:

```python
Tp[1:N] = T[1:N] + c*(T[0:N-1]+T[2:N+1]-2*T[1:N])
```

Because Python can do operations with entire arrays almost as fast as it can with single variables, this makes a huge difference to the speed of the program. On the author's computer the first, pedestrian program takes about 60 seconds to finish. The modified program using the trick above takes only 3 seconds—faster by about a factor of twenty.

Figure 9.6 shows the figure produced by the program. As you can see, the temperature profile starts off with a large region of the system at 20°C and much smaller regions of hotter and colder temperatures near the ends. But as time goes by the profile becomes smoother until by $t = 10$ it is a single straight line from the hot temperature of 50°C to the cold temperature of 0°C.

In this example, we assumed that the boundary conditions on the system, the temperatures at the beginning and end of the grid, were constant in time. But there is no reason why this has to be the case. There are many interesting physics problems where the boundary conditions vary in time to drive the system through a set of different states, and the FTCS method can be used to solve these problems as well. The method is exactly the same as for the case of fixed boundary conditions; the only change we have to make is varying the array elements that hold the boundary conditions as time goes by.

For instance, we might want to study the thermal diffusion problem above, but allow the hot water inside the container to cool down over time. It's a simple matter to vary the array element representing the temperature at the hot boundary so as to incorporate this change. In other respects the program would be exactly the same.

**Exercise 9.4: Thermal diffusion in the Earth's crust**

A classic example of a diffusion problem with a time-varying boundary condition is the diffusion of heat into the crust of the Earth, as surface temperature varies with the seasons. Suppose the mean daily temperature at a particular point on the surface varies as:

$$T_0(t) = A + B\sin\frac{2\pi t}{\tau},$$

where $\tau = 365$ days, $A = 10$°C and $B = 12$°C. At a depth of 20 m below the surface almost all annual temperature variation is ironed out and the temperature is, to a good approximation, a constant 11°C (which is higher than the mean surface temperature of 10°C—temperature increases with depth, due to heating from the hot core of the planet). The thermal diffusivity of the Earth's crust varies somewhat from place to place, but for our purposes we will treat it as constant with value $D = 0.1$ m$^2$ day$^{-1}$.

Write a program, or modify one of the ones given in this chapter, to calculate the temperature profile of the crust as a function of depth up to 20 m and time up to 10 years. Start with temperature everywhere equal to 10°C, except at the surface and the deepest point, choose values for the number of grid points and the time-step $h$, then run your program for the first nine simulated years, to allow it to settle down into whatever pattern it reaches. Then for the tenth and final year plot four temperature profiles taken at 3-month intervals on a single graph to illustrate how the temperature changes as a function of depth and time.

### 9.3.2 Numerical Stability

The FTCS method works well for the diffusion equation, but there are other cases in which it works less well. An example of the latter is the wave equation, one of the most important partial differential equations in physics, describing sound waves and vibrations, electromagnetic waves, water waves, and a host of other phenomena. The FTCS method fails badly when applied to the wave equation, and it does so for interesting reasons.

In one-dimension the wave equation is usually written as

$$\frac{\partial^2\phi}{\partial x^2} - \frac{1}{v^2}\frac{\partial^2\phi}{\partial t^2} = 0, \tag{9.25}$$

but for our purposes it will be useful to rearrange it in the form

$$\frac{\partial^2\phi}{\partial t^2} = v^2\frac{\partial^2\phi}{\partial x^2}. \tag{9.26}$$

We could use this equation to model, for instance, the movement of a vibrating string of length $L$, held fixed at both ends. To solve the equation using the FTCS method we would start by dividing the string into discrete points with spacing $a$. Then we would replace the second derivative on the right-hand side with a discrete difference, using Eq. (5.109), and hence derive a set of second-order ordinary differential equations, one for each grid point:

$$\frac{\mathrm{d}^2\phi}{\mathrm{d}t^2} = \frac{v^2}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.27}$$

Now, using the techniques we learned in Section 8.3, we can change this second-order equation into two first-order equations by defining a new variable $\psi$ thus:

$$\frac{\mathrm{d}\phi}{\mathrm{d}t} = \psi(x,t), \qquad \frac{\mathrm{d}\psi}{\mathrm{d}t} = \frac{v^2}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.28}$$

Then, applying Euler's method, these equations become two FTCS equations thus:

$$\phi(x,t+h) = \phi(x,t) + h\psi(x,t), \tag{9.29a}$$

$$\psi(x,t+h) = \psi(x,t) + h\frac{v^2}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.29b}$$

Now we simply iterate these equations from any given starting condition to get our solution.

Figure 9.7 shows three snapshots from a typical solution, depicting the displacement $\phi$ of the string at three different times $t$ during the run of the program. As we can see, the solution starts off looking fine—we have a normal looking wave on our string (Fig. 9.7a)—but around about the 50 millisecond mark errors start to creep in (Fig. 9.7b), and by 100 milliseconds the errors have grown to dominate the calculation and the results are meaningless (Fig. 9.7c). If we were to let the calculation run longer, we would find that the errors keep on growing until they become so large that they overflow the largest numbers the computer can store. This is not mere rounding error of the kind discussed in Section 4.2. This is something more serious. We say that the calculation has become **numerically unstable**.

What is going on here? Why did the FTCS method work so well for the diffusion equation, but break down for the wave equation? To answer this question let's us return for a moment to the diffusion equation and consider again the basic FTCS form:

$$\phi(x,t+h) = \phi(x,t) + h\frac{D}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.30}$$

(We derived this previously in Eq. (9.23).)

Consider now the following argument, which is known as a **von Neumann stability analysis**, after its inventor John von Neumann, one of the early pioneers of computational physics. We know that the spatial variation of $\phi$ at any time $t$ can always be expressed in the form of a Fourier series $\phi(x,t) = \sum_k c_k(t) e^{ikx}$ for some suitable set of wavevectors $k$ and (time-varying and potentially complex) coefficients $c_k(t)$. Given such an expression let us then ask what form the solution takes at the next time-step of the FTCS calculation, as given by Eq. (9.30) above. Since the equation is linear, we can answer this question by studying what happens to each term in the Fourier series separately, and then adding them up at the end. Plugging a single term $\phi(x,t) = c_k(t) e^{ikx}$ into the equation, we find that

$$\begin{aligned}
\phi(x,t+h) &= c_k(t)e^{ikx} + h\frac{D}{a^2}c_k(t)\left[e^{ik(x+a)} + e^{ik(x-a)} - 2e^{ikx}\right] \\
&= \left[1 + h\frac{D}{a^2}\left(e^{ika} + e^{-ika} - 2\right)\right]c_k(t)e^{ikx} \\
&= \left[1 - h\frac{4D}{a^2}\sin^2\frac{1}{2}ka\right]c_k(t)e^{ikx},
\end{aligned} \tag{9.31}$$

where we have made use of the fact that $e^{i\theta} + e^{-i\theta} = 2\cos\theta$, as well as the half-angle formula $1 - \cos\theta = 2\sin^2\frac{1}{2}\theta$.

This equation tells us that each term in our Fourier series transforms independently under the FTCS equations—the term for wavevector $k$ is multiplied by a $k$-dependent factor, but does not mix with any of the other wavevectors. Knowing this allows us to read off the coefficient of $e^{ikx}$ at time $t+h$ from Eq. (9.31):

$$c_k(t+h) = \left[1 - h\frac{4D}{a^2}\sin^2\frac{1}{2}ka\right]c_k(t). \tag{9.32}$$

So on each time-step of the calculation, $c_k(t)$ is just multiplied by the factor in brackets, which depends on $k$ but not on either $x$ or $t$.

Now we can see how the calculation could become unstable: if the magnitude of the factor in brackets exceeds unity for any wavevector $k$, then the Fourier component with that value of $k$ will grow exponentially as it gets repeatedly multiplied by the same factor on each time-step. Luckily the factor in brackets in this case is always less than one. However, its *magnitude* could become greater than one if it became negative and fell below $-1$. This happens if the term $h(4D/a^2)\sin^2\frac{1}{2}ka$ ever becomes greater than 2. To put that another way, the solution is stable if $h(4D/a^2)\sin^2\frac{1}{2}ka \leq 2$ for all $k$. But the largest possible value of $\sin^2\frac{1}{2}ka$ for any $k$ is 1, so the solution will be stable for all $k$ if we have $h(4D/a^2) \leq 2$, or equivalently

$$h \leq \frac{a^2}{2D}. \tag{9.33}$$

If $h$ is larger than this limit then the solution can diverge, which is an unphysical behavior for the diffusion equation—thermal diffusion never results in a cool object becoming infinitely hot, for example.

On the other hand, if $h < a^2/2D$ then all terms in the Fourier series will decay exponentially and eventually go to zero, except for the $k = 0$ term, for which the multiplicative factor in Eq. (9.32) is always exactly 1. And this is precisely the physical behavior we expect of the diffusion equation. We expect all Fourier components except the one for $k = 0$ to decay, leaving a solution that is uniform in space (unless there are time-varying boundary conditions that are preventing the system from reaching a steady state).

The von Neumann analysis method doesn't work for all equations. For instance, it doesn't work for nonlinear differential equations, because it requires that the full solution of the equation, written as a Fourier composition, can be analyzed by treating each of its Fourier components separately, which is not possible for nonlinear equations. Nonetheless it is applicable to many of the equations we encounter in physics and is one of the simplest ways of demonstrating numerical stability or instability.

Having used the von Neumann analysis to analyze the stability of the diffusion equation, let us now return to the wave equation, for which the FTCS equations are given in Eq. (9.29). Applying the von Neumann analysis to these equations is more complicated than for the diffusion equation because there are now two FTCS equations, one for each of the two variables $\phi$ and $\psi$, but the analysis can still be done. We consider the two variables to be the elements of a two element vector $(\phi, \psi)$, and write a single term in the Fourier series for the solution as

$$\begin{pmatrix} \phi(x,t) \\ \psi(x,t) \end{pmatrix} = \begin{pmatrix} c_\phi(t) \\ c_\psi(t) \end{pmatrix} e^{ikx}. \tag{9.34}$$

Substituting into Eq. (9.29) and following the same line of argument as before, we find that the coefficients of $e^{ikx}$ at the next time-step are

$$c_\phi(t+h) = c_\phi(t) + hc_\psi(t), \tag{9.35a}$$

$$c_\psi(t+h) = c_\psi(t) - hc_\phi(t)\frac{4v^2}{a^2}\sin^2\frac{1}{2}ka, \tag{9.35b}$$

or in vector form

$$\mathbf{c}(t+h) = \mathbf{A}\mathbf{c}(t), \tag{9.36}$$

where $\mathbf{c}(t)$ is the vector $(c_\phi, c_\psi)$ and $\mathbf{A}$ is the matrix

$$\mathbf{A} = \begin{pmatrix} 1 & h \\ -hr^2 & 1 \end{pmatrix} \quad \text{with} \quad r = \frac{2v}{a}\sin\frac{1}{2}ka. \tag{9.37}$$

In other words the vector $\mathbf{c}(t)$ gets multiplied on each time-step by a $2 \times 2$ matrix that depends on $k$ but not on $x$ or $t$.

Now let us write $\mathbf{c}(t)$ as a linear combination of the two (right) eigenvectors of $\mathbf{A}$, which we will call $\mathbf{v}_1$ and $\mathbf{v}_2$, so that $\mathbf{c}(t) = \alpha_1\mathbf{v}_1 + \alpha_2\mathbf{v}_2$ for some constants $\alpha_1$ and $\alpha_2$. Substituting this form into Eq. (9.36) gives

$$\mathbf{c}(t+h) = \mathbf{A}(\alpha_1\mathbf{v}_1 + \alpha_2\mathbf{v}_2) = \alpha_1\lambda_1\mathbf{v}_1 + \alpha_2\lambda_2\mathbf{v}_2, \tag{9.38}$$

where $\lambda_1$ and $\lambda_2$ are the eigenvalues corresponding to the two eigenvectors. We can then repeat the process and multiply by the matrix again to get the value on the next time-step:

$$\mathbf{c}(t+2h) = \alpha_1\lambda_1^2\mathbf{v}_1 + \alpha_2\lambda_2^2\mathbf{v}_2. \tag{9.39}$$

And after $m$ time-steps

$$\mathbf{c}(t+mh) = \alpha_1\lambda_1^m\mathbf{v}_1 + \alpha_2\lambda_2^m\mathbf{v}_2. \tag{9.40}$$

If either (or both) of the eigenvalues have magnitude greater than unity, this solution will diverge to infinity as we take higher and higher powers of the eigenvalues. Or, to put that another way, the solution is numerically stable only if both eigenvalues have magnitude less than or equal to one.

The eigenvalues of the matrix are given by the characteristic determinant equation $\det(\mathbf{A} - \lambda\mathbf{I}) = 0$, where $\mathbf{I}$ is the identity matrix. Making use of Eq. (9.37) for $\mathbf{A}$ and writing out the determinant in full, the equation becomes $(1-\lambda)^2 + h^2r^2 = 0$, which has solutions $\lambda = 1 \pm ihr$. Thus the eigenvalues are complex in this case and both have the same magnitude,

$$|\lambda| = \sqrt{1+h^2r^2} = \sqrt{1 + \frac{4h^2v^2}{a^2}\sin^2\frac{1}{2}ka}. \tag{9.41}$$

But this magnitude is never less than unity. No matter how small we make the value of $h$, the value of $|\lambda|$ will always be greater than one (except for the $k = 0$ Fourier component), and hence the FTCS method is *never stable* for the wave equation.

Unfortunately, this means that the FTCS method simply will not work for solving the wave equation, except over very short time intervals—short enough that the errors don't grow large and swamp the solution. For any but the shortest of intervals, however, we are going to need a different method to solve the wave equation.

**Exercise 9.5: FTCS solution of the wave equation**

Consider a piano string of length $L$, initially at rest. At time $t = 0$ the string is struck by the piano hammer a distance $d$ from the end of the string:

The string vibrates as a result of being struck, except at the ends, $x = 0$ and $x = L$, where it is held fixed.

a) Write a program that uses the FTCS method to solve the complete set of simultaneous first-order equations, Eq. (9.28), for the case $v = 100$ m s$^{-1}$, with the initial condition that $\phi(x) = 0$ everywhere but the velocity $\psi(x)$ is nonzero, with profile

$$\psi(x) = C\frac{x(L-x)}{L^2}\exp\left[-\frac{(x-d)^2}{2\sigma^2}\right],$$

where $L = 1$ m, $d = 10$ cm, $C = 1$ m s$^{-1}$, and $\sigma = 0.3$ m. You will also need to choose a value for the time-step $h$. A reasonable choice is $h = 10^{-6}$ s.

b) Make an animation of the motion of the piano string using the facilities provided by the `visual` package, which we studied in Section 3.4. There are various ways you could do this. A simple one would be to just place a small sphere at the location of each grid point on the string. A more sophisticated approach would be to use the `curve` object in the `visual` package—see the on-line documentation at www.vpython.org for details. A convenient feature of the `curve` object is that you can specify its set of $x$ positions and $y$ positions separately as arrays. In this exercise the $x$ positions only need to specified once, since they never change, while the $y$ positions will need to be specified anew each time you take a time-step. Also, since the vertical displacement of the string is much less than its horizontal length, you will probably need to multiply the vertical displacement by a fairly large factor to make it visible on the screen.

Allow your animation to run for some time, until numerical instabilities start to appear.

### 9.3.3 The Implicit and Crank-Nicolson Methods

One possible approach for remedying the stability problems of the previous section is to use the so-called **implicit method**. Consider Eq. (9.29) again, and let us make the substitution $h \rightarrow -h$ in the equations, giving

$$\phi(x,t-h) = \phi(x,t) - h\psi(x,t), \tag{9.42a}$$

$$\psi(x,t-h) = \psi(x,t) - h\frac{v^2}{a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right]. \tag{9.42b}$$

These equations now tell us how to go back, not forward, in time by an interval $h$. But if we make a second substitution $t \rightarrow t+h$ then, after rearranging, we get

$$\phi(x,t+h) - h\psi(x,t+h) = \phi(x,t) \tag{9.43a}$$

$$\psi(x,t+h) - h\frac{v^2}{a^2}\left[\phi(x+a,t+h) + \phi(x-a,t+h) - 2\phi(x,t+h)\right] = \psi(x,t). \tag{9.43b}$$

Now the equations give us $\phi$ and $\psi$ at $t+h$ again, in terms of the values at $t$, but they don't do so directly—we don't have an explicit expression for $\phi(x,t+h)$ as we did in Eq. (9.29). However, we can regard the equations as a set of simultaneous equations in the values of $\phi$ and $\psi$ at each grid point, which can be solved by standard methods of the kind we looked at in Chapter 6, such as Gaussian elimination. Programs using these equations are going to be more complicated than our FTCS program, and will presumably run slower, but they have the advantage of being numerically stable, as we can show by again performing a von Neumann stability analysis. Using the same form as before for the solution, Eq. (9.34), and retracing our earlier steps, the equivalent of Eq. (9.36) is now

$$\mathbf{B}\mathbf{c}(t+h) = \mathbf{c}(t), \tag{9.44}$$

where $\mathbf{B}$ is the matrix

$$\mathbf{B} = \begin{pmatrix} 1 & -h \\ hr^2 & 1 \end{pmatrix}, \tag{9.45}$$

with $r = (2v/a)\sin\frac{1}{2}ka$ as before. Multiplying (9.44) on both sides by $\mathbf{B}^{-1}$, this then implies that $\mathbf{c}(t+h) = \mathbf{B}^{-1}\mathbf{c}(t)$, with

$$\mathbf{B}^{-1} = \frac{1}{1+h^2r^2}\begin{pmatrix} 1 & h \\ -hr^2 & 1 \end{pmatrix}, \tag{9.46}$$

where we have made use of the standard formula for the inverse of a $2 \times 2$ matrix.

Following the argument we made before, the calculation will be stable only if both eigenvalues of this matrix have magnitude less than or equal to one. The eigenvalues are again solutions of the characteristic equation, which in this case reads $[1-(1+h^2r^2)\lambda]^2 + h^2r^2 = 0$, giving eigenvalues

$$\lambda = \frac{1 \pm ihr}{1+h^2r^2} \tag{9.47}$$

and again the two eigenvalues have the same magnitude:

$$|\lambda| = \frac{1}{\sqrt{1+h^2r^2}}. \tag{9.48}$$

But this value is always less than or equal to one, no matter what the values of $h$ and $r$. Thus the calculation is always numerically stable. We say that the implicit method for the wave equation is **unconditionally stable**.

Unfortunately, we are not finished yet. Being stable is not enough. We have just shown that all Fourier components of our solution will decay exponentially as time passes, which means any initial wave will die away (except for the $k = 0$ component, which is constant and so doesn't give any wave-like behavior). Thus our solution is stable, but it's still unphysical: as we know from elementary physics, waves described by the wave equation normally propagate forever without growing either larger or smaller. In a sense the implicit method goes too far. It overcorrects for the exponential growth of the FTCS method, creating a method with exponential decay instead. What we need is some method that lies in between the FTCS and implicit methods, a method where solutions neither decay or grow out of hand. Such a method is the **Crank-Nicolson method**.

The Crank-Nicolson method is precisely a hybrid of our two previous methods. The equations are derived by taking the average of Eqs. (9.29) and (9.43) to get

$$\phi(x,t+h) - \frac{1}{2}h\psi(x,t+h) = \phi(x,t) + \frac{1}{2}h\psi(x,t), \tag{9.49a}$$

$$\begin{aligned}
\psi(x,t+h) &- h\frac{v^2}{2a^2}\left[\phi(x+a,t+h) + \phi(x-a,t+h) - 2\phi(x,t+h)\right] \\
&= \psi(x,t) + h\frac{v^2}{2a^2}\left[\phi(x+a,t) + \phi(x-a,t) - 2\phi(x,t)\right].
\end{aligned} \tag{9.49b}$$

These equations are again indirect—they do not give us an explicit expression for $\phi$ at $t+h$ but must instead be solved as a set of simultaneous equations to give us the values we want.

If we apply our von Neumann analysis to the Crank-Nicolson method, using again a solution of the form (9.34), we get $\mathbf{B}\mathbf{c}(t+h) = \mathbf{A}\mathbf{c}(t)$, where the matrices $\mathbf{A}$ and $\mathbf{B}$ are the same as before, except that the constant $r$ now takes the value $r = (v/a)\sin\frac{1}{2}ka$, (i.e., it is a factor of two smaller, because of the extra factors of $\frac{1}{2}$ in Eq. (9.49)). Rearranging, we get

$$\mathbf{c}(t+h) = \mathbf{B}^{-1}\mathbf{A}\,\mathbf{c}(t), \tag{9.50}$$

where

$$\mathbf{B}^{-1}\mathbf{A} = \frac{1}{1+h^2r^2}\begin{pmatrix} 1 & h \\ -hr^2 & 1 \end{pmatrix}\begin{pmatrix} 1 & h \\ -hr^2 & 1 \end{pmatrix} = \frac{1}{1+h^2r^2}\begin{pmatrix} 1-h^2r^2 & 2h \\ -2hr^2 & 1-h^2r^2 \end{pmatrix}. \tag{9.51}$$

The characteristic equation for the eigenvalues of this matrix is

$$\left[1-h^2r^2 - (1+h^2r^2)\lambda\right]^2 + 4h^2r^2 = 0, \tag{9.52}$$

which has solutions

$$\lambda = \frac{1-h^2r^2 \pm 2ihr}{1+h^2r^2}, \tag{9.53}$$

and, once again, the two eigenvectors have the same magnitude:

$$|\lambda| = \frac{\sqrt{(1-h^2r^2+2ihr)(1-h^2r^2-2ihr)}}{1+h^2r^2} = 1. \tag{9.54}$$

In other words, the Crank-Nicolson method falls exactly on the boundary between the unstable (FTCS) and stable (implicit) methods, with wave amplitudes that neither grow uncontrollably nor die out as time passes, but instead remain exactly constant (apart from rounding error, presumably). And this is exactly the physical behavior we expect of the wave equation: waves present in the initial conditions should, in theory, persist forever. Thus one should be able, with the help of the Crank-Nicolson method, to solve the wave equation for its behavior over long periods of time.

Although the Crank-Nicolson method is more complicated than the FTCS method, it is still relatively fast. An important point to notice is that in Eq. (9.49) the variables $\phi(x,t)$ and $\psi(x,t)$ on each grid point depend only on the values on the points immediately to the left and right of them. This means that when viewed as a matrix problem the simultaneous equations we need to solve involve **tridiagonal matrices**, and we saw in Section 6.1.6 that such problems can be solved quickly using Gaussian elimination. Exercise 9.8 at the end of this chapter gives you the opportunity to apply the Crank-Nicolson method to the calculation of a solution to the Schrödinger equation of quantum mechanics, to make an animation showing how the wavefunction of a particle evolves over time.

### 9.3.4 Spectral Methods

Finite difference methods are not the only approach for solving partial differential equations. There are a number of other methods available, some of which have fewer stability problems, run faster, or give more accurate solutions, though typically at the cost of substantially more difficult analysis and programming. One popular method is the **finite element method** (not to be confused with the finite difference methods studied in this chapter). In this method one solves the differential equation of interest approximately within small elements of space and time and then stitches those solutions together at the boundaries of the elements to get a complete solution. The finite element method is widely used for large-scale solution of partial differential equations, but is also highly nontrivial—it is the subject of entire books just on its own. We will not look at the finite element method here, but we will look at another method that is invaluable for many of the partial differential equations encountered in physics, is not particularly complicated, and—when it's applicable—gives results much better than either finite difference or finite element methods. This is the **spectral method**, also sometimes called the **Fourier transform method**.

Consider again the wave equation, Eq. (9.26), for a wave on a string of length $L$, fixed at both ends so that $\phi = 0$ at $x = 0$ and at $x = L$. Then consider the trial solution

$$\phi_k(x,t) = \sin\left(\frac{\pi kx}{L}\right)e^{i\omega t}. \tag{9.55}$$

Assuming $\phi$ is supposed to be real, we should really take the real part as our solution, but, as is often the case in physics problems, it will be more convenient to do the math using the complex form and take the real part at the end. So for the moment we will retain the full complex form.

So long as the constant $k$ is an integer, Eq. (9.55) satisfies the requirement of being zero at $x = 0$ and $x = L$, and, substituting into Eq. (9.26), we find that it is indeed a solution of the wave equation provided

$$\omega = \frac{\pi vk}{L}. \tag{9.56}$$

Now let us divide the string into $N$ equal intervals, bounded by $N+1$ grid points, counting the ones at either end, both of which have $\phi = 0$. The positions of the points are

$$x_n = \frac{n}{N}L, \tag{9.57}$$

and the value of our solution at these points is

$$\phi_k(x_n,t) = \sin\left(\frac{\pi kn}{N}\right)\exp\left(i\frac{\pi vkt}{L}\right). \tag{9.58}$$

Since the wave equation is linear, any linear combination of solutions like these for different values of $k$ is also a solution. Thus

$$\phi(x_n,t) = \frac{1}{N}\sum_{k=1}^{N-1} b_k \sin\left(\frac{\pi kn}{N}\right)\exp\left(i\frac{\pi vkt}{L}\right) \tag{9.59}$$

is a solution for any choice of coefficients $b_k$, which may be complex. Note that the sum starts at $k = 1$, because the $k = 0$ term vanishes. (The factor of $1/N$ in front of the sum is optional, but it's convenient for the developments that follow.)

Now notice that at time $t = 0$ this solution takes the form

$$\phi(x_n,0) = \frac{1}{N}\sum_{k=1}^{N-1} b_k \sin\left(\frac{\pi kn}{N}\right). \tag{9.60}$$

If we now write the complex coefficients in the form $b_k = \alpha_k + i\eta_k$ and take the real part of (9.60) we get

$$\phi(x_n,0) = \frac{1}{N}\sum_{k=1}^{N-1} \alpha_k \sin\left(\frac{\pi kn}{N}\right), \tag{9.61}$$

which is a standard Fourier sine series with coefficients $\alpha_k$, of the kind that we looked at in Chapter 7, and particularly in Section 7.3. Such a series can represent any set of samples $\phi(x_n)$ and hence we can match any given initial value of $\phi$ with the solution (9.59) on the grid points.

Similarly, the time derivative of the real part of the solution at $t = 0$ is

$$\frac{\partial\phi}{\partial t} = -\left(\frac{\pi v}{L}\right)\frac{1}{N}\sum_{k=1}^{N-1} k\eta_k \sin\left(\frac{\pi kn}{N}\right), \tag{9.62}$$

which, apart from the leading numerical factor, is another sine series, but with coefficients $k\eta_k$. Hence, by a suitable choice of $\eta_k$ this series allows us to match any given initial derivative of $\phi$.

To put it another way, if we are given both the initial value and the initial derivative of $\phi$ at all points, then that fixes both the real and imaginary parts of the coefficients $b_k$, and hence our entire solution, Eq. (9.59), is determined, not just at $t = 0$ but at all times. Note that it is normal that we need both the value and the derivative of $\phi$ because the wave equation is second-order in time, requiring two initial conditions to fix the solution.

There are a couple of nice features of this approach. First, since Eqs. (9.61) and (9.62) are both standard Fourier sine series, we can calculate the coefficients $\alpha_k$ and $\eta_k$ using the fast Fourier transform of Section 7.4, or more correctly the fast discrete sine transform. Doing this is usually a lot faster than directly evaluating the sums in the equations. Moreover, once we have the coefficients, we can also evaluate the solution, Eq. (9.59), using fast transforms. Again writing $b_k = \alpha_k + i\eta_k$ and taking the real part of (9.59), we have

$$\phi(x_n,t) = \frac{1}{N}\sum_{k=1}^{N-1}\left[\alpha_k\cos\left(\frac{\pi vkt}{L}\right) - \eta_k\sin\left(\frac{\pi vkt}{L}\right)\right]\sin\left(\frac{\pi kn}{N}\right). \tag{9.63}$$

But this is just another sine series, with coefficients equal to the quantity in square brackets. Thus we can evaluate the sum using the fast inverse discrete sine transform.

Second, notice that, unlike finite difference methods, this method doesn't require us to "step through" one time-step after another in order to calculate the solution at some specified time $t$. Equation (9.63) gives the solution at any time directly, without passing through previous times. Thus, if we want to know the solution at just a single time in the future, we can go straight there. Or if we want to create an animation of the system at intervals of $\Delta t$, we can just calculate the solution at those intervals and nowhere else.

In principle, the spectral method is slower than FTCS for calculating the solution in a single time slice. As we saw in Section 7.4, the fast Fourier transform takes time proportional to $N\log N$, whereas one step of the FTCS method takes time proportional to $N$. For large enough values of $N$, therefore, one FTCS step will always be quicker than one spectral method step. But the fact that we don't have to calculate the solution at all time-steps often outweighs the difference in speed of individual steps. We might have to do a million steps of the FTCS method to reach the time we want, whereas we only have to do a single step of the spectral method. (And of course FTCS is numerically unstable, while the spectral method has no such problems. The Crank-Nicolson method of Section 9.3.3 is stable, but somewhat slower than FTCS, and it still requires us to go through many time-steps to get to the time we want.)

The spectral method does have its limitations. In particular, it only works for problems such as this one where the boundary conditions are rather simple, such as $\phi = 0$ at the edges of a simply shaped region or box. There is no straightforward way to adapt the method to more strangely shaped boundary conditions. Also the method is applicable only to linear differential equations because for nonlinear equations we cannot add together a set of individual solutions to get a complete solution as we did above. The finite difference methods suffer from neither of these limitations.

Exercise 9.9 gives you an opportunity to develop a program to apply the spectral method to the solution of the same Schrödinger equation problem studied with the Crank-Nicolson method in Exercise 9.8. If you do both exercises you can compare the answers to see how well they agree and find which method is faster for this problem.

---

## Further Exercises

**Exercise 9.6:** What would the equivalent of Eq. (9.7) be in three dimensions?

**Exercise 9.7:** The relaxation method for ordinary differential equations: There is no reason why the relaxation method must be restricted to the solution of differential equations with two or more independent variables. It can also be applied to those with one independent variable, i.e., to ordinary differential equations. In this context, as with partial differential equations, it is a technique for solving boundary value problems, which are less common with ordinary differential equations but do occur—we discussed them in Section 8.6.

Consider the problem we looked at in Example 8.8 on page 390, in which a ball of mass $m = 1$ kg is thrown from height $x = 0$ into the air and lands back at $x = 0$ ten seconds later. The problem is to calculate the trajectory of the ball, but we cannot do it using initial value methods like the ordinary Runge-Kutta method because we are not told the initial velocity of the ball. One approach to finding a solution is the shooting method of Section 8.6.1. Another is the relaxation method.

Ignoring friction effects, the trajectory is the solution of the ordinary differential equation

$$\frac{\mathrm{d}^2x}{\mathrm{d}t^2} = -g,$$

where $g$ is the acceleration due to gravity.

a) Replacing the second derivative in this equation with its finite-difference approximation, Eq. (5.109), derive a relaxation-method equation for solving this problem on a time-like "grid" of points with separation $h$.

b) Taking the boundary conditions to be that $x = 0$ at $t = 0$ and $t = 10$, write a program to solve for the height of the ball as a function of time using the relaxation method with 100 points and make a plot of the result from $t = 0$ to $t = 10$. Run the relaxation method until the answers change by $10^{-6}$ or less at every point on each step.

Note that, unlike the shooting method, the relaxation method does not give us the initial value of the velocity needed to achieve the required solution. It gives us only the solution itself, although one could get an approximation to the initial velocity by calculating a numerical derivative of the solution at time $t = 0$. On balance, however, the relaxation method for ordinary differential equations is most useful when one wants to know the details of the solution itself, but not the initial conditions needed to achieve it.

**Exercise 9.8:** The Schrödinger equation and the Crank-Nicolson method: Perhaps the most important partial differential equation, at least for physicists, is the Schrödinger equation. This exercise uses the Crank-Nicolson method to solve the full time-dependent Schrödinger equation and hence develop a picture of how a wavefunction evolves over time. The following exercise, Exercise 9.9, solves the same problem again, but using the spectral method.

We will look at the Schrödinger equation in one dimension. The techniques for calculating solutions in two or three dimensions are basically the same as for one dimension, but the calculations take much longer on the computer, so in the interests of speed we'll stick with one dimension. In one dimension the Schrödinger equation for a particle of mass $M$ with no potential energy reads

$$-\frac{\hbar^2}{2M}\frac{\partial^2\psi}{\partial x^2} = i\hbar\frac{\partial\psi}{\partial t}.$$

For simplicity, let's put our particle in a box with impenetrable walls, so that we only have to solve the equation in a finite-sized space. The box forces the wavefunction $\psi$ to be zero at the walls, which we'll put at $x = 0$ and $x = L$.

Replacing the second derivative in the Schrödinger equation with a finite difference and applying Euler's method, we get the FTCS equation

$$\psi(x,t+h) = \psi(x,t) + h\frac{i\hbar}{2ma^2}\left[\psi(x+a,t) + \psi(x-a,t) - 2\psi(x,t)\right],$$

where $a$ is the spacing of the spatial grid points and $h$ is the size of the time-step. (Be careful not to confuse the time-step $h$ with Planck's constant $\hbar$.) Performing a similar step in reverse, we get the implicit equation

$$\psi(x,t+h) - h\frac{i\hbar}{2ma^2}\left[\psi(x+a,t+h) + \psi(x-a,t+h) - 2\psi(x,t+h)\right] = \psi(x,t).$$

And taking the average of these two, we get the Crank-Nicolson equation for the Schrödinger equation:

$$\begin{aligned}
\psi(x,t+h) &- h\frac{i\hbar}{4ma^2}\left[\psi(x+a,t+h) + \psi(x-a,t+h) - 2\psi(x,t+h)\right] \\
&= \psi(x,t) + h\frac{i\hbar}{4ma^2}\left[\psi(x+a,t) + \psi(x-a,t) - 2\psi(x,t)\right].
\end{aligned}$$

This gives us a set of simultaneous equations, one for each grid point.

The boundary conditions on our problem tell us that $\psi = 0$ at $x = 0$ and $x = L$ for all $t$. In between these points we have grid points at $a, 2a, 3a$, and so forth. Let us arrange the values of $\psi$ at these interior points into a vector

$$\boldsymbol{\psi}(t) = \begin{pmatrix} \psi(a,t) \\ \psi(2a,t) \\ \psi(3a,t) \\ \vdots \end{pmatrix}.$$

Then the Crank-Nicolson equations can be written in the form

$$\mathbf{A}\boldsymbol{\psi}(t+h) = \mathbf{B}\boldsymbol{\psi}(t),$$

where the matrices $\mathbf{A}$ and $\mathbf{B}$ are both symmetric and tridiagonal:

$$\mathbf{A} = \begin{pmatrix} a_1 & a_2 & & & \\ a_2 & a_1 & a_2 & & \\ & a_2 & a_1 & a_2 & \\ & & a_2 & a_1 & \\ & & & & \ddots \end{pmatrix}, \qquad \mathbf{B} = \begin{pmatrix} b_1 & b_2 & & & \\ b_2 & b_1 & b_2 & & \\ & b_2 & b_1 & b_2 & \\ & & b_2 & b_1 & \\ & & & & \ddots \end{pmatrix},$$

with

$$a_1 = 1 + h\frac{i\hbar}{2ma^2}, \quad a_2 = -h\frac{i\hbar}{4ma^2}, \quad b_1 = 1 - h\frac{i\hbar}{2ma^2}, \quad b_2 = h\frac{i\hbar}{4ma^2}.$$

(Note the different signs and the factors of 2 and 4 in the denominators.)

The equation $\mathbf{A}\boldsymbol{\psi}(t+h) = \mathbf{B}\boldsymbol{\psi}(t)$ has precisely the form $\mathbf{A}\mathbf{x} = \mathbf{v}$ of the simultaneous equation problems we studied in Chapter 6 and can be solved using the same methods. Specifically, since the matrix $\mathbf{A}$ is tridiagonal in this case, we can use the fast tridiagonal version of Gaussian elimination that we looked at in Section 6.1.6.

Consider an electron (mass $M = 9.109 \times 10^{-31}$ kg) in a box of length $L = 10^{-8}$ m. Suppose that at time $t = 0$ the wavefunction of the electron has the form

$$\psi(x,0) = \exp\left[-\frac{(x-x_0)^2}{2\sigma^2}\right]e^{i\kappa x},$$

where

$$x_0 = \frac{L}{2}, \qquad \sigma = 1 \times 10^{-10} \text{ m}, \qquad \kappa = 5 \times 10^{10} \text{ m}^{-1},$$

and $\psi = 0$ on the walls at $x = 0$ and $x = L$. (This expression for $\psi(x,0)$ is not normalized—there should really be an overall multiplying coefficient to make sure that the probability density for the electron integrates to unity. It's safe to drop the constant, however, because the Schrödinger equation is linear, so the constant cancels out on both sides of the equation and plays no part in the solution.)

a) Write a program to perform a single step of the Crank-Nicolson method for this electron, calculating the vector $\boldsymbol{\psi}(t)$ of values of the wavefunction, given the initial wavefunction above and using $N = 1000$ spatial slices with $a = L/N$. Your program will have to perform the following steps. First, given the vector $\boldsymbol{\psi}(0)$ at $t = 0$, you will have to multiply by the matrix $\mathbf{B}$ to get a vector $\mathbf{v} = \mathbf{B}\boldsymbol{\psi}$. Because of the tridiagonal form of $\mathbf{B}$, this is fairly simple. The $i$th component of $\mathbf{v}$ is given by

$$v_i = b_1\psi_i + b_2(\psi_{i+1} + \psi_{i-1}).$$

You will also have to choose a value for the time-step $h$. A reasonable choice is $h = 10^{-18}$ s.

Second you will have to solve the linear system $\mathbf{A}\mathbf{x} = \mathbf{v}$ for $\mathbf{x}$, which gives you the new value of $\boldsymbol{\psi}$. You could do this using a standard linear equation solver like the function `solve` in `numpy.linalg`, but since the matrix $\mathbf{A}$ is tridiagonal a better approach would be to use the fast solver for banded matrices given in Appendix E, which can be imported from the file `banded.py` (which you can find in the on-line resources). This solver works fine with complex-valued arrays, which you'll need to use to represent the wavefunction $\psi$ and the matrix $\mathbf{A}$.

Once you have the code in place to perform a single step of the calculation, extend your program to perform repeated steps and hence solve for $\psi$ at a sequence of times a separation $h$ apart. Note that the matrix $\mathbf{A}$ is independent of time, so it doesn't change from one step to another. You can set up the matrix just once and then keep on reusing it for every step.

b) Extend your program to make an animation of the solution by displaying the real part of the wavefunction at each time-step. You can use the function `rate` from the package `visual` to ensure a smooth frame-rate for your animation—see Section 3.5 on page 117.

There are various ways you could do the animation. A simple one would be to just place a small sphere at each grid point with vertical position representing the value of the real part of the wavefunction. A more sophisticated approach would be to use the `curve` object from the `visual` package—see the on-line documentation at www.vpython.org for details. Depending on what coordinates you use for measuring $x$, you may need to scale the values of the wavefunction by an additional constant to make them a reasonable size on the screen. (If you measure your $x$ position in meters then a scale factor of about $10^{-9}$ works well for the wavefunction.)

c) Run your animation for a while and describe what you see. Write a few sentences explaining in physics terms what is going on in the system.

**Exercise 9.9:** The Schrödinger equation and the spectral method: This exercise uses the spectral method to solve the time-dependent Schrödinger equation

$$-\frac{\hbar^2}{2M}\frac{\partial^2\psi}{\partial x^2} = i\hbar\frac{\partial\psi}{\partial t}$$

for the same system as in Exercise 9.8, a single particle in one dimension in a box of length $L$ with impenetrable walls. The wavefunction in such a box necessarily goes to zero on the walls and hence one possible (unnormalized) solution of the equation is

$$\psi_k(x,t) = \sin\left(\frac{\pi kx}{L}\right)e^{iEt/\hbar},$$

where the energy $E$ can be found by substituting into the Schrödinger equation, giving

$$E = \frac{\pi^2\hbar^2k^2}{2ML^2}.$$

As with the vibrating string of Section 9.3.4, we can write a full solution as a linear combination of such individual solutions, which on the grid points $x_n = nL/N$ takes the value

$$\psi(x_n,t) = \frac{1}{N}\sum_{k=1}^{N-1} b_k \sin\left(\frac{\pi kn}{N}\right)\exp\left(i\frac{\pi^2\hbar k^2}{2ML^2}t\right),$$

where the $b_k$ are some set of (possibly complex) coefficients that specify the exact shape of the wavefunction and the leading factor of $1/N$ is optional but convenient.

Since the Schrödinger equation (unlike the wave equation) is first order in time, we need only a single initial condition on the value of $\psi(x,t)$ to specify the coefficients $b_k$, although, since the coefficients are in general complex, we will need to calculate both real and imaginary parts of each coefficient.

As in Exercise 9.8 we consider an electron (mass $M = 9.109 \times 10^{-31}$ kg) in a box of length $L = 10^{-8}$ m. At time $t = 0$ the wavefunction of the electron has the form

$$\psi(x,0) = \exp\left[-\frac{(x-x_0)^2}{2\sigma^2}\right]e^{i\kappa x},$$

where

$$x_0 = \frac{L}{2}, \qquad \sigma = 1 \times 10^{-10} \text{ m}, \qquad \kappa = 5 \times 10^{10} \text{ m}^{-1},$$

and $\psi = 0$ on the walls at $x = 0$ and $x = L$.

a) Write a program to calculate the values of the coefficients $b_k$, which for convenience can be broken down into their real and imaginary parts as $b_k = \alpha_k + i\eta_k$. Divide the box into $N = 1000$ slices and create two arrays containing the real and imaginary parts of $\psi(x_n,0)$ at each grid point. Perform discrete sine transforms on each array separately and hence calculate the values of the $\alpha_k$ and $\eta_k$ for all $k = 1 \ldots N-1$.

To perform the discrete sine transforms, you can use the fast transform function `dst` from the package `dcst`, which you can find in the on-line resources in the file named `dcst.py`. A copy of the code for the package can also be found in Appendix E. The function takes an array of $N$ real numbers and returns the discrete sine transform as another array of $N$ numbers.

b) Putting $b_k = \alpha_k + i\eta_k$ in the solution above and taking the real part we get

$$\text{Re}\,\psi(x_n,t) = \frac{1}{N}\sum_{k=1}^{N-1}\left[\alpha_k\cos\left(\frac{\pi^2\hbar k^2}{2ML^2}t\right) - \eta_k\sin\left(\frac{\pi^2\hbar k^2}{2ML^2}t\right)\right]\sin\left(\frac{\pi kn}{N}\right)$$

for the real part of the wavefunction. This is an inverse sine transform with coefficients equal to the quantities in the square brackets. Extend your program to calculate the real part of the wavefunction $\psi(x,t)$ at an arbitrary time $t$ using this formula and the inverse discrete sine transform function `idst`, also from the package `dcst`. Test your program by making a graph of the wavefunction at time $t = 10^{-16}$ s.

c) Extend your program further to make an animation of the wavefunction over time, similar to that described in part (b) of Exercise 9.8 above. A suitable time interval for each frame of the animation is about $10^{-18}$ s.

d) Run your animation for a while and describe what you see. Write a few sentences explaining in physics terms what is going on in the system.
