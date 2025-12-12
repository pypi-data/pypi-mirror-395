# User Guide: How to Use Prime Number Methods

This guide shows you how to use all the prime number methods in this library.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [JavaScript API](#javascript-api)
3. [Python API](#python-api)
4. [Common Tasks](#common-tasks)
5. [Examples](#examples)

---

## Quick Start

### Installation

**JavaScript** (if published to NPM):
```bash
npm install fm-prime
```

**Or use directly** from the repository:
```bash
git clone https://github.com/yourusername/fm-prime.git
cd fm-prime
```

**Python**:
```bash
# Add to your Python path
import sys
sys.path.insert(0, 'src/services-py')
```

### Interactive Prime Finder (Easiest Way!)

The quickest way to start finding primes is using the interactive menu:

**JavaScript:**
```bash
node findPrimes.mjs
```

**Python:**
```bash
python3 findPrimes.py
```

Both provide an interactive menu where you can:
1. Choose from 6 different prime-finding methods
2. Enter any limit (e.g., 10,000,000)
3. See timing and verification results
4. View all primes or just the count

### Your First Prime Check (Programmatic)

**JavaScript:**
```javascript
import { isPrimeOptimized } from './src/services/primeChecker.optimized.mjs';

console.log(isPrimeOptimized('17'));  // true
console.log(isPrimeOptimized('18'));  // false
```

**Python:**
```python
from prime_optimized import is_prime_optimized

print(is_prime_optimized(17))  # True
print(is_prime_optimized(18))  # False
```

---

## JavaScript API

### 1. Basic Prime Checking

#### Check if a number is prime (6k±1 method)

```javascript
import { isPrimeOptimized } from './src/services/primeChecker.optimized.mjs';

// Works with strings for big numbers
console.log(isPrimeOptimized('999983'));  // true
console.log(isPrimeOptimized('1000000')); // false

// Also works with numbers
console.log(isPrimeOptimized(17));  // true
```

#### Miller-Rabin (for very large numbers)

```javascript
import { millerRabinTest } from './src/services/primeChecker.optimized.mjs';

// k = number of rounds (default 5)
// Higher k = more accurate but slower
console.log(millerRabinTest('1000000007', 5));  // true
console.log(millerRabinTest('1000000007', 10)); // true (more certain)
```

### 2. Generate Prime Candidates

#### Generate 6k±1 candidates

```javascript
import { findNextCandidate } from './src/services/helper.optimized.mjs';

let current = '5';
for (let i = 0; i < 10; i++) {
  console.log(current);  // 5, 7, 11, 13, 17, 19, 23, 25, 29, 31
  current = findNextCandidate(current);
}
```

#### Generate Wheel-30 candidates

```javascript
import { Wheel30 } from './src/services/primeHybrid.optimized.mjs';

// Generate candidates in range
for (const candidate of Wheel30.generateCandidates('100', '200')) {
  console.log(candidate);
}

// Get next candidate
let current = '100';
current = Wheel30.nextCandidate(current);
console.log(current);  // 101
```

#### Generate Wheel-210 candidates

```javascript
import { Wheel210 } from './src/services/wheel210.optimized.mjs';

// Generate candidates in range
for (const candidate of Wheel210.generateCandidates('100', '200')) {
  console.log(candidate);
}
```

### 3. Find All Primes (Sieve Methods)

#### 6k±1 optimized sieve

```javascript
import { sieve6kOptimized } from './src/services/primeHybrid.optimized.mjs';

// Find all primes up to 10,000
const primes = sieve6kOptimized('10000');
console.log(`Found ${primes.length} primes`);
console.log(`First 10:`, primes.slice(0, 10));
```

#### Wheel-210 sieve (fastest single-run)

```javascript
import { sieveWheel210 } from './src/services/wheel210.optimized.mjs';

// Find all primes up to 100,000
const primes = sieveWheel210('100000');
console.log(`Found ${primes.length} primes`);
```

#### Hyperbolic sieve with caching ⭐ (best for repeated use)

```javascript
import { sieveHyperbolicOptimized } from './src/services/primeHyperbolic.optimized.mjs';

// Find all primes up to 100,000 (uses file caching)
const primes = sieveHyperbolicOptimized('100000');
console.log(`Found ${primes.length} primes`);

// Second call is VERY fast (loads from cache)
const primes2 = sieveHyperbolicOptimized('50000');  // Instant!
console.log(`Found ${primes2.length} primes`);
```

### 4. Hybrid Approach

```javascript
import { HybridPrimeFinder } from './src/services/primeHybrid.optimized.mjs';

const finder = new HybridPrimeFinder();

// Automatically chooses best method
console.log(finder.isPrime('17'));          // Uses 6k±1
console.log(finder.isPrime('1000000007'));  // Uses Miller-Rabin

// Find primes in range
const primes = finder.findPrimesInRange('100', '200');
console.log(primes);
```

---

## Python API

### 1. Basic Prime Checking

#### Check if a number is prime (6k±1 method)

```python
from prime_optimized import is_prime_optimized

print(is_prime_optimized(999983))   # True
print(is_prime_optimized(1000000))  # False
```

#### Miller-Rabin (for very large numbers)

```python
from prime_optimized import miller_rabin_test

# k = number of rounds (default 5)
print(miller_rabin_test(1000000007, k=5))   # True
print(miller_rabin_test(1000000007, k=10))  # True (more certain)
```

### 2. Generate Prime Candidates

#### Generate 6k±1 candidates

```python
from primeUtils_optimized import find_next_candidate

current = 5
for i in range(10):
    print(current)  # 5, 7, 11, 13, 17, 19, 23, 25, 29, 31
    current = find_next_candidate(current)
```

#### Generate Wheel-30 candidates

```python
from prime_optimized import Wheel30

# Generate candidates in range
for candidate in Wheel30.generate_candidates(100, 200):
    print(candidate)

# Get next candidate
current = 100
current = Wheel30.next_candidate(current)
print(current)  # 101
```

#### Generate Wheel-210 candidates

```python
from wheel210 import Wheel210

# Generate candidates in range
for candidate in Wheel210.generate_candidates(100, 200):
    print(candidate)
```

### 3. Find All Primes (Sieve Methods)

#### Traditional sieve

```python
from prime_optimized import sieve_of_eratosthenes

# Find all primes up to 10,000
primes = sieve_of_eratosthenes(10000)
print(f"Found {len(primes)} primes")
print(f"First 10: {primes[:10]}")
```

#### Wheel-210 sieve (fastest single-run)

```python
from wheel210 import sieve_wheel210

# Find all primes up to 100,000
primes = sieve_wheel210(100000)
print(f"Found {len(primes)} primes")
```

#### Hyperbolic sieve with caching ⭐ (best for repeated use)

```python
from prime_hyperbolic_optimized import sieve_hyperbolic_optimized

# Find all primes up to 100,000 (uses file caching)
primes = sieve_hyperbolic_optimized(100000)
print(f"Found {len(primes)} primes")

# Second call is VERY fast (loads from cache)
primes2 = sieve_hyperbolic_optimized(50000)  # Instant!
print(f"Found {len(primes2)} primes")
```

### 4. Hybrid Approach

```python
from prime_optimized import Wheel30
from prime_optimized import is_prime_optimized, miller_rabin_test

def smart_is_prime(n):
    """Choose best method based on size"""
    if n < 1000000:
        return is_prime_optimized(n)
    else:
        return miller_rabin_test(n, k=5)

# Use it
print(smart_is_prime(17))          # Uses 6k±1
print(smart_is_prime(1000000007))  # Uses Miller-Rabin
```

---

## Common Tasks

### Task 1: Check if a single number is prime

**Small number (< 1 million):**
```javascript
// JavaScript
import { isPrimeOptimized } from './src/services/primeChecker.optimized.mjs';
console.log(isPrimeOptimized('999983'));
```

```python
# Python
from prime_optimized import is_prime_optimized
print(is_prime_optimized(999983))
```

**Large number (> 1 million):**
```javascript
// JavaScript
import { millerRabinTest } from './src/services/primeChecker.optimized.mjs';
console.log(millerRabinTest('1000000007', 5));
```

```python
# Python
from prime_optimized import miller_rabin_test
print(miller_rabin_test(1000000007, k=5))
```

### Task 2: Find all primes up to N

**JavaScript:**
```javascript
import { sieveWheel210 } from './src/services/wheel210.optimized.mjs';

const N = '100000';
const primes = sieveWheel210(N);

console.log(`Found ${primes.length} primes up to ${N}`);
console.log(`Largest prime: ${primes[primes.length - 1]}`);
```

**Python:**
```python
from wheel210 import sieve_wheel210

N = 100000
primes = sieve_wheel210(N)

print(f"Found {len(primes)} primes up to {N}")
print(f"Largest prime: {primes[-1]}")
```

### Task 3: Find primes in a range

**JavaScript:**
```javascript
import { Wheel30 } from './src/services/primeHybrid.optimized.mjs';
import { isPrimeOptimized } from './src/services/primeChecker.optimized.mjs';

function primesInRange(start, end) {
  const primes = [];
  for (const candidate of Wheel30.generateCandidates(start, end)) {
    if (isPrimeOptimized(candidate)) {
      primes.push(candidate);
    }
  }
  return primes;
}

const primes = primesInRange('100', '200');
console.log(primes);  // [101, 103, 107, 109, ...]
```

**Python:**
```python
from prime_optimized import Wheel30, is_prime_optimized

def primes_in_range(start, end):
    primes = []
    for candidate in Wheel30.generate_candidates(start, end):
        if is_prime_optimized(candidate):
            primes.append(candidate)
    return primes

primes = primes_in_range(100, 200)
print(primes)  # [101, 103, 107, 109, ...]
```

---

## Testing

Run comprehensive tests to verify all methods:

**JavaScript:**
```bash
node test-all-methods.mjs
```

**Python:**
```bash
python test-all-methods.py
```

Both scripts will:
1. Verify correctness of all methods
2. Compare performance
3. Show memory efficiency
4. Provide recommendations

---

## Further Reading

- **Methods Guide**: See `METHODS_GUIDE.md` for algorithm details
- **Comparison**: See `COMPARISON.md` for performance benchmarks
- **Source Code**: Explore `src/services/` (JavaScript) and `src/services-py/` (Python)

---

## Quick Reference

### JavaScript Imports

```javascript
// Basic
import { isPrimeOptimized, millerRabinTest } from './src/services/primeChecker.optimized.mjs';
import { findNextCandidate } from './src/services/helper.optimized.mjs';

// Advanced
import { Wheel30, sieve6kOptimized, HybridPrimeFinder } from './src/services/primeHybrid.optimized.mjs';
import { Wheel210, sieveWheel210 } from './src/services/wheel210.optimized.mjs';
```

### Python Imports

```python
# Basic
from prime_optimized import is_prime_optimized, miller_rabin_test
from primeUtils_optimized import find_next_candidate

# Advanced
from prime_optimized import Wheel30, sieve_of_eratosthenes
from wheel210 import Wheel210, sieve_wheel210
```

### Method Selection

```
Single check (< 10⁶):        isPrimeOptimized / is_prime_optimized
Single check (> 10⁶):        millerRabinTest / miller_rabin_test
All primes up to N:          sieveWheel210 / sieve_wheel210
Primes in range [a, b]:      Wheel30 + isPrime
```
