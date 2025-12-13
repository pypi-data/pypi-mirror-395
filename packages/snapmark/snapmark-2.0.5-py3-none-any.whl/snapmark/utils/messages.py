"""
Centralized message system for SnapMark.

Contains all user-facing messages to maintain consistency and ease translation.
"""


def file_in_use_error(file_name: str) -> str:
    """Message when file is open in another application."""
    return f"🔒 The file '{file_name}' is currently open in another application. Please close it and try again."


def file_not_found_error(file_name: str) -> str:
    """Message when file does not exist."""
    return f"❓ The file or the folder '{file_name}' was not found."


def cannot_open_error(file_name: str, reason: str = None) -> str:
    """Message when file cannot be opened."""
    if reason:
        return f"❌ Cannot open '{file_name}': {reason}"
    return f"❌ Cannot open '{file_name}'."


def cannot_save_error(file_name: str, reason: str = None) -> str:
    """Message when file cannot be saved."""
    if reason:
        return f"❌ Cannot save '{file_name}': {reason}"
    return f"❌ Cannot save '{file_name}'."


def processing_error(file_name: str, reason: str) -> str:
    """Message when error occurs during processing."""
    return f"❌ Error processing '{file_name}': {reason}"


def backup_error(file_name: str, reason: str) -> str:
    """Message when backup operation fails."""
    return f"❌ Backup error on '{file_name}': {reason}"

def invalid_path_error(path: str) -> str:
    """Message when path is neither a file nor a folder."""
    return f"❓ The path '{path}' does not exist."

def not_a_dxf_error(file_name: str) -> str:
    """Message when file is not a DXF."""
    return f"❌ The file '{file_name}' is not a DXF file."

def no_dxf_found_error(folder_path: str) -> str:
    """Message when no DXF files found in folder."""
    return f"❓ No DXF files found in '{folder_path}'."

def dxf_3d_geometry_error(file_name: str) -> str:
    """Message when 3D geometry is detected in the DXF file."""
    return (
        f"❌ 3D GEOMETRY DETECTED in '{file_name}'!\n\n"
        "SnapMark only supports 2D drawings for laser marking.\n"
        "Please flatten your DXF to 2D before processing and ensure all Z coordinates are zero.\n\n"
    )

# Success messages
def backup_created(file_name: str) -> str:
    """Message when backup is created."""
    return f"✓ Backup created: {file_name}"


def file_restored(file_name: str) -> str:
    """Message when file is restored from backup."""
    return f"↻ Restored from backup: {file_name}"


def operation_completed(file_name: str, operation: str = None) -> str:
    """Generic operation completion message."""
    if operation:
        return f"✓ {operation} completed on {file_name}"
    return f"✓ Operation complete on {file_name}"


# Utility function to print with emoji
def print_error(message: str):
    """Prints an error message."""
    print(message)


def print_success(message: str):
    """Prints a success message."""
    print(message)


def print_warning(message: str):
    """Prints a warning message."""
    print(message)