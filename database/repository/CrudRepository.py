from abc import ABC

from database.client.IDatabaseClient import IDatabaseClient


class CrudRepository(ABC):
    def __init__(self, client, table_name):
        self.db: IDatabaseClient = client
        self.table_name = table_name

    def insert(self, item):
        return self.db.insert(self.table_name, item)

    def find(self, _id):
        return self.db.find_by_id(self.table_name, _id)

    def update(self, item):
        return self.db.update(self.table_name, item)

    def delete(self, _id):
        return self.db.delete(self.table_name, _id)

    def find_all_by_column(self, column, value):
        return self.db.find_all_by_column(self.table_name, column, value)
