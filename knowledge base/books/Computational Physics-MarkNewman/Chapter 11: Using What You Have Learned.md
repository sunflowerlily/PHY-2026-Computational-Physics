# Chapter 11 Using What You Have Learned

In the preceding chapters of this book we have studied the main pillars of computational physics, including numerical integration and differentiation, linear algebra, the solution of ordinary and partial differential equations, and Monte Carlo methods, and seen how to put the theoretical concepts into practice using the Python programming language. The material in this book forms a solid foundation for the solution of physics problems using computational methods.

That is not to say, however, that the book covers everything there is to know about computational physics. Certainly it does not. Computational physics is a huge field, heavily researched and developed over the decades, and it encompasses an enormous range of knowledge and approaches, some general, some specialized. If you continue with the study of computational physics, or if you do computational work in a professional situation in industry, business, or academia, you will almost certainly have to learn additional techniques not covered in this book. Here is just a taste of some of the advanced techniques currently in use in different areas of physics:

1. In Chapter 5 we studied several methods for performing integrals, including the trapezoidal rule and Gaussian quadrature, but there are many other methods that can prove useful under certain circumstances. Two important examples are *Clenshaw-Curtis quadrature* and *Gauss-Kronrod quadrature*, which are similar to Gaussian quadrature in using unevenly spaced integration points to improve on simple rules like the trapezoidal rule. They are in general less accurate than Gaussian quadrature, but they allow nesting of integration points in a manner similar to the adaptive integration method of Section 5.3, which allows us, for example, to make estimates of the errors on our integrals with relatively little computational effort. Gauss-Kronrod quadrature is discussed briefly in Appendix C. For multidimensional integrals there are also a wide range of techniques available, some specialized to integration domains of particular shapes, others designed to get accurate answers in a minimum of computation time. The *low-discrepancy point sets* mentioned in Section 5.9 are an important example of the latter.

2. In Chapter 6 we studied the solution of linear systems of equations. An important class of linear equation problems that arises in physics are those involving *sparse equations*, whose matrix representation contains a large number of zeros and only a few nonzero elements. We saw one example in Section 6.1.6, where we looked at tridiagonal and banded matrices, which have zeros everywhere except close to the diagonal, but there are many more general examples also, which may have nonzero elements anywhere in the matrix but nonetheless have only a few nonzero elements overall. For such matrices the standard methods of equation solving, inversion, and calculation of eigenvalues are inefficient because they waste time performing computations on all the zeros that have no effect on the final result. Luckily, as with tridiagonal matrices, there are special techniques for sparse matrices that are more efficient, such as the *conjugate gradient method* and the *Lanczos algorithm*. These methods find use particularly in condensed matter physics, where they are employed to solve problems involving the lattices of atoms in a solid.

3. In Chapter 9 we studied the solution of partial differential equations using finite difference methods and spectral methods, but we omitted an important third class of methods, the *finite element methods*. These methods, though complex and challenging to use, are some of the most powerful available for the general solution of partial differential equations, and are particularly useful for problems such as the solution of Maxwell's equations or the Navier-Stokes equations of fluid dynamics.

4. In our discussion of Monte Carlo simulation in Chapter 10, we mentioned only the most common and important of sampling algorithms, the Metropolis algorithm, but there are others that may be appropriate for particular problems, including the *heat-bath algorithm*, rejection-free methods like the *Swendsen-Wang algorithm*, and continuous-time methods like the *Bortz-Kalos-Lebowitz algorithm*.

Entire books have been written on each of these topics and on many others as well, and while it's certainly not practical to read all of them, there are plenty of opportunities to learn more about a particular problem or class of problems when the need arises.

Another important way in which your future experiences with computational physics might differ from the material in this book is in the computer language employed. We have used the Python language exclusively, which is a good choice—it's easy to learn, powerful, and contains many features that are well suited to physics calculations. It does have its disadvantages, however, the primary one being that it is slower than some other languages, and significantly so for certain types of calculations. If you find yourself doing computational work in the future, it's quite likely that you will have to use a language other than Python, perhaps because you need greater speed, or because you are working as part of a team that routinely uses another language. The most likely alternative languages for physics work are C and Fortran, but you might also use C++, Java, IDL, Julia, or Matlab, among others.

Luckily, these computer languages do not differ greatly from one another. To be sure, there are differences in the details—the exact words and symbols you use to represent a statement—but the concepts of programming are similar in all of them and you will find, once you know how to program in Python, that switching to another language is not difficult. Armed with your knowledge of Python you can probably pick up the main points of a new language in just a day or so.

Consider, for example, the following short Python program, which calculates the integral $\int_0^1 e^{-x^2} dx$ using the trapezoidal rule with 1000 points:

