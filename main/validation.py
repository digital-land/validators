import pandas as pd
import os
def validate_csv(file_path):
   
   try:
        # Load data from the CSV file
        data = pd.read_csv(file_path)
        
        if data.empty:
            return "CSV file empty"

        # Check for missing fields
        missing = data.isnull().sum()
        
        # Check if any missing fields exist
        if missing.any():
            missing_fields = missing[missing > 0]
            print("Missing fields:")
            for field, count in missing_fields.items():
                print(f"{field}: {count} missing value(s)")
        else:
            print("No missing fields found.")
    
   except pd.errors.EmptyDataError:
        return "error: No content in file."
   except Exception as e:
        print(f"Error occurred while checking CSV: {str(e)}")
        return False



