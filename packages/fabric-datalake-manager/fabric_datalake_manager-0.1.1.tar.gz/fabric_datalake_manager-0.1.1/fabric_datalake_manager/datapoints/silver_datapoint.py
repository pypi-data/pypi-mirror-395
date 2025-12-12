from typing import List

from pyspark.sql import DataFrame

from fabric_datalake_manager.enums.enum import ELayer
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig
from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint

from fabric_datalake_manager.ingestion_models.app_config import Configuration
from fabric_datalake_manager.loggers.logger_executor import LoggerExecutor


# ==========================
# DataPointSilver Class
# ==========================

class DataPointSilver(IDataPoint):
    def __init__(
        self,
        config: Configuration
    ):
        """
        :param dp: existing DataPoint instance to operate on
        :param json_path: optional config path (default used if empty)
        """
        self.logger = LoggerExecutor(config.loggers)
        self.config: ILakeConfig = config.silver.config
        self.layer = ELayer.SILVER.value

    def read(
        self,
        table_name: str,
        partition_paths: List[str] = None,
    ) -> DataFrame | None:
        """Read a parquet table if it exists, using the in-memory DataPoint instance."""

        if not self.config:
            raise ValueError(
                "No DataPoint instance provided to DataPointSilver")

        base_path = f"{self.config.path}/{self.layer}/{table_name}"

        try:
            # If partition subpaths were provided, construct full paths
            if partition_paths:
                full_paths = [f"{base_path}/{p}" for p in partition_paths]
                df = spark.read.parquet(*full_paths)

            else:
                df = spark.read.parquet(base_path)

            print(f"Successfully read parquet table '{table_name}'")
            return df

        except Exception as e:
            # If the file doesn't exist or any other error occurs, log it and return None
            print(f"Failed to read parquet file at {base_path}: {e}")  # Debug print
            return None

    def write(
        self,
        table_name: str,
        data: DataFrame,
        partitions: List[str] = None,
    ) -> str:
        """Execute ingestion steps using all provided ingesters."""

        path = f"{self.config.path}/{self.layer}/{table_name}/"

        try:
            writer = data.write.mode("overwrite")

            # Apply dynamic partitioning if partitions exist
            if partitions:
                writer = writer.partitionBy(partitions)

            writer.parquet(path)
            return path

        except Exception as e:
            print(f"Failed to write data to path {path}: {e}")

            message = (
                "*Data Ingestion Failed*\n"
                f"*Layer:* `{self.layer}`\n"
                f"*Table:* `{table_name}`\n"
                f"*Path:* `{path}`\n"
                f"*Status:* Failed\n"
            )

            self.logger.log(message)
            return ""
