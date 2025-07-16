#!/usr/bin/env python3
"""
Main application entry point.

This file demonstrates the usage of the base classes and utilities
created for the Python project.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.base import Config, Logger, BaseClass, DataProcessor, APIClient
from src.utils import FileUtils, StringUtils, DateUtils


class ExampleApp(BaseClass):
    """
    Example application demonstrating the usage of base classes.
    """
    
    def __init__(self):
        """Initialize the example application."""
        super().__init__(name="ExampleApp")
        self.data_processor = DataProcessor(name="ExampleDataProcessor")
        self.file_utils = FileUtils(self.logger)
        self.string_utils = StringUtils()
        self.date_utils = DateUtils()
    
    def initialize(self) -> bool:
        """
        Initialize the application.
        
        Returns:
            True if initialization was successful
        """
        self.log_info("Initializing ExampleApp...")
        
        # Initialize data processor
        if not self.data_processor.initialize():
            self.log_error("Failed to initialize data processor")
            return False
        
        self.log_info("ExampleApp initialized successfully")
        return True
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self.log_info("Cleaning up ExampleApp...")
        self.data_processor.cleanup()
        self.log_info("ExampleApp cleanup completed")
    
    def run_examples(self) -> None:
        """Run example demonstrations of the base classes."""
        self.log_info("Running examples...")
        
        # Configuration example
        self._example_config()
        
        # String utilities example
        self._example_string_utils()
        
        # Date utilities example
        self._example_date_utils()
        
        # File utilities example
        self._example_file_utils()
        
        # Data processing example
        self._example_data_processing()
        
        self.log_info("Examples completed successfully")
    
    def _example_config(self) -> None:
        """Demonstrate configuration management."""
        self.log_info("=== Configuration Example ===")
        
        # Set some configuration values
        self.set_config("app_name", "ExampleApp")
        self.set_config("version", "1.0.0")
        self.set_config("debug", True)
        
        # Get configuration values
        app_name = self.get_config("app_name", "Unknown")
        version = self.get_config("version", "0.0.0")
        debug = self.get_config("debug", False)
        
        self.log_info(f"App Name: {app_name}")
        self.log_info(f"Version: {version}")
        self.log_info(f"Debug Mode: {debug}")
        
        # Save configuration to file
        config_data = self.config.to_dict()
        self.data_processor.write_json(config_data, "config_example.json")
    
    def _example_string_utils(self) -> None:
        """Demonstrate string utilities."""
        self.log_info("=== String Utilities Example ===")
        
        sample_text = "  Hello, World! This is a test string.  "
        
        # Normalize whitespace
        normalized = self.string_utils.normalize_whitespace(sample_text)
        self.log_info(f"Normalized: '{normalized}'")
        
        # Create slug
        slug = self.string_utils.slugify(sample_text)
        self.log_info(f"Slug: '{slug}'")
        
        # Truncate text
        truncated = self.string_utils.truncate(sample_text, 20)
        self.log_info(f"Truncated: '{truncated}'")
        
        # Count words
        word_count = self.string_utils.count_words(sample_text)
        self.log_info(f"Word count: {word_count}")
        
        # Check palindrome
        palindrome_text = "racecar"
        is_palindrome = self.string_utils.is_palindrome(palindrome_text)
        self.log_info(f"'{palindrome_text}' is palindrome: {is_palindrome}")
    
    def _example_date_utils(self) -> None:
        """Demonstrate date utilities."""
        self.log_info("=== Date Utilities Example ===")
        
        # Current date and time
        now = self.date_utils.now()
        today = self.date_utils.today()
        
        self.log_info(f"Current datetime: {self.date_utils.format_datetime(now)}")
        self.log_info(f"Current date: {self.date_utils.format_date(today)}")
        
        # Add days
        tomorrow = self.date_utils.add_days(today, 1)
        self.log_info(f"Tomorrow: {self.date_utils.format_date(tomorrow)}")
        
        # Check if weekend
        is_weekend = self.date_utils.is_weekend(today)
        self.log_info(f"Today is weekend: {is_weekend}")
        
        # Week start and end
        week_start = self.date_utils.get_week_start(today)
        week_end = self.date_utils.get_week_end(today)
        self.log_info(f"Week start: {self.date_utils.format_date(week_start)}")
        self.log_info(f"Week end: {self.date_utils.format_date(week_end)}")
    
    def _example_file_utils(self) -> None:
        """Demonstrate file utilities."""
        self.log_info("=== File Utilities Example ===")
        
        # Create a test file
        test_file = "test_example.txt"
        test_content = "This is a test file for demonstration purposes."
        
        # Write test file
        self.data_processor.write_text(test_content, test_file)
        
        # Check if file exists
        exists = self.file_utils.file_exists(test_file)
        self.log_info(f"Test file exists: {exists}")
        
        if exists:
            # Get file info
            file_info = self.file_utils.get_file_info(test_file)
            self.log_info(f"File info: {file_info}")
            
            # Calculate file hash
            file_hash = self.file_utils.calculate_file_hash(test_file, "md5")
            self.log_info(f"File MD5 hash: {file_hash}")
        
        # Clean up test file
        self.file_utils.delete_file(test_file)
    
    def _example_data_processing(self) -> None:
        """Demonstrate data processing."""
        self.log_info("=== Data Processing Example ===")
        
        # Create sample data
        sample_data = {
            "users": [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
                {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
            ],
            "metadata": {
                "total_users": 3,
                "created_at": self.date_utils.format_datetime(self.date_utils.now())
            }
        }
        
        # Write JSON data
        self.data_processor.write_json(sample_data, "users_example.json")
        self.log_info("Wrote sample JSON data")
        
        # Read JSON data
        loaded_data = self.data_processor.read_json("users_example.json")
        self.log_info(f"Loaded {len(loaded_data['users'])} users from JSON")
        
        # Create CSV data
        csv_data = sample_data["users"]
        self.data_processor.write_csv(csv_data, "users_example.csv")
        self.log_info("Wrote sample CSV data")
        
        # Read CSV data
        loaded_csv = self.data_processor.read_csv("users_example.csv")
        self.log_info(f"Loaded {len(loaded_csv)} users from CSV")
        
        # Validate data
        schema = {"id": int, "name": str, "email": str}
        for user in loaded_csv:
            is_valid = self.data_processor.validate_data(user, schema)
            self.log_info(f"User {user.get('name', 'Unknown')} is valid: {is_valid}")


def main():
    """Main function to run the example application."""
    try:
        # Create and initialize the application
        app = ExampleApp()
        
        if not app.initialize():
            print("Failed to initialize application")
            return 1
        
        # Run examples
        app.run_examples()
        
        # Cleanup
        app.cleanup()
        
        print("Application completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Application failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 