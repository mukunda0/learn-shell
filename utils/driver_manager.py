from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.config_reader import ConfigReader
import logging

class DriverManager:
    """Manages WebDriver instances with different browsers and configurations"""
    
    def __init__(self):
        self.config = ConfigReader()
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def get_driver(self, browser=None):
        """
        Initialize and return WebDriver instance
        Args:
            browser (str): Browser name (chrome, firefox, edge)
        Returns:
            WebDriver: Selenium WebDriver instance
        """
        if browser is None:
            browser = self.config.get_browser()
        
        browser = browser.lower()
        
        try:
            if browser == 'chrome':
                self.driver = self._get_chrome_driver()
            elif browser == 'firefox':
                self.driver = self._get_firefox_driver()
            elif browser == 'edge':
                self.driver = self._get_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Set timeouts
            self.driver.implicitly_wait(self.config.get_implicit_wait())
            self.driver.set_page_load_timeout(self.config.get_page_load_timeout())
            
            # Maximize window
            self.driver.maximize_window()
            
            self.logger.info(f"WebDriver initialized successfully for {browser}")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver for {browser}: {str(e)}")
            raise
    
    def _get_chrome_driver(self):
        """Initialize Chrome WebDriver"""
        options = ChromeOptions()
        
        if self.config.get_headless():
            options.add_argument('--headless')
        
        # Additional Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _get_firefox_driver(self):
        """Initialize Firefox WebDriver"""
        options = FirefoxOptions()
        
        if self.config.get_headless():
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _get_edge_driver(self):
        """Initialize Edge WebDriver"""
        options = EdgeOptions()
        
        if self.config.get_headless():
            options.add_argument('--headless')
        
        # Additional Edge options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def quit_driver(self):
        """Quit the WebDriver instance"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit successfully")
            except Exception as e:
                self.logger.error(f"Error while quitting WebDriver: {str(e)}")
            finally:
                self.driver = None