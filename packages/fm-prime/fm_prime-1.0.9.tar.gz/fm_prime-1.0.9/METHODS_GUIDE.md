# Prime Number Methods: Comprehensive Guide

This guide explains all the prime number detection and generation methods available in this library.

---

## Table of Contents

1. [Overview](#overview)
2. [The 6k±1 Pattern (Wheel-6)](#the-6k1-pattern-wheel-6)
3. [Advanced Wheel Factorization](#advanced-wheel-factorization)
4. [Miller-Rabin Primality Test](#miller-rabin-primality-test)
5. [Sieve of Eratosthenes](#sieve-of-eratosthenes)
6. [Hyperbolic Equation Approach](#hyperbolic-equation-approach)
7. [Combining Methods](#combining-methods)

---

## Overview

All our methods are optimizations based on one fundamental insight:

**Not all numbers need to be tested for primality.**

We can eliminate large classes of numbers that cannot possibly be prime, dramatically reducing the work needed.

### Method Comparison

| Method | Tests | Best For | Complexity |
|--------|-------|----------|------------|
| Naive | 100% | Learning | O(n) |
| **6k±1** | **33%** | **General use** | **O(√n)** |
| Wheel-30 | 27% | Better performance | O(√n / 1.2) |
| Wheel-210 | 23% | Maximum single-run | O(√n / 1.4) |
| Miller-Rabin | Variable | Very large primes | O(k log³ n) |
| Sieve | N/A | All primes up to N | O(n log log n) |
| **Hyperbolic ⭐** | **33%** | **Repeated queries + Caching** | **O(√n)** |

---

## The 6k±1 Pattern (Wheel-6)

### The Foundation

**All primes greater than 3 are of the form 6k±1**

### Why This Works

Every integer can be written as one of: 6k, 6k+1, 6k+2, 6k+3, 6k+4, or 6k+5

Let's analyze each:
- **6k** = 6×k → divisible by 6, not prime
- **6k+1** → could be prime ✓
- **6k+2** = 2(3k+1) → divisible by 2, not prime
- **6k+3** = 3(2k+1) → divisible by 3, not prime
- **6k+4** = 2(3k+2) → divisible by 2, not prime
- **6k+5** = 6k-1 → could be prime ✓

Only **2 out of every 6** positions can be prime (except 2 and 3 themselves).

### Implementation

```python
def is_prime_6k(n):
    """Check if n is prime using 6k±1 pattern"""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check only 6k±1 candidates up to √n
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True
```

```javascript
function isPrime6k(n) {
  if (n <= 3) return n > 1;
  if (n % 2 === 0 || n % 3 === 0) return false;

  // Check only 6k±1 candidates up to √n
  for (let i = 5; i * i <= n; i += 6) {
    if (n % i === 0 || n % (i + 2) === 0) return false;
  }

  return true;
}
```

### Performance

- **Tests**: 33% of numbers (3x faster than naive)
- **Complexity**: O(√n) but with 3x fewer operations
- **Best for**: General-purpose prime checking

---

## Advanced Wheel Factorization

Wheel-6 (6k±1) can be extended to eliminate multiples of more primes.

### Wheel-30

**Eliminates multiples of 2, 3, AND 5**

Only these positions in each group of 30 can be prime:
```
1, 7, 11, 13, 17, 19, 23, 29
```

That's **8 out of 30 = 26.7%** of numbers.

#### Pattern

```
Wheel-30 spokes: [1, 7, 11, 13, 17, 19, 23, 29]
Increments:      [6, 4, 2, 4, 2, 4, 6, 2]
```

Example sequence: 1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, ...

#### Implementation

```python
class Wheel30:
    SPOKES = [1, 7, 11, 13, 17, 19, 23, 29]
    INCREMENTS = [6, 4, 2, 4, 2, 4, 6, 2]

    @classmethod
    def generate_candidates(cls, start, end):
        """Generate prime candidates using Wheel-30"""
        if start <= 2:
            yield 2
        if start <= 3:
            yield 3
        if start <= 5:
            yield 5

        # Find starting position in wheel
        cycle = (start // 30) * 30
        spoke_idx = 0

        for idx, spoke in enumerate(cls.SPOKES):
            candidate = cycle + spoke
            if candidate >= start:
                spoke_idx = idx
                break

        # Generate candidates
        while True:
            candidate = cycle + cls.SPOKES[spoke_idx]
            if candidate > end:
                break
            if candidate >= start:
                yield candidate

            spoke_idx += 1
            if spoke_idx >= len(cls.SPOKES):
                spoke_idx = 0
                cycle += 30
```

### Wheel-210

**Eliminates multiples of 2, 3, 5, AND 7**

Only **48 out of 210 = 22.9%** of numbers need testing.

#### The 48 Spokes

```
[1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
 107, 109, 113, 121, 127, 131, 137, 139, 143, 149,
 151, 157, 163, 167, 169, 173, 179, 181, 187, 191,
 193, 197, 199, 209]
```

#### When to Use

✅ Use Wheel-210 when:
- Generating millions of primes
- Maximum performance is critical
- Memory efficiency matters

⚠️ Consider the tradeoff:
- More complex code (48 spokes vs 2 for Wheel-6)
- Only 31% improvement over Wheel-6
- Diminishing returns

### Comparison

In range [50, 100]:

**Wheel-6 generates**: 53, 55, 59, 61, 65, 67, 71, 73, 77, 79, 83, 85, 89, 91, 95, 97 (16 candidates)

**Wheel-30 generates**: 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 (10 candidates)

**Wheel-210 generates**: 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 (10 candidates)

Wheel-30 and Wheel-210 eliminate: 55, 65, 77, 85, 91, 95 (multiples of 5 or 7)

---

## Miller-Rabin Primality Test

A probabilistic primality test for **very large numbers**.

### How It Works

Based on Fermat's Little Theorem: If p is prime, then for any a: a^(p-1) ≡ 1 (mod p)

Miller-Rabin extends this with additional checks to reduce false positives.

### Algorithm

1. Write n-1 as 2^r × d (where d is odd)
2. Pick random witness a
3. Compute x = a^d mod n
4. Perform r squaring tests
5. If all tests pass, n is probably prime

### Implementation

```python
def miller_rabin(n, k=5):
    """
    Miller-Rabin primality test
    k = number of rounds (higher = more accurate)
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test k random witnesses
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d mod n

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite

    return True  # Probably prime
```

### Accuracy

- k=1: ~75% accuracy
- k=5: >99.9% accuracy
- k=10: >99.9999% accuracy

For most purposes, k=5 is sufficient.

### When to Use

✅ **Use Miller-Rabin for**:
- Numbers > 10^15
- Cryptographic applications
- When deterministic test is too slow

❌ **Don't use for**:
- Small numbers (< 10^9) - trial division is faster
- When 100% certainty is required

---

## Sieve of Eratosthenes

Ancient algorithm for finding **all primes up to N**.

### How It Works

1. Create array of all numbers from 2 to N
2. Starting with 2, mark all multiples as composite
3. Move to next unmarked number, repeat
4. Unmarked numbers are prime

### Optimization with 6k±1

Instead of tracking all numbers, only track 6k±1 candidates:

```python
def sieve_6k_optimized(limit):
    """Sieve tracking only 6k±1 candidates"""
    # Array size is limit/3 instead of limit
    sieve_size = limit // 6 * 2 + 2
    is_composite = [False] * sieve_size

    def index_to_number(i):
        """Convert array index to actual number"""
        return (6 * (i // 2 + 1) - 1) if i % 2 == 0 else (6 * ((i + 1) // 2) + 1)

    def number_to_index(n):
        """Convert number to array index"""
        return (n // 6) * 2 + (0 if n % 6 == 5 else 1)

    # Mark composites
    for i in range(sieve_size):
        if not is_composite[i]:
            num = index_to_number(i)
            if num * num > limit:
                break

            # Mark multiples of num
            multiple = num * num
            while multiple <= limit:
                idx = number_to_index(multiple)
                is_composite[idx] = True
                multiple += num

    # Collect primes
    primes = [2, 3]
    for i in range(sieve_size):
        if not is_composite[i]:
            num = index_to_number(i)
            if num <= limit:
                primes.append(num)

    return primes
```

### Performance

- **Time**: O(n log log n)
- **Space**: O(n/3) with 6k±1 optimization
- **Best for**: Finding all primes up to N where N > 10,000

### Comparison

Finding all primes up to 100,000:
- Trial division: ~250ms
- Sieve (traditional): ~80ms
- **Sieve (6k±1)**: ~50ms
- **Sieve (Wheel-210)**: ~40ms

**5-10x faster** than trial division for bulk generation.

---

## Hyperbolic Equation Approach ⭐

An advanced mathematical approach using hyperbolic equations with intelligent optimizations.

### The Mathematics

For numbers of form 6n+1, if composite, factors as (6k+1)(6kk+1).

This can be transformed into a hyperbolic equation:
```
m² - 9r² = 6n+1
```

Solving for m:
```
m = √(9r² + 6n + 1)
```

**Key insight**: If this square root is an integer satisfying certain constraints, we've found a divisor.

### Optimizations (New!)

The production version includes major improvements:

1. **Two-way search**:
   - Bottom-up: Checks r values (finds factors near √N)
   - Top-down: Checks small factors k = 6i±1 (finds small factors quickly)

2. **Modular filters** (eliminates ~94% of non-squares):
   - Quadratic residue checks modulo 64, 63, and 65
   - Avoids expensive square root calculations

3. **Intelligent file caching**:
   - Saves results to `output-big` folder
   - Reuses previously computed primes
   - Extends from existing cache when possible

### Algorithm

```python
def find_divisor_hyperbolic(num):
    """Find smallest divisor using hyperbolic equations"""
    if num % 2 == 0:
        return 2
    if num % 3 == 0:
        return 3

    n = (num - 1) // 6
    r = 0

    while 7*r <= n - 8:
        # Check if m = √(9r² + 6n + 1) is an integer
        discriminant = 9*r*r + 6*n + 1
        m = isqrt(discriminant)  # Integer square root

        if m*m == discriminant:  # Perfect square?
            check = m - 3*r - 1
            if check % 6 == 0 and check >= 6:
                return check + 1  # Found divisor!
        r += 1

    return num  # Prime
```

### Characteristics

- **Complexity**: O(√n) with two-way search guarantee
- **Operations**: Modular arithmetic + selective square roots
- **Caching**: File-based caching for repeated queries
- **Accuracy**: 100% verified (664,579 primes under 10M)
- **Status**: Production-ready

### When to Use

✓ **Repeated queries** - Extremely fast with caching
✓ **Bulk generation** - Competitive with Wheel-210
✓ **Long-running applications** - Benefits from accumulated cache
✓ **Educational purposes** - Shows connection between algebra and number theory
✓ **Mathematical research** - Novel hyperbolic formulation

### Performance

- **First run**: Similar to other O(√N) methods
- **Cached reads**: < 1 second for 664K primes
- **Cache extension**: Only computes new primes beyond cached limit

---

## Combining Methods

The most powerful approach is combining multiple methods.

### Hybrid Prime Checker

```python
class HybridPrimeFinder:
    def __init__(self):
        # Pre-generate small primes for quick lookup
        self.small_primes = set(sieve_6k_optimized(10000))

    def is_prime(self, n):
        """Intelligently choose best method"""
        # Quick checks
        if n < 2:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False

        # Lookup for small primes
        if n < 10000:
            return n in self.small_primes

        # Trial division for medium primes
        if n < 1000000:
            return is_prime_6k(n)

        # Miller-Rabin for large primes
        return miller_rabin(n, 5)
```

### Best Practices

**For single prime checks:**
```
n < 10⁶:        Use 6k±1 trial division
n > 10⁶:        Use Miller-Rabin
```

**For bulk generation:**
```
n < 10,000:     Use 6k±1 sieve
n < 1,000,000:  Use Wheel-30 sieve
n > 1,000,000:  Use Wheel-210 sieve
```

**For prime ranges [a, b]:**
```
Small range:    6k±1 with trial division
Large range:    Wheel-30 + Miller-Rabin
```

### Example: Finding Primes in Range

```python
def primes_in_range(start, end):
    """Find all primes in [start, end] using hybrid approach"""
    # Use appropriate wheel based on range size
    range_size = end - start

    if range_size < 10000:
        # Use 6k±1 pattern
        candidates = generate_6k_candidates(start, end)
    elif range_size < 1000000:
        # Use Wheel-30
        candidates = Wheel30.generate_candidates(start, end)
    else:
        # Use Wheel-210
        candidates = Wheel210.generate_candidates(start, end)

    # Test each candidate
    primes = []
    for candidate in candidates:
        if candidate < 1000000:
            # Trial division for smaller
            if is_prime_6k(candidate):
                primes.append(candidate)
        else:
            # Miller-Rabin for larger
            if miller_rabin(candidate, 5):
                primes.append(candidate)

    return primes
```

---

## Summary

### Quick Reference

| Task | Best Method |
|------|-------------|
| Check if single number is prime | 6k±1 (small), Miller-Rabin (large) |
| Find all primes up to N (first time) | Wheel-210 or Hyperbolic |
| Find all primes up to N (repeated) | Hyperbolic with Caching ⭐ |
| Find primes in range [a, b] | Hybrid approach |
| Maximum single-run performance | Wheel-210 |
| Long-running applications | Hyperbolic with Caching ⭐ |
| Educational purposes | 6k±1 or Hyperbolic |
| Very large numbers (>10^15) | Miller-Rabin |

### Performance Hierarchy

```
Fastest → Slowest (for bulk generation):
Wheel-210 Sieve > Wheel-30 Sieve > 6k±1 Sieve > Trial Division > Naive

Fastest → Slowest (for single checks):
Miller-Rabin (large) > 6k±1 (small) > Naive
```

### Memory Hierarchy

```
Most efficient → Least efficient:
Wheel-210 (23%) > Wheel-30 (27%) > 6k±1 (33%) > Traditional (100%)
```

---

## Further Reading

For implementation details, see:
- `USER_GUIDE.md` - How to use these methods
- `COMPARISON.md` - Detailed performance benchmarks
- Source code in `src/services/` (JavaScript) and `src/services-py/` (Python)

For testing:
- Run `node test-all-methods.mjs` (JavaScript)
- Run `python test-all-methods.py` (Python)
