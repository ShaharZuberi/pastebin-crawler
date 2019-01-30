import threading
from Modules.PastedBin import *
from Modules.TinyDB import *
from Modules.SiteRequest import *
from tinydb import Query #TODO: Can I move this to the TinyDB.py also?


class WebCrawler:
    TIME_INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"
    MAX_IN_MEMORY_PASTES_SAVED = 200

    def __init__(self):
        self.recent_pasted_bins = [] #Our pasted bin data structure. a list of PastedBin objects
        return

    def start(self):
        threading.Timer(self.TIME_INTERVAL,self.start).start()
        print("Begining crawling "+str(arrow.now()))
        print("IN_MEMORY_PASTES:"+str(len(self.recent_pasted_bins)))

        unsaved_bins_keys=self.get_unsaved_pasted_bins_keys() # TODO: I can export this to a different method
        for key in unsaved_bins_keys:
            print("Importing "+key)
            new_bin = PastedBin(self.SITE_URL, key)
            imported = new_bin.import_pasted_bin()
            if imported is True:
                new_bin.save_pasted_bin_to_db()

                if (len(self.recent_pasted_bins)>self.MAX_IN_MEMORY_PASTES_SAVED):
                    del self.recent_pasted_bins[0]
                self.recent_pasted_bins.append(new_bin)
            else:
                print("Import of "+key+" failed. skipping it")

    def get_unsaved_pasted_bins_keys(self):
        bins_keys = self.get_recent_pasted_bin_keys()
        print("RECENT pasted bins:" + str(len(bins_keys)))

        unsaved_keys = [key for key in bins_keys if not self.is_pasted_bin_exist_in_db(key)]
        print("UNSAVED pasted bins:" + str(len(unsaved_keys)))

        return unsaved_keys

    def get_recent_pasted_bin_keys(self):
        r = Request()
        parsed_html = r.parse_html(self.ARCHIVE_URL)
        if parsed_html is None:
            raise Exception("Unable to load url "+self.ARCHIVE_URL)

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