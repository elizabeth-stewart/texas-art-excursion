from metadata.models import MuseumSearchResult
from metadata.museum_info import MuseumInfo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from typing import List
from webdriver_manager.chrome import ChromeDriverManager
import re


ON_VIEW_FILTER = "&f[0]=on_view:1"

class KimbellArtMuseum:
    """
    Kimbell Art Museum
    Fort Worth, TX
    """

    museum_info = MuseumInfo(
        street = "3333 Camp Bowie Boulevard",
        city = "Fort Worth",
        state = "TX",
        zip = "76107",
        website = "https://kimbellart.org/"
    )

    def __init__(self, base_url = "https://kimbellart.org/collection") -> None:
        self.base_url = base_url

    def run_search(self, artist: str, on_view_only: bool) -> List[MuseumSearchResult]:
        selenium_driver = self.get_selenium_driver()
        search_results = self.fetch_artwork_results(artist, self.get_search_url(artist, on_view_only), selenium_driver)
        selenium_driver.close()

        return search_results

    def fetch_artwork_results(self, artist: str, url: str, selenium_driver: webdriver.Chrome) -> List[MuseumSearchResult]:
        """
        Inputs:
            artist: search will do a case insensitive match for the entire string
                ex. "monet" will return results for "Claude Monet", "Monet, Claude", "Monet"
                    "claude monet" will return results for "Claude Monet" and NOT "Monet, Claude" or "Monet"
        """
        selenium_driver.get(url)

        elements = selenium_driver.find_elements(By.CLASS_NAME, "collection-teaser__text")

        search_results: List[MuseumSearchResult] = []

        for element in elements:
            # description will be in the form
            # artist, title, year(s)
            # multiple years will be something like 1918-19
            art_description = element.text

            if re.search(artist, art_description, re.IGNORECASE):
                artwork_attributes = self.get_artwork_attributes(art_description)
                link = self.get_artwork_link(element)
                search_results.append(
                    MuseumSearchResult(
                        artist=artwork_attributes["artist"],
                        title=artwork_attributes["title"],
                        year=artwork_attributes["year"],
                        link=link
                    )
                )

        return search_results
    
    def get_search_url(self, artist: str, on_view_only: bool) -> str:
        return f"{self.base_url}?keys={artist}{ON_VIEW_FILTER if on_view_only else ''}"

    def get_selenium_driver(self):
        options = Options()
        options.add_argument('--headless=new')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # TODO: need to rework this for things like "Edgar Degas, After the Bath, Woman Drying Her Hair, c. 1895"
    # The title is always in a <a href> element:
    # <div>Edgar Degas, <em><a href="/collection/ap-199504" rel="bookmark">After the Bath, Woman Drying Her Hair</a></em>, c. 1895</div>
    def get_artwork_attributes(self, artwork_description):
        artist, title, year = artwork_description.split(", ", 3)

        return {
            "artist": artist,
            "title": title,
            "year": year
        }

    def get_artwork_link(self, teaser_element):
        return teaser_element.find_element(By.XPATH, ".//a[@rel='bookmark']").get_attribute("href")


if __name__ == "__main__":
    search_results = KimbellArtMuseum().run_search("caravaggio", False)

    for search_result in search_results:
        search_result.print()