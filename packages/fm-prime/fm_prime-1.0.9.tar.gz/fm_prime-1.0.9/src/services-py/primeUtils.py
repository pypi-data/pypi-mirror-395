from textUtils import (
    create_folder,
    write_data_to_file,
    sort_files_by_numeric_suffix,
    find_folder_for_number,
    find_file_for_number,
    find_files_up_to_number,
    file_contains_text,
    copy_file,
    num_folder_exist,
    write_text_file,
    list_files_and_folders,
)
from prime import is_prime
import os

folder_path = "output-big"


def create_prime_folder(number, base_folder=folder_path):
    """
    Creates a folder for storing primes associated with the given number.

    :param number: The target number.
    :param base_folder: Path to the base folder.
    """
    return create_folder(".", base_folder, f"output-{number}")


def write_prime_file(folder_number, filename, data, base_folder=folder_path):
    """
    Creates or appends data to a prime output file.

    :param folder_number: Number identifying the folder.
    :param filename: name of the output file.
    :param data: Data to write to the file.
    :param base_folder: Path to the base folder.
    """
    write_data_to_file(folder_number, filename, data)


def get_sorted_prime_folders():
    """
    Retrieves all prime folders sorted by numeric suffix.

    :return: Sorted list of prime folders.
    """
    return sort_files_by_numeric_suffix(folder_path)


def get_sorted_prime_files(folder_name):
    """
    Retrieves all prime files inside a folder sorted by numeric suffix.

    :param folder_name: Path to the folder.
    :return: Sorted list of prime files.
    """
    return sort_files_by_numeric_suffix(folder_name)


def get_last_prime_folder():
    """
    Retrieves the last prime folder.

    :return: Path to the last prime folder.
    """
    folders = get_sorted_prime_folders()
    return folders[-1]


def get_proper_prime_folder(number):
    """
    Finds the proper folder for a specific prime number.

    :param number: The target number.
    :return: Path to the matching folder or an error message.
    """
    return find_folder_for_number(number, folder_path)


def get_proper_prime_file(number):
    """
    Finds the proper file for a specific prime number.

    :param number: The target number.
    :return: Path to the matching file or False if not found.
    """
    return find_file_for_number(number, folder_path)


def get_all_files_for_division(number):
    """
    Retrieves all files containing numbers up to a specific number.

    :param number: The target number.
    :return: List of matching file paths.
    """
    return find_files_up_to_number(number, folder_path)


def get_numbers_in_file(file_path):
    """
    Extracts all numbers from a file as a list.

    :param file_path: Path to the file.
    :return: List of numbers in the file.
    """
    with open(file_path, "r") as file:
        data = file.read().strip()
        data = "".join(
            [
                line.split("| ")[-1] if "| " in line else line
                for line in data.split("\n")
            ]
        )
        data = data.split(",")
        data.pop()
        return data


def is_prime_in_files(number):
    """
    Checks if a number exists in the prime files.

    :param number: The target number.
    :return: True if the number exists in the files, otherwise False.
    """
    file_path = get_proper_prime_file(number)
    if not file_path:
        return False
    return file_contains_text(file_path, str(number))


def copy_prime_files(files, new_folder_number, up_to_index):
    """
    Copies prime files to a new folder up to a specified index.

    :param files: List of file paths.
    :param new_folder_number: Target folder number.
    :param up_to_index: Index up to which files should be copied.
    """
    for i in range(up_to_index):
        source_file = files[i]
        destination_folder = f"{folder_path}/output-{new_folder_number}"
        file_name = source_file.split("Output")[1]
        copy_file(source_file, f"{destination_folder}/Output{file_name}")


