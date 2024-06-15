import pandas as pd
from datetime import datetime

class ExcelWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.writer = pd.ExcelWriter(file_name, engine='openpyxl')
        
    def write_sheet(self, df, sheet_name):
        df = df.applymap(lambda x: x.replace(tzinfo=None) if isinstance(x, datetime) and x.tzinfo else x)
        df.to_excel(self.writer, sheet_name=sheet_name, index=False)
    
  
    def close(self):
        self.writer.close()