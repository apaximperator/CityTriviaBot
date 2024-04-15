import requests
import bs4
from tqdm import tqdm
import pickle
import pandas as pd

TOWNS_INFO_FILE = 'data/townsInfo.pickle'
TOWNS_FILE = 'data/towns.pickle'

HEADERS = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
}


class TownsInfoParser:

    def __init__(self, townUrls):
        self.townUrls = townUrls

    def parse(self):
        towersInfo = []
        for townUrl in tqdm(self.townUrls):
            page = bs4.BeautifulSoup(requests.get(townUrl, headers=HEADERS).text, 'lxml')
            page.select_one('#block-system-main .views-field span div b a').clear()

            continent = page.select_one('#block-system-main .views-field span div')
            if continent is None or continent.text == '':
                continent = ['continent', '-']
            else:
                continent = continent.text.lower().split(': ')

            country = page.select_one('#block-system-main [itemtype="http://schema.org/Country"]')
            if country is None or country.text == '':
                country = ['country', '-']
            else:
                country = country.text.lower().split(': ')

            state = page.select_one('#block-system-main [itemtype="http://schema.org/State"]')
            if state is None or state.text == '':
                state = ['state', '-']
            else:
                state = state.text.lower().split(': ')

            city = page.select_one('#block-system-main [itemtype="http://schema.org/City"]')
            if city is None or city.text == '':
                city = ['city', '-']
            else:
                city = city.text.lower().split(': ')

            population = page.select_one('#block-system-main .views-field-field-naselenie')
            if population is None or population.text == '':
                population = ['population', '-']
            else:
                population = population.text.lower().split(': ')

            square = page.select_one('#block-system-main .views-field-field-ploshad-goroda')
            if square is None or square.text == '':
                square = ['square', '-']
            else:
                square = square.text.lower().split(': ')

            founded = page.select_one('#block-system-main .views-field-field-god-osnov')
            if founded is None or founded.text == '':
                founded = ['city founded', '-']
            else:
                founded = founded.text.lower().split(': ')

            density = page.select_one('#block-system-main .views-field-field-plotnost')
            if density is None or density.text == '':
                density = ['city density', '-']
            else:
                density = density.text.lower().split(': ')

            agglomeration = page.select_one('#block-system-main .views-field-field-aglomeraciya')
            if agglomeration is None or agglomeration.text == '':
                agglomeration = ['agglomeration', '-']
            else:
                agglomeration = agglomeration.text.lower().split(': ')

            dayOfTheCity = page.select_one('#block-system-main .views-field-field-den-goroda')
            if dayOfTheCity is None or dayOfTheCity.text == '':
                dayOfTheCity = ['day of the city', '-']
            else:
                dayOfTheCity = dayOfTheCity.text.lower().split(': ')

            timeZone = page.select_one('#block-system-main .views-field-field-time-zone')
            if timeZone is None or timeZone.text == '':
                timeZone = ['time zone', '-']
            else:
                timeZone = timeZone.text.lower().split(': ')

            telCode = page.select_one('#block-system-main .views-field-field-tel-kod')
            if telCode is None or telCode.text == '':
                telCode = ['telephone code', '-']
            else:
                telCode = telCode.text.lower().split(': ')

            autoCode = page.select_one('#block-system-main .views-field-field-avto-kod')
            if autoCode is None or autoCode.text == '':
                autoCode = ['auto code', '-']
            else:
                autoCode = autoCode.text.lower().split(': ')

            postCode = page.select_one('#block-system-main .views-field-field-pocht-indeks')
            if postCode is None or postCode.text == '':
                postCode = ['post code', '-']
            else:
                postCode = postCode.text.lower().split(': ')

            towersInfo.append({
                continent[0].strip(): continent[1].strip(),
                country[0].strip(): country[1].strip(),
                state[0].strip(): state[1].strip(),
                city[0].strip(): city[1].strip(),
                population[0].strip(): population[1].strip(),
                square[0].strip(): square[1].strip(),
                founded[0].strip(): founded[1].strip(),
                density[0].strip(): density[1].strip(),
                agglomeration[0].strip(): agglomeration[1].strip(),
                dayOfTheCity[0].strip(): dayOfTheCity[1].strip(),
                timeZone[0].strip(): timeZone[1].strip(),
                telCode[0].strip(): telCode[1].strip(),
                autoCode[0].strip(): autoCode[1].strip(),
                postCode[0].strip(): postCode[1].strip(),
            })
        return towersInfo


def main():
    with open(TOWNS_FILE, 'rb') as f:
        town_urls_df = pickle.load(f)
    townUrls = list(town_urls_df.loc[:, 'TownUrl'])

    towersInfo: list[dict] = TownsInfoParser(townUrls).parse()
    town_info_df = pd.DataFrame(towersInfo)

    with open(TOWNS_INFO_FILE, 'wb') as f:
        pickle.dump(towersInfo, f)
        print(towersInfo)


if __name__ == '__main__':
    main()