def check_divisor_from_files(num, folder):
    """
    Checks if a number is divisible by any prime number listed in the files within a given folder.

    :param num: The number to check divisors for.
    :param folder: Path to the folder containing files with prime numbers.
    :return: True if a divisor is found; otherwise, False.
    """
    # Check if the number is already marked as prime in the files
    if is_prime_in_files(num):
        return False

    # Use the get_sorted_prime_files method to retrieve and sort all files
    files = get_sorted_prime_files(folder)
    # Iterate over files to find a divisor
    for file in files:
        primes = get_numbers_in_file(file)
        for prime in primes:
            if num % int(prime) == 0:
                print(f"{num} is divisible by {prime}")
                return True

    return False


def find_next_candidate(current):
    """
    Finds the next candidate number for prime checking using a 6k ± 1 optimization.

    :param current: The current candidate number.
    :return: The next candidate number.
    """
    if current == 2:
        return 3
    if current == 3:
        return 5

    remainder = current % 6
    if remainder == 5:
        return current + 2
    elif remainder == 1:
        return current + 4
    else:
        # Default to the 6k ± 1 formula
        quotient = current // 6
        return (quotient + 1) * 6 - 1


def generate_primes_up_to(
    number, current=2, data_buffer="", count=0, page_index=0, folder_path=folder_path
):
    """
    Generates primes up to a given number and writes them into files.

    :param number: The upper limit up to which primes should be generated.
    :param current: The starting number for generating primes (default is 2).
    :param count: Counter for the total primes generated (default is 0).
    :param page_index: Index of the current file being written (default is 0).
    :param folder_path: Path to the folder where output files will be stored.
    :return: Total count of primes generated.
    """
    # Check if folder already exists
    if num_folder_exist(number):
        return

    folder_name = create_folder(".", folder_path, f"output-{number}")
    while current <= number:
        if is_prime(current):
            print(f"Current prime: {current}")
            if count % 1000000 == 0 and count != 0:
                if f"({count})" not in data_buffer:
                    data_buffer += f"\n({count})"
                write_text_file(folder_name, page_index, data_buffer)
                data_buffer = ""
                page_index += 1

            data_buffer += (
                f"\n({count}) | {current}," if count % 20 == 0 else f"{current},"
            )
            count += 1

        current += 1

    # Write remaining primes to file
    if data_buffer:
        write_text_file(folder_name, page_index, data_buffer + f"\n({count})")

    return count


def filter_line_data(line, num, last_count=""):
    """
    Filters a line of prime numbers based on a given number and updates count information.

    :param line: A string containing prime numbers separated by commas.
    :param num: The number to filter the line against.
    :param last_count: The last count value (optional).
    :return: A tuple containing the filtered line and a boolean indicating whether to continue processing.
    """
    line_elements = line.split(",")
    # line_elements_size = len(line_elements)
    last_prime = line_elements[-2]

    if int(last_prime) < num:
        if int(last_prime) != num:
            return line, True
        else:
            return f"{line},\n({last_count})", False

    first_element_array = line_elements[0].split(" | ")
    line_elements[0] = first_element_array[1]
    count_to_last_line = first_element_array[0].replace("(", "").replace(")", "")
    count = int(count_to_last_line)

    if int(line_elements[0]) > num:
        return f"({count})", False

    filtered_last_line = []
    for item in line_elements[:-1]:
        if int(item) <= num:
            count += 1
            filtered_last_line.append(item)

    filtered_last_line[0] = f"({count_to_last_line}) | {filtered_last_line[0]}"
    return f"{','.join(filtered_last_line)},\n({count})", False


def copy_all_files(files, source_path, target_folder):
    """
    Copies all files except the last one to the target folder.

    :param files: List of file names.
    :param source_path: Path to the source folder.
    :param target_folder: Path to the target folder.
    :return: Name of the last file.
    """
    for file in files[:-1]:
        os.system(
            f"cp {os.path.join(source_path, file)} {os.path.join(target_folder, file)}"
        )
    return files[-1]


