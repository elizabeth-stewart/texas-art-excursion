from app.kimbell_art_museum import KimbellArtMuseum
from app.metadata.models import MuseumSearchResult


class TestKimbellArtMuseumUnit:
    def test_get_search_result_from_art_description(self):
        artwork_description_text = "Claude Monet, Weeping Willow, 1918-19"
        artwork_attributes = KimbellArtMuseum().get_artwork_attributes(artwork_description_text)

        expected_result = {
            "artist": "Claude Monet",
            "title": "Weeping Willow",
            "year": "1918-19"
        }

        assert artwork_attributes == expected_result