from app.kimbell_art_museum import KimbellArtMuseum

class TestKimbellArtMuseumE2E:
    def test_monet_on_view_filter_unchecked(self):
        search_results = KimbellArtMuseum().run_search("monet", False)

        assert len(search_results) == 2

    def test_monet_on_view_filter_checked(self):
        search_results = KimbellArtMuseum().run_search("monet", True)

        assert len(search_results) == 2