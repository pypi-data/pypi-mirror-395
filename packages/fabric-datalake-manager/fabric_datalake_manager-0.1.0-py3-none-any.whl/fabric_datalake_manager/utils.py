from typing import List
from pyspark.sql import DataFrame, functions as F

from fabric_datalake_manager.enums.enum import ELayer
from fabric_datalake_manager.interfaces.config_interface import IConfig
from fabric_datalake_manager.interfaces.ingest_interface import IIngest
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig
from fabric_datalake_manager.interfaces.datapoint_interface import IDataPoint

from fabric_datalake_manager.loggers.logger_executor import LoggerExecutor
from fabric_datalake_manager.ingestion_models.app_config import Configuration

from fabric_datalake_manager.datapoints.bronze_datapoint import DataPointBronze
from fabric_datalake_manager.datapoints.silver_datapoint import DataPointSilver
from fabric_datalake_manager.datapoints.gold_datapoint import DataPointGold
from fabric_datalake_manager.datapoints.warehouse_datapoint import DataPointWH


# ==========================
# DataLakeManager Class
# ==========================

class DataLakeManager:
    """Manager class for orchestrating DataPointBronze ingestion."""

    def __init__(
        self,
        config: IConfig,
        ingester: List[IIngest] = None
    ):
        # Create Configuration instance and let AppConfig configure it
        self.configuration = Configuration()
        config.configure(self.configuration)

        self.ingester = ingester or []

        if self.configuration.bronze:
            self.bronze: IDataPoint = DataPointBronze(
                config=self.configuration)

        if self.configuration.silver:
            self.silver: IDataPoint = DataPointSilver(
                config=self.configuration)

        if self.configuration.gold:
            self.gold: IDataPoint = DataPointGold(config=self.configuration)

        if self.configuration.wh_name and self.configuration.gold:
            self.wh: IDataPoint = DataPointWH(config=self.configuration)

        self.logger = LoggerExecutor(self.configuration.loggers)

    def read(
        self,
        layer: ELayer,
        table_name: str = None,
        country_name: str = None,
        source_name: str = None,
        query: str = None,
        partition_paths: List[str] = None,
    ) -> DataFrame | None:
        print("Reading from Lakehouse / Warehouse")

        data = None
        try:
            if layer.value == ELayer.BRONZE.value:
                data = self.bronze.read(
                    country_name=country_name,
                    source_name=source_name,
                    table_name=table_name,
                )
            elif layer.value == ELayer.SILVER.value:
                data = self.silver.read(
                    table_name=table_name,
                    partition_paths=partition_paths
                )
            elif layer.value == ELayer.GOLD.value:
                data = self.gold.read(
                    table_name=table_name,
                    query=query,
                )
            elif layer.value == ELayer.WH.value:
                data = self.wh.read(
                    table_name=table_name,
                    query=query
                )
        except Exception as e:
            print(f"Got an error during read from lakehouse: {e}")

        return data

    def write(self, layer: ELayer) -> None:
        if not self.ingester:
            print("\nDataLakeManager: No ingester found or ingester is empty.")
            return

        for ing in self.ingester:
            try:
                if layer.value == ELayer.BRONZE.value:
                    print(
                        f"\nStarting ingestion for {ing.__class__.__name__} on BRONZE layer.")
                    dfr = ing.ingest(
                        source_layer=self.bronze
                    )
                    if dfr:
                        for dfr_item in dfr:
                            try:
                                country_id = self._get_country_id(
                                    layer_config=self.bronze.config,
                                    country_name=dfr_item.country_name
                                )
                                if country_id:
                                    if "country_id" in dfr_item.data.columns:
                                        # Only fill NULL rows with correct country_id
                                        dfr_item.data = dfr_item.data.withColumn("country_id", F.when(
                                            F.col("country_id").isNull(), F.lit(country_id)).otherwise(F.col("country_id")))
                                    else:
                                        dfr_item.data = dfr_item.data.withColumn(
                                            "country_id", F.lit(country_id))

                                dfr_item.data = dfr_item.data.withColumn(
                                    "ingest_date", F.current_timestamp())

                                bronze_write_path = self.bronze.write(
                                    country_name=dfr_item.country_name,
                                    source_name=dfr_item.source_name,
                                    table_name=dfr_item.item.table,
                                    data=dfr_item.data
                                )
                                print(
                                    f"Written data to bronze write step: {bronze_write_path}")

                            except Exception as e:
                                print(
                                    f"Failed to write data for {dfr_item.country_name}/{dfr_item.source_name}/{dfr_item.item.table}: {e}")

                    print(
                        f"\nDataLakeManager: Layer: {layer.value}, Write operation completed for {ing.__class__.__name__}.")

                    message = (
                        "*Data Ingestion Complete*\n"
                        f"*Layer:* `{ELayer.BRONZE.value}`\n"
                        f"*Name:* `{getattr(ing, 'name', ing.__class__.__name__)}`\n"
                        f"*Message:* Completed"
                    )
                    self.logger.log(message)

                elif layer.value == ELayer.SILVER.value:
                    print(
                        f"\nStarting ingestion for {ing.__class__.__name__} on SILVER layer.")
                    try:
                        dfr = ing.ingest(
                            source_layer=self.bronze,
                            destination_layer=self.silver,
                            validators=self.configuration.silver.validators,
                            transformers=self.configuration.silver.transformers,
                        )

                        if dfr:
                            for dfr_item in dfr:
                                try:
                                    silver_write_path = self.silver.write(
                                        table_name=dfr_item.item.table,
                                        partitions=dfr_item.item.partitions,
                                        data=dfr_item.data
                                    )
                                    print(
                                        f"Written data to silver write step: {silver_write_path}")

                                except Exception as e:
                                    print(
                                        f"Failed to write data for {dfr_item.country_name}/{dfr_item.source_name}/{dfr_item.item.table}: {e}")

                    except Exception as e:
                        print(
                            f"Error ingesting SILVER layer for {ing.__class__.__name__}: {e}")

                    print(
                        f"\nDataLakeManager: Layer: {layer.value}, Write operation completed for {ing.__class__.__name__}.")

                elif layer.value == ELayer.GOLD.value:
                    print(
                        f"\nStarting ingestion for {ing.__class__.__name__} on GOLD layer.")
                    try:
                        dfr = ing.ingest(
                            source_layer=self.silver,
                            destination_layer=self.gold
                        )

                        if dfr:
                            for dfr_item in dfr:
                                try:
                                    gold_write_path = self.gold.write(
                                        table_name=dfr_item.item.table,
                                        data=dfr_item.data
                                    )
                                    print(
                                        f"Written data to gold table: {dfr_item.item.table}")

                                except Exception as e:
                                    print(
                                        f"Failed to write data for table: {dfr_item.item.table}: {e}")

                    except Exception as e:
                        print(
                            f"Error ingesting GOLD layer for {ing.__class__.__name__}: {e}")

                    print(
                        f"\nDataLakeManager: Layer: {layer.value}, Write operation completed for {ing.__class__.__name__}.")
                elif layer.value == ELayer.WH.value:
                    print(
                        f"\nStarting ingestion for {ing.__class__.__name__} on WH layer.")
                    try:
                        dfr = ing.ingest(
                            source_layer=self.gold,
                            destination_layer=self.wh
                        )

                        if dfr:
                            for dfr_item in dfr:
                                try:
                                    wh_write_path = self.wh.write(
                                        table_name=dfr_item.item.table,
                                        merge_keys=dfr_item.item.upsert_columns,
                                        data=dfr_item.data
                                    )
                                    print(
                                        f"Written data to warehouse table: {dfr_item.item.table}")

                                except Exception as e:
                                    print(
                                        f"Failed to write data for table: {dfr_item.item.table}: {e}")

                    except Exception as e:
                        print(
                            f"Error ingesting GOLD layer for {ing.__class__.__name__}: {e}")

                    print(
                        f"\nDataLakeManager: Layer: {layer.value}, Write operation completed for {ing.__class__.__name__}.")

            except Exception as e:
                print(
                    f"Error during ingestion for {ing.__class__.__name__}: {e}")

    def _get_country_id(self, layer_config: ILakeConfig, country_name: str) -> str | None:
        """Return country_id from silver configuration."""
        try:
            for c in layer_config.countries:
                if c.name == country_name:
                    return c.country_id
        except:
            pass
        return None
