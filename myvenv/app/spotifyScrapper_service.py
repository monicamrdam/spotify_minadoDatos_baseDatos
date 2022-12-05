


baseURL = 'https://charts.spotify.com/charts/overview/global'
#countryList = ['cl', 'co', 'ar', 'pe', 'pr', 'uy', 've', 'ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']
countryList = ['ec', 'pa', 'mx', 'hn', 'gt', 'cr', 'do', 'es']





class SpotifyScrapper:

    def requestAndObtainTopSongs(self, country: str, date: str, driver) -> Iterator[Song]:
        