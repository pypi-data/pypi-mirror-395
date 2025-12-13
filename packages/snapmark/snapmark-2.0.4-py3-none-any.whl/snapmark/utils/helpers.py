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

def find_dxf_files(folder_path, recursive=False):
    """Finds all DXF files in a folder."""
    
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if recursive:
        dxf_files = [f for f in folder.rglob("*") if f.suffix.lower() == ".dxf"]
    else:
        dxf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".dxf"]

    print(f"🔧 Found {len(dxf_files)} file to process in {folder_path}")
    return dxf_files
    

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