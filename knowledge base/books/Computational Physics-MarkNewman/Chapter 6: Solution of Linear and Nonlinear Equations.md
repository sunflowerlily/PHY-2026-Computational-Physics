# Chapter 6: Solution of Linear and Nonlinear Equations

One of the commonest uses of computers in physics is the solution of equations or sets of equations of various kinds. In this chapter we look at methods for solving both linear and nonlinear equations. Solutions of linear equations involve techniques from linear algebra, so we will spend some time learning how linear algebra tasks such as inversion and diagonalization of matrices can be accomplished on the computer. In the second part of the chapter we will look at schemes for solving nonlinear equations.

## 6.1 Simultaneous Linear Equations

A single linear equation in one variable, such as $x - 1 = 0$, is trivial to solve. We do not need computers to do this for us. But simultaneous sets of linear equations in many variables are harder. In principle the techniques for solving them are well understood and straightforward—all of us learned them at some point in school—but they are also tedious, involving many operations, additions, subtractions, multiplications, one after another. Humans are slow and prone to error in such calculations, but computers are perfectly suited to the work and the solution of systems of simultaneous equations, particularly large systems with many variables, is a common job for computers in physics.

Let us take an example. Suppose you want to solve the following four simultaneous equations for the variables $w, x, y,$ and $z$:

$$2w + x + 4y + z = -4 \quad (6.1a)$$
$$3w + 4x - y - z = 3 \quad (6.1b)$$
$$w - 4x + y + 5z = 9 \quad (6.1c)$$
$$2w - 2x + y + 3z = 7 \quad (6.1d)$$

For computational purposes the simplest way to think of these is in matrix form: they can be written as

$$\begin{pmatrix} 2 & 1 & 4 & 1 \\ 3 & 4 & -1 & -1 \\ 1 & -4 & 1 & 5 \\ 2 & -2 & 1 & 3 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -4 \\ 3 \\ 9 \\ 7 \end{pmatrix} \quad (6.2)$$

Alternatively, we could write this out shorthand as

$$\mathbf{Ax} = \mathbf{v} \quad (6.3)$$

where $\mathbf{x} = (w, x, y, z)$ and the matrix $\mathbf{A}$ and vector $\mathbf{v}$ take the appropriate values.

One way to solve equations of this form is to find the inverse of the matrix $\mathbf{A}$ then multiply both sides of (6.3) by it to get the solution $\mathbf{x} = \mathbf{A}^{-1}\mathbf{v}$. This sounds like a promising approach for solving equations on the computer but in practice it's not as good as you might think. Inverting the matrix $\mathbf{A}$ is a rather complicated calculation that is inefficient and cumbersome to carry out numerically. There are other ways of solving simultaneous equations that don't require us to calculate an inverse and it turns out that these are faster, simpler, and more accurate. Perhaps the most straightforward method, and the first one we will look at, is **Gaussian elimination**.

### 6.1.1 Gaussian Elimination

Suppose we wish to solve a set of simultaneous equations like Eq. (6.1). We will carry out the solution by working on the matrix form $\mathbf{Ax} = \mathbf{v}$ of the equations. As you are undoubtedly aware, the following useful rules apply:

1. We can multiply any of our simultaneous equations by a constant and it's still the same equation. For instance, we can multiply Eq. (6.1a) by 2 to get $4w + 2x + 8y + 2z = -8$ and the solution for $w, x, y, z$ stays the same. To put that another way: *If we multiply any row of the matrix $\mathbf{A}$ by any constant, and we multiply the corresponding row of the vector $\mathbf{v}$ by the same constant, then the solution does not change.*

2. We can take any linear combination of two equations to get another correct equation. To put that another way: *If we add to or subtract from any row of $\mathbf{A}$ a multiple of any other row, and we do the same for the vector $\mathbf{v}$, then the solution does not change.*

We can use these operations to solve our equations as follows. Consider the matrix form of the equations given in Eq. (6.2) and let us perform the following steps:

1. We divide the first row by the top-left element of the matrix, which has the value 2 in this case. Recall that we must divide both the matrix itself and the corresponding element on the right-hand side of the equation, in order that the equations remain correct. Thus we get:

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 3 & 4 & -1 & -1 \\ 1 & -4 & 1 & 5 \\ 2 & -2 & 1 & 3 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 3 \\ 9 \\ 7 \end{pmatrix} \quad (6.4)$$

Because we have divided both on the left and on the right, the solution to the equations is unchanged from before, but note that the top-left element of the matrix, by definition, is now equal to 1.

2. Next, note that the first element in the second row of the matrix is a 3. If we now subtract 3 times the first row from the second this element will become zero, thus:

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 0 & 2.5 & -7 & -2.5 \\ 1 & -4 & 1 & 5 \\ 2 & -2 & 1 & 3 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 9 \\ 9 \\ 7 \end{pmatrix} \quad (6.5)$$

Notice again that we have performed the same subtraction on the right-hand side of the equation, to make sure the solution remains unchanged.

3. We now do a similar trick with the third and fourth rows. These have first elements equal to 1 and 2 respectively, so we subtract 1 times the first row from the third, and 2 times the first row from the fourth, which gives us the following:

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 0 & 2.5 & -7 & -2.5 \\ 0 & -4.5 & 1 & 4.5 \\ 0 & -3 & -3 & 2 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 9 \\ 11 \\ 11 \end{pmatrix} \quad (6.6)$$

The end result of this series of operations is that the first column of our matrix has been reduced to the simple form $(1, 0, 0, 0)$, but the solution of the complete set of equations is unchanged.

Now we move on to the second row of the matrix and perform a similar series of operations. We divide the second row by its *second* element, to get

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 0 & 1 & -2.8 & -1 \\ 0 & -4.5 & 1 & 4.5 \\ 0 & -3 & -3 & 2 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 3.6 \\ 11 \\ 11 \end{pmatrix} \quad (6.7)$$

Then we subtract the appropriate multiple of the second row from each of the rows below it, so as to make the second element of each of those rows zero. That is, we subtract $-4.5$ times the second row from the third, and $-3$ times the second row from the fourth, to give

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 0 & 1 & -2.8 & -1 \\ 0 & 0 & -13.6 & 0 \\ 0 & 0 & -11.4 & -1 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 3.6 \\ 27.2 \\ 21.8 \end{pmatrix} \quad (6.8)$$

Then we move onto the third and fourth rows, and do the same thing, dividing each then subtracting from the rows below (except that the fourth row obviously doesn't have any rows below, so it only needs to be divided). The end result of the entire set of operations is the following:

$$\begin{pmatrix} 1 & 0.5 & 2 & 0.5 \\ 0 & 1 & -2.8 & -1 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -2 \\ 3.6 \\ -2 \\ 1 \end{pmatrix} \quad (6.9)$$

By definition, this set of equations still has the same solution for the variables $w, x, y,$ and $z$ as the equations we started with, but the matrix is now **upper triangular**: all the elements below the diagonal are zero. This allows us to determine the solution for the variables quite simply by the process of **backsubstitution**.

### 6.1.2 Backsubstitution

Suppose we have any set of equations of the form

$$\begin{pmatrix} 1 & a_{01} & a_{02} & a_{03} \\ 0 & 1 & a_{12} & a_{13} \\ 0 & 0 & 1 & a_{23} \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} v_0 \\ v_1 \\ v_2 \\ v_3 \end{pmatrix} \quad (6.10)$$

which is exactly the form of Eq. (6.9) generated by the Gaussian elimination procedure. We can write the equations out in full as

$$w + a_{01}x + a_{02}y + a_{03}z = v_0 \quad (6.11a)$$
$$x + a_{12}y + a_{13}z = v_1 \quad (6.11b)$$
$$y + a_{23}z = v_2 \quad (6.11c)$$
$$z = v_3 \quad (6.11d)$$

Note that we are using Python-style numbering for the elements here, starting from zero, rather than one. This isn't strictly necessary, but it will be convenient when we want to translate our calculation into computer code.

Given equations of this form, we see now that the solution for the value of $z$ is trivial—it is given directly by Eq. (6.11d):

$$z = v_3 \quad (6.12)$$

But given this value, the solution for $y$ is also trivial, being given by Eq. (6.11c):

$$y = v_2 - a_{23}z \quad (6.13)$$

And we can go on. The solution for $x$ is

$$x = v_1 - a_{12}y - a_{13}z \quad (6.14)$$

and

$$w = v_0 - a_{01}x - a_{02}y - a_{03}z \quad (6.15)$$

Applying these formulas to Eq. (6.9) gives

$$w = 2, \quad x = -1, \quad y = -2, \quad z = 1 \quad (6.16)$$

which is, needless to say, the correct answer.

Thus by the combination of Gaussian elimination with backsubstitution we have solved our set of simultaneous equations.

**Example 6.1: Gaussian Elimination with Backsubstitution**

We are now in a position to create a complete program for solving simultaneous equations. Here is a program to solve the equations in (6.1) using Gaussian elimination and backsubstitution:

```python
from numpy import array, empty

A = array([[ 2,  1,  4,  1 ],
           [ 3,  4, -1, -1 ],
           [ 1, -4,  1,  5 ],
           [ 2, -2,  1,  3 ]], float)
v = array([ -4, 3, 9, 7 ], float)
N = len(v)

# Gaussian elimination
for m in range(N):
    # Divide by the diagonal element
    div = A[m,m]
    A[m,:] /= div
    v[m] /= div
    
    # Now subtract from the lower rows
    for i in range(m+1,N):
        mult = A[i,m]
        A[i,:] -= mult*A[m,:]
        v[i] -= mult*v[m]

# Backsubstitution
x = empty(N, float)
for m in range(N-1,-1,-1):
    x[m] = v[m]
    for i in range(m+1,N):
        x[m] -= A[m,i]*x[i]

print(x)
```

There are number of features to notice about this program. We store the matrices and vectors as arrays, whose initial values are set at the start of the program. The elimination portion of the program goes through each row of the matrix, one by one, and first normalizes it by dividing by the appropriate diagonal element, then subtracts a multiple of that row from each lower row. Notice how the program uses Python's ability to perform operations on entire rows at once, which makes the calculation faster and simpler to program. The second part of the program is a straightforward version of the backsubstitution procedure. Note that the entire program is written so as to work for matrices of any size: we use the variable `N` to represent the size, so that no matter what size of matrix we feed to the program it will perform the correct calculation.

---

**Exercise 6.1: A circuit of resistors**

Consider the following circuit of resistors:

[Diagram of resistor network with nodes V₁, V₂, V₃, V₄ connected to V₊ = 5V at top and 0 Volts (ground) at bottom]

All the resistors have the same resistance $R$. The power rail at the top is at voltage $V_+ = 5$ V. What are the other four voltages, $V_1$ to $V_4$?

To answer this question we use Ohm's law and the Kirchhoff current law, which says that the total net current flow out of (or into) any junction in a circuit must be zero. Thus for the junction at voltage $V_1$, for instance, we have

$$\frac{V_1-V_2}{R} + \frac{V_1-V_3}{R} + \frac{V_1-V_4}{R} + \frac{V_1-V_+}{R} = 0,$$

or equivalently

$$4V_1 - V_2 - V_3 - V_4 = V_+.$$

a) Write similar equations for the other three junctions with unknown voltages.

b) Write a program to solve the four resulting equations using Gaussian elimination and hence find the four voltages (or you can modify a program you already have, such as the program `gausselim.py` in Example 6.1).

### 6.1.3 Pivoting

Suppose the equations we want to solve are slightly different from those of the previous section, thus:

