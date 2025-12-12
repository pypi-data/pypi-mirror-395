import math
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def is_semi_prime(n, pattern_type):
    """
    Determine if a given index n corresponds to a semi-prime based on the equations.
    pattern_type: "6n+1" or "6n-1"
    """
    for k in range(1, n):  # Explore possible k values
        for kk in range(1, n):  # Explore possible kk values
            if pattern_type == "6n+1":
                if (6 * k + 1) * (6 * kk + 1) == 6 * n + 1:
                    return True
                if (6 * k - 1) * (6 * kk - 1) == 6 * n + 1:
                    return True
            elif pattern_type == "6n-1":
                if (6 * k - 1) * (6 * kk + 1) == 6 * n - 1:
                    return True
                if (6 * k + 1) * (6 * kk - 1) == 6 * n - 1:
                    return True
    return False

def classify_indices(max_n):
    """
    Classify indices n into primes and semi-primes using fractal-like logic.
    """
    primes1 = []
    semi_primes1 = []

    primes2 = []
    semi_primes2 = []
    for n in range(1, max_n + 1):
        pattern1 = 6*n+1
        pattern2 = 6*n-1
        if is_semi_prime(n, "6n+1"):
            semi_primes1.append(pattern1)
        else:
            primes1.append(pattern1)
        if is_semi_prime(n, "6n-1"):
            semi_primes2.append(pattern2)
        else:
            primes2.append(pattern2)

    return primes1, semi_primes1, primes2, semi_primes2

