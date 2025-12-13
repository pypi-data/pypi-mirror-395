"""
Helpers.py - Generic utility functions for SnapMark.

Collects common helper functions used by multiple modules.
"""

from snapmark.checking.checking import find_spec_holes


def count_holes(hole_list):
    """Counts the number of holes in a list."""

    return len(list(hole_list))
    

def get_file_base_name(file_name):
    """Extracts the base name of a file without extension."""
    
    import os
    return os.path.splitext(file_name)[0]


def find_all_circles(doc):
    """Finds all circles in a DXF document."""
    
    msp = doc.modelspace()
    return msp.query('CIRCLE')


from pathlib import Path
from snapmark.utils.messages import file_not_found_error, not_a_dxf_error, no_dxf_found_error

def find_dxf_files(folder_path, recursive=False):
    """Finds all DXF files in a folder or validates a single DXF file."""
    
    path = Path(folder_path)
    
    # 1. Controlla se esiste
    if not path.exists():
        print(file_not_found_error(folder_path))
        return []
    
    # 2. Se è un FILE singolo
    if path.is_file():
        # Controlla se è un DXF
        if path.suffix.lower() != ".dxf":
            print(not_a_dxf_error(path.name))
            return []
        print(f"🔧 Found 1 file to process: {path.name}")
        return [path]
    
    # 3. Se è una CARTELLA
    if recursive:
        dxf_files = [f for f in path.rglob("*") if f.suffix.lower() == ".dxf"]
    else:
        dxf_files = [f for f in path.iterdir() if f.suffix.lower() == ".dxf"]
    
    # 4. Se non trova nessun DXF
    if not dxf_files:
        print(no_dxf_found_error(folder_path))
        return []
    
    print(f"🔧 Found {len(dxf_files)} file(s) to process in {folder_path}")
    return dxf_files


# def find_dxf_files(folder_path, recursive=False):
#     """Finds all DXF files in a folder."""
    
#     folder = Path(folder_path)
#     if not folder.exists():
#         raise FileNotFoundError(f"File or folder not found: {folder_path}")

#     if recursive:
#         dxf_files = [f for f in folder.rglob("*") if f.suffix.lower() == ".dxf"]
#     else:
#         dxf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".dxf"]

#     print(f"🔧 Found {len(dxf_files)} file to process in {folder_path}")
#     return dxf_files
    

# Alias for backward compatibility
def select_files(filtered_files):
    """DEPRECATED: Use file_pattern in process_folder() instead."""

    filtered_files = [f.lower() for f in filtered_files]
    
    def __filter_file(folder, dxf_file):
        return dxf_file.lower() in filtered_files
    
    return lambda folder, dxf_file: __filter_file(folder, dxf_file)



def find_circle_by_radius(min_diam=0, max_diam=float('inf')):
    """Creates a function that finds circles within a specified diameter range."""
    
    return lambda doc: find_spec_holes(doc, min_diam, max_diam)



def is_excluded_layer(entity_layer, excluded_list):
    if excluded_list is None:
        return False  # niente è escluso
    layer = entity_layer.strip().lower()
    excluded = [e.strip().lower() for e in excluded_list]
    return layer in excluded