from enum import Enum


class ELayer(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    WH = "wh"


class EConnectionType(Enum):
    MSSQL = "mssql"
    REST_API = "rest_api"
