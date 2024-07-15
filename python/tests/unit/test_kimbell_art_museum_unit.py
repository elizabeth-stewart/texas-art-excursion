from unittest.mock import Mock, patch
from kimbell_art_museum import KimbellArtMuseum
from metadata.models import MuseumSearchResult


class TestKimbellArtMuseumUnit:
    def test_fetch_artwork_results_loads_html_file_using_selenium(self):
        selenium_driver = Mock()
        selenium_driver.find_elements.return_value = []

        local_html_file = "path/to/website"

        kimbell = KimbellArtMuseum()
        kimbell.fetch_artwork_results("", local_html_file, selenium_driver)
        
        selenium_driver.get.assert_called_with(local_html_file)

    def test_get_search_result_from_art_description(self):
        artwork_description_text = "Claude Monet, Weeping Willow, 1918-19"
        artwork_attributes = KimbellArtMuseum("path/to/collection").get_artwork_attributes(artwork_description_text)

        expected_result = {
            "artist": "Claude Monet",
            "title": "Weeping Willow",
            "year": "1918-19"
        }

        assert artwork_attributes == expected_result

    @patch("kimbell_art_museum.KimbellArtMuseum.fetch_artwork_results")
    @patch("kimbell_art_museum.webdriver.Chrome")
    def test_run_search_returns_museum_search_results(self, mock_selenium_driver, mock_fetch_artwork_results):
        mock_fetch_artwork_results.return_value = [
            MuseumSearchResult(
                artist="Claude Monet",
                title="La Pointe de la Hève at Low Tide Test",
                year="1865",
                link="file:///collection/ap-196807"
            )
        ]
        kimbell = KimbellArtMuseum("path/to/collection")
        search_results = kimbell.run_search("monet", False)

        assert len(search_results) == 1
        assert search_results[0].artist == "Claude Monet"
        assert search_results[0].title == "La Pointe de la Hève at Low Tide Test"
        assert search_results[0].year == "1865"
        assert search_results[0].link == "file:///collection/ap-196807"
