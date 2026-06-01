import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient


# Load variables from .env
load_dotenv()

# Read MongoDB connection string
MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL not found in .env file")

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_URL)

# Create / access database
database = client["vehicle_insurance"]

# Create / access collection
collection = database["insurance_data"]

# Read CSV file
df = pd.read_csv("notebook/data.csv")

# Convert DataFrame to list of dictionaries
records = df.to_dict(orient="records")

# Optional: clear existing data to avoid duplicates
collection.delete_many({})

# Insert all records
result = collection.insert_many(records)

print(f"Inserted {len(result.inserted_ids)} documents successfully!")