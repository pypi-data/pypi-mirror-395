from abc import ABC, abstractmethod
from typing import List

from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint

from fabric_datalake_manager.ingestion_models.ingested_data import IngestedData

# ==========================
# IIngest Class
# ==========================


class IIngest(ABC):
    """Interface for ingestion operations."""

    @abstractmethod
    def ingest(
        self,
        source_layer: IDataPoint,
        destination_layer: IDataPoint = None
    ) -> List[IngestedData]:
        """Perform ingestion logic using the provided DataPoint object."""
        raise NotImplementedError
