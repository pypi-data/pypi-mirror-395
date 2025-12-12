#!/usr/bin/env python3
"""
Prime Number Finder - Interactive Menu System
Python equivalent of findPrimes.mjs
"""

import sys
import os
import time

# Add src/services-py to path
sys.path.insert(0, 'src/services-py')

from wheel210 import sieve_wheel210
from prime_optimized import is_prime_optimized, sieve_of_eratosthenes, Wheel30
from prime_hyperbolic_optimized import sieve_hyperbolic_optimized


def sieve_wheel30(limit):
    """
    Wheel-30 Sieve (eliminates multiples of 2, 3, 5)
    Tests only 27% of candidates
    """
    n = int(limit)
    if n < 2:
        return []

    primes = []
    if n >= 2:
        primes.append(2)
    if n >= 3:
        primes.append(3)
    if n >= 5:
        primes.append(5)

    # Wheel-30 pattern: numbers coprime to 30
    wheel30_pattern = [1, 7, 11, 13, 17, 19, 23, 29]
    sqrt_n = int(n ** 0.5)

    base = 0
    while base * 30 <= n:
        for offset in wheel30_pattern:
            candidate = base * 30 + offset
            if candidate <= 5:
                continue
            if candidate > n:
                break

            is_prime = True
            for p in primes:
                if p > sqrt_n:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break

            if is_prime:
                primes.append(candidate)

        base += 1

    return primes


def sieve_6k_optimized(limit):
    """
    6k±1 Pattern Sieve
    Tests only 33% of candidates
    """
    n = int(limit)
    if n < 2:
        return []

    primes = []
    if n >= 2:
        primes.append(2)
    if n >= 3:
        primes.append(3)

    # Check 6k±1 candidates
    for candidate in range(5, n + 1, 2):
        if is_prime_optimized(candidate):
            primes.append(candidate)

    return primes


def sieve_trial_division(limit):
    """
    Trial division with 6k±1 pattern
    Tests each candidate individually
    """
    n = int(limit)
    if n < 2:
        return []

    primes = []
    if n >= 2:
        primes.append(2)
    if n >= 3:
        primes.append(3)

    for candidate in range(5, n + 1, 2):
        if is_prime_optimized(candidate):
            primes.append(candidate)

    return primes


def sieve_hybrid(limit):
    """
    Hybrid approach using Wheel30
    Combines precomputed primes with wheel pattern
    """
    wheel = Wheel30()
    return wheel.find_primes_up_to(int(limit))


# Method implementations
methods = {
    '1': {
        'name': '6k±1 Pattern Sieve',
        'description': 'Tests only 33% of candidates - Good balance',
        'category': 'Optimized Sieves',
        'run': lambda limit: sieve_6k_optimized(limit)
    },
    '2': {
        'name': 'Wheel-30 Sieve',
        'description': 'Tests only 27% of candidates (eliminates 2, 3, 5)',
        'category': 'Optimized Sieves',
        'run': lambda limit: sieve_wheel30(limit)
    },
    '3': {
        'name': 'Wheel-210 Sieve ⭐',
        'description': 'Tests only 23% of candidates (eliminates 2, 3, 5, 7) - FASTEST',
        'category': 'Optimized Sieves',
        'run': lambda limit: sieve_wheel210(limit)
    },
    '4': {
        'name': 'Hybrid Sieve',
        'description': 'Combines precomputed primes with wheel pattern',
        'category': 'Optimized Sieves',
        'run': lambda limit: sieve_hybrid(limit)
    },
    '5': {
        'name': 'Trial Division (6k±1) - Check each number',
        'description': 'Tests each candidate individually - Slower but simple',
        'category': 'Trial Division Methods',
        'run': lambda limit: sieve_trial_division(limit)
    },
    '6': {
        'name': 'Hyperbolic Sieve with Caching ⭐',
        'description': 'O(√N) two-way search + file caching - VERY FAST for repeated use',
        'category': 'Optimized Sieves',
        'run': lambda limit: sieve_hyperbolic_optimized(limit)
    }
}


def display_menu():
    """Display the interactive menu"""
    print('\n' + '=' * 70)
    print('PRIME NUMBER FINDER - Choose Your Method')
    print('=' * 70)

    # Group methods by category
    categories = {}
    for key, method in methods.items():
        cat = method.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({'key': key, 'method': method})

    # Display by category
    for category, items in categories.items():
        print(f'\n{category}:')
        for item in items:
            key = item['key']
            method = item['method']
            print(f'  [{key}] {method["name"]}')
            print(f'      {method["description"]}')

    print('\n' + '=' * 70)


def main():
    """Main interactive loop"""
    try:
        display_menu()

        method_choice = input('\nEnter method number (1-6): ').strip()

        if method_choice not in methods:
            print('Invalid method choice!')
            return

        limit_input = input('Enter the upper limit (e.g., 10000000): ').strip()
        try:
            limit = int(limit_input)
        except ValueError:
            print('Invalid limit! Must be a number.')
            return

        if limit < 2:
            print('Limit must be at least 2')
            return

        selected_method = methods[method_choice]
        print(f'\n{"=" * 70}')
        print(f'Using: {selected_method["name"]}')
        print(f'Finding all primes less than: {limit:,}')
        print(f'{"=" * 70}\n')

        start_time = time.perf_counter()
        primes = selected_method['run'](limit)
        end_time = time.perf_counter()

        time_elapsed = end_time - start_time

        print(f'\n{"=" * 70}')
        print('RESULTS')
        print('=' * 70)
        print(f'Total primes found: {len(primes):,}')
        print(f'Time elapsed: {time_elapsed:.3f} seconds')
        print('=' * 70 + '\n')

        show_primes = input('Show all primes? (y/n): ').strip().lower()
        if show_primes == 'y':
            print('\nPrimes:', ', '.join(map(str, primes)))

        verify = input('\nVerify with known count? (y/n): ').strip().lower()
        if verify == 'y':
            # Known prime counts for verification
            known_counts = {
                100: 25,
                1000: 168,
                10000: 1229,
                100000: 9592,
                1000000: 78498,
                10000000: 664579
            }

            if limit in known_counts:
                expected = known_counts[limit]
                matches = len(primes) == expected
                print(f'\nExpected count for {limit:,}: {expected}')
                print(f'Actual count: {len(primes)}')
                print(f'Verification: {"✓ PASSED" if matches else "✗ FAILED"}')
            else:
                print(f'\nNo known count available for {limit:,}')

    except KeyboardInterrupt:
        print('\n\nInterrupted by user.')
    except Exception as error:
        print(f'Error: {error}')


if __name__ == '__main__':
    main()
