"""
API client utilities for making HTTP requests.
"""

import requests
import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin
from .base_class import BaseClass


class APIClient(BaseClass):
    """
    Base API client for making HTTP requests.
    
    This class provides common functionality for API interactions including
    request/response handling, authentication, retry logic, and error handling.
    """
    
    def __init__(
        self,
        base_url: str = "",
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        config: Optional[Any] = None,
        logger: Optional[Any] = None,
        name: Optional[str] = None
    ):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API requests
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            config: Configuration instance
            logger: Logger instance
            name: Name for this client
        """
        super().__init__(config, logger, name)
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'{self.name}/1.0'
        })
        
        # Add API key to headers if provided
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def initialize(self) -> bool:
        """
        Initialize the API client.
        
        Returns:
            True if initialization was successful
        """
        try:
            # Test connection if base_url is provided
            if self.base_url:
                response = self.session.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    self.log_info("API client initialized successfully")
                    return True
                else:
                    self.log_warning(f"Health check failed with status {response.status_code}")
                    return True  # Still return True as the client is functional
            else:
                self.log_info("API client initialized (no base URL)")
                return True
        except Exception as e:
            self.log_error(f"Failed to initialize API client: {e}")
            return False
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.session:
            self.session.close()
        self.log_info("API client cleanup completed")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (will be joined with base_url)
            data: Request data
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If all retry attempts fail
        """
        url = urljoin(f"{self.base_url}/", endpoint.lstrip('/'))
        
        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        for attempt in range(self.max_retries + 1):
            try:
                self.log_debug(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=request_headers,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Log response
                self.log_debug(f"Response status: {response.status_code}")
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                    self.log_warning(f"Rate limited, waiting {retry_after} seconds")
                    time.sleep(retry_after)
                    continue
                
                # Handle server errors
                if response.status_code >= 500 and attempt < self.max_retries:
                    self.log_warning(f"Server error {response.status_code}, retrying...")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                
                return response
                
            except requests.RequestException as e:
                if attempt < self.max_retries:
                    self.log_warning(f"Request failed (attempt {attempt + 1}): {e}")
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    self.log_error(f"Request failed after {self.max_retries + 1} attempts: {e}")
                    raise
        
        # This should never be reached, but just in case
        raise requests.RequestException("Max retries exceeded")
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._make_request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._make_request('POST', endpoint, data=data, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._make_request('PUT', endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._make_request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make a PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._make_request('PATCH', endpoint, data=data, **kwargs)
    
    def get_json(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Make a GET request and return JSON response.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: If request fails
            ValueError: If response is not valid JSON
        """
        response = self.get(endpoint, params=params, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def post_json(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Make a POST request and return JSON response.
        
        Args:
            endpoint: API endpoint
            data: Request data
            **kwargs: Additional arguments
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.RequestException: If request fails
            ValueError: If response is not valid JSON
        """
        response = self.post(endpoint, data=data, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def set_api_key(self, api_key: str) -> None:
        """
        Set or update the API key.
        
        Args:
            api_key: New API key
        """
        self.api_key = api_key
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        self.log_info("API key updated")
    
    def set_base_url(self, base_url: str) -> None:
        """
        Set or update the base URL.
        
        Args:
            base_url: New base URL
        """
        self.base_url = base_url.rstrip('/')
        self.log_info(f"Base URL updated to: {self.base_url}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the API client.
        
        Returns:
            Dictionary with client status information
        """
        return {
            "base_url": self.base_url,
            "has_api_key": bool(self.api_key),
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        } 