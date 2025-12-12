import math
from dataclasses import dataclass

from astropy.coordinates import EarthLocation

@dataclass
class Location:
    LON: float
    LAT: float
    ELE: int

LOCATION: Location = Location(
    -0.31203578143571958,
    0.50199547796805788,
    2400
)

MyEarthLocation = EarthLocation.from_geodetic(
    LOCATION.LON / math.pi * 180,
    LOCATION.LAT / math.pi * 180,
    LOCATION.ELE
)