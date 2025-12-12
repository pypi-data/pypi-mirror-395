# Examples

This directory contains example scripts demonstrating how to use the fm-prime library in both Python and JavaScript.

## Available Examples

### Python Examples

#### example_hyperbolic_optimized.py

Comprehensive demonstration of the optimized hyperbolic prime detection method with file-level granular caching.

**Features demonstrated:**
- Generating primes with caching
- Checking individual numbers for primality
- Finding all divisors of a number
- Checking cache status
- Performance benchmarking

**Run:**
```bash
python examples/example_hyperbolic_optimized.py
```

### JavaScript Examples

#### example_hyperbolic_optimized.mjs

JavaScript equivalent of the Python demonstration, showing the same features using the JavaScript implementation.

**Features demonstrated:**
- Generating primes with caching
- Checking individual numbers for primality
- Checking cache status
- Performance benchmarking

**Run:**
```bash
node examples/example_hyperbolic_optimized.mjs
```

**Expected output:**
```
======================================================================
OPTIMIZED HYPERBOLIC PRIME DETECTION WITH CACHING
======================================================================

📊 Cache Status:
   Cached folders: 5
   Largest limit: 30,300,000

TEST 1: Generate primes up to 100,000
----------------------------------------------------------------------
Found 9,592 primes in 24.35ms
First 10: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
Last 10: [99877, 99881, 99901, 99907, 99923, 99929, 99961, 99971, 99989, 99991]
Verification: True (expected 9,592)

TEST 2: Check individual numbers
----------------------------------------------------------------------
✓  15,485,863 (1 millionth prime)
  Result: PRIME, Time: 0.123ms
✓     999,983 (largest prime < 1M)
  Result: PRIME, Time: 0.089ms
...
```

## Basic Usage Patterns

### Python

#### Check if a number is prime

```python
from fm_prime import is_prime_hyperbolic_optimized

# Check single number
print(is_prime_hyperbolic_optimized(999983))  # True
print(is_prime_hyperbolic_optimized(1000000))  # False
```

### JavaScript

#### Check if a number is prime

```javascript
import { isPrimeHyperbolicOptimized } from './src/services/primeHyperbolic.optimized.mjs';

// Check single number
console.log(isPrimeHyperbolicOptimized('999983'));   // true
console.log(isPrimeHyperbolicOptimized('1000000'));  // false
```

#### Generate all primes up to N

**Python:**
```python
from fm_prime import sieve_hyperbolic_optimized

# Generate primes up to 100,000
primes = sieve_hyperbolic_optimized(100000)
print(f"Found {len(primes)} primes")
print(f"First 10: {primes[:10]}")
print(f"Last 10: {primes[-10:]}")
```

**JavaScript:**
```javascript
import { sieveHyperbolicOptimized } from './src/services/primeHyperbolic.optimized.mjs';

// Generate primes up to 100,000
const primes = sieveHyperbolicOptimized('100000');
console.log(`Found ${primes.length} primes`);
console.log(`First 10: [${primes.slice(0, 10)}]`);
console.log(`Last 10: [${primes.slice(-10)}]`);
```

#### Check cache status

**Python:**
```python
from fm_prime import get_hyperbolic_cache_stats

# Get cache information
stats = get_hyperbolic_cache_stats()
print(f"Cached folders: {stats['folders']}")
print(f"Largest cached limit: {stats['largest_limit']:,}")
print(f"Total cache size: {stats['size_mb']:.2f} MB")
```

**JavaScript:**
```javascript
import { getHyperbolicCacheStats } from './src/services/primeHyperbolic.optimized.mjs';

// Get cache information
const stats = getHyperbolicCacheStats();
console.log(`Cached folders: ${stats.folders}`);
console.log(`Largest cached limit: ${stats.largestLimit.toLocaleString()}`);
console.log(`Total cache size: ${stats.sizeMb.toFixed(2)} MB`);
```

#### Find all divisors of a number

**Python:**
```python
from fm_prime import get_all_divisions_hyperbolic

# Find prime factors
factors = get_all_divisions_hyperbolic(12345)
print(f"Prime factors of 12345: {factors}")  # [3, 5, 823]
```

**JavaScript:**
```javascript
// Note: This function is available in Python only
// For JavaScript, use the division_hyperbolic function iteratively
```

### Manage cache

```python
from fm_prime import (
    get_cache_size_mb,
    manage_cache_size,
    compress_cache_files,
    clear_all_cache
)

# Check cache size
size = get_cache_size_mb()
print(f"Cache size: {size:.2f} MB")

# Manage cache (keep only 500MB)
result = manage_cache_size(max_size_mb=500)
print(f"Removed {result['folders_removed']} folders")

# Compress cache files
result = compress_cache_files()
print(f"Compressed {result['files_compressed']} files")
print(f"Saved {result['space_saved_mb']:.2f} MB")

# Clear all cache
result = clear_all_cache()
print(f"Cleared {result['folders_removed']} folders")
```

## Performance Tips

1. **First run**: When generating primes for the first time, it will compute and cache them
2. **Subsequent runs**: Cached primes load instantly (typically < 1 second for millions of primes)
3. **File-level granular caching**: Only reads/processes necessary files (2.5x faster on average)
4. **Cache extends automatically**: If you request a number beyond cached range, it extends from existing cache
5. **Missing folders**: Algorithm intelligently uses the next best available cache folder

## More Examples

For more usage examples, see:
- [USER_GUIDE.md](../USER_GUIDE.md) - Complete API reference
- [METHODS_GUIDE.md](../METHODS_GUIDE.md) - Algorithm explanations
- [README.md](../README.md) - Quick start guide
