"""
WHEEL-210 FACTORIZATION
Advanced wheel that eliminates multiples of 2, 3, 5, and 7
Tests only 23% of candidates (vs 33% for 6k±1)

Use this when maximum performance is needed for large-scale prime generation
"""

import math


class Wheel210:
    """
    Wheel-210: Eliminates multiples of 2, 3, 5, and 7
    Tests only 23% of candidates vs 27% for Wheel-30 or 33% for 6k±1
    """

    # All residues mod 210 that are coprime to 210
    # These are the only candidates that could possibly be prime (for n > 7)
    SPOKES = [
        1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
        107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157,
        163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 209
    ]

    # Increments between consecutive spokes (computed below)
    INCREMENTS = []

    @classmethod
    def _compute_increments(cls):
        """Pre-compute the gaps between consecutive spokes"""
        if cls.INCREMENTS:
            return

        for i in range(len(cls.SPOKES)):
            next_i = (i + 1) % len(cls.SPOKES)
            if next_i == 0:
                # Wrap around to next wheel rotation
                gap = 210 - cls.SPOKES[-1] + cls.SPOKES[0]
            else:
                gap = cls.SPOKES[next_i] - cls.SPOKES[i]
            cls.INCREMENTS.append(gap)

    @classmethod
    def generate_candidates(cls, start, end):
        """
        Generate all Wheel-210 candidates in range [start, end]

        :param start: Starting number (inclusive)
        :param end: Ending number (inclusive)
        :yield: Candidate numbers that could be prime

        Example:
            >>> list(Wheel210.generate_candidates(100, 150))
            [101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149]
        """
        # Yield small primes if in range
        small_primes = [2, 3, 5, 7, 11]
        for p in small_primes:
            if start <= p <= end:
                yield p

        if end < 13:
            return

        # Find starting position in wheel
        if start < 13:
            base = 0
            pos = 0
        else:
            base = (start // 210) * 210
            pos = 0
            # Find first spoke >= start
            while base + cls.SPOKES[pos] < start:
                pos = (pos + 1) % len(cls.SPOKES)

        # Generate candidates
        while True:
            current = base + cls.SPOKES[pos]

            if current > end:
                break

            if current >= start:
                yield current

            pos = (pos + 1) % len(cls.SPOKES)
            if pos == 0:
                base += 210

    @classmethod
    def next_candidate(cls, current):
        """
        Get the next Wheel-210 candidate after current

        :param current: Current number
        :return: Next Wheel-210 candidate

        Example:
            >>> Wheel210.next_candidate(100)
            101
            >>> Wheel210.next_candidate(101)
            103
        """
        # Handle small primes
        small_primes = [2, 3, 5, 7, 11, 13]
        for i, p in enumerate(small_primes[:-1]):
            if current < p:
                return p
        if current < 13:
            return 13

        # Find position in wheel
        base = (current // 210) * 210
        offset = current % 210

        # Find next spoke in current rotation
        for spoke in cls.SPOKES:
            if offset < spoke:
                return base + spoke

        # Move to next wheel rotation
        return base + 210 + cls.SPOKES[0]


# Compute increments on module load
Wheel210._compute_increments()


def sieve_wheel210(limit):
    """
    Sieve of Eratosthenes using Wheel-210
    Only tracks 23% of candidates for maximum memory efficiency

    :param limit: Upper bound (inclusive)
    :return: List of all primes up to limit

    Example:
        >>> primes = sieve_wheel210(100)
        >>> len(primes)
        25
    """
    if limit < 2:
        return []

    # Start with small primes
    primes = [2, 3, 5, 7]
    if limit < 11:
        return [p for p in primes if p <= limit]

    # Add 11 if in range
    if limit >= 11:
        primes.append(11)

    # Create sieve for Wheel-210 candidates only
    # This uses only 23% of the memory compared to full sieve!
    candidates = {}
    for candidate in Wheel210.generate_candidates(13, limit):
        candidates[candidate] = True

    # Mark multiples of 11 (11 is not in candidates since we start from 13)
    if limit >= 11:
        multiple = 11 * 11  # Start from 11²
        while multiple <= limit:
            if multiple in candidates:
                candidates[multiple] = False
            multiple += 11

    # Sieving phase
    sqrt_limit = int(math.sqrt(limit))

    for candidate in sorted(candidates.keys()):
        if not candidates[candidate]:
            continue

        if candidate > sqrt_limit:
            break

        # Mark multiples as composite
        # Start from candidate² (smaller multiples already marked)
        multiple = candidate * candidate
        while multiple <= limit:
            if multiple in candidates:
                candidates[multiple] = False
            multiple += candidate

    # Collect remaining primes
    for candidate, is_prime in sorted(candidates.items()):
        if is_prime:
            primes.append(candidate)

    return primes


def is_prime_wheel210(n):
    """
    Check if n is prime using Wheel-210 + trial division

    :param n: Number to test
    :return: True if prime, False otherwise

    Example:
        >>> is_prime_wheel210(97)
        True
        >>> is_prime_wheel210(98)
        False
    """
    if n < 2:
        return False
    if n in [2, 3, 5, 7, 11]:
        return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False

    # Check if n is in Wheel-210 form
    if n % 210 not in Wheel210.SPOKES:
        return False

    # Trial division using Wheel-210 candidates
    limit = int(math.sqrt(n))

    # Check small primes first
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if p > limit:
            return True
        if n % p == 0:
            return n == p

    # Check Wheel-210 candidates
    for candidate in Wheel210.generate_candidates(37, limit):
        if n % candidate == 0:
            return n == candidate

    return True


def primes_in_range_wheel210(start, end):
    """
    Find all primes in range [start, end] using Wheel-210

    :param start: Starting number (inclusive)
    :param end: Ending number (inclusive)
    :return: List of primes

    Example:
        >>> primes_in_range_wheel210(100, 200)
        [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, ...]
    """
    primes = []

    for candidate in Wheel210.generate_candidates(start, end):
        if is_prime_wheel210(candidate):
            primes.append(candidate)

    return primes


# ============================================================================
# BENCHMARKING AND COMPARISON
# ============================================================================

def benchmark_wheels(limit=100000):
    """
    Compare Wheel-6 (6k±1), Wheel-30, and Wheel-210

    :param limit: Test up to this limit
    :return: Dictionary with results
    """
    import time

    results = {}

    # Count Wheel-6 candidates (6k±1 pattern)
    count_w6 = 2  # 2 and 3
    k = 1
    while 6 * k - 1 <= limit:
        if 6 * k - 1 >= 5:
            count_w6 += 1
        if 6 * k + 1 <= limit:
            count_w6 += 1
        k += 1

    results['wheel6'] = {
        'candidates': count_w6,
        'percentage': count_w6 / limit * 100
    }

    # Count Wheel-30 candidates
    from prime_optimized import Wheel30
    count_w30 = len(list(Wheel30.generate_candidates(2, limit)))

    results['wheel30'] = {
        'candidates': count_w30,
        'percentage': count_w30 / limit * 100
    }

    # Count Wheel-210 candidates
    count_w210 = len(list(Wheel210.generate_candidates(2, limit)))

    results['wheel210'] = {
        'candidates': count_w210,
        'percentage': count_w210 / limit * 100
    }

    # Calculate improvements
    results['improvements'] = {
        'w6_to_w30': (1 - count_w30 / count_w6) * 100,
        'w30_to_w210': (1 - count_w210 / count_w30) * 100,
        'w6_to_w210': (1 - count_w210 / count_w6) * 100,
    }

    # Benchmark sieve operations
    from prime_optimized import sieve_of_eratosthenes

    # Traditional sieve
    start = time.time()
    primes_traditional = sieve_of_eratosthenes(limit)
    results['traditional_sieve_time'] = time.time() - start

    # Wheel-210 sieve
    start = time.time()
    primes_w210 = sieve_wheel210(limit)
    results['wheel210_sieve_time'] = time.time() - start

    results['primes_count'] = len(primes_traditional)
    results['results_match'] = primes_traditional == primes_w210

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("WHEEL-210 DEMONSTRATION")
    print("=" * 60)

    # Test 1: Generate candidates
    print("\n1. Generating Wheel-210 candidates in [100, 150]:")
    candidates = list(Wheel210.generate_candidates(100, 150))
    print(f"   Candidates: {candidates}")
    print(f"   Count: {len(candidates)} (vs 51 if testing all)")

    # Test 2: Next candidate function
    print("\n2. Testing next_candidate function:")
    current = 100
    for _ in range(10):
        next_val = Wheel210.next_candidate(current)
        print(f"   After {current}: {next_val}")
        current = next_val

    # Test 3: Prime checking
    print("\n3. Testing primality with Wheel-210:")
    test_numbers = [97, 98, 99, 100, 101, 102, 103]
    for num in test_numbers:
        result = is_prime_wheel210(num)
        print(f"   {num}: {'PRIME' if result else 'composite'}")

    # Test 4: Primes in range
    print("\n4. Finding primes in [1000, 1100] with Wheel-210:")
    primes = primes_in_range_wheel210(1000, 1100)
    print(f"   Found {len(primes)} primes")
    print(f"   Primes: {primes}")

    # Test 5: Sieve comparison
    print("\n5. Sieve with Wheel-210 up to 10,000:")
    primes = sieve_wheel210(10000)
    print(f"   Found {len(primes)} primes")
    print(f"   First 20: {primes[:20]}")
    print(f"   Last 10: {primes[-10:]}")

    # Test 6: Benchmark
    print("\n6. Benchmarking wheels up to 100,000:")
    results = benchmark_wheels(100000)

    print(f"\n   Candidate Generation:")
    print(f"   Wheel-6 (6k±1):   {results['wheel6']['candidates']:>7,} ({results['wheel6']['percentage']:.1f}%)")
    print(f"   Wheel-30:         {results['wheel30']['candidates']:>7,} ({results['wheel30']['percentage']:.1f}%)")
    print(f"   Wheel-210:        {results['wheel210']['candidates']:>7,} ({results['wheel210']['percentage']:.1f}%)")

    print(f"\n   Improvements:")
    print(f"   Wheel-6 → Wheel-30:  {results['improvements']['w6_to_w30']:.1f}% fewer candidates")
    print(f"   Wheel-30 → Wheel-210: {results['improvements']['w30_to_w210']:.1f}% fewer candidates")
    print(f"   Wheel-6 → Wheel-210: {results['improvements']['w6_to_w210']:.1f}% fewer candidates")

    print(f"\n   Sieve Performance:")
    print(f"   Traditional sieve: {results['traditional_sieve_time']:.6f}s")
    print(f"   Wheel-210 sieve:   {results['wheel210_sieve_time']:.6f}s")
    print(f"   Results match: {results['results_match']}")
    print(f"   Primes found: {results['primes_count']:,}")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
