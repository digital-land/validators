import pandas as pd
import os
from flask import Flask, request, jsonify

class JsonResponse:
    def __init__(self, scope, level, rowNumber,columnNames, errorCode, errorMessage,url):
        self.scope = scope
        self.level = level
        self.rowNumber = rowNumber
        self.columnNames = columnNames
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.url = url

    def to_dict(self):
        response = {
            'scope': self.scope,
            'level': self.level,
            'rowNumber': self.rowNumber,
            'columnNames': self.columnNames,
            'errorCode': self.errorCode,
            'errorMessage': self.errorMessage,
            'url': self.url,
            
        }
        return response

def validate_csv(file_path):
   
   try:
        # Load data from the CSV file
        data = pd.read_csv(file_path,  index_col=False)
        
        if data.empty:
            return "No content in file"


        response = []
        for index, row in data.iterrows():
            missing = row.isnull().tolist()
            if any(missing):
                missing_columns = [column for column, is_missing in zip(data.columns, missing) if is_missing]
                additional_data = JsonResponse(
                        scope= 'Field',
                        level= 'Fatal',
                        rowNumber= index + 1,
                        columnNames= missing_columns,
                        errorCode= 'F001',
                        errorMessage= 'Missing Fields',
                        url= 'demo')
                response.append(additional_data.to_dict())

        if response is not None:
            return jsonify(response), 400
    
    
   except pd.errors.EmptyDataError:
        return "error: No content in file"
   except Exception as e:
        print(f"Error occurred while checking CSV: {str(e)}")
        return False



