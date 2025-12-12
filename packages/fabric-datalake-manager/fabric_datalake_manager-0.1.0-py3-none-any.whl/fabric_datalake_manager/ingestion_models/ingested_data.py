from pyspark.sql import DataFrame

from fabric_datalake_manager.dataclass.bronze_dataclass import BronzeScheduleEntity
from fabric_datalake_manager.dataclass.silver_dataclass import SilverScheduleEntity
from fabric_datalake_manager.dataclass.gold_dataclass import GoldScheduleEntity

# ==========================
# IngestedData Class
# ==========================


class IngestedData:
    def __init__(
        self,
        item: BronzeScheduleEntity | SilverScheduleEntity | GoldScheduleEntity,
        data: DataFrame,
        country_name: str = None,
        source_name: str = None,
    ):
        self.country_name = country_name
        self.source_name = source_name
        self.item = item
        self.data = data
