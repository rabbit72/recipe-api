import os
import urllib.parse

import motor.motor_asyncio

# TODO root user should not be used in production
login = urllib.parse.quote_plus(os.environ["MONGO_ROOT"])
password = urllib.parse.quote_plus(os.environ["MONGO_ROOT_PASSWORD"])
mongo_url = os.environ["MONGO_URL"]
database_name = os.environ["MONGODB_NAME"]

mongo_connection_string = (
    f"mongodb://{login}:{password}@{mongo_url}/?retryWrites=true&w=majority"
)

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_connection_string)
database_connection = client[database_name]
