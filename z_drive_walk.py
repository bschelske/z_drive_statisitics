import os
import csv
import time

def get_folder_size(folder_path):
    """
    Get the size of a folder including its subdirectories and files, similar to how Windows calculates folder size.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        int: Total size of the folder in bytes.
    """
    total_size = 0

    for dirpath, _, filenames in os.walk(folder_path):
        try:
            # Get the size of all files in the directory
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                file_info = os.stat(filepath)
                total_size += file_info.st_size

            # Account for directory size (4096 bytes on NTFS, may vary on other file systems)
            total_size += 4096
        except Exception as e:
            print(f"Error accessing directory: {e}")

    return total_size


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


def get_directory_statistics(directory):
    """
    Collects statistics about directories and files within the specified directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list[dict]: A list of dictionaries containing folder statistics.
            Each dictionary has keys: "Path", "Folder Name", "Number of Files",
            "Number of Folders", and "Folder Size (bytes)".
    """
    folder_statistics = []
    total_directories = 0
    total_files = 0
    start_time = time.time()
    for dirpath, dirnames, filenames in os.walk(directory):
        total_directories += 1
        total_files += len(filenames)

        folder_name = os.path.basename(dirpath)
        num_files = len(filenames)
        num_folders = len(dirnames)
        folder_size = get_folder_size(dirpath)  # Assuming you've fixed the get_directory_size function

        folder_statistics.append({
            "Path": dirpath,
            "Folder Name": folder_name,
            "Number of Files": num_files,
            "Number of Folders": num_folders,
            "Folder Size (bytes)": folder_size
        })

        # Display progress
        progress_percent = (total_directories / total_directories) * 100
        elapsed_time = time.time() - start_time
        progress_message = f"Progress: {progress_percent:.2f}% ({total_directories}/{total_directories} directories) - Elapsed Time: {elapsed_time:.2f} seconds"
        print(progress_message.ljust(len(progress_message) + 10), end='\r', flush=True)

    return folder_statistics

# Example usage:
z_drive_path =  r"Z:\\"
# z_drive_path =  r"C:\Users\bensc\PycharmProjects\z_drive_statisitics"
statistics = get_directory_statistics(z_drive_path)

# Define the CSV file path
csv_file_path = "20240524_z_drive_path_statistics.csv"

# Save the statistics to a CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ["Path", "Folder Name", "Number of Files", "Number of Folders", "Folder Size (bytes)"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the statistics for each folder
    for stats in statistics:
        writer.writerow(stats)

print(f"\nStatistics saved to {csv_file_path}")
