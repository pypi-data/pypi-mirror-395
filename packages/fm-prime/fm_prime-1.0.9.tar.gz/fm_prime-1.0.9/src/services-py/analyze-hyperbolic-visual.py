"""
Visual Analysis of Hyperbolic Equation Approach
Explores mathematical patterns and properties through visualization
"""

import sys
sys.path.insert(0, 'src/services-py')

import matplotlib.pyplot as plt
import numpy as np
from prime_optimized import is_prime_optimized

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Hyperbolic Equation Approach: Visual Analysis\nm² - 9r² = 6n±1',
             fontsize=16, fontweight='bold')

# ============================================================================
# PLOT 1: Hyperbola Curves for Different n Values
# ============================================================================

ax1 = plt.subplot(3, 3, 1)
ax1.set_title('Hyperbola Curves: m² - 9r² = 6n+1')
ax1.set_xlabel('r')
ax1.set_ylabel('m')
ax1.grid(True, alpha=0.3)

# Plot hyperbolas for different n values
n_values = [1, 5, 10, 20, 50, 100]
colors = plt.cm.viridis(np.linspace(0, 1, len(n_values)))

for n, color in zip(n_values, colors):
    r_range = np.linspace(0, 50, 1000)
    # m² = 9r² + 6n + 1
    discriminant = 9 * r_range**2 + 6*n + 1
    m_positive = np.sqrt(discriminant)

    ax1.plot(r_range, m_positive, color=color, label=f'n={n}', alpha=0.7)

ax1.legend(fontsize=8)
ax1.set_xlim(0, 50)
ax1.set_ylim(0, 150)

# ============================================================================
# PLOT 2: Integer Solutions (r, m) for Composite Numbers
# ============================================================================

ax2 = plt.subplot(3, 3, 2)
ax2.set_title('Integer Solutions (r, m) for Composites')
ax2.set_xlabel('r')
ax2.set_ylabel('m')
ax2.grid(True, alpha=0.3)

# Find integer solutions for composite numbers up to 1000
composite_solutions = []
prime_solutions = []

for num in range(5, 1000):
    if num % 6 not in (1, 5):  # Not 6k±1
        continue

    n = (num - 1) // 6 if num % 6 == 1 else (num + 1) // 6

    # Try different r values
    for r in range(int(np.sqrt(n)) + 10):
        discriminant = 9*r*r + 6*n + 1
        m = int(np.sqrt(discriminant))

        if m*m == discriminant:  # Integer solution found
            check = m - 3*r - 1
            if check % 6 == 0 and check >= 6:
                # Valid solution - this number is composite
                if is_prime_optimized(num):
                    prime_solutions.append((r, m))
                else:
                    composite_solutions.append((r, m))
                break

if composite_solutions:
    comp_r, comp_m = zip(*composite_solutions)
    ax2.scatter(comp_r, comp_m, c='red', alpha=0.6, s=20, label='Composites')

if prime_solutions:
    prime_r, prime_m = zip(*prime_solutions)
    ax2.scatter(prime_r, prime_m, c='blue', alpha=0.6, s=20, label='Primes (edge cases)')

ax2.legend(fontsize=8)

# ============================================================================
# PLOT 3: Density of Integer Solutions
# ============================================================================

ax3 = plt.subplot(3, 3, 3)
ax3.set_title('Density of Solutions by n')
ax3.set_xlabel('n value')
ax3.set_ylabel('Number of integer solutions found')
ax3.grid(True, alpha=0.3)

n_range = range(1, 200)
solution_counts = []

for n in n_range:
    count = 0
    for r in range(int(np.sqrt(n) * 2) + 10):
        discriminant = 9*r*r + 6*n + 1
        m_squared = discriminant
        m = int(np.sqrt(m_squared))
        if m*m == m_squared:
            count += 1
    solution_counts.append(count)

ax3.plot(n_range, solution_counts, linewidth=2, color='purple')
ax3.fill_between(n_range, solution_counts, alpha=0.3, color='purple')

# ============================================================================
# PLOT 4: Factorization Pattern Visualization
# ============================================================================

ax4 = plt.subplot(3, 3, 4)
ax4.set_title('Factorization Patterns: 6k±1 Numbers')
ax4.set_xlabel('Number')
ax4.set_ylabel('Smallest Divisor Found')
ax4.grid(True, alpha=0.3)

