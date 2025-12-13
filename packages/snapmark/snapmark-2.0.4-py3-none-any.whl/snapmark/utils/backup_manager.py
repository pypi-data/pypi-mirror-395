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
        
        Args:
            file_path: Path of the file to back up
            force: If True, overwrites an existing backup
            
        Returns:
            True if the backup was created, False if it already existed
        """
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
    def restore_all_in_folder(folder_path: str, delete_backups: bool = False, 
                            recursive: bool = False):
        """
        Restores all .dxf.bak backups in the specified folder.
        
        Args:
            folder_path: Folder containing the backups
            delete_backups: If True, deletes the backups after restoration
            recursive: If True, searches in subfolders as well
        
        Returns:
            dict: Restoration statistics
        """
        from pathlib import Path
        
        restored_count = 0
        not_found_count = 0
        
        if recursive:
            # Search recursively in all subfolders
            backup_files = []
            for ext in [".dxf.bak", ".DXF.bak"]:
                backup_files.extend(Path(folder_path).rglob(f"*{ext}"))
            
            for backup_path in backup_files:
                # Remove .bak to get the original path
                original_path = str(backup_path)[:-len(BackupManager.BACKUP_EXTENSION)]
                
                if BackupManager.restore_backup(original_path, delete_backup=delete_backups):
                    restored_count += 1
        else:
            # Non-recursive mode (as before)
            for filename in os.listdir(folder_path):
                if filename.endswith(f".dxf{BackupManager.BACKUP_EXTENSION}") or \
                   filename.endswith(f".DXF{BackupManager.BACKUP_EXTENSION}"):
                    
                    backup_path = os.path.join(folder_path, filename)
                    original_name = filename[:-len(BackupManager.BACKUP_EXTENSION)]
                    original_path = os.path.join(folder_path, original_name)
                    
                    if BackupManager.restore_backup(original_path, delete_backup=delete_backups):
                        restored_count += 1
                    else:
                        not_found_count += 1
        
        print(f"\n✓ Restored {restored_count} files in {folder_path}")
        
        return {
            'restored': restored_count,
            'not_found': not_found_count,
            'folder': folder_path
        }

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