from fabric_datalake_manager.enums.enum import EConnectionType

from fabric_datalake_manager.dataclass.bronze_dataclass import APIConnection, MSSQLConnection

# ==========================
# ConnectionInformation Class
# ==========================


class ConnectionInformation:
    def __init__(
        self,
        connection_type: EConnectionType,
        connection: APIConnection | MSSQLConnection
    ):
        self.connection_type = connection_type
        self.connection = connection
