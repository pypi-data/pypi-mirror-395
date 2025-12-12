from typing import List, Optional

from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from com.microsoft.spark.fabric import *
from com.microsoft.spark.fabric.Constants import Constants

from fabric_datalake_manager.enums.enum import ELayer
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig
from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint

from fabric_datalake_manager.ingestion_models.app_config import Configuration
from fabric_datalake_manager.loggers.logger_executor import LoggerExecutor

# ==========================
# DataPointWarehouse Class
# ==========================


class DataPointWH(IDataPoint):
    def __init__(
        self,
        config: Configuration
    ):
        """
        :param dp: existing DataPoint instance to operate on
        :param json_path: optional config path (default used if empty)
        """
        self.logger = LoggerExecutor(config.loggers)
        self.config: ILakeConfig = config.gold.config
        self.wh_name = config.wh_name
        self.layer = ELayer.WH.value

    def read(
        self,
        table_name: str = None,
        query: str = None
    ) -> DataFrame | None:
        """
        Read table from Synapse SQL with all conditions in one chained statement.

        Args:
            table_name: Name of the table or view
            query: T-SQL query (e.g., SELECT * FROM table_name)
        """
        if not self.wh_name:
            raise ValueError("No warehouse found")

        if not table_name and not query:
            raise ValueError("Either table_name or query must be provided")

        try:
            # Build query
            if not query:
                query = f"SELECT * FROM {table_name}"

            df = spark.read.option(
                Constants.DatabaseName, self.wh_name).synapsesql(query)
            return df

        except Exception as e:
            if query:
                print(f"Failed to execute query: {query}\nError: {e}")
            else:
                print(f"Failed to read table {table_name}: {e}")

    def write(
        self,
        table_name: str,
        data: DataFrame,
        schema_name: str = "dbo",
        mode: str = "append",
        merge_keys: Optional[List[str]] = None
    ) -> str:

        full_table_name = f"{self.wh_name}.{schema_name}.{table_name}"

        try:
            # =======================================================
            # UPSERT (DELETE + INSERT based on merge keys)
            # =======================================================
            if merge_keys:
                # TO DO
                # UPSERT Process
                data.write.mode("append").synapsesql(full_table_name)
            else:
                # Write new data
                data.write.mode("append").synapsesql(full_table_name)

            return full_table_name

        except Exception as e:
            print(
                f"Failed to write data to warehouse table {full_table_name}: {e}")

            message = (
                "*Data Write on Warehouse Failed*\n"
                f"*Layer:* `{self.layer}`\n"
                f"*Warehouse:* `{self.wh_name}`\n"
                f"*Schema:* `{schema_name}`\n"
                f"*Table:* `{table_name}`\n"
                f"*Mode:* `{mode}`\n"
                f"*Status:* Failed`\n"
                f"*Error:* `{str(e)}`"
            )
            self.logger.log(message)
            return ""
