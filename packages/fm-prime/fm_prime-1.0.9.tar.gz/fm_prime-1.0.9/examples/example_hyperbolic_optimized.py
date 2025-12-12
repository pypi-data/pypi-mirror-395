"""
Example: Using the Optimized Hyperbolic Prime Method with Caching

This example demonstrates how to use the production-ready hyperbolic prime
detection method with file-level granular caching.

Run this file directly:
    python examples/example_hyperbolic_optimized.py
"""

import sys
import os

# Add parent directory to path to import fm_prime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fm_prime import (
    sieve_hyperbolic_optimized,
    is_prime_hyperbolic_optimized,
    get_hyperbolic_cache_stats,
    get_all_divisions_hyperbolic
)


def demonstrate():
    """Demonstration of optimized hyperbolic approach with caching"""
    print('=' * 70)
    print('OPTIMIZED HYPERBOLIC PRIME DETECTION WITH CACHING')
    print('=' * 70)
    print()

    # Show cache status
    stats = get_hyperbolic_cache_stats()
    print('📊 Cache Status:')
    print(f'   Cached folders: {stats["folders"]}')
    print(f'   Largest limit: {stats["largest_limit"]:,}' if stats["largest_limit"] else '   No cache available')
    print()

    # Test 1: Generate primes with caching
    print('TEST 1: Generate primes up to 100,000')
    print('-' * 70)

    import time
    start = time.time()
    primes = sieve_hyperbolic_optimized(100000)
    elapsed = (time.time() - start) * 1000

    print(f'Found {len(primes):,} primes in {elapsed:.2f}ms')
    print(f'First 10: {primes[:10]}')
    print(f'Last 10: {primes[-10:]}')
    print(f'Verification: {len(primes) == 9592} (expected 9,592)')
    print()

    # Test 2: Check individual primes
    print('TEST 2: Check individual numbers')
    print('-' * 70)

    test_numbers = [
        (15485863, True, '1 millionth prime'),
        (999983, True, 'largest prime < 1M'),
        (15485864, False, 'composite number'),
        (1000000, False, 'composite number'),
    ]

    for num, expected, desc in test_numbers:
        start = time.time()
        result = is_prime_hyperbolic_optimized(num)
        elapsed = (time.time() - start) * 1000

        status = '✓' if result == expected else '✗'
        result_str = 'PRIME' if result else 'COMPOSITE'
        print(f'{status} {num:>10,} ({desc})')
        print(f'  Result: {result_str}, Time: {elapsed:.3f}ms')

    print()

    # Test 3: Find all divisions of a number
    print('TEST 3: Find all divisions of a number')
    print('-' * 70)

    num_to_factor = 12345
    expected_factors = [3, 5, 823]

    start = time.time()
    factors = get_all_divisions_hyperbolic(num_to_factor)
    elapsed = (time.time() - start) * 1000

    status = '✓' if factors == expected_factors else '✗'
    print(f'{status} Factorization of {num_to_factor}:')
    print(f'  Result: {factors}, Time: {elapsed:.3f}ms')
    print()

    # Final cache stats
    final_stats = get_hyperbolic_cache_stats()
    print('📊 Final Cache Status:')
    print(f'   Cached folders: {final_stats["folders"]}')
    print(f'   Largest limit: {final_stats["largest_limit"]:,}' if final_stats["largest_limit"] else '   No cache available')
    print()

    # Verification table
    print('Known Prime Counts for Verification:')
    print('─' * 70)
    print('Limit          | Expected Count | Status')
    print('─' * 70)

    known_counts = [
        (100, 25),
        (1000, 168),
        (10000, 1229),
        (100000, 9592),
    ]

    for limit_val, expected_count in known_counts:
        actual_primes = [p for p in primes if p <= limit_val]
        actual_count = len(actual_primes)
        status = '✓ PASS' if actual_count == expected_count else '✗ FAIL'
        print(f'{limit_val:>14,} | {expected_count:>14,} | {status} (actual: {actual_count:,})')

    print('─' * 70)


def basic_usage_examples():
    """Show basic usage patterns"""
    print('\n' + '=' * 70)
    print('BASIC USAGE EXAMPLES')
    print('=' * 70)
    print()

    print('Example 1: Check if a number is prime')
    print('-' * 70)
    print('from fm_prime import is_prime_hyperbolic_optimized')
    print()
    print('result = is_prime_hyperbolic_optimized(999983)')
    print(f'>>> {is_prime_hyperbolic_optimized(999983)}  # True')
    print()

    print('Example 2: Generate all primes up to N')
    print('-' * 70)
    print('from fm_prime import sieve_hyperbolic_optimized')
    print()
    print('primes = sieve_hyperbolic_optimized(1000)')
    primes_1000 = sieve_hyperbolic_optimized(1000)
    print(f'>>> Found {len(primes_1000)} primes')
    print(f'>>> {primes_1000[:10]} ...')
    print()

    print('Example 3: Check cache status')
    print('-' * 70)
    print('from fm_prime import get_hyperbolic_cache_stats')
    print()
    print('stats = get_hyperbolic_cache_stats()')
    stats = get_hyperbolic_cache_stats()
    print(f'>>> Cached folders: {stats["folders"]}')
    print(f'>>> Largest cached: {stats["largest_limit"]:,}' if stats["largest_limit"] else '>>> No cache')
    print()


if __name__ == '__main__':
    # Run demonstrations
    demonstrate()
    basic_usage_examples()
