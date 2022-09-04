from typing import Optional
import requests
from bs4 import BeautifulSoup
from grappa import expect
from http import HTTPStatus
from urllib.parse import urljoin


HeadlineDictType = dict[str, list[str]]


class HeadlineList():
    """ Used for printing list of headlines """

    def __init__(self, headline_list: list[str]):
        self.headlines = headline_list

    def __str__(self) -> str:
        text = "".join(
            [f"- {headline}\n" for headline in self.headlines]).rstrip('/n')
        if not text:
            text = "No results. "
        return text

    def __repr__(self) -> str:
        return self.__str__


class HeadlineDict():
    """ Used for printing a dictionary of header - headline list values """

    def __init__(self, headline_dict: HeadlineDictType):
        self.headline_dict = headline_dict

    def __str__(self) -> str:
        text = ""
        for header, headlines in self.headline_dict.items():
            text += f"{header}\t" + "-" * 20 + '\n'
            text += str(headlines)
        return text

    def __repr__(self) -> str:
        return self.__str__


class news():
    def __init__(self, url_base: str = "https://edition.cnn.com", filtering: Optional[bool] = False):
        if not url_base.startswith("http"):
            url_base = "https://" + url_base
        self.URL_BASE = url_base
        self.URL = self.URL_BASE  # this can be overwritten with self.set_section()
        self.set_filtering(filtering)
        self.set_filters()

    def set_filtering(self, filtering: bool) -> None:
        self.filtering = filtering

    def set_filters(self, filter_list: list[str] = []) -> None:
        default_filters = ["world", "europe", "business"]
        self.section_filter = filter_list if filter_list else default_filters

    @property
    def page(self) -> requests.Response:
        try:
            response = requests.get(self.URL)
            expect(response.status_code).to.equal(HTTPStatus.OK)
            return response
        except ConnectionError:
            print(f"Connection refused: {self.URL = }")
            return None

    @property
    def soup(self) -> "BeautifulSoup":
        return BeautifulSoup(self.page.content, 'html.parser')

    @property
    def section_list(self) -> list[str]:
        return [header_tag["href"] for header_tag in self.soup.find_all('a', attrs={"data-analytics": "footer"}) if header_tag["href"].startswith('/')]

    def set_section(self, section: str) -> str:
        self.URL = urljoin(self.URL_BASE, section)

    def get_headlines(self) -> HeadlineList:
        return HeadlineList([headline.text for headline in self.soup.find_all("span", {"class": "cd__headline-text"})])

    @property
    def section(self) -> str:
        return self.URL.rsplit('.com/')[-1]

    @property
    def headline_dict(self) -> HeadlineDict:
        headline_dict = {}

        self.set_section("")  # homepage
        headline_dict.update({"homepage": self.get_headlines()})

        for section in self.section_list:
            self.set_section(section)
            if not self.section_filter or self.section in self.section_filter:
                hl = self.get_headlines()
                if hl:
                    headline_dict.update({self.section: hl})
        return HeadlineDict(headline_dict)

    @property
    def all_headlines(self) -> HeadlineList:
        high_list = self.headline_dict.headline_dict.values()
        return HeadlineList([item for sublist in high_list for item in sublist.headlines])

    def search_for_keyword(self, keyword: str) -> HeadlineList:
        print(f"Results for '{keyword}': ")
        return HeadlineList(list(filter(lambda x: keyword.lower() in x.lower(), self.all_headlines.headlines)))


if __name__ == '__main__':
    cnn = news(filtering=True)
    print(cnn.headline_dict)
    print(cnn.search_for_keyword("Russia"))
