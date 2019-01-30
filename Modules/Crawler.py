import threading
from Modules.PastedBin import *
from Modules.TinyDB import *
from Modules.SiteRequest import *


class Crawler:
    INTERVAL = 120
    SITE_URL = "https://pastebin.com"
    ARCHIVE_URL = SITE_URL+"/archive"
    MAX_IN_MEMORY_PASTES_SAVED = 200

    def __init__(self):
        self.pastes = []
        return

    def start(self):
        threading.Timer(self.INTERVAL,self.start).start()
        print("Begining crawling "+str(arrow.now()))
        print("IN_MEMORY_PASTES:"+str(len(self.pastes)))

        self.parse_and_save()

    def parse_and_save(self):
        recent_keys = self.recent_pastes_keys() # All keys
        unsaved_keys = self.filter_unsaved_keys(recent_keys) # Unsaved keys only

        for key in unsaved_keys:
            print("Parsing "+key)
            new_paste = PastedBin(self.SITE_URL, key)

            parsed = new_paste.parse_paste()
            if parsed is True:
                new_paste.save_paste()

                if len(self.pastes) > self.MAX_IN_MEMORY_PASTES_SAVED:
                    del self.pastes[0]
                self.pastes.append(new_paste)
            else:
                print("Import of "+key+" failed. skipping it")

    def filter_unsaved_keys(self,keys):
        db = DB()
        unsaved_keys = [key for key in keys if not db.search_key(key)]
        db.close()

        print("UNSAVED pasted bins:" + str(len(unsaved_keys)))
        return unsaved_keys

    def recent_pastes_keys(self):
        r = Request()
        parsed_html = r.parse(self.ARCHIVE_URL)
        if parsed_html is None:
            raise Exception("Unable to load url "+self.ARCHIVE_URL)

        main_table = parsed_html.body.find("table", {"class": "maintable"})
        keys_list = [paste_tag['href'] for paste_tag in main_table.findAll("a") if '/archive' not in paste_tag['href']]

        print("RECENT pasted bins:" + str(len(keys_list)))
        return keys_list