import arrow
from Modules.TinyDB import *
from Modules.SiteRequest import *

class PastedBin:
    def __init__(self,site,key):
        self.site = site
        self.key = key
        self.author = ""
        self.title = ""
        self.date = ""
        self.content = ""

    def import_pasted_bin(self):
        r = Request()
        parsed_html = r.parse_html(self.site+self.key)
        if parsed_html is None:
            return False
        title_tag = parsed_html.body.find("div", {"class": "paste_box_line1"})
        info_tag = parsed_html.body.find("div", {"class": "paste_box_line2"})

        self.html_field_extraction(title_tag,info_tag)
        return True

    def html_field_extraction(self, title_tag, info_tag):
        author = info_tag.find("a")
        if author is not None:
            self.author=author.text.strip(' \t\n\r')

        title = title_tag.text.strip(' \t\n\r')
        if title != 'Untitled':
            self.title = title

        date = info_tag.find("span")['title']
        self.date = arrow.get(date,'dddd Do of MMMM YYYY HH:mm:ss A')

        self.content = requests.get(self.site+'/raw'+self.key).text.strip(' ')

    def save_pasted_bin_to_db(self):
        row = {
            'key': self.key,
            'title': self.title,
            'author': self.author,
            'date': str(self.date),
            'content': self.content
            }
        db = DB().get_handle()
        db.insert(row)
        db.close()