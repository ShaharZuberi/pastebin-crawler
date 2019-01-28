import requests
from bs4 import BeautifulSoup


class Crawler:
    SAMPLE_TIME_INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"

    def __init__(self):
        # TODO: load the lastest crawled pasteBin object and continue crawl from there
        return

    def start(self):
        self.get_unsaved_pasted_bins()

    def get_unsaved_pasted_bins(self):
        r = requests.get(self.ARCHIVE_URL)
        # TODO: handle different status_code: 200, 404, 401
        parsed_html = BeautifulSoup(r.text)
        main_table = parsed_html.body.find("table", {"class": "maintable"})
        pasted_bin_links_list = main_table.findAll("a")
        

    def last_saved_pasted_bin(self):
        #TODO: return the last saved pasted bin from the tinyDB
        return

C = Crawler()
C.start()