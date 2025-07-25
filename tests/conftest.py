import pytest
import os
from datetime import datetime
from pathlib import Path
from utils.driver_manager import DriverManager
from utils.logger import Logger
from utils.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def setup_logger():
    """Setup logger for test session"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger = Logger.setup_logger("TestFramework", f"logs/test_execution_{timestamp}.log")
    return logger

@pytest.fixture(scope="function")
def driver(setup_logger):
    """Setup and teardown WebDriver for each test"""
    driver_manager = DriverManager()
    driver = None
    
    try:
        config = ConfigReader()
        browser = config.get_browser()
        driver = driver_manager.get_driver(browser)
        setup_logger.info(f"WebDriver initialized for test: {browser}")
        yield driver
    finally:
        if driver:
            driver_manager.quit_driver()
            setup_logger.info("WebDriver quit after test")

@pytest.fixture(scope="function")
def home_page(driver):
    """Initialize HomePage object"""
    return HomePage(driver)

@pytest.fixture(scope="function")
def login_page(driver):
    """Initialize LoginPage object"""
    return LoginPage(driver)

@pytest.fixture(scope="session")
def config():
    """Get configuration reader"""
    return ConfigReader()

@pytest.fixture(scope="function")
def test_data():
    """Load test data"""
    from utils.data_reader import DataReader
    data_reader = DataReader()
    
    # Load test users
    test_users_file = Path("test_data/test_users.json")
    if test_users_file.exists():
        test_users = data_reader.read_json(test_users_file)
    else:
        test_users = {}
    
    return {
        "users": test_users
    }

@pytest.fixture(autouse=True)
def setup_test_environment(setup_logger):
    """Setup test environment before each test"""
    # Create necessary directories
    directories = ["logs", "reports", "screenshots", "test_data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    setup_logger.info("Test environment setup completed")

def pytest_configure(config):
    """Configure pytest"""
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Set custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login test")
    config.addinivalue_line("markers", "search: mark test as search test")

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Selenium Hybrid Framework Test Report"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Extend pytest report with screenshot on failure"""
    outcome = yield
    report = outcome.get_result()
    
    # Only add screenshot for failed tests during the call phase
    if report.when == "call" and report.failed:
        # Get the driver from the test function
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshots/failed_{item.name}_{timestamp}.png"
            
            try:
                driver.save_screenshot(screenshot_name)
                # Add screenshot to HTML report
                if hasattr(report, "extra"):
                    report.extra.append(pytest_html.extras.image(screenshot_name))
            except Exception as e:
                print(f"Failed to take screenshot: {str(e)}")

# Pytest command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default="demo",
        help="Environment to run tests against"
    )

@pytest.fixture(scope="session")
def browser(request):
    """Get browser from command line"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def headless(request):
    """Get headless mode from command line"""
    return request.config.getoption("--headless")

@pytest.fixture(scope="session")
def environment(request):
    """Get environment from command line"""
    return request.config.getoption("--env")