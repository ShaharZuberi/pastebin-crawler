import requests
import os
import arrow
from bs4 import BeautifulSoup
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

    def get_handle(self):
        self.db = TinyDB(self.TINY_DB_PATH)
        return self.db

    def close(self):
        self.db.close()


class PastedBin:
    def __init__(self,site,key):
        self.site = site
        self.key = key

    def import_pasted_bin(self):
        r = requests.get(self.site+'/Z5h3AXD1')
        # TODO: handle different status codes: 200, 404, 401, maybe try and make a class for the request that can be used in both classes
        parsed_html = BeautifulSoup(r.text,features="html.parser")

        title_tag = parsed_html.body.find("div", {"class": "paste_box_line1"})
        info_tag = parsed_html.body.find("div", {"class": "paste_box_line2"})

        author = info_tag.find("a")
        if author==None:
            author="Unknown"
        else:
            author = author.text

        title = title_tag.text # TODO: Normalize
        date = info_tag.find("span")['title']
        date = arrow.get(date,'dddd Do of MMMM YYYY HH:mm:ss A')
        content = requests.get(self.site+'/raw'+self.key)

        self.save_pasted_bin_values(title,author,date,content,)

    def save_pasted_bin_values(self,title,author,date,content):
        author = author.strip(' \t\n\r')
        title = title.strip(' \t\n\r')
        content = content.text.strip(' ')
        row = {'key': self.key, 'title': title, 'author': author, 'date': str(date), 'content': content}
        print('key'+self.key+' saved to db')
        db = DB().get_handle()
        db.insert(row)
        db.close()


class WebCrawler:
    SAMPLE_TIME_INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"

    def __init__(self):
        return

    def start(self):
        unsaved_bins_keys=self.get_unsaved_pasted_bins()
        for key in unsaved_bins_keys:
            a = PastedBin(self.SITE_URL, key)
            a.import_pasted_bin()

    def get_unsaved_pasted_bins(self):
        bins_keys = self.get_recent_pasted_bin_keys()
        print("RECENT pasted bins:" + str(len(bins_keys)))
        unsaved_keys = [key for key in bins_keys if not self.is_pasted_bin_exist_in_db(key)]
        print("UNSAVED pasted bins:" + str(len(unsaved_keys)))
        return unsaved_keys

    def get_recent_pasted_bin_keys(self):
        r = requests.get(self.ARCHIVE_URL)
        # TODO: handle different status_code: 200, 404, 401
        parsed_html = BeautifulSoup(r.text,features="html.parser")
        main_table = parsed_html.body.find("table", {"class": "maintable"})
        pasted_bins_key_list = [bin_key['href'] for bin_key in main_table.findAll("a") if '/archive' not in bin_key['href']]
        return pasted_bins_key_list

    #TODO: I can imrove the search if I open a connection to the DB once and query all and then return the list instead of open-search-close for each key
    def is_pasted_bin_exist_in_db(self,pasted_bin_key):
        db = DB().get_handle()
        bin_query = Query()
        fetched_bin = db.search(bin_query.key == pasted_bin_key)
        db.close()
        if len(fetched_bin)==0:
            return False
        return True

C = WebCrawler()
C.start()