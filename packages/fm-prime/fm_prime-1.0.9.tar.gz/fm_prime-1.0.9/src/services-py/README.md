# Python Prime Number Services

Comprehensive Python implementations for prime number computations using multiple mathematical approaches including novel methods.

---

## Table of Contents

- [Overview](#overview)
- [Core Modules](#core-modules)
- [Optimized Modules](#optimized-modules)
- [Advanced Methods](#advanced-methods)
- [Performance Comparison](#performance-comparison)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)

---

## Overview

This directory contains Python implementations for prime number operations, organized into three categories:

### 1. **Original Implementations** (File-based approach)
- `prime.py` - Basic prime validation and generation
- `primeUtils.py` - File-based storage and utilities
- `primeIndex.py` - Non-prime index calculations
- `primeText.py` - Text file-based prime operations
- `primePlot.py` - Visualization tools
- `primeFractal.py` - Fractal pattern analysis
- `textUtils.py` - Text file utilities

### 2. **Optimized Implementations** (Performance-focused)
- `prime_optimized.py` - Fast algorithms (Sieve, 6k±1, Miller-Rabin, Wheel-30)
- `wheel210.py` - Wheel-210 factorization (23% candidates)
- `primeUtils_optimized.py` - Optimized utility functions
- `prime_hybrid.py` - Intelligent hybrid approach
- `fm_prime/prime_hyperbolic_optimized.py` 🚀⭐ - Production-ready hyperbolic method with file-level granular caching (2.5x faster)

### 3. **Novel Methods** (Research & Educational)
- `prime_hyperbolic.py` - Hyperbolic equation approach (original research version)
- `analyze-hyperbolic-visual.py` - Visual analysis with matplotlib
- `analyze-hyperbolic-patterns.py` - Pattern analysis and CSV export

---

## Core Modules

### prime.py

**Purpose**: Basic prime number validation and classification

**Key Functions**:

```python
is_prime(num)                 # Basic primality test (6k±1 pattern)
is_sophie_prime(num)          # Sophie Germain prime check
is_mersenne_prime(num)        # Mersenne prime validation
is_twin_prime(num)            # Twin prime identification
is_isolated_prime(num)        # Isolated prime check
primes_count(num)             # Count primes up to num
list_primes(num)              # List all primes up to num
primes_in_range(start, end)   # Primes in specific range
primes_in_chunks(start, end, size) # Chunked prime generation
prime_factorization(num)      # Prime factorization
```

**Example**:
```python
from prime import is_prime, list_primes, prime_factorization

print(is_prime(17))                    # True
print(list_primes(20))                 # [2, 3, 5, 7, 11, 13, 17, 19]
print(prime_factorization(100))        # "2**2 * 5**2"
```

### primeUtils.py

**Purpose**: File-based storage and retrieval of prime data

**Key Functions**:

```python
create_prime_folder(number)           # Create storage folder
write_prime_file(folder, filename, data) # Write prime data
get_sorted_prime_folders()            # Get all prime folders
get_last_prime_folder()               # Get most recent folder
check_divisor_from_files(num, folder) # Check divisibility from files
generate_primes_up_to(number)         # Generate and store primes
```

**Example**:
```python
from primeUtils import generate_primes_up_to, get_last_prime_folder

generate_primes_up_to(10000)
last_folder = get_last_prime_folder()
print(f"Latest primes stored in: {last_folder}")
```

### primeText.py

**Purpose**: Text file-based prime operations for large-scale computations

**Key Functions**:

```python
generate_primes(number)                    # Generate primes to file
is_prime_from_text_files(num)             # Check primality using files
prime_range(start, end)                   # List primes in range
count_prime_in_range(start, end)          # Count primes in range
get_all_divisors(number)                  # Find all divisors
generate_primes_files(num)                # Generate prime files
count_primes_up_to(limit)                 # Count using Sieve
```

**Example**:
```python
from primeText import generate_primes, is_prime_from_text_files, get_all_divisors

generate_primes(100000)
print(is_prime_from_text_files(999983))   # True
print(get_all_divisors(100))              # [1, 2, 4, 5, 10, 20, 25, 50, 100]
```

---

## Optimized Modules

### prime_optimized.py ⚡

**Purpose**: High-performance prime operations with multiple algorithms

**Core Algorithms**:

#### 1. Sieve of Eratosthenes
```python
sieve_of_eratosthenes(limit)       # O(n log log n) - fastest for bulk generation
segmented_sieve(start, end)        # Memory-efficient for ranges
```

#### 2. 6k±1 Pattern (Wheel-6)
```python
is_prime_optimized(num)            # 3x faster than naive trial division
smallest_divisor_optimized(num)    # Find smallest divisor with 6k±1
prime_factorization_optimized(num) # Optimized factorization
```

#### 3. Miller-Rabin Test
```python
miller_rabin(n, k=20)              # Probabilistic test for large primes
is_prime_fast(num, threshold=10000) # Auto-choose best algorithm
```

#### 4. Wheel-30 Factorization
```python
Wheel30.generate_candidates(start, end)  # Generate 27% of candidates
Wheel30.primes_in_range(start, end)      # Find primes in range
```

#### High-Level API
```python
list_primes_optimized(limit, method='auto')      # Auto-select best method
primes_in_range_optimized(start, end, method='auto') # Optimized range search
primes_count_optimized(limit)                    # Fast prime counting
```

**Example**:
```python
from prime_optimized import (
    sieve_of_eratosthenes,
    is_prime_optimized,
    miller_rabin,
    Wheel30
)

# Sieve for bulk generation
primes = sieve_of_eratosthenes(100000)
print(f"Found {len(primes)} primes")

# 6k±1 for medium numbers
print(is_prime_optimized(999983))  # True

# Miller-Rabin for very large numbers
print(miller_rabin(1000000007))     # True

# Wheel-30 for range generation
primes = Wheel30.primes_in_range(1000, 2000)
print(f"Found {len(primes)} primes in range")
```

**Complexity**:
- Sieve: O(n log log n)
- 6k±1 trial division: O(√n / 3)
- Miller-Rabin: O(k log³ n)
- Wheel-30: Tests 27% of candidates

### wheel210.py ⚡⚡

**Purpose**: Maximum performance with Wheel-210 factorization

**Key Features**:
- Tests only 23% of candidates (vs 27% for Wheel-30, 33% for 6k±1)
- Eliminates multiples of 2, 3, 5, and 7
- 48 spokes per 210-number wheel

**API**:

```python
# Wheel-210 class
Wheel210.generate_candidates(start, end)  # Generate prime candidates
Wheel210.next_candidate(current)          # Get next candidate
Wheel210.SPOKES                           # 48 residues mod 210

# Functions
sieve_wheel210(limit)                     # Sieve using Wheel-210
is_prime_wheel210(n)                      # Primality test with Wheel-210
primes_in_range_wheel210(start, end)      # Primes in range
benchmark_wheels(limit)                   # Compare Wheel-6/30/210
```

**Example**:
```python
from wheel210 import Wheel210, sieve_wheel210

# Generate all primes up to 1,000,000
primes = sieve_wheel210(1000000)
print(f"Found {len(primes)} primes")

# Generate candidates in range
candidates = list(Wheel210.generate_candidates(1000, 1100))
print(f"Testing only {len(candidates)} candidates")

# Compare wheel methods
results = benchmark_wheels(100000)
print(f"Wheel-210 tests {results['wheel210']['percentage']:.1f}% of numbers")
```

**Performance**:
- Wheel-6 (6k±1): 33.3% candidates
- Wheel-30: 26.7% candidates
- Wheel-210: 22.9% candidates
- **30% fewer tests than 6k±1!**

### primeUtils_optimized.py

**Purpose**: Optimized utility functions

**Key Functions**:

```python
find_next_candidate(num)              # Get next 6k±1 candidate
are_twin_primes(p1, p2)               # Check if twin primes
get_prime_gaps(primes)                # Calculate gaps between primes
nth_prime(n)                          # Find nth prime number
prime_pi(x)                           # Prime counting function
```

**Example**:
```python
from primeUtils_optimized import find_next_candidate, nth_prime, prime_pi

# Navigate 6k±1 pattern
current = 5
for _ in range(5):
    print(current)
    current = find_next_candidate(current)
# Output: 5, 7, 11, 13, 17

# Find specific prime
print(f"The 100th prime is: {nth_prime(100)}")  # 541

# Count primes up to x
print(f"There are {prime_pi(1000)} primes below 1000")  # 168
```

---

## Advanced Methods

### prime_hybrid.py 🚀

**Purpose**: Intelligent hybrid approach combining multiple methods

**Key Class**: `HybridPrimeFinder`

**Features**:
- Pre-computed primes for instant lookup (default: 100,000)
- Auto-selects best algorithm based on number size
- 6k±1 pattern for candidate generation
- Miller-Rabin for very large numbers

**API**:

```python
finder = HybridPrimeFinder(precompute_limit=100000)

# Methods
finder.is_prime(n)                           # Intelligent primality test
finder.find_nth_prime(n)                     # Find nth prime
finder.find_primes_in_range(start, end)      # Primes in range
finder.find_twin_primes_in_range(start, end) # Twin prime pairs
finder.find_sophie_germain_primes_in_range(start, end) # Sophie primes
```

**Algorithm Selection**:
- `n ≤ 100,000`: Pre-computed lookup (instant)
- `100,000 < n < 10,000,000`: 6k±1 trial division
- `n ≥ 10,000,000`: Miller-Rabin test

**Example**:
```python
from prime_hybrid import HybridPrimeFinder

finder = HybridPrimeFinder(precompute_limit=100000)

# Auto-selects best method
print(finder.is_prime(997))           # Lookup (instant)
print(finder.is_prime(1000003))       # 6k±1 trial division
print(finder.is_prime(1000000007))    # Miller-Rabin

# Find twin primes
twins = finder.find_twin_primes_in_range(100, 1000)
print(f"Found {len(twins)} twin prime pairs")
# Example: [(101, 103), (107, 109), (137, 139), ...]

# Find Sophie Germain primes
sophie = finder.find_sophie_germain_primes_in_range(100, 1000)
print(f"Found {len(sophie)} Sophie Germain primes")
```

**Additional Functions**:

```python
sieve_6k_optimized(limit)                     # 6k±1 sieve (3x less memory)
find_primes_6k_miller_rabin(start, end)       # 6k±1 + Miller-Rabin combo
```

### prime_hyperbolic.py 🔍

**Purpose**: Novel hyperbolic equation approach for primality testing

**Mathematical Foundation**:

For **6n+1** numbers:
```
If composite: (6k+1)(6kk+1) = 6n+1
Derivation: (m - 3r)(m + 3r) = 6n+1
Equation: m² - 9r² = 6n+1
Check: m = √(9r² + 6n + 1) must be integer
```

For **6n-1** numbers:
```
If composite: (6k-1)(6kk-1) = 6n-1
Derivation: (3r - m)(3r + m) = 6n-1
Equation: 9r² - m² = 6n-1
Check: m = √(9r² - 6n + 1) must be integer
```

**API**:

```python
# Core functions
division_hyperbolic(num)        # Find smallest divisor
is_prime_hyperbolic(num)        # Check primality
factorize_hyperbolic(num)       # Complete factorization
factors_to_string(factors)      # Format factorization

# Internal (trend-specific)
division_first_trend(num, n)    # For 6n+1 numbers
division_second_trend(num, n)   # For 6n-1 numbers
isqrt(n)                        # Integer square root
```

**Example**:
```python
from prime_hyperbolic import (
    is_prime_hyperbolic,
    factorize_hyperbolic,
    factors_to_string,
    demonstrate
)

# Check primality
print(is_prime_hyperbolic(143))     # False (11 × 13)
print(is_prime_hyperbolic(1517))    # True

# Factorize
factors = factorize_hyperbolic(2021)
print(factors)                      # {43: 1, 47: 1}
print(factors_to_string(factors))   # "43 × 47"

# Run full demonstration
demonstrate()
```

**Properties**:
- ✅ Mathematically elegant (geometry meets number theory)
- ✅ Educational value (shows alternative perspective)
- ⚠️ Similar O(√n) complexity to trial division
- ⚠️ More operations per iteration (sqrt, multiply, modulo)
- 🔍 Potentially novel formulation (requires literature review)

**Key Insight**:
Instead of doing trial division, we check if certain square roots are integers. If √(9r² + 6n + 1) is an integer satisfying constraints, we've found a divisor without explicit division!

**Constraints**:
- For 6n+1 (first): 7r ≤ n - 8
- For 6n+1 (second): r² ≤ n
- For 6n-1 (first): 7r ≤ n + 2
- For 6n-1 (second): r² ≤ n

### Analysis Tools

#### analyze-hyperbolic-visual.py

**Purpose**: Generate 9-panel visualization of hyperbolic patterns

**Generates**:
1. Hyperbola curves for different n values
2. Integer solutions (r, m) scatter plot
3. Density of solutions by n
4. Factorization patterns
5. m vs r relationship (linear bounds)
6. Detection rate by number size
7. Distribution of r values
8. Perfect square discriminant analysis
9. Operations comparison

**Output**: `hyperbolic_analysis.png`

**Usage**:
```bash
python analyze-hyperbolic-visual.py
```

**Requirements**: matplotlib, numpy

#### analyze-hyperbolic-patterns.py

**Purpose**: Text-based pattern analysis with CSV export

**Analysis Includes**:
1. Integer solutions for composites
2. Pattern analysis (m/r ratios, bounds)
3. Geometric interpretation
4. Comparison with trial division
5. Unique mathematical insights
6. Potential research directions
7. Publishability assessment

**Outputs**:
- `hyperbolic_solutions.csv` - Integer solution data
- `hyperbola_curves.csv` - Curve data for plotting

**Usage**:
```bash
python analyze-hyperbolic-patterns.py
```

---

## Performance Comparison

| Method | Complexity | Candidates Tested | Best Use Case |
|--------|-----------|------------------|---------------|
| **Sieve of Eratosthenes** | O(n log log n) | 100% (marks all) | All primes up to N |
| **6k±1 Trial Division** | O(√n / 3) | 33% | Single prime checks (< 10⁶) |
| **Wheel-30** | O(√n / 3.7) | 27% | Better performance |
| **Wheel-210** | O(√n / 4.4) | 23% | Maximum performance |
| **Miller-Rabin** | O(k log³ n) | Variable | Very large primes (> 10⁶) |
| **Hyperbolic** | O(√n) | 33% | Educational/Research |

**Speedup Examples** (for primes up to 100,000):
- Sieve vs Trial Division: ~100x faster
- Wheel-210 vs 6k±1: ~30% fewer tests
- Miller-Rabin (large n): ~1000x faster

**Memory Usage**:
- Traditional Sieve: O(n)
- 6k±1 Sieve: O(n/3)
- Wheel-210 Sieve: O(n/4.4)

---

## Quick Start

### Basic Usage

```python
# 1. Simple primality check
from prime_optimized import is_prime_optimized

print(is_prime_optimized(17))  # True

# 2. Generate all primes up to N
from prime_optimized import sieve_of_eratosthenes

primes = sieve_of_eratosthenes(1000)
print(f"Found {len(primes)} primes")

# 3. Large prime testing
from prime_optimized import miller_rabin

print(miller_rabin(1000000007))  # True

# 4. Hybrid approach (recommended)
from prime_hybrid import HybridPrimeFinder

finder = HybridPrimeFinder()
print(finder.is_prime(999983))  # Auto-selects best method
```

### Advanced Usage

```python
# 1. Maximum performance with Wheel-210
from wheel210 import sieve_wheel210

primes = sieve_wheel210(1000000)
print(f"Found {len(primes)} primes (23% candidates tested)")

# 2. Range operations
from prime_optimized import Wheel30

primes = Wheel30.primes_in_range(1000, 2000)
print(f"Primes in range: {len(primes)}")

# 3. Specialized prime types
from prime_hybrid import HybridPrimeFinder

finder = HybridPrimeFinder()
twins = finder.find_twin_primes_in_range(100, 1000)
sophie = finder.find_sophie_germain_primes_in_range(100, 1000)

# 4. Hyperbolic approach (educational)
from prime_hyperbolic import is_prime_hyperbolic, factorize_hyperbolic

print(is_prime_hyperbolic(143))  # False
print(factorize_hyperbolic(143)) # {11: 1, 13: 1}
```

---

## API Reference

### Method Selection Guide

```python
# For single prime check (< 1 million):
from prime_optimized import is_prime_optimized
result = is_prime_optimized(999983)

# For single prime check (> 1 million):
from prime_optimized import miller_rabin
result = miller_rabin(1000000007, k=20)

# For all primes up to N:
from prime_optimized import sieve_of_eratosthenes
primes = sieve_of_eratosthenes(100000)

# For maximum performance (all primes up to N):
from wheel210 import sieve_wheel210
primes = sieve_wheel210(1000000)

# For primes in range [a, b]:
from prime_optimized import Wheel30
primes = Wheel30.primes_in_range(1000, 2000)

# For intelligent auto-selection:
from prime_hybrid import HybridPrimeFinder
finder = HybridPrimeFinder()
result = finder.is_prime(n)  # Auto-selects best method
```

### Import Quick Reference

```python
# Optimized methods
from prime_optimized import (
    sieve_of_eratosthenes,      # Bulk generation
    is_prime_optimized,          # Single check (6k±1)
    miller_rabin,                # Probabilistic test
    Wheel30,                     # 27% candidates
    list_primes_optimized,       # High-level API
    primes_in_range_optimized,   # High-level API
)

# Maximum performance
from wheel210 import (
    Wheel210,                    # 23% candidates
    sieve_wheel210,              # Fastest sieve
    is_prime_wheel210,           # Wheel-210 primality
)

# Hybrid approach
from prime_hybrid import (
    HybridPrimeFinder,           # Intelligent finder
    sieve_6k_optimized,          # 6k±1 sieve
)

# Hyperbolic method
from prime_hyperbolic import (
    is_prime_hyperbolic,         # Hyperbolic primality
    division_hyperbolic,         # Find divisor
    factorize_hyperbolic,        # Complete factorization
)

# Original methods (file-based)
from prime import (
    is_prime,                    # Basic primality
    list_primes,                 # List generation
    prime_factorization,         # Factorization
)
```

---

## Performance Tips

1. **For bulk generation**: Use `sieve_wheel210()` for maximum speed
2. **For single checks < 10⁶**: Use `is_prime_optimized()` (6k±1)
3. **For single checks > 10⁶**: Use `miller_rabin()` with k=20
4. **For ranges**: Use `Wheel30.primes_in_range()`
5. **For convenience**: Use `HybridPrimeFinder` (auto-selects)
6. **For education**: Explore `prime_hyperbolic.py`

---

## Examples

For complete working examples with detailed demonstrations, see the **[examples/](../../examples/)** directory:

```bash
# Run Python hyperbolic caching example
python examples/example_hyperbolic_optimized.py
```

**The examples demonstrate:**
- Generating primes with file-level granular caching
- Checking individual numbers for primality
- Finding all divisors of a number
- Checking cache status and performance
- Cache management utilities
- Real-world usage patterns

See **[examples/README.md](../../examples/README.md)** for complete documentation with both Python and JavaScript usage patterns.

---

## Testing

Run comprehensive tests:

```bash
# Test all Python methods
python ../test-all-methods.py

# Test hyperbolic analysis
python analyze-hyperbolic-patterns.py
python analyze-hyperbolic-visual.py
```

---

## Author

**Farid Masjedi**

GitHub: [Farid Masjedi](https://github.com/faridmasjedi)

---

## Version History

- **Version 2.0** (2024-12-03)
  - Added optimized implementations
  - Added Wheel-30 and Wheel-210
  - Added Miller-Rabin test
  - Added hybrid approach
  - Added hyperbolic method

- **Version 1.0** (2024-12-03)
  - Initial file-based implementations
  - Basic prime operations

---

## License

Open source - feel free to use, modify, and distribute.

---

*For complete usage guide, see [USER_GUIDE.md](../../USER_GUIDE.md)*

*For performance benchmarks, see [COMPARISON.md](../../COMPARISON.md)*

*For method explanations, see [METHODS_GUIDE.md](../../METHODS_GUIDE.md)*
