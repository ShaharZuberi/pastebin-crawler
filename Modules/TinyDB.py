import os
from tinydb import TinyDB, Query


class DB:
    TINY_DB_PATH = 'tinyDB/db.json' # TODO: Take this to config

    def __init__(self):
        db_dir_path = os.path.dirname(self.TINY_DB_PATH)
        if not os.path.isdir(db_dir_path):
            os.makedirs(db_dir_path)
        if not os.path.isfile(
                self.TINY_DB_PATH):  # TODO: Handle the case where the folder(s) path to the file does not exist, for example "tinyDB" in this case
            file = open(self.TINY_DB_PATH, "w")
            file.close()
        self.db = None

    def get_handle(self):
        self.db = TinyDB(self.TINY_DB_PATH)
        return self.db

    def close(self):
        self.db.close()