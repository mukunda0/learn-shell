#!/usr/bin/env python3
"""
Main script to run the hybrid automation framework tests
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from utils.logger import Logger

def run_pytest_tests(args):
    """Run pytest tests with specified arguments"""
    logger = Logger.setup_logger("TestRunner")
    
    # Build pytest command
    pytest_args = ["python", "-m", "pytest"]
    
    # Add test path
    if args.test_path:
        pytest_args.append(args.test_path)
    else:
        pytest_args.append("tests/")
    
    # Add markers
    if args.markers:
        pytest_args.extend(["-m", args.markers])
    
    # Add browser option
    if args.browser:
        pytest_args.extend(["--browser", args.browser])
    
    # Add headless option
    if args.headless:
        pytest_args.append("--headless")
    
    # Add environment option
    if args.environment:
        pytest_args.extend(["--env", args.environment])
    
    # Add parallel execution
    if args.parallel:
        pytest_args.extend(["-n", str(args.parallel)])
    
    # Add HTML report
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/test_report_{timestamp}.html"
        pytest_args.extend(["--html", report_file, "--self-contained-html"])
    
    # Add JUnit XML report
    if args.junit_xml:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        xml_file = f"reports/junit_report_{timestamp}.xml"
        pytest_args.extend(["--junit-xml", xml_file])
    
    # Add Allure report
    if args.allure:
        pytest_args.extend(["--alluredir", "reports/allure-results"])
    
    # Add verbose output
    if args.verbose:
        pytest_args.append("-v")
    
    # Add capture option
    if args.capture:
        pytest_args.append("-s")
    
    # Add reruns for flaky tests
    if args.reruns:
        pytest_args.extend(["--reruns", str(args.reruns)])
    
    logger.info(f"Running command: {' '.join(pytest_args)}")
    
    try:
        # Run pytest
        result = subprocess.run(pytest_args, capture_output=False)
        
        if result.returncode == 0:
            logger.info("All tests passed successfully!")
        else:
            logger.error(f"Some tests failed. Exit code: {result.returncode}")
        
        return result.returncode
        
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return 1

def run_keyword_tests(args):
    """Run keyword-driven tests from Excel file"""
    logger = Logger.setup_logger("KeywordTestRunner")
    
    try:
        from keywords.keyword_executor import KeywordExecutor
        
        executor = KeywordExecutor()
        
        # Check if Excel file exists
        excel_file = Path(args.excel_file)
        if not excel_file.exists():
            logger.error(f"Excel file not found: {excel_file}")
            return 1
        
        logger.info(f"Running keyword-driven tests from: {excel_file}")
        
        # Execute test suite
        results = executor.execute_test_suite_from_excel(str(excel_file), args.sheet_name)
        
        if results:
            # Generate report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"reports/keyword_test_report_{timestamp}.txt"
            executor.generate_test_report(results, report_file)
            
            # Log summary
            logger.info("Test Execution Summary:")
            logger.info(f"Total Tests: {results['total_tests']}")
            logger.info(f"Passed Tests: {results['passed_tests']}")
            logger.info(f"Failed Tests: {results['failed_tests']}")
            logger.info(f"Pass Rate: {(results['passed_tests']/results['total_tests']*100):.2f}%")
            
            # Return appropriate exit code
            return 0 if results['failed_tests'] == 0 else 1
        else:
            logger.error("Failed to execute keyword-driven tests")
            return 1
            
    except Exception as e:
        logger.error(f"Error running keyword tests: {str(e)}")
        return 1
    finally:
        if 'executor' in locals():
            executor.cleanup()

def setup_directories():
    """Create necessary directories"""
    directories = ["logs", "reports", "screenshots", "test_data", "reports/allure-results"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Hybrid Selenium Automation Framework Test Runner")
    
    # Test execution mode
    parser.add_argument("--mode", choices=["pytest", "keyword"], default="pytest",
                       help="Test execution mode (default: pytest)")
    
    # Common arguments
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], default="chrome",
                       help="Browser to run tests on (default: chrome)")
    parser.add_argument("--headless", action="store_true",
                       help="Run tests in headless mode")
    parser.add_argument("--environment", default="demo",
                       help="Environment to run tests against (default: demo)")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose output")
    
    # Pytest specific arguments
    parser.add_argument("--test-path", default="tests/",
                       help="Path to test files (default: tests/)")
    parser.add_argument("--markers",
                       help="Pytest markers to run (e.g., 'smoke', 'regression')")
    parser.add_argument("--parallel", type=int,
                       help="Number of parallel processes for test execution")
    parser.add_argument("--html-report", action="store_true",
                       help="Generate HTML test report")
    parser.add_argument("--junit-xml", action="store_true",
                       help="Generate JUnit XML report")
    parser.add_argument("--allure", action="store_true",
                       help="Generate Allure report data")
    parser.add_argument("--capture", action="store_true",
                       help="Don't capture stdout/stderr")
    parser.add_argument("--reruns", type=int, default=0,
                       help="Number of reruns for failed tests")
    
    # Keyword-driven specific arguments
    parser.add_argument("--excel-file", default="test_data/keyword_test_data.xlsx",
                       help="Excel file for keyword-driven tests")
    parser.add_argument("--sheet-name",
                       help="Sheet name in Excel file")
    
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Run tests based on mode
    if args.mode == "pytest":
        exit_code = run_pytest_tests(args)
    elif args.mode == "keyword":
        exit_code = run_keyword_tests(args)
    else:
        print(f"Unknown mode: {args.mode}")
        exit_code = 1
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()