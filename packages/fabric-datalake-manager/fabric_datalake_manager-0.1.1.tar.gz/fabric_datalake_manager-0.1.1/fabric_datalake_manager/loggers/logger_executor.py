from typing import List

from fabric_datalake_manager.interfaces.log_interface import ILog

# ==========================================
# Execute Logs
# ==========================================
class LoggerExecutor:

    def __init__(self, loggers: List[ILog] = None):
        self.loggers = loggers

    def log(self, message: str, **kwargs) -> None:
        """
        Logs a message through all configured loggers safely.
        """

        for logger in self.loggers:
            try:
                logger.log(message, **kwargs)
            except Exception as e:
                print(
                    f"[LoggerExecutor] Error while logging with {logger.__class__.__name__}: {e}")
