from abc import abstractmethod


class IDatabaseClient:
    @abstractmethod
    def query(self, query):
        raise NotImplementedError

    @abstractmethod
    def insert(self, table_name, item):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, table_name, _id):
        raise NotImplementedError

    @abstractmethod
    def update(self, table_name, item):
        raise NotImplementedError

    @abstractmethod
    def delete(self, table_name, _id):
        raise NotImplementedError

    @abstractmethod
    def find_all_by_column(self, table_name, column, value):
        raise NotImplementedError
