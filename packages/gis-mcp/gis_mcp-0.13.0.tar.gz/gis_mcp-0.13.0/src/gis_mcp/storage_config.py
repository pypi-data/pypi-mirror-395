"""
Storage configuration for GIS MCP Server.

This module manages the storage path for file operations, allowing users
to specify a custom folder or use a default location.
"""

import os
from pathlib import Path
from typing import Optional

# Global storage path - will be initialized on server startup
_storage_path: Optional[Path] = None


def get_default_storage_path() -> Path:
    """
    Get the default storage path: ~/.gis_mcp/data/
    
    Returns:
        Path object pointing to the default storage directory
    """
    home = Path.home()
    default_path = home / ".gis_mcp" / "data"
    return default_path


def initialize_storage(storage_config: Optional[str] = None) -> Path:
    """
    Initialize the storage configuration.
    
    If storage_config is provided, use that path. Otherwise, use the default.
    Creates the directory if it doesn't exist.
    
    Args:
        storage_config: Optional path to the storage folder. If None, uses default.
        
    Returns:
        Path object pointing to the storage directory
    """
    global _storage_path
    
    if storage_config:
        storage_path = Path(storage_config).expanduser().resolve()
    else:
        storage_path = get_default_storage_path()
    
    # Create directory if it doesn't exist
    storage_path.mkdir(parents=True, exist_ok=True)
    
    _storage_path = storage_path
    return storage_path


def get_storage_path() -> Path:
    """
    Get the current storage path.
    
    If not initialized, initializes with default path.
    
    Returns:
        Path object pointing to the storage directory
    """
    global _storage_path
    
    if _storage_path is None:
        _storage_path = initialize_storage()
    
    return _storage_path


def resolve_path(file_path: str, relative_to_storage: bool = True) -> Path:
    """
    Resolve a file path, optionally making it relative to the storage directory.
    
    If the path is absolute, it's used as-is. If relative and relative_to_storage
    is True, it's resolved relative to the storage directory.
    
    Args:
        file_path: The file path to resolve
        relative_to_storage: If True and path is relative, resolve relative to storage
        
    Returns:
        Resolved Path object
    """
    path = Path(file_path)
    
    # If absolute path, use as-is
    if path.is_absolute():
        return path.expanduser().resolve()
    
    # If relative and we should use storage, resolve relative to storage
    if relative_to_storage:
        storage = get_storage_path()
        return (storage / path).resolve()
    
    # Otherwise, resolve relative to current working directory
    return path.expanduser().resolve()

