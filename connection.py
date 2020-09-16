from pymongo import MongoClient
import settings

client = MongoClient(settings.mongodb_uri, settings.port)
db = client['usersdata']
