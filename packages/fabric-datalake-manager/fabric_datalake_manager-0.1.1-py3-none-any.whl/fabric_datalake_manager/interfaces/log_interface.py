from abc import ABC, abstractmethod

# ==========================================
# ILog Interface
# ==========================================

class ILog(ABC):
    @abstractmethod
    def log(self, message: str, **kwargs):
        raise NotImplementedError


class SlackLogger(ILog):
    def log(self, message: str):
        print(f"SlackLogger: {message}")
