from abc import ABC, abstractmethod

from fabric_datalake_manager.dataclass.silver_dataclass import SilverScheduleEntity

from fabric_datalake_manager.ingestion_models.source_data import SourceData

# ==========================
# IValidate Class
# ==========================

class IValidate(ABC):
    """Interface for Data validate."""
    name: str

    @abstractmethod
    def validate(self, data: SourceData, item: SilverScheduleEntity) -> bool:
        """Perform validate logic using the data."""
        raise NotImplementedError