$$\begin{pmatrix} 0 & 1 & 4 & 1 \\ 3 & 4 & -1 & -1 \\ 1 & -4 & 1 & 5 \\ 2 & -2 & 1 & 3 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} -4 \\ 3 \\ 9 \\ 7 \end{pmatrix} \quad (6.17)$$

Just one thing has changed from the old equations in (6.2): the first element of the first row of the matrix is zero, where previously it was nonzero. But this makes all the difference in the world, because the first step of our Gaussian elimination procedure requires us to divide the first row of the matrix by its first element, which we can no longer do, because we would have to divide by zero. In cases like these, Gaussian elimination no longer works. So what are we to do?

The standard solution is to use **pivoting**, which means simply interchanging the rows of the matrix to get rid of the problem. Clearly we are allowed to interchange the order in which we write our simultaneous equations—it will not affect their solution—so we could, if we like, swap the first and second equations, which in matrix notation is equivalent to writing

$$\begin{pmatrix} 3 & 4 & -1 & -1 \\ 0 & 1 & 4 & 1 \\ 1 & -4 & 1 & 5 \\ 2 & -2 & 1 & 3 \end{pmatrix} \begin{pmatrix} w \\ x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 3 \\ -4 \\ 9 \\ 7 \end{pmatrix} \quad (6.18)$$

In other words, we have swapped the first and second rows of the matrix and also swapped the first and second elements of the vector on the right-hand side. Now the first element of the matrix is no longer zero, and Gaussian elimination will work just fine.

Pivoting has to be done with care. We must make sure, for instance, that in swapping equations to get rid of a problem we don't introduce another problem somewhere else. Moreover, the elements of the matrix change as the Gaussian elimination procedure progresses, so it's not always obvious in advance where problems are going to arise. A number of different rules or schemes for pivoting have been developed to guide the order in which the equations should be swapped. A good, general scheme that works well in most cases is the so-called **partial pivoting** method, which is as follows.

As we have seen the Gaussian elimination procedure works down the rows of the matrix one by one, dividing each by the appropriate diagonal element, before performing subtractions. With partial pivoting we consider rearranging the rows at each stage. When we get to the $m$th row, we compare it to all lower rows, looking at the value each row has in its $m$th element and finding the one such value that is farthest from zero—either positive or negative. If the row containing this winning value is not currently the $m$th row then we move it up to $m$th place by swapping it with the current $m$th row. This has the result of ensuring that the element we divide by in our Gaussian elimination is always as far from zero as possible.

If we look at Eq. (6.18), we see that in fact we inadvertently did exactly the right thing when we swapped the first and second rows of our matrix, since we moved the row with the largest first element to the top of the matrix. Now we would perform the first step of the Gaussian elimination procedure on the resulting matrix, move on to the second row and pivot again.

In practice, one should always use pivoting when applying Gaussian elimination, since you rarely know in advance when the equations you're trying to solve will present a problem. Exercise 6.2 invites you to extend the Gaussian elimination program from Example 6.1 to incorporate partial pivoting.

---

**Exercise 6.2:**

a) Modify the program `gausselim.py` in Example 6.1 to incorporate partial pivoting (or you can write your own program from scratch if you prefer). Run your program and demonstrate that it gives the same answers as the original program when applied to Eq. (6.1).

b) Modify the program to solve the equations in (6.17) and show that it can find the solution to these as well, even though Gaussian elimination without pivoting fails.

### 6.1.4 LU Decomposition

The Gaussian elimination method, combined with partial pivoting, is a reliable method for solving simultaneous equations and is widely used. For the types of calculations that crop up in computational physics, however, it is commonly used in a slightly different form from the one we have seen so far. In physics calculations it often happens that we want to solve many different sets of equations $\mathbf{Ax} = \mathbf{v}$ with the same matrix $\mathbf{A}$ but different right-hand sides $\mathbf{v}$. In such cases it would be wasteful to perform a full Gaussian elimination for every set of equations. The effect on the matrix $\mathbf{A}$ will be the same every time—it will always be transformed into the same upper triangular matrix—and only the vector $\mathbf{v}$ will change. It would be more efficient if we could do the full Gaussian elimination just once and somehow record or memorize the divisions, multiplications, and subtractions we perform on each side of the equation, so that we can later perform them on as many vectors $\mathbf{v}$ as we like without having to perform them again on the matrix $\mathbf{A}$. There is a variant of Gaussian elimination that does exactly this, called **LU decomposition** (pronounced as two separate letters "L-U").

Suppose we have a matrix $\mathbf{A}$ of the form

$$\mathbf{A} = \begin{pmatrix} a_{00} & a_{01} & a_{02} & a_{03} \\ a_{10} & a_{11} & a_{12} & a_{13} \\ a_{20} & a_{21} & a_{22} & a_{23} \\ a_{30} & a_{31} & a_{32} & a_{33} \end{pmatrix} \quad (6.19)$$

where we have numbered the elements in Python style, starting from zero. We use a $4 \times 4$ matrix here, but the generalization of the calculation to matrices of other sizes is straightforward.

Let us perform Gaussian elimination on this matrix to reduce it to upper-triangular form, but we will write the elimination process in a manner slightly different from before, using matrix notation. Recall that in the first step of the elimination process we divide the first row of the matrix by its first element $a_{00}$, then we subtract the first row times $a_{10}$ from the second, times $a_{20}$ from the third, and times $a_{30}$ from the fourth. These operations can be neatly written as a single matrix multiplication, thus:

$$\frac{1}{a_{00}}\begin{pmatrix} 1 & 0 & 0 & 0 \\ -a_{10} & a_{00} & 0 & 0 \\ -a_{20} & 0 & a_{00} & 0 \\ -a_{30} & 0 & 0 & a_{00} \end{pmatrix} \begin{pmatrix} a_{00} & a_{01} & a_{02} & a_{03} \\ a_{10} & a_{11} & a_{12} & a_{13} \\ a_{20} & a_{21} & a_{22} & a_{23} \\ a_{30} & a_{31} & a_{32} & a_{33} \end{pmatrix} = \begin{pmatrix} 1 & b_{01} & b_{02} & b_{03} \\ 0 & b_{11} & b_{12} & b_{13} \\ 0 & b_{21} & b_{22} & b_{23} \\ 0 & b_{31} & b_{32} & b_{33} \end{pmatrix} \quad (6.20)$$

(It's worth doing the multiplication for yourself, to see how it works out.) The matrix we're multiplying by on the left we will call $\mathbf{L}_0$. Note that this matrix is **lower triangular**—all the elements above the diagonal are zero:

$$\mathbf{L}_0 = \frac{1}{a_{00}}\begin{pmatrix} 1 & 0 & 0 & 0 \\ -a_{10} & a_{00} & 0 & 0 \\ -a_{20} & 0 & a_{00} & 0 \\ -a_{30} & 0 & 0 & a_{00} \end{pmatrix} \quad (6.21)$$

The next step of the Gaussian elimination process involves dividing the second row of the matrix by its second element $b_{11}$ and then subtracting appropriate multiples from lower rows. This too can be represented as a matrix multiplication:

$$\frac{1}{b_{11}}\begin{pmatrix} b_{11} & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & -b_{21} & b_{11} & 0 \\ 0 & -b_{31} & 0 & b_{11} \end{pmatrix} \begin{pmatrix} 1 & b_{01} & b_{02} & b_{03} \\ 0 & b_{11} & b_{12} & b_{13} \\ 0 & b_{21} & b_{22} & b_{23} \\ 0 & b_{31} & b_{32} & b_{33} \end{pmatrix} = \begin{pmatrix} 1 & c_{01} & c_{02} & c_{03} \\ 0 & 1 & c_{12} & c_{13} \\ 0 & 0 & c_{22} & c_{23} \\ 0 & 0 & c_{32} & c_{33} \end{pmatrix} \quad (6.22)$$

Again, note that the matrix we are multiplying by—call it $\mathbf{L}_1$—is lower triangular:

$$\mathbf{L}_1 = \frac{1}{b_{11}}\begin{pmatrix} b_{11} & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & -b_{21} & b_{11} & 0 \\ 0 & -b_{31} & 0 & b_{11} \end{pmatrix} \quad (6.23)$$

For the $4 \times 4$ example considered here, there are two more steps to the Gaussian elimination, which correspond to multiplying by the lower-triangular matrices

$$\mathbf{L}_2 = \frac{1}{c_{22}}\begin{pmatrix} c_{22} & 0 & 0 & 0 \\ 0 & c_{22} & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & -c_{32} & c_{22} \end{pmatrix}, \quad \mathbf{L}_3 = \frac{1}{d_{33}}\begin{pmatrix} d_{33} & 0 & 0 & 0 \\ 0 & d_{33} & 0 & 0 \\ 0 & 0 & d_{33} & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \quad (6.24)$$

where $d_{33}$ is defined in the obvious way.

Putting the whole process together, the complete Gaussian elimination on the matrix $\mathbf{A}$ is equivalent to multiplying the matrix in succession by $\mathbf{L}_0, \mathbf{L}_1, \mathbf{L}_2,$ and $\mathbf{L}_3$. Or, to put that another way, the matrix $\mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{A}$ must be upper triangular, since it is the end product of a Gaussian elimination process. Knowing this it is now easy to see how we solve our original set of equations $\mathbf{Ax} = \mathbf{v}$ for the unknown vector $\mathbf{x}$. We multiply on both sides by $\mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0$ to get

$$\mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{Ax} = \mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{v} \quad (6.25)$$

All the quantities on the right are known, so we can perform the multiplications and get a vector. On the left we have an upper-triangular matrix times $\mathbf{x}$. So our equation is now in the form of Eq. (6.10), which can be solved easily by backsubstitution.

This approach is, mathematically speaking, entirely equivalent to the Gaussian elimination of earlier sections. Practically speaking, however, it has the significant advantage that the matrices $\mathbf{L}_0$ to $\mathbf{L}_3$ encapsulate the entire sequence of transformations performed during the elimination process, which allows us to efficiently solve sets of equations with the same matrix $\mathbf{A}$ but different right-hand sides $\mathbf{v}$. Every such set involves solving Eq. (6.25) for a different vector $\mathbf{v}$ but the matrix $\mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{A}$ on the left is the same every time, so we only need to calculate it once. Since calculating the matrix is the most time-consuming part of the Gaussian elimination process, this simplification can speed up our program enormously. Once we have the matrices $\mathbf{L}_0$ to $\mathbf{L}_3$, the only thing we need to do on being handed a new vector $\mathbf{v}$ is multiply to get $\mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{v}$, then apply backsubstitution to the result.

This is, in essence the entire LU decomposition method. It's just a version of Gaussian elimination expressed in terms of matrices. However, in practice the calculations are usually performed in a slightly different way that is a little simpler and more convenient than the way described here. We define the matrices

$$\mathbf{L} = \mathbf{L}_0^{-1}\mathbf{L}_1^{-1}\mathbf{L}_2^{-1}\mathbf{L}_3^{-1}, \quad \mathbf{U} = \mathbf{L}_3\mathbf{L}_2\mathbf{L}_1\mathbf{L}_0\mathbf{A} \quad (6.26)$$

Note that $\mathbf{U}$ is just the matrix on the left-hand side of Eq. (6.25), which is upper triangular (hence the name $\mathbf{U}$). Multiplying these two matrices together we get

$$\mathbf{LU} = \mathbf{A} \quad (6.27)$$

and hence the set of equations $\mathbf{Ax} = \mathbf{v}$ can also be written as

$$\mathbf{LUx} = \mathbf{v} \quad (6.28)$$

The nice thing about this form is that not only is $\mathbf{U}$ upper triangular, but $\mathbf{L}$ is also lower triangular. In fact $\mathbf{L}$ has a very simple form. Consider the matrix $\mathbf{L}_0$:

$$\mathbf{L}_0 = \frac{1}{a_{00}}\begin{pmatrix} 1 & 0 & 0 & 0 \\ -a_{10} & a_{00} & 0 & 0 \\ -a_{20} & 0 & a_{00} & 0 \\ -a_{30} & 0 & 0 & a_{00} \end{pmatrix} \quad (6.29)$$

It takes only a moment to confirm that the inverse of this matrix is

$$\mathbf{L}_0^{-1} = \begin{pmatrix} a_{00} & 0 & 0 & 0 \\ a_{10} & 1 & 0 & 0 \\ a_{20} & 0 & 1 & 0 \\ a_{30} & 0 & 0 & 1 \end{pmatrix} \quad (6.30)$$

which is also lower triangular. Similarly the inverses of the other matrices are

$$\mathbf{L}_1^{-1} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & b_{11} & 0 & 0 \\ 0 & b_{21} & 1 & 0 \\ 0 & b_{31} & 0 & 1 \end{pmatrix}, \quad \mathbf{L}_2^{-1} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & c_{22} & 0 \\ 0 & 0 & c_{32} & 1 \end{pmatrix}, \quad \mathbf{L}_3^{-1} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & d_{33} \end{pmatrix} \quad (6.31)$$

Multiplying them all together, we find that

$$\mathbf{L} = \mathbf{L}_0^{-1}\mathbf{L}_1^{-1}\mathbf{L}_2^{-1}\mathbf{L}_3^{-1} = \begin{pmatrix} a_{00} & 0 & 0 & 0 \\ a_{10} & b_{11} & 0 & 0 \\ a_{20} & b_{21} & c_{22} & 0 \\ a_{30} & b_{31} & c_{32} & d_{33} \end{pmatrix} \quad (6.32)$$

Thus, not only is $\mathbf{L}$ lower triangular, but its value is easy to calculate from numbers we already know.

Equation (6.27) is called the **LU decomposition** of the matrix $\mathbf{A}$. It tells us that $\mathbf{A}$ is equal to a product of two matrices, the first being lower triangular and the second being upper triangular.

Once we have the LU decomposition of $\mathbf{A}$ we can use it to solve $\mathbf{Ax} = \mathbf{v}$ directly. Here's how the process goes for a $3 \times 3$ example. The LU decomposition of $\mathbf{A}$ looks like this in general:

$$\mathbf{A} = \begin{pmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \\ a_{20} & a_{21} & a_{22} \end{pmatrix} = \begin{pmatrix} l_{00} & 0 & 0 \\ l_{10} & l_{11} & 0 \\ l_{20} & l_{21} & l_{22} \end{pmatrix} \begin{pmatrix} u_{00} & u_{01} & u_{02} \\ 0 & u_{11} & u_{12} \\ 0 & 0 & u_{22} \end{pmatrix} \quad (6.33)$$

Then our set of simultaneous equations takes the form

$$\begin{pmatrix} l_{00} & 0 & 0 \\ l_{10} & l_{11} & 0 \\ l_{20} & l_{21} & l_{22} \end{pmatrix} \begin{pmatrix} u_{00} & u_{01} & u_{02} \\ 0 & u_{11} & u_{12} \\ 0 & 0 & u_{22} \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} = \begin{pmatrix} v_0 \\ v_1 \\ v_2 \end{pmatrix} \quad (6.34)$$

Now let us define a new vector $\mathbf{y}$ according to

$$\begin{pmatrix} u_{00} & u_{01} & u_{02} \\ 0 & u_{11} & u_{12} \\ 0 & 0 & u_{22} \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} = \begin{pmatrix} y_0 \\ y_1 \\ y_2 \end{pmatrix} \quad (6.35)$$

