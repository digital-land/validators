import pandas as pd
import os
from flask import Flask, request, jsonify
from validation_result import JsonResponse, JsonError



def validate_csv(file_path):
   try:
        response = []
        # Load data from the CSV file
        data = pd.read_csv(file_path,  index_col=False)
        
        if data.size == 0:
            error_message = {'Error occurred while checking CSV': 'Only header found'}
            error = JsonError(
                scope='File',
                level='Fatal',
                errorCode='F001',
                errorMessage=error_message,
                url='demo'
            )
            statusResponse = JsonResponse(status='FAILED')
            statusResponse.add_error(error.to_dict())
            return jsonify(statusResponse.to_dict()), 400
        
        for index, row in data.iterrows():
            missing = row.isnull().tolist()
            if any(missing):
                missing_columns = [column for column, is_missing in zip(data.columns, missing) if is_missing]
                additional_data = JsonError(
                        scope= 'Field',
                        level= 'Fatal',
                        errorCode= 'F002',
                        errorMessage= 'Missing Fields',
                        url= 'demo')
                additional_data.rowNumber= index + 1,
                additional_data.columnNames= missing_columns,
                response.append(additional_data.to_dict())

        if response is not None:
             statusResponse = JsonResponse(status= 'FAILED')
             statusResponse.add_error(response)
             return jsonify(statusResponse.to_dict()), 400
    
    
   except pd.errors.EmptyDataError:
       error = JsonError(
          scope='File',
          level='Fatal',
          errorCode='F001',
          errorMessage='Empty File',
          url='demo'
         )
       statusResponse = JsonResponse(status='FAILED')
       statusResponse.add_error(error.to_dict())
       return jsonify(statusResponse.to_dict()), 400
   except Exception as e:
         error_message = {'Error occurred while checking CSV': str(e)}
         error = JsonError(
          scope='File',
          level='Fatal',
          errorCode='F001',
          errorMessage=error_message,
          url='demo'
         )
         statusResponse = JsonResponse(status='FAILED')
         statusResponse.add_error(error.to_dict())
         return jsonify(statusResponse.to_dict()), 400



