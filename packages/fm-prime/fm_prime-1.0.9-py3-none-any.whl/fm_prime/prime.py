import math

def smallest_divisor(num):
    """
    Finds the smallest divisor of a given number.

    :param num: Integer to find the smallest divisor for.
    :return: Smallest divisor of the number.
    """
    if num % 2 == 0:
        return 2
    if num % 3 == 0:
        return 3

    limit = int(math.sqrt(num))
    for i in range(5, limit + 1, 6):
        if num % i == 0:
            return i
        if num % (i + 2) == 0:
            return i + 2

    return num

def prime_factorization(num):
    """
    Returns the prime factorization of a number in scientific notation.

    :param num: Integer to factorize.
    :return: String representation of prime factorization.
    """
    factors = {}
    while num != 1:
        divisor = smallest_divisor(num)
        factors[divisor] = factors.get(divisor, 0) + 1
        num //= divisor

    return " * ".join(
        f"{factor}**{power}" if power > 1 else f"{factor}"
        for factor, power in factors.items()
    )

def is_prime(num):
    """
    Checks if a number is prime.

    :param num: Integer to check.
    :return: True if the number is prime, otherwise False.
    """
    if num <= 1:
        return False
    if num in (2, 3):
        return True
    if num % 6 not in (1, 5):
        return False

    return num == smallest_divisor(num)

def is_sophie_prime(num):
    """
    Checks if a number is a Sophie prime.

    :param num: Integer to check.
    :return: String indicating if the number is a Sophie prime.
    """
    if not is_prime(num):
        return f"{num} is not a Prime."

    return (
        f"{num} is a Sophie Prime."
        if is_prime(2 * num + 1)
        else f"{num} is not a Sophie Prime."
    )

def is_mersenne_prime(num):
    """
    Checks if a number is a Mersenne prime.

    :param num: Integer to check.
    :return: String indicating if the number is a Mersenne prime.
    """
    if not is_prime(num):
        return f"{num} is not a Prime."

    mersenne_num = 2 ** num - 1
    return (
        f"{num} is a Mersenne Prime."
        if is_prime(mersenne_num)
        else f"{num} is not a Mersenne Prime."
    )

def is_twin_prime(num):
    """
    Checks if a number is a Twin prime.

    :param num: Integer to check.
    :return: String indicating if the number is a Twin prime.
    """
    if not is_prime(num):
        return f"{num} is not a Prime."

    twins = []
    if is_prime(num - 2):
        twins.append(f"{num} & {num - 2} : Twins")
    if is_prime(num + 2):
        twins.append(f"{num} & {num + 2} : Twins")

    return "\n".join(twins) if twins else "No Twins"

def is_isolated_prime(num):
    """
    Checks if a number is an Isolated prime.

    :param num: Integer to check.
    :return: String indicating if the number is an Isolated prime.
    """
    twin_result = is_twin_prime(num)
    if twin_result == "No Twins":
        return f"{num} is an Isolated Prime."
    if "not a Prime" in twin_result:
        return twin_result

    return f"{num} is not an Isolated Prime.\n{twin_result}"

def primes_count(num):
    """
    Lists all primes up to a given number or returns their count.

    :param num: Integer up to which primes are listed.
    :param count_only: Boolean to return only the count of primes.
    :return: Count of primes.
    """
    if num < 2:
        return 0

    count = 1
    for candidate in range(3, num + 1, 2):
        if is_prime(candidate):
            count += 1

    return count

def list_primes(num):
    """
    Lists all primes up to a given number or returns their count.

    :param num: Integer up to which primes are listed.
    :param count_only: Boolean to return only the count of primes.
    :return: List or count of primes.
    """
    if num < 2:
        return []

    primes = [2]
    for candidate in range(3, num + 1, 2):
        if is_prime(candidate):
            primes.append(candidate)

    return primes

def primes_in_range(start, end, count_only=False):
    """
    Lists primes within a specified range or returns their count.

    :param start: Starting number of the range.
    :param end: Ending number of the range.
    :param count_only: Boolean to return only the count of primes.
    :return: List or count of primes.
    """
    primes = [n for n in range(max(2, start), end + 1) if is_prime(n)]
    return len(primes) if count_only else primes

def primes_in_chunks(start, end, chunk_size=10000):
    """
    Splits primes within a range into chunks.

    :param start: Starting number of the range.
    :param end: Ending number of the range.
    :param chunk_size: Number of primes per chunk.
    :return: Dictionary with chunk indices and their primes.
    """
    primes = []
    chunked_primes = {}
    count = 0

    for n in range(max(2, start), end + 1):
        if is_prime(n):
            primes.append(n)
            count += 1
            if count % chunk_size == 0:
                chunked_primes[count] = ", ".join(map(str, primes))
                primes = []

    if primes:
        chunked_primes[count] = ", ".join(map(str, primes))

    return chunked_primes