In terms of this vector, our equation (6.34) becomes

$$\begin{pmatrix} l_{00} & 0 & 0 \\ l_{10} & l_{11} & 0 \\ l_{20} & l_{21} & l_{22} \end{pmatrix} \begin{pmatrix} y_0 \\ y_1 \\ y_2 \end{pmatrix} = \begin{pmatrix} v_0 \\ v_1 \\ v_2 \end{pmatrix} \quad (6.36)$$

Thus we have broken our original problem down into two separate matrix problems, Eqs. (6.35) and (6.36). If we can solve (6.36) for $\mathbf{y}$ given $\mathbf{v}$ then we can substitute the answer into (6.35) and solve to get a solution for $\mathbf{x}$.

But both of these two new problems involves only a triangular matrix, not a full matrix and, as we saw in Section 6.1.2, such equations are easy to solve by backsubstitution. For instance, Eq. (6.36) can be solved for $\mathbf{y}$ by noting that the first line of the equation implies $l_{00}y_0 = v_0$, or

$$y_0 = \frac{v_0}{l_{00}} \quad (6.37)$$

Then the second line gives us $l_{10}y_0 + l_{11}y_1 = v_1$, or

$$y_1 = \frac{v_1 - l_{10}y_0}{l_{11}} \quad (6.38)$$

and the third line gives us

$$y_2 = \frac{v_2 - l_{20}y_0 - l_{21}y_1}{l_{22}} \quad (6.39)$$

and so we have all the elements of $\mathbf{y}$. Now we take these values, substitute them into Eq. (6.35), and then use a similar backsubstitution procedure to solve for the elements of $\mathbf{x}$, which gives us our final solution.

This LU decomposition method is the most commonly used form of Gaussian elimination, and indeed the most commonly used method for solving simultaneous equations altogether. To avoid problems with small or zero diagonal elements, one must in general also incorporate pivoting, as discussed in Section 6.1.3, but this is straightforward to do. The standard method for solving equations then breaks down into two separate operations, the LU decomposition of the matrix $\mathbf{A}$ with partial pivoting, followed by the double backsubstitution process above to recover the final solution. For solving multiple sets of equations with the same matrix $\mathbf{A}$ the LU decomposition need be performed only once, and only the backsubstitutions need be repeated for each individual set. Exercise 6.3 invites you to try your hand at writing a program to solve simultaneous equations using this method, and you are encouraged to give it a go.

Solving simultaneous equations, however, is such a common operation, both in physics and elsewhere, that you don't need to write your own program to do it if you don't want to. Many programs to do the calculation have already been written by other people. Professionally written programs to perform LU decomposition and solve equations exist in most computer languages, including Python, and there is no reason not to use them when they're available.

It might seem like cheating to use a program written by someone else to solve a problem, but in many cases it's actually an excellent idea. Of course, it can be a very good exercise to write your own program. You can learn a lot, both about physics and about programming, by doing so. And there is no shortage of hard physics problems where no one has written a program yet and you'll have no choice but to do it yourself. But in the cases where a program is already available you shouldn't feel bad about using it.

In Python, functions for solving simultaneous equations are provided by the module `linalg` which is found in the `numpy` package. In particular, the module contains a function `solve`, which solves systems of linear equations of the form $\mathbf{Ax} = \mathbf{v}$ using LU decomposition and backsubstitution. You need only import the function then use it like this:

```python
from numpy.linalg import solve
x = solve(A, v)
```

In most cases, if you need to solve a large system of equations (or even a small one) in Python, this is the simplest and quickest way to get an answer. There are also functions that perform the LU decomposition step separately from the backsubstitution, so that you can efficiently solve multiple sets of equations, as described above. We will not need these separate functions in this book, but if you wish to learn about them you can find more information at www.scipy.org.

---

**Exercise 6.3: LU decomposition**

This exercise invites you to write your own program to solve simultaneous equations using the method of LU decomposition.

a) Starting, if you wish, with the program for Gaussian elimination in Example 6.1 on page 218, write a Python function that calculates the LU decomposition of a matrix. The calculation is same as that for Gaussian elimination, except that at each step of the calculation you need to extract the appropriate elements of the matrix and assemble them to form the lower diagonal matrix $\mathbf{L}$ of Eq. (6.32). Test your function by calculating the LU decomposition of the matrix from Eq. (6.2), then multiplying the $\mathbf{L}$ and $\mathbf{U}$ you get and verifying that you recover the original matrix once more.

b) Build on your LU decomposition function to create a complete program to solve Eq. (6.2) by performing a double backsubstitution as described in this section. Solve the same equations using the function `solve` from the `numpy` package and verify that you get the same answer either way.

c) If you're feeling ambitious, try your hand at LU decomposition with partial pivoting. Partial pivoting works in the same way for LU decomposition as it does for Gaussian elimination, swapping rows to get the largest diagonal element as explained in Section 6.1.3, but the extension to LU decomposition requires two additional steps. First, every time you swap two rows you also have to swap the same rows in the matrix $\mathbf{L}$. Second, when you use your LU decomposition to solve a set of equations $\mathbf{Ax} = \mathbf{v}$ you will also need to perform the same sequence of swaps on the vector $\mathbf{v}$ on the right-hand side. This means you need to record the swaps as you are doing the decomposition so that you can recreate them later. The simplest way to do this is to set up a list or array in which the value of the $i$th element records the row you swapped with on the $i$th step of the process. For instance, if you swapped the first row with the second then the second with the fourth, the first two elements of the list would be 2 and 4. Solving a set of equations for given $\mathbf{v}$ involves first performing the required sequence of swaps on the elements of $\mathbf{v}$ then performing a double backsubstitution as usual. (In ordinary Gaussian elimination with pivoting, one swaps the elements of $\mathbf{v}$ as the algorithm proceeds, rather than all at once, but the difference has no effect on the results, so it's fine to perform all the swaps at once if we wish.)

Modify the function you wrote for part (a) to perform LU decomposition with partial pivoting. The function should return the matrices $\mathbf{L}$ and $\mathbf{U}$ for the LU decomposition of the swapped matrix, plus a list of the swaps made. Then modify the rest of your program to solve equations of the form $\mathbf{Ax} = \mathbf{v}$ using LU decomposition with pivoting. Test your program on the example from Eq. (6.17), which cannot be solved without pivoting because of the zero in the first element of the matrix. Check your results against a solution of the same equations using the `solve` function from `numpy`.

LU decomposition with partial pivoting is the most widely used method for the solution of simultaneous equations in practice. Precisely this method is used in the function `solve` from the `numpy` package. There's nothing wrong with using the `solve` function—it's well written, fast, and convenient. But it does nothing you haven't already done yourself if you've solved this exercise.

**Exercise 6.4:** Write a program to solve the resistor network problem of Exercise 6.1 on page 220 using the function `solve` from `numpy.linalg`. If you also did Exercise 6.1, you should check that you get the same answer both times.

**Exercise 6.5:** Here's a more complicated circuit problem:

[Diagram of RC circuit with resistors R₁-R₆ and capacitors C₁, C₂]

The voltage $V_+$ is time-varying and sinusoidal of the form $V_+ = x_+e^{i\omega t}$ with $x_+$ a constant. (The voltage is actually real, of course, but things are made simpler by treating it as complex, as is common in circuit calculations.) The resistors in the circuit can be treated using Ohm's law as usual. For the capacitors the charge $Q$ and voltage $V$ across them are related by the capacitor law $Q = CV$, where $C$ is the capacitance. Differentiating both sides of this expression gives the current $I$ flowing in on one side of the capacitor and out on the other:

$$I = \frac{dQ}{dt} = C\frac{dV}{dt}.$$

a) Assuming the voltages at the points labeled 1, 2, and 3 are of the form $V_1 = x_1e^{i\omega t}$, $V_2 = x_2e^{i\omega t}$, and $V_3 = x_3e^{i\omega t}$, apply Kirchhoff's law at each of the three points, along with Ohm's law and the capacitor law, to show that the constants $x_1, x_2,$ and $x_3$ satisfy the equations

