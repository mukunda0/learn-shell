from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class LoginPage(BasePage):
    """Login page object model"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    REMEMBER_ME_CHECKBOX = (By.ID, "RememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot your password?")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    ERROR_MESSAGE = (By.CLASS_NAME, "message-error")
    VALIDATION_SUMMARY = (By.CLASS_NAME, "validation-summary-errors")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        base_url = self.config.get_base_url()
        login_url = f"{base_url}/login"
        self.navigate_to_url(login_url)
    
    def enter_email(self, email):
        """
        Enter email address
        Args:
            email (str): Email address
        """
        self.send_keys(self.EMAIL_INPUT, email)
        self.logger.info(f"Entered email: {email}")
    
    def enter_password(self, password):
        """
        Enter password
        Args:
            password (str): Password
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        self.logger.info("Password entered")
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        if not self.is_element_selected(self.REMEMBER_ME_CHECKBOX):
            self.click_element(self.REMEMBER_ME_CHECKBOX)
            self.logger.info("Checked remember me checkbox")
    
    def click_forgot_password_link(self):
        """Click forgot password link"""
        self.click_element(self.FORGOT_PASSWORD_LINK)
        self.logger.info("Clicked forgot password link")
    
    def click_register_link(self):
        """Click register link"""
        self.click_element(self.REGISTER_LINK)
        self.logger.info("Clicked register link")
    
    def get_error_message(self):
        """
        Get error message text
        Returns:
            str: Error message
        """
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        elif self.is_element_present(self.VALIDATION_SUMMARY):
            return self.get_text(self.VALIDATION_SUMMARY)
        return ""
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed
        Returns:
            bool: True if error message is displayed
        """
        return (self.is_element_present(self.ERROR_MESSAGE) or 
                self.is_element_present(self.VALIDATION_SUMMARY))
    
    def login(self, email, password, remember_me=False):
        """
        Perform login action
        Args:
            email (str): Email address
            password (str): Password
            remember_me (bool): Check remember me checkbox
        """
        self.enter_email(email)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login_button()
        self.logger.info(f"Login attempt completed for email: {email}")
    
    def is_element_selected(self, locator):
        """
        Check if element is selected (for checkboxes/radio buttons)
        Args:
            locator (tuple): Element locator
        Returns:
            bool: True if element is selected
        """
        try:
            element = self.find_element(locator)
            return element.is_selected()
        except Exception:
            return False