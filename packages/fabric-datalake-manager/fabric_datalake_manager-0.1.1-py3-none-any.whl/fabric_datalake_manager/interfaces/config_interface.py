from abc import ABC, abstractmethod

from fabric_datalake_manager.ingestion_models.app_config import Configuration

class ILakeConfig(ABC):
    pass


class IConfig(ABC):
    """Interface for Data configuration."""
    @abstractmethod
    def configure(self, config: Configuration):
        raise NotImplementedError
