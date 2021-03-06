import arrow
from Modules.TinyDB import DB
from Modules.SiteRequest import Request


class PastedBin:
    def __init__(self, site, key):
        self.site = site
        self.key = key
        self.author = ""
        self.title = ""
        self.date = ""
        self.content = ""

    def parse_paste(self):
        r = Request()
        parsed_html = r.parse(self.site+self.key)
        if parsed_html is None:
            return False

        title_tag = parsed_html.body.find("div", {"class": "paste_box_line1"})
        info_tag = parsed_html.body.find("div", {"class": "paste_box_line2"})

        success = self.html_field_extraction(title_tag, info_tag)
        return success

    def html_field_extraction(self, title_tag, info_tag):
        author = info_tag.find("a")
        if author is not None:
            self.author = author.text.strip(' \t\n\r')

        title = title_tag.text.strip(' \t\n\r')
        if title != 'Untitled':
            self.title = title

        date = info_tag.find("span")['title']
        self.date = arrow.get(date, 'dddd Do of MMMM YYYY HH:mm:ss A')

        r = Request()
        self.content = r.parse(self.site+'/raw'+self.key).text.strip(' ')
        if self.content is None:
            return False
        return True

    def save_paste(self):
        row = {
            'key': self.key,
            'title': self.title,
            'author': self.author,
            'date': str(self.date),
            'content': self.content
            }
        db = DB()
        db.insert(row)
        db.close()
