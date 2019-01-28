import requests
import os
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query


class WebCrawler:
    SAMPLE_TIME_INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"
    TINY_DB_PATH = 'tinyDB/db.json'

    def __init__(self):
        return

    def start(self):
        self.get_unsaved_pasted_bins()

    def get_unsaved_pasted_bins(self):
        self.is_pasted_bin_exist_in_db("sfsf")

    def get_recent_pasted_bin_keys(self):
        r = requests.get(self.ARCHIVE_URL)
        # TODO: handle different status_code: 200, 404, 401
        parsed_html = BeautifulSoup(r.text)
        main_table = parsed_html.body.find("table", {"class": "maintable"})
        pasted_bins_key_list = [bin_key['href'] for bin_key in main_table.findAll("a")]
        return pasted_bins_key_list

    def is_pasted_bin_exist_in_db(self,pasted_bin_key):
        if not os.path.isfile(self.TINY_DB_PATH): # TODO: Handle the case where the folder(s) path to the file does not exist, for example "tinyDB" in this case
            file = open(self.TINY_DB_PATH, "w")
            file.close()
        db = TinyDB(self.TINY_DB_PATH)
        bin_query = Query()
        fetched_bin = db.search(bin_query.key == pasted_bin_key)

        if len(fetched_bin)==0:
            return False
        return True


C = WebCrawler()
C.start()