numbers = []
divisors = []

for num in range(25, 500, 2):
    if num % 6 not in (1, 5):
        continue

    if num % 2 == 0:
        divisors.append(2)
        numbers.append(num)
        continue
    if num % 3 == 0:
        divisors.append(3)
        numbers.append(num)
        continue

    n = (num - 1) // 6 if num % 6 == 1 else (num + 1) // 6
    found = False

    for r in range(int(np.sqrt(num)) + 1):
        discriminant = 9*r*r + 6*n + 1
        m = int(np.sqrt(discriminant))

        if m*m == discriminant:
            check = m - 3*r - 1
            if check % 6 == 0 and check >= 6:
                divisor = check + 1
                divisors.append(divisor)
                numbers.append(num)
                found = True
                break

    if not found and not is_prime_optimized(num):
        # Find divisor by trial division for comparison
        for d in range(5, int(np.sqrt(num)) + 1, 2):
            if num % d == 0:
                divisors.append(d)
                numbers.append(num)
                break

if numbers:
    colors_map = ['green' if d < 100 else 'orange' if d < 200 else 'red'
                  for d in divisors]
    ax4.scatter(numbers, divisors, c=colors_map, alpha=0.6, s=10)

# ============================================================================
# PLOT 5: m vs r Relationship (Linear Bounds)
# ============================================================================

ax5 = plt.subplot(3, 3, 5)
ax5.set_title('Bounds: m ≈ 3r (from m² - 9r² ≈ 0)')
ax5.set_xlabel('r')
ax5.set_ylabel('m')
ax5.grid(True, alpha=0.3)

# Plot actual solutions
if composite_solutions:
    comp_r, comp_m = zip(*composite_solutions)
    ax5.scatter(comp_r, comp_m, c='red', alpha=0.6, s=20, label='Solutions')

# Plot theoretical bound: m = 3r
r_line = np.linspace(0, max(comp_r) if composite_solutions else 20, 100)
ax5.plot(r_line, 3*r_line, 'b--', linewidth=2, label='m = 3r (bound)')
ax5.plot(r_line, 3*r_line + 5, 'g--', linewidth=1, alpha=0.5, label='m = 3r + 5')
ax5.plot(r_line, 3*r_line - 5, 'g--', linewidth=1, alpha=0.5, label='m = 3r - 5')

ax5.legend(fontsize=8)

# ============================================================================
# PLOT 6: Success Rate vs Number Size
# ============================================================================

ax6 = plt.subplot(3, 3, 6)
ax6.set_title('Hyperbolic Detection Rate')
ax6.set_xlabel('Number Range')
ax6.set_ylabel('% Composites Detected')
ax6.grid(True, alpha=0.3)

ranges = [(10, 100), (100, 200), (200, 500), (500, 1000)]
detection_rates = []
range_labels = []

for start, end in ranges:
    total_composites = 0
    detected = 0

    for num in range(start, end):
        if num % 6 not in (1, 5):
            continue
        if is_prime_optimized(num):
            continue

        total_composites += 1

        # Try to detect with hyperbolic
        n = (num - 1) // 6 if num % 6 == 1 else (num + 1) // 6

        for r in range(int(np.sqrt(num)) + 1):
            discriminant = 9*r*r + 6*n + 1
            m = int(np.sqrt(discriminant))

            if m*m == discriminant:
                check = m - 3*r - 1
                if check % 6 == 0 and check >= 6:
                    detected += 1
                    break

    rate = (detected / total_composites * 100) if total_composites > 0 else 0
    detection_rates.append(rate)
    range_labels.append(f'{start}-{end}')

ax6.bar(range_labels, detection_rates, color='teal', alpha=0.7)
ax6.set_ylim(0, 100)
ax6.axhline(y=100, color='r', linestyle='--', alpha=0.3, label='Perfect detection')

# ============================================================================
# PLOT 7: Distribution of r values
# ============================================================================

ax7 = plt.subplot(3, 3, 7)
ax7.set_title('Distribution of r Values (First Solution)')
ax7.set_xlabel('r value')
ax7.set_ylabel('Frequency')
ax7.grid(True, alpha=0.3)

