from dataclasses import dataclass


@dataclass
class MuseumSearchResult:
    artist: str
    title: str
    year: str
    link: str

    def print(self):
        print(
            f"Artist: {self.artist}\n"
            f"Title: {self.title}\n"
            f"Year: {self.year}\n"
            f"Link: {self.link}"
        )
