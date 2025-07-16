"""
Base class providing common functionality for project classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .config import Config
from .logger import Logger


class BaseClass(ABC):
    """
    Abstract base class providing common functionality for project classes.
    
    This class provides:
    - Configuration management
    - Logging capabilities
    - Common utility methods
    - Abstract methods for subclasses to implement
    """
    
    def __init__(
        self,
        config: Optional[Config] = None,
        logger: Optional[Logger] = None,
        name: Optional[str] = None
    ):
        """
        Initialize the base class.
        
        Args:
            config: Configuration instance
            logger: Logger instance
            name: Name for this instance
        """
        self.name = name or self.__class__.__name__
        self.config = config or Config()
        self.logger = logger or Logger(name=self.name)
        
        self.logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the class. Must be implemented by subclasses.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Clean up resources. Must be implemented by subclasses.
        """
        pass
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config.set(key, value)
    
    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(f"[{self.name}] {message}")
    
    def log_info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(f"[{self.name}] {message}")
    
    def log_error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_exception(self, message: str) -> None:
        """Log an exception message with traceback."""
        self.logger.exception(f"[{self.name}] {message}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary representation.
        
        Returns:
            Dictionary representation of the object
        """
        return {
            "name": self.name,
            "class": self.__class__.__name__,
            "config": self.config.to_dict()
        }
    
    def __str__(self) -> str:
        """String representation of the object."""
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the object."""
        return f"{self.__class__.__name__}(name='{self.name}', config={self.config})" 