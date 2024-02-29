from dataclasses import dataclass


@dataclass
class MuseumInfo:
    street: str
    city: str
    state: str
    zip: str
    website: str