```python
from math import exp

def f(x):
    return exp(-x*x)

a = 0.0
b = 1.0
N = 1000
h = (b-a)/N

s = 0.5*(f(a)+f(b))
for k in range(1,N):
    s += f(a+k*h)
print(h*s)
```

Now here is the same program written in the C programming language:

```c
#include <math.h>
#include <stdio.h>

double f(double x)
{
    return exp(-x*x);
}

main()
{
    double a,b,h,s;
    int N,k;

    a = 0.0;
    b = 1.0;
    N = 1000;
    h = (b-a)/N;

    s = 0.5*(f(a)+f(b));
    for (k=1; k<N; k++) s += f(a+k*h);
    printf("%g\n",h*s);
}
```

There are some obvious differences between the two programs. Note how almost every line in the C program ends with a semicolon. In C you use the semicolon to show when a statement is finished, and a statement that does not end with a semicolon is considered to continue on the following line. In Python, rather than using a special symbol to show when a line ends we use one to show when it *doesn't* end—recall that when we want a statement to continue on the next line we use a backslash symbol "\" (see Section 3.4). Either approach works fine. Both allow you to use both single-line and multi-line statements as needed. But the two languages make different choices about the details. These are the kinds of things you will need to learn if you have to work in a different computer language.

Another important difference between Python and C, visible in the example programs above, is that in C all variables have to be *declared* before they can be used. For example, the statement "double a,b,h,s;" in the C program above tells the computer that we are going to be using floating-point variables called a, b, h, and s. (In C the floating-point variable type is called "double" for historical reasons.[^1]) If we omit this statement, the program will not run.

However, there are strong similarities between the two programs as well. In the C program the statements at the beginning that start with "#include" are the equivalent of import statements in Python. They tell the computer that we are going to be using functions imported from other modules. The definition of the function f(x) in the C program is similar to the Python definition, except for the occurrence of the word "double" again, which tells the computer that both the variable x and the result returned by the function are of floating-point type. In the main program we go through the same steps in the C and Python versions, first assigning values to various variables, then using a for loop to calculate the trapezoidal rule sum, and finally printing out the result. The details of the individual statements vary, but the overall logical structure is closely similar between the two languages.

Apart from differences in the programs themselves, another difference between Python and C (and some other languages, such as Fortran) is that the latter makes use of a *compiler*. At their lowest level, computers speak to themselves in a native language called a *machine language* or *machine code*, which is well suited for computers but very unintuitive for human beings. You can write programs in machine code, but it's challenging. Instead, therefore, we write our programs in more human-compatible languages like Python or C and then have the computer translate them into machine code for us. There are two general schemes for doing this. The first is to use an *interpreter*, which is a program that translates the lines of code one by one as the program is executed. This is the scheme Python uses. The second approach is to use a compiler, which translates the entire program into machine code in one go, then we run the machine-code version. This is the scheme that C uses. The advantage of using a compiler is that the final program runs significantly faster, because no translation needs to be done while the program is running. This is the main reason why C programs are faster than Python programs. However, using a compiler has disadvantages too. The compiler has to be used and the program translated every time we make even the smallest change to our code, even just changing the value of a single parameter, and this can be time-consuming and inconvenient. Large programs can take minutes or even hours to translate. Languages like C that use a compiler also tend to be more cumbersome and difficult to work with than languages that use an interpreter. The requirement that we declare all our variables before we use them, for instance, is a result of the way the compiler works. In Python there is no such requirement—one can use any variable one likes at any time, and this makes programming significantly simpler and easier. So both approaches have their pluses and minuses. Naturally this means that each may be better in some situations than the other, and this is precisely why we have more than one computer language in the first place.

Nonetheless, the similarities between computer languages are much greater than their differences, and, as we have said, you should have little difficulty applying what you have learned about Python to another language if and when the need arises. Armed with the principles of computational physics, the practical experience you've acquired here, and a good fast computer, you should be able to go out and start doing physics.

[^1]: The floating-point type in C was originally called "float", which is more logical, but there was also another type, called "double", short for "double-precision," which was a more accurate floating-point type that could store larger numbers to greater precision, at the expense of slower calculations. On modern computer hardware, however, calculations are equally fast with either type, and hence the float type has become obsolete and is no longer used, since the double type is more accurate and just as fast.

## 总结：两大主题
1. 进阶技术方向
数值积分：Clenshaw-Curtis求积、Gauss-Kronrod求积
稀疏矩阵：共轭梯度法、Lanczos算法
偏微分方程：有限元法
蒙特卡洛：热浴算法、Swendsen-Wang算法等
2. 编程语言转换
Python易学但慢，实际工作可能需要C/Fortran等更快的语言
用梯形法则计算积分的例子对比Python和C代码
关键区别：Python用解释器（动态类型、慢但方便），C用编译器（需声明变量、快但繁琐）
结论：语言间的相似性大于差异，掌握Python后学其他语言很容易。