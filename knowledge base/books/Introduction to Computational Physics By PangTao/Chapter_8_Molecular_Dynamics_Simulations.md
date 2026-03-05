# Chapter 8: Molecular Dynamics Simulations

Most physical systems are collections of interacting objects. For example, a drop of water contains more than $10^{21}$ water molecules, and a galaxy is a collection of millions and millions of stars. In general, there is no analytical solution that can be found for an interacting system with more than two objects. We can solve the problem of a two-body system, such as the Earth–Sun system, analytically, but not a three-body system, such as the Moon–Earth–Sun system. The situation is similar in quantum mechanics, in that one can obtain the energy levels of the hydrogen atom (one electron and one proton) analytically, but not those of the helium atom (two electrons and a nucleus). Numerical techniques beyond those we have discussed so far are needed to study a system of a large number of interacting objects, or the so-called many-body system. Of course, there is a distinction between three-body systems such as the Moon–Earth–Sun system and a more complicated system, such as a drop of water. Statistical mechanics has to be applied to the latter.

## 8.1 General Behavior of a Classical System

In this chapter, we introduce a class of simulation techniques called molecular dynamics, which solves the dynamics of a classical many-body system described by the Hamiltonian

$$H = E_K + E_P = \sum_{i=1}^{N} \frac{p_i^2}{2m_i} + \sum_{i>j=1}^{N} V(r_{ij}) + \sum_{i=1}^{N} U_{ext}(r_i) \tag{8.1}$$

where $E_K$ and $E_P$ are the kinetic energy and potential energy of the system, respectively, $m_i$, $r_i$, and $p_i$ are the mass, position vector, and momentum of the $i$th particle, and $V(r_{ij})$ and $U(r_i)$ are the corresponding interaction energy and external potential energy. From Hamilton's principle, the position vector and momentum satisfy

$$\dot{r}_i = \frac{\partial H}{\partial p_i} = \frac{p_i}{m_i} \tag{8.2}$$

$$\dot{p}_i = -\frac{\partial H}{\partial q_i} = f_i \tag{8.3}$$

which are called Hamilton's equations and valid for any given $H$, including the case of a system that can exchange energy or heat with its environment. Here the force $f_i$ is given by

$$f_i = -\nabla U_{ext}(r_i) - \sum_{j \neq i} \nabla V(r_{ij}) \tag{8.4}$$

The methods for solving Newton's equation discussed in Chapter 1 and Chapter 4 can be used to solve the above equation set. However, those methods are not as practical as the ones about to be discussed, in terms of the speed and accuracy of the computation and given the statistical nature of large systems. In this chapter, we discuss several commonly used molecular dynamics simulation schemes and offer a few examples.

Before we go into the numerical schemes and actual physical systems, we need to discuss several issues. There are several ways to simulate a many-body system. Most simulations are done either through a stochastic process, such as the Monte Carlo simulation, which will be discussed in Chapter 10, or through a deterministic process, such as a molecular dynamics simulation. Some numerical simulations are performed in a hybridized form of both, for example, Langevin dynamics, which is similar to molecular dynamics except for the presence of a random dissipative force, and Brownian dynamics, which is performed under the condition that the acceleration is balanced out by the drifting and random dissipative forces. We will not discuss Langevin or Brownian dynamics in this book, but interested readers can find detailed discussions in Heermann (1986) and Kadanoff (2000).

Another issue is the distribution function of the system. In statistical mechanics, each special environment is dealt with by way of a special ensemble. For example, for an isolated system we use the microcanonical ensemble, which assumes a constant total energy, number of particles, and volume. A system in good contact with a thermal bath is dealt with using the canonical ensemble, which assumes a constant temperature, number of particles, and volume (or pressure). For any given ensemble, the system is described by a probability function $W(R, P)$, which is in general a function of phase space, consisting of all coordinates and momenta of the particles $R = (r_1, r_2, \ldots, r_N)$ and $P = (p_1, p_2, \ldots, p_N)$, and other quantities, such as temperature, total particle number of the system, and so forth. For the canonical ensemble, we have

$$W(R, P) = \frac{1}{N} e^{-H/k_B T} \tag{8.5}$$

where $T$ is the temperature of the system, $k_B$ is the Boltzmann constant, and $N$ is a normalization constant. For an $N$-particle quasi-classical system, $N = N!h^{3N}$, where $h$ is the Planck constant. Note that we can separate the position dependence and momentum dependence in $W(R, P)$ if they are not coupled in $H$. Any average of the momentum-dependent quantity becomes quite simple because of the quadratic behavior of the momentum in $H$. So we concentrate on the position dependence here. The statistical average of a physical quantity $A(R, P)$ is then given by

$$\langle A \rangle = \int A(R, P) W(R, P) dR dP \tag{8.6}$$

where $Z$ is the partition function of the system from

$$Z = \int W(R, P) dR dP \tag{8.7}$$

The ensemble average given above is equivalent to the time average

$$\langle A \rangle = \lim_{\tau \to \infty} \frac{1}{\tau} \int_0^{\tau} A(t) dt \tag{8.8}$$

if the system is ergodic: that is, every possible state is accessed with an equal probability. Because molecular dynamics simulations are deterministic in nature, almost all physical quantities are obtained through time averages. Sometimes the average over all the particles is also needed to characterize the system. For example, the average kinetic energy of the system can be obtained from any ensemble average, and the result is given by the partition theorem

$$\langle E_K \rangle = \sum_{i=1}^{N} \frac{p_i^2}{2m_i} = \frac{G}{2} k_B T \tag{8.9}$$

where $G$ is the total number of degrees of freedom. For a very large system, $G \approx 3N$, because each particle has three degrees of freedom. In molecular dynamics simulations, the average kinetic energy of the system can be obtained through

$$\langle E_K \rangle = \frac{1}{M} \sum_{j=1}^{M} E_K(t_j) \tag{8.10}$$

where $M$ is the total number of data points taken at different time steps and $E_K(t_j)$ is the kinetic energy of the system at time $t_j$. If the system is ergodic, the time average is equivalent to the ensemble average. The temperature $T$ of the simulated system is then given by the average kinetic energy with the application of the partition theorem, $T = 2\langle E_K \rangle / Gk_B$.

## 8.2 Basic Methods for Many-Body Systems

In general, we can define an n-body density function

$$\rho_n(r_1, r_2, \ldots, r_n) = \frac{1}{Z} \frac{N!}{(N-n)!} \int W(R, P) dR_n dP \tag{8.11}$$

