# Selenium Hybrid Automation Framework

A comprehensive hybrid automation framework built with Python and Selenium WebDriver that combines multiple testing approaches including Page Object Model (POM), Data-Driven Testing (DDT), and Keyword-Driven Testing (KDT).

## 🚀 Features

- **Hybrid Framework**: Combines POM, DDT, and KDT approaches
- **Multi-Browser Support**: Chrome, Firefox, Edge with WebDriver Manager
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Data-Driven Testing**: Support for Excel, CSV, JSON, and YAML data files
- **Keyword-Driven Testing**: Execute tests using keywords from Excel files
- **Comprehensive Reporting**: HTML, JUnit XML, and Allure reports
- **Parallel Execution**: Run tests in parallel for faster execution
- **Screenshot on Failure**: Automatic screenshot capture for failed tests
- **Configurable**: Easy configuration management through INI files
- **Logging**: Comprehensive logging with multiple log levels
- **API Testing**: Built-in API testing capabilities
- **CI/CD Ready**: Easy integration with Jenkins, GitHub Actions, etc.

## 📁 Project Structure

```
selenium-hybrid-framework/
├── config/
│   └── config.ini                 # Configuration settings
├── keywords/
│   ├── __init__.py
│   ├── keyword_executor.py        # Keyword execution engine
│   └── web_keywords.py           # Web automation keywords
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Base page class
│   ├── home_page.py              # Home page object
│   └── login_page.py             # Login page object
├── test_data/
│   ├── keyword_test_data.xlsx    # Keyword test data
│   ├── login_test_data.xlsx      # Login test data
│   └── test_users.json           # Test user data
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures and configuration
│   ├── test_home_page.py         # Home page tests
│   ├── test_keyword_driven.py    # Keyword-driven tests
│   └── test_login.py             # Login tests
├── utils/
│   ├── __init__.py
│   ├── api_helper.py             # API testing utilities
│   ├── base_page.py              # Base page utilities
│   ├── config_reader.py          # Configuration reader
│   ├── data_reader.py            # Data file reader
│   ├── driver_manager.py         # WebDriver manager
│   └── logger.py                 # Logging utilities
├── logs/                         # Log files
├── reports/                      # Test reports
├── screenshots/                  # Screenshot files
├── pytest.ini                   # Pytest configuration
├── requirements.txt              # Python dependencies
├── run_tests.py                  # Main test runner script
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Chrome/Firefox/Edge browser

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd selenium-hybrid-framework
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python run_tests.py --help
   ```

## 🚀 Quick Start

### Running Tests with Pytest

1. **Run all tests:**
   ```bash
   python run_tests.py
   ```

2. **Run smoke tests only:**
   ```bash
   python run_tests.py --markers smoke
   ```

3. **Run tests in Firefox:**
   ```bash
   python run_tests.py --browser firefox
   ```

4. **Run tests in headless mode:**
   ```bash
   python run_tests.py --headless
   ```

5. **Run tests with HTML report:**
   ```bash
   python run_tests.py --html-report
   ```

6. **Run tests in parallel:**
   ```bash
   python run_tests.py --parallel 4
   ```

### Running Keyword-Driven Tests

1. **Run keyword tests from Excel:**
   ```bash
   python run_tests.py --mode keyword --excel-file test_data/keyword_test_data.xlsx
   ```

2. **Run specific sheet from Excel:**
   ```bash
   python run_tests.py --mode keyword --excel-file test_data/login_test_data.xlsx --sheet-name Sheet1
   ```

### Direct Pytest Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run tests with specific marker
pytest -m smoke

# Run tests with HTML report
pytest --html=reports/report.html --self-contained-html

# Run tests in parallel
pytest -n 4

# Run tests with verbose output
pytest -v -s
```

## 📊 Test Data Management

### Excel Files
The framework supports reading test data from Excel files with the following format:

```excel
TestCase          | Keyword              | email              | password  | expected_title
Login_Valid_User  | open_browser        |                    |           |
Login_Valid_User  | navigate_to_login   |                    |           |
Login_Valid_User  | login_with_creds    | test@example.com   | Test123!  |
Login_Valid_User  | verify_login        |                    |           |
```

### JSON Files
Test data can also be stored in JSON format:

```json
{
  "valid_users": [
    {
      "email": "test@example.com",
      "password": "Test123!",
      "role": "customer"
    }
  ]
}
```

## 🔧 Configuration

### Config File (config/config.ini)

```ini
[DEFAULT]
browser = chrome
headless = false
implicit_wait = 10
explicit_wait = 20

[URLS]
base_url = https://demo.nopcommerce.com/

[CREDENTIALS]
admin_username = admin@yourstore.com
admin_password = admin
```

## 📝 Writing Tests

### Page Object Model Example

```python
from pages.login_page import LoginPage
from pages.home_page import HomePage

def test_login(driver):
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    login_page.navigate_to_login_page()
    login_page.login("test@example.com", "password123")
    
    assert home_page.is_user_logged_in()
```

### Keyword-Driven Test Example

```python
from keywords.keyword_executor import KeywordExecutor

def test_keyword_login():
    executor = KeywordExecutor()
    
    test_steps = [
        {'keyword': 'open_browser', 'parameters': {'browser': 'chrome'}},
        {'keyword': 'navigate_to_login_page', 'parameters': {}},
        {'keyword': 'login_with_credentials', 'parameters': {
            'email': 'test@example.com', 'password': 'Test123!'
        }},
        {'keyword': 'verify_login_success', 'parameters': {}},
        {'keyword': 'close_browser', 'parameters': {}}
    ]
    
    test_passed, results = executor.execute_test_case(test_steps)
    assert test_passed
```

## 📊 Reporting

### HTML Reports
Generate beautiful HTML reports with screenshots:
```bash
python run_tests.py --html-report
```

### Allure Reports
Generate interactive Allure reports:
```bash
python run_tests.py --allure
allure serve reports/allure-results
```

### JUnit XML
Generate JUnit XML for CI/CD integration:
```bash
python run_tests.py --junit-xml
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Automated Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python run_tests.py --headless --html-report --junit-xml
        
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: reports/
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python run_tests.py --headless --junit-xml'
            }
        }
    }
    
    post {
        always {
            junit 'reports/*.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: '*.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

## 🐛 Debugging

### Enable Debug Logging
```bash
python run_tests.py --verbose --capture
```

### Screenshot on Failure
Screenshots are automatically captured for failed tests and saved in the `screenshots/` directory.

### Log Files
Check the `logs/` directory for detailed execution logs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in this README
- Review the example test files in the `tests/` directory

## 🎯 Best Practices

1. **Page Object Model**: Keep page elements and actions separate
2. **Data-Driven**: Use external data files for test data
3. **Logging**: Add appropriate logging for debugging
4. **Screenshots**: Take screenshots for important steps
5. **Configuration**: Use configuration files for environment settings
6. **Parallel Execution**: Use parallel execution for faster test runs
7. **CI/CD Integration**: Integrate with your CI/CD pipeline

## 📈 Advanced Features

### API Testing Integration
```python
from utils.api_helper import APIHelper

def test_api_integration():
    api = APIHelper()
    response = api.get('/users/1')
    assert api.validate_status_code(response, 200)
```

### Database Integration
The framework can be extended to include database testing capabilities.

### Custom Keywords
Add your own keywords by extending the `WebKeywords` class:

```python
def custom_keyword(self, parameter):
    """Custom keyword implementation"""
    # Your implementation here
    return True
```

---

**Happy Testing! 🎉**