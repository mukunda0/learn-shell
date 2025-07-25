from utils.base_page import BasePage as BasePageUtils
from utils.config_reader import ConfigReader
import logging

class BasePage(BasePageUtils):
    """Base page class for Page Object Model"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigReader()
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_url(self, url):
        """
        Navigate to specific URL
        Args:
            url (str): URL to navigate to
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to URL {url}: {str(e)}")
            raise
    
    def navigate_to_base_url(self):
        """Navigate to base URL from config"""
        base_url = self.config.get_base_url()
        self.navigate_to_url(base_url)
    
    def wait_for_page_load(self, timeout=30):
        """
        Wait for page to load completely
        Args:
            timeout (int): Timeout in seconds
        """
        try:
            self.driver.execute_script("return document.readyState") == "complete"
            self.logger.info("Page loaded successfully")
        except Exception as e:
            self.logger.error(f"Page load timeout: {str(e)}")
            raise
    
    def verify_page_title(self, expected_title):
        """
        Verify page title
        Args:
            expected_title (str): Expected page title
        Returns:
            bool: True if title matches
        """
        actual_title = self.get_page_title()
        if expected_title.lower() in actual_title.lower():
            self.logger.info(f"Page title verification passed: {actual_title}")
            return True
        else:
            self.logger.error(f"Page title verification failed. Expected: {expected_title}, Actual: {actual_title}")
            return False
    
    def verify_current_url(self, expected_url):
        """
        Verify current URL
        Args:
            expected_url (str): Expected URL
        Returns:
            bool: True if URL matches
        """
        actual_url = self.get_current_url()
        if expected_url in actual_url:
            self.logger.info(f"URL verification passed: {actual_url}")
            return True
        else:
            self.logger.error(f"URL verification failed. Expected: {expected_url}, Actual: {actual_url}")
            return False