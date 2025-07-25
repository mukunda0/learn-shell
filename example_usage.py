#!/usr/bin/env python3
"""
Example usage script demonstrating the Selenium Hybrid Framework capabilities
"""

from utils.driver_manager import DriverManager
from utils.config_reader import ConfigReader
from utils.data_reader import DataReader
from utils.logger import Logger
from pages.home_page import HomePage
from pages.login_page import LoginPage
from keywords.keyword_executor import KeywordExecutor
from keywords.web_keywords import WebKeywords
import time

def example_page_object_model():
    """Example demonstrating Page Object Model usage"""
    print("\n" + "="*50)
    print("EXAMPLE: Page Object Model")
    print("="*50)
    
    logger = Logger.setup_logger("POM_Example")
    driver_manager = DriverManager()
    
    try:
        # Initialize driver
        driver = driver_manager.get_driver("chrome")
        
        # Initialize page objects
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        
        # Navigate to home page
        home_page.navigate_to_home_page()
        logger.info("Navigated to home page")
        
        # Verify home page loaded
        if home_page.verify_home_page_loaded():
            logger.info("Home page loaded successfully")
        
        # Search for a product
        home_page.search_product("laptop")
        logger.info("Searched for laptop")
        time.sleep(3)
        
        # Navigate to login page
        login_page.navigate_to_login_page()
        logger.info("Navigated to login page")
        
        # Attempt login (will fail with demo credentials)
        login_page.login("demo@example.com", "demopass")
        time.sleep(2)
        
        if login_page.is_error_message_displayed():
            error_msg = login_page.get_error_message()
            logger.info(f"Login failed as expected: {error_msg}")
        
        logger.info("Page Object Model example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Page Object Model example: {str(e)}")
    finally:
        driver_manager.quit_driver()

def example_data_driven_testing():
    """Example demonstrating Data-Driven Testing"""
    print("\n" + "="*50)
    print("EXAMPLE: Data-Driven Testing")
    print("="*50)
    
    logger = Logger.setup_logger("DDT_Example")
    data_reader = DataReader()
    
    try:
        # Read test data from JSON file
        test_data = data_reader.read_json("test_data/test_users.json")
        
        if test_data:
            logger.info("Successfully loaded test data from JSON")
            
            # Display valid users
            valid_users = test_data.get("valid_users", [])
            logger.info(f"Found {len(valid_users)} valid users")
            
            for i, user in enumerate(valid_users, 1):
                logger.info(f"User {i}: {user['email']} - Role: {user['role']}")
            
            # Display invalid users
            invalid_users = test_data.get("invalid_users", [])
            logger.info(f"Found {len(invalid_users)} invalid users for negative testing")
            
            # Display test products
            test_products = test_data.get("test_products", [])
            logger.info(f"Found {len(test_products)} test products")
            
            for product in test_products:
                logger.info(f"Product: {product['name']} - Category: {product['category']}")
        
        logger.info("Data-Driven Testing example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Data-Driven Testing example: {str(e)}")

def example_keyword_driven_testing():
    """Example demonstrating Keyword-Driven Testing"""
    print("\n" + "="*50)
    print("EXAMPLE: Keyword-Driven Testing")
    print("="*50)
    
    logger = Logger.setup_logger("KDT_Example")
    keyword_executor = KeywordExecutor()
    
    try:
        # Define test steps using keywords
        test_steps = [
            {
                'keyword': 'open_browser',
                'parameters': {'browser': 'chrome'}
            },
            {
                'keyword': 'navigate_to_home_page',
                'parameters': {}
            },
            {
                'keyword': 'verify_page_title',
                'parameters': {'expected_title': 'nopCommerce demo store'}
            },
            {
                'keyword': 'search_product',
                'parameters': {'search_term': 'computer'}
            },
            {
                'keyword': 'wait_for_seconds',
                'parameters': {'seconds': 3}
            },
            {
                'keyword': 'take_screenshot',
                'parameters': {'filename': 'screenshots/keyword_example.png'}
            },
            {
                'keyword': 'click_category',
                'parameters': {'category': 'electronics'}
            },
            {
                'keyword': 'wait_for_seconds',
                'parameters': {'seconds': 2}
            },
            {
                'keyword': 'close_browser',
                'parameters': {}
            }
        ]
        
        logger.info("Executing keyword-driven test case")
        
        # Execute the test case
        test_passed, step_results = keyword_executor.execute_test_case(test_steps)
        
        # Display results
        logger.info(f"Test Result: {'PASSED' if test_passed else 'FAILED'}")
        
        for step_result in step_results:
            status = step_result['result']
            keyword = step_result['keyword']
            logger.info(f"Step {step_result['step']}: {keyword} - {status}")
        
        logger.info("Keyword-Driven Testing example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Keyword-Driven Testing example: {str(e)}")
    finally:
        keyword_executor.cleanup()

