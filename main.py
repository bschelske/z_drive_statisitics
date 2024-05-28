import os
import csv
import time

# Define the root directory of the Z drive
z_drive_path = r"Z:\\"

# z_drive_path = r'C:\Users\bensc\PycharmProjects\z_drive_statisitics\venv'

# Specify the maximum depth you want to analyze
max_depth = 1


# Function to calculate the size of a directory
# def get_directory_size(directory):
#     total_size = 0
#     current_depth = directory.count(os.sep) - z_drive_path.count(os.sep)
#
#     if current_depth <= max_depth:
#         for dirpath, dirnames, filenames in os.walk(directory):
#             # Skip directories beyond the desired depth
#             if dirpath.count(os.sep) - directory.count(os.sep) > max_depth:
#                 continue
#
#             for filename in filenames:
#                 filepath = os.path.join(dirpath, filename)
#                 total_size += os.path.getsize(filepath)
#     return total_size
#
# def get_directory_size(directory):
#     total_size = 0
#     current_depth = directory.count(os.sep) - z_drive_path.count(os.sep)
#
#     if current_depth <= max_depth:
#         for dirpath, dirnames, filenames in os.walk(directory):
#             # Skip directories beyond the desired depth
#             if dirpath.count(os.sep) - directory.count(os.sep) > max_depth:
#                 continue
#
#             for filename in filenames:
#                 filepath = os.path.join(dirpath, filename)
#                 total_size += os.path.getsize(filepath)
#
#             # Add the size of all files in the current directory
#             # total_size += sum(os.path.getsize(os.path.join(dirpath, filename)) for filename in filenames)
#
#             # Add the size of all subdirectories using recursion
#             total_size += sum(get_directory_size(os.path.join(dirpath, dirname)) for dirname in dirnames)
#
#     return total_size


def get_directory_size(directory, max_depth=10):
    total_size = 0
    current_depth = directory.count(os.sep)

    if current_depth <= max_depth:
        for dirpath, dirnames, filenames in os.walk(directory):
            # Skip directories beyond the desired depth
            if dirpath.count(os.sep) - directory.count(os.sep) > max_depth:
                continue

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)

            # Add the size of all subdirectories using recursion
            total_size += sum(get_directory_size(os.path.join(dirpath, dirname), max_depth) for dirname in dirnames)

    return total_size

# Initialize variables to store statistics
folder_statistics = []

# Track progress
total_directories = 0
total_files = 0
processed_directories = 0
processed_files = 0

# Calculate total directories and files
for dirpath, dirnames, filenames in os.walk(z_drive_path):
    total_directories += 1
    total_files += len(filenames)

# Start time
start_time = time.time()

# Iterate through each directory in the Z drive
for dirpath, dirnames, filenames in os.walk(z_drive_path):
    folder_name = os.path.basename(dirpath)
    num_files = len(filenames)
    num_folders = len(dirnames)
    folder_size = get_directory_size(dirpath)
    # Append statistics to the list
    folder_statistics.append({
        "Path": dirpath,
        "Folder Name": folder_name,
        "Number of Files": num_files,
        "Number of Folders": num_folders,
        "Folder Size (bytes)": folder_size
    })

    processed_directories += 1
    processed_files += num_files

    # Calculate and display progress with padding
    progress_percent = (processed_directories / total_directories) * 100
    elapsed_time = time.time() - start_time
    progress_message = f"Progress: {progress_percent:.2f}% ({processed_directories}/{total_directories} directories) - Elapsed Time: {elapsed_time:.2f} seconds"
    print(progress_message.ljust(len(progress_message) + 10), end='\r', flush=True)

# Define the CSV file path
csv_file_path = "20240524_z_drive_path_statistics.csv"

# Save the statistics to a CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ["Path", "Folder Name", "Number of Files", "Number of Folders", "Folder Size (bytes)"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the statistics for each folder
    for stats in folder_statistics:
        writer.writerow(stats)

print(f"\nStatistics saved to {csv_file_path}")
