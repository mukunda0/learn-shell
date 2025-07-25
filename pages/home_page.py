from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

class HomePage(BasePage):
    """Home page object model"""
    
    # Locators
    LOGO = (By.CLASS_NAME, "header-logo")
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class, 'search-box-button')]")
    LOGIN_LINK = (By.LINK_TEXT, "Log in")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    MY_ACCOUNT_LINK = (By.LINK_TEXT, "My account")
    WISHLIST_LINK = (By.LINK_TEXT, "Wishlist")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "cart-label")
    CURRENCY_SELECTOR = (By.ID, "customerCurrency")
    MAIN_MENU = (By.CLASS_NAME, "top-menu")
    FEATURED_PRODUCTS = (By.CLASS_NAME, "product-grid")
    NEWSLETTER_EMAIL = (By.ID, "newsletter-email")
    NEWSLETTER_BUTTON = (By.ID, "newsletter-subscribe-button")
    
    # Category menu locators
    COMPUTERS_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Computers')]")
    ELECTRONICS_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Electronics')]")
    APPAREL_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Apparel')]")
    DIGITAL_DOWNLOADS_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Digital downloads')]")
    BOOKS_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Books')]")
    JEWELRY_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Jewelry')]")
    GIFT_CARDS_MENU = (By.XPATH, "//ul[@class='top-menu notmobile']//a[contains(text(),'Gift Cards')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_home_page(self):
        """Navigate to home page"""
        self.navigate_to_base_url()
    
    def search_product(self, search_term):
        """
        Search for a product
        Args:
            search_term (str): Product search term
        """
        self.send_keys(self.SEARCH_BOX, search_term)
        self.click_element(self.SEARCH_BUTTON)
        self.logger.info(f"Searched for product: {search_term}")
    
    def click_login_link(self):
        """Click login link"""
        self.click_element(self.LOGIN_LINK)
        self.logger.info("Clicked login link")
    
    def click_register_link(self):
        """Click register link"""
        self.click_element(self.REGISTER_LINK)
        self.logger.info("Clicked register link")
    
    def click_logout_link(self):
        """Click logout link"""
        self.click_element(self.LOGOUT_LINK)
        self.logger.info("Clicked logout link")
    
    def click_my_account_link(self):
        """Click my account link"""
        self.click_element(self.MY_ACCOUNT_LINK)
        self.logger.info("Clicked my account link")
    
    def click_wishlist_link(self):
        """Click wishlist link"""
        self.click_element(self.WISHLIST_LINK)
        self.logger.info("Clicked wishlist link")
    
    def click_shopping_cart_link(self):
        """Click shopping cart link"""
        self.click_element(self.SHOPPING_CART_LINK)
        self.logger.info("Clicked shopping cart link")
    
    def select_currency(self, currency):
        """
        Select currency from dropdown
        Args:
            currency (str): Currency to select
        """
        self.select_dropdown_by_text(self.CURRENCY_SELECTOR, currency)
        self.logger.info(f"Selected currency: {currency}")
    
    def subscribe_to_newsletter(self, email):
        """
        Subscribe to newsletter
        Args:
            email (str): Email address
        """
        self.send_keys(self.NEWSLETTER_EMAIL, email)
        self.click_element(self.NEWSLETTER_BUTTON)
        self.logger.info(f"Subscribed to newsletter with email: {email}")
    
    def click_category_menu(self, category):
        """
        Click on category menu
        Args:
            category (str): Category name (computers, electronics, etc.)
        """
        category_lower = category.lower()
        
        if category_lower == "computers":
            self.click_element(self.COMPUTERS_MENU)
        elif category_lower == "electronics":
            self.click_element(self.ELECTRONICS_MENU)
        elif category_lower == "apparel":
            self.click_element(self.APPAREL_MENU)
        elif category_lower == "digital downloads":
            self.click_element(self.DIGITAL_DOWNLOADS_MENU)
        elif category_lower == "books":
            self.click_element(self.BOOKS_MENU)
        elif category_lower == "jewelry":
            self.click_element(self.JEWELRY_MENU)
        elif category_lower == "gift cards":
            self.click_element(self.GIFT_CARDS_MENU)
        else:
            raise ValueError(f"Unknown category: {category}")
        
        self.logger.info(f"Clicked category menu: {category}")
    
    def is_user_logged_in(self):
        """
        Check if user is logged in
        Returns:
            bool: True if user is logged in
        """
        return self.is_element_present(self.LOGOUT_LINK)
    
    def is_user_logged_out(self):
        """
        Check if user is logged out
        Returns:
            bool: True if user is logged out
        """
        return self.is_element_present(self.LOGIN_LINK)
    
    def get_featured_products_count(self):
        """
        Get count of featured products
        Returns:
            int: Number of featured products
        """
        try:
            products = self.find_elements((By.CLASS_NAME, "product-item"))
            count = len(products)
            self.logger.info(f"Found {count} featured products")
            return count
        except Exception as e:
            self.logger.error(f"Error getting featured products count: {str(e)}")
            return 0
    
    def verify_home_page_loaded(self):
        """
        Verify home page is loaded
        Returns:
            bool: True if home page is loaded
        """
        return (self.is_element_present(self.LOGO) and 
                self.is_element_present(self.SEARCH_BOX) and
                self.is_element_present(self.MAIN_MENU))