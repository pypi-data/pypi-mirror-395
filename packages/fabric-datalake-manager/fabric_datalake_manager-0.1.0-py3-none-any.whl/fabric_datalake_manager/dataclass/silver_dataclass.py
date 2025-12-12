from typing import List, Optional, Dict
from dataclasses import dataclass, field

# ==========================
# ScheduleItem equivalent
# ==========================
@dataclass
class SilverScheduleEntity:
    table: Optional[str] = None
    map_table: Optional[str] = None
    mapping: Dict[str, str] = field(default_factory=dict)
    partitions: List[str] = field(default_factory=list)
    status: bool = True


# ==========================
# Schedules
# ==========================
@dataclass
class SilverScheduleEntities:
    frequency: str
    tables: List[SilverScheduleEntity] = field(default_factory=list)
    status: bool = True


# ==========================
# Source
# ==========================
@dataclass
class SilverSource:
    name: Optional[str] = None
    schedules: List[SilverScheduleEntities] = field(default_factory=list)
    status: bool = True


# ==========================
# Country
# ==========================
@dataclass
class SilverCountry:
    name: Optional[str] = None
    sources: List[SilverSource] = field(default_factory=list)
    status: bool = True
