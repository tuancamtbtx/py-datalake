import pandas as pd

class ExcelReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.reader = pd.ExcelFile(file_name, engine='openpyxl')
    
    def read_sheet(self, sheet_name):
        """
        Reads a specific sheet from the Excel file.

        Parameters:
        - sheet_name (str): The name of the sheet to read.

        Returns:
        - df (pandas.DataFrame): The contents of the sheet as a DataFrame.
        """
        df = self.reader.parse(sheet_name)
        return df