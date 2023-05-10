# validators
Make sure that data meets the specification for the collections.


# Steps to setup the project
    pip install -r requirements.txt

# To run it locally, 
    python3 main.py runserver

# Use the curl command to test the endpoint /validate
    example curl command: 
        curl -X POST -H "Content-Type: multipart/form-data" -F "file=@validators/csv/camden_conservation_areas.csv" http://127.0.0.1:5000/validate 
