from flask import Flask, request, jsonify
import pandas as pd
import validation
import os

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_endpoint():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400
    
    file = request.files['file']
   
   # Save the file to a temporary location
    file_path = 'temp.csv'
    file.save(file_path)
    # Validate the CSV data
    validation_result = validation.validate_csv(file_path)
    
    # Delete the temporary file
    os.remove(file_path)
    # Return the validation result as JSON
    return jsonify(validation_result)

if __name__ == '__main__':
    app.run()






