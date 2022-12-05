from typing import List
from typing import Iterator

from datetime import date

from bs4 import BeautifulSoup
from dateutil import relativedelta

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from spotifyScrapper_client import Song
#Minuto 48
#from spotifyScrapper_BBDD import SongService


baseURL = 'https://charts.spotify.com/charts/view/regional-global-weekly'
# countryList = ['cl', 'co', 'ar', 'pe', 'pr', 'uy', 've', 'ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']
countryList = ['ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']


class SpotifyScrapper:
    #Minuto 40
    def requestAndObtainTopSongs(self, country: str, date: str, driver) -> Iterator[Song]:
        driver.get(baseURL + '{}/daily/{}'.format(country, date))
        delay = 20
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-table')))
            generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
            songsList = generalDetails.find('table', {'class': 'chart-table'}) \
                            .find_all('tr')[1:]
            return map(
                lambda songRaw: self.parseSong(songRaw, country, date),
                songsList
            )

        except TimeoutException:
            print("Loading took too much time!")
            exit()

    #Minuto 30
    def parseSong(self, songRaw: BeautifulSoup, country: str, date: str) -> Song:
        nameAndArtist = songRaw.find('td', {'class': 'styled__Wrapper-sc-135veyd-14 gPJpnT"'})
        name = nameAndArtist.find('styled__StyledHyperlink-sc-135veyd-25 bVVLJU').getText() \
            .replace("\"", "") \
            .strip()
        artist = nameAndArtist.find('styled__StyledHyperlink-sc-135veyd-25 bVVLJU').getText() \
            .replace("by", "") \
            .replace("\"", "") \
            .strip()
        position = songRaw.find('td', {'class': 'ableCell__TableCellElement-sc-1nn7cfv-0 dLdEGj'}).getText()
        return Song(int(position), name, artist, date, country)


def generateMonthlyDateRange(startDate: date, endDate: date) -> List[date]:
    date_modified = startDate
    dateList = [startDate]

    while date_modified < endDate:
        date_modified += relativedelta.relativedelta(months=1)
        dateList.append(date_modified)

    return dateList

#minuto 35
dateRange = generateMonthlyDateRange(date(2019, 1, 1), date(2021, 8, 1))

driver = webdriver.Chrome(
    executable_path=r'C:/home/monica/Escritorio/PYTHON_Alberto/spotify/spotify_minadoDatos_baseDatos/chromedriver_linux64/chromedriver'
)

songService = SongService()


for country in countryList:
    for dateObj in dateRange:
        songs = list(SpotifyScrapper().requestAndObtainTopSongs(
            country,
            dateObj.strftime("%Y-%m-%d"),
            driver
        ))
        for song in songs:
            songService.save(song)


