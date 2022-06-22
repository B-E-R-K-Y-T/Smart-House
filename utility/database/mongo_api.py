import pymongo

from config_files.config import MONGO_IP, MONGO_PORT


class MongoSH:
    def __init__(self, mongo_ip=MONGO_IP, mongo_port=MONGO_PORT):
        try:
            # Create the client
            self.client = pymongo.MongoClient(mongo_ip, mongo_port)
        except Exception as e:
            print(e)

    def create_user(self, first_name, last_name, phone, email, password):
        return {
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
                "email": email,
                "hash": password,
                }

    def get_mongo_object(self):
        return self.client

    def get_database(self, key_database):
        return self.client[key_database]

    def get_collection(self, database, key_collection):
        return database[key_collection]

    def insert_data(self, key, data):
        key.insert_one(data)
