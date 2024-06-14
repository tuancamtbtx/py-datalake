import pandas as pd

class ExcelReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.reader = pd.ExcelFile(file_name, engine='openpyxl')
    
    def read_sheet(self, sheet_name):
        df = self.reader.parse(sheet_name)
        return df