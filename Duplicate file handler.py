# write your code here
import argparse
import os
import hashlib
# import sys
# args = sys.argv
#     if len(args) < 2:
#         print('Directory is not specified')

parser = argparse.ArgumentParser(description="You must enter a folder to list files in dir and subdir")
parser.add_argument("folder", nargs="?")
args = parser.parse_args()
choice = args.folder
FILTER_BY_EXTENSION = False


# Function to get files in directory and create list with dictionaries (dic per file) with file attributes
# (filename, extension, bytes, full path and md5_hash)
def file_listing():
    files_values = []
    if choice is None:
        print("Directory is not specified")
    else:
        for root, dirs, files in os.walk(choice):
            for name in files:
                hash_md5 = hashlib.md5()
                with open(os.path.join(root, name), "rb") as f:
                    for chunk in iter(lambda: f.read(1024), b""):
                        hash_md5.update(chunk)

                file_values = {
                    "filename": name,
                    "extension": name[name.rfind(".") + 1:],
                    "bytes": os.path.getsize(os.path.join(root, name)),
                    "full_path": os.path.join(root, name),
                    "md5_hash": hash_md5.hexdigest()
                }
                files_values.append(file_values)
    return files_values


def file_filter_by_extension(files_values):
    global FILTER_BY_EXTENSION
    extension = input("Enter file format:\n")
    if len(extension) == 0:
        return False
    extension_dictionary = []
    for i in files_values:
        if i["extension"] == extension:
            extension_dictionary.append(i)
    print()
    FILTER_BY_EXTENSION = True
    return extension_dictionary


# Grouping files by size and return a sorted list with pairs of (bytes, [{full path, md5_hash]}).
# If bytes are the same the pairs are (bytes, [{full path, md5_hash}...{full path, md5_hash}]
def bytes_filter(files_values):
    sorting_type = input('''Size sorting options:
            1. Descending
            2. Ascending\n''')
    print()
    bytes_dictionary = {key["bytes"]: [] for key in files_values}
    sorted_list = []
    for i in files_values:
        bytes_dictionary[i["bytes"]].append({"full_path": i["full_path"], "md5_hash": i["md5_hash"]})

    while True:
        if sorting_type in ["1", "2"]:
            break
        else:
            print("Wrong option\nEnter a sorting option:\n")
            sorting_type = input()
    if sorting_type == "1":
        for i, j in sorted(bytes_dictionary.items(), reverse=True):
            print(f'{i} bytes')
            sorted_list.append([i, j])
            for files in range(len(j)):
                print(j[files]["full_path"])
            print()

    if sorting_type == "2":
        for i, j in sorted(bytes_dictionary.items()):
            sorted_list.append([i, j])
            print(f'{i} bytes')
            for files in range(len(j)):
                print(j[files]["full_path"])
            print()
    return sorted_list


# Checking for duplicates - Constructing a duplicates dicts and a list to print by group if bytes are the same.
# Printed values: Bytes \n Hash \n full path of files with line numbering.
# If the bytes are the same in the next different file pairs we dont print bytes again instead
# we print only hash and full path else we print again a completely new line Bytes \n Hash \n full path

def duplicates_check(files_values):
    duplicates_ask = input('Check for duplicates?\n').lower()
    while True:
        if duplicates_ask in ["yes", "no"]:
            if duplicates_ask == "yes":
                break
            elif duplicates_ask == "no":
                return False
        else:
            print("Wrong option\n")
            duplicates_ask = input()
    duplicates_list = {}

    line_number = 1
    for i in files_values:
        for j in i[1]:
            if (j["md5_hash"], i[0]) not in duplicates_list:
                duplicates_list[tuple((j["md5_hash"], i[0]))] = []
                duplicates_list[(j["md5_hash"], i[0])].append(j["full_path"])
            else:
                duplicates_list[tuple((j["md5_hash"], i[0]))].append(j["full_path"])

    # Constructing a final list to return with numbered duplicate files
    temporary_bytes = []
    final_duplicate_list = {}
    for key, value in duplicates_list.items():
        if len(duplicates_list[(key[0], key[1])]) > 1:
            if key[1] not in temporary_bytes:
                temporary_bytes.append(key[1])
                print()
                print(f'{key[1]} bytes\nHash: {key[0]}')
            else:
                print(f'Hash: {key[0]}')
            for path_value in duplicates_list[(key[0], key[1])]:
                print(f'{line_number}. {path_value}')
                final_duplicate_list[str(line_number)] = path_value
                line_number += 1
    return final_duplicate_list


def delete_duplicates(list_duplicates, working_directory):
    print()
    total_bytes_removed = 0
    duplicates_delete = input('Delete files?\n').lower()
    while True:
        if duplicates_delete in ["yes", "no"]:
            if duplicates_delete == "yes":
                break
            elif duplicates_delete == "no":
                return False
        else:
            print("\nWrong option")
            duplicates_delete = input()
    duplicates_index = input("\nEnter file numbers to delete:\n").strip().split(" ")
    while True:
        if set(duplicates_index).issubset(list_duplicates):
            break
        else:
            print("\nWrong format")
            duplicates_index = input().strip().split(" ")

    for i in duplicates_index:
        for j in range(len(working_directory)):
            if list_duplicates[i] == working_directory[j]["full_path"]:
                total_bytes_removed += working_directory[j]["bytes"]
                os.remove(list_duplicates[i])
    print(f'\nTotal freed up space: {total_bytes_removed} bytes')


def main():
    directory = file_listing()
    extension_filter = file_filter_by_extension(directory)
    if FILTER_BY_EXTENSION:
        bytes_filtering = bytes_filter(extension_filter)
        duplicates = duplicates_check(bytes_filtering)
        delete_duplicates(duplicates, directory)

    else:
        bytes_filtering = bytes_filter(directory)
        duplicates = duplicates_check(bytes_filtering)
        delete_duplicates(duplicates, directory)


if __name__ == main():
    main()
