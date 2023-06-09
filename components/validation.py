import pandas as pd
import os
import json
from components.models.validation_result import JsonResponse, JsonError
from shapely.geometry import Polygon, Point
from shapely import wkt
from components.logger import get_logger
#import pdb
#from factory import Factory
import components.models.entity as Entity


logger = get_logger(__name__)

# Define the polygon for the UK
uk_polygon = Polygon([
    (-10.854492, 59.686853),   # Northwest corner (Scotland)
    (-13.710937, 49.823809),   # Southwest corner (Wales)
    (1.076660, 50.731547),     # Southeast corner (England)
    (-5.097656, 58.763656),    # Northeast corner (Scotland)
    (-10.854492, 59.686853)    # Closing the polygon
])


def validate_endpoint(data):

    logger.info("Validations running against uploaded file..")
    #Checking if file is empty or only comtains header
    if len(data) == 0:
        error = JsonError(
            scope='File',
            level='Fatal',
            errorCode='F001',
            errorMessage='Empty File',
            url='demo'
            )
        statusResponse = JsonResponse(status='FAILED')
        statusResponse.add_error(error.to_dict())
        raise statusResponse
        
   
    try:
        # try:
        #     factory_obj = Factory()
        #     dataset_specifications = factory_obj.get_specification("conservation-area") #dataset passed from frontend
        # except KeyError:
        #     logger.error("Dataset does not have specification defined")
        
        result = []
        response = []
        statusResponse = JsonResponse()
        duplicate_rows = []
        reference_values = set()
       
        #headers = data.columns.tolist() 
        # missing_headers = [header for header in mandatory_fields if header not in headers]
       
        ### Iterating over the rows
        for index, entity in enumerate(data):
            result_entity = entity
            
            # Check if the geometry falls within the UK geometry
            geometry = wkt.loads(entity.Geometry)
            is_within_uk = uk_polygon.contains(geometry)

            if not is_within_uk:
                additional_data = JsonError(
                    scope='Field',
                    level='Fatal',
                    errorCode='F003',
                    errorMessage='Point is not within the UK',
                    url='demo',
                    rowNumber=index + 1,
                    columnNames='Point'
                )
                response=additional_data.to_dict()
                result_entity.errors.append(response)
            
            # Checking for null values
            for field, value in entity.__dict__.items():
                 if value is None or value == '':
                    additional_data = JsonError(
                    scope='Field',
                    level='Fatal',
                    errorCode='F002',
                    errorMessage='Missing Fields',
                    url='demo',
                    rowNumber=index + 1,
                    columnNames=field
                )
                    response=additional_data.to_dict()
                    result_entity.errors.append(response)
            
                
            
            
            # # Identify duplicate rows based on the reference column
            reference = entity.Reference
            if reference in reference_values:
                duplicate_rows.append(index + 1)
            else:
                reference_values.add(reference)

            if reference_values:
                additional_data =JsonError(
                    scope='Row',
                    level='Fatal',
                    errorCode='D001',
                    errorMessage=f"Duplicate row found for reference: {reference}",
                    url='demo',
                    rowNumber= index+1,
                    columnNames= 'Reference'
                )
                response=additional_data.to_dict()
                result_entity.errors.append(response)
            
            result.append(result_entity)
        logger.info("Validations executed successfully.")
        return result
       
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
         raise statusResponse



