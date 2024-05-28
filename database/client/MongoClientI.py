import logging
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from util import utils as util

from database.client.IDatabaseClient import IDatabaseClient


class MongoClientI(IDatabaseClient):
    def __init__(self):
        load_dotenv()
        self.client = MongoClient(os.environ.get('MONGO_URI'), server_api=ServerApi('1'))
        self.db = self.client['one_player_bot']

        try:
            self.client.admin.command('ping')
            logging.log(logging.INFO, 'Connected to MongoDB')
        except Exception as e:
            logging.log(logging.ERROR, f'Error connecting to MongoDB: {e}')

    def query(self, query):
        logging.log(logging.INFO, f'Executing query: {query}')

    def insert(self, table_name, item):
        logging.log(logging.INFO, f'Inserting {item} into {table_name} table')
        self.db[table_name].insert_one(item.__dict__)
        return item

    def update(self, table_name, item):
        logging.log(logging.INFO, f'Updating {item} in {table_name} table')
        item_as_map = util.to_dict(item)
        self.db[table_name].update_one({'_chat_id': item_as_map['_chat_id']}, {'$set': item_as_map})

    def delete(self, table_name, _id):
        logging.log(logging.INFO, f'Deleting {_id} from {table_name} table')
        self.db[table_name].delete_one({'_chat_id': _id})

    def find_by_id(self, table_name, _id):
        response = self.find_all_by_column(table_name, '_chat_id', _id)
        return response[0] if response else None

    def find_all_by_column(self, table_name, column, value):
        logging.log(logging.INFO, f'Searching {value} in {column} column of {table_name} table')
        find = []
        for item in self.db[table_name].find({column: value}):
            find.append(item)
        return find
