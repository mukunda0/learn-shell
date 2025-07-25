import configparser
import os
from pathlib import Path

class ConfigReader:
    """Utility class to read configuration from config.ini file"""
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / "config" / "config.ini"
        if config_path.exists():
            self.config.read(config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    def get_browser(self):
        """Get browser name from config"""
        return self.config.get('DEFAULT', 'browser', fallback='chrome')
    
    def get_headless(self):
        """Get headless mode setting"""
        return self.config.getboolean('DEFAULT', 'headless', fallback=False)
    
    def get_implicit_wait(self):
        """Get implicit wait time"""
        return self.config.getint('DEFAULT', 'implicit_wait', fallback=10)
    
    def get_explicit_wait(self):
        """Get explicit wait time"""
        return self.config.getint('DEFAULT', 'explicit_wait', fallback=20)
    
    def get_page_load_timeout(self):
        """Get page load timeout"""
        return self.config.getint('DEFAULT', 'page_load_timeout', fallback=30)
    
    def get_base_url(self):
        """Get base URL"""
        return self.config.get('URLS', 'base_url', fallback='')
    
    def get_admin_url(self):
        """Get admin URL"""
        return self.config.get('URLS', 'admin_url', fallback='')
    
    def get_api_base_url(self):
        """Get API base URL"""
        return self.config.get('URLS', 'api_base_url', fallback='')
    
    def get_admin_credentials(self):
        """Get admin credentials"""
        username = self.config.get('CREDENTIALS', 'admin_username', fallback='')
        password = self.config.get('CREDENTIALS', 'admin_password', fallback='')
        return username, password
    
    def get_test_user_credentials(self):
        """Get test user credentials"""
        email = self.config.get('CREDENTIALS', 'test_user_email', fallback='')
        password = self.config.get('CREDENTIALS', 'test_user_password', fallback='')
        return email, password
    
    def get_screenshot_on_failure(self):
        """Get screenshot on failure setting"""
        return self.config.getboolean('REPORTING', 'screenshot_on_failure', fallback=True)
    
    def get_allure_results_dir(self):
        """Get allure results directory"""
        return self.config.get('REPORTING', 'allure_results_dir', fallback='reports/allure-results')