def format_last_file_in_last_folder_recursive(
    source_folder, last_file, last_number, sqrt_num
):
    """
    Formats the last file in a folder and recursively generates primes.

    :param source_folder: Path to the source folder.
    :param last_file: Name of the last file.
    :param last_number: The last number processed.
    :param sqrt_num: The square root of the number to process.
    """
    with open(last_file, "r") as file:
        file_lines = file.read().strip().split("\n")
    last_count = int(file_lines.pop().replace("(", "").replace(")", ""))
    data_buffer = "\n".join(file_lines)
    page_index = int(last_file.split("Output")[1].replace(".txt", ""))
    last_number = find_next_candidate(last_number)
    generate_primes_up_to(sqrt_num, last_number, data_buffer, last_count, page_index)


def copy_files_and_format_last_file(num):
    """
    Copies files from the last folder and formats the last file for a new folder.

    :param num: The upper limit of primes.
    """
    source = "./output-big"
    last_folder_path = get_last_prime_folder()
    files = sort_files_by_numeric_suffix(last_folder_path)
    last_file = files[-1]
    last_number = int(
        last_folder_path.replace("output-big/", "").replace("output-", "")
    )
    format_last_file_in_last_folder_recursive(
        last_folder_path, last_file, last_number, num
    )
    target_folder_path = os.path.join(source, f"output-{num}")
    copy_all_files(files, last_folder_path, target_folder_path)


def copy_selected_files(source_folder, target_folder, files, num):
    """
    Copies selected files containing primes up to a given number.

    :param source_folder: Path to the source folder.
    :param target_folder: Path to the target folder.
    :param files: List of file names.
    :param num: The upper limit of primes.
    :return: Name of the last selected file.
    """
    selected_files = [
        file
        for file in files
        if int(open(file).read().split("| ")[1].split(",")[0]) <= num
    ]

    for file in selected_files[:-1]:
        os.system(
            f"cp {os.path.join(source_folder, file)} {os.path.join(target_folder, file)}"
        )
    return selected_files[-1]


def formatted_data_from_selected_file(source_folder, selected_file, num):
    """
    Formats data from a selected file by filtering lines based on a given number.

    :param source_folder: Path to the source folder.
    :param selected_file: Name of the selected file.
    :param num: The upper limit of primes.
    :return: Filtered data as a string.
    """
    with open(selected_file, "r") as file:
        file_lines = file.read().strip().split("\n")

    last_count = file_lines.pop()
    last_filtered_data = []

    for line in file_lines:
        line_result = filter_line_data(line, num, last_count)
        last_filtered_data.append(line_result[0])
        if not line_result[1]:
            break

    return "\n".join(last_filtered_data)


def copy_all_prime_outputs(source_folder, num, get_dirs_func):
    """
    Copies all prime outputs from source to target and filters data.

    :param source_folder: Path to the source folder.
    :param num: The upper limit of primes.
    :param get_dirs_func: Function to retrieve directories.
    :return: Filtered data and folder details.
    """
    files = sort_files_by_numeric_suffix(source_folder)
    target_folder = create_folder(".", "output-big", f"output-{num}")
    selected_file = copy_selected_files(source_folder, target_folder, files, num)

    last_filtered_data = formatted_data_from_selected_file(
        source_folder, selected_file, num
    )
    return last_filtered_data, target_folder, selected_file


def generate_prime_output_from_text(num, get_dirs_func=list_files_and_folders):
    """
    Generates prime output data from existing files and writes it to new files.

    :param num: The upper limit of primes to generate.
    :param get_dirs_func: Function to retrieve directories (default: list_files_and_folders).
    :return: Status message.
    """
    source_folder = get_last_prime_folder()
    folder_number = int(source_folder.replace("output-big/", "").replace("output-", ""))
    if int(folder_number) < num:
        return f"{num} is greater than largest output"

    last_filtered_data, folder, target_file_name = copy_all_prime_outputs(
        source_folder, num, get_dirs_func
    )
    target_file_name = target_file_name.split("Output")[1].replace(".txt", "")
    write_prime_file(folder, target_file_name, last_filtered_data)
    return f"{folder} has been created."
