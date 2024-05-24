import logging
import os

from dotenv import load_dotenv
from supabase import create_client, Client

from database.client.IDatabaseClient import IDatabaseClient


class PostgresClientI(IDatabaseClient):
    def __init__(self):
        load_dotenv()
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')
        self.db: Client = create_client(supabase_url, supabase_key)

    def query(self, query):
        return self.db.rpc('execute_sql', {'_script': query}).execute()

    def insert(self, table_name, item):
        logging.log(logging.INFO, f'Inserting {item.__dict__} into {table_name}')
        return self.db.from_(table_name).insert([item.__dict__]).execute()

    def update(self, table_name, item):
        logging.log(logging.DEBUG, f'Updating {item.__dict__} in {table_name}')
        return self.db.table(table_name).update(item.__dict__).eq('id', item.id).execute()

    def delete(self, table_name, _id):
        logging.log(logging.WARN, f'Deleting {_id} from {table_name}')
        return self.db.table(table_name).delete().eq('id', _id).execute()

    def find_by_id(self, table_name, _id):
        response = self.find_all_by_column(table_name, 'id', _id)
        return response['data'][0] if response['data'] else None

    def find_all_by_column(self, table_name, column, value):
        logging.log(logging.DEBUG, f'Searching {value} in {column} column of {table_name} table')
        response = self.db.from_(table_name).select('*').eq(column, value).execute()
        return response['data']
