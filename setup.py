#!/usr/bin/env python3
"""
Setup script for Selenium Hybrid Automation Framework
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "reports",
        "reports/allure-results",
        "screenshots",
        "test_data"
    ]
    
    print("Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("  Required: Python 3.8 or higher")
        return False

def check_browsers():
    """Check if browsers are installed"""
    print("\nChecking browser availability...")
    
    browsers = {
        "Chrome": ["google-chrome", "chrome", "chromium"],
        "Firefox": ["firefox"],
        "Edge": ["microsoft-edge", "edge"]
    }
    
    available_browsers = []
    
    for browser_name, commands in browsers.items():
        for command in commands:
            try:
                subprocess.run([command, "--version"], 
                             capture_output=True, 
                             check=True, 
                             timeout=5)
                print(f"✓ {browser_name} is available")
                available_browsers.append(browser_name)
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        else:
            print(f"✗ {browser_name} not found")
    
    if not available_browsers:
        print("⚠ Warning: No browsers found. Please install Chrome, Firefox, or Edge.")
        return False
    
    return True

def create_sample_test():
    """Create a sample test file for quick verification"""
    sample_test = '''#!/usr/bin/env python3
"""
Sample test to verify framework setup
"""

from utils.driver_manager import DriverManager
from utils.config_reader import ConfigReader
from pages.home_page import HomePage
import time

def test_framework_setup():
    """Simple test to verify framework is working"""
    print("Testing framework setup...")
    
    try:
        # Initialize components
        config = ConfigReader()
        driver_manager = DriverManager()
        
        # Get driver
        driver = driver_manager.get_driver("chrome")
        home_page = HomePage(driver)
        
        # Navigate to home page
        home_page.navigate_to_home_page()
        time.sleep(3)
        
        # Verify page loaded
        title = home_page.get_page_title()
        print(f"Page title: {title}")
        
        # Take screenshot
        driver.save_screenshot("screenshots/setup_test.png")
        print("Screenshot saved: screenshots/setup_test.png")
        
        # Cleanup
        driver_manager.quit_driver()
        
        print("✓ Framework setup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Framework setup test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_framework_setup()
'''
    
    with open("test_setup.py", "w") as f:
        f.write(sample_test)
    
    print("✓ Created sample test file: test_setup.py")

def main():
    """Main setup function"""
    print("🚀 Selenium Hybrid Framework Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Check browsers
    check_browsers()
    
    # Create sample test
    create_sample_test()
    
    print("\n" + "=" * 50)
    
    if success:
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run sample test: python test_setup.py")
        print("2. Run all tests: python run_tests.py")
        print("3. Run smoke tests: python run_tests.py --markers smoke")
        print("4. Generate HTML report: python run_tests.py --html-report")
        print("5. Run in headless mode: python run_tests.py --headless")
        print("\nFor more options: python run_tests.py --help")
    else:
        print("❌ Setup completed with warnings/errors")
        print("Please resolve the issues above before running tests")
    
    print("\n📚 Documentation: README.md")
    print("🔧 Configuration: config/config.ini")
    print("📊 Test Data: test_data/")
    print("📝 Logs: logs/")
    print("📈 Reports: reports/")

if __name__ == "__main__":
    main()