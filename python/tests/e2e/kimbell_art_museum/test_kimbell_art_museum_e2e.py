from kimbell_art_museum import KimbellArtMuseum

class TestKimbellArtMuseumE2E:
    def test_monet_on_view_filter_unchecked(self):
        results = KimbellArtMuseum().run_search("monet", False)

        assert len(results) == 2
        assert results[0].artist == "Claude Monet"
        assert results[0].title == "La Pointe de la Hève at Low Tide"
        assert results[0].year == "1865"
        assert results[0].link == "https://kimbellart.org/collection/ap-196807"
        assert results[1].artist == "Claude Monet"
        assert results[1].title == "Weeping Willow"
        assert results[1].year == "1918–19"
        assert results[1].link == "https://kimbellart.org/collection/ap-199602"

    def test_monet_on_view_filter_checked(self):
        results = KimbellArtMuseum().run_search("monet", True)

        assert len(results) == 2
        assert results[0].artist == "Claude Monet"
        assert results[0].title == "La Pointe de la Hève at Low Tide"
        assert results[0].year == "1865"
        assert results[0].link == "https://kimbellart.org/collection/ap-196807"
        assert results[1].artist == "Claude Monet"
        assert results[1].title == "Weeping Willow"
        assert results[1].year == "1918–19"
        assert results[1].link == "https://kimbellart.org/collection/ap-199602"
