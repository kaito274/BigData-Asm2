#1
import pymongo 
import os
import pandas as pd

DATA_PATH = 'EEET2574_Assignment2_data'

# PATH_HOME = os.path.dirname(os.path.realpath(__file__)) 

# Replace this with your MongoDB cluster
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.etnbg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# check the connection
if client:
    print("Connected to MongoDB.")
else:
    print("Connection to MongoDB failed.")

# Create or reference the database
db = client['energy_data']


def load_data(data_path):
    entries = os.listdir(data_path)
    # Filter out directories (subfolders)
    subfolders = [entry for entry in entries if os.path.isdir(os.path.join(data_path, entry))]
    print(subfolders)
    for subfolder in subfolders:
        db[subfolder].drop() # Drop the collection if it exists
        subfolder_path = os.path.join(data_path, subfolder)
        # print(subfolder_path)
        files = os.listdir(subfolder_path)
        # print(files)
        for file in files:
            print("Loading data from file:", file)
            file_name = file.rsplit('.', 1)[0]
            [company_name, energy, year] = file_name.split('_')
            if file.endswith(".csv"):
                file_path = os.path.join(subfolder_path, file)
                try: 
                    df = pd.read_csv(file_path)
                    records = df.to_dict(orient='records')
                    for record in records:
                        record.update({"company": company_name, "year": int(year)})
                    # Insert the records in bulk
                    db[energy].insert_many(records)
                    print(f"Inserted {len(records)} records into {energy} collection.")
                except Exception as e:
                    print(f"An error occurred: {e}")

    print("Load data successfully.")

load_data(DATA_PATH)



