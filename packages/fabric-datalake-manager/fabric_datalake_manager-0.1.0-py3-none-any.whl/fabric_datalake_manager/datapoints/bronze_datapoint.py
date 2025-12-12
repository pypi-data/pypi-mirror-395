import requests
from requests.auth import HTTPBasicAuth

from typing import List, Dict

from pyspark.sql import DataFrame

from fabric_datalake_manager.enums.enum import EConnectionType, ELayer
from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig

from fabric_datalake_manager.loggers.logger_executor import LoggerExecutor
from fabric_datalake_manager.ingestion_models.app_config import Configuration
from fabric_datalake_manager.ingestion_models.connection_information import ConnectionInformation

from fabric_datalake_manager.dataclass.bronze_dataclass import BronzeScheduleEntity

# ==========================
# DataPointBronze Class
# ==========================


class DataPointBronze(IDataPoint):  # Layer Operation Like Read/Write
    def __init__(
        self,
        config: Configuration
    ):
        """
        :param dp: existing DataPoint instance to operate on
        :param lake_path: optional config path (default used if empty)
        """
        self.logger = LoggerExecutor(config.loggers)
        self.config: ILakeConfig = config.bronze.config
        self.layer = ELayer.BRONZE.value

    def read(
        self,
        country_name: str,
        source_name: str,
        table_name: str,
    ) -> DataFrame | None:
        """Read a parquet table if it exists, using the in-memory DataPoint instance."""

        if not self.config:
            raise ValueError(
                "No DataPoint instance provided to DataPointSilver")

        path = f"{self.config.path}/{self.layer}/{country_name}/{source_name}/{table_name}"

        try:
            # Try reading the Parquet file from the ADLS path
            df = spark.read.parquet(path)
            print(f"Successfully read parquet file at {path}")
            return df
        except Exception as e:
            # If the file doesn't exist or any other error occurs, log it and return None
            print(f"Failed to read parquet file at {path}: {e}")  # Debug print
            return None

    def write(
        self,
        country_name: str,
        source_name: str,
        table_name: str,
        data: DataFrame
    ) -> str:
        """Execute ingestion steps using all provided ingesters."""

        path = f"{self.config.path}/{self.layer}/{country_name}/{source_name}/{table_name}/"
        try:
            data.write.mode("overwrite").parquet(path)
            return path
        except Exception as e:
            print(f"Failed to write data to path {path}: {e}")
            message = (
                "*Data Ingestion Failed*\n"
                f"*Layer:* `{self.layer}`\n"
                f"*Country:* {country_name}\n"
                f"*Source:* {source_name}\n"
                f"*Table:* {table_name}\n"
                f"*Path:* `{path}`\n"
                f"*Status:* Failed\n"
                # f"*Error:* {str(e)}"
            )
            self.logger.log(message)
            return ""

    def sourceRead(
        self,
        connection_info: ConnectionInformation,
        item: BronzeScheduleEntity,
        query: str = None
    ) -> DataFrame | List[Dict] | Dict | None:

        data = None

        if connection_info.connection_type.value == EConnectionType.MSSQL.value and getattr(connection_info.connection, 'server', None):
            if not query:
                query = f"SELECT * FROM {item.table}"

            try:
                data = (
                    spark.read.format("jdbc")
                    .option(
                        "url",
                        f"jdbc:sqlserver://{connection_info.connection.server}:1433;"
                        f"databaseName={connection_info.connection.database};encrypt=true;trustServerCertificate=true"
                    )
                    .option("user", connection_info.connection.username)
                    .option("password", connection_info.connection.password)
                    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                    .option("dbtable", f"({query}) AS t")
                    .load()
                )

            except Exception as e:
                print(
                    f"An error occurred while reading data from the MSSQL server: {e}")

                # Log Trigger error message
                message = (
                    "*Data Source Read Failed*\n"
                    f"*Connection Type:* `{connection_info.connection_type.value}`\n"
                    f"*Connection Info:*\n"
                    f"  • Server: `{connection_info.connection.server}`\n"
                    f"  • Database: `{connection_info.connection.database}`\n"
                    f"  • Username: `{connection_info.connection.username}`\n"
                    f"  • Password: `{connection_info.connection.password}`\n"
                    f"*Table:* `{item.table}`\n"
                    f"*Status:* Failed\n"
                    # f"*Error:* {str(e)}"
                )
                self.logger.log(message)

        elif connection_info.connection_type.value == EConnectionType.REST_API.value:
            base_url = getattr(connection_info.connection, "base_url", None)
            if not base_url:
                print("No base_url provided for REST API connection.")
                return None

            auth = None
            headers = {}

            try:
                if hasattr(connection_info.connection, "auth_type"):
                    if connection_info.connection.auth_type == "Basic Auth":
                        auth = HTTPBasicAuth(
                            connection_info.connection.username, connection_info.connection.password)
                    elif connection_info.connection.auth_type == "Bearer" and getattr(connection_info.connection, "token", None):
                        headers["Authorization"] = f"Bearer {connection_info.connection.token}"

                # If no auth_type but username exists, assume Basic Auth
                if auth is None and getattr(connection_info.connection, "username", None):
                    auth = HTTPBasicAuth(
                        connection_info.connection.username, connection_info.connection.password)

                # Combine base_url + endpoint
                full_url = f"{base_url.rstrip('/')}/{item.endpoint.lstrip('/')}" if item.endpoint else base_url

                # Add query string
                if query:
                    if "?" in full_url:
                        full_url = f"{full_url}&{query}"
                    else:
                        full_url = f"{full_url}?{query}"

                response = requests.get(
                    full_url, auth=auth, headers=headers, verify=True)
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.HTTPError as e:
                print(
                    f"HTTP Error fetching REST API data for {item.table} at {full_url}: {e}")
                print(
                    f"Response status: {getattr(response, 'status_code', 'unknown')}")

                if getattr(response, "status_code", None) == 401:
                    print(f"Authentication failed. Check credentials for source.")

                # Log Trigger error message
                message = (
                    "*Data Source Read Failed*\n"
                    f"*Connection Type:* `{connection_info.connection_type.value}`\n"
                    f"*Connection Info:* {connection_info.connection}\n"
                    f"*Table:* {item.table}\n"
                    f"*Status:* Failed\n"
                    # f"*Error:* {str(e)}"
                )
                self.logger.log(message)

            except requests.exceptions.RequestException as e:
                print(
                    f"Error fetching REST API data for {item.table} at {base_url}: {e}")
                # Log Trigger error message
                message = (
                    "*Data Source Read Failed*\n"
                    f"*Connection Type:* `{connection_info.connection_type.value}`\n"
                    f"*Connection Info:* {connection_info.connection}\n"
                    f"*Table:* {item.table}\n"
                    f"*Status:* Failed\n"
                    # f"*Error:* {str(e)}"
                )
                self.logger.log(message)

            except Exception as e:
                print(
                    f"Unexpected error fetching REST API data for {item.table}: {e}")
                # Log Trigger error message
                message = (
                    "*Data Source Read Failed*\n"
                    f"*Connection Type:* `{connection_info.connection_type.value}`\n"
                    f"*Connection Info:*\n"
                    f"  • Base URL: `{connection_info.connection.base_url}`\n"
                    f"  • Database: `{connection_info.connection.database}`\n"
                    f"  • Username: `{connection_info.connection.username}`\n"
                    f"  • Password: `{connection_info.connection.password}`\n"
                    f"*Table:* `{item.table}`\n"
                    f"*Status:* Failed\n"
                    # f"*Error:* {str(e)}"
                )
                self.logger.log(message)

        else:
            print(
                f"Unsupported connection type: {connection_info.connection_type.value}")

        return data
