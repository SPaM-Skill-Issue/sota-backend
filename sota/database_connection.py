from pymongo import MongoClient
from decouple import config
from mongomock import MongoClient as MockMongoClient


def get_database_client():
    if config('TESTING', default=False, cast=bool):
        return MockMongoClient()
    else:
        return MongoClient(config("MONGO", cast=str))


client = get_database_client()

sota_database = client[config("DATABASE", cast=str, default="")]
sport_detail_collection = sota_database[config("SPORT_DETAIL_COLLECTION", cast=str, default="")]
sub_sport_collection = sota_database[config("SUB_SPORT_COLLECTION", cast=str, default="")]
audient_collection = sota_database[config("AUDIENT_COLLECTION", cast=str, default="")]
medal_collection = sota_database[config("MEDAL_COLLECTION", cast=str, default="")]
keys_collection = sota_database[config("KEYS_COLLECTION", cast=str, default="")]