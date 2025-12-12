from datetime import date, datetime, time
from marvel_schedule_maker.utils.LocationConfig import MyEarthLocation

import astroplan
import astropy.units as units
from astropy.time import Time as AstroTime
from astropy.coordinates import get_sun
from astropy.utils import iers
from astropy.utils.data import download_file
from astropy.utils.iers import conf

conf.auto_download = True     # try online
conf.auto_max_age = 30        # allow cached file up to 30 days old

try:
    iers_a = iers.IERS_Auto.open()
except Exception as e:
    print(f"Warning: using offline IERS data ({e})")
    iers_a = iers.IERS_B.open()



class TwilightHorizons:
    """Horizon angles for twilight calculations."""
    CIVIL = -6  # Sun 6° below horizon
    NAUTICAL = -12  # Sun 12° below horizon
    ASTRONOMICAL = -18  # Sun 18° below horizon

class ObservationDateModel:
    """Observation date and twilight time calculator."""

    def __init__(self):
        self._observation_date = datetime.now().date()
        self._civil_twilight_start: datetime = None   # type: ignore[assignment]
        self._civil_twilight_end: datetime = None   # type: ignore[assignment]
        self._astronomical_twilight_start: datetime = None   # type: ignore[assignment]
        self._astronomical_twilight_end: datetime = None     # type: ignore[assignment]
        self._calculate_twilight_times()

    @property
    def observation_date(self) -> date:
        return self._observation_date

    @property
    def civil_twilight_start(self) -> datetime:
        return self._civil_twilight_start

    @property
    def civil_twilight_end(self) -> datetime:
        return self._civil_twilight_end

    @property
    def astronomical_twilight_start(self) -> datetime:
        return self._astronomical_twilight_start

    @property
    def astronomical_twilight_end(self) -> datetime:
        return self._astronomical_twilight_end
    
    def set_date(self, new_date: date) -> None:
        """Set new observation date and recalculate twilight times."""
        self._observation_date = new_date
        self._calculate_twilight_times()

    def _calculate_twilight_times(self):
        observer = astroplan.Observer(MyEarthLocation)
        late_time = AstroTime(datetime.combine(self._observation_date, time(23, 59, 59)))
        target = get_sun(late_time)

        self._civil_twilight_start = observer.target_set_time(late_time, target, "nearest", TwilightHorizons.CIVIL * units.degree).to_datetime() # type: ignore[assignment]
        self._civil_twilight_end = observer.target_rise_time(late_time, target, "nearest", TwilightHorizons.CIVIL * units.degree).to_datetime() # type: ignore[assignment]
        self._astronomical_twilight_start = observer.target_set_time(late_time, target, "nearest", TwilightHorizons.ASTRONOMICAL * units.degree).to_datetime() # type: ignore[assignment]
        self._astronomical_twilight_end = observer.target_rise_time(late_time, target, "nearest", TwilightHorizons.ASTRONOMICAL * units.degree).to_datetime() # type: ignore[assignment]
