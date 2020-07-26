import requests
# import pprint
from bs4 import BeautifulSoup
import re
# import html2text


def get_headline(line, class_text):
    match = re.search(r'(<span class="%s">)(.*)(</span>)' % class_text, line)
    if match:
        return match.groups()[1]
    else:
        return None


class news():
    def __init__(self, URL_BASE, SECTION):
        self.URL_BASE = URL_BASE
        self.SECTION = SECTION

        URL = URL_BASE + SECTION
        page = requests.get(URL)
        # pprint(page.content)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())
        # print(soup.get_text())
        print('========================================================')
        for headline in soup.find_all('span'):
            hl = get_headline(str(headline), 'cd__headline-text')
            if hl:
                print(hl)