$$\left(\frac{1}{R_1} + \frac{1}{R_4} + i\omega C_1\right)x_1 - i\omega C_1 x_2 = \frac{x_+}{R_1},$$
$$-i\omega C_1 x_1 + \left(\frac{1}{R_2} + \frac{1}{R_5} + i\omega C_1 + i\omega C_2\right)x_2 - i\omega C_2 x_3 = \frac{x_+}{R_2},$$
$$-i\omega C_2 x_2 + \left(\frac{1}{R_3} + \frac{1}{R_6} + i\omega C_2\right)x_3 = \frac{x_+}{R_3}.$$

b) Write a program to solve for $x_1, x_2,$ and $x_3$ when
- $R_1 = R_3 = R_5 = 1\text{ k}\Omega$
- $R_2 = R_4 = R_6 = 2\text{ k}\Omega$
- $C_1 = 1\mu\text{F}, \quad C_2 = 0.5\mu\text{F}$
- $x_+ = 3\text{ V}, \quad \omega = 1000\text{ s}^{-1}$

Notice that the matrix for this problem has complex elements. You will need to define a complex array to hold it, but you can still use the `solve` function just as before to solve the equations—it works with either real or complex arguments. Using your solution have your program calculate and print the amplitudes of the three voltages $V_1, V_2,$ and $V_3$ and their phases in degrees. (Hint: You may find the functions `polar` or `phase` in the `cmath` package useful. If $z$ is a complex number then "`r,theta = polar(z)`" will return the modulus and phase (in radians) of $z$ and "`theta = phase(z)`" will return the phase alone.)

### 6.1.5 Calculating the Inverse of a Matrix

As we said at the beginning of the chapter, one can solve equations of the form $\mathbf{Ax} = \mathbf{v}$ by multiplying on both sides by the inverse of $\mathbf{A}$, but this is not a very efficient way to do the calculation. Gaussian elimination or LU decomposition is faster. But what if we wanted to know the inverse of a matrix for some other reason? In fact, it's rare in physics problems that we need to do this, but just suppose for a moment that we do. How could we find the inverse?

One way to calculate a matrix inverse—the way most of us are taught in our linear algebra classes—is to compute a matrix of cofactors and divide it by the determinant. However, as with several of the problems we've examined in this book, the obvious approach is not always the best, and this method of calculating an inverse is typically quite slow and can be subject to large rounding errors. A better approach is to turn the problem of inverting the matrix into a problem of solving a set of simultaneous equations, then tackle that problem using the methods we have already seen.

Consider the form

$$\mathbf{AX} = \mathbf{V} \quad (6.40)$$

which is the same as before, except that $\mathbf{X}$ and $\mathbf{V}$ are $N \times N$ matrices now, not just single vectors. We can solve this equation in the same way as we did previously, using either Gaussian elimination or LU decomposition to reduce the matrix $\mathbf{A}$ to a simpler form, then solving for the elements of $\mathbf{X}$ by backsubstitution. You have to solve for each column of $\mathbf{X}$ separately, in terms of the corresponding column of $\mathbf{V}$, but in principle the calculation is just the same as the one we did before.

But now suppose we choose the value of $\mathbf{V}$ to be the identity matrix $\mathbf{I}$, so that $\mathbf{AX} = \mathbf{I}$. Then, by definition, the value of $\mathbf{X}$ is $\mathbf{A}^{-1}$, which is the inverse that we want. So when we find the solution with this choice of $\mathbf{V}$ we get the inverse of $\mathbf{A}$.

Thus, for instance, we could use the function `solve` from the `numpy.linalg` module to solve for the columns of $\mathbf{X}$ and so invert a matrix $\mathbf{A}$. This, however, is a bit cumbersome, so there is a separate function in `numpy.linalg` called `inv` that does the calculation for us in one step. To use it we simply say

```python
from numpy.linalg import inv
X = inv(A)
```

which sets $\mathbf{X}$ equal to the value of the inverse.

As we've said, however, we don't often need the inverse in physics calculations, and indeed we will not need it for any of the calculations we do in this book, so let us move on to other things.

### 6.1.6 Tridiagonal and Banded Matrices

A special case that arises often in physics problems is the solution of $\mathbf{Ax} = \mathbf{v}$ when the matrix $\mathbf{A}$ is **tridiagonal**, thus:

$$\mathbf{A} = \begin{pmatrix} a_{00} & a_{01} & & & \\ a_{10} & a_{11} & a_{12} & & \\ & a_{21} & a_{22} & a_{23} & \\ & & a_{32} & a_{33} & a_{34} \\ & & & a_{43} & a_{44} \end{pmatrix} \quad (6.41)$$

Here all the elements not shown are zero. That is, the matrix has nonzero elements only along the diagonal and immediately above and below it. This is a case where simple Gaussian elimination is a good choice for solving the problem—it works quickly, and pivoting is typically not used so the programming is straightforward.

The point to notice about tridiagonal problems is that we don't need to go through the entire Gaussian elimination procedure to solve them. Each row only needs to be subtracted from the single row immediately below it—and not all lower rows—to make the matrix triangular. Suppose, for instance, we have a $4 \times 4$ matrix of the form

$$\mathbf{A} = \begin{pmatrix} 2 & 1 & 0 & 0 \\ 3 & 4 & -5 & 0 \\ 0 & -4 & 3 & 5 \\ 0 & 0 & 1 & 3 \end{pmatrix} \quad (6.42)$$

The initial step of our Gaussian elimination would be to divide the first row of the matrix by 2, then subtract 3 times the result from the second row, which would give a new matrix

$$\begin{pmatrix} 1 & 0.5 & 0 & 0 \\ 0 & 2.5 & -5 & 0 \\ 0 & -4 & 3 & 5 \\ 0 & 0 & 1 & 3 \end{pmatrix} \quad (6.43)$$

Note that the first column now has the required form $1, 0, 0, 0$. Next we would divide the second row by 2.5 and subtract $-4$ times the result from the third row, to get

$$\begin{pmatrix} 1 & 0.5 & 0 & 0 \\ 0 & 1 & -2 & 0 \\ 0 & 0 & -5 & 5 \\ 0 & 0 & 1 & 3 \end{pmatrix} \quad (6.44)$$

Then we divide the third row by $-5$ and subtract it from the fourth to get

$$\begin{pmatrix} 1 & 0.5 & 0 & 0 \\ 0 & 1 & -2 & 0 \\ 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & 4 \end{pmatrix} \quad (6.45)$$

Finally we divide the last row by 4:

$$\begin{pmatrix} 1 & 0.5 & 0 & 0 \\ 0 & 1 & -2 & 0 \\ 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & 1 \end{pmatrix} \quad (6.46)$$

In the process we have reduced our matrix to upper-triangular form and we can now use back substitution to find the solution for $\mathbf{x}$.

The backsubstitution process is also simplified by the tridiagonal form. After the Gaussian elimination is complete we are left with an equation of the general form

$$\begin{pmatrix} 1 & a_{01} & 0 & 0 \\ 0 & 1 & a_{12} & 0 \\ 0 & 0 & 1 & a_{23} \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} v_0 \\ v_1 \\ v_2 \\ v_3 \end{pmatrix} \quad (6.47)$$

which has the simple solution

$$x_3 = v_3 \quad (6.48a)$$
$$x_2 = v_2 - a_{23}x_3 \quad (6.48b)$$
$$x_1 = v_1 - a_{12}x_2 \quad (6.48c)$$
$$x_0 = v_0 - a_{01}x_1 \quad (6.48d)$$

When used in this way, Gaussian elimination is sometimes called the **tridiagonal matrix algorithm** or the **Thomas algorithm**. You can also solve tridiagonal problems using general solution methods like those in the function `solve` from `numpy.linalg`, but doing so will usually be slower than the Thomas algorithm, because those methods do not take take advantage of the shortcuts we have used here to simplify the calculation. Indeed for large matrices using `solve` can be *much* slower, so the Thomas algorithm is usually the right way to go with large tridiagonal matrices.

A related issue comes up when the matrix $\mathbf{A}$ is **banded**, meaning that it is similar to a tridiagonal matrix but can have more than one nonzero element to either side of the diagonal, like this:

$$\mathbf{A} = \begin{pmatrix} a_{00} & a_{01} & a_{02} & & & & \\ a_{10} & a_{11} & a_{12} & a_{13} & & & \\ a_{20} & a_{21} & a_{22} & a_{23} & a_{24} & & \\ & a_{31} & a_{32} & a_{33} & a_{34} & a_{35} & \\ & & a_{42} & a_{43} & a_{44} & a_{45} & a_{46} \\ & & & a_{53} & a_{54} & a_{55} & a_{56} \\ & & & & a_{64} & a_{65} & a_{66} \end{pmatrix} \quad (6.49)$$

Problems containing banded matrices can be solved in the same way as for the tridiagonal case, using Gaussian elimination. If there are $m$ nonzero elements below the diagonal then each row must now be subtracted from the $m$ rows below it, and not just from one single row. And the equations for the backsubstitution are more complex, involving terms for each of the nonzero rows above the diagonal. These differences make the solution process slower, but it can still be much faster than using the `solve` function from `numpy.linalg`.

**Example 6.2: Vibration in a One-Dimensional System**

Suppose we have a set of $N$ identical masses in a row, joined by identical linear springs, thus:

[Diagram of masses connected by springs]

For simplicity, we'll ignore gravity—the masses and springs are floating in outer space. If we jostle this system the masses will vibrate relative to one another under the action of the springs. The motions of the system could be used as a model of the vibration of atoms in a solid, which can be represented with reasonable accuracy in exactly this way. Here we examine the modes of horizontal vibration of the system.

Let us denote the displacement of the $i$th mass relative to its rest position by $\xi_i$. Then the equations of motion for the system are given by Newton's second law:

$$m\frac{d^2\xi_i}{dt^2} = k(\xi_{i+1} - \xi_i) + k(\xi_{i-1} - \xi_i) + F_i \quad (6.50)$$

where $m$ is the mass and $k$ is the spring constant. The left-hand side of this equation is just mass times acceleration, while the right-hand side is the force on mass $i$ due to the springs connecting it to the two adjacent masses, plus an extra term $F_i$ that represents any external force imposed on mass $i$. The only exceptions to Eq. (6.50) are for the masses at the two ends of the line, for which there is only one spring force each, so that they obey the equations

$$m\frac{d^2\xi_1}{dt^2} = k(\xi_2 - \xi_1) + F_1 \quad (6.51)$$
$$m\frac{d^2\xi_N}{dt^2} = k(\xi_{N-1} - \xi_N) + F_N \quad (6.52)$$

Now suppose we drive our system by applying a harmonic (i.e., sinusoidal) force to the first mass: $F_1 = Ce^{i\omega t}$, where $C$ is a constant and we use a complex form, as one commonly does in such cases, on the understanding that we will take the real part at the end of the calculation. If we are thinking of this as a model of atoms in a solid, such a force could be created by the charge of the atoms interacting with a varying electric field, such as would be produced by an electromagnetic wave falling on the solid.

The net result of the applied force will be to make all the atoms oscillate in some fashion with angular frequency $\omega$, so that the overall solution for the positions of the atoms will take the form

$$\xi_i(t) = x_i e^{i\omega t} \quad (6.53)$$

for all $i$. The magnitude of the quantity $x_i$ controls the amplitude of vibration of mass $i$ and its phase controls the phase of the vibration relative to the driving force.

Substituting Eq. (6.53) into Eqs. (6.50) to (6.52) we find that

$$-m\omega^2 x_1 = k(x_2 - x_1) + C \quad (6.54a)$$
$$-m\omega^2 x_i = k(x_{i+1} - x_i) + k(x_{i-1} - x_i) \quad (6.54b)$$
$$-m\omega^2 x_N = k(x_{N-1} - x_N) \quad (6.54c)$$