where $dR_n = dr_{n+1} dr_{n+2} \cdots dr_N$. Note that the particle density $\rho(r) = \rho_1(r)$ is the special case of $n = 1$. The two-body density function is related to the pair-distribution function $g(r, r')$ through

$$\rho_2(r, r') = \rho(r) g(r, r') \rho(r') \tag{8.12}$$

and one can easily show that

$$\rho_2(r, r') = \langle \hat{\rho}(r) \hat{\rho}(r') \rangle - \delta(r - r') \rho(r) \tag{8.13}$$

where the first term is the so-called density–density correlation function. Here $\hat{\rho}(r)$ is the density operator, defined as

$$\hat{\rho}(r) = \sum_{i=1}^{N} \delta(r - r_i) \tag{8.14}$$

The density of the system is given by the average of the density operator,

$$\rho(r) = \langle \hat{\rho}(r) \rangle \tag{8.15}$$

If the density of the system is nearly a constant, the expression for $g(r, r')$ can be reduced to a much simpler form

$$g(r) = \frac{1}{\rho N} \sum_{i \neq j} \delta(r - r_{ij}) \tag{8.16}$$

where $\rho$ is the averaged density from the points $r' = 0$ and $r$. If the angular distribution is not the information needed, we can take the angular average to obtain the radial distribution function

$$g(r) = \frac{1}{4\pi} \int g(r) \sin\theta d\theta d\phi \tag{8.17}$$

where $\theta$ and $\phi$ are the polar and azimuthal angles from the spherical coordinate system. The pair-distribution or radial distribution function is related to the static structure factor $S(k)$ through the Fourier transform

$$S(k) - 1 = \rho \int [g(r) - 1] e^{-ik \cdot r} dr \tag{8.18}$$

and its inverse

$$g(r) - 1 = \frac{1}{(2\pi)^3 \rho} \int [S(k) - 1] e^{ik \cdot r} dk \tag{8.19}$$

The angular average of $S(k)$ is given by

$$S(k) - 1 = 4\pi\rho \int_0^{\infty} [g(r) - 1] \frac{\sin kr}{kr} r^2 dr \tag{8.20}$$

The structure factor of a system can be measured with the light- or neutron-scattering experiment.

The behavior of the pair-distribution function can provide a lot of information regarding the translational nature of the particles in the system. For example, a solid structure would have a pair-distribution function with sharp peaks at the distances of nearest neighbors, next nearest neighbors, and so forth. If the system is a liquid, the pair-distribution still has some broad peaks at the average distances of nearest neighbors, next nearest neighbors, and so forth, but the feature fades away after several peaks.

If the bond orientational order is important, one can also define an orientational correlation function

$$g_n(r, r') = \langle q_n(r) q_n(r') \rangle \tag{8.21}$$

where $q_n(r)$ is a quantity associated with the orientation of a specific bond. Detailed discussions on orientational order can be found in Strandburg (1992).

Here we discuss how one can calculate $\rho(r)$ and $g(r)$ in a numerical simulation. The density at a specific point is given by

$$\rho(r) \approx \frac{\langle N(r, \Delta r) \rangle}{\Omega(r, \Delta r)} \tag{8.22}$$

where $\Omega(r, \Delta r)$ is the volume of a sphere centered at $r$ with a radius $\Delta r$ and $N(r, \Delta r)$ is the number of particles in the volume. Note that we may need to adjust the radius $\Delta r$ to have a smooth and realistic density distribution $\rho(r)$ for a specific system. The average is taken over the time steps.

Similarly, we can obtain the radial distribution function numerically. We need to measure the radius $r$ from the position of a specific particle $r_i$, and then the radial distribution function $g(r)$ is the probability of another particle's showing up at a distance $r$. Numerically, we have

$$g(r) \approx \frac{\langle \Delta N(r, \Delta r) \rangle}{\rho \Delta\Omega(r, \Delta r)} \tag{8.23}$$

where $\Delta\Omega(r, \Delta r) \approx 4\pi r^2 \Delta r$ is the volume element of a spherical shell with radius $r$ and thickness $\Delta r$ and $\Delta N(r, \Delta r)$ is the number of particles in the shell with the $i$th particle at the center of the sphere. The average is taken over the time steps as well as over the particles, if necessary.

The dynamics of the system can be measured from the displacement of the particles in the system. We can evaluate the time dependence of the mean-square displacement of all the particles,

$$\Delta^2(t) = \frac{1}{N} \sum_{i=1}^{N} [r_i(t) - r_i(0)]^2 \tag{8.24}$$

where $r_i(t)$ is the position vector of the $i$th particle at time $t$. For a solid system, $\Delta^2(t)$ is relatively small and does not grow with time, and the particles are in nondiffusive, or oscillatory, states. For a liquid system, $\Delta^2(t)$ grows linearly with time:

$$\Delta^2(t) = 6Dt + \Delta^2(0) \tag{8.25}$$

where $D$ is the self-diffusion coefficient (a measure of the motion of a particle in a medium of identical particles) and $\Delta^2(0)$ is a time-independent constant. The particles are then in diffusive, or propagating, states.

The very first issue in numerical simulations for a bulk system is how to extend a finite simulation box to model the nearly infinite system. A common practice is to use a periodic boundary condition, that is, to approximate an infinite system by piling up identical simulation boxes periodically. A periodic boundary condition removes the conservation of the angular momentum of the simulated system (particles in one simulation box), but still preserves the translational symmetry of the center of mass. So the temperature is related to the average kinetic energy by

$$\langle E_K \rangle = \frac{3}{2}(N - 1)k_B T \tag{8.26}$$

where the factor $(N - 1)$ is due to the removal of the rotation around the center of mass.

The remaining issue, then, is how to include the interactions among the particles in different simulation boxes. If the interaction is a short-range interaction, one can truncate it at a cut-off length $r_c$. The interaction $V(r_c)$ has to be small enough that the truncation does not affect the simulation results significantly. A typical simulation box usually has much larger dimensions than $r_c$. For a three-dimensional cubic box with sides of length $L$, the total interaction potential can be evaluated with many fewer summations than $N!/2$, the number of possible pairs in the system. For example, if we have $L/2 > r_c$, and if $|x_{ij}|$, $|y_{ij}|$, and $|z_{ij}|$ are all smaller than $L/2$, we can use $V_{ij} = V(r_{ij})$; otherwise, we use the corresponding point in the neighboring box. For example, if $|x_{ij}| > L/2$, we can replace $x_{ij}$ with $x_{ij} \pm L$ in the interaction. We can deal with $y$ and $z$ coordinates similarly. In order to avoid a finite jump at the truncation, one can always shift the interaction to $V(r) - V(r_c)$ to make sure that it is zero at the truncation.

The pressure of a bulk system can be evaluated from the pair-distribution function through

$$P = \rho k_B T - \frac{2\pi\rho^2}{3} \int_0^{\infty} \frac{\partial V(r)}{\partial r} g(r) r^3 dr \tag{8.27}$$

which is the result of the virial theorem that relates the average kinetic energy to the average potential energy of the system. The correction due to the truncation of the potential is then given by

$$\Delta P = -\frac{2\pi\rho^2}{3} \int_{r_c}^{\infty} \frac{\partial V(r)}{\partial r} g(r) r^3 dr \tag{8.28}$$

which is useful for estimating the influence on the pressure from the truncation in the interaction potential. Numerically, one can also evaluate the pressure from the time average

$$\langle w \rangle = \frac{1}{3} \sum_{i>j} \langle r_{ij} \cdot f_{ij} \rangle \tag{8.29}$$

because $g(r)$ can be interpreted as the probability of seeing another particle at a distance $r$. Then we have

$$P = \rho k_B T + \frac{\rho}{N} \langle w \rangle + \Delta P \tag{8.30}$$

which can be evaluated quite easily, because at every time step the force $f_{ij} = -\nabla V(r_{ij})$ is calculated for each particle pair.

## 8.3 The Verlet Algorithm

Hamilton's equations given in Eqs. (8.2) and (8.3) are equivalent to Newton's equation

$$m_i \frac{d^2r_i}{dt^2} = f_i \tag{8.31}$$

for the $i$th particle in the system. To simplify the notation, we will use $R$ to represent all the coordinates $(r_1, r_2, \ldots, r_N)$ and $G$ to represent all the accelerations $(f_1/m_1, f_2/m_2, \ldots, f_N/m_N)$. Thus, we can rewrite Newton's equations for all the particles as

$$\frac{d^2R}{dt^2} = G \tag{8.32}$$

If we apply the three-point formula to the second-order derivative $d^2R/dt^2$, we have

$$\frac{d^2R}{dt^2} = \frac{1}{\tau^2}(R_{k+1} - 2R_k + R_{k-1}) + O(\tau^2) \tag{8.33}$$

with $t = k\tau$. We can also apply the three-point formula to the velocity

$$V = \frac{dR}{dt} = \frac{1}{2\tau}(R_{k+1} - R_{k-1}) + O(\tau^2) \tag{8.34}$$

After we put all the above together, we obtain the simplest algorithm, which is called the Verlet algorithm, for a classical many-body system, with

$$R_{k+1} = 2R_k - R_{k-1} + \tau^2 G_k + O(\tau^4) \tag{8.35}$$

$$V_k = \frac{R_{k+1} - R_{k-1}}{2\tau} + O(\tau^2) \tag{8.36}$$

The Verlet algorithm can be started if the first two positions $R_0$ and $R_1$ of the particles are given. However, in practice, only the initial position $R_0$ and initial velocity $V_0$ are given. Therefore, we need to figure out $R_1$ before we can start the recursion. A common practice is to treat the force during the first time interval $[0, \tau]$ as a constant, and then to apply the kinematic equation to obtain

$$R_1 = R_0 + \tau V_0 + \frac{\tau^2}{2} G_0 \tag{8.37}$$

where $G_0$ is the acceleration vector evaluated at the initial configuration $R_0$.

Of course, the position $R_1$ can be improved by carrying out the Taylor expansion to higher-order terms if the accuracy in the first two points is critical. We can also replace $G_0$ in Eq. (8.37) with the average $(G_0 + G_1)/2$, with $G_1$ evaluated at $R_1$, given from Eq. (8.37). This procedure can be iterated several times before starting the algorithm for the velocity $V_1$ and the next position $R_2$.

The Verlet algorithm has advantages and disadvantages. It preserves the time reversibility that is one of the important properties of Newton's equation. The rounding error may eventually destroy this time symmetry. The error in the velocity is two orders of magnitude higher than the error in the position. In many applications, we may only need information about the positions of the particles, and the Verlet algorithm yields very high accuracy for the position. If the velocity is not needed, we can totally ignore the evaluation of the velocity, since the evaluation of the position does not depend on the velocity at each time step. The biggest disadvantage of the Verlet algorithm is that the velocity is evaluated one time step behind the position. However, this lag can be removed if the velocity is evaluated directly from the force. A two-point formula would yield

$$V_{k+1} = V_k + \tau G_k + O(\tau^2) \tag{8.38}$$

We would get much better accuracy if we replaced $G_k$ with the average $(G_k + G_{k+1})/2$. The new position can be obtained by treating the motion within $t \in [k\tau, (k+1)\tau]$ as motion with a constant acceleration $G_k$; that is,

$$R_{k+1} = R_k + \tau V_k + \frac{\tau^2}{2} G_k \tag{8.39}$$

Then a variation of the Verlet algorithm with the velocity calculated at the same time step of the position is

$$R_{k+1} = R_k + \tau V_k + \frac{\tau^2}{2} G_k + O(\tau^4) \tag{8.40}$$

$$V_{k+1} = V_k + \frac{\tau}{2}(G_{k+1} + G_k) + O(\tau^2) \tag{8.41}$$

Note that the evaluation of the position still has the same accuracy because the velocity is now updated according to Eq. (8.41), which provides the cancelation of the third-order term in the new position.

Here we demonstrate this velocity version of the Verlet algorithm with a very simple example, the motion of Halley's comet, which has a period of about 76 years.

The potential between the comet and the Sun is given by

$$V(r) = -G \frac{Mm}{r} \tag{8.42}$$

where $r$ is the distance between the comet and the Sun, $M$ and $m$ are the respective masses of the Sun and the comet, and $G$ is the gravitational constant. If we use the center-of-mass coordinate system as described in Chapter 3 for the two-body collision, the dynamics of the comet is governed by

$$\mu \frac{d^2r}{dt^2} = f = -GMm \frac{r}{r^3} \tag{8.43}$$

with the reduced mass

$$\mu = \frac{Mm}{M + m} \approx m \tag{8.44}$$

for the case of Halley's comet. We can take the farthest point (aphelion) as the starting point, and then we can easily obtain the comet's whole orbit with one of the versions of the Verlet algorithm. Two quantities can be assumed as the known quantities, the total energy and the angular momentum, which are the constants of motion. We can describe the motion of the comet in the $xy$ plane and choose $x_0 = r_{max}$, $v_{x0} = 0$, $y_0 = 0$, and $v_{y0} = v_{min}$. From well-known results we have that $r_{max} = 5.28 \times 10^{12}$ m and $v_{min} = 9.13 \times 10^2$ m/s. Let us apply the velocity version of the Verlet algorithm to this problem. Then we have

$$x^{(k+1)} = x^{(k)} + \tau v_x^{(k)} + \frac{\tau^2}{2} g_x^{(k)} \tag{8.45}$$

$$v_x^{(k+1)} = v_x^{(k)} + \frac{\tau}{2}(g_x^{(k+1)} + g_x^{(k)}) \tag{8.46}$$

$$y^{(k+1)} = y^{(k)} + \tau v_y^{(k)} + \frac{\tau^2}{2} g_y^{(k)} \tag{8.47}$$

$$v_y^{(k+1)} = v_y^{(k)} + \frac{\tau}{2}(g_y^{(k+1)} + g_y^{(k)}) \tag{8.48}$$

where the time-step index is given in parentheses as superscripts in order to distinguish it from the x-component or y-component index. The acceleration components are given by

$$g_x = -\kappa \frac{x}{r^3} \tag{8.49}$$

$$g_y = -\kappa \frac{y}{r^3} \tag{8.50}$$

with $r = \sqrt{x^2 + y^2}$ and $\kappa = GM$. We can use more specific units in the numerical calculations, for example, 76 years as the time unit and the semimajor axis of the orbital $a = 2.68 \times 10^{12}$ m as the length unit. Then we have $r_{max} = 1.97$, $v_{min} = 0.816$, and $\kappa = 39.5$. The following program is the implementation of the algorithm outlined above for Halley's comet.

```java
// An example to study the time-dependent position and
// velocity of Halley's comet via the Verlet algorithm.
import java.lang.*;

public class Comet {
    static final int n = 20000, m = 200;
    
    public static void main(String argv[]) {
        double t[] = new double[n];
        double x[] = new double[n];
        double y[] = new double[n];
        double r[] = new double[n];
        double vx[] = new double[n];
        double vy[] = new double[n];
        double gx[] = new double[n];
        double gy[] = new double[n];
        double h = 2.0/(n-1), h2 = h*h/2, k = 39.478428;
        
        // Initialization of the problem
        t[0] = 0;
        x[0] = 1.966843;
        y[0] = 0;
        r[0] = x[0];
        vx[0] = 0;
        vy[0] = 0.815795;
        gx[0] = -k/(r[0]*r[0]);
        gy[0] = 0;
        
        // Verlet algorithm for the position and velocity
        for (int i=0; i<n-1; ++i) {
            t[i+1] = h*(i+1);
            x[i+1] = x[i]+h*vx[i]+h2*gx[i];
            y[i+1] = y[i]+h*vy[i]+h2*gy[i];
            double r2 = x[i+1]*x[i+1]+y[i+1]*y[i+1];
            r[i+1] = Math.sqrt(r2);
            double r3 = r2*r[i+1];
            gx[i+1] = -k*x[i+1]/r3;
            gy[i+1] = -k*y[i+1]/r3;
            vx[i+1] = vx[i]+h*(gx[i+1]+gx[i])/2;
            vy[i+1] = vy[i]+h*(gy[i+1]+gy[i])/2;
        }
        
        for (int i=0; i<n-m; i+=m) {
            System.out.println(t[i]);
            System.out.println(r[i]);
            System.out.println();
        }
    }
}
```

In Fig. 8.1, we show the result for the distance between Halley's comet and the Sun calculated using the above program.

The accuracy of the velocity version of the Verlet algorithm is reasonable in practice; it is usually accurate enough because the corresponding physical quantities are rescaled according to, for example, the temperature of the system in most molecular dynamics simulations. The accumulated errors are thus removed when the rescaling is applied. More accurate algorithms, such as the Gear predictor–corrector algorithm, will be discussed later in this chapter.

## 8.4 Structure of Atomic Clusters

One of the simplest applications of the Verlet algorithm is in the study of an isolated collection of particles. For an isolated system, there is a significant difference between a small system and a large system. For a small system, the ergodic assumption of statistical mechanics fails and the system may never reach the so-called equilibrium state. However, some parallel conclusions can be drawn on the thermodynamics of small systems against infinite systems (Gross, 2001). For a very large system, standard statistical mechanics applies, even if it is isolated from the environment; the interactions among the particles cause the exchange of energies and drive the system to equilibrium. Very small clusters with just a few particles usually behave like molecules (Sugano and Koizumi, 1998). What is unclear is the behavior of a cluster of an intermediate size, say, about 100 atoms.

In this section, we demonstrate the application of the velocity version of the Verlet algorithm in determining the structure and dynamics of clusters of an intermediate size. We will assume that the system consists of $N$ atoms that interact with each other through the Lennard–Jones potential

$$V(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right] \tag{8.51}$$

where $r$ is the distance between the two particles, and $\varepsilon$ and $\sigma$ are the system-dependent parameters. The force exerted on the $i$th particle is therefore given by

$$f_i = \frac{48\varepsilon}{\sigma^2} \sum_{j \neq i} \left(\frac{\sigma}{r_{ij}}\right)^{14} - \frac{1}{2}\left(\frac{\sigma}{r_{ij}}\right)^8 \right] r_{ij} \tag{8.52}$$

In order to simplify the notation, $\varepsilon$ is usually used as the unit of energy, $\varepsilon/k_B$ as the unit of temperature, and $\sigma$ as the unit of length. Then the unit of time is given by $\sqrt{m\sigma^2/48\varepsilon}$. Newton's equation for each particle then becomes dimensionless,

$$\frac{d^2r_i}{dt^2} = g_i = \sum_{j \neq i} \left(\frac{1}{r_{ij}^{14}} - \frac{1}{2r_{ij}^8}\right) r_{ij} \tag{8.53}$$

After discretization with the Verlet algorithm, we have

$$r_i^{(k+1)} = r_i^{(k)} + \tau v_i^{(k)} + \frac{\tau^2}{2} g_i^{(k)} \tag{8.54}$$

$$v_i^{(k+1)} = v_i^{(k)} + \frac{\tau}{2}(g_i^{(k+1)} + g_i^{(k)}) \tag{8.55}$$

The update of the velocity is usually done in two steps in practice. When $g_i^{(k)}$ is evaluated, the velocity is partially updated with

$$v_i^{(k+1/2)} = v_i^{(k)} + \frac{\tau}{2} g_i^{(k)} \tag{8.56}$$

and then updated again when $g_i^{(k+1)}$ becomes available after the coordinate is updated, with

$$v_i^{(k+1)} = v_i^{(k+1/2)} + \frac{\tau}{2} g_i^{(k+1)} \tag{8.57}$$

This is equivalent to the one-step update but more economical, because it does not require storage of the acceleration of the previous time step. We can then simulate the structure and dynamics of the cluster starting from a given initial position and velocity for each particle. However, several aspects still need special care. The initial positions of the particles are usually taken as the lattice points on a closely packed structure, for example, the face-centered cubic structure. What we want to avoid is the breaking up of the system in the first few time steps, which happens if some particles are too close to each other. Another way to set up a relatively stable initial cluster is to cut out a piece from a bulk simulation. The corresponding bulk simulation is achieved with the application of the periodic boundary condition. The initial velocities of the particles should also be assigned reasonably. A common practice is to assign velocities from the Maxwell distribution

$$W(v_x) \propto e^{-mv_x^2/2k_B T} \tag{8.58}$$

which can be achieved numerically quite easily with the availability of Gaussian random numbers. The variance in the Maxwell distribution is $\sqrt{k_B T/m}$ for each velocity component. For example, the following method returns the Maxwell distribution of the velocity for a given temperature.

```java
// Method to draw initial velocities from the Maxwell
// distribution for a given mass m, temperature T, and
// paritcle number N.
public static double[] maxwell(double m, double T, int N) {
    int nv = 3*N;
    int ng = nv-6;
    double v[] = new double[nv];
    double r[] = new double[2];
    
    // Assign a Gaussian number to each velocity component
    for (int i=0; i<nv-1; i+=2) {
        r = rang();
        g[i] = r[0];
        g[i+1] = r[1];
    }
    
    // Scale the velocity to satisfy the partition theorem
    double ek = 0;
    for (int i=0; i<nv; ++i) ek += v[i]*v[i];
    double vs = Math.sqrt(m*ek*nv/(ng*T));
    for (int i=0; i<nv; ++i) v[i] /= vs;
    return v;
}
```

However, we always have difficulty in defining a temperature if the system is very small, that is, where the thermodynamic limit is not applicable. In practice, we can still call a quantity associated with the kinetic energy of the system the temperature, which is basically a measure of the kinetic energy at each time step,

$$E_K = \frac{G}{2} k_B T \tag{8.59}$$

where $G$ is the total number of independent degrees of freedom in the system. Note that now $T$ is not necessarily a constant and that $G$ is equal to $3N - 6$, with $N$ being the number of particles in the system, because we have to remove the center-of-mass motion and rotation around the center of mass when we study the structure and dynamics of the isolated cluster.

The total energy of the system is given by

$$E = \sum_{i=1}^{N} \frac{m_i v_i^2}{2} + \sum_{i>j=1}^{N} V(r_{ij}) \tag{8.60}$$

where the kinetic energy $E_K$ is given by the first term on the right-hand side and the potential energy $E_P$ by the second.

One remarkable effect observed in the simulations of finite clusters is that there is a temperature region where the system fluctuates from a liquid state to a solid state over time. A phase is identified as solid if the particles in the system vibrate only around their equilibrium positions; otherwise they are in a liquid phase. Simulations of clusters have revealed some very interesting phenomena that are unique to clusters of intermediate size (with $N \approx 100$). We have discussed how to analyze the structural and dynamical information of a collection of particles in Sections 8.1 and 8.2. One can evaluate the mean square of the displacement of each particle. For the solid state, $\Delta^2(t)$ is relatively small and does not grow with time, and the particles are nondiffusive but oscillatory. For the liquid state, $\Delta^2(t)$ grows with time close to the linear relation $\Delta^2(t) = 6Dt + \Delta^2(0)$, where $D$ is the self-diffusion coefficient and $\Delta^2(0)$ is a constant. In a small system, this relation in time may not be exactly linear. One can also measure the specific structure of the cluster from the pair-distribution function $g(r)$ and the orientational correlation function of the bonds. The temperature (or total kinetic energy) can be gradually changed to cool or heat the system.

The results from simulations on clusters of about 100 particles show that the clusters can fluctuate from a group of solid states with lower energy levels to a group of liquid states that lie at higher energy levels in a specific temperature region, with $k_B T$ in the same order as the energy that separates the two groups. This is not expected because the higher-energy-level liquid states are not supposed to have an observable lifetime. However, the statistical mechanics may not be accurate here, because the number of particles is relatively small. More detailed simulations also reveal that the melting of the cluster usually starts from the surface. Interested readers can find more discussions of this topic in Matsuoka et al. (1992) and Kunz and Berry (1993; 1994).

## 8.5 The Gear Predictor–Corrector Method

We discussed multistep predictor–corrector methods in Chapter 4 when solving initial-value problems. Another type of predictor–corrector method uses the truncated Taylor expansion of the function and its derivatives as a prediction and then evaluates the function and its derivatives at the same time step with a correction given from the restriction of the differential equation. This multivalue predictor–corrector scheme was developed by Nordsieck and Gear. Details of the derivations can be found in Gear (1971).

We will take a first-order differential equation

$$\frac{dr}{dt} = f(r, t) \tag{8.61}$$

as an example and then generalize the method to other types of initial-value problems, such as Newton's equation. For simplicity, we will introduce the rescaled quantities

$$r^{(l)} = \frac{\tau^l}{l!} \frac{d^l r}{dt^l} \tag{8.62}$$

with $l = 0, 1, 2, \ldots$. Note that $r^{(0)} = r$. Now if we define a vector

$$x = (r^{(0)}, r^{(1)}, r^{(2)}, \ldots) \tag{8.63}$$

we can obtain the predicted value of $x$ in the next time step $x_{k+1}$, with $t_{k+1} = (k+1)\tau$, from that of the current time step $x_k$, with $t_k = k\tau$, from the Taylor expansion for each component of $x_{k+1}$: that is,

$$x_{k+1} = Bx_k \tag{8.64}$$

where $B$ is the coefficient matrix from the Taylor expansion. One can easily show that $B$ is an upper triangular matrix with unit diagonal and first row elements, with the other elements given by

$$B_{ij} = \binom{j-1}{i} = \frac{(j-1)!}{i!(j-i-1)!} \tag{8.65}$$

Note that the dimension of $B$ is $(n+1) \times (n+1)$, that is, $x$ is a vector of dimension $n+1$, if the Taylor expansion is carried out up to the term of $d^n r/dt^n$.

The correction in the Gear method is performed with the application of the differential equation under study. The difference between the predicted value of the first-order derivative $r_{k+1}^{(1)}$ and the velocity field $\tau f_{k+1}$ is

$$\delta r_{k+1}^{(1)} = \tau f_{k+1} - r_{k+1}^{(1)} \tag{8.66}$$

which would be zero if the exact solution were obtained with $\tau \to 0$. Note that $r_{k+1}^{(1)}$ in the above equation is from the prediction of the Taylor expansion. So if we combine the prediction and the correction in one expression, we have

$$x_{k+1} = Bx_k + C \delta x_{k+1} \tag{8.67}$$

where $\delta x_{k+1}$ has only one nonzero component, $\delta r_{k+1}^{(1)}$, and $C$ is the correction coefficient matrix, which is diagonal with zero off-diagonal elements and nonzero diagonal elements $C_{ii} = c_i$ for $i = 0, 1, \ldots, n$. Here $c_i$ are obtained by solving a matrix eigenvalue problem involving $B$ and the gradient of $\delta x_{k+1}$ with respect to $x_{k+1}$. It is straightforward to solve for $c_i$ if the truncation in the Taylor expansion is not very high. Interested readers can find the derivation in Gear (1971), with a detailed table listing up to the fourth-order differential equations (Gear 1971, p. 154). The most commonly used Gear scheme for the first-order differential equation is the fifth-order Gear algorithm (with the Taylor expansion carried out up to $n = 5$), with $c_0 = 95/288$, $c_1 = 1$, $c_2 = 25/24$, $c_3 = 35/72$, $c_4 = 5/48$, and $c_5 = 1/120$.

We should point out that the above procedure is not unique to first-order differential equations. The predictor part is identical for any higher-order differential equation. The only change one needs to make is the correction, which is the result of the difference between the prediction and the solution restricted by the equation. In molecular dynamics, we are interested in the solution of Newton's equation, which is a second-order differential equation with

$$\frac{d^2r}{dt^2} = \frac{f(r, t)}{m} \tag{8.68}$$

where $f$ is the force on a specific particle of mass $m$. We can still formally express the algorithm as

$$x_{k+1} = Bx_k + C \delta x_{k+1} \tag{8.69}$$

where $\delta x_{k+1}$ also has only one nonzero element

$$\delta r_{k+1}^{(2)} = \tau^2 f_{k+1}/2m - r_{k+1}^{(2)} \tag{8.70}$$

which provides the corrections to all the components of $x$. Similarly, $r_{k+1}^{(2)}$ in the above equation is from the Taylor expansion. The corrector coefficient matrix is still diagonal with zero off-diagonal elements and nonzero diagonal elements $C_{ii} = c_i$ for $i = 0, 1, \ldots, n$. Here $c_i$ for the second-order differential equation have also been worked out by Gear (1971, p. 154). The most commonly used Gear scheme for the second-order differential equation is still the fifth-order Gear algorithm (with the Taylor expansion carried out up to $n = 5$), with $c_0 = 3/20$, $c_1 = 251/360$, $c_2 = 1$, $c_3 = 11/18$, $c_4 = 1/6$, and $c_5 = 1/60$. The values of these coefficients are obtained with the assumption that the force in Eq. (8.68) does not have an explicit dependence on the velocity, that is, the first-order derivative of $r$. If it does, $c_0 = 3/20$ needs to be changed to $c_0 = 3/16$ (Allen and Tildesley, 1987, pp. 340–2).

## 8.6 Constant Pressure, Temperature, and Bond Length

Several issues still need to be addressed when we want to compare the simulation results with the experimental measurements. For example, environmental parameters, such as temperature or pressure, are the result of thermal or mechanical contact of the system with the environment or the result of the equilibrium of the system. For a macroscopic system, we deal with average quantities by means of statistical mechanics, so it is highly desirable for the simulation environment to be as close as possible to a specific ensemble. The scheme adopted in Section 8.4 for atomic cluster systems is closely related to the microcanonical ensemble, which has the total energy of the system conserved. It is important that we also be able to find ways to deal with constant-temperature and/or constant-pressure conditions. We should emphasize that there have been many efforts to model realistic systems with simulation boxes by introducing some specific procedures. However, all these procedures do not introduce any new concepts in physics. They are merely numerical techniques to make the simulation boxes as close as possible to the physical systems under study.

### Constant Pressure: The Andersen Scheme

The scheme for dealing with a constant-pressure environment was devised by Andersen (1980) with the introduction of an environmental variable, the instantaneous volume of the system, in the effective Lagrangian. When the Lagrange equation is applied to the Lagrangian, the equations of motion for the coordinates of the particles and the volume result. The constant pressure is then a result of the zero average of the second-order time derivative of the volume.

The effective Lagrangian of Andersen (1980) is given by

$$L = \sum_{i=1}^{N} \frac{m_i L^2 \dot{x}_i^2}{2} - \sum_{i>j} V(Lx_{ij}) + \frac{M}{2}\dot{\Omega}^2 - P_0\Omega \tag{8.71}$$

where the last two terms are added to deal with the constant pressure from the environment. The parameter $M$ can be viewed here as an effective inertia associated with the expansion and contraction of the volume $\Omega$, and $P_0$ is the external pressure, which introduces a potential energy $P_0\Omega$ to the system under the assumption that the system is in contact with the constant-pressure environment. The coordinate of each particle $r_i$ is rescaled with the dimension of the simulation box, $L = \Omega^{1/3}$, because the distance between any two particles changes with $L$ and the coordinates independent of the volume are then given by

$$x_i = r_i/L \tag{8.72}$$

which are not directly related to the changing volume. Note that this effective Lagrangian is not the result of any new physical principles or concepts but is merely a method of modeling the effect of the environment in realistic systems.

Now if we apply the Lagrange equation to the above Lagrangian, we obtain the equations of motion for the particles and the volume $\Omega$,

$$\ddot{x}_i = \frac{g_i}{L} - \frac{2\dot{\Omega}}{3\Omega} \dot{x}_i \tag{8.73}$$

$$\ddot{\Omega} = \frac{P - P_0}{M} \tag{8.74}$$

where $g_i = f_i/m_i$ and $P$ is given by

$$P = \frac{1}{3\Omega} \left[\sum_i m_i L^2 \dot{x}_i^2 + \sum_{i>j} r_{ij} \cdot f_{ij}\right] \tag{8.75}$$

which can be interpreted as the instantaneous pressure of the system and has a constant average $P_0$, because $\langle \ddot{\Omega} \rangle \equiv 0$.

After we have the effective equations of motion, the algorithm can be worked out quite easily. We will use

$$X = (x_1, x_2, \cdots, x_N) \tag{8.76}$$

$$G = (f_1/m_1, f_2/m_2, \cdots, f_N/m_N) \tag{8.77}$$

to simplify the notation. If we apply the velocity version of the Verlet algorithm, the difference equations for the volume and the rescaled coordinates are given by

$$\Omega_{k+1} = \Omega_k + \tau \dot{\Omega}_k + \frac{\tau^2(P_k - P_0)}{2M} \tag{8.78}$$

$$X_{k+1} = \left(1 - \frac{\tau^2 \dot{\Omega}_k}{2\Omega_k}\right) X_k + \tau \dot{X}_k + \frac{\tau^2 G_k}{2L_k} \tag{8.79}$$

$$\dot{\Omega}_{k+1} = \dot{\Omega}_{k+1/2} + \frac{\tau(P_{k+1} - P_0)}{2M} \tag{8.80}$$

$$\dot{X}_{k+1} = \left(1 - \frac{\tau \dot{\Omega}_{k+1}}{2\Omega_{k+1}}\right) \dot{X}_{k+1/2} + \frac{\tau G_{k+1}}{2L_{k+1}} \tag{8.81}$$

where the values with index $k+1/2$ are intermediate values before the pressure and force are updated, with

$$\dot{\Omega}_{k+1/2} = \dot{\Omega}_k + \frac{\tau(P_k - P_0)}{2M} \tag{8.82}$$

$$\dot{X}_{k+1/2} = \left(1 - \frac{\tau \dot{\Omega}_k}{2\Omega_k}\right) \dot{X}_k + \frac{\tau G_k}{2L_{k+1}} \tag{8.83}$$

which are usually evaluated immediately after the volume and the coordinates are updated.

In practice, we first need to set up the initial positions and velocities of the particles and the initial volume and its time derivative. The initial volume is determined from the given particle number and density, and its initial time derivative is usually set to be zero. The initial coordinates of the particles are usually arranged on a densely packed lattice, for example, a face-centered cubic lattice, and the initial velocities are usually drawn from the Maxwell distribution. One should test the program with different $M$s in order to find the value of $M$ that minimizes the fluctuation.

A generalization of the Andersen constant-pressure scheme was introduced by Parrinello and Rahman (1980; 1981) to allow the shape of the simulation box to change as well. This generalization is important in the study of the structural phase transition. With the shape of the simulation box allowed to vary, the particles can easily move to the lattice points of the structure with the lowest free energy. The idea of Parrinello and Rahman can be summarized in the Lagrangian

$$L = \sum_{i=1}^{N} \frac{1}{2} m_i \dot{x}_i^T B \dot{x}_i - \sum_{i>j} V(x_{ij}) + \sum_{i,j=1}^{3} \frac{M}{2} \dot{A}_{ij}^2 - P_0\Omega \tag{8.84}$$

where $y_i$ is the coordinate of the $i$th particle in the vector representation of the simulation box, $\Omega = a \cdot (b \times c)$, with

$$r_i = x_i^{(1)}a + x_i^{(2)}b + x_i^{(3)}c \tag{8.85}$$

Here $A$ is the matrix representation of $(a, b, c)$ in Cartesian coordinates and $B = A^T A$. Instead of a single variable $\Omega$, there are nine variables $A_{ij}$, with $i, j = 1, 2, 3$; this allows both the volume size and the shape of the simulation box to change. The equations of motion for $x_i$ and $A_{ij}$ can be derived by applying the Lagrange equation to the above Lagrangian. An external stress can also be included in such a procedure (Parrinello and Rahman, 1981).

### Constant Temperature: The Nosé Scheme

The constant-pressure scheme discussed above is usually performed with an ad hoc constant-temperature constraint, which is done by rescaling the velocities during the simulation to ensure the relation between the total kinetic energy and the desired temperature in the canonical ensemble.

This rescaling can be shown to be equivalent to a force constraint up to first order in the time step $\tau$. The constraint method for the constant-temperature simulation is achieved by introducing an artificial force $-\eta p_i$, which is similar to a frictional force if $\eta$ is greater than zero or to a heating process if $\eta$ is less than zero. The equations of motion are modified under this force to

$$\dot{r}_i = \frac{p_i}{m_i} \tag{8.86}$$

$$\dot{v}_i = \frac{f_i}{m_i} - \eta v_i \tag{8.87}$$

where $p_i$ is the momentum of the $i$th particle and $\eta$ is the constraint parameter, which can be obtained from the relevant Lagrange multiplier (Evans et al., 1983) in the Lagrange equations with

$$\eta = \frac{\sum_i f_i \cdot v_i}{\sum_i m_i v_i^2} = -\frac{dE_P/dt}{v_i^2 G k_B T} \tag{8.88}$$

which can be evaluated at every time step. Here $G$ is the total number of degrees of freedom of the system, and $E_P$ is the total potential energy. So one can simulate the canonical ensemble averages from the equations for $r_i$ and $v_i$ given in Eqs. (8.86) and (8.87).

The most popular constant-temperature scheme is that of Nosé (1984a; 1984b), who introduced a fictitious dynamical variable to take the constant-temperature environment into account. The idea is very similar to that of Andersen for the constant-pressure case. In fact, one can put both fictitious variables together to have simulations for constant pressure and constant temperature together. Here we will briefly discuss the Nosé scheme.

We can introduce a rescaled effective Lagrangian

$$L = \sum_{i=1}^{N} \frac{m_i s^2 \dot{x}_i^2}{2} - \sum_{i>j} V(x_{ij}) + \frac{m_s \dot{s}^2}{2} - G k_B T \ln s \tag{8.89}$$

where $s$ and $v_s$ are the coordinate and velocity of an introduced fictitious variable that rescales the time and the kinetic energy in order to have the constraint of the canonical ensemble satisfied. The rescaling is achieved by replacing the time element $dt$ with $dt/s$ and holding the coordinates unchanged, that is, $x_i = r_i$. The velocity is rescaled with time: $\dot{r}_i = s \dot{x}_i$. We can then obtain the equation of motion for the coordinate $x_i$ and the variables by applying the Lagrange equation. Hoover (1985; 1999) showed that the Nosé Lagrangian leads to a set of equations very similar to the result of the constraint force scheme discussed at the beginning of this subsection. The Nosé equations of motion are given in the Hoover version by

$$\dot{r}_i = v_i \tag{8.90}$$

$$\dot{v}_i = \frac{f_i}{m_i} - \eta v_i \tag{8.91}$$

where $\eta$ is given in a differential form,

$$\dot{\eta} = \frac{1}{m_s} \left(\sum_{i=1}^{N} \frac{p_i^2}{m_i} - G k_B T\right) \tag{8.92}$$

and the original variables, introduced by Nosé, is related to $\eta$ by

$$s = s_0 e^{\eta(t-t_0)} \tag{8.93}$$

with $s_0$ as the initial value of $s$ at $t = t_0$. We can discretize the above equation set easily with either the Verlet algorithm or one of the Gear schemes. Note that the behavior of the parameters is no longer directly related to the simulation; it is merely a parameter Nosé introduced to accomplish the microscopic processes happening in the constant-temperature environment. We can also combine the Andersen constant-pressure scheme with the Nosé constant-temperature scheme in a single effective Lagrangian

$$L = \sum_{i=1}^{N} \frac{m_i s^2 L^2 \dot{x}_i^2}{2} - \sum_{i>j} V(Lx_{ij}) + \frac{m_s \dot{s}^2}{2} - G k_B T \ln s + \frac{M}{2}\dot{\Omega}^2 - P_0\Omega \tag{8.94}$$

which is worked out in detail in the original work of Nosé (1984a; 1984b).

Another constant-temperature scheme was introduced by Berendsen et al. (1984) with the parameter $\eta$ given by

$$\eta = \frac{1}{m_s} \left(\sum_{i=1}^{N} m_i v_i^2 - G k_B T\right) \tag{8.95}$$

which can be interpreted as a similar form of the constraint that differs from the Hoover–Nosé form in the choice of $\eta$. For a review on the subject, see Nosé (1991).

### Constant Bond Length

Another issue we have to deal with in practice is that for large molecular systems, such as biopolymers, the bond length of a pair of nearest neighbors does not change very much even though the angle between a pair of nearest bonds does. If we want to obtain accurate simulation results, we have to choose a time step much smaller than the period of the vibration of each pair of atoms. This costs a lot of computing time and might exclude the applicability of the simulation to more complicated systems, such as biopolymers.

A procedure commonly known as the SHAKE algorithm (Ryckaert, Ciccotti, and Berendsen, 1977; van Gunsteren and Berendsen, 1977) was introduced to deal with the constraint on the distance between a pair of particles in the system. The idea of this procedure is to adjust each pair of particles iteratively to have

$$\left|\frac{r_{ij}^2 - d_{ij}^2}{d_{ij}^2}\right| \leq \delta \tag{8.96}$$

in each time step. Here $d_{ij}$ is the distance constraint between the $i$th and $j$th particles and $\delta$ is the tolerance in the simulation. The adjustment of the position of each particle is performed after each time step of the molecular dynamics simulation. Assume that we are working on a specific pair of particles and for the $l$th constraint and that we would like to have

$$(r_{ij} + \delta r_{ij})^2 - d_{ij}^2 = 0 \tag{8.97}$$

where $r_{ij}$ is the new position vector difference after a molecular time step starting from $r_{ij}^{(0)}$ and the adjustments for the $l-1$ constraints have been completed. Here $\delta r_{ij} = \delta r_j - \delta r_i$ is the total amount of adjustment needed for both particles.

One can show, in conjunction with the Verlet algorithm, that the adjustments needed are given by

$$\delta r_i = -\frac{m_j}{m_i} \delta r_j = -g_{ij} \delta r_{ij} \tag{8.98}$$

with $g_{ij}$ as a parameter to be determined. The center of mass of these two particles remains the same during the adjustment.

If we substitute $\delta r_i$ and $\delta r_j$ given in Eq. (8.98), we obtain

$$r_{ij}^{(0)2} g_{ij}^2 + 2\mu_{ij} r_{ij}^{(0)} \cdot r_{ij} g_{ij} + \mu_{ij}^2 r_{ij}^2 - d_{ij}^2 = 0 \tag{8.99}$$

where $\mu_{ij} = m_i m_j/(m_i + m_j)$ is the reduced mass of the two particles. If we keep only the linear term in $g_{ij}$, we have

$$g_{ij} = \frac{\mu_{ij}}{2r_{ij}^{(0)} \cdot r_{ij}}(d_{ij}^2 - r_{ij}^2) \tag{8.100}$$

which is reasonable, because $g_{ij}$ is a small number during the simulation. More importantly, by the end of the iteration, all the constraints will be satisfied as well; all $g_{ij}$ go to zero at the convergence. Equation (8.100) is used to estimate each $g_{ij}$ for each constraint in each iteration. After one has the estimate of $g_{ij}$ for each constraint, the positions of the relevant particles are all adjusted. The adjustments have to be performed several times until the convergence is reached. For more details on the algorithm, see Ryckaert et al. (1977).

This procedure has been used in the simulation of chain-like systems as well as of proteins and nucleic acids. Interested readers can find some detailed discussions on the dynamics of proteins and nucleic acids in McCammon and Harvey (1987).

## 8.7 Structure and Dynamics of Real Materials

In this section, we will discuss some typical methods used to extract information about the structure and dynamics of real materials in molecular dynamics simulations.

A numerical simulation of a specific material starts with a determination of the interaction potential in the system. In most cases, the interaction potential is formulated in a parameterized form, which is usually determined separately from the available experimental data, first principles calculations, and condition of the system under study. The accuracy of the interaction potential determines the validity of the simulation results. Accurate model potentials have been developed for many realistic materials, for example, the Au(100) surface (Ercolessi, Tosatti, and Parrinello, 1986) and Si$_3$N$_4$ ceramics (Vashishta et al., 1995). In the next section, we will discuss an ab initio molecular dynamics scheme in which the interaction potential is obtained by calculating the electronic structure of the system at each particle configuration.

We then need to set up a simulation box under the periodic boundary condition. Because most experiments are performed in a constant-pressure environment, we typically use the constant-pressure scheme developed by Andersen (1980) or its generalization (Parrinello and Rahman, 1980; 1981). The size of the simulation box has to be decided together with the available computing resources and the accuracy required for the quantities to be evaluated. The initial positions of the particles are usually assigned at the lattice points of a closely packed structure, for example, a face-centered cubic structure. The initial velocities of the particles are drawn from the Maxwell distribution for a given temperature. The temperature can be changed by rescaling the velocities. This is extremely useful in the study of phase transitions with varying temperature, such as the transition between different lattice structures, glass transition under quenching, or liquid–solid transition when the system is cooled down slowly. The advantage of simulation over actual experiments also shows up when we want to observe some behavior that is not achievable experimentally due to the limitations of the technique or equipment. For example, the glass transition in the Lennard–Jones system is observed in molecular dynamics simulations but not in the experiments for liquid Ar, because the necessary quenching rate is so high that it is impossible to achieve it experimentally.

Studying the dynamics of different materials requires a more general time-dependent density–density correlation function

$$C(r, r'; t) = \langle \hat{\rho}(r + r', t) \hat{\rho}(r', 0) \rangle \tag{8.101}$$

with the time-dependent density operator given by

$$\hat{\rho}(r, t) = \sum_{i=1}^{N} \delta[r - r_i(t)] \tag{8.102}$$

If the system is homogeneous, we can integrate out $r'$ in the time-dependent density–density correlation function to reach the van Hove time-dependent distribution function (van Hove, 1954)

$$G(r, t) = \frac{1}{\rho N} \sum_{i,j} \delta\{r - [r_i(t) - r_j(0)]\} \tag{8.103}$$

The dynamical structure factor measured in an experiment, for example, neutron scattering, is given by the Fourier transform of $G(r, t)$ as

$$S(k, \omega) = \frac{\rho}{2\pi} \int e^{i(\omega t - k \cdot r)} G(r, t) dr dt \tag{8.104}$$

The above equation reduces to the static case with

$$S(k) - 1 = 4\pi\rho \int \frac{\sin kr}{kr} [g(r) - 1] r^2 dr \tag{8.105}$$

if we realize that

$$G(r, 0) = g(r) + \frac{\delta(r)}{\rho} \tag{8.106}$$

and

$$S(k) = \int_{-\infty}^{\infty} S(k, \omega) d\omega \tag{8.107}$$

where $g(r)$ is the pair distribution discussed earlier in this chapter and $S(k)$ is the angular average of $S(k)$. Here $G(r, t)$ can be interpreted as the probability of observing one of the particles at $r$ at time $t$ if a particle was observed at $r = 0$ at $t = 0$. This leads to the numerical evaluation of $G(r, t)$, which is the angular average of $G(r, t)$. If we write $G(r, t)$ in two parts,

$$G(r, t) = G_s(r, t) + G_d(r, t) \tag{8.108}$$

with $G_s(r, t)$ the probability of observing the same particle that was at $r = 0$ at $t = 0$, and $G_d(r, t)$ the probability of observing other particles, we have

$$G_d(r, t) \approx \frac{\langle \Delta N(r, \Delta r; t) \rangle}{\rho \Delta\Omega(r, \Delta r)} \tag{8.109}$$

where $\Delta\Omega(r, \Delta r) \approx 4\pi r^2 \Delta r$ is the volume of a spherical shell with radius $r$ and thickness $\Delta r$, and $\Delta N(r, \Delta r; t)$ is the number of particles in the spherical shell at time $t$. The position of each particle at $t = 0$ is chosen as the origin in the evaluation of $G_d(r, t)$ and the average is taken over all the particles in the system. Note that this is different from the evaluation of $g(r)$, in which we always select a particle position as the origin and take the average over time. We can also take the average over all the particles in the evaluation of $g(r)$. Here $G_s(r, t)$ can be evaluated in a similar fashion. Because $G_s(r, t)$ represents the probability for a particle to be at a distance $r$ at time $t$ from its original position at $t = 0$, we can introduce

$$\langle \Delta^{2n}(t) \rangle = \frac{1}{N} \sum_{i=1}^{N} [r_i(t) - r_i(0)]^{2n} = \int r^{2n} G_s(r, t) dr \tag{8.110}$$

in the evaluation of the diffusion coefficient with $n = 1$. The diffusion coefficient can also be evaluated from the autocorrelation function

$$c(t) = \langle v(t) \cdot v(0) \rangle = \frac{1}{N} \sum_{i=1}^{N} [v_i(t) \cdot v_i(0)] \tag{8.111}$$

with

$$D = \frac{1}{3c(0)} \int_0^{\infty} c(t) dt \tag{8.112}$$

because the velocity of each particle at each time step $v_i(t)$ is known from the simulation. The velocity correlation function can also be used to obtain the power spectrum

$$P(\omega) = \frac{6}{\pi c(0)} \int_0^{\infty} c(t) \cos\omega t dt \tag{8.113}$$

which has many features similar to those of the phonon spectrum of the system: for example, a broad peak for the glassy state and sharp features for a crystalline state.

Thermodynamical quantities can also be evaluated from molecular dynamics simulations. For example, if a simulation is performed under the constant-pressure condition, we can obtain physical quantities such as the particle density, pair-distribution function, and so on, at different temperature. The inverse of the particle density is called the specific volume, denoted $V_P(T)$. The thermal expansion coefficient under the constant-pressure condition is then given by

$$\alpha_P = \frac{\partial V_P(T)}{\partial T} \tag{8.114}$$

which is quite different when the system is in a liquid phase than it is in a solid phase. Furthermore, we can calculate the temperature-dependent enthalpy

$$H = E + P\Omega \tag{8.115}$$

where $E$ is the internal energy given by

$$E = \sum_{i=1}^{N} \frac{m_i v_i^2}{2} + \sum_{i \neq j} V(r_{ij}) \tag{8.116}$$

with $P$ the pressure, and $\Omega$ the volume of the system. The specific heat under the constant-pressure condition is then obtained from

$$c_P = \frac{1}{N} \frac{\partial H}{\partial T} \tag{8.117}$$

The specific heat under the constant-volume condition can be derived from the fluctuation of the internal energy $\langle (\delta E)^2 \rangle = \langle [E - \langle E \rangle]^2 \rangle$ with time, given as

$$c_V = \frac{\langle (\delta E)^2 \rangle}{k_B T^2} \tag{8.118}$$

The isothermal compressibility $\kappa_T$ is then obtained from the identity

$$\kappa_T = \frac{T\Omega \alpha_P^2}{c_P - c_V} \tag{8.119}$$

which is also quite different for the liquid phase than for the solid phase. For more discussions on the molecular dynamics simulation of glass transition, see Yonezawa (1991).

Other aspects related to the structure and dynamics of a system can be studied through molecular dynamics simulations. The advantage of molecular dynamics over a typical stochastic simulation is that molecular dynamics can give all the information on the time dependence of the system, which is necessary for analyzing the structural and dynamical properties of the system. Molecular dynamics is therefore the method of choice in computer simulations of many-particle systems. However, stochastic simulations, such as Monte Carlo simulations, are sometimes easier to perform for some systems and are closely related to the simulations of quantum systems.

## 8.8 Ab Initio Molecular Dynamics

In this section, we outline a very interesting simulation scheme that combines the calculation of the electronic structure and the molecular dynamics simulation for a system. This is known as ab initio molecular dynamics, which was devised and put into practice by Car and Parrinello (1985).

The maturity of molecular dynamics simulation schemes and the great advances in computing capacity have made it possible to perform molecular dynamics simulations for amorphous materials, biopolymers, and other complex systems. However, in order to obtain an accurate description of a specific system, we have to know the precise behavior of the interactions among the particles, that is, the ions in the system. Electrons move much faster than ions because the electron mass is much smaller than that of an ion. The position dependence of the interactions among the ions in a given system is therefore determined by the distribution of the electrons (electronic structure) at the specific moment. Thus, a good approximation of the electronic structure in a calculation can be obtained with all the nuclei fixed in space for that moment. This is the essence of the Born–Oppenheimer approximation, which allows the degrees of freedom of the electrons to be treated separately from those of the ions.

In the past, the interactions among the ions were given in a parameterized form based on experimental data, quantum chemistry calculations, or the specific conditions of the system under study. All these procedures are limited due to the complexity of the electronic structure of the actual materials. We can easily obtain accurate parameterized interactions for the inert gases, such as Ar, but would have a lot of difficulties in obtaining an accurate parameterized interaction that can produce the various structures of ice correctly in the molecular dynamics simulation.

It seems that a combined scheme is highly desirable. We can calculate the many-body interactions among the ions in the system from the electronic structure calculated at every molecular dynamics time step and then determine the next configuration from such ab initio interactions. This can be achieved in principle, but in practice the scheme is restricted by the existing computing capacity. The combined method devised by Car and Parrinello (1985) was the first in its class and has been applied to the simulation of real materials.

### Density Functional Theory

The density functional theory (Hohenberg and Kohn, 1964; Kohn and Sham, 1965) was introduced as a practical scheme to cope with the many-electron effect in atoms, molecules, and solids. The theorem proved by Hohenberg and Kohn (1964) states that the ground-state energy of an interacting system is the optimized value of an energy functional $E[\rho(r)]$ of the electron density $\rho(r)$ and that the corresponding density distribution of the optimization is the unique ground-state density distribution. Symbolically, we can write

$$E[\rho(r)] = E_{ext}[\rho(r)] + E_H[\rho(r)] + E_K[\rho(r)] + E_{xc}[\rho(r)] \tag{8.120}$$

where $E_{ext}[\rho(r)]$ is the contribution from the external potential $U_{ext}(r)$ with

$$E_{ext}[\rho(r)] = \int U_{ext}(r)\rho(r) dr \tag{8.121}$$

$E_H[\rho(r)]$ is the Hartree type of contribution due to the electron–electron interaction, given by

$$E_H[\rho(r)] = \frac{1}{2} \int \frac{e^2 \rho(r')\rho(r)}{4\pi\varepsilon_0 |r' - r|} dr dr' \tag{8.122}$$

$E_K$ is the contribution of the kinetic energy, and $E_{xc}$ denotes the rest of the contributions and is termed the exchange–correlation energy functional.

In general, we can express the electron density in a spectral representation

$$\rho(r) = \sum_i \psi_i^\dagger(r)\psi_i(r) \tag{8.123}$$

where $\psi_i^\dagger(r)$ is the complex conjugate of the wavefunction $\psi_i(r)$ and the summation is over all the degrees of freedom, that is, all the occupied states with different spin orientations. Then the kinetic energy functional can be written as

$$E_K[\rho(r)] = -\frac{\hbar^2}{2m} \sum_i \int \psi_i^\dagger(r)\nabla^2\psi_i(r) dr \tag{8.124}$$

There is a constraint from the total number of electrons in the system, namely,

$$\int \rho(r) dr = N \tag{8.125}$$

which introduces the Lagrange multipliers into the variation. If we use the spectral representation of the density in the energy functional and apply the Euler equation with the Lagrange multipliers, we have

$$\frac{\delta E[\rho(r)]}{\delta \psi_i^\dagger(r)} - \varepsilon_i \psi_i(r) = 0 \tag{8.126}$$

which leads to the Kohn–Sham equation

$$\left(-\frac{\hbar^2}{2m}\nabla^2 + V_E(r)\right)\psi_i(r) = \varepsilon_i \psi_i(r) \tag{8.127}$$

where $V_E(r)$ is an effective potential given by

$$V_E(r) = U_{ext}(r) + V_H(r) + V_{xc}(r) \tag{8.128}$$

with

$$V_{xc}(r) = \frac{\delta E_{xc}[\rho(r)]}{\delta \rho(r)} \tag{8.129}$$

which cannot be obtained exactly. A common practice is to approximate it by its homogeneous density equivalent, the so-called local approximation, in which we assume that $V_{xc}(r)$ is given by the same quantity of a uniform electron gas with density equal to $\rho(r)$. This is termed the local density approximation. The local density approximation has been successfully applied to many physical systems, including atomic, molecular, and condensed-matter systems. The unexpected success of the local density approximation in materials research has made it a standard technique for calculating electronic properties of new materials and systems. The procedure for calculating the electronic structure with the local density approximation can be described in several steps. We first construct the local approximation of $V_{xc}(r)$ with a guessed density distribution. Then the Kohn–Sham equation is solved, and a new density distribution is constructed from the solution. With the new density distribution, we can improve $V_{xc}(r)$ and then solve the Kohn–Sham equation again. This procedure is repeated until convergence is reached. Interested readers can find detailed discussions on the density functional theory in many monographs or review articles, for example, Kohn and Vashishta (1983), and Jones and Gunnarsson (1989).

### The Car–Parrinello Simulation Scheme

The Hohenberg–Kohn energy functional forms the Born–Oppenheimer potential surface for the ions in the system. The idea of ab initio molecular dynamics is similar to the relaxation scheme we discussed in Chapter 7. We introduced a functional

$$U = \int \left[\frac{1}{2}\varepsilon(x)\left(\frac{d\psi(x)}{dx}\right)^2 - \rho(x)\psi(x)\right] dx \tag{8.130}$$

for the one-dimensional Poisson equation. Note that $\rho(x)$ here is the charge density instead of the particle density. The physical meaning of this functional is the electrostatic energy of the system. After applying the trapezoid rule to the integral and taking a partial derivative of $U$ with respect to $\phi_i$, we obtain the corresponding difference equation

$$(H_i + \rho_i)\psi_i = 0 \tag{8.131}$$

for the one-dimensional Poisson equation. Here $H_i \phi_i$ denotes $\varepsilon_{i+1/2}\phi_{i+1} + \varepsilon_{i-1/2}\phi_{i-1} - (\varepsilon_{i+1/2} + \varepsilon_{i-1/2})\phi_i$. If we combine the above equation with the relaxation scheme discussed in Section 7.5, we have

$$\psi_i^{(k+1)} = (1 - p)\psi_i^{(k)} + p(H_i + \rho_i + 1)\psi_i^{(k)} \tag{8.132}$$

which would optimize (minimize) the functional (the electrostatic energy) as $k \to \infty$. The indices $k$ and $k+1$ are for iteration steps, and the index $n$ is for the spatial points. The iteration can be interpreted as a fictitious time step, since we can rewrite the above equation as

$$\frac{\psi_i^{(k+1)} - \psi_i^{(k)}}{p} = (H_i + \rho_i)\psi_i^{(k)} \tag{8.133}$$

with $p$ acting like a fictitious time step. The solution converges to the true solution of the Poisson equation as $k$ goes to infinity if the functional $U$ decreases during the iterations.

The ab initio molecular dynamics is devised by introducing a fictitious time-dependent equation for the electron degrees of freedom:

$$\mu \frac{d^2\psi_i(r, t)}{dt^2} = -\frac{1}{2}\frac{\delta E[\rho(r, t); R_n]}{\delta \psi_i^\dagger(r, t)} + \sum_j \Lambda_{ij} \psi_j(r) \tag{8.134}$$

where $\mu$ is an adjustable parameter introduced for convenience, $\Lambda_{ij}$ is the Lagrange multiplier, introduced to ensure the orthonormal condition of the wavefunctions $\psi_i(r, t)$, and the summation is over all the occupied states. Note that the potential energy surface $E$ is a functional of the electron density as well as a function of the ionic coordinates $R_n$ for $n = 1, 2, \ldots, N_c$, with a total of $N_c$ ions in the system. In practice, we can also consider the first-order time derivative equation, with $d^2\psi_i(r, t)/dt^2$ replaced by the first-order derivative $d\psi_i(r, t)/dt$, because either the first-order or the second-order derivative will approach zero at the limit of convergence. Second-order derivatives were used in the original work of Car and Parrinello and were later shown to yield a fast convergence if a special damping term is introduced (Tassone, Mauri, and Car, 1994). The ionic degrees of freedom are then simulated from Newton's equation

$$M_n \frac{d^2R_n}{dt^2} = -\frac{\partial E[\rho(r, t); R_n]}{\partial R_n} \tag{8.135}$$

where $M_n$ and $R_n$ are the mass and the position vector of the $n$th particle. The advantage of ab initio molecular dynamics is that the electron degrees of freedom and the ionic degrees of freedom are simulated simultaneously by the above equations. Since its introduction by Car and Parrinello (1985), the method has been applied to many systems, especially those without a crystalline structure, namely, liquids and amorphous materials. We will not go into more detail on the method or its applications; interested readers can find them in the review by Tassone, Mauri, and Car (1994). Progress in ab initio molecular dynamics has also included mapping the Hamiltonian onto a tight-binding model in which the evaluation of the electron degrees of freedom is drastically simplified (Wang, Chan, and Ho, 1989). This approach has also been applied to many systems, for example, amorphous carbon and carbon clusters. More discussions on the method can be found in several review articles, for example, Oguchi and Sasaki (1991).

---

## Exercises

**8.1** Show that the Verlet algorithm preserves the time reversal of Newton's equation.

**8.2** Derive the velocity version of the Verlet algorithm and show that the position update has the same accuracy as in the original Verlet algorithm.

**8.3** Write a program that uses the velocity version of the Verlet algorithm to simulate the small clusters of ions (Na$^+$)$_n$(Cl$^-$)$_m$ for small $n$ and $m$. Use the empirical interaction potential given in Eq. (5.64) for the ions and set up the initial configuration as the equilibrium configuration. Assign initial velocities from the Maxwell distribution. Discuss the time dependence of the kinetic energy with different total energies.

**8.4** Explore the coexistence of the liquid and solid phases in a Lennard–Jones cluster that has an intermediate size of about 150 particles through the microcanonical molecular dynamics simulation. Analyze the melting process in the cluster and the size dependence of the coexistence region.

**8.5** A two-dimensional system can behave quite differently from its three-dimensional counterpart. Use the molecular dynamics technique to study a two-dimensional Lennard–Jones cluster of the intermediate size of about 100 particles. Do the liquid and solid phases coexist in any temperature region? Discuss the difference found between the three-dimensional and two-dimensional clusters.

**8.6** Develop a program with the fifth-order Gear predictor–corrector scheme and apply it to the damped pendulum under a sinusoidal driving force. Study the properties of the pendulum with different values of the parameters.

**8.7** Apply the fifth-order Gear scheme to study the long-time behavior of a classical helium atom in two dimensions. Explore different initial conditions. Is the system unstable or chaotic under certain initial conditions?

**8.8** Derive the Hoover equations from the Nosé Lagrangian. Show that the generalized Lagrangian given in Section 8.6 can provide the correct equations of motion to ensure the constraint of constant temperature as well as that of constant pressure.

**8.9** Develop a molecular dynamics program to study the structure of a cluster of identical charges inside a three-dimensional isotropic, harmonic trap. Under what condition does the cluster form a crystal? What happens if the system is confined in a plane?

**8.10** Show that the Parrinello–Rahman Lagrangian allows the shape of the simulation box to change, and derive equations of motion from it. Find the Lagrangian that combines the Parrinello–Rahman Lagrangian and Nosé Lagrangian and derive the equations of motion from this generalized Lagrangian.

**8.11** For quantum many-body systems, the n-body density function is defined by

$$\rho_n(r_1, r_2, \ldots, r_n) = \frac{1}{Z} \frac{N!}{(N-n)!} \int |\Psi(R)|^2 dr_{n+1} dr_{n+2} \cdots dr_N$$

where $\Psi(R)$ is the ground-state wavefunction of the many-body system and $Z$ is the normalization constant given by

$$Z = \int |\Psi(R)|^2 dr_1 dr_2 \cdots dr_N$$

The pair-distribution function is related to the two-body density function through

$$\rho(r)g(r, r')\rho(r') = \rho_2(r, r')$$

Show that

$$\int \rho(r)[\tilde{g}(r, r') - 1] dr = -1$$

where

$$\tilde{g}(r, r') = \int_0^1 g(r, r'; \lambda) d\lambda$$

with $g(r, r'; \lambda)$ as the pair-distribution function under the scaled interaction $V(r, r'; \lambda) = \lambda V(dr, r')$.

**8.12** Show that the exchange–correlation energy functional is given by

$$E_{xc}[\rho(r)] = \frac{1}{2} \int \rho(r)V(r, r')[\tilde{g}(r, r') - 1]\rho(r') dr dr'$$

with $\tilde{g}(r, dr')$ given from the last problem.
