from keywords.web_keywords import WebKeywords
from utils.data_reader import DataReader
from utils.logger import Logger
import logging
from pathlib import Path

class KeywordExecutor:
    """Executes keyword-driven test cases"""
    
    def __init__(self):
        self.web_keywords = WebKeywords()
        self.data_reader = DataReader()
        self.logger = Logger.setup_logger("KeywordExecutor")
        self.test_results = []
    
    def execute_test_case(self, test_steps):
        """
        Execute a single test case
        Args:
            test_steps (list): List of test steps with keywords and parameters
        Returns:
            bool: True if all steps passed
        """
        test_passed = True
        step_results = []
        
        for i, step in enumerate(test_steps, 1):
            try:
                keyword = step.get('keyword', '').strip()
                parameters = step.get('parameters', {})
                
                self.logger.info(f"Executing Step {i}: {keyword}")
                
                # Execute the keyword
                result = self._execute_keyword(keyword, parameters)
                
                step_results.append({
                    'step': i,
                    'keyword': keyword,
                    'parameters': parameters,
                    'result': 'PASS' if result else 'FAIL'
                })
                
                if not result:
                    test_passed = False
                    self.logger.error(f"Step {i} failed: {keyword}")
                else:
                    self.logger.info(f"Step {i} passed: {keyword}")
                    
            except Exception as e:
                test_passed = False
                step_results.append({
                    'step': i,
                    'keyword': keyword,
                    'parameters': parameters,
                    'result': 'ERROR',
                    'error': str(e)
                })
                self.logger.error(f"Step {i} error: {str(e)}")
        
        return test_passed, step_results
    
    def execute_test_suite_from_excel(self, file_path, sheet_name=None):
        """
        Execute test suite from Excel file
        Args:
            file_path (str): Path to Excel file
            sheet_name (str): Sheet name (optional)
        Returns:
            dict: Test execution results
        """
        try:
            # Read test data from Excel
            test_data = self.data_reader.read_excel(file_path, sheet_name)
            
            if not test_data:
                raise Exception("No test data found in Excel file")
            
            # Group steps by test case
            test_cases = self._group_steps_by_test_case(test_data)
            
            # Execute each test case
            suite_results = []
            
            for test_case_name, steps in test_cases.items():
                self.logger.info(f"Executing test case: {test_case_name}")
                
                test_passed, step_results = self.execute_test_case(steps)
                
                suite_results.append({
                    'test_case': test_case_name,
                    'result': 'PASS' if test_passed else 'FAIL',
                    'steps': step_results
                })
                
                self.logger.info(f"Test case {test_case_name}: {'PASSED' if test_passed else 'FAILED'}")
            
            return {
                'total_tests': len(suite_results),
                'passed_tests': len([r for r in suite_results if r['result'] == 'PASS']),
                'failed_tests': len([r for r in suite_results if r['result'] == 'FAIL']),
                'results': suite_results
            }
            
        except Exception as e:
            self.logger.error(f"Failed to execute test suite: {str(e)}")
            return None
    
    def _group_steps_by_test_case(self, test_data):
        """Group test steps by test case name"""
        test_cases = {}
        
        for row in test_data:
            test_case = row.get('test_case', row.get('TestCase', 'Unknown'))
            keyword = row.get('keyword', row.get('Keyword', ''))
            
            # Extract parameters from the row (excluding test_case and keyword columns)
            parameters = {}
            for key, value in row.items():
                if key.lower() not in ['test_case', 'testcase', 'keyword'] and value:
                    parameters[key] = value
            
            step = {
                'keyword': keyword,
                'parameters': parameters
            }
            
            if test_case not in test_cases:
                test_cases[test_case] = []
            
            test_cases[test_case].append(step)
        
        return test_cases
    
    def _execute_keyword(self, keyword, parameters):
        """
        Execute a specific keyword
        Args:
            keyword (str): Keyword to execute
            parameters (dict): Parameters for the keyword
        Returns:
            bool: True if keyword executed successfully
        """
        keyword_lower = keyword.lower().replace(' ', '_')
        
        try:
            if keyword_lower == 'open_browser':
                browser = parameters.get('browser', 'chrome')
                return self.web_keywords.open_browser(browser)
            
            elif keyword_lower == 'close_browser':
                return self.web_keywords.close_browser()
            
            elif keyword_lower == 'navigate_to_url':
                url = parameters.get('url', '')
                return self.web_keywords.navigate_to_url(url)
            
            elif keyword_lower == 'navigate_to_home_page':
                return self.web_keywords.navigate_to_home_page()
            
            elif keyword_lower == 'navigate_to_login_page':
                return self.web_keywords.navigate_to_login_page()
            
            elif keyword_lower == 'login_with_credentials':
                email = parameters.get('email', '')
                password = parameters.get('password', '')
                remember_me = parameters.get('remember_me', False)
                return self.web_keywords.login_with_credentials(email, password, remember_me)
            
            elif keyword_lower == 'verify_login_success':
                return self.web_keywords.verify_login_success()
            
            elif keyword_lower == 'verify_login_failure':
                return self.web_keywords.verify_login_failure()
            
            elif keyword_lower == 'logout':
                return self.web_keywords.logout()
            
            elif keyword_lower == 'search_product':
                search_term = parameters.get('search_term', '')
                return self.web_keywords.search_product(search_term)
            
            elif keyword_lower == 'click_category':
                category = parameters.get('category', '')
                return self.web_keywords.click_category(category)
            
            elif keyword_lower == 'verify_page_title':
                expected_title = parameters.get('expected_title', '')
                return self.web_keywords.verify_page_title(expected_title)
            
            elif keyword_lower == 'verify_current_url':
                expected_url = parameters.get('expected_url', '')
                return self.web_keywords.verify_current_url(expected_url)
            
            elif keyword_lower == 'take_screenshot':
                filename = parameters.get('filename', 'screenshot.png')
                return self.web_keywords.take_screenshot(filename)
            
            elif keyword_lower == 'wait_for_seconds':
                seconds = int(parameters.get('seconds', 1))
                return self.web_keywords.wait_for_seconds(seconds)
            
            else:
                self.logger.error(f"Unknown keyword: {keyword}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing keyword {keyword}: {str(e)}")
            return False
    
    def generate_test_report(self, results, output_file):
        """
        Generate test execution report
        Args:
            results (dict): Test execution results
            output_file (str): Output file path
        """
        try:
            report_content = []
            report_content.append("TEST EXECUTION REPORT")
            report_content.append("=" * 50)
            report_content.append(f"Total Tests: {results['total_tests']}")
            report_content.append(f"Passed Tests: {results['passed_tests']}")
            report_content.append(f"Failed Tests: {results['failed_tests']}")
            report_content.append(f"Pass Rate: {(results['passed_tests']/results['total_tests']*100):.2f}%")
            report_content.append("\n")
            
            for test_result in results['results']:
                report_content.append(f"Test Case: {test_result['test_case']}")
                report_content.append(f"Result: {test_result['result']}")
                report_content.append("-" * 30)
                
                for step in test_result['steps']:
                    report_content.append(f"  Step {step['step']}: {step['keyword']} - {step['result']}")
                    if 'error' in step:
                        report_content.append(f"    Error: {step['error']}")
                
                report_content.append("\n")
            
            # Write report to file
            with open(output_file, 'w') as f:
                f.write('\n'.join(report_content))
            
            self.logger.info(f"Test report generated: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate test report: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.web_keywords.close_browser()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup error: {str(e)}")