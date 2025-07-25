import pandas as pd
import openpyxl
import json
import yaml
from pathlib import Path
import logging

class DataReader:
    """Utility class to read test data from various file formats"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def read_excel(self, file_path, sheet_name=None):
        """
        Read data from Excel file
        Args:
            file_path (str): Path to Excel file
            sheet_name (str): Sheet name (optional)
        Returns:
            list: List of dictionaries containing test data
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Excel file not found: {file_path}")
            
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            # Convert DataFrame to list of dictionaries
            data = df.to_dict('records')
            
            # Replace NaN values with empty strings
            for row in data:
                for key, value in row.items():
                    if pd.isna(value):
                        row[key] = ""
            
            self.logger.info(f"Successfully read {len(data)} rows from Excel file: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error reading Excel file {file_path}: {str(e)}")
            raise
    
    def read_csv(self, file_path):
        """
        Read data from CSV file
        Args:
            file_path (str): Path to CSV file
        Returns:
            list: List of dictionaries containing test data
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to list of dictionaries
            data = df.to_dict('records')
            
            # Replace NaN values with empty strings
            for row in data:
                for key, value in row.items():
                    if pd.isna(value):
                        row[key] = ""
            
            self.logger.info(f"Successfully read {len(data)} rows from CSV file: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            raise
    
    def read_json(self, file_path):
        """
        Read data from JSON file
        Args:
            file_path (str): Path to JSON file
        Returns:
            dict/list: JSON data
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.logger.info(f"Successfully read JSON file: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise
    
    def read_yaml(self, file_path):
        """
        Read data from YAML file
        Args:
            file_path (str): Path to YAML file
        Returns:
            dict/list: YAML data
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"YAML file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            self.logger.info(f"Successfully read YAML file: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error reading YAML file {file_path}: {str(e)}")
            raise
    
    def get_test_data_by_test_name(self, file_path, test_name, sheet_name=None):
        """
        Get specific test data by test name
        Args:
            file_path (str): Path to data file
            test_name (str): Test case name
            sheet_name (str): Sheet name for Excel files
        Returns:
            dict: Test data for specific test case
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.xlsx' or file_extension == '.xls':
                data = self.read_excel(file_path, sheet_name)
            elif file_extension == '.csv':
                data = self.read_csv(file_path)
            elif file_extension == '.json':
                data = self.read_json(file_path)
                if isinstance(data, dict):
                    return data.get(test_name, {})
                elif isinstance(data, list):
                    for item in data:
                        if item.get('test_name') == test_name:
                            return item
                    return {}
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            # For Excel and CSV, find the row with matching test name
            for row in data:
                if row.get('test_name') == test_name or row.get('TestName') == test_name:
                    return row
            
            self.logger.warning(f"Test data not found for test: {test_name}")
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting test data for {test_name}: {str(e)}")
            raise
    
    def write_excel(self, data, file_path, sheet_name='Sheet1'):
        """
        Write data to Excel file
        Args:
            data (list): List of dictionaries to write
            file_path (str): Output file path
            sheet_name (str): Sheet name
        """
        try:
            df = pd.DataFrame(data)
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            self.logger.info(f"Successfully wrote data to Excel file: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error writing Excel file {file_path}: {str(e)}")
            raise
    
    def write_csv(self, data, file_path):
        """
        Write data to CSV file
        Args:
            data (list): List of dictionaries to write
            file_path (str): Output file path
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)
            self.logger.info(f"Successfully wrote data to CSV file: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file {file_path}: {str(e)}")
            raise