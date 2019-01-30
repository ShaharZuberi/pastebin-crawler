import os
from tinydb import TinyDB, Query


class DB:
    DB_PATH = 'tinyDB/db.json'

    def __init__(self):
        dir_path = os.path.dirname(self.DB_PATH)

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        if not os.path.isfile(
                self.DB_PATH):
            file = open(self.DB_PATH, "w")
            file.close()

        self.db = TinyDB(self.DB_PATH)

    def search_key(self, key):
        query = Query()
        return self.db.search(query.key == key)

    def insert(self, json):
        self.db.insert(json)

    def close(self):
        self.db.close()
