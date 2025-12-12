import re
from typing import List

from com.microsoft.spark.fabric import *
from com.microsoft.spark.fabric.Constants import Constants

from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

from delta.tables import DeltaTable

from fabric_datalake_manager.enums.enum import ELayer
from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig

from fabric_datalake_manager.ingestion_models.app_config import Configuration
from fabric_datalake_manager.loggers.logger_executor import LoggerExecutor

# ==========================
# DataPointGold Class
# ==========================

class DataPointGold(IDataPoint):
    def __init__(
        self,
        config: Configuration
    ):
        """
        :param dp: existing DataPoint instance to operate on
        :param json_path: optional config path (default used if empty)
        """
        self.spark = SparkSession.builder.getOrCreate()

        self.logger = LoggerExecutor(config.loggers)
        self.config: ILakeConfig = config.gold.config
        self.layer = ELayer.GOLD.value

    def read(
        self,
        table_name: str = None,
        query: str = None
    ) -> DataFrame | None:
        """Read a parquet table if it exists, using the in-memory DataPoint instance."""

        if not self.config:
            raise ValueError("No DataPoint instance provided to DataPointGold")

        lakehouse_name = self._extract_lakehouse_name()
        if not lakehouse_name:
            raise ValueError("No lakehouse found")

        if not table_name and not query:
            raise ValueError("Either table_name or query must be provided")

        df: DataFrame = None
        try:
            # Build query
            if not query:
                query = f"SELECT * FROM {table_name}"

            df = spark.read.option(
                Constants.DatabaseName, lakehouse_name).synapsesql(query)
            return df

        except Exception as e:
            if query:
                print(f"Failed to execute query: {query}\nError: {e}")
            else:
                print(f"Failed to read table {table_name}: {e}")

        return df

    def write(
        self,
        table_name: str,
        data: DataFrame,
        merge_keys: List[str] = None
    ) -> str:
        """Execute ingestion steps using all provided ingesters."""

        path = self.config.path.replace("Files", "Tables")
        table_path = f"{path}/{table_name}"

        try:
            # Check if table exists at the path
            if DeltaTable.isDeltaTable(self.spark, table_path):
                # Load DeltaTable object (missing in your code!)
                delta_table = DeltaTable.forPath(self.spark, table_path)

                if merge_keys:
                    # Build merge condition
                    merge_condition = " AND ".join(
                        [f"target.{col} = source.{col}" for col in merge_keys])

                    delta_table.alias("target").merge(
                        data.alias("source"),
                        merge_condition
                    ).whenMatchedUpdateAll() \
                        .whenNotMatchedInsertAll() \
                        .execute()
                else:
                    # No merge keys → append
                    # data.write.format("delta").mode("append").save(table_path)
                    data.write.format("delta").mode(
                        "overwrite").save(table_path)
            else:
                # Table doesn't exist → create it
                data.write.format("delta").mode("overwrite").save(table_path)

            return table_path

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

    def _extract_lakehouse_name(self) -> str:
        match = re.search(r'/([^/]+)\.Lakehouse', self.config.path)
        return match.group(1) if match else None

    def _apply_schema(self, df: DataFrame, schema):
        for field in schema.fields:
            if field.name in df.columns:
                df = df.withColumn(field.name, col(
                    field.name).cast(field.dataType))
        return df