where (6.54b) applies for all $i$ in the range $2 \leq i \leq N-1$. These equations can be rearranged to read

$$(\alpha - k)x_1 - kx_2 = C \quad (6.55a)$$
$$\alpha x_i - kx_{i-1} - kx_{i+1} = 0 \quad (6.55b)$$
$$(\alpha - k)x_N - kx_{N-1} = 0 \quad (6.55c)$$

where $\alpha = 2k - m\omega^2$. Thus in matrix form we have:

$$\begin{pmatrix} (\alpha-k) & -k & & & \\ -k & \alpha & -k & & \\ & -k & \alpha & -k & \\ & & \ddots & \ddots & \ddots \\ & & & -k & \alpha & -k \\ & & & & -k & (\alpha-k) \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \\ \vdots \\ x_{N-1} \\ x_N \end{pmatrix} = \begin{pmatrix} C \\ 0 \\ 0 \\ \vdots \\ 0 \\ 0 \end{pmatrix} \quad (6.56)$$

This is precisely a tridiagonal set of simultaneous equations of the type we have been considering in this section, which we can solve by Gaussian elimination. Note that even though we employed a complex form for the driving force, the equations above are entirely real and hence their solution will also be real. So it is safe to write a program to solve them using real variables only. (We could choose $C$ complex, but this simply multiplies the entire solution by a constant phase factor, so it doesn't give us any new behavior.)

Here is a program to solve the problem for the case where $N = 26$, $C = 1$, $m = 1$, $k = 6$, and $\omega = 2$, so that $\alpha = 8$. The program calculates all the $x_i$ then makes a graph of the values, which reflect the amplitudes of the oscillating masses.

```python
from numpy import zeros, empty
from pylab import plot, show

# Constants
N = 26
C = 1.0
m = 1.0
k = 6.0
omega = 2.0
alpha = 2*k - m*omega*omega

# Set up the initial values of the arrays
A = zeros([N, N], float)
for i in range(N-1):
    A[i, i] = alpha
    A[i, i+1] = -k
    A[i+1, i] = -k

A[0, 0] = alpha - k
A[N-1, N-1] = alpha - k
v = zeros(N, float)
v[0] = C

# Perform the Gaussian elimination
for i in range(N-1):
    # Divide row i by its diagonal element
    A[i, i+1] /= A[i, i]
    v[i] /= A[i, i]
    
    # Now subtract it from the next row down
    A[i+1, i+1] -= A[i+1, i] * A[i, i+1]
    v[i+1] -= A[i+1, i] * v[i]

# Divide the last element of v by the last diagonal element
v[N-1] /= A[N-1, N-1]

# Backsubstitution
x = empty(N, float)
x[N-1] = v[N-1]
for i in range(N-2, -1, -1):
    x[i] = v[i] - A[i, i+1] * x[i+1]

# Make a plot using both dots and lines
plot(x)
plot(x, "ko")
show()
```

Note that in this case we did not make use of Python's array processing abilities to perform operations on entire rows of the matrix in a single step. Each row that we work with has only two nonzero elements, so it makes no sense to divide, multiply, or subtract entire rows—it's quicker to explicitly manipulate just the two nonzero elements and leave all the others alone. We also did not bother to set the diagonal elements of the matrix to one or the elements below the diagonal to zero. We know that they will end up with these values, but the values are not needed in the backsubstitution process, so we can save ourselves a little effort, and make a simpler program, by leaving these elements as they are.

Figure 6.1 shows the plot produced by the program. As we can see, the amplitude of motion of the masses varies in a wave along the length of the chain, with some masses vibrating vigorously while others remain almost stationary. This is the classic form of a standing wave in a driven spatial system, and it's not a bad model for what happens when we excite vibrations in the atoms of a solid.

The solution of tridiagonal or banded systems of equations is a relatively common operation in computational physics, so it would be a good candidate for a user-defined function, similar to the function `solve` in the module `numpy.linalg`, which solves general linear systems of equations as discussed in Section 6.1.4. One would have to write such a function only once and then one could use it whenever one wanted to solve banded systems. Such a function, called `banded`, is provided in Appendix E and can be found in the file `banded.py` in the on-line resources. This function will come in handy for a number of later problems that involve the solution of tridiagonal or banded systems. As an example, here is how we would use it to solve the problem of the masses and springs above:

```python
from numpy import empty, zeros
from banded import banded
from pylab import plot, show

# Constants
N = 26
C = 1.0
m = 1.0
k = 6.0
omega = 2.0
alpha = 2*k - m*omega*omega

# Set up the initial values of the arrays
A = empty([3, N], float)
A[0, :] = -k
A[1, :] = alpha
A[2, :] = -k
A[1, 0] = alpha - k
A[1, N-1] = alpha - k
v = zeros(N, float)
v[0] = C

# Solve the equations
x = banded(A, v, 1, 1)

# Make a plot using both dots and lines
plot(x)
plot(x, "ko")
show()
```

Unsurprisingly, this program produces a plot identical to Fig. 6.1. For more details of how the `banded` function is used, particularly the special format used for the matrix $\mathbf{A}$, take a look at Appendix E.

---

**Exercise 6.6:** Starting with either the program `springs.py` on page 237 or the program `springsb.py` above, remove the code that makes a graph of the results and replace it with code that creates an animation of the masses as they vibrate back and forth, their displacements relative to their resting positions being given by the real part of Eq. (6.53). For clarity, assume that the resting positions are two units apart in a horizontal line. At a minimum your animation should show each of the individual masses, perhaps as small spheres. (Spheres of radius about 0.2 or 0.3 seem to work well.)

**Exercise 6.7: A chain of resistors**

Consider a long chain of resistors wired up like this:

[Diagram of resistor ladder network]

All the resistors have the same resistance $R$. The power rail at the top is at voltage $V_+ = 5$V. The problem is to find the voltages $V_1 \ldots V_N$ at the internal points in the circuit.

a) Using Ohm's law and the Kirchhoff current law, which says that the total net current flow out of (or into) any junction in a circuit must be zero, show that the voltages $V_1 \ldots V_N$ satisfy the equations

$$3V_1 - V_2 - V_3 = V_+$$
$$-V_1 + 4V_2 - V_3 - V_4 = V_+$$
$$\vdots$$
$$-V_{i-2} - V_{i-1} + 4V_i - V_{i+1} - V_{i+2} = 0$$
$$\vdots$$
$$-V_{N-3} - V_{N-2} + 4V_{N-1} - V_N = 0$$
$$-V_{N-2} - V_{N-1} + 3V_N = 0$$

Express these equations in vector form $\mathbf{Av} = \mathbf{w}$ and find the values of the matrix $\mathbf{A}$ and the vector $\mathbf{w}$.

b) Write a program to solve for the values of the $V_i$ when there are $N = 6$ internal junctions with unknown voltages. (Hint: All the values of $V_i$ should lie between zero and 5V. If they don't, something is wrong.)

c) Now repeat your calculation for the case where there are $N = 10\,000$ internal junctions. This part is not possible using standard tools like the `solve` function. You need to make use of the fact that the matrix $\mathbf{A}$ is banded and use the `banded` function from the file `banded.py`, discussed in Appendix E.

## 6.2 Eigenvalues and Eigenvectors

Another common matrix problem that arises in physics is the calculation of the eigenvalues and/or eigenvectors of a matrix. This problem arises in classical mechanics, quantum mechanics, electromagnetism, and other areas. Most eigenvalue problems in physics concern real symmetric matrices (or Hermitian matrices when complex numbers are involved, such as in quantum mechanics). For a symmetric matrix $\mathbf{A}$, an eigenvector $\mathbf{v}$ is a vector satisfying

$$\mathbf{Av} = \lambda\mathbf{v} \quad (6.57)$$

