import os
from .textUtils import (
    find_folder_for_number,
    list_files_and_folders
)

from pathlib import Path

def calculate_non_prime_indices(k2, t):
    k1 = k2 + t
    p = k1**2 - k2**2

    return {
        1: 6 * p - 2 * k1,
        2: 6 * (p + t) - 2 * k1 - 1,
        3: 6 * p + 2 * k1,
        4: 6 * (p + t) + 2 * k1 + 1,
        5: 6 * p - 2 * k2,
        6: 6 * (p + t) - 2 * k2 - 1,
        7: 6 * p + 2 * k2,
        8: 6 * (p + t) + 2 * k2 + 1,
    }

def read_non_prime_indices_from_file(file_path):
    if not Path(file_path).exists():
        return set()
    with open(file_path, "r") as f:
        return set(map(int, f.read().split(",")))

def create_output_folder(number):
    root_folder = Path("./not-prime-indexes")
    if not Path(root_folder).exists():
        root_folder.mkdir(parents=True, exist_ok=True)

    folder_path = Path(f"{root_folder}/output-{number}")
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

def write_to_file(number, folder, indices, filename):
    if not Path(folder).exists():
        create_output_folder(number)
    with open(f"{folder}/{filename}.txt", "w") as f:
        f.write(",".join(map(str, sorted(indices))))

def generate_non_prime_indices(number, k2=0, t=1):
    folder = f"./not-prime-indexes/output-{number}"
    pattern_one_file = f"{folder}/OutputPattern1.txt"
    pattern_two_file = f"{folder}/OutputPattern2.txt"

    pattern_one_indices = read_non_prime_indices_from_file(pattern_one_file)
    pattern_two_indices = read_non_prime_indices_from_file(pattern_two_file)

    indices = calculate_non_prime_indices(k2, t)
    min_index = indices[1]
    max_index = (number + 1) // 6

    while k2 <= max_index:
        for key, ind in indices.items():
            if ind > max_index:
                continue
            if key <= 4:
                pattern_one_indices.add(ind)
            else:
                pattern_two_indices.add(ind)
            min_index = min(min_index, ind)

        if min_index > max_index:
            t = 1
            k2 += 1
        else:
            t += 1

        indices = calculate_non_prime_indices(k2, t)
        min_index = indices[1]

    write_to_file(number, folder, pattern_one_indices, "OutputPattern1")
    write_to_file(number, folder, pattern_two_indices, "OutputPattern2")
    return pattern_one_indices, pattern_two_indices

def calculate_primes(number):
    numFolder = f"./not-prime-indexes/output-{number}"

    if Path(numFolder).exists():
        print(f"Primes for {number} already exist.")
        return

    pattern_one_indices, pattern_two_indices = generate_non_prime_indices(number)
    primes = {2, 3}
    maxIndex = (number + 1) // 6
    for index in range(1, maxIndex + 1):
        pattern_one_number = 6 * index + 1
        pattern_two_number = 6 * index - 1

        if index not in pattern_one_indices:
            primes.add(pattern_one_number)
        if index not in pattern_two_indices:
            primes.add(pattern_two_number)

    primes = sorted(filter(lambda x: x <= number, primes))
    write_to_file(number, numFolder, primes, f"OutputPrimes-{len(primes)}")
    print(f"Primes up to {number} written to {numFolder}")

def copy_from_other_folder(number, root_folder, num_folder):

    max_index = (number + 1) // 6
    matched_folder = find_folder_for_number(number, root_folder)

    if "is larger" in matched_folder:
        return False

    # Initialize sets to store indices and primes
    pattern_one_indices, pattern_two_indices, primes = set(), set(), set()

    # Process all files in the matched folder
    for filename in list_files_and_folders(matched_folder):
        if "OutputPattern1" in filename:
            pattern_one_indices.update(
                x for x in read_non_prime_indices_from_file(filename) if x <= max_index
            )
        elif "OutputPattern2" in filename:
            pattern_two_indices.update(
                x for x in read_non_prime_indices_from_file(filename) if x <= max_index
            )
        elif "OutputPrimes" in filename:
            primes.update(
                x for x in read_non_prime_indices_from_file(filename) if x <= number
            )
        
    # Write data to the target folder
    write_to_file(number, num_folder, pattern_one_indices, "OutputPattern1")
    write_to_file(number, num_folder, pattern_two_indices, "OutputPattern2")
    write_to_file(number, num_folder, primes, f"OutputPrimes-{len(primes)}")
    return True

def calculate_primes_text(number):

    root_folder = Path("./not-prime-indexes")
    num_folder = Path(f"{root_folder}/output-{number}")

    # Check if the folder already exists
    if num_folder.exists():
        print(f"{num_folder} already exists.")
        return

    # Attempt to copy data from another matching folder
    if copy_from_other_folder(number, root_folder, num_folder):
        print(f"Primes up to {number} copied from an existing folder.")
        return

    calculate_primes(number)

# calculate_primes_text(12000000)