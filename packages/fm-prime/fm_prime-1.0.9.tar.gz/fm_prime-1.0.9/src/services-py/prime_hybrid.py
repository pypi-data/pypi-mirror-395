"""
HYBRID PRIME FINDER
Combines 6k±1 pattern with Miller-Rabin and Sieve for maximum performance

This module demonstrates how to combine multiple optimization techniques:
1. Pre-computed sieve for small primes (instant lookup)
2. 6k±1 pattern for candidate generation (skip 2/3 of numbers)
3. Trial division for medium primes
4. Miller-Rabin for large primes (probabilistic but very fast)
"""

import math
from prime_optimized import sieve_of_eratosthenes, miller_rabin


class HybridPrimeFinder:
    """
    Intelligent prime finder that uses the best algorithm for each scenario
    """

    def __init__(self, precompute_limit=100000):
        """
        Initialize with pre-computed primes for fast lookup

        :param precompute_limit: Generate primes up to this limit for quick lookup
        """
        print(f"Pre-computing primes up to {precompute_limit:,}...")
        self.small_prime_limit = precompute_limit
        self.small_primes_set = set(sieve_of_eratosthenes(precompute_limit))
        self.small_primes_list = sorted(self.small_primes_set)
        print(f"Pre-computed {len(self.small_primes_list):,} primes")

    def is_prime(self, n):
        """
        Intelligently test if n is prime using the best algorithm

        :param n: Number to test
        :return: True if prime, False otherwise
        """
        # Negative numbers and 0, 1 are not prime
        if n < 2:
            return False

        # Use pre-computed lookup for small numbers (instant!)
        if n <= self.small_prime_limit:
            return n in self.small_primes_set

        # Quick divisibility checks (before expensive operations)
        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
            return False

        # Check if it's in 6k±1 form (fundamental pattern)
        # All primes > 3 must be of form 6k±1
        if not (n % 6 == 1 or n % 6 == 5):
            return False

        # For medium numbers, use trial division with 6k±1 optimization
        if n < 10_000_000:
            return self._trial_division_6k_optimized(n)

        # For very large numbers, use Miller-Rabin (probabilistic but extremely fast)
        return miller_rabin(n, k=20)

    def _trial_division_6k_optimized(self, n):
        """
        Trial division using 6k±1 pattern
        Only tests candidates that could be prime
        """
        limit = int(math.sqrt(n))

        # Test against pre-computed small primes first (very fast)
        for p in self.small_primes_list:
            if p > limit:
                break
            if n % p == 0:
                return False

        # If we've checked beyond sqrt, it's prime
        if self.small_primes_list[-1] >= limit:
            return True

        # Continue with 6k±1 candidates beyond our pre-computed range
        k = ((self.small_primes_list[-1] + 1) // 6) + 1

        while True:
            candidate1 = 6 * k - 1
            candidate2 = 6 * k + 1

            if candidate1 > limit:
                break

            if n % candidate1 == 0 or n % candidate2 == 0:
                return False

            k += 1

        return True

    def find_nth_prime(self, n):
        """
        Find the nth prime number (1-indexed)

        :param n: Which prime to find (1st, 2nd, 3rd, etc.)
        :return: The nth prime

        Example:
            >>> finder.find_nth_prime(1)
            2
            >>> finder.find_nth_prime(100)
            541
        """
        if n <= 0:
            raise ValueError("n must be positive")

        # Use pre-computed primes if possible
        if n <= len(self.small_primes_list):
            return self.small_primes_list[n - 1]

        # Otherwise, continue searching with 6k±1 pattern
        count = len(self.small_primes_list)
        candidate = self.small_primes_list[-1] + 2

        while count < n:
            if self.is_prime(candidate):
                count += 1
                if count == n:
                    return candidate
            candidate = self._next_6k_candidate(candidate)

        return candidate

    def find_primes_in_range(self, start, end):
        """
        Find all primes in range [start, end] using 6k±1 optimization

        :param start: Starting number (inclusive)
        :param end: Ending number (inclusive)
        :return: List of primes in range
        """
        primes = []

        # Handle small primes
        if start <= 2 <= end:
            primes.append(2)
        if start <= 3 <= end:
            primes.append(3)

        # Use pre-computed primes if range is small
        if end <= self.small_prime_limit:
            return [p for p in self.small_primes_list if start <= p <= end]

        # Generate 6k±1 candidates and test them
        k = max(1, (start - 1) // 6 + 1)

        while True:
            candidate1 = 6 * k - 1
            candidate2 = 6 * k + 1

            if candidate1 > end:
                break

            if start <= candidate1 <= end and candidate1 > 3:
                if self.is_prime(candidate1):
                    primes.append(candidate1)

            if start <= candidate2 <= end:
                if self.is_prime(candidate2):
                    primes.append(candidate2)

            k += 1

        return sorted(primes)

    def find_twin_primes_in_range(self, start, end):
        """
        Find all twin prime pairs in range [start, end]

        Twin primes are pairs of primes that differ by 2 (e.g., 11 and 13)

        :param start: Starting number
        :param end: Ending number
        :return: List of twin prime pairs as tuples
        """
        primes = self.find_primes_in_range(start, end + 2)  # Include p+2
        primes_set = set(primes)

        twin_pairs = []
        for p in primes:
            if start <= p <= end and (p + 2) in primes_set:
                twin_pairs.append((p, p + 2))

        return twin_pairs

    def find_sophie_germain_primes_in_range(self, start, end):
        """
        Find all Sophie Germain primes in range [start, end]

        Sophie Germain prime: A prime p where 2p + 1 is also prime

        :param start: Starting number
        :param end: Ending number
        :return: List of Sophie Germain primes
        """
        sophie_primes = []

        for p in self.find_primes_in_range(start, end):
            safe_prime = 2 * p + 1
            if self.is_prime(safe_prime):
                sophie_primes.append(p)

        return sophie_primes

    def _next_6k_candidate(self, current):
        """
        Find next 6k±1 candidate
        This implements your pattern!
        """
        if current == 2:
            return 3
        if current == 3:
            return 5

        remainder = current % 6
        if remainder == 5:
            return current + 2  # From 6k-1 to 6k+1
        elif remainder == 1:
            return current + 4  # From 6k+1 to 6(k+1)-1
        else:
            # Not on 6k±1 form, jump to next 6k-1
            return ((current // 6) + 1) * 6 - 1


def sieve_6k_optimized(limit):
    """
    6k±1 OPTIMIZED SIEVE OF ERATOSTHENES

    Combines the speed of sieve with 6k±1 pattern
    Uses 3x less memory than traditional sieve!

    :param limit: Upper bound
    :return: List of all primes up to limit
    """
    if limit < 2:
        return []
    if limit == 2:
        return [2]
    if limit == 3:
        return [2, 3]

    # Start with small primes
    primes = [2, 3]

    # Create a dictionary for 6k±1 candidates only
    # This uses 3x less memory!
    candidates = {}

    k = 1
    while True:
        candidate1 = 6 * k - 1  # 6k - 1
        candidate2 = 6 * k + 1  # 6k + 1

        if candidate1 > limit:
            break

        if candidate1 >= 5:
            candidates[candidate1] = True
        if candidate2 <= limit:
            candidates[candidate2] = True

        k += 1

    # Sieve phase: mark composites
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
    for candidate, is_prime in candidates.items():
        if is_prime:
            primes.append(candidate)

    return sorted(primes)


def find_primes_6k_miller_rabin(start, end):
    """
    Combine 6k±1 candidate generation with Miller-Rabin testing
    Perfect for finding large primes!

    :param start: Starting number
    :param end: Ending number
    :return: List of primes in range
    """
    primes = []

    # Handle small primes
    if start <= 2 <= end:
        primes.append(2)
    if start <= 3 <= end:
        primes.append(3)

    # Generate 6k±1 candidates
    k = max(1, (start - 1) // 6 + 1)

    while True:
        candidate1 = 6 * k - 1
        candidate2 = 6 * k + 1

        if candidate1 > end:
            break

        if start <= candidate1 <= end and candidate1 > 3:
            if miller_rabin(candidate1, k=20):
                primes.append(candidate1)

        if start <= candidate2 <= end:
            if miller_rabin(candidate2, k=20):
                primes.append(candidate2)

        k += 1

    return primes


# ============================================================================
# DEMONSTRATION AND BENCHMARKING
# ============================================================================

if __name__ == "__main__":
    import time

    print("=" * 60)
    print("HYBRID PRIME FINDER DEMONSTRATION")
    print("=" * 60)

    # Initialize finder
    finder = HybridPrimeFinder(precompute_limit=100000)

    # Test 1: Check individual primes
    print("\n1. Testing individual numbers:")
    test_numbers = [997, 10007, 1000003, 1000000007, 2**61 - 1]

    for num in test_numbers:
        start = time.time()
        result = finder.is_prime(num)
        duration = time.time() - start
        print(f"   {num:>20,}: {'PRIME' if result else 'NOT PRIME':12} ({duration*1000:.3f}ms)")

    # Test 2: Find nth prime
    print("\n2. Finding nth primes:")
    for n in [100, 1000, 10000]:
        start = time.time()
        prime = finder.find_nth_prime(n)
        duration = time.time() - start
        print(f"   {n:>6,}th prime: {prime:>12,} ({duration*1000:.3f}ms)")

    # Test 3: Primes in range
    print("\n3. Finding primes in range:")
    ranges = [(100, 200), (10000, 10100), (1000000, 1000100)]

    for start_num, end_num in ranges:
        start = time.time()
        primes = finder.find_primes_in_range(start_num, end_num)
        duration = time.time() - start
        print(f"   [{start_num:>8,}, {end_num:>8,}]: {len(primes):>3} primes ({duration*1000:.3f}ms)")

    # Test 4: Twin primes
    print("\n4. Finding twin primes:")
    start = time.time()
    twins = finder.find_twin_primes_in_range(100, 1000)
    duration = time.time() - start
    print(f"   Found {len(twins)} twin prime pairs in [100, 1000]")
    print(f"   First few: {twins[:5]}")
    print(f"   Time: {duration*1000:.3f}ms")

    # Test 5: Sophie Germain primes
    print("\n5. Finding Sophie Germain primes:")
    start = time.time()
    sophie = finder.find_sophie_germain_primes_in_range(100, 1000)
    duration = time.time() - start
    print(f"   Found {len(sophie)} Sophie Germain primes in [100, 1000]")
    print(f"   First few: {sophie[:10]}")
    print(f"   Time: {duration*1000:.3f}ms")

    # Test 6: Compare sieve methods
    print("\n6. Comparing sieve implementations:")
    limit = 100000

    # Traditional sieve
    start = time.time()
    primes_traditional = sieve_of_eratosthenes(limit)
    time_traditional = time.time() - start

    # 6k±1 optimized sieve
    start = time.time()
    primes_6k = sieve_6k_optimized(limit)
    time_6k = time.time() - start

    print(f"   Traditional sieve: {time_traditional:.6f}s")
    print(f"   6k±1 sieve:       {time_6k:.6f}s")
    print(f"   Speedup:          {time_traditional/time_6k:.2f}x")
    print(f"   Results match:    {primes_traditional == primes_6k}")
    print(f"   Primes found:     {len(primes_6k):,}")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
