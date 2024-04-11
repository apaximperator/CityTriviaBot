import requests
import bs4
from tqdm import tqdm
import pickle
import pandas as pd

url = 'https://geogoroda.ru/bukva'
urlCore = 'https://geogoroda.ru'
TOWNS_FILE = 'data/towns.pickle'

HEADERS = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
}


class GeoParser:
    def __init__(self, url):
        self.url = url

    def _getMainLettersUrls(self) -> list[str]:  # alphabet urls
        page = bs4.BeautifulSoup(requests.get(self.url, headers=HEADERS).text, 'lxml')
        letters = page.select('#first > div:nth-child(2) > h4 > a')
        return [urlCore + letter['href'] for letter in letters]

    def _getAllLettersUrls(self) -> list[str]:
        listUrls = []
        for mainLetterUrl in self._getMainLettersUrls():
            page = bs4.BeautifulSoup(requests.get(mainLetterUrl, headers=HEADERS).text,
                                     'lxml')
            lastPage = page.select_one('a[title="На последнюю страницу"]')
            if lastPage is None:
                print(mainLetterUrl)
                listUrls += [mainLetterUrl]
            else:
                lastPageNum: int = int(lastPage['href'].split('page=')[-1])
                listUrls += [f"{mainLetterUrl}?page={i}" for i in range(lastPageNum + 1)]
        return listUrls

    def getTownsUrls(self):
        townUrls = []
        for pageUrl in tqdm(self._getAllLettersUrls()):
            page = bs4.BeautifulSoup(requests.get(pageUrl, headers=HEADERS).text,
                                     'lxml')
            towns = page.select('.views-field.views-field-title.large a')
            townUrls += [urlCore + town['href'] for town in towns]
        return townUrls


def main():
    parser = GeoParser(url)
    df = pd.DataFrame({'TownUrl': parser.getTownsUrls()})

    with open(TOWNS_FILE, 'wb') as f:
        pickle.dump(df, f)

    with open(TOWNS_FILE, 'rb') as f:
        df = pickle.load(f)

    print(df)


if __name__ == '__main__':
    main()
