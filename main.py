import requests
from bs4 import BeautifulSoup


class Crawler:
    SAMPLE_TIME_INTERVAL = 120
    CRAWL_URL = "https://pastebin.com/archive"

    def __init__(self):
        # TODO: load the lastest crawled pasteBin object and continue crawl from there
        return

    def start(self):
        r = requests.get(self.CRAWL_URL)
        # TODO: handle different status_code: 200, 404, 401
        parsed_html = BeautifulSoup(r.text)
        main_table = parsed_html.body.find("table",{"class":"maintable"})
        pastes_links_list = main_table.findAll("a")


C = Crawler()
C.start()