where $\lambda$ is the corresponding eigenvalue. For an $N \times N$ matrix there are $N$ eigenvectors $\mathbf{v}_1 \ldots \mathbf{v}_N$ with eigenvalues $\lambda_1 \ldots \lambda_N$. The eigenvectors have the property that they are orthogonal to one another $\mathbf{v}_i \cdot \mathbf{v}_j = 0$ if $i \neq j$, and we will assume they are normalized to have unit length $\mathbf{v}_i \cdot \mathbf{v}_i = 1$ (although this is merely conventional, since Eq. (6.57) itself doesn't fix the normalization).

If we wish, we can consider the eigenvectors to be the columns of a single $N \times N$ matrix $\mathbf{V}$ and combine all the equations $\mathbf{Av}_i = \lambda_i\mathbf{v}_i$ into a single matrix equation

$$\mathbf{AV} = \mathbf{VD} \quad (6.58)$$

where $\mathbf{D}$ is the diagonal matrix with the eigenvalues $\lambda_i$ as its diagonal entries. Notice that the matrix $\mathbf{V}$ is orthogonal, meaning that its transpose $\mathbf{V}^T$ is equal to its inverse, so that $\mathbf{V}^T\mathbf{V} = \mathbf{VV}^T = \mathbf{I}$, the identity matrix.

The most widely used technique for calculating eigenvalues and eigenvectors of real symmetric or Hermitian matrices on a computer is the **QR algorithm**, which we examine in this section. The QR algorithm works by calculating the matrices $\mathbf{V}$ and $\mathbf{D}$ that appear in Eq. (6.58). We'll look at the case where $\mathbf{A}$ is real and symmetric, although the Hermitian case is a simple extension.

The QR algorithm makes use of the **QR decomposition** of a matrix. In Section 6.1.4 we encountered the LU decomposition, which breaks a matrix into two parts, writing it as the product of a lower-triangular matrix $\mathbf{L}$ and an upper-triangular matrix $\mathbf{U}$. The QR decomposition is a variant on the same idea in which the matrix is written as the product $\mathbf{QR}$ of an **orthogonal** matrix $\mathbf{Q}$ and an upper-triangular matrix $\mathbf{R}$. Any square matrix can be written in this form and you'll have the opportunity shortly to write your own program to calculate QR decompositions (see Exercise 6.8), but for the moment let's just assume we have some way to calculate them.

Suppose we have a real, square, symmetric matrix $\mathbf{A}$ and let us break it down into its QR decomposition, which we'll write as

$$\mathbf{A} = \mathbf{Q}_1\mathbf{R}_1 \quad (6.59)$$

Multiplying on the left by $\mathbf{Q}_1^T$, we get

$$\mathbf{Q}_1^T\mathbf{A} = \mathbf{Q}_1^T\mathbf{Q}_1\mathbf{R}_1 = \mathbf{R}_1 \quad (6.60)$$

where we have made use of the fact that $\mathbf{Q}_1$ is orthogonal.

Now let us define a new matrix

$$\mathbf{A}_1 = \mathbf{R}_1\mathbf{Q}_1 \quad (6.61)$$

which is just the product of the same two matrices, but in the reverse order. Combining Eqs. (6.60) and (6.61), we have

$$\mathbf{A}_1 = \mathbf{Q}_1^T\mathbf{AQ}_1 \quad (6.62)$$

Now we repeat this process, forming the QR decomposition of the matrix $\mathbf{A}_1$, which we'll write as $\mathbf{A}_1 = \mathbf{Q}_2\mathbf{R}_2$, and defining a new matrix

$$\mathbf{A}_2 = \mathbf{R}_2\mathbf{Q}_2 = \mathbf{Q}_2^T\mathbf{A}_1\mathbf{Q}_2 = \mathbf{Q}_2^T\mathbf{Q}_1^T\mathbf{AQ}_1\mathbf{Q}_2 \quad (6.63)$$

And then we do it again, and again, repeatedly forming the QR decomposition of the current matrix, then multiplying $\mathbf{R}$ and $\mathbf{Q}$ in the opposite order to get a new matrix. If we do a total of $k$ steps, we generate the sequence of matrices

$$\mathbf{A}_1 = \mathbf{Q}_1^T\mathbf{AQ}_1 \quad (6.64)$$
$$\mathbf{A}_2 = \mathbf{Q}_2^T\mathbf{Q}_1^T\mathbf{AQ}_1\mathbf{Q}_2 \quad (6.65)$$
$$\mathbf{A}_3 = \mathbf{Q}_3^T\mathbf{Q}_2^T\mathbf{Q}_1^T\mathbf{AQ}_1\mathbf{Q}_2\mathbf{Q}_3 \quad (6.66)$$
$$\vdots$$
$$\mathbf{A}_k = (\mathbf{Q}_k^T \cdots \mathbf{Q}_1^T)\mathbf{A}(\mathbf{Q}_1 \cdots \mathbf{Q}_k) \quad (6.67)$$

It can be proven that if you continue this process long enough, the matrix $\mathbf{A}_k$ will eventually become diagonal. The off-diagonal entries of the matrix get smaller and smaller the more iterations of the process you do until they eventually reach zero—or as close to zero as makes no difference. Suppose we continue until we reach this point, the point where the off-diagonal elements become so small that, to whatever accuracy we choose, the matrix $\mathbf{A}_k$ approximates a diagonal matrix $\mathbf{D}$. Let us define the additional matrix

$$\mathbf{V} = \mathbf{Q}_1\mathbf{Q}_2\mathbf{Q}_3 \cdots \mathbf{Q}_k = \prod_{i=1}^k \mathbf{Q}_i \quad (6.68)$$

which is an orthogonal matrix, since a product of orthogonal matrices is always another orthogonal matrix. Then from Eq. (6.67) we have $\mathbf{D} = \mathbf{A}_k = \mathbf{V}^T\mathbf{AV}$, and, multiplying on the left by $\mathbf{V}$ we find that $\mathbf{AV} = \mathbf{VD}$. But this is precisely the definition of the eigenvalues and eigenvectors of $\mathbf{A}$, in the matrix form of Eq. (6.58). Thus, the columns of $\mathbf{V}$ are the eigenvectors of $\mathbf{A}$ and the diagonal elements of $\mathbf{D}$ are the corresponding eigenvalues (in the same order as the eigenvectors).

This is the QR algorithm for calculating eigenvalues and eigenvectors. Although we have described it in terms of the series of matrices $\mathbf{A}_k$, only the last of these matrices is actually needed for the eigenvalues, so in practice one doesn't retain all of the matrices (which could take up a lot of memory space), instead reusing a single array to store the matrix at each step. For a given $N \times N$ starting matrix $\mathbf{A}$, the complete algorithm is as follows:

1. Create an $N \times N$ matrix $\mathbf{V}$ to hold the eigenvectors and initially set it equal to the identity matrix $\mathbf{I}$. Also choose a target accuracy $\epsilon$ for the off-diagonal elements of the eigenvalue matrix.

2. Calculate the QR decomposition $\mathbf{A} = \mathbf{QR}$.

3. Update $\mathbf{A}$ to the new value $\mathbf{A} = \mathbf{RQ}$.

4. Multiply $\mathbf{V}$ on the right by $\mathbf{Q}$.

5. Check the off-diagonal elements of $\mathbf{A}$. If they are all less than $\epsilon$, we are done. Otherwise go back to step 2.

When the algorithm ends, the diagonal elements of $\mathbf{A}$ contain the eigenvalues and the columns of $\mathbf{V}$ contain the eigenvectors.

The QR algorithm is short and simple to describe. The only tricky part is calculating the QR decomposition itself, although even this is not very complicated. It can be done in a few lines in Python. Exercise 6.8 explains how to do it and invites you to write your own program to calculate the eigenvalues and eigenvectors of a matrix. It's a good exercise to write such a program, at least once, so you can see that it's really not a complicated calculation.

Most people, however, don't write their own programs to do the QR algorithm. Like the solution of simultaneous equations in Section 6.1.4, the problem of finding eigenvalues and eigenvectors is so common, both in physics and elsewhere, that others have already taken the time to write robust general-purpose programs for its solution. In Python the module `numpy.linalg` provides functions for solving eigenvalue problems. For instance, the function `eigh` calculates the eigenvalues and eigenvectors of a real symmetric or Hermitian matrix using the QR algorithm. Here's an example:

```python
from numpy import array
from numpy.linalg import eigh

A = array([[1, 2], [2, 1]], float)
x, V = eigh(A)
print(x)
print(V)
```

The function calculates the eigenvalues and eigenvectors of the matrix stored in the two-dimensional array `A` and returns two results, both also arrays. (We discussed functions that return more the one result in Section 2.6.) The first result returned is a one-dimensional array `x` containing the eigenvalues, while the second is a two-dimensional array `V` whose *columns* are the corresponding eigenvectors. If we run the program above, it produces the following output:

```
[-1.  3.]
[[-0.70710678  0.70710678]
 [ 0.70710678  0.70710678]]
```

Thus the program is telling us that the eigenvalues of the matrix are $-1$ and $3$ and the corresponding eigenvectors are $(-1, 1)/\sqrt{2}$ and $(1, 1)/\sqrt{2}$.

Sometimes we only want the eigenvalues of a matrix and not its eigenvectors, in which case we can save ourselves some time by not calculating the matrix of eigenvectors $\mathbf{V}$, Eq. (6.68). (This part of the calculation takes quite a lot of time because matrix multiplications involve a lot of operations, so it's a significant saving to skip this step.) The `numpy.linalg` module provides a separate function called `eigvalsh` that does this for symmetric or Hermitian matrices, calculating the eigenvalues alone, significantly faster than the function `eigh`. Here's an example:

```python
from numpy import array
from numpy.linalg import eigvalsh

A = array([[1, 2], [2, 1]], float)
x = eigvalsh(A)
print(x)
```

The function `eigvalsh` returns a single, one-dimensional array containing the eigenvalues. If we run this program it prints

```
[-1.  3.]
```

telling us again that the eigenvalues are $-1$ and $3$.

The functions `eigh` and `eigvalsh` are only for calculating the eigenvalues and eigenvectors of symmetric or Hermitian matrices. You might ask what happens if you provide an asymmetric matrix as argument to these functions? We might imagine the computer would give an error message, but in fact it does not. Instead it just ignores all elements of the matrix above the diagonal. It *assumes* that the elements above the diagonal are mirror images of the ones below and never even looks at their values. If they are not mirror images, the computer will never know, or care. It's as if the function copies the lower triangle of the matrix into the upper one before it does its calculation. You can if you wish leave the upper triangle blank—assign no values to these elements, or set them to zero. It will have no effect on the answer. In the program above we could have written

```python
A = array([[1, 0], [2, 1]], float)
x = eigvalsh(A)
```

and the answer would have been exactly the same.

If the matrix is complex instead of real, `eigh` and `eigvalsh` will assume it to be Hermitian and calculate the eigenvalues and eigenvectors accordingly. Again only the lower triangle matters: the upper triangle is assumed to be the complex conjugate of the lower one (and any imaginary part of the diagonal elements is ignored).

The module `linalg` does also supply functions for calculating eigenvalues and eigenvectors of nonsymmetric (or non-Hermitian) matrices: the functions `eig` and `eigvals` are the equivalents of `eigh` and `eigvalsh` when the matrix is nonsymmetric. We will not have call to use these functions in this book, however, and nonsymmetric eigenvalue problems come up only rarely in physics in general.

---

**Exercise 6.8: The QR algorithm**

In this exercise you'll write a program to calculate the eigenvalues and eigenvectors of a real symmetric matrix using the QR algorithm. The first challenge is to write a program that finds the QR decomposition of a matrix. Then we'll use that decomposition to find the eigenvalues.

As described above, the QR decomposition expresses a real square matrix $\mathbf{A}$ in the form $\mathbf{A} = \mathbf{QR}$, where $\mathbf{Q}$ is an orthogonal matrix and $\mathbf{R}$ is an upper-triangular matrix. Given an $N \times N$ matrix $\mathbf{A}$ we can compute the QR decomposition as follows.

Let us think of the matrix as a set of $N$ column vectors $\mathbf{a}_0 \ldots \mathbf{a}_{N-1}$ thus:

$$\mathbf{A} = \begin{pmatrix} | & | & | & \cdots \\ \mathbf{a}_0 & \mathbf{a}_1 & \mathbf{a}_2 & \cdots \\ | & | & | & \cdots \end{pmatrix}$$

where we have numbered the vectors in Python fashion, starting from zero, which will be convenient when writing the program. We now define two new sets of vectors $\mathbf{u}_0 \ldots \mathbf{u}_{N-1}$ and $\mathbf{q}_0 \ldots \mathbf{q}_{N-1}$ as follows:

$$\mathbf{u}_0 = \mathbf{a}_0, \quad \mathbf{q}_0 = \frac{\mathbf{u}_0}{|\mathbf{u}_0|}$$
$$\mathbf{u}_1 = \mathbf{a}_1 - (\mathbf{q}_0 \cdot \mathbf{a}_1)\mathbf{q}_0, \quad \mathbf{q}_1 = \frac{\mathbf{u}_1}{|\mathbf{u}_1|}$$
$$\mathbf{u}_2 = \mathbf{a}_2 - (\mathbf{q}_0 \cdot \mathbf{a}_2)\mathbf{q}_0 - (\mathbf{q}_1 \cdot \mathbf{a}_2)\mathbf{q}_1, \quad \mathbf{q}_2 = \frac{\mathbf{u}_2}{|\mathbf{u}_2|}$$

and so forth. The general formulas for calculating $\mathbf{u}_i$ and $\mathbf{q}_i$ are

$$\mathbf{u}_i = \mathbf{a}_i - \sum_{j=0}^{i-1}(\mathbf{q}_j \cdot \mathbf{a}_i)\mathbf{q}_j, \quad \mathbf{q}_i = \frac{\mathbf{u}_i}{|\mathbf{u}_i|}$$

a) Show, by induction or otherwise, that the vectors $\mathbf{q}_i$ are orthonormal, i.e., that they satisfy

$$\mathbf{q}_i \cdot \mathbf{q}_j = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases}$$

Now, rearranging the definitions of the vectors, we have

$$\mathbf{a}_0 = |\mathbf{u}_0|\mathbf{q}_0$$
$$\mathbf{a}_1 = |\mathbf{u}_1|\mathbf{q}_1 + (\mathbf{q}_0 \cdot \mathbf{a}_1)\mathbf{q}_0$$
$$\mathbf{a}_2 = |\mathbf{u}_2|\mathbf{q}_2 + (\mathbf{q}_0 \cdot \mathbf{a}_2)\mathbf{q}_0 + (\mathbf{q}_1 \cdot \mathbf{a}_2)\mathbf{q}_1$$

and so on. Or we can group the vectors $\mathbf{q}_i$ together as the columns of a matrix and write all of these equations as a single matrix equation

$$\mathbf{A} = \begin{pmatrix} | & | & | & \cdots \\ \mathbf{a}_0 & \mathbf{a}_1 & \mathbf{a}_2 & \cdots \\ | & | & | & \cdots \end{pmatrix} = \begin{pmatrix} | & | & | & \cdots \\ \mathbf{q}_0 & \mathbf{q}_1 & \mathbf{q}_2 & \cdots \\ | & | & | & \cdots \end{pmatrix} \begin{pmatrix} |\mathbf{u}_0| & \mathbf{q}_0 \cdot \mathbf{a}_1 & \mathbf{q}_0 \cdot \mathbf{a}_2 & \cdots \\ 0 & |\mathbf{u}_1| & \mathbf{q}_1 \cdot \mathbf{a}_2 & \cdots \\ 0 & 0 & |\mathbf{u}_2| & \cdots \end{pmatrix}$$

