import pandas as pd
import os
import json
from main.models.validation_result import JsonResponse, JsonError
from shapely.geometry import Polygon, Point
from shapely import wkt
from main.logger import get_logger
#import pdb
#from specification import Specification


logger = get_logger(__name__)

# Define the polygon for the UK
uk_polygon = Polygon([
    (-10.854492, 59.686853),   # Northwest corner (Scotland)
    (-13.710937, 49.823809),   # Southwest corner (Wales)
    (1.076660, 50.731547),     # Southeast corner (England)
    (-5.097656, 58.763656),    # Northeast corner (Scotland)
    (-10.854492, 59.686853)    # Closing the polygon
])


def validate_csv(file_path):
   try:
        # specification = Specification()
        # mandatory_fields = specification.schema_field['conservation-area']
        
        response = []
        statusResponse = JsonResponse()
       
        data = pd.read_csv(file_path,  index_col=False)
        
        #Checking if file only contains headers
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
            return json.dumps(statusResponse.to_dict()), 400
        

        #headers = data.columns.tolist() 
        # missing_headers = [header for header in mandatory_fields if header not in headers]
        # print(missing_headers)
        ### Iterating over the rows
        for index, row in data.iterrows():
            #pdb.set_trace()

            ## Check if the point falls within the UK geometry
            # Remove the "POINT" prefix and parentheses
            point = row.Point.replace("POINT", "").strip()[1:-1]
            # Split the coordinates by space
            coordinates = point.split()
            # polygon = wkt.loads(row.Geometry)
            # if polygon.within(uk_polygon):
            #     print("yes it is")
            # else:
            #     print("No it is not")
            point = Point(float(coordinates[0]), float(coordinates[1]))
            is_within_uk = uk_polygon.contains(point)
            if not is_within_uk:
                additional_data = JsonError(
                        scope= 'Field',
                        level= 'Fatal',
                        errorCode= 'F003',
                        errorMessage= 'Point is not within the UK',
                        url= 'demo',
                        rowNumber= index+1,
                        columnNames='Point')
                response.append(additional_data.to_dict())

            #Checking for null values    
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
        
        #Adding all responses together
        if response:
            status_response = JsonResponse(status='FAILED')
            for error in response:
                status_response.add_error(error)
            return json.dumps(status_response.to_dict()), 400
    
    
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
       return json.dumps(statusResponse.to_dict()), 400
   except Exception as e:
         logger.error('Error occurred while checking CSV:%s', str(e))
         error_message = 'Error occurred while checking CSV'
         error = JsonError(
          scope='File',
          level='Fatal',
          errorCode='F001',
          errorMessage=error_message,
          url='demo'
         )
         statusResponse = JsonResponse(status='FAILED')
         statusResponse.add_error(error.to_dict())
         return json.dumps(statusResponse.to_dict()), 400



