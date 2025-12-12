from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

# ==========================
# Connection Classes
# ==========================
@dataclass
class MSSQLConnection:
    server: str
    database: str
    username: str
    password: str


@dataclass
class APIConnection:
    base_url: str
    auth_type: str
    username: Optional[str]
    password: Optional[str]
    token: Optional[str]


# ==========================
# Schedule Class
# ==========================
@dataclass
class BronzeScheduleEntity:
    table: str
    endpoint: Optional[str]
    fields: Optional[List[str]]
    where: Optional[str]
    params: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]
    status: bool = True


# ==========================
# Schedules
# ==========================
@dataclass
class BronzeScheduleEntities:
    frequency: str
    tables: List[BronzeScheduleEntity] = field(default_factory=list)
    status: bool = True


# ==========================
# Source Class
# ==========================
@dataclass
class BronzeSource:
    name: str
    type: str
    connection: APIConnection | MSSQLConnection
    schedules: List[BronzeScheduleEntities] = field(default_factory=list)


# ==========================
# Country Class
# ==========================
@dataclass
class BronzeCountry:
    name: str
    country_id: str
    sources: List[BronzeSource] = field(default_factory=list)
    status: bool = True