r_values = [r for r, m in composite_solutions]
ax7.hist(r_values, bins=30, color='steelblue', alpha=0.7, edgecolor='black')

# ============================================================================
# PLOT 8: Discriminant Analysis
# ============================================================================

ax8 = plt.subplot(3, 3, 8)
ax8.set_title('Perfect Squares: 9r² + 6n + 1')
ax8.set_xlabel('n')
ax8.set_ylabel('r at first perfect square')
ax8.grid(True, alpha=0.3)

n_values_ps = []
r_first_square = []

for n in range(1, 200):
    for r in range(50):
        discriminant = 9*r*r + 6*n + 1
        if int(np.sqrt(discriminant))**2 == discriminant:
            n_values_ps.append(n)
            r_first_square.append(r)
            break

ax8.scatter(n_values_ps, r_first_square, c='magenta', alpha=0.5, s=10)

# ============================================================================
# PLOT 9: Comparison: Hyperbolic vs Trial Division Speed
# ============================================================================

ax9 = plt.subplot(3, 3, 9)
ax9.set_title('Operations Required: Hyperbolic vs Trial')
ax9.set_xlabel('Number Size (n)')
ax9.set_ylabel('Number of Operations')
ax9.grid(True, alpha=0.3)

n_sizes = [10, 50, 100, 500, 1000, 5000]
hyp_ops = []
trial_ops = []

for n_size in n_sizes:
    # Hyperbolic: roughly sqrt(n) r values to check
    hyp_ops.append(int(np.sqrt(n_size)))

    # Trial division: roughly sqrt(n)/3 candidates to check (6k±1)
    trial_ops.append(int(np.sqrt(n_size) / 3))

ax9.plot(n_sizes, hyp_ops, 'o-', linewidth=2, markersize=8,
         label='Hyperbolic', color='red')
ax9.plot(n_sizes, trial_ops, 's-', linewidth=2, markersize=8,
         label='Trial Division (6k±1)', color='blue')
ax9.set_xscale('log')
ax9.set_yscale('log')
ax9.legend(fontsize=8)

plt.tight_layout()

# Save figure
output_file = 'hyperbolic_analysis.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✓ Visualization saved to: {output_file}")
print()

# ============================================================================
# TEXT ANALYSIS
# ============================================================================

print("=" * 70)
print("HYPERBOLIC EQUATION ANALYSIS")
print("=" * 70)
print()

print("KEY FINDINGS:")
print()

print("1. MATHEMATICAL STRUCTURE:")
print(f"   • Found {len(composite_solutions)} integer solutions for composites")
if composite_solutions:
    avg_r = np.mean([r for r, m in composite_solutions])
    avg_m = np.mean([m for r, m in composite_solutions])
    print(f"   • Average r value: {avg_r:.2f}")
    print(f"   • Average m value: {avg_m:.2f}")
    print(f"   • m/r ratio: {avg_m/avg_r if avg_r > 0 else 0:.2f} (close to 3)")

print()
print("2. DETECTION EFFICIENCY:")
for i, (start, end) in enumerate(ranges):
    print(f"   • Range [{start}, {end}]: {detection_rates[i]:.1f}% detected")

print()
print("3. PATTERN OBSERVATIONS:")
print("   • m² - 9r² = 6n+1 forms a family of hyperbolas")
print("   • Solutions cluster near m ≈ 3r line")
print("   • Density of solutions increases with n")
print(f"   • Most solutions have r < {max(r_values) if r_values else 0}")

print()
print("4. COMPARISON WITH TRIAL DIVISION:")
print("   • Both methods have O(√n) complexity")
print("   • Hyperbolic: Check r from 0 to ~√n")
print("   • Trial: Check divisors in 6k±1 up to √n")
print("   • Operations per iteration:")
print("     - Hyperbolic: multiply, add, sqrt, square, modulo")
print("     - Trial: single modulo operation")
print("   • Result: Trial division is simpler and hardware-optimized")

print()
print("5. INTERESTING PROPERTIES:")
print("   • The bound m ≈ 3r emerges naturally")
print("   • Solutions form predictable patterns")
print("   • Can visualize composite structure geometrically")
print("   • Educational value: shows algebraic approach to factorization")

print()
print("=" * 70)
print()

plt.show()
