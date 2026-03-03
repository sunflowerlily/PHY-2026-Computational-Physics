import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Logistic map function
def logistic_map(x, r):
    """Calculate the next value of the logistic map"""
    return r * x * (1 - x)

# Derivative of logistic map
def logistic_map_derivative(x, r):
    """Calculate the derivative of the logistic map"""
    return r * (1 - 2 * x)

# Generate logistic map sequence
def generate_sequence(r, x0, n_iterations):
    """Generate a logistic map sequence of specified length"""
    sequence = np.zeros(n_iterations)
    sequence[0] = x0
    for i in range(1, n_iterations):
        sequence[i] = logistic_map(sequence[i-1], r)
    return sequence

# Calculate Lyapunov exponent for logistic map
def calculate_lyapunov_exponent(r, x0, n_iterations):
    """Calculate Lyapunov exponent for logistic map"""
    x = x0
    lyapunov_sum = 0.0
    
    # Transient phase
    for _ in range(1000):
        x = logistic_map(x, r)
    
    # Calculate Lyapunov exponent
    for _ in range(n_iterations):
        x = logistic_map(x, r)
        lyapunov_sum += np.log(np.abs(logistic_map_derivative(x, r)))
    
    return lyapunov_sum / n_iterations

# Generate bifurcation diagram data
def generate_bifurcation_diagram(r_values, x0, n_transient, n_iterations):
    """Generate bifurcation diagram data"""
    x_values = []
    r_plot = []
    
    for r in r_values:
        # First generate a transient to remove initial unstable values
        x = x0
        for _ in range(n_transient):
            x = logistic_map(x, r)
        
        # Then record stable values
        for _ in range(n_iterations):
            x = logistic_map(x, r)
            x_values.append(x)
            r_plot.append(r)
    
    return r_plot, x_values

# Main function
def main():
    # Parameter settings
    x0 = 0.5  # Initial value
    n_iterations = 10000  # Number of iterations
    n_transient = 1000  # Number of transient iterations
    
    # Generate r values for bifurcation diagram and Lyapunov exponent
    r_min = 2.8
    r_max = 4.0
    n_r = 1000
    r_values = np.linspace(r_min, r_max, n_r)
    
    # 1. Generate bifurcation diagram data
    print("Generating bifurcation diagram data...")
    r_plot, x_values = generate_bifurcation_diagram(r_values, x0, n_transient, 100)
    
    # 2. Calculate Lyapunov exponents
    print("Calculating Lyapunov exponents...")
    lyapunov_exponents = []
    for r in r_values:
        lyapunov = calculate_lyapunov_exponent(r, x0, 10000)
        lyapunov_exponents.append(lyapunov)
    
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    # 3. Plot bifurcation diagram
    ax1.scatter(r_plot, x_values, s=0.1, c='k')
    ax1.set_title('Logistic Map Bifurcation Diagram')
    ax1.set_xlabel('r')
    ax1.set_ylabel('Stable x values')
    ax1.set_xlim(r_min, r_max)
    ax1.grid(True, alpha=0.3)
    
    # 4. Plot Lyapunov exponents
    ax2.plot(r_values, lyapunov_exponents, 'r-', linewidth=1)
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    ax2.set_title('Lyapunov Exponent of Logistic Map')
    ax2.set_xlabel('r')
    ax2.set_ylabel('Lyapunov Exponent')
    ax2.set_xlim(r_min, r_max)
    ax2.set_ylim(-2, 1)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('logistic_bifurcation_lyapunov.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()