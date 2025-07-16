"""
String utility functions and classes.
"""

import re
import unicodedata
from typing import List, Optional, Dict, Any


class StringUtils:
    """
    Utility class for common string operations.
    
    This class provides methods for string manipulation, validation,
    formatting, and text processing.
    """
    
    @staticmethod
    def is_empty(value: Optional[str]) -> bool:
        """
        Check if a string is empty or None.
        
        Args:
            value: String to check
            
        Returns:
            True if string is None, empty, or contains only whitespace
        """
        return value is None or value.strip() == ""
    
    @staticmethod
    def is_not_empty(value: Optional[str]) -> bool:
        """
        Check if a string is not empty.
        
        Args:
            value: String to check
            
        Returns:
            True if string is not None and contains non-whitespace characters
        """
        return not StringUtils.is_empty(value)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in a string.
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        if not text:
            return ""
        
        # Replace multiple whitespace characters with single space
        normalized = re.sub(r'\s+', ' ', text)
        return normalized.strip()
    
    @staticmethod
    def remove_special_characters(text: str, keep_spaces: bool = True) -> str:
        """
        Remove special characters from a string.
        
        Args:
            text: Input text
            keep_spaces: Whether to keep spaces
            
        Returns:
            Text with special characters removed
        """
        if not text:
            return ""
        
        if keep_spaces:
            # Keep alphanumeric characters and spaces
            pattern = r'[^a-zA-Z0-9\s]'
        else:
            # Keep only alphanumeric characters
            pattern = r'[^a-zA-Z0-9]'
        
        return re.sub(pattern, '', text)
    
    @staticmethod
    def slugify(text: str, separator: str = "-") -> str:
        """
        Convert text to a URL-friendly slug.
        
        Args:
            text: Input text
            separator: Character to use as word separator
            
        Returns:
            URL-friendly slug
        """
        if not text:
            return ""
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)
        
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^\w\s-]', '', text.lower())
        
        # Replace spaces and hyphens with separator
        text = re.sub(r'[-\s]+', separator, text)
        
        # Remove leading/trailing separators
        return text.strip(separator)
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to a maximum length.
        
        Args:
            text: Input text
            max_length: Maximum length
            suffix: Suffix to add if text is truncated
            
        Returns:
            Truncated text
        """
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """
        Capitalize the first letter of each word.
        
        Args:
            text: Input text
            
        Returns:
            Text with capitalized words
        """
        if not text:
            return ""
        
        return text.title()
    
    @staticmethod
    def reverse_words(text: str) -> str:
        """
        Reverse the order of words in a string.
        
        Args:
            text: Input text
            
        Returns:
            Text with reversed word order
        """
        if not text:
            return ""
        
        words = text.split()
        return " ".join(reversed(words))
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        Count the number of words in a string.
        
        Args:
            text: Input text
            
        Returns:
            Number of words
        """
        if not text:
            return 0
        
        # Split on whitespace and filter out empty strings
        words = [word for word in text.split() if word.strip()]
        return len(words)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from text.
        
        Args:
            text: Input text
            
        Returns:
            List of email addresses found
        """
        if not text:
            return []
        
        # Basic email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text.
        
        Args:
            text: Input text
            
        Returns:
            List of URLs found
        """
        if not text:
            return []
        
        # Basic URL regex pattern
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def is_palindrome(text: str, case_sensitive: bool = False) -> bool:
        """
        Check if a string is a palindrome.
        
        Args:
            text: Input text
            case_sensitive: Whether to consider case
            
        Returns:
            True if text is a palindrome
        """
        if not text:
            return True
        
        # Remove non-alphanumeric characters
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text)
        
        if not case_sensitive:
            cleaned = cleaned.lower()
        
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def format_template(template: str, **kwargs) -> str:
        """
        Format a template string with keyword arguments.
        
        Args:
            template: Template string with placeholders like {name}
            **kwargs: Values to substitute
            
        Returns:
            Formatted string
            
        Raises:
            KeyError: If a placeholder is not provided
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise KeyError(f"Missing template variable: {e}")
    
    @staticmethod
    def split_safe(text: str, delimiter: str = ",", max_split: Optional[int] = None) -> List[str]:
        """
        Safely split a string with optional maximum splits.
        
        Args:
            text: Input text
            delimiter: Delimiter to split on
            max_split: Maximum number of splits
            
        Returns:
            List of split parts
        """
        if not text:
            return []
        
        if max_split is not None:
            parts = text.split(delimiter, max_split)
        else:
            parts = text.split(delimiter)
        
        # Strip whitespace from each part
        return [part.strip() for part in parts if part.strip()]
    
    @staticmethod
    def join_safe(parts: List[str], delimiter: str = " ") -> str:
        """
        Safely join a list of strings.
        
        Args:
            parts: List of strings to join
            delimiter: Delimiter to use between parts
            
        Returns:
            Joined string
        """
        if not parts:
            return ""
        
        # Filter out None and empty strings
        valid_parts = [str(part).strip() for part in parts if part and str(part).strip()]
        return delimiter.join(valid_parts) 