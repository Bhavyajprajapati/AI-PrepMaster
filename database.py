import pymongo

# MongoDB Connection
# client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
client = pymongo.MongoClient("mongodb+srv://sumitraval120:lCMRq8Ni6I3PlxBE@clusterforai.otg78.mongodb.net/")  # Update with your MongoDB URI

db = client["user_database"]
users_collection = db["users"]
