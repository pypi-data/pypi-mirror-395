from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from fabric_datalake_manager.ingestion_models.source_data import SourceData
from fabric_datalake_manager.dataclass.silver_dataclass import SilverScheduleEntity

# ==========================
# ITransform Class
# ==========================

class ITransform(ABC):
    """Interface for Data ITransform."""
    name: str

    @abstractmethod
    def transform(self, data: SourceData, item: SilverScheduleEntity) -> DataFrame:
        """Perform transform logic using the data."""
        raise NotImplementedError
