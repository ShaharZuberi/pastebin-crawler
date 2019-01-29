import requests
import os
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

class PastedBin:


    def __init__(self,site,key):
        self.site = site
        self.key = key

    def load_pasted_bin(self):
        r = requests.get(self.site+self.key)
        # TODO: handle different status codes: 200, 404, 401, maybe try and make a class for the request that can be used in both classes
        parsed_html = BeautifulSoup(r.text,features="html.parser")

        title_tag = parsed_html.body.find("div", {"class": "paste_box_line1"})
        info_tag = parsed_html.body.find("div", {"class": "paste_box_line2"})

        title = title_tag.text
        author = info_tag.contents[2]
        date = info_tag.contents[5]['title']
        content = requests.get(self.site+'/raw'+self.key)

        self.save_pasted_bin_values(title,author,date,content)

    def save_pasted_bin_values(self,title,author,date,content):
        # TODO: Continue from here
        return "remove me"


class WebCrawler:
    SAMPLE_TIME_INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"
    TINY_DB_PATH = 'tinyDB/db.json'

    def __init__(self):
        return

    def start(self):
        unsaved_bins_keys=self.get_unsaved_pasted_bins()
        a = PastedBin(self.SITE_URL,unsaved_bins_keys[0])
        a.load_pasted_bin()

    def fetch_bins(self,keys):
        return "some value"

    def get_unsaved_pasted_bins(self):
        bins_keys = self.get_recent_pasted_bin_keys()
        unsaved_keys = [key for key in bins_keys if not self.is_pasted_bin_exist_in_db(key)]
        return unsaved_keys

    def get_recent_pasted_bin_keys(self):
        r = requests.get(self.ARCHIVE_URL)
        # TODO: handle different status_code: 200, 404, 401
        parsed_html = BeautifulSoup(r.text,features="html.parser")
        main_table = parsed_html.body.find("table", {"class": "maintable"})
        pasted_bins_key_list = [bin_key['href'] for bin_key in main_table.findAll("a")]
        return pasted_bins_key_list

    #TODO: I can imrove the search if I open a connection to the DB once and query all and then return the list instead of open-search-close for each key
    def is_pasted_bin_exist_in_db(self,pasted_bin_key):
        db_dir_path=os.path.dirname(self.TINY_DB_PATH)
        if not os.path.isdir(db_dir_path):
            os.makedirs(db_dir_path)
        if not os.path.isfile(self.TINY_DB_PATH): # TODO: Handle the case where the folder(s) path to the file does not exist, for example "tinyDB" in this case
            file = open(self.TINY_DB_PATH, "w")
            file.close()
        db = TinyDB(self.TINY_DB_PATH)
        bin_query = Query()
        fetched_bin = db.search(bin_query.key == pasted_bin_key)
        db.close()
        if len(fetched_bin)==0:
            return False
        return True


C = WebCrawler()
C.start()