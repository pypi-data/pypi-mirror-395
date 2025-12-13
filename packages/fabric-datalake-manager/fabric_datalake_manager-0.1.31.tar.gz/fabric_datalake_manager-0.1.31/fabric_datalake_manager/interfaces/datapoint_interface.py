from abc import ABC, abstractmethod

# ==========================
# IDataPoint Classes
# ==========================

class IDataPoint(ABC):
    @abstractmethod
    def read(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def write(self, output_path: str) -> None:
        raise NotImplementedError
