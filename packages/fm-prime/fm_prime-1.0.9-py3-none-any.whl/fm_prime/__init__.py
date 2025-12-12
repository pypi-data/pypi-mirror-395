"""
fm-prime: Comprehensive Prime Number Utilities
================================================

A powerful collection of prime number algorithms including:
- 6k±1 Pattern (Wheel-6)
- Wheel-30 and Wheel-210 factorization
- Miller-Rabin probabilistic test
- Hyperbolic Equation Method with intelligent caching

Basic Usage:
-----------
    from fm_prime import is_prime_optimized, sieve_wheel210, sieve_hyperbolic_optimized

    # Check if a number is prime
    print(is_prime_optimized(999983))  # True

    # Find all primes up to 100,000
    primes = sieve_wheel210(100000)
    print(f"Found {len(primes)} primes")

    # Use caching for repeated queries
    cached_primes = sieve_hyperbolic_optimized(100000)

For more information, see: https://github.com/faridmasjedi/fm-prime
"""

__version__ = "1.0.9"
__author__ = "Farid Masjedi <farid.masjedi1985@gmail.com>"
__license__ = "MIT"

# Import main functions for easy access
from .prime_optimized import (
    is_prime_optimized,
    miller_rabin,
    sieve_of_eratosthenes,
    Wheel30
)

from .wheel210 import (
    Wheel210,
    sieve_wheel210,
    is_prime_wheel210
)

from .prime_hyperbolic_optimized import (
    sieve_hyperbolic_optimized,
    sieve_hyperbolic_parallel,
    is_prime_hyperbolic_optimized,
    division_hyperbolic,
    get_hyperbolic_cache_stats,
    get_cache_size_mb,
    manage_cache_size,
    compress_cache_files,
    clear_all_cache
)

from .primeUtils_optimized import (
    find_next_candidate
)

__all__ = [
    # Basic prime checking
    'is_prime_optimized',
    'miller_rabin',

    # Sieve methods
    'sieve_of_eratosthenes',
    'sieve_wheel210',
    'sieve_hyperbolic_optimized',

    # Wheel classes
    'Wheel30',
    'Wheel210',

    # Hyperbolic methods
    'is_prime_hyperbolic_optimized',
    'sieve_hyperbolic_parallel',
    'division_hyperbolic',
    'get_hyperbolic_cache_stats',
    'get_cache_size_mb',
    'manage_cache_size',
    'compress_cache_files',
    'clear_all_cache',

    # Individual prime checking
    'is_prime_wheel210',

    # Utilities
    'find_next_candidate',
]
