"""
Configuration management for the project.
"""

import os
import json
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """
    Configuration management class for handling project settings.
    
    This class provides a centralized way to manage configuration settings
    from environment variables, config files, and default values.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Optional path to a JSON configuration file
        """
        self._config: Dict[str, Any] = {}
        self._config_file = config_file
        
        # Load configuration from file if provided
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        # Load from environment variables
        self.load_from_env()
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the JSON configuration file
        """
        try:
            with open(config_file, 'r') as f:
                self._config.update(json.load(f))
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Failed to load config file {config_file}: {e}")
    
    def load_from_env(self) -> None:
        """
        Load configuration from environment variables.
        
        Environment variables should be prefixed with 'APP_' to be loaded.
        """
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                config_key = key[4:].lower()  # Remove 'APP_' prefix and convert to lowercase
                self._config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def save_to_file(self, config_file: Optional[str] = None) -> None:
        """
        Save current configuration to a JSON file.
        
        Args:
            config_file: Path to save the configuration file (uses default if None)
        """
        file_path = config_file or self._config_file
        if not file_path:
            raise ValueError("No config file path specified")
        
        with open(file_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the configuration as a dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to configuration."""
        return self._config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style setting of configuration."""
        self._config[key] = value
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the configuration."""
        return key in self._config 