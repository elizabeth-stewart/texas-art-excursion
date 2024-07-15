from pathlib import Path
from unittest import TestCase
from kimbell_art_museum import KimbellArtMuseum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestKimbellArtMuseumIntegration(TestCase):
    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')

        self.selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.local_html_file = f"file:///{Path(__file__).parent / 'data/kimbell_monet_no_filters.html'}"

    def test_fetch_artwork_results_returns_two_results_for_monet(self):
        kimbell = KimbellArtMuseum("path/to/collection")
        results = kimbell.fetch_artwork_results("monet", self.local_html_file, self.selenium_driver)

        assert len(results) == 2
        assert results[0].artist == "Claude Monet"
        assert results[0].title == "La Pointe de la Hève at Low Tide Test"
        assert results[0].year == "1865"
        assert results[0].link == "file:///collection/ap-196807"
        assert results[1].artist == "Claude Monet"
        assert results[1].title == "Weeping Willow Test"
        assert results[1].year == "1918–19"
        assert results[1].link == "file:///collection/ap-199602"

    def test_get_search_url_returns_url_for_monet_no_filter(self):
        kimbell = KimbellArtMuseum(base_url = "path/to/kimbell/collection")
        url = kimbell.get_search_url("monet", False)

        assert url == "path/to/kimbell/collection?keys=monet"

    def test_get_search_url_returns_url_for_monet_with_filter(self):
        kimbell = KimbellArtMuseum(base_url = "path/to/kimbell/collection")
        url = kimbell.get_search_url("monet", True)

        assert url == "path/to/kimbell/collection?keys=monet&f[0]=on_view:1"

    def test_run_search_returns_two_results_for_monet(self):
        kimbell = KimbellArtMuseum(self.local_html_file)
        results = kimbell.run_search("monet", False)

        assert len(results) == 2
        assert results[0].artist == "Claude Monet"
        assert results[0].title == "La Pointe de la Hève at Low Tide Test"
        assert results[0].year == "1865"
        assert results[0].link == "file:///collection/ap-196807"
        assert results[1].artist == "Claude Monet"
        assert results[1].title == "Weeping Willow Test"
        assert results[1].year == "1918–19"
        assert results[1].link == "file:///collection/ap-199602"

    def tearDown(self) -> None:
        self.selenium_driver.quit()