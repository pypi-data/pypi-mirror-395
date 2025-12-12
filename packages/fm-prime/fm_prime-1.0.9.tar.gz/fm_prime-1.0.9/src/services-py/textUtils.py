import os
from glob import glob


def num_folder_exist(number):
    """
    Checks if a folder for a specific number already exists.

    :param number: The number for which the folder should exist.
    :return: The folder path if it exists, otherwise False.
    """
    root_folder = "./output-big"
    dir_path = os.path.join(root_folder, f"output-{number}")

    if os.path.exists(dir_path):
        print(f"{dir_path} already exists...")
        return dir_path
    return False


def create_folder(parent_path, parent_name, child_name):
    """
    Creates a nested folder structure if it does not exist.

    :param parent_path: Path to the parent directory.
    :param parent_name: Name of the parent folder.
    :param child_name: Name of the child folder to create.
    :return: Path to the created folder or False if it already exists.
    """
    root_folder = os.path.join(parent_path, parent_name)
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)

    child_folder = os.path.join(root_folder, child_name)
    if not os.path.exists(child_folder):
        os.mkdir(child_folder)
        return child_folder
    return child_folder


def copy_file(source_path, destination_path):
    """
    Copies a file from source to destination.

    :param source_path: Path to the source file.
    :param destination_path: Path to the destination.
    """
    os.system(f"cp {source_path} {destination_path}")


def write_text_file(folder_path, file_name, data):
    """
    Writes data to a text file, creating or appending as necessary.

    :param folder_path: Path to the folder where the file will be created.
    :param file_name: Name of the file to create or append to.
    :param data: Data to write into the file.
    """
    file_path = os.path.join(folder_path, f"Output{file_name}.txt")
    with open(file_path, "a" if os.path.isfile(file_path) else "w") as file:
        file.write(data)


def write_data_to_file(folder_name, filename, data):
    """
    Writes data to a file, appending to it if it already exists.
    Handles both legacy OutputX.txt and new outputX.txt formats.

    :param folder_name: Path to the folder where the file will be created or updated.
    :param filename: Name of the file to write to.
    :param data: Data to write into the file.
    """
    # If filename already has an extension or starts with output/Output, use it as is
    if filename.endswith('.txt') or filename.lower().startswith('output'):
        file_path = os.path.join(folder_name, filename)
    else:
        file_path = os.path.join(folder_name, f"Output{filename}.txt")

    with open(file_path, "a") as file:
        file.write(data)


def list_files_and_folders(folder_path):
    """
    Lists all files and folders inside a specified directory.

    :param folder_path: Path to the directory.
    :return: List of files and folders inside the directory.
    """
    return glob(os.path.join(folder_path, "*"))


def sort_files_by_numeric_suffix(folder_path):
    """
    Sorts files by their numeric suffix in ascending order.

    :param folder_path: Path to the folder containing the files.
    :return: Sorted list of file paths.
    """
    files = list_files_and_folders(folder_path)
    return sorted(files, key=lambda x: (len(x), x))


def find_folder_for_number(number, folder_path):
    """
    Finds the appropriate folder containing or close to a given number.

    :param number: The target number to find a folder for.
    :param folder_path: Path to the parent directory containing folders.
    :return: Path to the appropriate folder or an error message if not found.
    """
    sorted_folders = sort_files_by_numeric_suffix(folder_path)
    for folder in sorted_folders:
        folder_number = int(folder.split("-")[-1])
        if folder_number >= number:
            return folder

    return f"\n{number} is larger than the available outputs.\n"


def find_file_for_number(number, folder_path):
    """
    Finds the file containing a specific number within the appropriate folder.

    :param number: The target number to find.
    :param folder_path: Path to the parent directory containing folders and files.
    :return: Path to the matching file or False if not found.
    """
    folder = find_folder_for_number(number, folder_path)
    if not folder:
        return False

    files = sort_files_by_numeric_suffix(folder)
    for file in files:
        with open(file, "r") as f:
            data = f.read().split("\n")
            first_prime = (data[1].split(",")[0]).split("| ")[1]
            last_prime = data[-2].split(",")[-2]
            if int(first_prime) <= number <= int(last_prime):
                return file

    return False


def file_contains_text(file_path, text):
    """
    Checks if a file contains a specific text.

    :param file_path: Path to the file.
    :param text: Text to search for.
    :return: True if the text is found, otherwise False.
    """
    with open(file_path, "r") as file:
        data = file.read()
        return f"| {text}," in data or f",{text}," in data


def find_files_up_to_number(number, folder_path):
    """
    Finds all files containing numbers up to a specified number.

    :param number: The target number.
    :param folder_path: Path to the folder containing the files.
    :return: List of file paths containing numbers up to the specified number.
    """
    folder = find_folder_for_number(number, folder_path)
    if folder:
        return search_files_up_to_number(folder, number)

    return []


def search_files_up_to_number(folder_path, number):
    """
    Searches files within a folder for those containing numbers up to a specified number.

    :param folder_path: Path to the folder.
    :param number: The target number.
    :return: List of file paths containing numbers up to the specified number.
    """
    result = []
    files = sort_files_by_numeric_suffix(folder_path)
    for file in files:
        with open(file, "r") as f:
            data = f.read().split("\n")
            first_prime = (data[1].split(",")[0]).split("| ")[1]
            if int(first_prime) > number:
                return result

            result.append(file)

    return result


def write_primes_to_split_files(folder_path, primes, max_file_size_kb=1024):
    """
    Write primes to folder, splitting into ~1MB files.
    Files are named by their first prime number.

    :param folder_path: Output folder path
    :param primes: List of primes (int or str)
    :param max_file_size_kb: Max file size in KB
    """
    if not primes:
        return

    current_file = []
    current_size = 0
    max_size_bytes = max_file_size_kb * 1024
    global_index = 0

    for prime in primes:
        prime_str = str(prime) + ','
        prime_size = len(prime_str.encode('utf-8'))

        if current_size + prime_size > max_size_bytes and current_file:
            first_prime = current_file[0]
            filename = f"output{first_prime}.txt"

            data = ""
            for j, p in enumerate(current_file):
                if j % 20 == 0:
                    prefix = "" if j == 0 else "\n"
                    data += f"{prefix}({global_index + j}) | "
                data += str(p) + ","

            data += f"\n({global_index + len(current_file)})"

            write_data_to_file(folder_path, filename, data)

            global_index += len(current_file)
            current_file = []
            current_size = 0

        current_file.append(prime)
        current_size += prime_size

    if current_file:
        first_prime = current_file[0]
        filename = f"output{first_prime}.txt"

        data = ""
        for j, p in enumerate(current_file):
            if j % 20 == 0:
                prefix = "" if j == 0 else "\n"
                data += f"{prefix}({global_index + j}) | "
            data += str(p) + ","

        data += f"\n({global_index + len(current_file)})"

        write_data_to_file(folder_path, filename, data)
