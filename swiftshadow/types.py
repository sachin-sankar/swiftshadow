from typing import TypedDict


class MonosansNames(TypedDict):
    de: str
    en: str
    es: str
    fr: str
    ja: str
    pt_BR: str
    ru: str
    zh_CN: str


class MonosansContinent(TypedDict):
    code: str
    geoname_id: int
    names: MonosansNames


class MonosansCountry(TypedDict):
    geoname_id: int
    is_in_european_union: bool
    iso_code: str
    names: MonosansNames


class MonosansLocation(TypedDict):
    accuracy_radius: int
    latitude: float
    longitude: float
    time_zone: str


class MonosansGeolocation(TypedDict):
    continent: MonosansContinent
    country: MonosansCountry
    location: MonosansLocation
    registered_country: MonosansCountry


class MonosansProxyDict(TypedDict):
    protocol: str
    username: str | None
    password: str | None
    host: str
    port: int
    exit_ip: str
    timeout: float
    geolocation: MonosansGeolocation
