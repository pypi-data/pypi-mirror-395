"""
OPTIMIZED PRIME NUMBER OPERATIONS

This module provides highly optimized implementations for prime number operations:
1. Sieve of Eratosthenes for bulk prime generation (10-100x faster)
2. Optimized trial division using 6k±1 pattern
3. Miller-Rabin primality test for probabilistic testing
4. Wheel-30 factorization for candidate generation

Performance improvements:
- Sieve: O(n log log n) vs O(n√n) for trial division
- Miller-Rabin: O(k log³ n) vs O(√n) for trial division
- 6k±1 optimization: Tests 33% of candidates vs 100%
- Wheel-30: Tests 27% of candidates vs 100%
"""

import math
import random


# ============================================================================
# SIEVE OF ERATOSTHENES - Optimal for generating all primes up to a limit
# ============================================================================

def sieve_of_eratosthenes(limit):
    """
    Generates all prime numbers up to limit using Sieve of Eratosthenes.

    This is the fastest method for generating ALL primes up to a limit.
    Complexity: O(n log log n)

    :param limit: Upper bound (inclusive)
    :return: List of all primes up to limit

    Example:
        >>> sieve_of_eratosthenes(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit < 2:
        return []

    # Create a boolean array "is_prime" and initialize all as true
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Start with the smallest prime number, 2
    p = 2
    while p * p <= limit:
        # If is_prime[p] is not changed, then it's a prime
        if is_prime[p]:
            # Mark all multiples of p as not prime
            # Start from p*p because smaller multiples are already marked
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
        p += 1

    # Collect all numbers that are still marked as prime
    return [num for num in range(2, limit + 1) if is_prime[num]]


def segmented_sieve(start, end):
    """
    Generates all primes in range [start, end] using segmented sieve.

    More memory-efficient than regular sieve for large ranges.
    Uses O(√end) memory instead of O(end).

    :param start: Starting number (inclusive)
    :param end: Ending number (inclusive)
    :return: List of primes in the range

    Example:
        >>> segmented_sieve(100, 150)
        [101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    """
    if start < 2:
        start = 2
    if end < start:
        return []

    # Step 1: Generate all primes up to √end using regular sieve
    limit = int(math.sqrt(end)) + 1
    base_primes = sieve_of_eratosthenes(limit)

    # Step 2: Create a boolean array for the range [start, end]
    size = end - start + 1
    is_prime = [True] * size

    # Step 3: Use base primes to mark composites in range
    for prime in base_primes:
        # Find the first multiple of prime >= start
        first_multiple = ((start + prime - 1) // prime) * prime

        # Ensure we don't mark the prime itself if it's in range
        if first_multiple == prime:
            first_multiple += prime

        # Mark all multiples in range as composite
        for multiple in range(first_multiple, end + 1, prime):
            is_prime[multiple - start] = False

    # Handle edge case: if start <= 2, include 2
    result = []
    for i in range(size):
        num = start + i
        if is_prime[i] and num >= 2:
            result.append(num)

    return result


# ============================================================================
# OPTIMIZED TRIAL DIVISION with 6k±1 pattern
# ============================================================================

def smallest_divisor_optimized(num):
    """
    Finds the smallest divisor using 6k±1 optimization.

    All primes > 3 are of the form 6k±1, so we only test those candidates.
    This is 3x faster than testing all numbers.

    :param num: Number to find divisor for
    :return: Smallest divisor (returns num if prime)
    """
    if num <= 1:
        return num
    if num % 2 == 0:
        return 2
    if num % 3 == 0:
        return 3

    # All primes > 3 are of form 6k±1
    limit = int(math.sqrt(num))
    k = 5
    while k <= limit:
        if num % k == 0:
            return k
        if num % (k + 2) == 0:
            return k + 2
        k += 6

    return num


def is_prime_optimized(num):
    """
    Optimized primality test using 6k±1 pattern.

    3x faster than naive trial division.

    :param num: Number to test
    :return: True if prime, False otherwise
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False

    # Check using 6k±1 pattern
    limit = int(math.sqrt(num))
    k = 5
    while k <= limit:
        if num % k == 0 or num % (k + 2) == 0:
            return False
        k += 6

    return True


# ============================================================================
# MILLER-RABIN PRIMALITY TEST - Probabilistic but very fast
# ============================================================================

def miller_rabin(n, k=20):
    """
    Miller-Rabin probabilistic primality test.

    Much faster than trial division for large numbers.
    With k=20 rounds, error probability < 4^(-20) ≈ 9.1×10^(-13)

    :param n: Number to test
    :param k: Number of rounds (higher = more accurate)
    :return: True if probably prime, False if definitely composite

    Example:
        >>> miller_rabin(1000000007)  # Large prime
        True
        >>> miller_rabin(1000000008)  # Composite
        False
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

    # Witness loop
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
            return False

    return True


def is_prime_fast(num, use_miller_rabin_threshold=10000):
    """
    Intelligent prime checking that chooses the best algorithm.

    - Small numbers: Direct trial division with 6k±1
    - Large numbers: Miller-Rabin test

    :param num: Number to test
    :param use_miller_rabin_threshold: Use Miller-Rabin for numbers above this
    :return: True if prime, False otherwise
    """
    if num < use_miller_rabin_threshold:
        return is_prime_optimized(num)
    else:
        return miller_rabin(num)


# ============================================================================
# WHEEL-30 FACTORIZATION - Tests only 27% of candidates
# ============================================================================

class Wheel30:
    """
    Wheel-30 factorization eliminates multiples of 2, 3, and 5.
    Only tests numbers ≡ 1,7,11,13,17,19,23,29 (mod 30)

    This reduces candidates to 8/30 = 26.67% of all numbers.
    Better than 6k±1 which tests 33% of candidates.
    """

    # Numbers to test in each wheel rotation (mod 30)
    WHEEL = [1, 7, 11, 13, 17, 19, 23, 29]

    # Increments to next candidate
    INCREMENTS = [6, 4, 2, 4, 2, 4, 6, 2]

    @staticmethod
    def generate_candidates(start, end):
        """
        Generate prime candidates using Wheel-30.

        :param start: Starting number
        :param end: Ending number
        :yield: Candidate numbers that could be prime
        """
        # Yield small primes if in range
        small_primes = [2, 3, 5]
        for p in small_primes:
            if start <= p <= end:
                yield p

        # Find starting position in wheel
        if start < 7:
            n = 7
            pos = 1  # Start at second position (7)
        else:
            wheel_cycle = (start // 30) * 30
            pos = 0
            while wheel_cycle + Wheel30.WHEEL[pos] < start:
                pos = (pos + 1) % 8
            n = wheel_cycle + Wheel30.WHEEL[pos]

        # Generate candidates
        while n <= end:
            if n >= start:
                yield n
            pos = (pos + 1) % 8
            n += Wheel30.INCREMENTS[pos]

    @staticmethod
    def primes_in_range(start, end):
        """
        Find all primes in range using Wheel-30 + primality test.

        :param start: Starting number
        :param end: Ending number
        :return: List of primes
        """
        primes = []
        for candidate in Wheel30.generate_candidates(start, end):
            if is_prime_optimized(candidate):
                primes.append(candidate)
        return primes


# ============================================================================
# HIGH-LEVEL API - Choose best algorithm automatically
# ============================================================================

def list_primes_optimized(limit, method='auto'):
    """
    Generates all primes up to limit using the most appropriate algorithm.

    :param limit: Upper bound (inclusive)
    :param method: 'auto', 'sieve', 'trial', or 'wheel'
    :return: List of primes

    Methods:
    - 'sieve': Best for generating all primes up to limit
    - 'trial': Good for testing individual numbers
    - 'wheel': Good balance between sieve and trial division
    - 'auto': Automatically choose based on limit
    """
    if method == 'auto':
        # Use sieve for limits up to 10 million (very fast)
        # For larger limits, might want to use segmented sieve or other methods
        if limit <= 10_000_000:
            method = 'sieve'
        else:
            method = 'sieve'  # Still best for most cases

    if method == 'sieve':
        return sieve_of_eratosthenes(limit)
    elif method == 'wheel':
        return Wheel30.primes_in_range(2, limit)
    elif method == 'trial':
        return [n for n in range(2, limit + 1) if is_prime_optimized(n)]
    else:
        raise ValueError(f"Unknown method: {method}")


def primes_in_range_optimized(start, end, method='auto'):
    """
    Generates primes in range [start, end] using optimal algorithm.

    :param start: Starting number (inclusive)
    :param end: Ending number (inclusive)
    :param method: 'auto', 'segmented', 'sieve', or 'wheel'
    :return: List of primes
    """
    if method == 'auto':
        range_size = end - start
        # For small ranges, use wheel; for large ranges, use segmented sieve
        if range_size < 100_000:
            method = 'wheel'
        else:
            method = 'segmented'

    if method == 'segmented':
        return segmented_sieve(start, end)
    elif method == 'sieve':
        all_primes = sieve_of_eratosthenes(end)
        return [p for p in all_primes if p >= start]
    elif method == 'wheel':
        return Wheel30.primes_in_range(start, end)
    else:
        raise ValueError(f"Unknown method: {method}")


def prime_factorization_optimized(num):
    """
    Returns the prime factorization using optimized smallest_divisor.

    :param num: Number to factorize
    :return: String representation of factorization
    """
    factors = {}
    while num != 1:
        divisor = smallest_divisor_optimized(num)
        factors[divisor] = factors.get(divisor, 0) + 1
        num //= divisor

    return " * ".join(
        f"{factor}**{power}" if power > 1 else f"{factor}"
        for factor, power in factors.items()
    )


def primes_count_optimized(limit):
    """
    Counts primes up to limit using optimized sieve.

    Much faster than counting with trial division.

    :param limit: Upper bound
    :return: Count of primes
    """
    return len(sieve_of_eratosthenes(limit))


# ============================================================================
# BACKWARDS COMPATIBILITY - Same API as original prime.py
# ============================================================================

# These functions maintain the same interface as the original module
def smallest_divisor(num):
    return smallest_divisor_optimized(num)


def is_prime(num):
    return is_prime_fast(num)


def prime_factorization(num):
    return prime_factorization_optimized(num)


def list_primes(num):
    return list_primes_optimized(num)


def primes_count(num):
    return primes_count_optimized(num)


def primes_in_range(start, end, count_only=False):
    primes = primes_in_range_optimized(start, end)
    return len(primes) if count_only else primes


# Sophie, Twin, Isolated primes use the fast primality check
def is_sophie_prime(num):
    if not is_prime_fast(num):
        return f"{num} is not a Prime."
    return (
        f"{num} is a Sophie Prime."
        if is_prime_fast(2 * num + 1)
        else f"{num} is not a Sophie Prime."
    )


def is_twin_prime(num):
    if not is_prime_fast(num):
        return f"{num} is not a Prime."

    twins = []
    if is_prime_fast(num - 2):
        twins.append(f"{num} & {num - 2} : Twins")
    if is_prime_fast(num + 2):
        twins.append(f"{num} & {num + 2} : Twins")

    return "\n".join(twins) if twins else "No Twins"


def is_isolated_prime(num):
    twin_result = is_twin_prime(num)
    if twin_result == "No Twins":
        return f"{num} is an Isolated Prime."
    if "not a Prime" in twin_result:
        return twin_result

    return f"{num} is not an Isolated Prime.\n{twin_result}"


# ============================================================================
# BENCHMARK UTILITIES
# ============================================================================

def benchmark_comparison(limit=100000):
    """
    Compare performance of different methods.

    :param limit: Test limit
    :return: Dictionary with timing results
    """
    import time

    results = {}

    # Test sieve
    start = time.time()
    sieve_primes = sieve_of_eratosthenes(limit)
    results['sieve'] = time.time() - start

    # Test wheel-30
    start = time.time()
    wheel_primes = Wheel30.primes_in_range(2, limit)
    results['wheel-30'] = time.time() - start

    # Verify they match
    assert sieve_primes == wheel_primes, "Results don't match!"

    results['count'] = len(sieve_primes)
    results['speedup'] = results['wheel-30'] / results['sieve']

    return results


if __name__ == "__main__":
    # Example usage
    print("Optimized Prime Operations Demo")
    print("=" * 50)

    # Generate primes up to 1000 using sieve
    print("\nPrimes up to 100 (using Sieve):")
    primes = list_primes_optimized(100)
    print(primes)
    print(f"Count: {len(primes)}")

    # Test large prime with Miller-Rabin
    large_prime = 1000000007
    print(f"\nIs {large_prime} prime? {miller_rabin(large_prime)}")

    # Wheel-30 demonstration
    print("\nWheel-30 primes in range [100, 200]:")
    wheel_primes = Wheel30.primes_in_range(100, 200)
    print(wheel_primes)

    # Benchmark
    print("\nBenchmark (primes up to 100,000):")
    bench = benchmark_comparison(100000)
    print(f"Sieve time: {bench['sieve']:.4f}s")
    print(f"Wheel-30 time: {bench['wheel-30']:.4f}s")
    print(f"Speedup: {bench['speedup']:.2f}x")
    print(f"Primes found: {bench['count']}")
