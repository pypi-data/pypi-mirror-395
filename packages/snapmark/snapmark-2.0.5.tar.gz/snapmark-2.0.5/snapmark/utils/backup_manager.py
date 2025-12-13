"""
Backup management system for DXF files.
The backup is created as .dxf.bak and is automatically restored before each modification.
"""
import os
import shutil
from pathlib import Path


class BackupManager:
    """Manages backup and restore of DXF files."""
    
    BACKUP_EXTENSION = ".bak"
    
    @staticmethod
    def get_backup_path(file_path: str) -> str:
        """Returns the path of the backup file."""
        return file_path + BackupManager.BACKUP_EXTENSION
    
    @staticmethod
    def create_backup(file_path: str, force: bool = False) -> bool:
        """
        Creates a backup of the original file (only if it does not already exist).
        Works only with DXF files.
        
        Args:
            file_path: Path of the file to back up
            force: If True, overwrites an existing backup
            
        Returns:
            True if the backup was created, False if it already existed
        """
        # Control if it's a DXF file
        if not file_path.lower().endswith('.dxf'):
            print(f"⚠ Backup skipped: '{os.path.basename(file_path)}' is not a DXF file.")
            return False
    
        backup_path = BackupManager.get_backup_path(file_path)
        
        # If the backup already exists and we are not forcing, do nothing
        if os.path.exists(backup_path) and not force:
            return False
        
        # Create the backup
        shutil.copy2(file_path, backup_path)
        print(f"✓ Backup created: {os.path.basename(backup_path)}")
        return True
    
    @staticmethod
    def restore_backup(file_path: str, delete_backup: bool = False) -> bool:
        """
        Restores the file from the backup.
        
        Args:
            file_path: Path of the file to restore
            delete_backup: If True, deletes the backup after restoration
            
        Returns:
            True if restored successfully, False if backup does not exist
            
        Raises:
            PermissionError: If file is open in another application
        """
        backup_path = BackupManager.get_backup_path(file_path)
        
        if not os.path.exists(backup_path):
            print(f"⚠ No backup found for: {os.path.basename(file_path)}")
            return False
        
        # Delete the current file if it exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except PermissionError:
                # FIX: removed reference to undefined variable 'e'
                raise PermissionError(
                    f"Cannot restore '{file_path}' because it is open in another application."
                )
        
        # Restore from the backup
        if delete_backup:
            shutil.move(backup_path, file_path)
            print(f"↻ Restored and backup deleted: {os.path.basename(file_path)}")
        else:
            shutil.copy2(backup_path, file_path)
        
        return True
    


    @staticmethod
    def restore_all_in_folder(file_or_folder: str, delete_backups: bool = False, 
                            recursive: bool = False):
        """
        Restores DXF files from backups. Works with a single file or a folder.
        
        Args:
            file_or_folder: Path to a file or folder
            delete_backups: If True, deletes the backups after restoration
            recursive: If True, searches subfolders (only relevant for folders)
        
        Returns:
            dict: Restoration statistics
        """
        restored_count = 0
        not_found_count = 0

        path_obj = Path(file_or_folder)

        if path_obj.is_file():
            # Single file
            if BackupManager.restore_backup(str(path_obj), delete_backup=delete_backups):
                restored_count += 1
            else:
                not_found_count += 1
        elif path_obj.is_dir():
            # Folder
            if recursive:
                backup_files = list(path_obj.rglob("*.dxf.bak")) + list(path_obj.rglob("*.DXF.bak"))
            else:
                backup_files = [p for p in path_obj.iterdir() if p.suffix.lower() == ".bak" and p.stem.lower().endswith(".dxf")]

            for backup_path in backup_files:
                original_path = str(backup_path)[:-len(BackupManager.BACKUP_EXTENSION)]
                if BackupManager.restore_backup(original_path, delete_backup=delete_backups):
                    restored_count += 1
                else:
                    not_found_count += 1
        else:
            print(f"⚠ File or folder not found: {file_or_folder}")
            return {'restored': 0, 'not_found': 1, 'folder': str(file_or_folder)}

        print(f"\n✓ Restored {restored_count} files in {file_or_folder}")
        return {'restored': restored_count, 'not_found': not_found_count, 'folder': str(file_or_folder)}


    @staticmethod
    def has_backup(file_path: str) -> bool:
        """Checks if a backup exists for the file."""
        return os.path.exists(BackupManager.get_backup_path(file_path))
    
    @staticmethod
    def ensure_original(file_path: str):
        """
        Ensures that the file is in its original version.
        If a backup exists, it restores from that (overwriting changes).
        Otherwise, it creates a backup of the current file.
        
        This method should be called BEFORE any modification operation.
        
        Raises:
            PermissionError: If file is open in another application
        """
        backup_path = BackupManager.get_backup_path(file_path)
        
        if os.path.exists(backup_path):
            # A backup already exists: restore from it (it is the original)
            BackupManager.restore_backup(file_path, delete_backup=False)
        else:
            # No backup exists: create a backup of the current file (it is the original)
            BackupManager.create_backup(file_path, force=False)