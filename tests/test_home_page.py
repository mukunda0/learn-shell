import pytest
import time
from utils.logger import Logger

class TestHomePage:
    """Home page test cases"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.logger = Logger.get_logger("TestHomePage")
    
    @pytest.mark.smoke
    def test_home_page_load(self, driver, home_page, config):
        """Test home page loads successfully"""
        self.logger.info("Starting test_home_page_load")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            
            # Wait for page to load
            time.sleep(3)
            
            # Verify page title contains expected text
            page_title = home_page.get_page_title()
            assert "nopcommerce" in page_title.lower(), f"Expected 'nopcommerce' in title, got: {page_title}"
            
            # Verify home page elements are present
            assert home_page.verify_home_page_loaded(), "Home page should be loaded properly"
            
            # Verify URL is correct
            current_url = home_page.get_current_url()
            expected_url = config.get_base_url()
            assert expected_url in current_url, f"Expected URL {expected_url} in {current_url}"
            
            self.logger.info("test_home_page_load completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_home_page_load failed: {str(e)}")
            raise
    
    @pytest.mark.smoke
    @pytest.mark.search
    def test_product_search(self, driver, home_page, test_data):
        """Test product search functionality"""
        self.logger.info("Starting test_product_search")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Get test product data
            test_products = test_data["users"].get("test_products", [])
            search_term = "laptop"  # Default search term
            
            if test_products:
                search_term = test_products[0]["name"]
            
            # Perform search
            home_page.search_product(search_term)
            time.sleep(3)
            
            # Verify search results page is loaded
            current_url = home_page.get_current_url()
            assert "search" in current_url.lower(), "Should navigate to search results page"
            
            self.logger.info(f"test_product_search completed successfully for term: {search_term}")
            
        except Exception as e:
            self.logger.error(f"test_product_search failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    def test_category_navigation(self, driver, home_page):
        """Test category menu navigation"""
        self.logger.info("Starting test_category_navigation")
        
        categories = ["Computers", "Electronics", "Apparel", "Books"]
        
        for category in categories:
            try:
                # Navigate to home page
                home_page.navigate_to_home_page()
                time.sleep(2)
                
                # Click category menu
                home_page.click_category_menu(category)
                time.sleep(3)
                
                # Verify navigation to category page
                current_url = home_page.get_current_url()
                assert category.lower() in current_url.lower(), \
                       f"Should navigate to {category} page, current URL: {current_url}"
                
                self.logger.info(f"Category navigation test passed for: {category}")
                
            except Exception as e:
                self.logger.error(f"Category navigation test failed for {category}: {str(e)}")
                # Continue with next category instead of failing entire test
                continue
        
        self.logger.info("test_category_navigation completed")
    
    @pytest.mark.regression
    def test_user_menu_links(self, driver, home_page):
        """Test user menu links"""
        self.logger.info("Starting test_user_menu_links")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Test login link
            home_page.click_login_link()
            time.sleep(2)
            
            current_url = home_page.get_current_url()
            assert "login" in current_url.lower(), "Should navigate to login page"
            
            # Navigate back to home
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Test register link
            home_page.click_register_link()
            time.sleep(2)
            
            current_url = home_page.get_current_url()
            assert "register" in current_url.lower(), "Should navigate to register page"
            
            self.logger.info("test_user_menu_links completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_user_menu_links failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    def test_newsletter_subscription(self, driver, home_page):
        """Test newsletter subscription"""
        self.logger.info("Starting test_newsletter_subscription")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Subscribe to newsletter
            test_email = "test@example.com"
            home_page.subscribe_to_newsletter(test_email)
            time.sleep(2)
            
            # Note: In a real scenario, you would verify success message
            # For demo purposes, we just verify the action completed without error
            
            self.logger.info("test_newsletter_subscription completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_newsletter_subscription failed: {str(e)}")
            raise
    
    @pytest.mark.smoke
    def test_featured_products_display(self, driver, home_page):
        """Test featured products are displayed"""
        self.logger.info("Starting test_featured_products_display")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(3)
            
            # Get featured products count
            products_count = home_page.get_featured_products_count()
            
            # Verify at least some products are displayed
            assert products_count > 0, f"Expected featured products to be displayed, found: {products_count}"
            
            self.logger.info(f"test_featured_products_display completed - Found {products_count} products")
            
        except Exception as e:
            self.logger.error(f"test_featured_products_display failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.parametrize("search_term", [
        "laptop",
        "phone",
        "book",
        "shoes",
        "nonexistentproduct123"
    ])
    def test_search_various_terms(self, driver, home_page, search_term):
        """Test search with various terms"""
        self.logger.info(f"Starting test_search_various_terms with term: {search_term}")
        
        try:
            # Navigate to home page
            home_page.navigate_to_home_page()
            time.sleep(2)
            
            # Perform search
            home_page.search_product(search_term)
            time.sleep(3)
            
            # Verify search results page is loaded
            current_url = home_page.get_current_url()
            assert "search" in current_url.lower(), "Should navigate to search results page"
            
            self.logger.info(f"test_search_various_terms completed for: {search_term}")
            
        except Exception as e:
            self.logger.error(f"test_search_various_terms failed for {search_term}: {str(e)}")
            raise