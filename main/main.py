import pandas as pd
import main.validation as validation
import os
import main.utils as utils
from main.logger import get_logger

logger = get_logger(__name__)

async def validate_endpoint(file):

    logger.info("Validations running against uploaded file..")
    # Save the file to a temporary location
    file_path = utils.save_uploaded_file(file)
    
    extracted_file = utils.extract_data(file_path)

    # Validate the CSV data
    validation_result = validation.validate_csv(extracted_file)
    logger.info("Validations executed successfully.")
    return validation_result








