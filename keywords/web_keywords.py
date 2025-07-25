from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.driver_manager import DriverManager
from utils.data_reader import DataReader
from utils.logger import Logger
import logging
import time

class WebKeywords:
    """Keyword-driven framework for web automation"""
    
    def __init__(self):
        self.driver_manager = DriverManager()
        self.driver = None
        self.home_page = None
        self.login_page = None
        self.data_reader = DataReader()
        self.logger = Logger.setup_logger("WebKeywords")
    
    def open_browser(self, browser="chrome"):
        """
        Open browser
        Args:
            browser (str): Browser name
        """
        try:
            self.driver = self.driver_manager.get_driver(browser)
            self.home_page = HomePage(self.driver)
            self.login_page = LoginPage(self.driver)
            self.logger.info(f"Browser opened: {browser}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open browser: {str(e)}")
            return False
    
    def close_browser(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver_manager.quit_driver()
                self.driver = None
                self.home_page = None
                self.login_page = None
                self.logger.info("Browser closed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close browser: {str(e)}")
            return False
    
    def navigate_to_url(self, url):
        """
        Navigate to URL
        Args:
            url (str): URL to navigate to
        """
        try:
            if not self.driver:
                raise Exception("Browser not opened")
            
            self.driver.get(url)
            self.logger.info(f"Navigated to URL: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to URL {url}: {str(e)}")
            return False
    
    def navigate_to_home_page(self):
        """Navigate to home page"""
        try:
            if not self.home_page:
                raise Exception("Home page not initialized")
            
            self.home_page.navigate_to_home_page()
            self.logger.info("Navigated to home page")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to home page: {str(e)}")
            return False
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        try:
            if not self.login_page:
                raise Exception("Login page not initialized")
            
            self.login_page.navigate_to_login_page()
            self.logger.info("Navigated to login page")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to login page: {str(e)}")
            return False
    
    def login_with_credentials(self, email, password, remember_me=False):
        """
        Login with credentials
        Args:
            email (str): Email address
            password (str): Password
            remember_me (bool): Remember me checkbox
        """
        try:
            if not self.login_page:
                raise Exception("Login page not initialized")
            
            self.login_page.login(email, password, remember_me)
            time.sleep(2)  # Wait for login to complete
            self.logger.info(f"Login attempted with email: {email}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to login: {str(e)}")
            return False
    
    def verify_login_success(self):
        """Verify login success"""
        try:
            if not self.home_page:
                raise Exception("Home page not initialized")
            
            # Navigate to home page first
            self.navigate_to_home_page()
            time.sleep(2)
            
            # Check if user is logged in
            is_logged_in = self.home_page.is_user_logged_in()
            
            if is_logged_in:
                self.logger.info("Login verification passed")
                return True
            else:
                self.logger.error("Login verification failed")
                return False
        except Exception as e:
            self.logger.error(f"Failed to verify login: {str(e)}")
            return False
    
    def verify_login_failure(self):
        """Verify login failure"""
        try:
            if not self.login_page:
                raise Exception("Login page not initialized")
            
            # Check if error message is displayed
            is_error_displayed = self.login_page.is_error_message_displayed()
            
            if is_error_displayed:
                error_message = self.login_page.get_error_message()
                self.logger.info(f"Login failure verification passed. Error: {error_message}")
                return True
            else:
                self.logger.error("Login failure verification failed - no error message")
                return False
        except Exception as e:
            self.logger.error(f"Failed to verify login failure: {str(e)}")
            return False
    
    def logout(self):
        """Logout from application"""
        try:
            if not self.home_page:
                raise Exception("Home page not initialized")
            
            self.home_page.click_logout_link()
            time.sleep(2)
            self.logger.info("Logout completed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to logout: {str(e)}")
            return False
    
    def search_product(self, search_term):
        """
        Search for product
        Args:
            search_term (str): Product search term
        """
        try:
            if not self.home_page:
                raise Exception("Home page not initialized")
            
            self.home_page.search_product(search_term)
            time.sleep(2)
            self.logger.info(f"Product search completed: {search_term}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to search product: {str(e)}")
            return False
    
    def click_category(self, category):
        """
        Click on category menu
        Args:
            category (str): Category name
        """
        try:
            if not self.home_page:
                raise Exception("Home page not initialized")
            
            self.home_page.click_category_menu(category)
            time.sleep(2)
            self.logger.info(f"Clicked category: {category}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click category: {str(e)}")
            return False
    
    def verify_page_title(self, expected_title):
        """
        Verify page title
        Args:
            expected_title (str): Expected page title
        """
        try:
            if not self.driver:
                raise Exception("Browser not opened")
            
            actual_title = self.driver.title
            
            if expected_title.lower() in actual_title.lower():
                self.logger.info(f"Page title verification passed: {actual_title}")
                return True
            else:
                self.logger.error(f"Page title verification failed. Expected: {expected_title}, Actual: {actual_title}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to verify page title: {str(e)}")
            return False
    
    def verify_current_url(self, expected_url):
        """
        Verify current URL
        Args:
            expected_url (str): Expected URL
        """
        try:
            if not self.driver:
                raise Exception("Browser not opened")
            
            actual_url = self.driver.current_url
            
            if expected_url in actual_url:
                self.logger.info(f"URL verification passed: {actual_url}")
                return True
            else:
                self.logger.error(f"URL verification failed. Expected: {expected_url}, Actual: {actual_url}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to verify URL: {str(e)}")
            return False
    
    def take_screenshot(self, filename):
        """
        Take screenshot
        Args:
            filename (str): Screenshot filename
        """
        try:
            if not self.driver:
                raise Exception("Browser not opened")
            
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return False
    
    def wait_for_seconds(self, seconds):
        """
        Wait for specified seconds
        Args:
            seconds (int): Number of seconds to wait
        """
        try:
            time.sleep(seconds)
            self.logger.info(f"Waited for {seconds} seconds")
            return True
        except Exception as e:
            self.logger.error(f"Failed to wait: {str(e)}")
            return False
    
    def read_test_data(self, file_path, test_name=None):
        """
        Read test data from file
        Args:
            file_path (str): Path to test data file
            test_name (str): Specific test name (optional)
        """
        try:
            if test_name:
                data = self.data_reader.get_test_data_by_test_name(file_path, test_name)
            else:
                # Determine file type and read accordingly
                if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    data = self.data_reader.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    data = self.data_reader.read_csv(file_path)
                elif file_path.endswith('.json'):
                    data = self.data_reader.read_json(file_path)
                else:
                    raise ValueError(f"Unsupported file format: {file_path}")
            
            self.logger.info(f"Test data read successfully from: {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to read test data: {str(e)}")
            return None