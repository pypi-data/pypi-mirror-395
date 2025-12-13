from pymongo import MongoClient, errors
from inception_audittrail_logger.settings_audittrail import get_audittrail_setting
from pymongo.database import Database

audittrail_setting = get_audittrail_setting()
MONGO_DB_NAME = "audittrail_db"
MONGO_COLLECTION_NAME = "audittrail"

# Connect to MongoDB
client_audittrail = MongoClient(audittrail_setting.mongodb_url)
try:
    client_audittrail.admin.command("ping")
    print("✅ Successfully connected to Audittrail MongoDB!")
except errors.ServerSelectionTimeoutError as e:
    print("❌ Failed to connect to Audittrail MongoDB.")

db_audittrail = client_audittrail[MONGO_DB_NAME]
collection_audittrail = db_audittrail[MONGO_COLLECTION_NAME]


async def insert_document(document: dict):
    result = collection_audittrail.insert_one(document)
    print(
        f"✅ Successfully inserted document into Audittrail MongoDB: {result.inserted_id}"
    )
    return result


async def search_documents(query: dict):
    return collection_audittrail.find(query)


def get_audittrail_mongo_db() -> Database:
    return db_audittrail
