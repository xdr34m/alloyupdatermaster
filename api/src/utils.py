import os,re
from pathlib import Path

def get_all_files_in_matching_dirs(base_dir: str, folder_name: str) -> list:
    """
    Recursively finds all files inside directories that match `folder_name` within `base_dir`.
    
    Args:
        base_dir (str): The root directory where folders are located.
        folder_name (str): The name of the folder to match.

    Returns:
        list: A list of absolute file paths found inside the matched directories.
    """
    base_path = Path(base_dir)
    matched_dirs = [d for d in base_path.iterdir() if d.is_dir() and d.name == folder_name]
    
    file_paths = []

    for matched_dir in matched_dirs:
        # Recursively find all files inside the matched directory tree
        file_paths.extend([str(f.resolve()) for f in matched_dir.rglob("*") if f.is_file()])

    return file_paths

def match_regex_from_file(file: str, my_str: str) -> bool:
    try:
        with open(file, 'r') as f:
            regex_pattern = f.readline().strip()  # Read the first line and remove any trailing newline
        
        match_result = bool(re.match(regex_pattern, my_str))  # Match the string with the regex pattern
        return match_result
    except Exception as e:
        print(f"Error opening file {file}: {e}")
        return False

def 


if __name__=="__main__":
    # Example Usage
    base_directory = "/path/to/search"
    folder_to_match = "example_folder"

    result = get_all_files_in_matching_dirs(base_directory, folder_to_match)
    print(result)  # List of all found file paths