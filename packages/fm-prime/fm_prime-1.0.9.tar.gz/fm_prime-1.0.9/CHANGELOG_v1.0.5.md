# Changelog

## [1.0.5] - 2025-11-28

### Bug Fixes - Python Package

#### Fixed: calculate_primes_text returning None
- **File**: `fm_prime/primeIndex.py`
- **Issue**: Function returned `None` when cached folder existed
- **Fix**: Now returns prime count by reading from OutputPrimes-{count}.txt filename
- **Impact**: Utility method now properly returns count for cached results

#### Fixed: services-py sieve case sensitivity issue  
- **File**: `src/services-py/prime_hyperbolic_optimized.py`
- **Issue**: read_primes_from_folder only looked for "Output*.txt" (uppercase), missing "output*.txt" (lowercase) files
- **Fix**: Updated file filter to check both cases: `f.startswith('Output') or f.startswith('output')`
- **Impact**: sieve_hyperbolic_optimized now correctly reads from all cached output files

### Testing
- All 10/10 comprehensive Python tests now pass ✅
- fm_prime (recommended) package: 4/4 tests ✓
- services-py legacy methods: 2/2 tests ✓  
- Legacy compatibility methods: 2/2 tests ✓
- Utility methods: 2/2 tests ✓

---

## [1.0.1] - 2025-11-28 (npm package: primefm)

### Bug Fixes - JavaScript/Node.js Package

#### Fixed: isPrimeFromTextFilesRecursiveUpdated type coercion
- **File**: `src/services/primeChecker.mjs`
- **Issue**: Function received numeric input but called string-expecting functions, causing incorrect results
- **Fix**: Added type conversion at function entry: `const numStr = typeof num === 'string' ? num : num.toString()`
- **Impact**: Prime checking now works correctly with both string and numeric inputs

#### Fixed: generatePrimesUpTo returning undefined
- **File**: `src/services/primeGenerator.mjs`
- **Issue**: Early return when cached folder exists without returning the primes array
- **Fix**: Added logic to read, parse, and return primes from cached folder
- **Impact**: Function now returns prime array instead of undefined when cache exists

#### Fixed: generatePrimesRecursiveUpdated memory leak
- **File**: `src/services/primeGenerator.mjs`  
- **Issue**: Recursive implementation caused stack overflow and memory exhaustion
- **Fix**: Complete rewrite using iterative approach with for-loop
- **Impact**: Eliminates memory leaks, supports larger ranges without crashes

### Testing
- All 31/31 comprehensive JavaScript tests now pass ✅
- Hyperbolic methods (production): 18/18 tests ✓
- Legacy compatibility methods: 13/13 tests ✓

### Notes
All fixes maintain backward compatibility and follow existing code patterns. No breaking changes.
