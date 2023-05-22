#from flask import Flask, request, jsonify
import pandas as pd
import main.validation as validation
import os
import main.utils as utils

#app = Flask(__name__)

#@app.route('/validate', methods=['POST'])
async def validate_endpoint(file):
    # Check if a file is included in the request
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file provided.'}), 400
    
    # file = request.files['file']

    # # Save the file to a temporary location
    # file_path = 'temp.csv'
    # file.save(file_path)
    file.file.seek(0)
    contents = file.file.read().decode("utf-8")
    print('file::::::::::::',contents)
    file_path = utils.save_uploaded_file(file)
    print(file_path)
    file1 = open(file_path, "r")
    print("Output of Read function is ")
    print(file1.read())
    print()
    extracted_file = utils.extract_data(file_path)


    # Validate the CSV data
    validation_result = validation.validate_csv(extracted_file)
    
    # Delete the temporary file
   # os.remove(file_path)
    # Return the validation result as JSON
    return validation_result

# if __name__ == '__main__':
#     app.run()








