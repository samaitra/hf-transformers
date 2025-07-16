"""
Unit tests for base classes.
"""

import pytest
import tempfile
import os
from pathlib import Path

# Add src to Python path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.base import Config, Logger, BaseClass, DataProcessor, APIClient


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_initialization(self):
        """Test Config initialization."""
        config = Config()
        assert isinstance(config._config, dict)
        assert config._config_file is None
    
    def test_config_with_file(self):
        """Test Config initialization with file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"test_key": "test_value"}')
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.get("test_key") == "test_value"
        finally:
            os.unlink(temp_file)
    
    def test_config_get_set(self):
        """Test Config get and set methods."""
        config = Config()
        
        # Test setting and getting values
        config.set("key1", "value1")
        config.set("key2", 123)
        config.set("key3", True)
        
        assert config.get("key1") == "value1"
        assert config.get("key2") == 123
        assert config.get("key3") is True
        assert config.get("nonexistent", "default") == "default"
    
    def test_config_dict_access(self):
        """Test Config dictionary-style access."""
        config = Config()
        config["key1"] = "value1"
        
        assert config["key1"] == "value1"
        assert "key1" in config
        assert "nonexistent" not in config
    
    def test_config_to_dict(self):
        """Test Config to_dict method."""
        config = Config()
        config.set("key1", "value1")
        config.set("key2", "value2")
        
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert config_dict["key1"] == "value1"
        assert config_dict["key2"] == "value2"


class TestLogger:
    """Test cases for Logger class."""
    
    def test_logger_initialization(self):
        """Test Logger initialization."""
        logger = Logger()
        assert logger.name == "app"
        assert logger.level == 20  # INFO level
        assert logger.log_file is None
    
    def test_logger_with_file(self):
        """Test Logger initialization with file."""
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as f:
            temp_file = f.name
        
        try:
            logger = Logger(log_file=temp_file)
            assert logger.log_file == temp_file
            assert Path(temp_file).exists()
        finally:
            os.unlink(temp_file)
    
    def test_logger_methods(self):
        """Test Logger logging methods."""
        logger = Logger()
        
        # These should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_logger_set_level(self):
        """Test Logger set_level method."""
        logger = Logger(level=20)  # INFO
        logger.set_level(10)  # DEBUG
        assert logger.level == 10


class TestBaseClass:
    """Test cases for BaseClass."""
    
    def test_base_class_initialization(self):
        """Test BaseClass initialization."""
        # This should raise an error since BaseClass is abstract
        with pytest.raises(TypeError):
            BaseClass()
    
    def test_base_class_inheritance(self):
        """Test BaseClass inheritance."""
        class ConcreteClass(BaseClass):
            def initialize(self):
                return True
            
            def cleanup(self):
                pass
        
        # This should work
        instance = ConcreteClass()
        assert instance.name == "ConcreteClass"
        assert isinstance(instance.config, Config)
        assert isinstance(instance.logger, Logger)
    
    def test_base_class_methods(self):
        """Test BaseClass utility methods."""
        class ConcreteClass(BaseClass):
            def initialize(self):
                return True
            
            def cleanup(self):
                pass
        
        instance = ConcreteClass()
        
        # Test config methods
        instance.set_config("test_key", "test_value")
        assert instance.get_config("test_key") == "test_value"
        
        # Test logging methods (should not raise exceptions)
        instance.log_debug("Debug message")
        instance.log_info("Info message")
        instance.log_warning("Warning message")
        instance.log_error("Error message")
    
    def test_base_class_to_dict(self):
        """Test BaseClass to_dict method."""
        class ConcreteClass(BaseClass):
            def initialize(self):
                return True
            
            def cleanup(self):
                pass
        
        instance = ConcreteClass()
        instance_dict = instance.to_dict()
        
        assert isinstance(instance_dict, dict)
        assert instance_dict["name"] == "ConcreteClass"
        assert instance_dict["class"] == "ConcreteClass"
        assert "config" in instance_dict


class TestDataProcessor:
    """Test cases for DataProcessor class."""
    
    def test_data_processor_initialization(self):
        """Test DataProcessor initialization."""
        processor = DataProcessor()
        assert processor.name == "DataProcessor"
        assert processor.supported_formats == ['json', 'csv', 'txt']
    
    def test_data_processor_initialize_cleanup(self):
        """Test DataProcessor initialize and cleanup methods."""
        processor = DataProcessor()
        
        assert processor.initialize() is True
        processor.cleanup()  # Should not raise exception
    
    def test_data_processor_json_operations(self):
        """Test DataProcessor JSON operations."""
        processor = DataProcessor()
        
        test_data = {"key1": "value1", "key2": 123, "key3": True}
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test write_json
            processor.write_json(test_data, temp_file)
            assert Path(temp_file).exists()
            
            # Test read_json
            loaded_data = processor.read_json(temp_file)
            assert loaded_data == test_data
        finally:
            os.unlink(temp_file)
    
    def test_data_processor_csv_operations(self):
        """Test DataProcessor CSV operations."""
        processor = DataProcessor()
        
        test_data = [
            {"name": "John", "age": "30", "city": "New York"},
            {"name": "Jane", "age": "25", "city": "Los Angeles"}
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test write_csv
            processor.write_csv(test_data, temp_file)
            assert Path(temp_file).exists()
            
            # Test read_csv
            loaded_data = processor.read_csv(temp_file)
            assert len(loaded_data) == 2
            assert loaded_data[0]["name"] == "John"
            assert loaded_data[1]["name"] == "Jane"
        finally:
            os.unlink(temp_file)
    
    def test_data_processor_text_operations(self):
        """Test DataProcessor text operations."""
        processor = DataProcessor()
        
        test_content = "This is a test file content."
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test write_text
            processor.write_text(test_content, temp_file)
            assert Path(temp_file).exists()
            
            # Test read_text
            loaded_content = processor.read_text(temp_file)
            assert loaded_content == test_content
        finally:
            os.unlink(temp_file)
    
    def test_data_processor_validation(self):
        """Test DataProcessor validation methods."""
        processor = DataProcessor()
        
        # Test valid data
        valid_data = {"id": 1, "name": "John", "email": "john@example.com"}
        schema = {"id": int, "name": str, "email": str}
        
        assert processor.validate_data(valid_data, schema) is True
        
        # Test invalid data
        invalid_data = {"id": "not_an_int", "name": "John"}
        assert processor.validate_data(invalid_data, schema) is False
        
        # Test None data
        assert processor.validate_data(None) is False


class TestAPIClient:
    """Test cases for APIClient class."""
    
    def test_api_client_initialization(self):
        """Test APIClient initialization."""
        client = APIClient()
        assert client.base_url == ""
        assert client.api_key is None
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.retry_delay == 1.0
    
    def test_api_client_with_parameters(self):
        """Test APIClient initialization with parameters."""
        client = APIClient(
            base_url="https://api.example.com",
            api_key="test_key",
            timeout=60,
            max_retries=5,
            retry_delay=2.0
        )
        
        assert client.base_url == "https://api.example.com"
        assert client.api_key == "test_key"
        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.retry_delay == 2.0
    
    def test_api_client_initialize_cleanup(self):
        """Test APIClient initialize and cleanup methods."""
        client = APIClient()
        
        # Should return True even without base_url
        assert client.initialize() is True
        client.cleanup()  # Should not raise exception
    
    def test_api_client_setters(self):
        """Test APIClient setter methods."""
        client = APIClient()
        
        # Test set_api_key
        client.set_api_key("new_key")
        assert client.api_key == "new_key"
        
        # Test set_base_url
        client.set_base_url("https://new-api.example.com")
        assert client.base_url == "https://new-api.example.com"
    
    def test_api_client_get_status(self):
        """Test APIClient get_status method."""
        client = APIClient(
            base_url="https://api.example.com",
            api_key="test_key"
        )
        
        status = client.get_status()
        assert isinstance(status, dict)
        assert status["base_url"] == "https://api.example.com"
        assert status["has_api_key"] is True
        assert status["timeout"] == 30
        assert status["max_retries"] == 3 