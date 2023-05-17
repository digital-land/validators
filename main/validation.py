import pandas as pd
import os
from flask import Flask, request, jsonify
from validation_result import JsonResponse, JsonError



def validate_csv(file_path):
   try:
        response = []
        statusResponse = JsonResponse()
        # Load data from the CSV file
        data = pd.read_csv(file_path,  index_col=False)
        
        if data.size == 0:
            error_message = 'Error occurred while checking CSV: Only header found'
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
                        url= 'demo',
                        rowNumber= index+1,
                        columnNames=missing_columns)
                response.append(additional_data.to_dict())

        
        
        # Identify duplicate rows based on the reference column
        reference_column = data.columns[0]
        duplicates = data.duplicated(subset=[reference_column], keep=False)
        
        # Iterate over the duplicate rows and create error responses
        for index, is_duplicate in enumerate(duplicates):
            if is_duplicate:
                duplicate_row = data.loc[index]
                reference_value = duplicate_row[reference_column]
                
                # Create the error response
                error = JsonError(
                    scope='Row',
                    level='Fatal',
                    errorCode='D001',
                    errorMessage=f"Duplicate row found for reference: {reference_value}",
                    url='demo',
                    rowNumber= index+1,
                    columnNames=missing_columns
                )
                error.rowNumber = index + 1
                response.append(error.to_dict())
        
        if response:
            status_response = JsonResponse(status='FAILED')
            for error in response:
                status_response.add_error(error)
            return jsonify(status_response.to_dict()), 400
    
    
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
         error_message = 'Error occurred while checking CSV:', str(e)
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



