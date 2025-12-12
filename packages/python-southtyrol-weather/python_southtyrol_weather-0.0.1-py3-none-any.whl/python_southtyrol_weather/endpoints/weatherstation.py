from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from typing import List, Literal, Type, TypeVar

from aiohttp import ClientSession

API_BASE_URL              = "https://tourism.api.opendatahub.com/v1/Weather/Realtime"
QUERY_PARAM_LANG          = "lang"
QUERY_PARAM_LATITUDE      = "latitude"
QUERY_PARAM_LONGITUDE     = "longitude"
QUERY_PARAM_RADIUS        = "radius"
QUERY_PARAM_FIELDS        = "fields"

NO_VALUE                  = "--"

class Category(Enum):
    VALLEY      = 1
    MOUNTAIN    = 2
    WATER_LEVEL = 3

class WindDirection(Enum):
    NONE        = "--"
    NORD        = "N"
    NORD_EAST   = "NE"
    EAST        = "E"
    SOUTH_EAST  = "SE"
    SOUTH       = "S"
    SOUTH_WEST  = "SW"
    WEST        = "W"
    NORD_WEST   = "NW"

class StationType(Enum):
    SNOW        = "1"
    WIND        = "2"

@dataclass
class WeatherStation:
    """Represents meta data of a single weatherstation."""
    id: str
    code: str
    name: str
    category: Category
    station_type: StationType
    latitude: float
    longitude: float
    altitude: int

    @staticmethod
    def from_json(json: dict):
        return WeatherStation(
            id = json["id"],
            code = json["code"],
            name = json["name"],
            category = get_enum(json, "categoryId", Category),
            station_type = get_enum(json, "lwdType", StationType),
            latitude = get_float(json, "latitude"),
            longitude = get_float(json, "longitude"),
            altitude = get_int(json, "altitude")
        )
    
@dataclass
class Measurement:
    """Represents data of a single measurement."""
    wind_direction: WindDirection
    wind_speed: float
    max_wind_speed: float
    precipitation: float
    airpressure: float
    relative_humidity: int
    temperature: float
    sunshine_duration: timedelta
    global_radiation: int
    snow_depth: float
    flow_rate: float
    water_level: int
    water_temperature: float
    last_updated: datetime

    @staticmethod
    def from_json(json: dict):
        return Measurement(
            wind_direction = get_enum(json, "dd", WindDirection),
            wind_speed = get_float(json, "ff"),
            max_wind_speed = get_float(json, "wMax"),
            precipitation = get_float(json, "n"),
            airpressure = get_float(json, "p"),
            relative_humidity = get_int(json, "rh"),
            temperature = get_float(json, "t"),
            sunshine_duration = get_timedelta(json, "sd"),
            global_radiation = get_int(json, "gs"),
            snow_depth = get_float(json, "hs"),
            flow_rate = get_float(json, "q"),
            water_level = get_int(json, "w"),
            water_temperature = get_float(json, "wt"),
            last_updated = get_timestamp(json, "lastUpdated")
        )

async def fetchStations(
        session: ClientSession,
        lang: Literal["de", "it", "en"] = "en",
        category: Category = None,
        latitude: float = None,
        longitude: float = None,
        radius: int = None
) -> List[WeatherStation]:
    query_params = [
        f"{QUERY_PARAM_FIELDS}=id,code,name,categoryId,lwdType,latitude,longitude,altitude"
    ]
    if lang != "en":
        query_params.append(f"{QUERY_PARAM_LANG}={lang}")
    if latitude is not None:
        query_params.append(f"{QUERY_PARAM_LATITUDE}={latitude}")
    if longitude is not None:
        query_params.append(f"{QUERY_PARAM_LONGITUDE}={longitude}")
    if radius is not None:
        query_params.append(f"{QUERY_PARAM_RADIUS}={radius}")
    query = "&".join(query_params)
    response = await session.get(f"{API_BASE_URL}?{query}")
    async with response:
        response.raise_for_status()
        text = await response.text()
        response_json = json.loads(text)
        stations = [WeatherStation.from_json(item) for item in response_json]
        if category is None:
            return stations
        return [s for s in stations if s.category == category]
            
async def fetchMeasurement(
    session: ClientSession,
    station_id: str,
    lang: Literal["de", "it", "en"] = "en"
) -> Measurement:
    query_params = [
        f"{QUERY_PARAM_FIELDS}=dd,ff,wMax,n,p,rh,t,sd,gs,hs,q,w,wt,lastUpdated"
    ]
    if (lang != "de"):
        query_params.append(f"{QUERY_PARAM_LANG}={lang}")
    query = "&".join(query_params)
    response = await session.get(f"{API_BASE_URL}/{station_id}?{query}")
    async with response:
        response.raise_for_status()
        text = await response.text()
        response_json = json.loads(text)
        return Measurement.from_json(response_json)

def get_float(json: dict, key: str, default: float = None) -> float:
    value = json.get(key)
    try:
        return float(value) if value is not None and value != NO_VALUE else default
    except (ValueError, TypeError):
        return default

def get_int(json: dict, key: str, default: int = None) -> int:
    value = json.get(key)
    try:
        return int(value) if value is not None and value != NO_VALUE else default
    except (ValueError, TypeError):
        return default

T = TypeVar("T", bound=Enum)

def get_enum(json: dict, key: str, type: Type[T], default: T = None) -> T:
    value = json.get(key)
    try:
        return type(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def get_timedelta(json: dict, key: str, default: timedelta = None) -> timedelta:
    value = json.get(key)
    try:
        hours, minutes = map(int, value.split(":"))
        return timedelta(hours=hours, minutes=minutes)
    except (ValueError, AttributeError):
        return default

def get_timestamp(json: dict, key: str, default: datetime = None) -> datetime:
    value = json.get(key)
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return default