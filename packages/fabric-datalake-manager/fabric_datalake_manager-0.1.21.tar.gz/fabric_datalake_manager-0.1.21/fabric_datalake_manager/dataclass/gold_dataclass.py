from typing import List, Optional
from dataclasses import dataclass, field

# ==========================
# GoldScheduleEntity
# ==========================
@dataclass
class GoldScheduleEntity:
    table: str
    upsert_columns: Optional[List[str]]
    status: bool

# ==========================
# GoldScheduleEntities
# ==========================


@dataclass
class GoldScheduleEntities:
    frequency: str
    status: bool
    tables: List[GoldScheduleEntity] = field(default_factory=list)
