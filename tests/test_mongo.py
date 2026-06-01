from vehicle_insurance.configuration.mongo_db_connection import MongoDBClient

client = MongoDBClient().client
print("MongoDB connected successfully!")
print(client.list_database_names())