def plot_fractal(primes1, semi_primes1, primes2, semi_primes2 , max_n):
    """Visualize the fractal-like structure of primes and semi-primes."""
    plt.figure(figsize=(12, 8))

    # Primes
    primes_x = [2,3]
    primes_y = [0,0]
    for n in primes1:
        primes_x.append(n)
        primes_y.append((n-1)//6)
    
    for n in primes2:
        primes_x.append(n)
        primes_y.append((n+1)//6)
    

    # Semi-Primes
    semi_primes_x = []
    semi_primes_y = []
    for n in semi_primes1:
        semi_primes_x.append(n)
        semi_primes_y.append((n-1)//6)

    for n in semi_primes2:
        semi_primes_x.append(n)
        semi_primes_y.append((n+1)//6)
    # Plot primes
    plt.scatter(primes_x, primes_y, color="blue", label="Primes", s=10)

    # Plot semi-primes
    plt.scatter(semi_primes_x, semi_primes_y, color="orange", label="Semi-Primes", s=10)

    # Plot setup
    plt.title(f"Fractal-Like Visualization of 6n ± 1 Patterns (Up to n={max_n})")
    plt.xlabel("Index (n)")
    plt.ylabel("Numbers (6n ± 1)")
    plt.legend()
    plt.grid()
    plt.show()

# Example:
# if __name__ == "__main__":
#     # Parameters
#     max_n = 10000//6  # Maximum index n to consider

#     # Classify indices
#     primes1, semi_primes1, primes2, semi_primes2 = classify_indices(max_n)
#     print(f"Prime count: {len(primes1) + len(primes2) + 2}")

#     # Plot fractal-like visualization
#     plot_fractal(primes1, semi_primes1, primes2, semi_primes2, max_n)
#
    
def generate_patterns(max_k):
    """
    Generate values for the four equations based on given range of k and kk.
    """
    data = {
        "6k.kk+k+kk": [],
        # "6k.kk-k-kk": [],
        # "6k.kk+k-kk": [],
        # "6k.kk-k+kk": []
    }

    for k in range(1, max_k + 1):
        for kk in range(1, max_k + 1):
            data["6k.kk+k+kk"].append((k, kk, 6 * k * kk + k + kk))
            # data["6k.kk-k-kk"].append((k, kk, 6 * k * kk - k - kk))
            # data["6k.kk+k-kk"].append((k, kk, 6 * k * kk + k - kk))
            # data["6k.kk-k+kk"].append((k, kk, 6 * k * kk - k + kk))

    return data

def plot_cartesian(data):
    """
    Plot the patterns in Cartesian coordinates.
    """
    plt.figure(figsize=(12, 8))
    for pattern, values in data.items():
        x, y = zip(*[(kk, n) for k, kk, n in values])  # kk as x and n as y
        plt.scatter(x, y, label=pattern, s=10)

    plt.title(f"Patterns in Cartesian Coordinates (kk vs. n)")
    plt.xlabel("kk")
    plt.ylabel("n")
    plt.legend()
    plt.grid()
    plt.show()

def plot_polar(data):
    """
    Plot the patterns in Polar coordinates.
    """
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': 'polar'})
    for pattern, values in data.items():
        r = [n for k, kk, n in values]  # Radius is n
        theta = [np.arctan2(k, kk) for k, kk, n in values]  # Angle based on k and kk
        ax.scatter(theta, r, label=pattern, s=10)

    ax.set_title(f"Patterns in Polar Coordinates")
    ax.legend()
    plt.show()

# Example:
# if __name__ == "__main__":
#     max_k = 50  # Maximum range for k and kk

#     # Generate data
#     patterns = generate_patterns(max_k)

#     # Plot in Cartesian Coordinates
#     plot_cartesian(patterns)

#     # Plot in Polar Coordinates
#     plot_polar(patterns)

def generate_patterns_from_n(max_n):
    """
    Generate (k, kk) values for given range of n based on the four equations.
    """
    data = {
        "6k.kk+k+kk": [],
        "6k.kk-k-kk": [],
        "6k.kk+k-kk": [],
        "6k.kk-k+kk": []
    }

    for n in range(1, max_n + 1):
        for k in range(1, int(np.sqrt(n)) + 1):  # Iterate up to sqrt(n) for efficiency
            for pattern in data.keys():
                # Solve each equation for kk and check if kk is an integer
                if pattern == "6k.kk+k+kk":
                    kk = (n - 6 * k * k - k) / (6 * k + 1)
                elif pattern == "6k.kk-k-kk":
                    kk = (n - 6 * k * k + k) / (6 * k - 1)
                elif pattern == "6k.kk+k-kk":
                    kk = (n - 6 * k * k - k) / (6 * k - 1)
                elif pattern == "6k.kk-k+kk":
                    kk = (n - 6 * k * k + k) / (6 * k + 1)
                else:
                    continue
                
                # If kk is an integer, add the pair (k, kk) with n
                if kk.is_integer() and kk > 0:
                    data[pattern].append((k, int(kk), n))

    return data

def plot_cartesian_n(data):
    """
    Plot the (k, kk) values in Cartesian coordinates for each pattern.
    """
    plt.figure(figsize=(12, 8))
    for pattern, values in data.items():
        x, y = zip(*[(k, kk) for k, kk, n in values])  # k as x and kk as y
        plt.scatter(x, y, label=pattern, s=10)

    plt.title(f"Patterns in Cartesian Coordinates (k vs. kk)")
    plt.xlabel("k")
    plt.ylabel("kk")
    plt.legend()
    plt.grid()
    plt.show()

def plot_polar_n(data):
    """
    Plot the patterns in Polar coordinates (k, kk) for each pattern.
    """
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': 'polar'})
    for pattern, values in data.items():
        r = [np.sqrt(k**2 + kk**2) for k, kk, n in values]  # Radius based on k and kk
        theta = [np.arctan2(kk, k) for k, kk, n in values]  # Angle based on k and kk
        ax.scatter(theta, r, label=pattern, s=10)

    ax.set_title(f"Patterns in Polar Coordinates")
    ax.legend()
    plt.show()

# Example
# if __name__ == "__main__":
#     max_n = 500  # Maximum range for n

#     # Generate data
#     patterns = generate_patterns_from_n(max_n)

#     # Plot in Cartesian Coordinates
#     plot_cartesian_n(patterns)

#     # Plot in Polar Coordinates
#     plot_polar_n(patterns)

def plot_cartesian_interactive(data):
    """
    Plot the patterns in Cartesian coordinates using Plotly for interactive visualization.
    """
    fig = go.Figure()

    for pattern, values in data.items():
        x, y = zip(*[(kk, n) for k, kk, n in values])  # kk as x and n as y
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=pattern))

    fig.update_layout(
        title="Patterns in Cartesian Coordinates (kk vs. n)",
        xaxis_title="kk",
        yaxis_title="n",
        legend_title="Patterns",
        template="plotly_white",
    )
    fig.show()

def plot_polar_interactive(data):
    """
    Plot the patterns in Polar coordinates using Plotly for interactive visualization.
    """
    fig = go.Figure()

    for pattern, values in data.items():
        r = [n for k, kk, n in values]  # Radius is n
        theta = [np.arctan2(k, kk) for k, kk, n in values]  # Angle based on k and kk
        fig.add_trace(go.Scatterpolar(r=r, theta=theta, mode='markers', name=pattern))

    fig.update_layout(
        title="Patterns in Polar Coordinates",
        polar=dict(radialaxis=dict(title="n")),
        legend_title="Patterns",
        template="plotly_white",
    )
    fig.show()

# if __name__ == "__main__":
#     max_n = 20  # Maximum range for n

#     # Generate data
#     patterns = generate_patterns(max_n)

#     # Plot Cartesian with interactive toggling
#     plot_cartesian_interactive(patterns)

#     # Plot Polar with interactive toggling
#     plot_polar_interactive(patterns)


def find_integer_n(step_size=0.00001, max_theta=2 * np.pi):
    results = []
    theta_values = np.arange(0, max_theta, step_size)
    
    for theta in theta_values:
        numerator = 1 - np.sqrt(2) * np.sin(theta + np.pi / 4)
        denominator = 3 * np.sin(2 * theta)
        
        # Avoid division by zero
        if np.abs(denominator) < 1e-10:
            continue
        
        n = numerator / denominator
        
        # Check if n is close to an integer
        if n > 0 and np.isclose(n, round(n), atol=1e-5):
            results.append((theta, int(round(n))))
    
    return results

# Find and print results
results = find_integer_n()
print(f"results: {results}")
for theta, n in results:
    print(f"Theta: {theta:.4f}, n: {n}")