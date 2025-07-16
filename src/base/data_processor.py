"""
Data processing utilities and base classes.
"""

import json
import csv
from typing import Any, Dict, List, Optional, Union, Iterator
from pathlib import Path
from .base_class import BaseClass


class DataProcessor(BaseClass):
    """
    Base class for data processing operations.
    
    This class provides common functionality for reading, writing,
    and transforming various data formats.
    """
    
    def __init__(
        self,
        config: Optional[Any] = None,
        logger: Optional[Any] = None,
        name: Optional[str] = None
    ):
        """
        Initialize the data processor.
        
        Args:
            config: Configuration instance
            logger: Logger instance
            name: Name for this processor
        """
        super().__init__(config, logger, name)
        self.supported_formats = ['json', 'csv', 'txt']
    
    def initialize(self) -> bool:
        """
        Initialize the data processor.
        
        Returns:
            True if initialization was successful
        """
        self.log_info("Data processor initialized successfully")
        return True
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.log_info("Data processor cleanup completed")
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Read data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dictionary containing the JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_info(f"Successfully read JSON file: {file_path}")
            return data
        except FileNotFoundError:
            self.log_error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in file {file_path}: {e}")
            raise
    
    def write_json(self, data: Dict[str, Any], file_path: str, indent: int = 2) -> None:
        """
        Write data to a JSON file.
        
        Args:
            data: Data to write
            file_path: Path to the output file
            indent: JSON indentation level
        """
        try:
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            self.log_info(f"Successfully wrote JSON file: {file_path}")
        except Exception as e:
            self.log_error(f"Failed to write JSON file {file_path}: {e}")
            raise
    
    def read_csv(self, file_path: str, delimiter: str = ',') -> List[Dict[str, str]]:
        """
        Read data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            delimiter: CSV delimiter character
            
        Returns:
            List of dictionaries, where each dictionary represents a row
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for row in reader:
                    data.append(row)
            self.log_info(f"Successfully read CSV file: {file_path}")
            return data
        except FileNotFoundError:
            self.log_error(f"File not found: {file_path}")
            raise
    
    def write_csv(self, data: List[Dict[str, Any]], file_path: str, delimiter: str = ',') -> None:
        """
        Write data to a CSV file.
        
        Args:
            data: List of dictionaries to write
            file_path: Path to the output file
            delimiter: CSV delimiter character
        """
        try:
            if not data:
                self.log_warning("No data to write to CSV")
                return
            
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            fieldnames = data[0].keys()
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            self.log_info(f"Successfully wrote CSV file: {file_path}")
        except Exception as e:
            self.log_error(f"Failed to write CSV file {file_path}: {e}")
            raise
    
    def read_text(self, file_path: str) -> str:
        """
        Read text from a file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Content of the text file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.log_info(f"Successfully read text file: {file_path}")
            return content
        except FileNotFoundError:
            self.log_error(f"File not found: {file_path}")
            raise
    
    def write_text(self, content: str, file_path: str) -> None:
        """
        Write text to a file.
        
        Args:
            content: Text content to write
            file_path: Path to the output file
        """
        try:
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log_info(f"Successfully wrote text file: {file_path}")
        except Exception as e:
            self.log_error(f"Failed to write text file {file_path}: {e}")
            raise
    
    def transform_data(self, data: Any, transformation_type: str) -> Any:
        """
        Apply a transformation to data.
        
        Args:
            data: Data to transform
            transformation_type: Type of transformation to apply
            
        Returns:
            Transformed data
        """
        self.log_info(f"Applying transformation: {transformation_type}")
        
        if transformation_type == "uppercase" and isinstance(data, str):
            return data.upper()
        elif transformation_type == "lowercase" and isinstance(data, str):
            return data.lower()
        elif transformation_type == "reverse" and isinstance(data, str):
            return data[::-1]
        else:
            self.log_warning(f"Unknown transformation type: {transformation_type}")
            return data
    
    def validate_data(self, data: Any, schema: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate data against a schema or basic rules.
        
        Args:
            data: Data to validate
            schema: Optional schema for validation
            
        Returns:
            True if data is valid, False otherwise
        """
        if data is None:
            self.log_warning("Data is None")
            return False
        
        if schema:
            # Basic schema validation
            if isinstance(schema, dict) and isinstance(data, dict):
                for key, expected_type in schema.items():
                    if key not in data:
                        self.log_warning(f"Missing required key: {key}")
                        return False
                    if not isinstance(data[key], expected_type):
                        self.log_warning(f"Invalid type for key {key}")
                        return False
        
        self.log_info("Data validation passed")
        return True 