import pytest
from keywords.keyword_executor import KeywordExecutor
from utils.logger import Logger
from pathlib import Path

class TestKeywordDriven:
    """Keyword-driven test cases"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.logger = Logger.get_logger("TestKeywordDriven")
        self.keyword_executor = KeywordExecutor()
    
    def teardown_method(self):
        """Teardown method for each test"""
        self.keyword_executor.cleanup()
    
    @pytest.mark.smoke
    def test_execute_login_keywords(self):
        """Test keyword-driven login scenario"""
        self.logger.info("Starting test_execute_login_keywords")
        
        try:
            # Define test steps
            test_steps = [
                {
                    'keyword': 'open_browser',
                    'parameters': {'browser': 'chrome'}
                },
                {
                    'keyword': 'navigate_to_login_page',
                    'parameters': {}
                },
                {
                    'keyword': 'login_with_credentials',
                    'parameters': {
                        'email': 'test@example.com',
                        'password': 'Test123!'
                    }
                },
                {
                    'keyword': 'verify_login_success',
                    'parameters': {}
                },
                {
                    'keyword': 'take_screenshot',
                    'parameters': {'filename': 'screenshots/keyword_login_success.png'}
                },
                {
                    'keyword': 'logout',
                    'parameters': {}
                },
                {
                    'keyword': 'close_browser',
                    'parameters': {}
                }
            ]
            
            # Execute test case
            test_passed, step_results = self.keyword_executor.execute_test_case(test_steps)
            
            # Verify test passed
            assert test_passed, f"Keyword-driven login test should pass. Results: {step_results}"
            
            # Verify all steps passed
            failed_steps = [step for step in step_results if step['result'] != 'PASS']
            assert len(failed_steps) == 0, f"All steps should pass. Failed steps: {failed_steps}"
            
            self.logger.info("test_execute_login_keywords completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_execute_login_keywords failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    def test_execute_search_keywords(self):
        """Test keyword-driven search scenario"""
        self.logger.info("Starting test_execute_search_keywords")
        
        try:
            # Define test steps for search scenario
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
                    'parameters': {'search_term': 'laptop'}
                },
                {
                    'keyword': 'wait_for_seconds',
                    'parameters': {'seconds': 3}
                },
                {
                    'keyword': 'verify_current_url',
                    'parameters': {'expected_url': 'search'}
                },
                {
                    'keyword': 'take_screenshot',
                    'parameters': {'filename': 'screenshots/keyword_search_results.png'}
                },
                {
                    'keyword': 'close_browser',
                    'parameters': {}
                }
            ]
            
            # Execute test case
            test_passed, step_results = self.keyword_executor.execute_test_case(test_steps)
            
            # Verify test passed
            assert test_passed, f"Keyword-driven search test should pass. Results: {step_results}"
            
            self.logger.info("test_execute_search_keywords completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_execute_search_keywords failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    def test_execute_category_navigation_keywords(self):
        """Test keyword-driven category navigation"""
        self.logger.info("Starting test_execute_category_navigation_keywords")
        
        try:
            # Define test steps for category navigation
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
                    'keyword': 'click_category',
                    'parameters': {'category': 'computers'}
                },
                {
                    'keyword': 'wait_for_seconds',
                    'parameters': {'seconds': 3}
                },
                {
                    'keyword': 'verify_current_url',
                    'parameters': {'expected_url': 'computers'}
                },
                {
                    'keyword': 'take_screenshot',
                    'parameters': {'filename': 'screenshots/keyword_computers_category.png'}
                },
                {
                    'keyword': 'close_browser',
                    'parameters': {}
                }
            ]
            
            # Execute test case
            test_passed, step_results = self.keyword_executor.execute_test_case(test_steps)
            
            # Verify test passed
            assert test_passed, f"Keyword-driven category navigation test should pass. Results: {step_results}"
            
            self.logger.info("test_execute_category_navigation_keywords completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_execute_category_navigation_keywords failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    def test_execute_from_excel_file(self):
        """Test executing keyword-driven tests from Excel file"""
        self.logger.info("Starting test_execute_from_excel_file")
        
        try:
            # Check if test data file exists
            excel_file = Path("test_data/keyword_test_data.xlsx")
            if not excel_file.exists():
                pytest.skip("Excel test data file not found")
            
            # Execute test suite from Excel
            results = self.keyword_executor.execute_test_suite_from_excel(str(excel_file))
            
            # Verify results
            assert results is not None, "Test execution results should not be None"
            assert results['total_tests'] > 0, "Should have executed at least one test"
            
            # Generate test report
            report_file = "reports/keyword_test_report.txt"
            self.keyword_executor.generate_test_report(results, report_file)
            
            # Log results summary
            self.logger.info(f"Test execution summary:")
            self.logger.info(f"Total tests: {results['total_tests']}")
            self.logger.info(f"Passed tests: {results['passed_tests']}")
            self.logger.info(f"Failed tests: {results['failed_tests']}")
            
            self.logger.info("test_execute_from_excel_file completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_execute_from_excel_file failed: {str(e)}")
            raise
    
    @pytest.mark.smoke
    def test_invalid_keyword_handling(self):
        """Test handling of invalid keywords"""
        self.logger.info("Starting test_invalid_keyword_handling")
        
        try:
            # Define test steps with invalid keyword
            test_steps = [
                {
                    'keyword': 'open_browser',
                    'parameters': {'browser': 'chrome'}
                },
                {
                    'keyword': 'invalid_keyword_that_does_not_exist',
                    'parameters': {}
                },
                {
                    'keyword': 'close_browser',
                    'parameters': {}
                }
            ]
            
            # Execute test case
            test_passed, step_results = self.keyword_executor.execute_test_case(test_steps)
            
            # Verify test failed due to invalid keyword
            assert not test_passed, "Test should fail due to invalid keyword"
            
            # Verify the invalid keyword step failed
            invalid_step = step_results[1]  # Second step
            assert invalid_step['result'] == 'FAIL', "Invalid keyword step should fail"
            
            self.logger.info("test_invalid_keyword_handling completed successfully")
            
        except Exception as e:
            self.logger.error(f"test_invalid_keyword_handling failed: {str(e)}")
            raise