(If this looks complicated it's worth multiplying out the matrices on the right to verify for yourself that you get the correct expressions for the $\mathbf{a}_i$.)

Notice now that the first matrix on the right-hand side of this equation, the matrix with columns $\mathbf{q}_i$, is orthogonal, because the vectors $\mathbf{q}_i$ are orthonormal, and the second matrix is upper triangular. In other words, we have found the QR decomposition $\mathbf{A} = \mathbf{QR}$. The matrices $\mathbf{Q}$ and $\mathbf{R}$ are

$$\mathbf{Q} = \begin{pmatrix} | & | & | & \cdots \\ \mathbf{q}_0 & \mathbf{q}_1 & \mathbf{q}_2 & \cdots \\ | & | & | & \cdots \end{pmatrix}, \quad \mathbf{R} = \begin{pmatrix} |\mathbf{u}_0| & \mathbf{q}_0 \cdot \mathbf{a}_1 & \mathbf{q}_0 \cdot \mathbf{a}_2 & \cdots \\ 0 & |\mathbf{u}_1| & \mathbf{q}_1 \cdot \mathbf{a}_2 & \cdots \\ 0 & 0 & |\mathbf{u}_2| & \cdots \end{pmatrix}$$

b) Write a Python function that takes as its argument a real square matrix $\mathbf{A}$ and returns the two matrices $\mathbf{Q}$ and $\mathbf{R}$ that form its QR decomposition. As a test case, try out your function on the matrix

$$\mathbf{A} = \begin{pmatrix} 1 & 4 & 8 & 4 \\ 4 & 2 & 3 & 7 \\ 8 & 3 & 6 & 9 \\ 4 & 7 & 9 & 2 \end{pmatrix}$$

Check the results by multiplying $\mathbf{Q}$ and $\mathbf{R}$ together to recover the original matrix $\mathbf{A}$ again.

c) Using your function, write a complete program to calculate the eigenvalues and eigenvectors of a real symmetric matrix using the QR algorithm. Continue the calculation until the magnitude of every off-diagonal element of the matrix is smaller than $10^{-6}$. Test your program on the example matrix above. You should find that the eigenvalues are $1, 21, -3,$ and $-8$.

**Exercise 6.9: Asymmetric quantum well**

Quantum mechanics can be formulated as a matrix problem and solved on a computer using linear algebra methods. Suppose, for example, we have a particle of mass $M$ in a one-dimensional quantum well of width $L$, but not a square well like the ones you commonly find discussed in textbooks. Suppose instead that the potential $V(x)$ varies somehow inside the well:

[Diagram of asymmetric potential well]

We cannot solve such problems analytically in general, but we can solve them on the computer.

In a pure state of energy $E$, the spatial part $\psi(x)$ of the wavefunction obeys the time-independent Schrödinger equation $\hat{H}\psi(x) = E\psi(x)$, where the Hamiltonian operator $\hat{H}$ is given by

$$\hat{H} = -\frac{\hbar^2}{2M}\frac{d^2}{dx^2} + V(x).$$

For simplicity, let's assume that the walls of the well are infinitely high, so that the wavefunction is zero outside the well, which means it must go to zero at $x = 0$ and $x = L$. In that case, the wavefunction can be expressed as a Fourier sine series thus:

$$\psi(x) = \sum_{n=1}^{\infty} \psi_n \sin\frac{\pi n x}{L}$$

where $\psi_1, \psi_2, \ldots$ are the Fourier coefficients.

a) Noting that, for $m, n$ positive integers

$$\int_0^L \sin\frac{\pi m x}{L} \sin\frac{\pi n x}{L} dx = \begin{cases} L/2 & \text{if } m = n \\ 0 & \text{otherwise} \end{cases}$$

show that the Schrödinger equation $\hat{H}\psi = E\psi$ implies that

$$\sum_{n=1}^{\infty} \psi_n \int_0^L \sin\frac{\pi m x}{L} \hat{H} \sin\frac{\pi n x}{L} dx = \frac{1}{2}LE\psi_m.$$

Hence, defining a matrix $\mathbf{H}$ with elements

$$H_{mn} = \frac{2}{L}\int_0^L \sin\frac{\pi m x}{L} \hat{H} \sin\frac{\pi n x}{L} dx = \frac{2}{L}\int_0^L \sin\frac{\pi m x}{L} \left[-\frac{\hbar^2}{2M}\frac{d^2}{dx^2} + V(x)\right] \sin\frac{\pi n x}{L} dx$$

show that Schrödinger's equation can be written in matrix form as $\mathbf{H}\psi = E\psi$, where $\psi$ is the vector $(\psi_1, \psi_2, \ldots)$. Thus $\psi$ is an eigenvector of the **Hamiltonian matrix** $\mathbf{H}$ with eigenvalue $E$. If we can calculate the eigenvalues of this matrix, then we know the allowed energies of the particle in the well.

b) For the case $V(x) = ax/L$, evaluate the integral in $H_{mn}$ analytically and so find a general expression for the matrix element $H_{mn}$. Show that the matrix is real and symmetric. You'll probably find it useful to know that

$$\int_0^L x\sin\frac{\pi m x}{L}\sin\frac{\pi n x}{L} dx = \begin{cases} 0 & \text{if } m \neq n \text{ and } m,n \text{ are both even or both odd} \\ -\left(\frac{2L}{\pi}\right)^2 \frac{mn}{(m^2-n^2)^2} & \text{if } m \neq n \text{ and one is even, one is odd} \\ L^2/4 & \text{if } m = n \end{cases}$$

Write a Python program to evaluate your expression for $H_{mn}$ for arbitrary $m$ and $n$ when the particle in the well is an electron, the well has width $5\,$Å, and $a = 10\,$eV. (The mass and charge of an electron are $9.1094 \times 10^{-31}\,$kg and $1.6022 \times 10^{-19}\,$C respectively.)

c) The matrix $\mathbf{H}$ is in theory infinitely large, so we cannot calculate all its eigenvalues. But we can get a pretty accurate solution for the first few of them by cutting off the matrix after the first few elements. Modify the program you wrote for part (b) above to create a $10 \times 10$ array of the elements of $\mathbf{H}$ up to $m, n = 10$. Calculate the eigenvalues of this matrix using the appropriate function from `numpy.linalg` and hence print out, in units of electron volts, the first ten energy levels of the quantum well, within this approximation. You should find, for example, that the ground-state energy of the system is around $5.84\,$eV. (Hint: Bear in mind that matrix indices in Python start at zero, while the indices in standard algebraic expressions, like those above, start at one. You will need to make allowances for this in your program.)

d) Modify your program to use a $100 \times 100$ array instead and again calculate the first ten energy eigenvalues. Comparing with the values you calculated in part (c), what do you conclude about the accuracy of the calculation?

e) Now modify your program once more to calculate the wavefunction $\psi(x)$ for the ground state and the first two excited states of the well. Use your results to make a graph with three curves showing the probability density $|\psi(x)|^2$ as a function of $x$ in each of these three states. Pay special attention to the normalization of the wavefunction—it should satisfy the condition $\int_0^L |\psi(x)|^2 dx = 1$. Is this true of your wavefunction?

## 6.3 Nonlinear Equations

So far in this chapter we have looked at problems involving the solution of linear equations—in the all the examples we have studied the equations are simple linear combinations of the unknown variables. Many equations that arise in physics, however, are **nonlinear**. Nonlinear equations are, in general, significantly harder to solve than their linear counterparts. Even solving a single nonlinear equation in a single variable can be a challenging problem, and solving simultaneous equations in many variables is harder still. In this section we look at techniques for solving nonlinear equations, starting with the single-variable case.

### 6.3.1 The Relaxation Method

Suppose we have a single nonlinear equation that we want to solve for the value of a single variable, such as

$$x = 2 - e^{-x} \quad (6.69)$$

There is no known analytic method for solving this equation, so we turn to computational methods. One elementary method that gives good answers in many cases is simply to iterate the equation. That is, we guess an initial value of the unknown variable $x$, plug it in on the right-hand side of the equation and get a new value $x'$ on the left-hand side. For instance, we might in this case guess an initial value $x = 1$ and plug it in on the right-hand side of (6.69) to get

$$x' = 2 - e^{-1} \simeq 1.632 \quad (6.70)$$

Then we repeat the process, taking this value and feeding it in on the right again to get

$$x'' = 2 - e^{-1.632} \simeq 1.804 \quad (6.71)$$

and so forth. If we keep on doing this, and if we are lucky, then the value will converge to a **fixed point** of the equation, meaning it stops changing. In this particular case, that's exactly what happens. Here's a program to perform ten iterations of the calculation:

```python
from math import exp

x = 1.0
for k in range(10):
    x = 2 - exp(-x)
    print(x)
```

and here's what it prints out:

```
1.63212055883
1.80448546585
1.83544089392
1.84045685534
1.84125511391
1.84138178281
1.84140187354
1.84140505985
1.84140556519
1.84140564533
```

It appears that the result is converging to a value around $1.8414$, and indeed if we continue the process for a short while it converges to $x = 1.84140566044$ and stops changing. If a process like this converges to a fixed point, then the value of $x$ you get is necessarily a solution to the original equation—you feed that value in on one side of the equation and get the same value out on the other. This is the definition of a solution.

This method is called the **relaxation method**. When it works, it's often a good way of getting a solution. It's trivial to program (the program above has only five lines) and it runs reasonably quickly (it took about fifty steps in this case to reach a solution accurate to twelve figures).

The method does have its problems. First, the equation you are solving needs to be in the simple form $x = f(x)$, where $f(x)$ is some known function, and this is not always the case. However, even when the equation you are given is not in this form, it is in most cases a straightforward task to rearrange it so that it is. If you have an equation like $\log x + x^2 - 1 = 0$, for instance, you can take the exponential of both sides and rearrange to get $x = e^{1-x^2}$.

Second, an equation may have more than one solution. Sometimes the relaxation method will converge to one solution and not to another, in which case you only learn about the one solution. You may be able to mitigate this problem somewhat by your choice of the starting value of $x$. Depending on the starting value, the iteration process may converge to more than one different fixed point, so you can find more than one solution to the equation. Typically if the process does converge to a given solution then you can find it by choosing a starting value near that solution. So if you have some approximate idea of the position of the solution you're looking for, you should choose a value near it for your starting point.

There are, however, some solutions to some equations that you cannot find by this method no matter what starting value you choose. Even with a starting value close to such a solution, the method will not converge to the solution. Consider, for instance, the equation discussed above:

$$x = e^{1-x^2} \quad (6.72)$$

Again there's no general analytic method for solving this equation, but in this particular case one can see by inspection that the solution is just $x = 1$. If we try and find that solution by the relaxation method, however, starting with $x = \frac{1}{2}$ say, we get the following for the first ten values of $x$:

```
2.11700001661
0.03075541907
2.71571183275
0.00170346518
2.71827394058
0.00167991310
2.71827415718
0.00167991112
2.71827415720
0.00167991112
```

As you can see, instead of settling down to a fixed point, the program is oscillating back and forth between two different values. And it goes on doing this no matter how long we wait, so we never get a solution to our equation. The relaxation method has failed.

A useful trick in cases like these is to try to find an alternative way of arranging the equation to give the value of $x$. For instance, if we take logs of both sides of Eq. (6.72) then rearrange, we find the following alternative form for the equation:

