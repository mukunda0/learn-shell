import pytest
import time
from utils.logger import Logger

class TestLogin:
    """Login test cases"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.logger = Logger.get_logger("TestLogin")
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, driver, login_page, home_page, test_data, config):
        """Test valid user login"""
        self.logger.info("Starting test_valid_login")
        
        try:
            # Get valid user credentials
            valid_users = test_data["users"].get("valid_users", [])
            if not valid_users:
                pytest.skip("No valid user data available")
            
            user = valid_users[0]  # Use first valid user
            
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Perform login
            login_page.login(user["email"], user["password"])
            
            # Wait for login to complete
            time.sleep(3)
            
            # Navigate to home page to verify login
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Verify user is logged in
            assert home_page.is_user_logged_in(), "User should be logged in"
            
            # Logout
            home_page.click_logout_link()
            time.sleep(2)
            
            # Verify user is logged out
            assert home_page.is_user_logged_out(), "User should be logged out"
            
            self.logger.info("test_valid_login completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_valid_login failed: {str(e)}")
            raise
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_invalid_login(self, driver, login_page, test_data):
        """Test invalid user login"""
        self.logger.info("Starting test_invalid_login")
        
        try:
            # Get invalid user credentials
            invalid_users = test_data["users"].get("invalid_users", [])
            if not invalid_users:
                pytest.skip("No invalid user data available")
            
            user = invalid_users[0]  # Use first invalid user
            
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Attempt login with invalid credentials
            login_page.login(user["email"], user["password"])
            
            # Wait for error message
            time.sleep(2)
            
            # Verify error message is displayed
            assert login_page.is_error_message_displayed(), "Error message should be displayed"
            
            error_message = login_page.get_error_message()
            self.logger.info(f"Error message displayed: {error_message}")
            
            # Verify error message contains expected text (if specified)
            if "expected_error" in user:
                assert user["expected_error"].lower() in error_message.lower(), \
                       f"Expected error '{user['expected_error']}' not found in '{error_message}'"
            
            self.logger.info("test_invalid_login completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_invalid_login failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_email_login(self, driver, login_page):
        """Test login with empty email"""
        self.logger.info("Starting test_empty_email_login")
        
        try:
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Attempt login with empty email
            login_page.login("", "password123")
            
            # Wait for validation
            time.sleep(2)
            
            # Verify error message is displayed
            assert login_page.is_error_message_displayed(), "Validation error should be displayed"
            
            self.logger.info("test_empty_email_login completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_empty_email_login failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_password_login(self, driver, login_page):
        """Test login with empty password"""
        self.logger.info("Starting test_empty_password_login")
        
        try:
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Attempt login with empty password
            login_page.login("test@example.com", "")
            
            # Wait for validation
            time.sleep(2)
            
            # Verify error message is displayed
            assert login_page.is_error_message_displayed(), "Validation error should be displayed"
            
            self.logger.info("test_empty_password_login completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_empty_password_login failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_remember_me_functionality(self, driver, login_page, home_page, test_data):
        """Test remember me checkbox functionality"""
        self.logger.info("Starting test_remember_me_functionality")
        
        try:
            # Get valid user credentials
            valid_users = test_data["users"].get("valid_users", [])
            if not valid_users:
                pytest.skip("No valid user data available")
            
            user = valid_users[0]
            
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Login with remember me checked
            login_page.login(user["email"], user["password"], remember_me=True)
            
            # Wait for login
            time.sleep(3)
            
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Verify user is logged in
            assert home_page.is_user_logged_in(), "User should be logged in"
            
            # Note: Full remember me testing would require browser restart
            # which is complex in automated tests
            
            # Logout for cleanup
            home_page.click_logout_link()
            time.sleep(2)
            
            self.logger.info("test_remember_me_functionality completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_remember_me_functionality failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize("email,password,should_fail", [
        ("", "password123", True),
        ("test@example.com", "", True),
        ("invalid@example.com", "wrongpass", True),
        ("notanemail", "password123", True),
    ])
    def test_login_validation_scenarios(self, driver, login_page, email, password, should_fail):
        """Test various login validation scenarios"""
        self.logger.info(f"Starting test_login_validation_scenarios with email: {email}")
        
        try:
            # Navigate to login page
            login_page.navigate_to_login_page()
            
            # Attempt login
            login_page.login(email, password)
            
            # Wait for response
            time.sleep(2)
            
            if should_fail:
                # Verify error message is displayed
                assert login_page.is_error_message_displayed(), \
                       f"Error message should be displayed for email: {email}"
            
            self.logger.info(f"test_login_validation_scenarios completed for email: {email}")
            
        except Exception as e:
            self.logger.error(f"test_login_validation_scenarios failed for email {email}: {str(e)}")
            raise