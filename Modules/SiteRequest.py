import requests
from bs4 import BeautifulSoup


class Request:
    def __init__(self):
        self.url = None
        self.response = None
        self.error = None

    def parse(self, url):
        try:
            self.response = requests.get(url)
        except Exception as e:
            print("Page loading error "+url)
            raise e

        if self.response.status_code == 401:
            print("Unauthorized error "+url)
            return None
        elif self.response.status_code == 404:
            print("Page not found error "+url)
            return None

        html = BeautifulSoup(self.response.text, features="html.parser")
        return html