$$x = \sqrt{1 - \log x} \quad (6.73)$$

If we now apply the relaxation method to this form, starting with $x = \frac{1}{2}$, we get the following:

```
1.30120989105
0.85831549149
1.07367757795
0.96379990441
1.01826891043
0.99090663593
1.00455709697
0.99772403758
1.00113862994
0.99943084694
```

The method is now converging to the solution at $x = 1$, and if we go on for a few more steps we get a very good approximation to that solution.

There is a mathematical theory behind the relaxation method that explains why this rearranging trick works. Assume we have an equation of the form $x = f(x)$ that has a solution at $x = x^*$ and let us consider the behavior of the relaxation method when $x$ is close to $x^*$. Performing a Taylor expansion, the value $x'$ after an iteration of the method is given in terms of the previous value $x$ by

$$x' = f(x) = f(x^*) + (x - x^*)f'(x^*) + \ldots \quad (6.74)$$

But by definition, $x^*$ is a solution of the original equation, meaning that $x^* = f(x^*)$, so Eq. (6.74) can also be written as

$$x' - x^* = (x - x^*)f'(x^*) \quad (6.75)$$

where we have neglected the higher-order terms.

This equation tells us that the distance $x - x^*$ to the true solution of the equation gets multiplied on each iteration of the method by a factor of $f'(x^*)$, the derivative of the function evaluated at $x^*$. If the absolute value of this derivative is less than one, then the distance will get smaller on each iteration, which means we are converging to the solution. If it is greater than one, on the other hand, then we are getting farther from the solution on each step and the method will not converge. Thus the relaxation method will converge to a solution at $x^*$ if and only if $|f'(x^*)| < 1$. This explains why the method failed for Eq. (6.72). In that case we have $f(x) = e^{1-x^2}$ and $x^* = 1$ so

$$|f'(x^*)| = \left|[-2xe^{1-x^2}]_{x=1}\right| = 2 \quad (6.76)$$

So the method will not converge.

Suppose that we find ourselves in a situation like this where the method does not converge because $|f'(x^*)| > 1$. Let us rearrange the equation $x = f(x)$ by inverting the function $f$ to get $x = f^{-1}(x)$, where $f^{-1}$ is the functional inverse of $f$. Now the method will be stable if the derivative of $f^{-1}$ is less than one at $x^*$.

To calculate this derivative we define $u = f^{-1}(x)$, so that the derivative we want is $du/dx$. But in that case we also have $x = f(u)$, so

$$\frac{dx}{du} = f'(u) \quad (6.77)$$

But when $x = x^*$ we have $u = f^{-1}(x^*) = x^*$ and, taking reciprocals, we then find that the derivative we want is

$$\frac{du}{dx} = \frac{1}{f'(x^*)} \quad (6.78)$$

Thus the derivative of $f^{-1}$ at $x^*$ is simply the reciprocal of the derivative of $f$. That means that if the derivative of $f$ is greater than one then the derivative of $f^{-1}$ must be less than one. Hence, if the relaxation method fails to converge for $x = f(x)$ it will succeed for the equivalent form $x = f^{-1}(x)$.

The bottom line is, if the method fails for a particular equation you should invert the equation and then the method will work. This is exactly what we did for Eq. (6.73).

Unfortunately, not all equations can be inverted. If your $f(x)$ is a polynomial of degree ten, for example, then inversion is not possible. In such cases it may still be possible to rearrange and get a different equation for $x$, but the theory above no longer applies and convergence is no longer guaranteed. You might get a convergent calculation if you're lucky, but you might not. Consider, for instance, the equation

$$x = x^2 + \sin 2x \quad (6.79)$$

This equation has a solution at $x^* = 0$, but if we apply the relaxation method directly we will not find that solution. The method fails to converge, as we can prove by calculating $|f'(x^*)|$, which turns out to be equal to 2 in this case. Moreover, the function $f(x) = x^2 + \sin 2x$ on the right-hand side of Eq. (6.79) cannot be inverted. We can, however, still rearrange the equation thus:

$$x = \frac{1}{2}\sin^{-1}(x - x^2) \quad (6.80)$$

Because this is not a true inversion of the original equation, we are not guaranteed that this version will converge any better than the original one, but in fact it does—if we calculate $|f'(x^*)|$ again, we find that it is now equal to $\frac{1}{2}$ and hence the relaxation method will now work. This time we got lucky.

In summary, the relaxation method does not always work, but between the cases where it works first time, the ones where it can be made to work by inverting, and the ones where some other rearrangement turns out by good luck to work, the method is useful for a wide range of problems.

### 6.3.2 Rate of Convergence of the Relaxation Method

An important question about the relaxation method is how fast it converges to a solution, assuming it does converge. We can answer this question by looking again at Eq. (6.75). This equation tells us that, when the method converges, the distance to the solution gets smaller by a factor of $|f'(x^*)|$ on each iteration. In other words, the distance decreases exponentially with the number of iterations we perform. Since the exponential is a rapidly decaying function this is a good thing: the relaxation method converges to a solution quickly, although there are other methods that converge faster still, such as **Newton's method**, which we study in Section 6.3.5.

This is a nice result as far as it goes, but it isn't very practical. In a typical application of the relaxation method what we really want to know is, "When can I stop iterating? When is the answer I have good enough?" One simple way to answer this question is just to look at the solutions you get on successive iterations of the method and observe when they stop changing. For instance, if you want an answer accurate to six figures, you continue until a few iterations have passed without any changes in the first six figures of $x$. If you want a quick answer to a problem and accuracy is not a big issue, this is actually not a bad approach. It's easy and it usually works.

In some cases, however, we may want to know exactly how accurate our answer is, or we may wish to stop immediately as soon as a required target accuracy is reached. If, for instance, a single iteration of the relaxation method takes a long time—minutes or hours—because the calculations involved are complex, then we may not want to perform even one more iteration than is strictly necessary. In such cases, we can take the following approach.

Let us define $\epsilon$ to be the error on our current estimate of the solution to the equation. That is, the true solution $x^*$ is related to the current estimate $x$ by $x^* = x + \epsilon$. Similarly let $\epsilon'$ be the error on the next estimate, so that $x^* = x' + \epsilon'$. Then Eq. (6.75) tells us that close to $x^*$ we have

$$\epsilon' = \epsilon f'(x^*) \quad (6.81)$$

Then

$$x^* = x + \epsilon = x + \frac{\epsilon'}{f'(x^*)} \quad (6.82)$$

and equating this with $x^* = x' + \epsilon'$ and rearranging for $\epsilon'$ we derive an expression for the error on the new estimate:

$$\epsilon' = \frac{x - x'}{1 - 1/f'(x^*)} \simeq \frac{x - x'}{1 - 1/f'(x)} \quad (6.83)$$

where we have made use of the fact that $x$ is close to $x^*$, so that $f'(x) \simeq f'(x^*)$. If we know the form of the function $f(x)$ then we can calculate its derivative and then use this formula to estimate the error $\epsilon'$ on the new value $x'$ for the solution at each step. Then, for instance, we can simply repeat the iteration until the magnitude of this estimated error falls below some target value, ensuring that we get an answer that is as accurate as we want, without wasting any time on additional iterations.

There are some cases, however, where we don't know the full formula for $f(x)$. For instance, $f(x)$ might not be given as a mathematical formula at all, but as the output of another program that itself performs some complicated calculation. In such cases we cannot calculate the derivative $f'(x)$ directly, but we can estimate it using a numerical derivative like those we studied in Section 5.10. As we saw there, calculating a numerical derivative involves taking the difference of the values of $f$ at two different points. In the most common application of this idea to the relaxation method we choose the points to be the values of $x$ at successive steps of the iteration.

Suppose we have three successive estimates of $x$, which we denote $x, x'$, and $x''$. We would like to calculate the error on the most recent estimate $x''$, which by Eq. (6.83) is

$$\epsilon'' = \frac{x' - x''}{1 - 1/f'(x^*)} \simeq \frac{x' - x''}{1 - 1/f'(x)} \quad (6.84)$$

Now we approximate $f'(x)$ as

$$f'(x) \simeq \frac{f(x) - f(x')}{x - x'} \quad (6.85)$$

But by definition $x' = f(x)$ and $x'' = f(x')$, so

$$f'(x) \simeq \frac{x' - x''}{x - x'} \quad (6.86)$$

Substituting into Eq. (6.84), we then find that the error on the third and most recent of our estimates of the solution is given approximately by

$$\epsilon'' \simeq \frac{x' - x''}{1 - (x - x')/(x' - x'')} = \frac{(x' - x'')^2}{2x' - x - x''} \quad (6.87)$$

Thus, if we keep track of three successive estimates of $x$ at each stage of the calculation we can estimate the error even when we cannot calculate a derivative of $f(x)$ directly.

**Example 6.3: Ferromagnetism**

In the mean-field theory of ferromagnetism, the strength $M$ of magnetization of a ferromagnetic material like iron depends on temperature $T$ according to the formula

$$M = \mu \tanh\frac{JM}{k_BT} \quad (6.88)$$

where $\mu$ is a magnetic moment, $J$ is a coupling constant, and $k_B$ is Boltzmann's constant. To simplify things a little, let us make the substitutions $m = M/\mu$ and $C = \mu J/k_B$ so that

$$m = \tanh\frac{Cm}{T} \quad (6.89)$$

It's clear that this equation always has a solution at $m = 0$, which implies a material that is not magnetized at all, but what about other solutions? Are there solutions with $m \neq 0$? There is no known method of solving for such solutions exactly, but we can find them using the computer. Let's assume that $C = 1$ for simplicity and look for solutions as a function of $T$, accurate to within $\pm 10^{-6}$ of the true answer. In this case, since we know the full functional form of the equation we are solving, we can evaluate the derivative in Eq. (6.83) explicitly and show that the error is given by

$$\epsilon' = \frac{m - m'}{1 - T\cosh^2(m/T)} \quad (6.90)$$

Here's a program to find the solutions and make a plot as a function of temperature:

```python
from math import tanh, cosh
from numpy import linspace
from pylab import plot, show, ylim, xlabel, ylabel

# Constants
Tmax = 2.0
points = 1000
accuracy = 1e-6

# Set up lists for plotting
y = []
temp = linspace(0.01, Tmax, points)

# Temperature loop
for T in temp:
    m1 = 1.0
    error = 1.0
    
    # Loop until error is small enough
    while error > accuracy:
        m1, m2 = tanh(m1/T), m1
        error = abs((m1-m2)/(1-T*cosh(m2/T)**2))
    y.append(m1)

# Make the graph
plot(temp, y)
ylim(-0.1, 1.1)
xlabel("Temperature")
ylabel("Magnetization")
show()
```

For each value of the temperature we iterate Eq. (6.89) starting with $m = 1$, until the magnitude of the error, estimated from Eq. (6.90), falls below the target value. Figure 6.2 shows the end result. As we can see the program does indeed find nonzero solutions of the equation, but only for values of the temperature below $T = 1$. As we approach $T = 1$ from below the value of the magnetization falls off and above $T = 1$ the program only finds the solution $m = 0$. This is a real physical phenomenon observed in experiments on real magnets. If you take a magnetized piece of iron and heat it, then the magnetization will
```

以上是这份PDF文档的完整Markdown转换。文档主要涵盖：

1. **线性方程组求解**：高斯消元法、回代法、选主元、LU分解
2. **特殊矩阵**：三对角矩阵和带状矩阵的高效算法
3. **特征值和特征向量**：QR算法及其在Python中的实现
4. **非线性方程**：松弛法（不动点迭代）及其收敛性分析
5. **物理应用**：电阻网络、弹簧质点系统、铁磁性、量子阱等