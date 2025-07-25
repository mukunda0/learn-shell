import requests
import json
import logging
from utils.config_reader import ConfigReader

class APIHelper:
    """Helper class for API testing and integration"""
    
    def __init__(self):
        self.config = ConfigReader()
        self.base_url = self.config.get_api_base_url()
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
    
    def get(self, endpoint, headers=None, params=None):
        """
        Send GET request
        Args:
            endpoint (str): API endpoint
            headers (dict): Request headers
            params (dict): Query parameters
        Returns:
            requests.Response: Response object
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = self.session.get(url, headers=headers, params=params)
            
            self.logger.info(f"GET request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in GET request to {endpoint}: {str(e)}")
            raise
    
    def post(self, endpoint, data=None, json_data=None, headers=None):
        """
        Send POST request
        Args:
            endpoint (str): API endpoint
            data (dict): Form data
            json_data (dict): JSON data
            headers (dict): Request headers
        Returns:
            requests.Response: Response object
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            if json_data:
                response = self.session.post(url, json=json_data, headers=headers)
            else:
                response = self.session.post(url, data=data, headers=headers)
            
            self.logger.info(f"POST request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in POST request to {endpoint}: {str(e)}")
            raise
    
    def put(self, endpoint, data=None, json_data=None, headers=None):
        """
        Send PUT request
        Args:
            endpoint (str): API endpoint
            data (dict): Form data
            json_data (dict): JSON data
            headers (dict): Request headers
        Returns:
            requests.Response: Response object
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            
            if json_data:
                response = self.session.put(url, json=json_data, headers=headers)
            else:
                response = self.session.put(url, data=data, headers=headers)
            
            self.logger.info(f"PUT request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in PUT request to {endpoint}: {str(e)}")
            raise
    
    def delete(self, endpoint, headers=None):
        """
        Send DELETE request
        Args:
            endpoint (str): API endpoint
            headers (dict): Request headers
        Returns:
            requests.Response: Response object
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = self.session.delete(url, headers=headers)
            
            self.logger.info(f"DELETE request to {url} - Status: {response.status_code}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in DELETE request to {endpoint}: {str(e)}")
            raise
    
    def validate_status_code(self, response, expected_status):
        """
        Validate response status code
        Args:
            response (requests.Response): Response object
            expected_status (int): Expected status code
        Returns:
            bool: True if status code matches
        """
        actual_status = response.status_code
        if actual_status == expected_status:
            self.logger.info(f"Status code validation passed: {actual_status}")
            return True
        else:
            self.logger.error(f"Status code validation failed. Expected: {expected_status}, Actual: {actual_status}")
            return False
    
    def validate_response_time(self, response, max_time_ms):
        """
        Validate response time
        Args:
            response (requests.Response): Response object
            max_time_ms (int): Maximum allowed response time in milliseconds
        Returns:
            bool: True if response time is within limit
        """
        response_time_ms = response.elapsed.total_seconds() * 1000
        if response_time_ms <= max_time_ms:
            self.logger.info(f"Response time validation passed: {response_time_ms}ms")
            return True
        else:
            self.logger.error(f"Response time validation failed. Max: {max_time_ms}ms, Actual: {response_time_ms}ms")
            return False
    
    def get_json_response(self, response):
        """
        Get JSON response data
        Args:
            response (requests.Response): Response object
        Returns:
            dict: JSON response data
        """
        try:
            return response.json()
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON response")
            return {}
    
    def validate_json_schema(self, response_data, expected_keys):
        """
        Validate JSON response schema
        Args:
            response_data (dict): Response data
            expected_keys (list): List of expected keys
        Returns:
            bool: True if all expected keys are present
        """
        missing_keys = []
        for key in expected_keys:
            if key not in response_data:
                missing_keys.append(key)
        
        if not missing_keys:
            self.logger.info("JSON schema validation passed")
            return True
        else:
            self.logger.error(f"JSON schema validation failed. Missing keys: {missing_keys}")
            return False
    
    def set_auth_token(self, token):
        """
        Set authorization token for session
        Args:
            token (str): Authorization token
        """
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        self.logger.info("Authorization token set for session")
    
    def clear_auth_token(self):
        """Clear authorization token from session"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
            self.logger.info("Authorization token cleared from session")