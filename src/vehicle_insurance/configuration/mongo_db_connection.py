import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


class MongoDBClient:
    """
    Creates and stores a reusable MongoDB client.
    """

    client = None

    def __init__(self):
        if MongoDBClient.client is None:
            mongodb_url = os.getenv("MONGODB_URL")

            if mongodb_url is None:
                raise ValueError("MONGODB_URL not found in .env file")

            MongoDBClient.client = MongoClient(
                mongodb_url,
                tlsCAFile=certifi.where()
            )

        self.client = MongoDBClient.client