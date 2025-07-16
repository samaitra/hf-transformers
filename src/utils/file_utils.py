"""
File utility functions and classes.
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Union
from ..base.logger import Logger


class FileUtils:
    """
    Utility class for common file operations.
    
    This class provides methods for file manipulation, validation,
    and common file system operations.
    """
    
    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize the file utilities.
        
        Args:
            logger: Logger instance for logging operations
        """
        self.logger = logger or Logger(name="FileUtils")
    
    def ensure_directory(self, directory_path: Union[str, Path]) -> bool:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            True if directory exists or was created successfully
        """
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Directory ensured: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {directory_path}: {e}")
            return False
    
    def file_exists(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        return Path(file_path).is_file()
    
    def directory_exists(self, directory_path: Union[str, Path]) -> bool:
        """
        Check if a directory exists.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            True if directory exists, False otherwise
        """
        return Path(directory_path).is_dir()
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.stat().st_size
    
    def get_file_extension(self, file_path: Union[str, Path]) -> str:
        """
        Get the file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File extension (including the dot)
        """
        return Path(file_path).suffix
    
    def get_file_name(self, file_path: Union[str, Path]) -> str:
        """
        Get the file name without extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File name without extension
        """
        return Path(file_path).stem
    
    def get_file_name_with_extension(self, file_path: Union[str, Path]) -> str:
        """
        Get the file name with extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File name with extension
        """
        return Path(file_path).name
    
    def list_files(self, directory_path: Union[str, Path], pattern: str = "*") -> List[Path]:
        """
        List files in a directory matching a pattern.
        
        Args:
            directory_path: Path to the directory
            pattern: File pattern to match (e.g., "*.txt", "*.py")
            
        Returns:
            List of matching file paths
        """
        try:
            path = Path(directory_path)
            if not path.is_dir():
                return []
            
            files = list(path.glob(pattern))
            self.logger.debug(f"Found {len(files)} files matching pattern '{pattern}' in {directory_path}")
            return files
        except Exception as e:
            self.logger.error(f"Failed to list files in {directory_path}: {e}")
            return []
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Copy a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if copy was successful
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.is_file():
                self.logger.error(f"Source file does not exist: {source}")
                return False
            
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_path, dest_path)
            self.logger.info(f"Copied file from {source} to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Move a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if move was successful
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.is_file():
                self.logger.error(f"Source file does not exist: {source}")
                return False
            
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source_path), str(dest_path))
            self.logger.info(f"Moved file from {source} to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to move file from {source} to {destination}: {e}")
            return False
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if deletion was successful
        """
        try:
            path = Path(file_path)
            if not path.is_file():
                self.logger.warning(f"File does not exist: {file_path}")
                return True  # Consider it successful if file doesn't exist
            
            path.unlink()
            self.logger.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")
            return False
    
    def calculate_file_hash(self, file_path: Union[str, Path], algorithm: str = "md5") -> str:
        """
        Calculate the hash of a file.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use (md5, sha1, sha256)
            
        Returns:
            File hash as hexadecimal string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If algorithm is not supported
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if algorithm not in ['md5', 'sha1', 'sha256']:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        hash_func = getattr(hashlib, algorithm)()
        
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def get_file_info(self, file_path: Union[str, Path]) -> dict:
        """
        Get comprehensive information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "stem": path.stem,
            "suffix": path.suffix,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "absolute_path": str(path.absolute()),
            "parent": str(path.parent),
            "exists": True
        } 