def example_configuration_management():
    """Example demonstrating Configuration Management"""
    print("\n" + "="*50)
    print("EXAMPLE: Configuration Management")
    print("="*50)
    
    logger = Logger.setup_logger("Config_Example")
    
    try:
        config = ConfigReader()
        
        # Display configuration settings
        logger.info("Current Configuration Settings:")
        logger.info(f"Browser: {config.get_browser()}")
        logger.info(f"Headless Mode: {config.get_headless()}")
        logger.info(f"Implicit Wait: {config.get_implicit_wait()} seconds")
        logger.info(f"Explicit Wait: {config.get_explicit_wait()} seconds")
        logger.info(f"Base URL: {config.get_base_url()}")
        logger.info(f"Admin URL: {config.get_admin_url()}")
        logger.info(f"API Base URL: {config.get_api_base_url()}")
        
        # Display credentials (masked for security)
        admin_user, admin_pass = config.get_admin_credentials()
        logger.info(f"Admin Username: {admin_user}")
        logger.info(f"Admin Password: {'*' * len(admin_pass)}")
        
        test_email, test_pass = config.get_test_user_credentials()
        logger.info(f"Test User Email: {test_email}")
        logger.info(f"Test User Password: {'*' * len(test_pass)}")
        
        logger.info("Configuration Management example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Configuration Management example: {str(e)}")

def example_web_keywords():
    """Example demonstrating Web Keywords usage"""
    print("\n" + "="*50)
    print("EXAMPLE: Web Keywords Usage")
    print("="*50)
    
    logger = Logger.setup_logger("WebKeywords_Example")
    web_keywords = WebKeywords()
    
    try:
        # Open browser
        if web_keywords.open_browser("chrome"):
            logger.info("Browser opened successfully")
        
        # Navigate to home page
        if web_keywords.navigate_to_home_page():
            logger.info("Navigated to home page")
        
        # Verify page title
        if web_keywords.verify_page_title("nopCommerce"):
            logger.info("Page title verification passed")
        
        # Search for product
        if web_keywords.search_product("laptop"):
            logger.info("Product search completed")
        
        # Wait for results
        web_keywords.wait_for_seconds(3)
        
        # Take screenshot
        if web_keywords.take_screenshot("screenshots/web_keywords_example.png"):
            logger.info("Screenshot captured")
        
        # Navigate to login page
        if web_keywords.navigate_to_login_page():
            logger.info("Navigated to login page")
        
        # Attempt login (will fail)
        if web_keywords.login_with_credentials("demo@example.com", "demopass"):
            logger.info("Login attempt completed")
        
        # Verify login failure
        if web_keywords.verify_login_failure():
            logger.info("Login failure verified as expected")
        
        logger.info("Web Keywords example completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Web Keywords example: {str(e)}")
    finally:
        web_keywords.close_browser()

def main():
    """Main function to run all examples"""
    print("🚀 Selenium Hybrid Framework - Example Usage")
    print("=" * 60)
    
    # Create necessary directories
    from pathlib import Path
    directories = ["logs", "screenshots", "reports", "test_data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    try:
        # Run all examples
        example_configuration_management()
        example_data_driven_testing()
        example_web_keywords()
        example_keyword_driven_testing()
        example_page_object_model()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("📁 Check the following directories for outputs:")
        print("   - logs/ : Log files")
        print("   - screenshots/ : Screenshot files")
        print("   - reports/ : Test reports")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")

if __name__ == "__main__":
    main()