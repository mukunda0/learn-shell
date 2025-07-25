from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.config_reader import ConfigReader
import logging
import time

class BasePage:
    """Base page class containing common web element operations"""
    
    def __init__(self, driver):
        self.driver = driver
        self.config = ConfigReader()
        self.wait = WebDriverWait(driver, self.config.get_explicit_wait())
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator):
        """
        Find element with explicit wait
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        Returns:
            WebElement: Found element
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        """
        Find multiple elements
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        Returns:
            list: List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []
    
    def click_element(self, locator):
        """
        Click on element with explicit wait
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
    
    def send_keys(self, locator, text):
        """
        Send keys to element
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to send
        """
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys '{text}' to element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to send keys to element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator):
        """
        Get text from element
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        Returns:
            str: Element text
        """
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.info(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def get_attribute(self, locator, attribute):
        """
        Get attribute value from element
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            attribute (str): Attribute name
        Returns:
            str: Attribute value
        """
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            self.logger.info(f"Got attribute '{attribute}' value '{value}' from element: {locator}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get attribute from element {locator}: {str(e)}")
            raise
    
    def is_element_present(self, locator):
        """
        Check if element is present
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        Returns:
            bool: True if element is present
        """
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_visible(self, locator):
        """
        Check if element is visible
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        Returns:
            bool: True if element is visible
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def wait_for_element_to_be_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout
        Returns:
            WebElement: Clickable element
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait
        
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable within timeout: {locator}")
            raise
    
    def select_dropdown_by_text(self, locator, text):
        """
        Select dropdown option by visible text
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Visible text to select
        """
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            self.logger.info(f"Selected dropdown option '{text}' for element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to select dropdown option for element {locator}: {str(e)}")
            raise
    
    def select_dropdown_by_value(self, locator, value):
        """
        Select dropdown option by value
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            value (str): Value to select
        """
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            self.logger.info(f"Selected dropdown value '{value}' for element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to select dropdown value for element {locator}: {str(e)}")
            raise
    
    def hover_over_element(self, locator):
        """
        Hover over element
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        try:
            element = self.find_element(locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element {locator}: {str(e)}")
            raise
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def switch_to_frame(self, locator):
        """
        Switch to frame
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        try:
            frame = self.find_element(locator)
            self.driver.switch_to.frame(frame)
            self.logger.info(f"Switched to frame: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to switch to frame {locator}: {str(e)}")
            raise
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.error(f"Failed to switch to default content: {str(e)}")
            raise
    
    def take_screenshot(self, filename):
        """
        Take screenshot
        Args:
            filename (str): Screenshot filename
        """
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")
    
    def navigate_back(self):
        """Navigate back"""
        self.driver.back()
        self.logger.info("Navigated back")
    
    def navigate_forward(self):
        """Navigate forward"""
        self.driver.forward()
        self.logger.info("Navigated forward")