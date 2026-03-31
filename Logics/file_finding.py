import os
import sys
import string
import ctypes

def get_windows_drives():
    """
    Returns a list of drive roots on Windows (e.g., ["C:\\", "D:\\", ...]).
    """
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def find_file(filename, search_path):
    """
    Recursively search for a file named 'filename' starting at 'search_path'.
    Returns the first matching full file path, or None if not found.
    """
    for root, dirs, files in os.walk(search_path, topdown=True, onerror=lambda e: None):
        if filename in files:
            return os.path.join(root, filename)
    return None

def search(file_name):
    found_path = None

    if sys.platform.startswith("win"):
        drives = get_windows_drives()
        
        # Define common folders inside the current user's profile
        user_profile = os.environ.get("USERPROFILE", "")
        common_user_folders = [
            "Desktop",
            "Documents",
            "Downloads",
            "Pictures",
            "Videos",
            "Music",
            "OneDrive",
            "Favorites",
            "Saved Games",
            "3D Objects"
        ]
        
        # Build absolute paths to common folders that exist
        common_folders = [
            os.path.join(user_profile, folder)
            for folder in common_user_folders
            if os.path.exists(os.path.join(user_profile, folder))
        ]

        # Optionally include Recycle Bin
        recycle_bin = "C:\\$Recycle.Bin"
        if os.path.exists(recycle_bin):
            common_folders.append(recycle_bin)

        for drive in drives:
            if drive.startswith("C:"):
                print(f"Searching for '{file_name}' in common folders on C: ...")
                for folder in common_folders:
                    found_path = find_file(file_name, folder)
                    if found_path:
                        print(f"Found file at: {found_path}")
                        return found_path
            else:
                print(f"Searching for '{file_name}' on drive {drive} ...")
                found_path = find_file(file_name, drive)
                if found_path:
                    print(f"Found file at: {found_path} on drive {drive}")
                    return found_path

    else:
        # For non-Windows systems, search starting at root.
        search_root = "/"
        print(f"Searching for '{file_name}' starting at {search_root} ...")
        found_path = find_file(file_name, search_root)

    if not found_path:
        return f"File '{file_name}' not found on the system."
    return found_path

# Example usage
# result = search("example.txt")
# print(result)
